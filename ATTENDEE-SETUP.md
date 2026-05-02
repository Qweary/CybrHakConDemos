# Attendee Setup — API Key + First Run

**Time required: ~5 minutes**

You only need to do this once. Your key is stored in your browser's localStorage — it persists across page reloads and will be there when you open any of the three demos.

---

## Do You Need an API Key?

**No** — if you want to observe. Every demo has a **DEMO MODE** that runs pre-scripted content with no network calls, no key, and no cost. Click `[ ◉ DEMO MODE ]` at the bottom of any demo.

**Yes** — if you want to run live AI calls (required for LAB-1, LAB-2, LAB-3). Pick one of the three live options below.

---

## Option D: Ollama — Fully Local, Offline

No API key. No internet required after setup. Runs open-weight models (llama3.2, mistral, phi3) entirely on your machine.

1. Install Ollama and pull a model — see **OLLAMA-SETUP.md** for full instructions
2. Run `ollama serve` in a terminal
3. In any demo, click **[ OLLAMA ]** in the provider selector
4. A model name field appears — type `llama3.2` (or your preferred model)
5. Click `[ LAUNCH FORGE ]` — calls go to `http://localhost:11434/v1/chat/completions`

**Note:** Output quality is lower than Claude or GPT-4. Expect shorter, less structured agent outputs. Good for offline demo and comparison runs.

---

## Option A: Zero-cost — OpenRouter Free Tier

No credit card. Free account at openrouter.ai. Models are lower quality than Claude (the free default is `google/gemini-2.0-flash-exp:free`) but are sufficient to see the swarm workflow in action.

1. Go to **https://openrouter.ai** and create a free account (Google sign-in works)
2. Navigate to **Keys** → **Create Key** — name it anything
3. Copy the key (starts with `sk-or-v1-...`)
4. In any demo, click **[ OR FREE ]** in the provider selector
5. Paste your key when prompted — it saves to localStorage
6. Click `[ LAUNCH FORGE ]` — no credits are consumed

**Note:** Output quality is noticeably lower than Claude. Expect shorter, less structured agent outputs. Good for seeing the workflow; use an OpenRouter paid key or the relay for a proper demo.

---

## Option B: Claude Code (if you have Claude Code installed)

If you (or the presenter) already have Claude Code installed and authenticated, a small local helper (`relay.py`) shells out to the `claude` CLI for each demo call — your existing Claude Code subscription is reused, no separate Anthropic API key required.

Prerequisite: `claude --version` works in your terminal. If not, install Claude Code first ([docs.claude.com/claude-code](https://docs.claude.com/claude-code)).

1. Run `python3 relay.py` from the workshop root directory (do this once, leave it running)
2. Open any demo and click **[ CLAUDE CODE ]**
3. No key field appears — authentication flows through your local `claude` CLI
4. Click `[ ⚛ INITIATE FISSION ]` — calls go to `http://localhost:3001/v1/chat`, which spawns `claude -p` for each phase

See **CLAUDE-CODE-SETUP.md** for installation prerequisites and troubleshooting.

---

## Option C: OpenRouter (Paid — Best Quality)

Full Claude Sonnet 4.6 quality via OpenRouter. ~$0.10–0.18 for the full workshop.

OpenRouter is a vendor-neutral API gateway. It gives you access to Claude, GPT-4, Gemini, and others through a single key and a single billing account.

1. Go to **https://openrouter.ai**
2. Click **Sign In** → create an account (email or Google)
3. After login, click your avatar → **Keys**
4. Click **Create Key** — name it anything (e.g., `aivillage-workshop`)
5. Copy the key — it starts with `sk-or-v1-...`

**Add credits:** Under your avatar → **Credits** → add $5. That covers roughly 50 full workshop runs.

---

### Step 2: Open a Demo

Open `demos/tmp-forge-live.html` directly in your browser. You can use `file://` paths (double-click the file) or serve it locally:

```bash
# If you have Python:
python3 -m http.server 8080
# Then open: http://localhost:8080/demos/tmp-forge-live.html
```

**Note on CORS:** The demos call `https://openrouter.ai/api/v1/chat/completions` directly from the browser. This works fine from `file://` — no server required. If you see a CORS error in your browser console, switch to the `localhost:8080` approach above.

---

### Step 3: Select Your Provider and Paste Your Key

1. In any demo, find the provider selector at the top — click the button matching your chosen option (**OR FREE**, **OPENROUTER**, etc.) and it will highlight
2. A text field appears below it — paste your key (`sk-or-v1-...`)
3. The key is saved to localStorage immediately as you type — no confirmation button needed
4. If a model field appears, leave it as-is (`anthropic/claude-sonnet-4-6` for OPENROUTER; `google/gemini-2.0-flash-exp:free` for OR FREE)

**The key is stored only in your browser.** It never leaves your machine except in direct API calls to the provider you selected.

---

### Step 4: First Run

1. In `tmp-forge-live.html`, select the **RED** preset
2. Click **[ LAUNCH FORGE ]**
3. Watch the six phases run — each one is a separate API call (~10–30 seconds total)
4. You should see agent names, system prompts, and fabricated outputs appear in sequence

If it works, you're ready for the labs. If it fails, check:

- **"Invalid API key"** → re-paste the key; make sure OPENROUTER is selected (not ANTHROPIC)
- **"Insufficient credits"** → add $5 at openrouter.ai → Credits
- **"Network error"** → try the `localhost:8080` approach above
- **Blank output after 30+ seconds** → your key may have been pasted with extra whitespace; clear and re-paste

---

## Cost Reference

| Lab | Demo | Estimated Cost |
|---|---|---|
| LAB-1 | FORGE — one CUSTOM run | ~$0.01–0.02 |
| LAB-2 | COMBAT — IRONCLAD + PHANTOM FEED | ~$0.08–0.12 |
| LAB-3 | EVOLVE — one improvement cycle | ~$0.02–0.04 |
| **Full workshop** | All three labs | **~$0.10–0.18** |

DEMO MODE is always $0.00.

---

## Key Storage Details

Your key is stored under one of these localStorage keys depending on the demo:

- Forge: `tmp_or_key`
- Combat: `tmp_or_key`
- Evolve: `tmp_or_key`

All three demos share the same key. Paste it once in any demo and it will be available in all three (as long as you're using the same browser and same origin path).

To clear your key: open browser DevTools → Application → Local Storage → delete `tmp_or_key`.
