#!/usr/bin/env bash
# bin/start.sh — launch the workshop relay (macOS / Linux).
#
# Picks the best Python interpreter available, ensures aiohttp is
# installed, and starts the relay. Optionally opens the launcher in
# your default browser.
#
# Interpreter preference (first that works):
#   1. uv  — fastest; treats the in-tree pyproject.toml as the source
#   2. existing .venv-e2e/  — created by previous test setup
#   3. fresh .venv/ at workshop root — created on first run
#   4. system python3 (last resort; may fail on Debian/Ubuntu PEP 668)
#
# Toggles:
#   --port N         override port 3001
#   --bind ADDR      override 127.0.0.1 — DANGER, exposes relay on LAN
#   --no-browser     don't auto-open
#   --skip-checks    skip bin/doctor.sh
#
# Stop with Ctrl+C; the relay shuts down cleanly.

set -u

WORKSHOP="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKSHOP"

PORT="${TMP_RELAY_PORT:-3001}"
BIND="127.0.0.1"
OPEN_BROWSER=1
SKIP_CHECKS=0

while [ $# -gt 0 ]; do
  case "$1" in
    --port)        PORT="$2"; shift 2;;
    --bind)        BIND="$2"; shift 2;;
    --no-browser)  OPEN_BROWSER=0; shift;;
    --skip-checks) SKIP_CHECKS=1; shift;;
    -h|--help)
      sed -n '2,/^$/p' "$0" | sed 's/^# \{0,1\}//'
      exit 0;;
    *) echo "Unknown flag: $1" >&2; exit 2;;
  esac
done

if [ "$BIND" != "127.0.0.1" ] && [ "$BIND" != "localhost" ]; then
  cat >&2 <<EOF

⚠ WARNING: --bind $BIND exposes the relay beyond loopback. Anyone on
  your network who can reach this host can use your claude CLI session
  for free model calls. Make sure you know who's on the network before
  proceeding. Press Ctrl+C now to abort, or wait 5s to continue.

EOF
  sleep 5
fi

# ── Pre-flight ─────────────────────────────────────────────────────────
if [ $SKIP_CHECKS -eq 0 ]; then
  if ! "$WORKSHOP/bin/doctor.sh"; then
    echo "" >&2
    echo "✗ doctor.sh reported failures. Fix above issues or pass --skip-checks." >&2
    exit 1
  fi
fi

# ── Pick interpreter ──────────────────────────────────────────────────
PYTHON=""
LAUNCH_VIA=""

# 1. uv (preferred when available)
if command -v uv >/dev/null 2>&1; then
  echo "→ Using uv (resolved via pyproject.toml)"
  LAUNCH_VIA="uv"
fi

# 2. existing .venv-e2e/
if [ -z "$LAUNCH_VIA" ] && [ -x ".venv-e2e/bin/python3" ] && \
   .venv-e2e/bin/python3 -c 'import aiohttp' 2>/dev/null; then
  PYTHON=".venv-e2e/bin/python3"
  echo "→ Using existing .venv-e2e/ ($($PYTHON --version))"
  LAUNCH_VIA="venv"
fi

# 3. fresh .venv/
if [ -z "$LAUNCH_VIA" ]; then
  if [ -x ".venv/bin/python3" ] && .venv/bin/python3 -c 'import aiohttp' 2>/dev/null; then
    PYTHON=".venv/bin/python3"
    echo "→ Using existing .venv/ ($($PYTHON --version))"
    LAUNCH_VIA="venv"
  elif command -v python3 >/dev/null 2>&1; then
    if python3 -c 'import aiohttp' 2>/dev/null; then
      # System python has aiohttp directly
      PYTHON="python3"
      echo "→ Using system python3 ($(python3 --version)) — has aiohttp"
      LAUNCH_VIA="venv"
    else
      echo "→ Creating .venv/ and installing aiohttp..."
      python3 -m venv .venv
      .venv/bin/pip install --quiet aiohttp
      PYTHON=".venv/bin/python3"
      LAUNCH_VIA="venv"
    fi
  else
    echo "✗ no python3 found — install Python 3.10+ first" >&2
    exit 1
  fi
fi

# ── Launch ────────────────────────────────────────────────────────────
URL="http://$BIND:$PORT/"
echo ""
echo "─── Starting relay ────────────────────────────────────────"
echo "    URL:   $URL"
echo "    Bind:  $BIND"
echo "    Port:  $PORT"
echo "    Quit:  Ctrl+C"
echo "──────────────────────────────────────────────────────────"
echo ""

# Auto-open browser shortly after the relay binds. Use Python sleep+open
# combo so it works in the background without depending on `at` or
# nohup. The opener is a one-shot script that exits.
if [ $OPEN_BROWSER -eq 1 ]; then
  (sleep 1.5 && {
    if command -v xdg-open >/dev/null 2>&1; then xdg-open "$URL" >/dev/null 2>&1
    elif command -v open >/dev/null 2>&1; then open "$URL"
    fi
  }) &
fi

# --port and --bind are honored via env-var overrides understood by
# settings.py (TMP_RELAY_PORT / TMP_RELAY_BIND).
export TMP_RELAY_PORT="$PORT"
export TMP_RELAY_BIND="$BIND"

if [ "$LAUNCH_VIA" = "uv" ]; then
  exec uv run --quiet python3 relay.py
else
  exec "$PYTHON" relay.py
fi
