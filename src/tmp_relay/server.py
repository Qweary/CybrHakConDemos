"""HTTP surface for tmp_relay.

Owns:
  - Middlewares (cors_middleware, dotfile_filter)
  - Handlers (handle_chat for POST /v1/chat, handle_health, handle_index,
    handle_chat_get for the GET /v1/chat 405, handle_options for CORS)
  - Helpers (per_call_timeout, chat_response)
  - make_app() factory that wires everything onto an aiohttp Application
    with the static layer mounted at '/' from settings.WEB_DIR.

The SSE branch lives in sse.py — handle_chat dispatches to it when the
request carries `Accept: text/event-stream`.
"""

from __future__ import annotations

import asyncio
import json
import os

from aiohttp import web

from .claude_subprocess import build_args, claude_path
from .settings import (
    CORS_HEADERS,
    DEFAULT_MODEL,
    MAX_PERCALL_TIMEOUT_SEC,
    MIN_PERCALL_TIMEOUT_SEC,
    SUBPROC_LIMIT,
    TIMEOUT_SEC,
    WEB_DIR,
)
from .sse import handle_chat_sse


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


def chat_response(response, timeout):
    """Stamp the effective per-call timeout on a chat response so a
    caller can detect when their `?timeout=N` was clamped (FRG-07).
    CORS headers are added by cors_middleware."""
    response.headers['X-Timeout-Used'] = str(timeout)
    return response


def per_call_timeout(request) -> int:
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


async def handle_chat(request):
    """POST /v1/chat. Dispatches to the SSE branch when the request
    carries Accept: text/event-stream; otherwise runs the JSON path
    inline (subprocess.communicate, return {"content": ...})."""
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
    # agent prompt — the slow path noted at the top of the package).
    # Sending whitespace would otherwise pass a degraded prompt that
    # subtly perturbs model output. To explicitly request the CLI default,
    # callers omit the field entirely; same effect.
    system = (body.get('system') or '').strip()
    user = body.get('user', '')
    model = DEFAULT_MODEL or body.get('model', 'claude-haiku-4-5')
    timeout = per_call_timeout(request)

    accept = request.headers.get('Accept', '')
    if 'text/event-stream' in accept:
        return await handle_chat_sse(request, binary, system, user, model, timeout)

    args = build_args(binary, system, model, streaming=False)

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
            return chat_response(web.json_response(
                {'error': f'claude CLI timeout ({timeout}s)'}, status=504
            ), timeout)

        if proc.returncode != 0:
            err = (stderr.decode('utf-8', errors='replace').strip()
                   or f'claude exited with code {proc.returncode}')
            return chat_response(web.json_response({'error': err}, status=502), timeout)

        try:
            data = json.loads(stdout.decode('utf-8', errors='replace'))
        except json.JSONDecodeError:
            return chat_response(web.json_response(
                {'error': 'claude returned non-JSON output (run `claude --version` to confirm CLI version supports --output-format json)'},
                status=502
            ), timeout)

        content = data.get('result')
        if content is None:
            return chat_response(web.json_response(
                {'error': f'claude JSON missing "result" field: {list(data.keys())}'},
                status=502
            ), timeout)
        return chat_response(web.json_response({'content': content}), timeout)
    except FileNotFoundError:
        return chat_response(web.json_response(
            {'error': 'Claude Code CLI not found on PATH. Install Claude Code to use this provider.'},
            status=500
        ), timeout)
    except Exception as e:
        return web.json_response({'error': str(e)}, status=502)


def make_app() -> web.Application:
    """Build the aiohttp Application with all routes and middlewares
    wired. cli.main() owns the runner/site lifecycle."""
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
    return app
