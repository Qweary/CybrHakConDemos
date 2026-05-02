#!/usr/bin/env python3
"""
test_snapshots.py — content-drift tripwire for the refactor.

Locks the shape and content of things that the structural suite in
test_workshop.py cannot. Three independent snapshot tests live here:

  whole_file  — SHA256 of each demo HTML (catches any byte change)
  prompts     — SHA256 of every SYS_* / SYS.* prompt constant individually
                (catches a prompt edit even if surrounding HTML changes)
  health      — shape (keys + value types) of relay /health JSON

Snapshot data lives in tests/snapshots/*.json. The default run verifies
against those snapshots; `--update` regenerates them. Refactor commits
should NOT need --update — a snapshot diff is the signal that the
refactor changed observable behavior.

Exit 0 on all-pass; non-zero on any drift or missing snapshot.

Usage:
  python3 test_snapshots.py              # verify
  python3 test_snapshots.py --update     # regenerate all snapshots
  python3 test_snapshots.py --update whole_file
  python3 test_snapshots.py whole_file   # verify just one
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from typing import Any

WORKSHOP = os.path.dirname(os.path.abspath(__file__))
SNAPSHOTS = os.path.join(WORKSHOP, 'tests', 'snapshots')
WEB = os.path.join(WORKSHOP, 'web')

DEMO_FILES = [
    ('forge', os.path.join(WEB, 'forge.html')),
    ('combat', os.path.join(WEB, 'combat.html')),
    ('evolve', os.path.join(WEB, 'evolve.html')),
]

# ── Result tracking ──────────────────────────────────────────────────


results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = '') -> None:
    results.append((name, ok, detail))
    status = 'PASS' if ok else 'FAIL'
    print(f'  [{status}] {name}')
    if not ok and detail:
        print(f'         → {detail}')


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode('utf-8'))


def read_text(path: str) -> str:
    with open(path, encoding='utf-8') as f:
        return f.read()


def read_json(path: str) -> Any:
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def write_json(path: str, data: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write('\n')


# ── Snapshot 1: whole-file SHA256 ────────────────────────────────────


WHOLE_FILE_PATH = os.path.join(SNAPSHOTS, 'whole_file.json')


def collect_whole_file() -> dict[str, str]:
    out = {}
    for label, path in DEMO_FILES:
        with open(path, 'rb') as f:
            out[label] = sha256_bytes(f.read())
    return out


def update_whole_file() -> None:
    write_json(WHOLE_FILE_PATH, collect_whole_file())
    print(f'  → wrote {WHOLE_FILE_PATH}')


def verify_whole_file() -> None:
    print('\n── whole_file: demo HTML SHA256 ───────────────────────────')
    if not os.path.exists(WHOLE_FILE_PATH):
        check('whole_file snapshot exists', False,
              f'no snapshot at {WHOLE_FILE_PATH} — run with --update to create')
        return
    expected = read_json(WHOLE_FILE_PATH)
    actual = collect_whole_file()
    for label in sorted(set(expected) | set(actual)):
        if label not in expected:
            check(f'{label}: in snapshot', False, 'demo present in repo but not in snapshot')
        elif label not in actual:
            check(f'{label}: file present', False, 'snapshot has entry but demo file missing')
        else:
            ok = expected[label] == actual[label]
            check(f'{label}: SHA256 matches', ok,
                  f'expected {expected[label][:12]}…, got {actual[label][:12]}…' if not ok else '')


# ── Snapshot 2: per-prompt SHA256 ────────────────────────────────────


PROMPTS_PATH = os.path.join(SNAPSHOTS, 'prompts.json')


def _scan_template(text: str, start: int) -> tuple[str, int] | None:
    """From position `start` (just after the opening backtick), return
    (body, end_index_exclusive). Walks the string respecting escaped
    characters (\\\\, \\`) so that an escaped backtick doesn't prematurely
    terminate the literal. Returns None if no closing backtick is found.

    Does NOT track ${...} interpolation depth — our prompts use simple
    interpolations with no nested template literals, so first unescaped
    backtick is the end. If a future prompt embeds a nested template,
    revisit this.
    """
    i = start
    while i < len(text):
        ch = text[i]
        if ch == '\\' and i + 1 < len(text):
            i += 2
            continue
        if ch == '`':
            return text[start:i], i + 1
        i += 1
    return None


def _extract_advisors_block(text: str) -> dict[str, str]:
    """SYS.ADVISORS = { NEUTRON: `...`, SCINTILLATOR: `...`, ... } —
    find the brace-balanced block, then extract each entry. Skips
    backtick contents while balancing braces."""
    m = re.search(r'SYS\.ADVISORS\s*=\s*\{', text)
    if not m:
        return {}
    i = m.end()
    depth = 1
    n = len(text)
    while i < n and depth > 0:
        ch = text[i]
        if ch == '`':
            tpl = _scan_template(text, i + 1)
            if tpl is None:
                return {}
            i = tpl[1]
            continue
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                break
        i += 1
    if depth != 0:
        return {}
    block = text[m.end():i]
    out: dict[str, str] = {}
    for entry in re.finditer(r'(\w+)\s*:\s*`', block):
        body = _scan_template(block, entry.end())
        if body is None:
            continue
        out[f'SYS.ADVISORS.{entry.group(1)}'] = body[0]
    return out


def extract_prompts(text: str) -> dict[str, str]:
    """Extract every SYS_* / SYS.* template literal from a demo HTML
    body. Returns a dict mapping canonical name → prompt body."""
    out: dict[str, str] = {}

    # const SYS_X = `...`   or   const SYS_X = (args) => `...`
    for m in re.finditer(
        r'const\s+(SYS_\w+)\s*=\s*(?:\([^)]*\)\s*=>\s*)?`',
        text,
    ):
        body = _scan_template(text, m.end())
        if body is not None:
            out[m.group(1)] = body[0]

    # SYS.X = `...`   (excludes SYS.ADVISORS = {...} which has `=` followed by `{`)
    for m in re.finditer(r'SYS\.(\w+)\s*=\s*`', text):
        body = _scan_template(text, m.end())
        if body is not None:
            out[f'SYS.{m.group(1)}'] = body[0]

    # SYS.ADVISORS = { NAME: `...`, ... }
    out.update(_extract_advisors_block(text))

    return out


def collect_prompts() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for label, path in DEMO_FILES:
        text = read_text(path)
        prompts = extract_prompts(text)
        out[label] = {name: sha256_text(body) for name, body in prompts.items()}
    return out


def update_prompts() -> None:
    write_json(PROMPTS_PATH, collect_prompts())
    snap = collect_prompts()
    counts = ', '.join(f'{label}={len(v)}' for label, v in snap.items())
    print(f'  → wrote {PROMPTS_PATH} ({counts})')


def verify_prompts() -> None:
    print('\n── prompts: per-prompt SHA256 ─────────────────────────────')
    if not os.path.exists(PROMPTS_PATH):
        check('prompts snapshot exists', False,
              f'no snapshot at {PROMPTS_PATH} — run with --update to create')
        return
    expected = read_json(PROMPTS_PATH)
    actual = collect_prompts()
    for label in sorted(set(expected) | set(actual)):
        exp = expected.get(label, {})
        act = actual.get(label, {})
        # Count check first — catches accidentally-deleted prompt early.
        check(f'{label}: prompt count matches ({len(exp)})',
              len(exp) == len(act),
              f'expected {len(exp)} prompts, found {len(act)}: '
              f'missing={sorted(set(exp) - set(act))[:3]} '
              f'extra={sorted(set(act) - set(exp))[:3]}'
              if len(exp) != len(act) else '')
        # Then individual hashes — narrows down which prompt drifted.
        for name in sorted(set(exp) | set(act)):
            if name not in exp:
                check(f'{label}.{name}: in snapshot', False, 'new prompt — run --update if intentional')
            elif name not in act:
                check(f'{label}.{name}: still present', False, 'prompt was deleted')
            else:
                ok = exp[name] == act[name]
                check(f'{label}.{name}: SHA256 matches', ok,
                      f'prompt body changed (was {exp[name][:12]}…, now {act[name][:12]}…)' if not ok else '')


# ── Snapshot 3: relay /health response schema ────────────────────────


HEALTH_PATH = os.path.join(SNAPSHOTS, 'relay_health.json')
RELAY_PORT = 3001  # current hardcode in relay.py; Phase 5 makes this configurable
RELAY_PY = os.path.join(WORKSHOP, 'relay.py')

_TYPE_NAMES: dict[str, type] = {
    'str': str, 'bool': bool, 'int': int, 'float': float,
    'dict': dict, 'list': list, 'NoneType': type(None),
}


def _interpreter_has_aiohttp(interp: str) -> bool:
    try:
        r = subprocess.run(
            [interp, '-c', 'import aiohttp'],
            capture_output=True, timeout=5,
        )
        return r.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def _pick_relay_interpreter() -> str | None:
    """Find a python that can run the relay. Tries the current
    interpreter first, then `.venv-e2e/bin/python3` (the interpreter
    the workshop install instructions create)."""
    candidates = [sys.executable, os.path.join(WORKSHOP, '.venv-e2e', 'bin', 'python3')]
    for interp in candidates:
        if interp and os.path.exists(interp) and _interpreter_has_aiohttp(interp):
            return interp
    return None


def _start_relay_subprocess(interp: str) -> tuple[subprocess.Popen | None, str]:
    """Spawn the relay; return (Popen, '') once /health responds, or
    (None, stderr_excerpt) if the relay crashed or didn't come up
    within 5 seconds."""
    proc = subprocess.Popen(
        [interp, RELAY_PY],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    deadline = time.time() + 5.0
    while time.time() < deadline:
        if proc.poll() is not None:
            err = (proc.stderr.read() if proc.stderr else b'').decode('utf-8', 'replace')
            return None, err.strip()[-500:]
        try:
            urllib.request.urlopen(
                f'http://127.0.0.1:{RELAY_PORT}/health', timeout=0.5,
            ).read()
            return proc, ''
        except urllib.error.URLError:
            time.sleep(0.1)
    proc.terminate()
    return None, f'relay did not respond within 5s on port {RELAY_PORT}'


def _stop_relay_subprocess(proc: subprocess.Popen) -> None:
    proc.terminate()
    try:
        proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()


def _try_existing_relay() -> tuple[int, dict[str, Any]] | None:
    """If a relay is already serving on 3001, hit it and return the
    response. Returns None if nothing answers (we don't conflate "port
    bound but stale" with "real relay running")."""
    try:
        r = urllib.request.urlopen(
            f'http://127.0.0.1:{RELAY_PORT}/health', timeout=1.0,
        )
        return r.getcode(), json.loads(r.read().decode('utf-8'))
    except (urllib.error.URLError, ConnectionError):
        return None


def _capture_health() -> tuple[int, dict[str, Any]] | tuple[None, str]:
    """Capture (status_code, response_dict). Tries an already-running
    relay first; otherwise spawns one. Returns (None, reason) on
    failure."""
    existing = _try_existing_relay()
    if existing is not None:
        return existing

    interp = _pick_relay_interpreter()
    if interp is None:
        return None, (
            'no python interpreter with aiohttp found; tried '
            f'{sys.executable} and .venv-e2e/bin/python3 — '
            'install with: pip install aiohttp  (or set up the e2e venv per TESTING.md)'
        )
    proc, err = _start_relay_subprocess(interp)
    if proc is None:
        return None, f'relay subprocess failed: {err}'
    try:
        r = urllib.request.urlopen(
            f'http://127.0.0.1:{RELAY_PORT}/health', timeout=2.0,
        )
        return r.getcode(), json.loads(r.read().decode('utf-8'))
    except Exception as e:
        return None, f'relay started but /health failed: {e}'
    finally:
        _stop_relay_subprocess(proc)


def _infer_schema(payload: dict[str, Any]) -> dict[str, Any]:
    """Infer a snapshot schema from a captured response. Treats the
    `claude_binary_path` key as nullable since its value depends on
    whether the claude CLI is installed on the snapshotting machine."""
    schema: dict[str, Any] = {}
    for k, v in payload.items():
        nullable = (k == 'claude_binary_path')  # may be None on machines without claude
        schema[k] = {'type': type(v).__name__, 'nullable': nullable}
    return schema


def update_health() -> None:
    code, payload = _capture_health()
    if code is None:
        print(f'  ✗ cannot capture: {payload}', file=sys.stderr)
        sys.exit(1)
    snap = {
        'endpoint': '/health',
        'method': 'GET',
        'response': {'status_code': code, 'schema': _infer_schema(payload)},
    }
    write_json(HEALTH_PATH, snap)
    keys = ', '.join(sorted(snap['response']['schema']))
    print(f'  → wrote {HEALTH_PATH} (keys: {keys})')


def verify_health() -> None:
    print('\n── health: relay /health response schema ──────────────────')
    if not os.path.exists(HEALTH_PATH):
        check('health snapshot exists', False,
              f'no snapshot at {HEALTH_PATH} — run with --update to create')
        return
    snap = read_json(HEALTH_PATH)
    expected_code = snap['response']['status_code']
    expected_schema = snap['response']['schema']

    code, payload = _capture_health()
    if code is None:
        check('relay /health reachable', False, payload)
        return
    check(f'/health status code is {expected_code}', code == expected_code,
          f'got {code}')
    if not isinstance(payload, dict):
        check('/health body is a JSON object', False,
              f'got {type(payload).__name__}')
        return
    check('/health body is a JSON object', True)

    expected_keys = set(expected_schema)
    actual_keys = set(payload)
    missing = expected_keys - actual_keys
    extra = actual_keys - expected_keys
    check('/health keys: no missing', not missing,
          f'missing keys: {sorted(missing)}' if missing else '')
    check('/health keys: no extra', not extra,
          f'extra keys (would silently leak data): {sorted(extra)}' if extra else '')

    for key in sorted(expected_keys & actual_keys):
        spec = expected_schema[key]
        expected_type = _TYPE_NAMES.get(spec['type'])
        nullable = spec.get('nullable', False)
        value = payload[key]
        if value is None and nullable:
            check(f'/health[{key}]: type ok ({spec["type"]} or null)', True)
            continue
        if expected_type is None:
            check(f'/health[{key}]: type ok', False,
                  f'unknown type name in snapshot: {spec["type"]!r}')
            continue
        ok = isinstance(value, expected_type)
        check(f'/health[{key}]: type matches {spec["type"]}', ok,
              f'got {type(value).__name__}={value!r}' if not ok else '')


# ── Driver ───────────────────────────────────────────────────────────


SNAPSHOTS_REGISTRY = {
    'whole_file': (update_whole_file, verify_whole_file),
    'prompts': (update_prompts, verify_prompts),
    'health': (update_health, verify_health),
}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--update', action='store_true',
                   help='regenerate snapshots instead of verifying')
    p.add_argument('which', nargs='*', choices=list(SNAPSHOTS_REGISTRY),
                   help='which snapshot(s) to operate on; default = all')
    args = p.parse_args(argv)

    selected = args.which or list(SNAPSHOTS_REGISTRY)
    for name in selected:
        update, verify = SNAPSHOTS_REGISTRY[name]
        (update if args.update else verify)()

    if args.update:
        return 0

    print()
    print('─' * 60)
    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    failed = total - passed
    if failed == 0:
        print(f'  ALL {total} SNAPSHOT TESTS PASSED')
        return 0
    print(f'  {passed}/{total} passed  |  {failed} FAILED')
    print()
    print('  Failed snapshots:')
    for name, ok, detail in results:
        if not ok:
            print(f'    ✗ {name}')
            if detail:
                print(f'      {detail}')
    print()
    print('  If the change is intentional, run:')
    print('    python3 test_snapshots.py --update')
    return 1


if __name__ == '__main__':
    sys.exit(main())
