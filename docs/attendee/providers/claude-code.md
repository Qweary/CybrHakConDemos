# Claude Code Provider Setup — No Anthropic API Key Required

The **CLAUDE CODE** provider lets you run LIVE MODE in the demos using your existing Claude Code subscription. The demos talk to a small local Python server (`relay.py`) that shells out to the `claude` CLI for each call — your Claude Code authentication is reused, no separate Anthropic API key required.

**Use this if:** you have Claude Code installed and authenticated (you can already run `claude` from your terminal).

**Skip this if:** you are using Anthropic direct, OpenRouter, OR FREE, Ollama, or DEMO MODE.

---

## Step 1: Verify Claude Code is Installed

The relay calls the `claude` CLI as a subprocess. Confirm it is on your PATH:

```bash
which claude
claude --version
```

You should see a path (e.g. `/usr/local/bin/claude`) and a version string (e.g. `2.1.123 (Claude Code)`). If the binary is missing, install Claude Code first — see [docs.claude.com/claude-code](https://docs.claude.com/claude-code) — and confirm `claude --version` works before continuing.

The relay uses `claude -p` (non-interactive print mode) with `--no-session-persistence`, so each demo call is a one-shot completion that does not affect any of your saved Claude Code sessions.

---

## Step 2: Install aiohttp

```bash
pip install aiohttp
```

aiohttp is the only Python dependency the relay needs (not in stdlib). If you already have it, skip this step.

---

## Step 3: Run the Relay

From the workshop root directory:

```bash
python3 relay.py
```

You should see:

```
[RELAY] claude CLI: /usr/local/bin/claude
[RELAY] Listening on http://localhost:3001
[RELAY] Test: curl http://localhost:3001/health
[RELAY] Ctrl+C to stop
```

The relay only binds to `127.0.0.1` — it is not reachable from other machines.

---

## Step 4: Test the Relay

```bash
curl http://localhost:3001/health
```

Expected response:

```json
{"status": "ok", "claude_binary_present": true, "claude_binary_path": "/usr/local/bin/claude"}
```

If `claude_binary_present` is `false`, the relay started in a shell where `claude` is not on PATH. Stop the relay, fix the PATH (or install Claude Code), and restart.

---

## Step 5: Select [ CLAUDE CODE ] in the Demo

1. Open any demo in your browser (file:// or localhost:8080)
2. Click the **[ CLAUDE CODE ]** button in the provider selector
3. No key field appears — authentication flows through your Claude Code installation
4. Click **[ ▶ INITIATE FORGE ]** (or **[ SETUP NETWORK ]** / **[ ▶ BEGIN ANALYSIS ]**) — the demo posts to `http://localhost:3001/v1/chat`

Each call spawns a one-shot `claude -p` subprocess. Expect the first call to take a few seconds longer than subsequent calls.

---

## What Attendees See

LIVE MODE through the CLAUDE CODE provider streams tokens from the model as they are produced. Each long phase (DIRECTOR, T2-ADVISOR A+B, RESEARCH-LEAD, AGENT-FABRICATOR, QUALITY-GATE, STRUCTURAL-REVIEWER for forge; red/blue stages for combat; ARBITER/SCULPTOR/RERUN for evolve) writes its output into the demo pane in real time, character by character — no more 60-300 second silent freeze while a phase generates.

A small **`tokens: N ▌`** counter in the header increments while the model is producing output. If you see the counter advancing, the model is responding correctly even if a particular pane is still filling. The counter resets at the start of each phase.

The relay opens a Server-Sent Events connection (`Accept: text/event-stream`) and forwards `claude -p --output-format stream-json --include-partial-messages` deltas as they arrive. The non-streaming JSON path remains unchanged — `/health` and any non-streaming client continue to work exactly as before.

---

## Troubleshooting

**`claude_binary_present: false` from /health**
→ The relay started in a shell where `claude` is not on PATH.
→ Stop the relay, run `which claude` to confirm the binary location, then restart relay.py from a shell with the same PATH.

**`Claude Code CLI not found on PATH` error from the demo**
→ Same as above — the relay process can't see the `claude` binary. Install Claude Code if needed, then restart the relay.

**`Connection refused` in the demo**
→ relay.py is not running. Start it and confirm you see the `Listening` message.

**`Address already in use` on port 3001**
→ Another process owns port 3001. Check with:
```bash
lsof -i :3001
```
Kill the process or change `PORT = 3001` in relay.py to a free port, then update the demo's `callClaudeCode` fetch URL to match.

**CORS error in browser console**
→ Should not happen — relay.py sends `Access-Control-Allow-Origin: *`. If you see one, confirm you are calling http://localhost:3001 (not https) and that the relay is actually running.

**`claude CLI timeout (600s)`**
→ A phase took longer than 600 seconds. The default already gives 10 minutes of headroom — the heavy phases (RESEARCH-LEAD research, AGENT-FABRICATOR fabrication, T2-ADVISOR Library Specification) run ~250-300s on typical workshop hardware. If you genuinely need more time, bump the timeout before starting the relay:
```bash
SWARM_RELAY_TIMEOUT_SEC=900 python3 relay.py
```
If a single phase needs more time without restarting the relay, the recovery banner's **[ ⏳ Continue waiting (+60s) ]** button bumps the budget for that one call — the demo posts to `?timeout=N` (clamped 60-1800) which overrides the per-call timeout for that single request only.
If timeouts persist, run `time claude -p "ping" --output-format json` in a separate shell to measure your CLI's baseline latency — anything over ~30s for that minimal call indicates a Claude Code installation issue rather than a relay problem.

**Recovery banner appeared during a phase**
→ A phase failed (timeout, transient API error, or other fault). The banner offers five options:
- **[ ⏳ Continue waiting (+60s) ]** — re-issue the same call with a 60s timeout boost. Use when the model is just slow.
- **[ ↻ Retry phase ]** — re-issue the call with the default budget. Use for transient API errors.
- **[ ⏭ Skip phase ]** — substitute a `[phase skipped by operator]` placeholder and continue. Downstream phases get the placeholder as context. Use when one phase is broken but the rest of the run is salvageable.
- **[ ◉ Switch to DEMO ]** — flip to DEMO MODE and retry. Use as a safety net if LIVE is genuinely unavailable.
- **[ ✕ Abort run ]** — surface to the whole-run recovery banner. Use to stop the run.

**Token ticker is stuck at 0 / a phase pane is empty**
→ The relay's SSE branch isn't producing deltas. Confirm streaming end-to-end with:
```bash
curl -N -H 'Accept: text/event-stream' -H 'Content-Type: application/json' \
  -X POST http://localhost:3001/v1/chat \
  -d '{"system":"Be brief","user":"count to 5"}'
```
You should see a sequence of `data: {"delta": "..."}` events ending in `data: {"done": true, ...}`. If you only see a single `data: {"error": ...}` line, your `claude` CLI does not support `--output-format stream-json` — upgrade Claude Code and restart the relay.

**`claude returned non-JSON output`**
→ Your Claude Code CLI is older than the version that supports `--output-format json`. Upgrade Claude Code (`claude --version` should be ≥ 2.0.x) and restart the relay.

**`claude exited with code N` from the demo**
→ The CLI failed before producing output. The error message in the demo banner will include the stderr text — usually authentication-related. Run `claude -p "hello"` in your terminal to confirm the CLI itself works; if it prompts you to log in, do so, then retry the demo.
