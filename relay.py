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
import shutil
from aiohttp import web

PORT = 3001
# Static web root — relay serves the workshop's launcher and demo HTML
# from here. Same-origin with /v1/chat eliminates the CORS surface for
# the demos and replaces the python -m http.server pattern attendees
# would otherwise be told to run (which binds 0.0.0.0 by default).
WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web')
# Each call spawns a fresh `claude -p` subprocess. CURIE and FERMI phases on
# typical workshop hardware land at ~250-300s for the unabridged forge demo
# prompts; 600s gives enough headroom for slower laptops without making real
# stalls take forever to surface. Override via TMP_RELAY_TIMEOUT_SEC.
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
# Default model overrides the demo's request. Haiku 4.5 is ~3-4x faster
# than Sonnet 4.6 and adequate for the workflow-focused demo. Operators
# who want max-quality output can set TMP_RELAY_MODEL=claude-sonnet-4-6.
# Set to empty string to honor whatever model the demo requests.
DEFAULT_MODEL = os.environ.get('TMP_RELAY_MODEL', 'claude-haiku-4-5')


def cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


def _chat_response(response, timeout):
    """Stamp the effective per-call timeout on a chat response so a
    caller can detect when their `?timeout=N` was clamped (FRG-07)."""
    response.headers['X-Timeout-Used'] = str(timeout)
    return cors(response)


def claude_path():
    return shutil.which('claude')


async def handle_options(request):
    return cors(web.Response(status=204))


async def handle_chat_get(request):
    """Explicit 405 for `GET /v1/chat`. Without this, an attendee who
    types the URL into a browser hits the static catch-all and sees a
    confusing "404 Not Found" instead of "this endpoint is POST-only."
    """
    return cors(web.Response(
        status=405,
        text='POST a JSON body to /v1/chat. See docs/dev/testing.md.',
        headers={'Allow': 'POST, OPTIONS'},
    ))


@web.middleware
async def dotfile_filter(request, handler):
    """Block any request whose path contains a dotfile segment. Static
    handler serves dotfiles by default, which would expose a stray
    .env / .git / .DS_Store dropped into web/. Cheaper than wrapping
    aiohttp's StaticResource."""
    for segment in request.path.split('/'):
        if segment.startswith('.') and segment not in ('', '.'):
            return cors(web.Response(status=404, text='Not Found'))
    return await handler(request)


async def handle_health(request):
    binary = claude_path()
    return cors(web.json_response({
        'status': 'ok',
        'claude_binary_present': bool(binary),
        'claude_binary_path': binary,
    }))


async def handle_index(request):
    """GET / serves the web/index.html launcher. aiohttp's add_static
    doesn't auto-serve index.html for directory roots, so this is a
    small explicit shim."""
    path = os.path.join(WEB_DIR, 'index.html')
    if not os.path.isfile(path):
        return cors(web.Response(
            status=404,
            text=(f'web/index.html not found at {path}. Open a specific '
                  f'demo instead, e.g. /forge.html'),
        ))
    return cors(web.FileResponse(path))


def _build_args(binary, system, model, streaming):
    # --tools ""               : strip the entire built-in tool set so the
    #                            model isn't reasoning about Read/Write/Bash/
    #                            WebSearch/etc. on every call. Cuts input
    #                            from ~30k cached tokens to ~3k.
    # --disable-slash-commands : skip skill/slash-command resolution.
    # --setting-sources ""     : skip CLAUDE.md auto-discovery and hooks.
    # Together these turn `claude -p` into a thin LLM-completion endpoint
    # rather than a full Claude-Code-as-agent invocation.
    #
    # The USER prompt is piped via stdin (not -p arg) — by Phase 3 the
    # accumulated context (architecture doc + advisor outputs + collection
    # design + research instructions) routinely exceeds the kernel's ARG_MAX
    # when passed as an exec argument. The SYSTEM prompt stays as
    # --system-prompt since it's bounded by the advisor template.
    args = [
        binary,
        '-p',
        '--model', model,
        '--no-session-persistence',
        '--permission-mode', 'bypassPermissions',
        '--tools', '',
        '--disable-slash-commands',
        '--setting-sources', '',
    ]
    if streaming:
        # stream-json + include-partial-messages emits NDJSON content_block_delta
        # frames as the model produces them. --verbose is required by the CLI
        # when combining stream-json with --print.
        args += ['--output-format', 'stream-json',
                 '--include-partial-messages', '--verbose']
    else:
        args += ['--output-format', 'json']
    if system:
        args += ['--system-prompt', system]
    return args


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
        return cors(web.json_response({'error': 'Invalid JSON body'}, status=400))

    binary = claude_path()
    if not binary:
        return cors(web.json_response(
            {'error': 'Claude Code CLI not found on PATH. Install Claude Code to use this provider.'},
            status=500
        ))

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
        return cors(web.json_response({'error': str(e)}, status=502))


