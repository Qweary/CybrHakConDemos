"""Command-line entry point for tmp_relay.

Two callable surfaces:
  serve()  — async; the long-running coroutine. Use this if you're
             embedding the relay inside another asyncio program.
  main()   — sync; wraps serve() with asyncio.run + KeyboardInterrupt
             handling. This is what `tmp-relay` (the console script)
             and `relay.py` (the workshop-root shim) both call.

Bind is hardcoded to 127.0.0.1 today — Phase 8 will plumb --bind /
--port through here when the init scripts land.
"""

from __future__ import annotations

import asyncio

from aiohttp import web

from .claude_subprocess import claude_path
from .server import make_app
from .settings import DEFAULT_MODEL, PORT, TIMEOUT_SEC


async def serve():
    """Build the app, bind 127.0.0.1:PORT, log a startup banner, and
    await forever. Cancellation (KeyboardInterrupt at the main()
    boundary) shuts down cleanly."""
    app = make_app()

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', PORT)
    await site.start()

    binary = claude_path()
    if binary:
        print(f'[RELAY] claude CLI: {binary}')
    else:
        print('[RELAY] WARNING: claude CLI not found on PATH — install Claude Code before running demos.')
    print(f'[RELAY] Model: {DEFAULT_MODEL or "(demo-supplied)"} (override with TMP_RELAY_MODEL=...)')
    print(f'[RELAY] Per-call timeout: {TIMEOUT_SEC}s (override with TMP_RELAY_TIMEOUT_SEC=...)')
    print(f'[RELAY] Listening on http://localhost:{PORT}')
    print(f'[RELAY] Demos:   http://localhost:{PORT}/  (forge.html, combat.html, evolve.html)')
    print(f'[RELAY] Test:    curl http://localhost:{PORT}/health')
    print('[RELAY] Ctrl+C to stop')

    await asyncio.Event().wait()


def main():
    """Sync entry point for console_scripts and the relay.py shim."""
    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        print('\n[RELAY] Stopped.')


if __name__ == '__main__':
    main()
