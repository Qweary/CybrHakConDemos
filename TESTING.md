# Testing the AI Village Workshop

Two test suites, run together via `./run_tests.sh`.

## Static suite — `test_workshop.py`

Fast string-level checks that lock in the structural invariants of the
demos: HTML parses, polish markers (S41-S44), Session 46 P0 fixes, Session
47 content authenticity, S47.5a CLAUDE CODE provider rebuild, S47.5c
streaming wiring (`callClaudeCode(sys, user, onDelta)`, `tok-count`
ticker, relay SSE branch), S47.5d output budgeting + recovery banner +
relay `?timeout=` and stall watchdog.

Runs in ~2 seconds with stdlib only. No setup required.

```
python3 test_workshop.py
```

## Browser e2e suite — `test_workshop_e2e.py`

Playwright-driven browser tests: actual page loads, console-error
capture, keyboard toggles (`Ctrl+P` pmode, `Ctrl+D` demo mode, Space
step gate), phase tooltips, `#tok-count` element presence, CLAUDE CODE
provider button click. Catches things the static suite cannot — JS
exceptions, render-time DOM breakage, broken handler wiring.

Does not make live API calls (use `test_relay_e2e.py` for that).

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
.venv-e2e/bin/pytest test_workshop_e2e.py -v
```

Or via the unified runner:

```
./run_tests.sh
```

Runs in ~10 seconds.

## End-to-end relay harness — `test_relay_e2e.py`

Drives the live relay through realistic phase sequences for forge (9
phases), combat (3 stage pairs + harden), and evolve (ARBITER →
SCULPTOR → RERUN). Uses real Claude API calls — exercises the SSE
streaming pipeline, ARG_MAX-safe stdin path, asyncio buffer headroom,
and graceful is_error recovery. ~16 minutes runtime.

Used for validating relay/streaming changes before commit. NOT part of
`run_tests.sh` because it spends real API budget.

```
# Start the relay first (in another shell):
python3 relay.py

# Then run the harness:
python3 test_relay_e2e.py
```

Exits 0 on success.

## Troubleshooting

**`.venv-e2e/bin/pytest missing`** — run the first-time setup commands above.

**`browserType.launch: Executable doesn't exist at /home/.../chromium`** —
the chromium binary wasn't installed; run `.venv-e2e/bin/playwright
install chromium`.

**Console errors during a test** — `safe_page` fixture raises at teardown
with the specific error messages. JavaScript bug somewhere in the demo;
fix the underlying issue (don't suppress).

**Hash parity fails** — n/a; the dual-layout parity check was removed
in the Phase 2 path normalization (the workshop is now its own root,
so there is only one copy to be parity-checked against). Phase 3
snapshot tests replace the underlying intent.