async def _handle_chat_sse(request, binary, system, user, model, timeout=None):
    if timeout is None:
        timeout = TIMEOUT_SEC
    args = _build_args(binary, system, model, streaming=True)

    response = web.StreamResponse(
        status=200,
        headers={
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no',
            'X-Timeout-Used': str(timeout),  # FRG-07
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Accept',
        },
    )
    await response.prepare(request)

    async def send_event(payload):
        try:
            await response.write(f'data: {json.dumps(payload)}\n\n'.encode('utf-8'))
        except (ConnectionResetError, asyncio.CancelledError):
            raise

    try:
        proc = await asyncio.create_subprocess_exec(
            *args,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            limit=SUBPROC_LIMIT,
        )
    except FileNotFoundError:
        await send_event({'error': 'Claude Code CLI not found on PATH. Install Claude Code to use this provider.'})
        await response.write_eof()
        return response
    except Exception as e:
        await send_event({'error': f'failed to spawn claude: {e}'})
        await response.write_eof()
        return response

    # Send the user prompt over stdin (avoids ARG_MAX when context is large)
    # then close stdin so the CLI starts processing immediately.
    try:
        proc.stdin.write(user.encode('utf-8'))
        await proc.stdin.drain()
        proc.stdin.close()
    except (ConnectionResetError, BrokenPipeError):
        pass

    stderr_tail = bytearray()

    async def drain_stderr():
        nonlocal stderr_tail
        assert proc.stderr is not None
        while True:
            chunk = await proc.stderr.read(4096)
            if not chunk:
                return
            stderr_tail.extend(chunk)
            # Keep only the last 2KB so a chatty stderr can't blow memory.
            if len(stderr_tail) > 2048:
                del stderr_tail[:-2048]

    stderr_task = asyncio.create_task(drain_stderr())

    full_content = ''
    delta_count = 0
    timed_out = False
    completed = False
    # Stall watchdog state: surface a non-fatal warning to the demo when no
    # text_delta arrives for STALL_WARN_SEC. Keeps the operator's UI from
    # going silent during long thinking pauses without bailing the call.
    last_delta_at = asyncio.get_running_loop().time()
    stall_warned = False
    STALL_WARN_SEC = 30

    async def stall_watcher():
        nonlocal stall_warned
        while not completed and not timed_out:
            await asyncio.sleep(5)
            if completed or timed_out:
                return
            gap = asyncio.get_running_loop().time() - last_delta_at
            if gap > STALL_WARN_SEC and not stall_warned:
                stall_warned = True
                try:
                    await send_event({'warning': f'stalled — no token in {int(gap)}s'})
                except (ConnectionResetError, RuntimeError):
                    # Client disconnected mid-warning, or aiohttp couldn't
                    # write because the response was already closed. Both
                    # are normal late-stream conditions; just exit. Bare
                    # `except Exception` would have masked CancelledError
                    # (BaseException subclass since 3.8 — already not
                    # caught here, but documenting the choice).
                    return

    stall_task = asyncio.create_task(stall_watcher())
    try:
        async def pump():
            """Read NDJSON frames from claude --output-format stream-json
            and either:
              - emit a `delta` SSE event for each text_delta chunk, or
              - emit a `done` SSE event on `result` and return, or
              - emit an `error` SSE event on `result` with is_error=True
                AND empty content, then return.

            Invariant: any return that is paired with a `done` event MUST
            set `completed = True` first. The post-loop exit-code check
            (after the finally block) gates on `not completed` to decide
            whether to surface a non-zero CLI exit as an error.
            """
            nonlocal full_content, delta_count, completed, last_delta_at, stall_warned
            assert proc.stdout is not None
            while True:
                line = await proc.stdout.readline()
                if not line:
                    return
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                t = obj.get('type')
                if t == 'stream_event':
                    ev = obj.get('event') or {}
                    if ev.get('type') == 'content_block_delta':
                        d = ev.get('delta') or {}
                        if d.get('type') == 'text_delta':
                            chunk = d.get('text') or ''
                            if chunk:
                                full_content += chunk
                                delta_count += 1
                                last_delta_at = asyncio.get_running_loop().time()
                                stall_warned = False
                                await send_event({'delta': chunk})
                elif t == 'result':
                    canonical = obj.get('result')
                    if obj.get('is_error'):
                        # The CLI reported a post-completion error (e.g.
                        # transient API hiccup, rate-limit at the tail,
                        # max_tokens truncation). If we already streamed
                        # visible text, surface what the user saw, but
                        # ALWAYS emit a `warning` ahead of `done` so the
                        # demo can render a "may be truncated" banner —
                        # rate-limit / max-tokens errors look like
                        # benign tail hiccups but are exactly the cases
                        # the workshop should show transparently.
                        # When we have no content to fall back on, fail.
                        if full_content:
                            completed = True
                            stall_task.cancel()  # FRG-05: prevent post-done warning
                            err_text = str(canonical) if canonical else 'claude reported an error'
                            await send_event({
                                'warning': f'recovered after CLI error — output may be truncated: {err_text}',
                            })
                            # BUG-02: prefer canonical when available — same policy
                            # as the non-error branch. Eliminates the double-count
                            # risk if partial frames overlap on recovery.
                            out_content = canonical if isinstance(canonical, str) and canonical else full_content
                            await send_event({
                                'done': True,
                                'content': out_content,
                                'deltas': delta_count,
                                'recovered': True,
                                'cli_error': err_text,
                            })
                            return
                        await send_event({'error': str(canonical) if canonical else 'claude reported an error'})
                        return
                    if isinstance(canonical, str) and canonical:
                        # Prefer the canonical aggregate when available — it
                        # captures any text we missed via partial frames.
                        out_content = canonical
                    else:
                        out_content = full_content
                    completed = True
                    stall_task.cancel()  # FRG-05: prevent post-done warning
                    await send_event({'done': True, 'content': out_content,
                                      'deltas': delta_count})
                    return

        try:
            await asyncio.wait_for(pump(), timeout=timeout)
        except asyncio.TimeoutError:
            timed_out = True
            try:
                proc.kill()
            except ProcessLookupError:
                pass
            tail = bytes(stderr_tail).decode('utf-8', errors='replace').strip()
            tail = tail[-200:] if tail else ''
            msg = f'claude CLI timeout ({timeout}s)'
            if tail:
                msg += f' — stderr tail: {tail}'
            await send_event({'error': msg})
    except (ConnectionResetError, asyncio.CancelledError):
        try:
            proc.kill()
        except ProcessLookupError:
            pass
        raise
    finally:
        # proc.wait() does NOT raise ProcessLookupError — only proc.kill()
        # does, when the process is already gone. So the outer except is
        # just for the wait_for timeout (process didn't exit within 2s
        # after pump returned/raised). The inner try wraps proc.kill()
        # which can race with natural exit.
        try:
            await asyncio.wait_for(proc.wait(), timeout=2)
        except asyncio.TimeoutError:
            try:
                proc.kill()
            except ProcessLookupError:
                pass
        stderr_task.cancel()
        try:
            await stderr_task
        except asyncio.CancelledError:
            pass
        except Exception as e:
            # Drain task exited with an unexpected error (e.g.
            # LimitOverrunError if SUBPROC_LIMIT was exceeded on stderr).
            # Surface to operator stderr so it isn't silently swallowed.
            print(f'[RELAY] stderr drain task error (non-fatal): {e!r}', flush=True)
        stall_task.cancel()
        try:
            await stall_task
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f'[RELAY] stall watcher error (non-fatal): {e!r}', flush=True)

    # Skip the post-stream exit-code check when pump() already emitted a done
    # event — the CLI's exit code is informational at that point and surfacing
    # it as an error would mask a successful streamed completion.
    if not completed and not timed_out and proc.returncode not in (0, None):
        tail = bytes(stderr_tail).decode('utf-8', errors='replace').strip()
        tail = tail[-200:] if tail else ''
        err = f'claude exited with code {proc.returncode}'
        if tail:
            err += f' — stderr tail: {tail}'
        await send_event({'error': err})

    await response.write_eof()
    return response


async def main():
    app = web.Application(middlewares=[dotfile_filter])
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
