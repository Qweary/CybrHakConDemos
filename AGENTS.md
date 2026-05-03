# AGENTS.md — orientation for AI assistants helping with this workshop

You are helping someone who landed in this repo. They are most likely
**an attendee at CybrHakCon's AI Village track** trying to run the demos
for the first time. They probably don't know:

- what "multi-agent swarms" or "The Manhattan Project" mean
- whether they need an API key (they might not)
- how to start a local server or what `bin/start.sh` does
- which provider to pick or how to get its credentials

**Default behavior: assume the user is an attendee, not a developer.**
Walk them through the simplest working path. Switch to developer mode
only when they say something like "I want to change…" or "where's the
code that…" or they paste a stack trace.

---

## What this project is (one paragraph)

A workshop kit demonstrating **The Manhattan Project (TMP)** — a
framework for building coordinated multi-agent AI swarms. Three browser
demos: **FORGE** designs swarms from a plain-language brief, **COMBAT**
runs red-vs-blue adversarial exercises between two swarms, **EVOLVE**
auto-rewrites the weakest agent based on its scorecard. They chain
together: FORGE → COMBAT → EVOLVE → COMBAT again. Everything runs locally
on the attendee's machine via a single Python relay (`relay.py`) bound
to `127.0.0.1:3001` that serves the demos and bridges them to whichever
LLM provider the attendee picks.

---

## ATTENDEE PATH — the default

### Step 0 — figure out what the user wants

Before anything else, distinguish three intents (one polite question if
unclear):

| User intent | What to recommend |
|---|---|
| "I just want to see what this is" | DEMO MODE — no install, no key, no cost |
| "I want to run it for real with AI" | LIVE MODE — needs a provider; pick one below |
| "I want to do the labs" | Same as LIVE MODE plus the lab files |

### Step 1 — start the relay

One command from the workshop root:

```bash
bin/start.sh        # macOS / Linux
bin\start.ps1       # Windows PowerShell
```

The script runs `bin/doctor.sh` first to verify Python ≥ 3.10, aiohttp,
port 3001 free, etc. If anything fails, doctor prints the exact fix.
After the relay binds, it auto-opens the launcher in the user's default
browser at `http://localhost:3001/`.

If the user is on **NixOS** and `bin/start.sh` complains about missing
deps, suggest `cd packaging && nix run .#relay` instead — that's the
flake-managed path that bypasses the system Python.

If the user is in **Docker / a container**:
```bash
docker build -t tmp-workshop -f packaging/Dockerfile .
docker run --rm -p 3001:3001 tmp-workshop
```

### Step 2 — pick a provider

The launcher page lists three demos. Inside any demo, the bottom-left
provider selector has five buttons. Recommend by user situation:

| User says | Recommend | Why |
|---|---|---|
| "I just want to watch" | DEMO MODE | No key, no cost, plays canned transcripts |
| "I have Claude Code installed" | CLAUDE CODE | Reuses their existing OAuth, no separate key |
| "I have an OpenRouter account" | OPENROUTER | Best quality (Claude via OR), ~$0.10–0.18 for full workshop |
| "I want zero cost but live calls" | OR FREE | Free OpenRouter tier (gemini-2.0-flash-exp:free), lower quality |
| "I'm offline / want fully local" | OLLAMA | Needs `ollama serve` + `ollama pull llama3.2`, lowest quality |
| "I have an Anthropic API key directly" | ANTHROPIC | Straight to api.anthropic.com |

**Where the credentials go:**

- **CLAUDE CODE** — no key field appears. Auth flows through the
  attendee's local `claude` CLI (whatever they used to log in). Make
  sure `claude --version` works in their terminal.
- **OPENROUTER / OR FREE** — paste `sk-or-v1-...` into the field that
  appears next to the provider button. Stored in browser localStorage
  only. Get a free key at <https://openrouter.ai>.
- **ANTHROPIC** — paste `sk-ant-...`. Get one at <https://console.anthropic.com>.
- **OLLAMA** — no key. Just needs Ollama running locally.

If the user doesn't know which to pick: **default to OR FREE** for live
calls (free, easy signup) or **DEMO MODE** for zero-touch viewing.

Detailed per-provider setup: `docs/attendee/first-run.md`. Provider-specific deep
dives: `docs/attendee/providers/claude-code.md` and `docs/attendee/providers/ollama.md`.

### Step 3 — run a demo

The user opens one of the three demos from the launcher and clicks the
big launch button (varies per demo):

| Demo | Launch button | What it does |
|---|---|---|
| FORGE | `[ ⚛ INITIATE FISSION ]` | Runs a 9-phase pipeline that designs an agent swarm |
| COMBAT | `[ SETUP NETWORK ]` then `[ ⚛ ENGAGE ]` | Runs a red-vs-blue exercise across 6 phases |
| EVOLVE | `[ ⚛ BEGIN ANALYSIS ]` then `[ LAUNCH EVOLVE ]` | Scores agents, rewrites the weakest, re-runs |

