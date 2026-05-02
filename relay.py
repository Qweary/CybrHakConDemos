#!/usr/bin/env python3
"""
TMP Local Relay — bridges demo API requests to the Claude Code CLI subprocess.

Usage:
  pip install aiohttp
  python3 relay.py

Spawns `claude -p` for each request. Uses the operator's existing Claude Code
authentication (OAuth / keychain) — no separate Anthropic API key required.
The demo posts {system, user, model, max_tokens} to localhost:3001/v1/chat,
which dispatches to the JSON or SSE branch based on the Accept header.

The implementation lives under src/tmp_relay/. This file is the
attendee-facing entry point (`python3 relay.py`). Power users can also
`pip install .` and run `tmp-relay`.

Test: curl http://localhost:3001/health
"""

import asyncio
import os
import sys

# Bootstrap: make the in-tree src/tmp_relay/ package importable without
# requiring `pip install -e .`. Attendees can run `python3 relay.py`
# directly from a fresh clone. Power users who pip-install get the
# `tmp-relay` console script instead — both end up at the same code.
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, 'src'))

from aiohttp import web

from tmp_relay.claude_subprocess import claude_path
from tmp_relay.server import make_app
from tmp_relay.settings import DEFAULT_MODEL, PORT, TIMEOUT_SEC


async def main():
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


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\n[RELAY] Stopped.')
