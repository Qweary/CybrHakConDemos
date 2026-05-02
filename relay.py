#!/usr/bin/env python3
"""
TMP Local Relay — bridges demo API requests to the Claude Code CLI subprocess.

Usage:
  pip install aiohttp
  python3 relay.py

Spawns `claude -p` for each request. Uses the operator's existing Claude Code
authentication (OAuth / keychain) — no separate Anthropic API key required.
The demo posts {system, user, model, max_tokens} to localhost:3001/v1/chat.

Two response modes:
  - Default JSON: returns {"content": "..."} when the subprocess finishes.
    Used by `/health` curl checks and any client that doesn't opt into SSE.
  - Streaming SSE: when the request includes `Accept: text/event-stream`,
    relay forwards `claude -p --output-format stream-json --include-partial-messages`
    NDJSON frames as Server-Sent Events. Each text_delta becomes
    `data: {"delta": "<chunk>"}\n\n`; the final aggregate becomes
    `data: {"done": true, "content": "<full result>"}\n\n`. Errors and
    timeouts arrive as `data: {"error": "<msg>"}\n\n`.

Prompt routing:
  - The demo's `system` field is passed as `--system-prompt` to override
    Claude Code's default agent system prompt. Without this override, every
    call carries the full Claude-Code-as-agent context (tool harness,
    permission prompts, etc.) which slows responses 3-5x and isn't relevant
    to demo completions.
  - The demo's `user` field is passed as the `-p` positional prompt.
  - Model defaults to claude-haiku-4-5 (fast enough for live demo pacing).
    Override globally via TMP_RELAY_MODEL env var.

Test: curl http://localhost:3001/health
"""
import asyncio
import json
import os
import sys

# Bootstrap: make the in-tree src/tmp_relay/ package importable without
# requiring `pip install -e .`. Attendees can run `python3 relay.py`
# directly from a fresh clone. Power users who pip-install get the
# `tmp-relay` console script instead — both end up at the same code.
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, 'src'))

from aiohttp import web

from tmp_relay.claude_subprocess import build_args as _build_args, claude_path
from tmp_relay.settings import (
    CORS_HEADERS,
    PORT,
    WEB_DIR,
    TIMEOUT_SEC,
    MIN_PERCALL_TIMEOUT_SEC,
    MAX_PERCALL_TIMEOUT_SEC,
    SUBPROC_LIMIT,
    DEFAULT_MODEL,
)
from tmp_relay.sse import handle_chat_sse as _handle_chat_sse


@web.middleware
async def cors_middleware(request, handler):
    """Inject CORS headers on every non-SSE response. Composes with
    dotfile_filter — list this OUTER (first in the middlewares=[] tuple)
    so that even early-return 404s from dotfile_filter come back
    through here and pick up the headers."""
    response = await handler(request)
    for k, v in CORS_HEADERS.items():
        response.headers[k] = v
    return response


def _chat_response(response, timeout):
    """Stamp the effective per-call timeout on a chat response so a
    caller can detect when their `?timeout=N` was clamped (FRG-07).
    CORS headers are added by cors_middleware."""
    response.headers['X-Timeout-Used'] = str(timeout)
    return response


async def handle_options(request):
    return web.Response(status=204)


async def handle_chat_get(request):
    """Explicit 405 for `GET /v1/chat`. Without this, an attendee who
    types the URL into a browser hits the static catch-all and sees a
    confusing "404 Not Found" instead of "this endpoint is POST-only."
    """
    return web.Response(
        status=405,
        text='POST a JSON body to /v1/chat. See docs/dev/testing.md.',
        headers={'Allow': 'POST, OPTIONS'},
    )


@web.middleware
async def dotfile_filter(request, handler):
    """Block any request whose path contains a dotfile segment. Static
    handler serves dotfiles by default, which would expose a stray
    .env / .git / .DS_Store dropped into web/. Cheaper than wrapping
    aiohttp's StaticResource."""
    for segment in request.path.split('/'):
        if segment.startswith('.') and segment not in ('', '.'):
            return web.Response(status=404, text='Not Found')
    return await handler(request)


async def handle_health(request):
    binary = claude_path()
    return web.json_response({
        'status': 'ok',
        'claude_binary_present': bool(binary),
        'claude_binary_path': binary,
    })


