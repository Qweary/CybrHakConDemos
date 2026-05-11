# Phase 5a — `relay.py` Code Review

Static review of `/home/tokugero/repos/github/Qweary/CybrHakConDemos/relay.py`
ahead of the Phase 5c module split into `src/swarm_relay/`. Cross-referenced
against `docs/dev/audit-phase-0.md` section 9 (which previewed several of
these items).

Categories:

- **Bug** — incorrect under realistic conditions; fix before module split.
- **Fragility** — works today but easy to break / surprising; fix before split.
- **Architecture** — observation the refactor should respect or improve.
- **Stylistic** — naming, layout, comment quality. Note for the refactor.

Numbering is `[CATEGORY-N]` for cross-reference. Findings 01–11 map to the
specific concerns in the task brief; 12+ are additional issues.

---

## Bugs

### [BUG-01] `asyncio.get_event_loop()` is removed in Python 3.14

- **File / lines:** `relay.py:304`, `relay.py:314`, `relay.py:348`
- **What's wrong:** Three call sites use `asyncio.get_event_loop().time()`.
  This emits a `DeprecationWarning` in Python 3.12 and is **removed** in
  Python 3.14: when there is no running loop, `get_event_loop()` will raise
  `RuntimeError`. Today it works only because each call is reached from
  inside the running coroutine and the loop exists, but the API itself is
  on its way out and currently produces warnings that pollute attendee
  consoles on 3.12+.
  - Audit phase-0 §9 already flagged 285/293; the additional site at
    line 348 (inside `pump()`'s `text_delta` branch) is missed there.
- **Risk:** As soon as workshop attendees install Python 3.14 (next stable
  cut), the relay either spams warnings or crashes mid-stream the first
  time the stall watcher / pump fires. Three independent failure points.
- **Suggested fix:** Replace with `asyncio.get_running_loop().time()` at
  all three sites. Simpler still: capture `loop = asyncio.get_running_loop()`
  once at the top of `_handle_chat_sse` (after `await response.prepare`)
  and pass `loop.time` (the bound method) to `pump()` and `stall_watcher()`
  — turns three deprecated calls into one and makes both helpers easier to
  test.

### [BUG-02] `text_delta` snapshot frames are double-counted as deltas

- **File / lines:** `relay.py:341-350`
- **What's wrong:** The pump treats every `content_block_delta` whose
  inner `delta.type == 'text_delta'` as a streamable chunk and appends
  `chunk` to `full_content`. The Claude Code CLI in
  `--include-partial-messages` mode also emits assistant-message
  *snapshots* (via `message_delta` / `content_block_start` etc.) — those
  paths are correctly ignored. But the in-stream `text_delta` events
  themselves are *not* always strict diffs across all CLI versions; in
  some they re-emit a small overlap on stream resume. This is the same
  reason the `result` branch at line 372–377 prefers `canonical` "when
  available — it captures any text we missed via partial frames." If
  partial frames can also *over-count*, `full_content` is wrong on the
  recovery path (`is_error` branch) where `canonical` is bypassed.
- **Risk:** On the `is_error` recovery path (BUG-03 below), the demo
  receives a doubled or partially-doubled transcript instead of the
  cleanly streamed one. Hard to detect — the demo just shows mangled
  output and the user files it under "the model glitched."
- **Suggested fix:** Either (a) trust the CLI's invariant that
  `text_delta` events are strict diffs and add a doc-comment asserting it
  (cheap), or (b) on the recovery path, reconstruct `out_content` from
  `obj.get('result')` if present even when `is_error=True`. Recommend
  (b) — it's two lines and removes the assumption entirely.

### [BUG-03] `is_error` recovery accepts any error as benign if any text streamed

- **File / lines:** `relay.py:351-371` (especially 360-368)
- **What's wrong:** Current logic: if `is_error=True` arrives and
  `full_content` is non-empty, the call is reported as a successful
  completion with `recovered: True` and `cli_error` set. The comment
  defends this for "transient API hiccups at the very end of the stream."
  But the policy is unconditional on the *kind* of error. Realistic
  failure modes that this masks:
  - Quota / rate-limit error after a partial stream — the user sees a
    truncated answer presented as if it completed, with no visible cue
    that the model was cut off mid-thought.
  - `max_tokens` budget exceeded — user gets the truncated prefix marked
    as `done`, no indication that the answer is incomplete.
  - Tool/permission errors that *also* contain a non-empty `result`
    string that is itself the error message (e.g. "I cannot complete
    this request because…"). The relay surfaces that string as
    `content`, with `cli_error` set to the same string. Demo treats it
    as a successful completion.
- **Risk:** Silent truncation of demo output during exactly the failure
  modes the workshop most needs to demonstrate transparently (rate
  limits, quota). The `recovered: True` flag is set but no demo
  consumes it — verify against `web/forge.html` etc. before deciding
  the demo can act on it.
- **Suggested fix:** Two-part policy: (1) always emit a `warning` event
  ahead of the `done` event when recovery happened, so the demo can
  surface a banner regardless of whether it inspects `recovered`. (2)
  Inspect `obj.get('subtype')` / message text for the small set of
  error subtypes that genuinely indicate a truncation (rate-limit,
  budget) and treat *those* as hard errors even when `full_content`
  is non-empty. Cross-check against the Claude Code CLI's documented
  `is_error` taxonomy — if there isn't one, ship the `warning` and
  punt on the taxonomy.

### [BUG-04] Static catch-all `add_static('/', WEB_DIR)` shadows `OPTIONS /v1/chat` preflight

- **File / lines:** `relay.py:439-447`
- **What's wrong:** Routes are registered in this order:
  1. `OPTIONS /{path_info:.*}` → `handle_options`
  2. `GET /health`
  3. `POST /v1/chat`
  4. `GET /`
  5. `add_static('/', WEB_DIR, show_index=False)` (mounted last)

  aiohttp's router resolves by *first match in registration order*, with
  one important wrinkle: `add_static('/')` registers both a `GET` and a
  `HEAD` handler under `PrefixedSubAppResource`-style matching. Static
  resources registered under `/` will *not* shadow earlier exact routes
  for the methods they handle — but they will respond to `HEAD /v1/chat`
  with 405 from the static layer rather than passing through. Worse,
  any future request to `GET /v1/chat` (e.g., a browser typed-URL
  smoke test) returns aiohttp's static-layer "file not found" instead
  of a method-not-allowed response that signals "this is an API endpoint."
  - Path-traversal: aiohttp's `StaticResource` does normalize `..`
    segments and refuses paths that escape the root, so traversal is
    safe today. (Confirmed by aiohttp source — `_resolve_path_to_response`
    rejects paths whose resolved location isn't under the configured root.)
  - Dotfiles: `add_static` serves dotfiles by default. `web/` shouldn't
    have any today, but a stray `.DS_Store` or `.git/` (if a future
    contributor copies a tree in) would be served as-is.
- **Risk:** Method-not-allowed surface for `/v1/chat` is muddied. Dotfile
  serving is a foot-gun the moment someone drops a `.env` or `.git/` into
  `web/` for testing. Path-traversal: not a current bug.
- **Suggested fix:** (1) Pass `follow_symlinks=False` (default, but make
  it explicit) and add a small allow-list filter or `append_version=False`
  + a wrapper that 404s on basenames starting with `.`. Easiest: a tiny
  middleware that 404s when the request path's last segment starts with
  `.`. (2) Add an explicit `add_route('GET', '/v1/chat', _gone_handler)`
  returning 405 with an explanatory body so that typing the URL into a
  browser produces a useful error instead of a confusing 404 from the
  static layer.

---

## Fragility

### [FRG-05] Stall watcher race: warning can fire after `completed=True`

- **File / lines:** `relay.py:299-322` (state declarations + watcher),
  `relay.py:361-381` (pump sets `completed`)
- **What's wrong:** Three coroutines share four flags (`completed`,
  `timed_out`, `last_delta_at`, `stall_warned`) with no synchronization.
  The watcher reads `completed`/`timed_out` twice (line 310 and 312) but
  the gap between the second check and the `await send_event(...)` at
  318 is unbounded — the pump can set `completed = True` in that gap and
  then the demo receives `{"warning": "stalled — no token in Ns"}` *after*
  the `{"done": true, ...}` event. That's a protocol violation that the
  demo's SSE consumer almost certainly doesn't handle gracefully.
  - Even within a single event loop, `await send_event(...)` yields
    control between the check and the actual write, so the race is real.
- **Risk:** Sporadic post-completion warning events. Demo state machine
  may transition out of "thinking" → "done" → back to "warned." Visible
  to attendees as a flickering banner after the answer renders.
- **Suggested fix:** Inside `stall_watcher`, re-check
  `completed or timed_out` *one more time inside the `if gap > … and not
  stall_warned` block immediately before `await send_event`*. Or simpler:
  cancel `stall_task` synchronously the moment the pump sets
  `completed = True` (i.e., move the `stall_task.cancel()` from the
  `finally` block to immediately before `return` in the pump's `result`
  branch). The latter eliminates the race entirely.

### [FRG-06] `--system-prompt` passes whitespace and empty strings inconsistently

- **File / lines:** `relay.py:137-138` (and `relay.py:169` where `system`
  is read from the body)
- **What's wrong:** `system = body.get('system', '')`, then later
  `if system: args += ['--system-prompt', system]`.
  - Empty string → flag omitted → CLI uses Claude Code's default agent
    system prompt (the slow path the comment at line 24-28 explicitly
    warns against).
  - Whitespace-only string (e.g., `"   "`) → truthy → flag passed with
    a useless prompt. The CLI accepts it and the model receives just
    whitespace as its system context, which can subtly perturb output.
  - Shell metacharacters / backticks: **not a concern.** `create_subprocess_exec`
    takes an `args` list and does not invoke a shell — the string is
    passed as a literal argv element regardless of content. (Different
    on Windows: see FRG-09.)
- **Risk:** A demo that intends "no system prompt override" by sending
  `system=""` actually triggers the slow Claude-Code-as-agent path
  silently. A demo that sends `"   "` ships a degraded prompt.
- **Suggested fix:** Normalize at the boundary: `system = (body.get('system')
  or '').strip()`. Then either (a) keep current behavior (omit on empty)
  with a doc-string note, or (b) make "no override" explicit by requiring
  callers to send `system: null` and treat both `""` and missing key as
  "use a sentinel empty system prompt" (`--system-prompt ""`). Without the
  decision, the contract is ambiguous.

### [FRG-07] `?timeout=0` falls through to `TIMEOUT_SEC`, masking caller intent

- **File / lines:** `relay.py:142-153`
- **What's wrong:** `if not raw: return TIMEOUT_SEC` short-circuits on
  empty *string* (good), but the path `raw='0'` parses to `n=0`, then
  `max(60, min(1800, 0))` returns 60. The clamp silently rewrites a
  nonsensical value into a real one. Same for negative numbers
  (`?timeout=-5` → 60). Better than crashing, but the caller never
  learns their intent was ignored.
  - Conversely, `?timeout=99999` clamps silently to 1800. A "Continue
    waiting" recovery banner that asks for a 1-hour extension gets 30
    minutes without any feedback.
- **Risk:** Surprise behavior for the recovery-banner UX. If the
  recovery banner posts `?timeout=3600` after a stall, the user thinks
  they got an hour and the call dies at 30 min with no indication of why.
- **Suggested fix:** Return a 400 error response when the value is
  outside `[60, 1800]` rather than silently clamping. Or, less invasive:
  set a response header `X-Timeout-Used: <n>` on every call so the demo
  can detect when its requested timeout was overridden. Either way,
  surface the magic numbers as named constants (`MIN_TIMEOUT_SEC=60`,
  `MAX_TIMEOUT_SEC=1800`) per audit phase-0 §9.

### [FRG-08] `finally` block races: `proc.wait()` can race with kill

- **File / lines:** `relay.py:403-420`
- **What's wrong:** Sequence in the `finally`:
  1. `await asyncio.wait_for(proc.wait(), timeout=2)`
  2. on `TimeoutError` or `ProcessLookupError`: `proc.kill()` (which
     itself can raise `ProcessLookupError`)
  3. `stderr_task.cancel()` + `await stderr_task`
  4. `stall_task.cancel()` + `await stall_task`

  Issues:
  - **Step 1 catching `ProcessLookupError`:** `proc.wait()` does not
    raise `ProcessLookupError` — that exception comes from `proc.kill()`
    or `proc.send_signal()` when the process is already gone. Listing
    it in the `except` for `wait_for` is dead code; the inner `kill()`
    call at step 2 catches it correctly.
  - **No `stdin.close()` cleanup**: if the pump returned early (e.g.,
    after a recovery `done`) the CLI may still be holding stdin open
    waiting for input. `proc.wait()` would block on it for the full 2s
    every time. The streaming path closes stdin at line 277, so this
    is fine *for streaming*, but the JSON path uses `proc.communicate()`
    which handles it — confirm the streaming path's `stdin.close()` is
    actually awaited. (It is, at 276 `await proc.stdin.drain()`; the
    `close()` at 277 is non-blocking and that's correct.)
  - **`await stderr_task` after `cancel()`:** if `drain_stderr` is
    blocked on `await proc.stderr.read(4096)`, cancellation propagates
    fine. But if the process exited cleanly between the `proc.wait()`
    and the `cancel()`, `drain_stderr` may have already returned —
    `cancel()` on a completed task is a no-op and `await` returns the
    result. That's caught by the `except (CancelledError, Exception)`.
    However, the broad `except Exception` here swallows real errors
    from the drain task (e.g., `LimitOverrunError` if SUBPROC_LIMIT
    is exceeded on stderr). The 2 KB tail then silently never updates,
    but the timeout error message at line 391-396 still references it.
- **Risk:** Stderr drain failures are invisible. The `ProcessLookupError`
  in the outer except is misleading code. Cleanup is *probably* correct
  but the chain of try/except hides genuine bugs.
- **Suggested fix:** (1) Drop `ProcessLookupError` from the outer
  `except` at line 406. (2) Replace `except (asyncio.CancelledError,
  Exception)` with `except asyncio.CancelledError` (the expected case)
  and let other exceptions propagate or be logged at a `print()` to
  stderr — silently swallowing them costs debuggability and that's the
  whole reason this code is hard to reason about. (3) Document the
  invariant that `pump()` MUST set `completed=True` before returning
  via the `done` branch, and assert it after `pump()` finishes.

### [FRG-09] Windows asyncio subprocess: `limit=` and Proactor pipes

- **File / lines:** `relay.py:181-187`, `relay.py:256-262`
- **What's wrong:** Three Windows-specific concerns for the streaming path:
  - **`limit=SUBPROC_LIMIT`:** On Python 3.8+, Windows defaults to
    `ProactorEventLoop`, which *does* honor the `limit` parameter for
    subprocess pipes (it passes it into the underlying StreamReader).
    Confirmed safe.
  - **`stdin/stdout/stderr=PIPE` reliability:** Proactor pipes are
    reliable for binary I/O but have historical issues with very large
    individual writes (>64 KB) on stdin. The streaming path writes the
    *entire user prompt* in one `proc.stdin.write(user.encode())` then
    drains. Workshop prompts can exceed 64 KB by Phase 3 (the comment
    at line 114-118 specifically calls this out as the reason stdin is
    used). On Windows this triggers `BrokenPipeError` intermittently
    when the kernel pipe buffer fills before the CLI starts reading.
  - **`claude.cmd` shim resolution:** `shutil.which('claude')` on
    Windows returns `'claude.cmd'` (the npm wrapper). On Python 3.12+
    this works with `create_subprocess_exec` because Python recognizes
    `.cmd`/`.bat` and routes through `cmd.exe`. **On 3.11 and earlier**
    this fails — Python tries to exec the `.cmd` directly, which the
    OS refuses. The audit phase-0 §10 flagged the `which` lookup but
    not the exec compatibility.
- **Risk:** Windows attendees on Python 3.11 hit a confusing
  "FileNotFoundError" or "exec format error" on every call. Windows
  attendees with prompts >64 KB hit sporadic `BrokenPipeError` mid-write.
- **Suggested fix:** (1) Add a `python --version` check at startup that
  warns when running <3.12 on Windows. (2) Chunk the stdin write: loop
  writing 32 KB blocks with `await proc.stdin.drain()` between each.
  This costs nothing on Linux/macOS and removes the Windows pipe
  flake. Documented under Phase 8 in audit but worth fixing in 5b
  since the chunking change is small and isolated.

### [FRG-10] CORS gap on static assets

- **File / lines:** `relay.py:66-70` (cors helper), `relay.py:447`
  (`add_static`)
- **What's wrong:** `cors()` is applied per-handler to `/health`,
  `/v1/chat`, `/`, and OPTIONS. The `add_static` registration produces
  responses that **do not** go through `cors()`. Today this is fine
  because demos served from `web/` are same-origin with `/v1/chat`, so
  no CORS preflight occurs. The gap appears the moment:
  - An attendee opens a demo from `file://` (skipping the relay
    launcher) and the page tries to load an asset from
    `http://localhost:3001/somefile.js` — the static handler returns
    no `Access-Control-Allow-Origin`, so the browser blocks the asset.
  - A future asset (image, font) is referenced cross-origin from a
    different page.
- **Risk:** Latent gotcha; not breaking anything *today*. Will
  surface confusingly the first time someone debugs a `file://`
  scenario.
- **Suggested fix:** Either (a) document that the relay only supports
  same-origin asset loading and remove the `*` CORS from `/v1/chat`
  too (tighter security; matches the 127.0.0.1 bind intent), or (b)
  add a tiny middleware that injects the CORS headers on every
  response regardless of handler. Pick one consistent policy.

### [FRG-11] Client disconnect mid-SSE: process kill is correct, drain task cleanup is best-effort

- **File / lines:** `relay.py:397-402` (CancelledError handler),
  `relay.py:411-420` (finally cleanup)
- **What's wrong:** When the browser closes the SSE connection,
  `response.write()` raises `ConnectionResetError`, `pump()` propagates
  it (caught by the outer `except (ConnectionResetError,
  asyncio.CancelledError)` at 397), `proc.kill()` runs, then the
  `finally` block awaits `proc.wait()` and cancels both helper tasks.
  This is mostly correct. Two concerns:
  - **`stderr_task` may be mid-`read()` at kill.** When the subprocess
    is killed, the read returns empty (EOF), the loop exits cleanly,
    and the `cancel()` is a no-op. Safe.
  - **`stall_watcher` may be in `await asyncio.sleep(5)` at cancel.**
    Cancellation through sleep is safe. The catch on
    `await send_event(...)` inside the watcher (line 319-320) swallows
    any exception bare — including `CancelledError`. That means
    `cancel()` against a watcher mid-`send_event` may not actually
    interrupt it, and the `await stall_task` at line 418 could hang
    until the bare-except path completes naturally. Not a deadlock
    (`send_event` itself fails fast on closed connection) but an
    inconsistent cancellation contract.
- **Risk:** Slow shutdown when the user cancels mid-warning-emission.
  No data loss.
- **Suggested fix:** In `stall_watcher`, change `except Exception` at
  line 319 to `except (ConnectionResetError, RuntimeError)` and let
  `CancelledError` propagate. Bare `except Exception` is a pattern to
  audit globally in this file (see STY-15).

---

## Architecture

### [ARCH-12] `pump()` mutates 6 closure variables across two coroutines

- **File / lines:** `relay.py:297-381` (closure variables and pump)
- **What's wrong:** `_handle_chat_sse` declares `full_content`,
  `delta_count`, `timed_out`, `completed`, `last_delta_at`,
  `stall_warned`, `stderr_tail` as locals; `pump()`, `stall_watcher()`,
  `drain_stderr()`, and the outer body all mutate or read subsets of
  them via `nonlocal`. The state machine is implicit and untestable in
  isolation. This is the central refactor target for Phase 5c.
- **Risk:** Hard to extend (e.g., add a metrics counter). Hard to test
  (no unit can drive `pump()` without spinning up a real subprocess).
  Every future bug fix here requires re-reading 80 lines to convince
  yourself of the invariants.
- **Suggested fix:** For Phase 5c module split: extract a
  `StreamSession` dataclass that owns the mutable state, with methods
  `record_delta(text)`, `mark_completed(content)`, `mark_timed_out()`,
  `should_warn_stall(now) -> bool`. Then `pump()`, `stall_watcher()`,
  and the finally block all interact with the dataclass instead of
  bare `nonlocal` variables. Each method is unit-testable. The pump
  itself becomes a thin frame-dispatch loop.

### [ARCH-13] Single-source-of-truth for prompt-handling args

- **File / lines:** `relay.py:104-139` (`_build_args`),
  `relay.py:178-187` (JSON path call), `relay.py:233` (SSE path call)
- **What's wrong:** `_build_args` is the right idea but two callers
  pass `streaming` as a bool flag, and the function then branches on
  it. Mixing "what arguments does the CLI need" with "which output
  format do we want" couples two concerns.
  - Audit phase-0 §5a flagged the model fallback duplication
    (`'claude-haiku-4-5'` at line 171 duplicates the env default at
    line 63). When `DEFAULT_MODEL=""` is set (the documented escape
    hatch), the body's model is honored, but the **fallback** at line
    171 also says `'claude-haiku-4-5'` — so the body's `model` field
    is only consulted if the body explicitly sends one. Fine today;
    confusing tomorrow.
- **Risk:** Adding a third output mode (e.g., `text` for piping to
  another tool) requires touching the bool, the branch, and both call
  sites. The model resolution chain has three layers (env → body →
  inline default) where two would do.
- **Suggested fix:** During Phase 5c, split into `build_base_args(...)`
  and small format-specific helpers (`as_streaming(args)`,
  `as_json(args)`). Move model resolution into a single
  `resolve_model(body) -> str` that documents the precedence.

### [ARCH-14] Hardcoded bind address and port in `main()`

- **File / lines:** `relay.py:451`, `relay.py:41`
- **What's wrong:** `web.TCPSite(runner, '127.0.0.1', PORT)` and
  `PORT = 3001` are inline. Phase 5/8 needs to expose `--bind` and
  `--port` (with a warning banner when binding non-loopback, per the
  audit phase-0 §9 callout). The current shape forces the future
  refactor to thread arguments down into `main()`.
- **Risk:** Today: none. Architecture: the module split should make
  this a settings concern, not a `main()` literal.
- **Suggested fix:** Phase 5c: a `Settings` dataclass loaded from env
  + CLI args, passed into `make_app(settings)` and `serve(settings)`
  factories. The current `main()` becomes
  `serve(Settings.from_argv())`. This also resolves the
  `STALL_WARN_SEC = 30` magic-number-inside-function flag from audit
  phase-0 §9.

### [ARCH-15] No structured logging or request IDs

- **File / lines:** `relay.py:454-464` (only logging is startup
  prints; no per-request log)
- **What's wrong:** When a workshop attendee reports "the demo
  hung," there's no trace in the relay's stderr to correlate. The
  warning event for stalls is sent to the client only; the operator
  sees nothing. Stderr from the CLI is captured into a 2 KB tail
  (good) but only surfaced if a timeout fires.
- **Risk:** Triage time during the live workshop. Operator can't
  tell whether the relay saw the request, whether the CLI started,
  whether a stall warning fired, or whether the client disconnected.
- **Suggested fix:** Phase 5c: add a `logging` setup with a per-call
  request ID (UUID4 first 8 chars), log start / first-delta /
  completion / error transitions at INFO. No external dependencies
  needed. This becomes essential the moment the relay supports
  multiple concurrent calls.

---

## Stylistic

### [STY-16] `cors()` wraps the response after construction; could be a middleware

- **File / lines:** `relay.py:66-70` and every call site
- **Note:** Repeating `return cors(web.json_response(...))` is fine but
  noisy. Phase 5c could replace with an `@web.middleware` that
  injects headers — collapses ~10 wrappings into one declaration. Low
  priority.

### [STY-17] Inconsistent error-response shapes

- **File / lines:** `relay.py:160` (`{'error': 'Invalid JSON body'}`,
  status 400), `relay.py:164-167` (binary missing, status 500),
  `relay.py:198` (timeout, status 504), `relay.py:204` (502),
  `relay.py:217-219` (502)
- **Note:** The `{'error': ...}` shape is consistent, but the status
  codes mix layers. "Binary missing" is a relay configuration error
  (500 is correct) but "claude returned non-JSON output" is also 502
  (the relay calling an upstream that misbehaved). Phase 5c could
  document a small status-code policy (4xx for caller errors, 5xx
  for relay/CLI errors with sub-distinction).

### [STY-18] Health endpoint exposes binary path

- **File / lines:** `relay.py:81-87`
- **Note:** Returning the absolute path of the `claude` binary in
  `/health` is fine for a 127.0.0.1-only relay but would be a minor
  information disclosure if the bind ever changed (ARCH-14). Worth
  re-evaluating during Phase 8 when `--bind` is added: at minimum
  return only the basename when bound non-loopback.

### [STY-19] Bare `except Exception` patterns

- **File / lines:** `relay.py:159` (`except Exception:` for JSON
  parse — covers `json.JSONDecodeError` *and* aiohttp's
  `RequestPayloadError`, both intended), `relay.py:226-227`
  (`except Exception as e: return cors(...)` — swallows everything
  including `KeyboardInterrupt` if it ever leaks here), `relay.py:319`
  (watcher), `relay.py:414`/`relay.py:419` (cleanup)
- **Note:** Each is defensible in isolation but several swallow
  errors that would help debugging. Phase 5c: tighten to specific
  exception classes; allow `BaseException` (Ctrl-C, SystemExit) to
  propagate.

### [STY-20] Comment density is high but localizes context well

- **File / lines:** Throughout (notably 47-58, 104-118, 130-134,
  301-306, 354-359)
- **Note:** Positive observation. The "why" comments are excellent
  and answer questions a reader would otherwise have to spelunk the
  CLI for. Keep this style during the Phase 5c split — extract them
  into module-level docstrings on the new files rather than dropping
  them.

---

## Cross-reference to `audit-phase-0.md` §9 and §10

| Audit item | This review |
|---|---|
| `asyncio.get_event_loop()` deprecation | BUG-01 (extends to 3 sites, not 2) |
| `is_error` recovery: prefer streamed content | BUG-03 (escalated from "document as invariant" to "policy is wrong for some error subtypes") |
| `pump()` 60+ lines, nested | ARCH-12 (with concrete refactor sketch) |
| `finally` double-cancel | FRG-08 (also flags dead `ProcessLookupError`) |
| 600s timeout, 4 MB buffer, prompt-overrides | Not re-reviewed — defer to Phase 5b verification |
| `--system-prompt` empty behavior | FRG-06 |
| `?timeout=` clamp magic numbers | FRG-07 (escalated from "magic numbers" to "silent rewriting of caller intent") |
| `STALL_WARN_SEC = 30` inside function | ARCH-14 (rolled into settings) |
| `127.0.0.1` hardcoded | ARCH-14 |
| Windows `ProactorEventLoop` + claude.cmd | FRG-09 (specific failure modes identified) |

Items I did **not** re-review (per task brief "don't worry about" + audit
phase-0 already adequate): the 600s/4 MB defaults, the prompt-routing CLI
flags themselves.

---

## Summary by severity

| Category | Count |
|---|---|
| Bug | 4 (BUG-01–04) |
| Fragility | 7 (FRG-05–11) |
| Architecture | 4 (ARCH-12–15) |
| Stylistic | 5 (STY-16–20) |

**Top three to fix before the module split:**

1. **BUG-01** (`get_event_loop` removal) — three-site fix, blocks Python
   3.14 attendees, mechanical.
2. **BUG-03** (`is_error` recovery semantics) — silent truncation during
   exactly the error modes the workshop should demonstrate transparently.
3. **FRG-05** (stall-watcher race) — protocol violation visible to
   attendees as a flickering banner; one-line fix (cancel the watcher
   from inside the pump's `result` branch).

The module split itself (Phase 5c) is the right time to land **ARCH-12**
(pump state extraction) and **ARCH-14** (settings dataclass).
