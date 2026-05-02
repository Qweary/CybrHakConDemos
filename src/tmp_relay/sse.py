"""SSE handler for /v1/chat (streaming).

Forwards `claude --output-format stream-json --include-partial-messages`
NDJSON frames as Server-Sent Events. Three event shapes the demo
consumer must handle:

  data: {"delta": "<chunk>"}                   — text_delta during stream
  data: {"warning": "<msg>"}                   — non-fatal (stall, recovery)
  data: {"done": true, "content": "<aggregate>", "deltas": N,
         "recovered"?: true, "cli_error"?: "<msg>"}  — terminal success
  data: {"error": "<msg>"}                     — terminal failure

Architecture note (deferred from review): pump/stall_watcher/drain_stderr
all mutate shared closure variables. ARCH-12 will refactor into a
StreamSession dataclass. Kept inline here so the move is content-preserving.
"""

from __future__ import annotations

import asyncio
import json

from aiohttp import web

from .claude_subprocess import build_args
from .settings import (
    CORS_HEADERS,
    STALL_WARN_SEC,
    STDIN_CHUNK,
    SUBPROC_LIMIT,
    TIMEOUT_SEC,
)


async def handle_chat_sse(request, binary, system, user, model, timeout=None):
    if timeout is None:
        timeout = TIMEOUT_SEC
    args = build_args(binary, system, model, streaming=True)

    response = web.StreamResponse(
        status=200,
        headers={
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no',
            'X-Timeout-Used': str(timeout),  # FRG-07
            # CORS duplicated here because cors_middleware can't set headers
            # after prepare() flushes them. Both reference CORS_HEADERS.
            **CORS_HEADERS,
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
    # then close stdin so the CLI starts processing immediately. Chunked
    # writes (STDIN_CHUNK) with drain between are necessary on Windows
    # ProactorEventLoop pipes — a single >64 KB write can intermittently
    # `BrokenPipeError` when the kernel pipe buffer fills before the CLI
    # starts reading. Workshop forge prompts exceed 64 KB by Phase 3, so
    # the chunking is load-bearing on Windows. Costs nothing on macOS/Linux.
    payload = user.encode('utf-8')
    try:
        for i in range(0, len(payload), STDIN_CHUNK):
            proc.stdin.write(payload[i:i + STDIN_CHUNK])
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
    last_delta_at = asyncio.get_running_loop().time()
    stall_warned = False

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
