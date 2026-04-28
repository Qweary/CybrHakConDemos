# Attendee Setup — API Key + First Run

**Time required: ~5 minutes**

You only need to do this once. Your key is stored in your browser's localStorage — it persists across page reloads and will be there when you open any of the three demos.

---

## Do You Need an API Key?

**No** — if you want to observe. Every demo has a **DEMO MODE** that runs pre-scripted content with no network calls, no key, and no cost. Click `[ ◉ DEMO MODE ]` at the bottom of any demo.

**Yes** — if you want to run live AI calls (required for LAB-1, LAB-2, LAB-3).

---

## Step 1: Get an OpenRouter Key

OpenRouter is a vendor-neutral API gateway. It gives you access to Claude, GPT-4, Gemini, and others through a single key and a single billing account.

1. Go to **https://openrouter.ai**
2. Click **Sign In** → create an account (email or Google)
3. After login, click your avatar → **Keys**
4. Click **Create Key** — name it anything (e.g., `aivillage-workshop`)
5. Copy the key — it starts with `sk-or-v1-...`

**Add credits:** Under your avatar → **Credits** → add $5. That covers roughly 50 full workshop runs.

---

## Step 2: Open a Demo

Open `demos/tmp-forge-live.html` directly in your browser. You can use `file://` paths (double-click the file) or serve it locally:

```bash
# If you have Python:
cd ai-village-workshop
python3 -m http.server 8080
# Then open: http://localhost:8080/demos/tmp-forge-live.html
```

**Note on CORS:** The demos call `https://openrouter.ai/api/v1/chat/completions` directly from the browser. This works fine from `file://` — no server required. If you see a CORS error in your browser console, switch to the `localhost:8080` approach above.

---

## Step 3: Select OpenRouter and Paste Your Key

1. In any demo, find the provider selector at the top — click **OPENROUTER** (it will highlight)
2. A text field appears below it — paste your key (`sk-or-v1-...`)
3. The key is saved to localStorage immediately — you'll see a lock icon or confirmation text
4. The model field will show `anthropic/claude-sonnet-4-6` — leave it as-is

**The key is stored only in your browser.** It never leaves your machine except in direct API calls to openrouter.ai.

---

## Step 4: First Run

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
