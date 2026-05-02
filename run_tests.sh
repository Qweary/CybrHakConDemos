#!/usr/bin/env bash
# run_tests.sh — full workshop test suite (static + e2e).
#
# Runs both layers:
#   1. test_workshop.py — fast static checks (HTML parse, regex lock-ins,
#      hash parity, S46-S47.5d regression markers). ~2 sec.
#   2. test_workshop_e2e.py — Playwright browser smoke (page loads,
#      Ctrl+P/Ctrl+D toggles, phase tooltips, tok-count, CC button).
#      ~10 sec on the operator's laptop.
#
# The e2e suite uses the venv at .venv-e2e/ — set up once with:
#   python3 -m venv .venv-e2e
#   .venv-e2e/bin/pip install playwright pytest pytest-playwright
#   .venv-e2e/bin/playwright install chromium

set -euo pipefail

WORKSHOP="$(cd "$(dirname "$0")" && pwd)"
cd "$WORKSHOP"

echo "═══ Static suite (test_workshop.py) ═══"
python3 test_workshop.py
STATIC_RC=$?

echo
echo "═══ Snapshot tripwires (test_snapshots.py) ═══"
python3 test_snapshots.py
SNAP_RC=$?

echo
echo "═══ Browser e2e suite (test_workshop_e2e.py) ═══"
if [ ! -x .venv-e2e/bin/pytest ]; then
  echo "✗ .venv-e2e/bin/pytest missing — first-time setup:"
  echo "    python3 -m venv .venv-e2e"
  echo "    .venv-e2e/bin/pip install playwright pytest pytest-playwright"
  echo "    .venv-e2e/bin/playwright install chromium"
  exit 1
fi
.venv-e2e/bin/pytest test_workshop_e2e.py -q --tb=short
E2E_RC=$?

echo
if [ $STATIC_RC -eq 0 ] && [ $SNAP_RC -eq 0 ] && [ $E2E_RC -eq 0 ]; then
  echo "✅ ALL SUITES PASSED"
  exit 0
fi
echo "❌ One or more suites failed (static=$STATIC_RC snap=$SNAP_RC e2e=$E2E_RC)"
exit 1
