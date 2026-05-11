#!/usr/bin/env bash
# bin/doctor.sh — pre-flight check for the workshop relay.
#
# Verifies the operator's machine has what it needs to run `bin/start.sh`
# and the relay. Reports each check as PASS/WARN/FAIL with a one-line fix
# suggestion. Exits 0 if all hard requirements pass, 1 otherwise.
#
# Hard requirements (FAIL exits non-zero):
#   - Python ≥ 3.10 on PATH
#   - aiohttp importable from chosen python
#   - port 3001 free (or warn if already used by what looks like a relay)
#
# Soft requirements (WARN, don't fail):
#   - claude CLI on PATH — only needed for the CLAUDE CODE provider
#   - uv available (faster than pip+venv; we'll use it if present)

set -u

WORKSHOP="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKSHOP"

# Color helpers — fall back to plain text if not a tty.
if [ -t 1 ] && command -v tput >/dev/null 2>&1; then
  C_PASS="$(tput setaf 2)"
  C_WARN="$(tput setaf 3)"
  C_FAIL="$(tput setaf 1)"
  C_INFO="$(tput setaf 6)"
  C_OFF="$(tput sgr0)"
else
  C_PASS=""; C_WARN=""; C_FAIL=""; C_INFO=""; C_OFF=""
fi

EXIT=0

pass() { printf "  ${C_PASS}✓${C_OFF} %s\n" "$1"; }
warn() { printf "  ${C_WARN}!${C_OFF} %s\n" "$1"; [ "${2-}" = "fix" ] && shift 2 && printf "      → %s\n" "$1"; }
fail() { printf "  ${C_FAIL}✗${C_OFF} %s\n" "$1"; [ "${2-}" = "fix" ] && shift 2 && printf "      → %s\n" "$1"; EXIT=1; }
info() { printf "  ${C_INFO}·${C_OFF} %s\n" "$1"; }

printf "\n${C_INFO}══${C_OFF} TMP relay doctor — workshop root: %s\n\n" "$WORKSHOP"

# ── Python ────────────────────────────────────────────────────────────
if command -v python3 >/dev/null 2>&1; then
  PY_VER="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")')"
  PY_MAJOR_MINOR="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
  PY_OK="$(python3 -c 'import sys; print("yes" if sys.version_info >= (3, 10) else "no")')"
  if [ "$PY_OK" = "yes" ]; then
    pass "Python $PY_VER ($(command -v python3))"
  else
    fail "Python $PY_VER too old; need ≥ 3.10" fix "Install Python 3.10+ — https://www.python.org/downloads/"
  fi
else
  fail "python3 not on PATH" fix "Install Python 3.10+ — https://www.python.org/downloads/"
fi

# ── aiohttp ───────────────────────────────────────────────────────────
if command -v python3 >/dev/null 2>&1; then
  if python3 -c 'import aiohttp' 2>/dev/null; then
    AIOHTTP_VER="$(python3 -c 'import aiohttp; print(aiohttp.__version__)' 2>/dev/null)"
    pass "aiohttp $AIOHTTP_VER importable from system python3"
  else
    # Maybe the e2e venv has it
    if [ -x ".venv-e2e/bin/python3" ] && .venv-e2e/bin/python3 -c 'import aiohttp' 2>/dev/null; then
      VENV_VER="$(.venv-e2e/bin/python3 -c 'import aiohttp; print(aiohttp.__version__)')"
      warn "aiohttp not in system python3 (have $VENV_VER in .venv-e2e/)"
      info "  bin/start.sh will use the .venv-e2e/ interpreter"
    else
      fail "aiohttp not importable" fix "pip install aiohttp  (or run: bin/start.sh — it'll set up a venv for you)"
    fi
  fi
fi

# ── claude CLI (soft) ─────────────────────────────────────────────────
if command -v claude >/dev/null 2>&1; then
  CLAUDE_PATH="$(command -v claude)"
  CLAUDE_VER="$(claude --version 2>/dev/null | head -1 || echo '?')"
  pass "claude CLI: $CLAUDE_VER ($CLAUDE_PATH)"
else
  warn "claude CLI not on PATH — CLAUDE CODE provider unavailable"
  info "  Other providers (OpenRouter, OR Free, Ollama, Anthropic) still work"
  info "  Install: https://docs.claude.com/claude-code"
fi

# ── port 3001 ─────────────────────────────────────────────────────────
# Use python3 socket.bind for a portable check — lsof varies across
# distros (NixOS, Alpine) and ss isn't always installed (macOS).
PORT=3001
if command -v python3 >/dev/null 2>&1; then
  PORT_FREE="$(python3 -c "
import socket
s = socket.socket()
try:
    s.bind(('127.0.0.1', $PORT))
    print('yes')
except OSError:
    print('no')
finally:
    s.close()
")"
  if [ "$PORT_FREE" = "yes" ]; then
    pass "port $PORT free"
  else
    # Probe whether it's already a healthy relay
    if command -v curl >/dev/null 2>&1 && curl -fsS "http://127.0.0.1:$PORT/health" >/dev/null 2>&1; then
      info "port $PORT already serving a healthy relay — bin/start.sh will reuse it or fail explicitly"
    else
      warn "port $PORT in use by something that isn't a relay /health responder"
      info "  free it (kill the process) or run with --port to pick a different port"
    fi
  fi
else
  info "no python3 — skipping port check"
fi

# ── uv (soft, preferred) ──────────────────────────────────────────────
if command -v uv >/dev/null 2>&1; then
  UV_VER="$(uv --version 2>/dev/null | head -1 || echo '?')"
  pass "uv $UV_VER (start.sh will prefer this over venv+pip)"
else
  info "uv not installed — start.sh will fall back to venv+pip"
  info "  optional speedup: curl -LsSf https://astral.sh/uv/install.sh | sh"
fi

# ── workshop layout sanity ────────────────────────────────────────────
for required in relay.py src/swarm_relay/cli.py web/index.html; do
  if [ -e "$required" ]; then
    pass "found $required"
  else
    fail "missing $required" fix "Run from the workshop root, not a subdirectory"
  fi
done

echo
if [ $EXIT -eq 0 ]; then
  printf "${C_PASS}══ READY${C_OFF} — run ${C_INFO}bin/start.sh${C_OFF} to launch the relay.\n\n"
else
  printf "${C_FAIL}══ NOT READY${C_OFF} — fix the items above and re-run.\n\n"
fi
exit $EXIT