async def handle_index(request):
    """GET / serves the web/index.html launcher. aiohttp's add_static
    doesn't auto-serve index.html for directory roots, so this is a
    small explicit shim."""
    path = os.path.join(WEB_DIR, 'index.html')
    if not os.path.isfile(path):
        return web.Response(
            status=404,
            text=(f'web/index.html not found at {path}. Open a specific '
                  f'demo instead, e.g. /forge.html'),
        )
    return web.FileResponse(path)


def _per_call_timeout(request) -> int:
    """Honor `?timeout=N` query param so a recovery banner's 'Continue
    waiting' button can extend the budget for one specific call without
    restarting the relay. Clamped to [MIN, MAX]; the X-Timeout-Used
    response header always reports the effective value so a caller can
    notice when their override was overridden."""
    raw = request.rel_url.query.get('timeout')
    if not raw:
        return TIMEOUT_SEC
    try:
        n = int(raw)
    except ValueError:
        return TIMEOUT_SEC
    return max(MIN_PERCALL_TIMEOUT_SEC, min(MAX_PERCALL_TIMEOUT_SEC, n))


async def handle_chat(request):
    try:
        body = await request.json()
    except Exception:
        return web.json_response({'error': 'Invalid JSON body'}, status=400)

    binary = claude_path()
    if not binary:
        return web.json_response(
            {'error': 'Claude Code CLI not found on PATH. Install Claude Code to use this provider.'},
            status=500
        )

    # Normalize system at the boundary. Empty string and whitespace-only
    # both mean "omit the --system-prompt flag" (CLI uses its default
    # agent prompt — the slow path noted at the top of this module).
    # Sending whitespace would otherwise pass a degraded prompt that
    # subtly perturbs model output. To explicitly request the CLI default,
    # callers omit the field entirely; same effect.
    system = (body.get('system') or '').strip()
    user = body.get('user', '')
    model = DEFAULT_MODEL or body.get('model', 'claude-haiku-4-5')
    timeout = _per_call_timeout(request)

    accept = request.headers.get('Accept', '')
    if 'text/event-stream' in accept:
        return await _handle_chat_sse(request, binary, system, user, model, timeout)

    args = _build_args(binary, system, model, streaming=False)

    try:
        proc = await asyncio.create_subprocess_exec(
            *args,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            limit=SUBPROC_LIMIT,
        )
        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(input=user.encode('utf-8')), timeout=timeout
            )
        except asyncio.TimeoutError:
            try:
                proc.kill()
            except ProcessLookupError:
                pass
            return _chat_response(web.json_response(
                {'error': f'claude CLI timeout ({timeout}s)'}, status=504
            ), timeout)

        if proc.returncode != 0:
            err = (stderr.decode('utf-8', errors='replace').strip()
                   or f'claude exited with code {proc.returncode}')
            return _chat_response(web.json_response({'error': err}, status=502), timeout)

        try:
            data = json.loads(stdout.decode('utf-8', errors='replace'))
        except json.JSONDecodeError:
            return _chat_response(web.json_response(
                {'error': 'claude returned non-JSON output (run `claude --version` to confirm CLI version supports --output-format json)'},
                status=502
            ), timeout)

        content = data.get('result')
        if content is None:
            return _chat_response(web.json_response(
                {'error': f'claude JSON missing "result" field: {list(data.keys())}'},
                status=502
            ), timeout)
        return _chat_response(web.json_response({'content': content}), timeout)
    except FileNotFoundError:
        return _chat_response(web.json_response(
            {'error': 'Claude Code CLI not found on PATH. Install Claude Code to use this provider.'},
            status=500
        ), timeout)
    except Exception as e:
        return web.json_response({'error': str(e)}, status=502)



async def main():
    # cors_middleware OUTER so dotfile_filter's early 404s come back through
    # it and pick up CORS headers. Order matters: aiohttp runs middlewares
    # in registration order; first-listed is outermost.
    app = web.Application(middlewares=[cors_middleware, dotfile_filter])
    app.router.add_route('OPTIONS', '/{path_info:.*}', handle_options)
    app.router.add_get('/health', handle_health)
    app.router.add_post('/v1/chat', handle_chat)
    # Friendly 405 for browser-typed GET /v1/chat (otherwise the static
    # catch-all swallows it as a confusing 404).
    app.router.add_get('/v1/chat', handle_chat_get)
    # GET / serves the launcher; static files (forge.html, combat.html,
    # evolve.html, future assets/) are served from web/ as a catch-all.
    # Exact-match routes above take precedence over the static prefix.
    app.router.add_get('/', handle_index)
    if os.path.isdir(WEB_DIR):
        app.router.add_static('/', WEB_DIR, show_index=False)

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