For LIVE mode, each phase is an API call (~10–30s for OR / Anthropic;
~30–60s for OR FREE; minutes for Ollama on CPU). DEMO MODE is instant.

### Step 4 — when they hit an error

Direct them to `docs/attendee/workshop-guide.md` first — it has the
canonical fix list (paste-into-LLM-friendly). Common ones:

| Error / symptom | Fix |
|---|---|
| "Invalid API key" / 401 | Re-paste; confirm right provider is selected |
| "Insufficient credits" / 402 | Add $5 at openrouter.ai → Credits, or switch to OR FREE |
| "Connection refused" (CLAUDE CODE) | `bin/start.sh` isn't running — start it first |
| "claude not found" (CLAUDE CODE) | `which claude` returns nothing — install Claude Code |
| "Connection refused" (OLLAMA) | `ollama serve` isn't running |
| "Network error" from `file://` | Open via the relay (`http://localhost:3001/forge.html`) instead |
| Blank pane after 30+ s | Key has whitespace — clear and re-paste; OR a phase is genuinely slow, watch the `tokens: N` ticker |
| Stalled — no token in N s | Non-fatal; relay surfaces this. Click `[ ⏳ Continue waiting ]` to extend timeout |

For CLAUDE CODE timeout/recovery deep dive: `docs/attendee/providers/claude-code.md`.

### Step 5 — the labs

| Lab | Time | What |
|---|---|---|
| `labs/LAB-1-FORGE.md` | ~30 min | Forge a swarm for the user's own domain |
| `labs/LAB-2-COMBAT.md` | ~45 min | Run both COMBAT scenarios; compare blue detection |
| `labs/LAB-3-EVOLVE.md` | stretch | Close the loop on the failing agent |

The labs are markdown — don't paraphrase, just point the user at them.

### Useful start.sh toggles (only mention if asked)

```bash
bin/start.sh --port 4000          # alternate port
bin/start.sh --bind 0.0.0.0       # LAN-exposed (5-second confirmation)
bin/start.sh --no-browser         # don't auto-open
bin/start.sh --skip-checks        # bypass doctor (rarely needed)
```

---

## DEVELOPER PATH — when modifying behavior

Switch to this mode if the user:

- pastes a stack trace and wants you to debug
- asks "where is X defined" / "how do I change Y"
- says they want to add a provider, edit a prompt, etc.
- mentions tests, snapshots, branches, refactor

### Repo layout

```
relay.py                          ← entry shim (32 lines); imports tmp_relay.cli.main
src/tmp_relay/                    ← Python package (~700 lines, 5 modules)
  settings.py                       env vars + constants (BIND, PORT, MIN/MAX timeouts, CORS_HEADERS, etc.)
  claude_subprocess.py              build_args() + claude_path() — pure functions
  sse.py                            handle_chat_sse() with the pump/stall_watcher loop
  server.py                         JSON handler + middlewares + make_app() factory
  cli.py                            serve() async entry; main() console-script wrapper
web/                              ← static assets served at http://localhost:3001/
  index.html                        cyberpunk launcher with 3 demo cards
  forge.html, combat.html, evolve.html
  assets/prompts/{forge,combat,evolve}/*.md
                                    38 SYS_* prompts as readable .md (DERIVED — see below)
labs/LAB-{1,2,3}-*.md             ← attendee labs (don't edit unless explicitly asked)
docs/
  attendee/                         user-facing setup + workshop guide
  dev/                              audit, relay-review, testing — refactor archaeology
tests/
  test_workshop.py                  186 static / structural checks
  test_snapshots.py                 90 content-drift tripwires
  e2e/test_browser_smoke.py         27 Playwright tests
  relay/test_relay_unit.py          21 in-process unit tests
  relay/test_relay_live.py          16-min real-API harness — MANUAL ONLY
bin/{start,doctor}.{sh,ps1}       ← attendee launcher + diagnostic
packaging/                        ← Dockerfile, flake.nix, README, windows-setup.md
.devcontainer/devcontainer.json   ← VS Code reopen-in-container
pyproject.toml                    ← `pip install .` exposes `tmp-relay` console script
```

### Code is single-source-of-truth, prompts are dual-source

- **Code** lives in `src/tmp_relay/` only. `relay.py` is a 32-line shim
  that bootstraps the path and calls `cli.main()`. Always edit code in
  `src/tmp_relay/`, never `relay.py`.
- **Prompts** live inline as `SYS_*` / `SYS.*` JavaScript constants in
  `web/forge.html`, `web/combat.html`, `web/evolve.html` — that's the
  RUNTIME source. The `.md` files in `web/assets/prompts/**/*.md` are a
  DERIVED read-only export. If you edit a prompt, edit it in the HTML
  and run `python3 tests/test_snapshots.py --update prompts` to
  regenerate the `.md` files.

### Test workflow

Always green before committing. Three runnable suites + the gated live one:

```bash
bash run_tests.sh                 # static + snapshot + unit + e2e (with venv)
python3 tests/test_workshop.py    # static only (~2s, stdlib only)
python3 tests/test_snapshots.py   # snapshot only (~3s)
.venv-e2e/bin/pytest tests/relay/test_relay_unit.py   # unit only (~0.15s)
```

