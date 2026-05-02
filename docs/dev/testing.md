# Testing the AI Village Workshop

Three suites, run together via `./run_tests.sh`. A fourth (live-API)
harness exists for relay regressions and is invoked manually.

```
tests/
├── test_workshop.py              static / structural checks         ← suite 1
├── test_snapshots.py             content-drift tripwires             ← suite 2
├── conftest.py                   shared pytest fixtures
├── e2e/
│   └── test_browser_smoke.py     Playwright browser smoke            ← suite 3
└── relay/
    ├── test_relay_unit.py        direct unit tests + fake claude     ← (Phase 7c)
    └── test_relay_live.py        real-claude harness — manual only   ← suite 4
```

## Suite 1 — Static (`tests/test_workshop.py`)

Fast string-level checks that lock in structural invariants of the
demos: HTML parses, polish markers, S46 P0 fixes, Session 47 content
authenticity, S47.5a CLAUDE CODE provider rebuild, S47.5c streaming
wiring (`callClaudeCode(sys, user, onDelta)`, `tok-count` ticker, relay
SSE branch), S47.5d output budgeting + recovery banner + relay
`?timeout=` and stall watchdog.

~2 seconds, stdlib only, no setup required.

```
python3 tests/test_workshop.py
```

## Suite 2 — Snapshots (`tests/test_snapshots.py`)

Content-drift tripwires for the refactor:

- **whole_file** — SHA256 of each demo HTML
- **prompts** — SHA256 of every `SYS_*` / `SYS.*` constant individually,
  PLUS round-trip check that the derived `web/assets/prompts/**/*.md`
  files match the inline constants byte-for-byte
- **health** — relay `/health` JSON shape (keys + types + nullability),
  spawning the relay subprocess to capture the actual response

Snapshot data lives under `tests/snapshots/`. Verify mode runs by
default; regenerate with `--update` when an intentional change lands.

```
python3 tests/test_snapshots.py              # verify
python3 tests/test_snapshots.py --update     # regenerate all
python3 tests/test_snapshots.py --update prompts   # one snapshot
```

## Suite 3 — Browser e2e (`tests/e2e/test_browser_smoke.py`)

Playwright-driven browser tests: actual page loads, console-error
capture, keyboard toggles (`Ctrl+P` pmode, `Ctrl+D` demo mode, Space
step gate), phase tooltips, `#tok-count` element presence, CLAUDE CODE
provider button click. Catches things the static suite cannot — JS
exceptions, render-time DOM breakage, broken handler wiring.

Does **not** make live API calls. Use suite 4 for that.

### First-time setup (~30 sec download)

```
python3 -m venv .venv-e2e
.venv-e2e/bin/pip install playwright pytest pytest-playwright
.venv-e2e/bin/playwright install chromium
```

The venv lives in `.venv-e2e/` (gitignored). 27 tests across 3 demos
× 9 checks each.

### Running

```
.venv-e2e/bin/pytest tests/e2e/test_browser_smoke.py -v
```

Or via the unified runner:

```
./run_tests.sh
```

~10 seconds.

## Suite 4 — Live relay harness (`tests/relay/test_relay_live.py`) — manual only

Drives the live relay through realistic phase sequences for forge (9
phases), combat (3 stage pairs + harden), and evolve (ARBITER →
SCULPTOR → RERUN). Uses **real Claude API calls** — exercises the SSE
streaming pipeline, ARG_MAX-safe stdin path, asyncio buffer headroom,
and graceful `is_error` recovery. ~16 minutes runtime.

Used for validating relay/streaming changes before commit. **NOT part
of `run_tests.sh`** — it spends real API budget. Pytest does not
discover any test functions in this file (it has only `main()`), so
`pytest tests/` collection will not invoke it accidentally either.

```
# Start the relay first (in another shell):
python3 relay.py

# Then run the harness manually:
python3 tests/relay/test_relay_live.py
```

Exits 0 on success.

## Troubleshooting

**`.venv-e2e/bin/pytest missing`** — run the first-time setup commands above.

**`browserType.launch: Executable doesn't exist at /home/.../chromium`** —
the chromium binary wasn't installed; run `.venv-e2e/bin/playwright
install chromium`.

**On NixOS, Playwright's vendored chromium fails to load `libstdc++`/`libglib`** —
this is a known interaction between Playwright wheels and NixOS's lack
of a global ld path. Workarounds: use `nix-ld` with the right libs in
`programs.nix-ld.libraries`, run inside a Docker/devcontainer, or use
the system chromium via Playwright's `executable_path`. Phase 8 will
ship a flake with a properly-wrapped chromium.

**Console errors during a test** — `safe_page` fixture raises at teardown
with the specific error messages. JavaScript bug somewhere in the demo;
fix the underlying issue (don't suppress).

**Snapshot drift** — if a snapshot fails after an intentional change,
regenerate with `python3 tests/test_snapshots.py --update <name>`.
Without `<name>`, all snapshots regenerate. Always commit the regenerated
JSON alongside the source change so reviewers see the diff.

**Hash parity fails** — n/a; the dual-layout parity check was removed
in the Phase 2 path normalization. Phase 3 snapshot tests replace the
underlying intent.
