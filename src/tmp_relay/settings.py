"""Configuration constants for tmp_relay.

All tunables live here so a refactor caller can `from .settings import *`
or pass a Settings object around. Today the constants are module-level
for backward compatibility with the in-place relay.py shape; ARCH-14
will introduce a Settings dataclass during a follow-up cleanup.

Env vars override the literals shown below.

  TMP_RELAY_TIMEOUT_SEC      — per-call wall-clock budget for the
                               claude subprocess (default 600s).
  TMP_RELAY_SUBPROC_LIMIT    — bytes per stream-json line (default 4 MB).
                               Snapshot frames in --include-partial-messages
                               can exceed asyncio's default 64 KB.
  TMP_RELAY_MODEL            — overrides the demo's requested model.
                               Default claude-haiku-4-5 is ~3-4x faster
                               than Sonnet 4.6 and adequate for the
                               workflow-focused demos. Set to empty
                               string to honor the body-supplied model.
"""

import os
from pathlib import Path

# Bind: 127.0.0.1:PORT — the relay never listens on a network-reachable
# address by default. Phase 8 will plumb --bind/--port through cli.main().
PORT = 3001

# Static web root — the relay serves the workshop's launcher and demo HTML
# from here. Same-origin with /v1/chat eliminates the CORS surface for
# the demos and replaces the python -m http.server pattern attendees
# would otherwise be told to run (which binds 0.0.0.0 by default).
# Resolved relative to the workshop root, two levels up from this file
# (src/tmp_relay/settings.py → src/tmp_relay → src → <root>).
WEB_DIR = str(Path(__file__).resolve().parents[2] / 'web')

# Each call spawns a fresh `claude -p` subprocess. CURIE and FERMI phases on
# typical workshop hardware land at ~250-300s for the unabridged forge demo
# prompts; 600s gives enough headroom for slower laptops without making real
# stalls take forever to surface.
TIMEOUT_SEC = int(os.environ.get('TMP_RELAY_TIMEOUT_SEC', '600'))

# Per-call ?timeout=N override bounds. Recovery banner's "Continue
# waiting" can extend the budget within these limits without restarting
# the relay. Out-of-bounds values clamp silently — every chat response
# carries an X-Timeout-Used header so the caller can detect the override.
MIN_PERCALL_TIMEOUT_SEC = 60
MAX_PERCALL_TIMEOUT_SEC = 1800

# Per-line buffer limit on the subprocess StreamReader. asyncio's default is
# 64 KB, but `claude --output-format stream-json` emits assistant-message
# snapshot lines that contain the FULL accumulated content for each chunk
# — those routinely exceed 64 KB once the model produces ~3K+ tokens of
# structured output, which throws LimitOverrunError mid-stream. 4 MB gives
# enough headroom for any realistic single-call output.
SUBPROC_LIMIT = int(os.environ.get('TMP_RELAY_SUBPROC_LIMIT', str(4 * 1024 * 1024)))

# Default model overrides the demo's request. See module docstring.
DEFAULT_MODEL = os.environ.get('TMP_RELAY_MODEL', 'claude-haiku-4-5')

# Stall watcher: emit a non-fatal `warning` SSE event when no text_delta
# arrives within this window. Keeps the operator's UI from going silent
# during long thinking pauses without bailing the call.
STALL_WARN_SEC = 30

# Chunked stdin write block size. Single >64 KB writes can BrokenPipeError
# on Windows ProactorEventLoop pipes if the kernel pipe buffer fills before
# the CLI starts reading; chunking with await drain() between blocks is
# necessary on Windows and free on macOS/Linux.
STDIN_CHUNK = 32 * 1024

# Single source of truth for CORS headers. Applied by server.cors_middleware
# on every regular Response and FileResponse (static layer included). The
# SSE StreamResponse path duplicates these into its construction headers
# because aiohttp middleware runs only after the handler returns — by which
# time the SSE response has already been prepared and headers flushed.
CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Accept',
}