If a snapshot fails after an intentional change:

```bash
python3 tests/test_snapshots.py --update          # regenerate all
python3 tests/test_snapshots.py --update prompts  # one snapshot
# Then commit the regenerated JSON alongside the source change.
```

Live API harness — only when validating relay/streaming changes. Costs
real money. Manual invocation only:

```bash
python3 relay.py                  # first, in another shell
python3 tests/relay/test_relay_live.py
```

### Refactor philosophy (read these if doing serious work)

- `docs/dev/audit-phase-0.md` — pre-refactor catalog of hardcoded paths
  and assumptions.
- `docs/dev/relay-review.md` — Opus-graded code review of the relay
  with 20 numbered findings (BUG-01 through STY-20). Findings 1–11 are
  resolved; 12–15 (ARCH) are intentional follow-ups; 16–20 (STY) are
  ambient nice-to-haves.
- `docs/dev/testing.md` — the canonical test-suite reference.

### Common dev tasks

**"I want to add a new provider"**
1. Edit each demo HTML's provider selector + a `call<Name>(sys, user, ak)` function
2. Wire localStorage key for the API token
3. Add an entry to `docs/attendee/first-run.md` explaining the user setup
4. The relay doesn't need changes unless the new provider goes through it

**"I want to change a system prompt"**
1. Edit the `SYS.*` / `SYS_*` constant in `web/{forge,combat,evolve}.html`
2. Run `python3 tests/test_snapshots.py --update prompts`
3. Commit both the HTML edit and the `.md` regeneration

**"I want to change how the relay handles X"**
1. Edit the relevant module in `src/tmp_relay/` (settings / subprocess /
   sse / server / cli)
2. Run `bash run_tests.sh` — snapshot will catch /health-shape changes
3. If you changed SSE behavior, manually run the live harness to verify
4. `relay.py` (the shim) almost never needs changes

**"I want to add a wrapper for platform X"**
1. Add to `packaging/` (or `bin/` if it's a launcher script)
2. Update `packaging/README.md` wrapper inventory
3. If it sets env vars, document the contract in `src/tmp_relay/settings.py`

**"I'm getting a CORS error"**
1. Check `cors_middleware` in `src/tmp_relay/server.py`
2. Verify the demo is loading via `http://localhost:3001/...`, not `file://`
3. The `tests/relay/test_relay_unit.py::test_health_carries_cors_headers`
   covers this end-to-end

### Branching + commit style

- Long-running refactor work: branch (`refactor/<topic>`), commit per
  feature/fix, snapshots stay green per commit.
- Small fix on `main`: just commit, push, done.
- Commit messages: conventional (feat / fix / docs / test / refactor /
  chore + scope), why-not-what body, reference review-finding IDs
  (BUG-XX, FRG-XX) when applicable.
- Never include external-repo URLs / issue numbers / PR refs in commit
  messages or source comments (per global CLAUDE.md privacy rule).

### Don't do these

- Don't edit `relay.py` directly — change `src/tmp_relay/` instead.
- Don't edit `web/assets/prompts/**/*.md` directly — they're derived.
- Don't commit `.venv-e2e/`, `.pytest_cache/`, `*.egg-info/`, `uv.lock`
  — already gitignored.
- Don't run `python -m http.server` — use the relay (Phase 4 decision;
  the relay binds 127.0.0.1, http.server binds 0.0.0.0).
- Don't drop session-stamp tests in `tests/test_workshop.py` (S46,
  S47.5d, etc.) without migrating their behavioral meaning to the new
  test layout — they're locking real invariants in.

---

## File map (quick reference)

| Question | File |
|---|---|
| What is this project? | `README.md` |
| How do I start? | `bin/start.sh` (or `.ps1`) |
| What's wrong with my setup? | `bin/doctor.sh` |
| Which provider should I use? | `docs/attendee/first-run.md` |
| Step-by-step lab? | `labs/LAB-{1,2,3}-*.md` |
| Common errors + fixes? | `docs/attendee/workshop-guide.md` |
| How does the relay work? | `src/tmp_relay/__init__.py` (roadmap) → individual modules |
| Where's a specific prompt? | `web/assets/prompts/{forge,combat,evolve}/*.md` |
| How do I run tests? | `docs/dev/testing.md` |
| Why is the relay coded this way? | `docs/dev/relay-review.md` |
| Docker / Nix / Windows packaging? | `packaging/README.md` |

---

## When the user is clearly stuck

1. Run `bin/doctor.sh` — most issues surface there with a fix.
2. Check the browser DevTools Console + Network tab — the relay returns
   errors as JSON 502/504 or as `data: {"error": ...}` SSE frames.
   Neither writes to the relay's stdout.
3. If the user is mid-demo and hit an error: the recovery banner inside
   the demo offers Continue / Retry / Skip / DEMO / Abort. They don't
   need to restart anything.
4. Switch to DEMO MODE as a fallback — confirms the UI/JS works, isolates
   the issue to provider/key/network.
