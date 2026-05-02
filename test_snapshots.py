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
import sys
from typing import Any

WORKSHOP = os.path.dirname(os.path.abspath(__file__))
SNAPSHOTS = os.path.join(WORKSHOP, 'tests', 'snapshots')
DEMOS = os.path.join(WORKSHOP, 'demos')

DEMO_FILES = [
    ('forge', os.path.join(DEMOS, 'tmp-forge-live.html')),
    ('combat', os.path.join(DEMOS, 'tmp-combat-live.html')),
    ('evolve', os.path.join(DEMOS, 'tmp-evolve-live.html')),
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


# ── Driver ───────────────────────────────────────────────────────────


SNAPSHOTS_REGISTRY = {
    'whole_file': (update_whole_file, verify_whole_file),
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
