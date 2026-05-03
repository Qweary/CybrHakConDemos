#!/usr/bin/env bash
# run_tests.sh — full workshop test suite (static + snapshot + e2e).
#
# Three layers:
#   1. tests/test_workshop.py        — fast static / structural checks.
#   2. tests/test_snapshots.py       — content-drift tripwires (whole-file
#                                      hashes, per-prompt hashes + .md
#                                      round-trip, /health schema).
#   3. tests/e2e/test_browser_smoke.py — Playwright browser smoke.
#
# The live-API harness (tests/relay/test_relay_live.py, ~16 min, real
# spend) is GATED — invoked only when RUN_LIVE_RELAY=1 is set, never
# from this script.
#
# E2E venv setup (once):
#   python3 -m venv .venv-e2e
#   .venv-e2e/bin/pip install playwright pytest pytest-playwright
#   .venv-e2e/bin/playwright install chromium

set -euo pipefail

WORKSHOP="$(cd "$(dirname "$0")" && pwd)"
cd "$WORKSHOP"

echo "═══ Static suite (tests/test_workshop.py) ═══"
python3 tests/test_workshop.py
STATIC_RC=$?

echo
echo "═══ Snapshot tripwires (tests/test_snapshots.py) ═══"
python3 tests/test_snapshots.py
SNAP_RC=$?

echo
echo "═══ Relay unit tests (tests/relay/test_relay_unit.py) ═══"
if [ ! -x .venv-e2e/bin/pytest ]; then
  echo "✗ .venv-e2e/bin/pytest missing — first-time setup:"
  echo "    python3 -m venv .venv-e2e"
  echo "    .venv-e2e/bin/pip install playwright pytest pytest-playwright aiohttp"
  echo "    .venv-e2e/bin/playwright install chromium"
  exit 1
fi
.venv-e2e/bin/pytest tests/relay/test_relay_unit.py -q --tb=short
UNIT_RC=$?

echo
echo "═══ Browser e2e suite (tests/e2e/test_browser_smoke.py) ═══"
.venv-e2e/bin/pytest tests/e2e/test_browser_smoke.py -q --tb=short
E2E_RC=$?

echo
if [ $STATIC_RC -eq 0 ] && [ $SNAP_RC -eq 0 ] && [ $UNIT_RC -eq 0 ] && [ $E2E_RC -eq 0 ]; then
  echo "✅ ALL SUITES PASSED"
  exit 0
fi
echo "❌ One or more suites failed (static=$STATIC_RC snap=$SNAP_RC unit=$UNIT_RC e2e=$E2E_RC)"
exit 1
