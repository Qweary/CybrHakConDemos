# Local Relay Setup — No API Key Pasting Required

The local relay is an alternative to pasting your Anthropic API key into the browser. You run a small Python server on your machine; the demos send requests to it instead of calling Anthropic directly.

**Use this if:** you have `ANTHROPIC_API_KEY` set in your shell and don't want to paste it into the browser.

**Skip this if:** you are using OpenRouter, OR FREE, or Demo Mode.

---

## Step 1: Install aiohttp

```bash
pip install aiohttp
```

aiohttp is the only dependency (not in stdlib). If you already have it, skip this step.

---

## Step 2: Export Your Key

The relay reads `ANTHROPIC_API_KEY` from its environment. Set it in the shell where you will run relay.py:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

Confirm it is set:

```bash
echo $ANTHROPIC_API_KEY
```

---

## Step 3: Run the Relay

From the repo root (or the `ai-village-workshop/` directory — either works since relay.py is at the root):

```bash
python3 relay.py
```

You should see:

```
[RELAY] Key loaded: sk-ant-api01-...
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
{"status": "ok", "key_loaded": true, "key_prefix": "sk-ant-api01-..."}
```

If `key_loaded` is `false`, check that `ANTHROPIC_API_KEY` is set in the shell where relay.py is running.

---

## Step 5: Select [ LOCAL ] in the Demo

1. Open any demo in your browser (file:// or localhost:8080)
2. Click the **[ LOCAL ]** button in the provider selector
3. No key field appears — the relay supplies the key automatically
4. Click **[ LAUNCH FORGE ]** (or **[ SETUP NETWORK ]** / **[ RUN CYCLE ]**) — the demo calls `http://localhost:3001/v1/chat`

---

## Troubleshooting

**`key_loaded: false`**
→ The relay started before the key was exported, or was started in a different shell.
→ Set `ANTHROPIC_API_KEY` and restart relay.py.

**`Connection refused` in the demo**
→ relay.py is not running. Start it and confirm you see the `Listening` message.

**`Address already in use` on port 3001**
→ Another process owns port 3001. Check with:
```bash
lsof -i :3001
```
Kill the process or change `PORT = 3001` in relay.py to a free port, then update the demo's `callLocal` fetch URL to match.

**CORS error in browser console**
→ Should not happen — relay.py sends `Access-Control-Allow-Origin: *`. If you see one, confirm you are calling http://localhost:3001 (not https) and that the relay is actually running.

**Demo shows `HTTP 401` or `invalid x-api-key`**
→ The key in `ANTHROPIC_API_KEY` is invalid or expired. Check your Anthropic Console at console.anthropic.com.
