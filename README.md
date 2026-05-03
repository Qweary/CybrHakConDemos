# AI Village Workshop — Multi-Agent AI Systems for Offensive and Defensive Security

**CybrHakCon 2026 | AI Village Track | May 27, 2026**

This package contains three live AI demos and three hands-on labs. Everything runs in your browser. No installation required.

---

## What This Is

These demos show what happens when you compose multiple AI agents into a coordinated system — agents that plan together, disagree with each other, and iteratively improve their own behavior.

Three demos, one progression:

| Demo | File | What It Shows |
|---|---|---|
| **FORGE** | `web/forge.html` | A factory that designs a multi-agent swarm from a plain-language description |
| **COMBAT** | `web/combat.html` | A red team swarm vs. a blue team swarm — live adversarial AI exercise |
| **EVOLVE** | `web/evolve.html` | An autonomous improvement loop: score the agents, rewrite the weakest one, rerun the test |

They are connected. FORGE builds swarms. COMBAT runs them. EVOLVE improves them. Import a COMBAT result into EVOLVE, refine the agent that failed, and send the improved version back.

---

## Quickstart — one command

```bash
bin/start.sh        # macOS / Linux
bin\start.ps1       # Windows PowerShell
```

That's it. The script verifies your environment (Python ≥ 3.10, port
3001 free), sets up dependencies if needed, starts the relay, and
opens `http://localhost:3001/` in your browser. From the launcher,
click any demo card.

**Prefer Docker / Nix / VS Code devcontainer?** All four runtimes are
documented in [`packaging/README.md`](packaging/README.md). They all
end at the same `http://localhost:3001/`.

---

## Three Ways to Engage

### Tier 1 — 15-Minute Observer

You don't need an API key. Every demo has a **DEMO MODE** button that plays back a pre-scripted run with no network calls.

1. Run `bin/start.sh` (or open `web/combat.html` directly via `file://` if you'd rather skip the relay)
2. Click **[ ◉ DEMO MODE ]** at the bottom
3. Select **IRONCLAD** and click **[ LAUNCH EXERCISE ]**
4. Watch the red and blue agents interact across six phases

Do the same for FORGE and EVOLVE. Total time: ~15 minutes. No signup, no cost.

### Tier 2 — 45-Minute Practitioner

You have an OpenRouter key and want to run live AI calls.

1. Read `docs/attendee/first-run.md` — it takes 5 minutes
2. Work through **LAB-1** (forge a swarm for something you actually do)
3. Work through **LAB-2** (run both combat scenarios, compare blue detection)
4. Optional stretch: **LAB-3** (close the loop — improve the agent that failed)

### Tier 3 — Researcher / Builder

You want to understand how this works and extend it.

- All three demos are single-file HTML — open in a text editor and read the JavaScript
- Agent system prompts are embedded as JavaScript constants (`SYS_ARBITER`, `SYS_SCULPTOR`, `SYS_PHANTOM_RED_RECON`, etc.)
- The coordination model is a sequential state-passing pattern: each agent receives the prior agent's output as context
- The full framework that generates these swarms lives at: `https://github.com/Qweary/The-Manhattan-Project`
- See the GitHub repo for full technical documentation.

---

## Files in This Package

```
.
├── README.md                     (this file)
├── relay.py                      (Claude Code relay + static host — python3 relay.py)
├── web/
│   ├── index.html                (launcher — open http://localhost:3001/ )
│   ├── forge.html
│   ├── combat.html
│   └── evolve.html
├── labs/
│   ├── LAB-1-FORGE.md            (30 min — forge a swarm for your domain)
│   ├── LAB-2-COMBAT.md           (45 min — run both scenarios, compare blue detection)
│   └── LAB-3-EVOLVE.md           (stretch — close the improvement loop)
└── docs/
    ├── attendee/
    │   ├── first-run.md          (API key setup — all four provider options)
    │   ├── workshop-guide.md     (paste into claude.ai for contextual help)
    │   └── providers/
    │       ├── claude-code.md    (reuse your Claude Code subscription, no separate key)
    │       └── ollama.md         (fully local, offline)
    └── dev/
        ├── testing.md            (test suite layout + how to run)
        └── audit-phase-0.md      (refactor audit notes)
```

---

## Cost Estimate

If you run all three labs with a live API key on Claude Sonnet 4.6 via
OpenRouter, expect to spend **~$2** total on API calls. Measured: a
single FORGE run lands around $0.40; COMBAT (which runs 24+ stages
across both scenarios) is the biggest line item at ~$1.20; EVOLVE
adds another ~$0.40 per cycle.

| Lab | Demo | Estimated Cost (Sonnet via OR) |
|---|---|---|
| LAB-1 | FORGE — one CUSTOM run | ~$0.40 |
| LAB-2 | COMBAT — IRONCLAD + PHANTOM FEED | ~$1.00–1.20 |
| LAB-3 | EVOLVE — one improvement cycle | ~$0.40 |
| **Full workshop** | All three labs | **~$2.00** |

DEMO MODE is always free. **OR FREE** (`google/gemini-2.0-flash-exp:free`)
is also $0. **Ollama** is $0 once the model is pulled. **CLAUDE CODE**
provider is free if your Claude Code subscription already covers it —
the relay reuses your existing OAuth, no separate metering.

Recommended model for paid use: `anthropic/claude-sonnet-4-6` via OpenRouter.

---

## Getting Help

**During the session:** Talk to the presenter.

**Using an AI assistant:** Open `docs/attendee/workshop-guide.md` and paste its contents into claude.ai (or any chat LLM) before asking your question. The guide gives the AI full context about all three demos, provider options, error messages, and lab flow — so you'll get accurate, specific answers instead of generic troubleshooting advice.

**After the conference:** Open an issue at the GitHub link above.
