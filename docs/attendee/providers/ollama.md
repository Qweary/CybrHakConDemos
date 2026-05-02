# Ollama Setup — Fully Local, Offline AI

Ollama lets you run open-weight models entirely on your machine. No API key, no internet required once the model is downloaded.

**Use this if:** you want fully local operation, are offline at the venue, or want to compare local model quality against Claude.

**Note on quality:** Local models (llama3.2, mistral, phi3) produce shorter, less structured outputs than Claude. The workflow is identical — you'll see all six phases run — but agent outputs will be simpler. Good for offline demo and comparison; not recommended for production swarm generation.

---

## Install Ollama

**macOS:**
```bash
brew install ollama
```

**Linux (apt-based):**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
```
winget install Ollama.Ollama
```

Or download the installer from https://ollama.com/download.

---

## Start the Ollama Server

```bash
ollama serve
```

You should see output like:
```
Ollama is running on http://localhost:11434
```

Leave this terminal open. The demos call `http://localhost:11434/v1/chat/completions` directly.

---

## Pull a Model

```bash
ollama pull llama3.2
```

This downloads ~2GB. Do this before the workshop if you are on a slow connection.

---

## Verify It Works

```bash
curl http://localhost:11434/api/tags
```

You should see a JSON response listing your pulled models.

---

## Recommended Models for This Workshop

| Model | Pull command | Size | Notes |
|---|---|---|---|
| **llama3.2** | `ollama pull llama3.2` | ~2GB | Best balance of speed and quality for the workshop |
| **mistral** | `ollama pull mistral` | ~4GB | Stronger instruction-following; slower on CPU |
| **phi3** | `ollama pull phi3` | ~2.2GB | Microsoft's compact model; fast, reasonable quality |

Start with `llama3.2` if you are unsure.

---

## Select Ollama in the Demo

1. Open any demo in your browser
2. Click **[ OLLAMA ]** in the provider selector
3. A model name field appears — type your model name (default: `llama3.2`)
4. No key field appears — Ollama has no authentication
5. Click **[ LAUNCH FORGE ]** (or **[ SETUP NETWORK ]** / **[ RUN CYCLE ]**) — calls go to `http://localhost:11434/v1/chat/completions`

---

## Troubleshooting

**`Connection refused` in the demo**
→ Ollama is not running. Start it with `ollama serve`.

**`model not found`**
→ You haven't pulled the model yet. Run `ollama pull llama3.2` (or your chosen model name).

**Slow responses**
→ Normal on CPU-only machines. llama3.2 takes 10–60 seconds per phase depending on hardware. Use DEMO MODE if you need speed for a presentation.

**CORS error in browser console**
→ Should not happen — Ollama's `/v1` endpoint allows browser requests. If you see one, run the relay (`python3 relay.py` from the workshop root) and load the demo at `http://localhost:3001/forge.html` instead of via `file://`.
