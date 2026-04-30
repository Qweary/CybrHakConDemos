# AI Village Workshop — Multi-Agent AI Systems for Offensive and Defensive Security

**CybrHakCon 2026 | AI Village Track | May 27, 2026**

This package contains three live AI demos and three hands-on labs. Everything runs in your browser. No installation required.

---

## What This Is

These demos show what happens when you compose multiple AI agents into a coordinated system — agents that plan together, disagree with each other, and iteratively improve their own behavior.

Three demos, one progression:

| Demo | File | What It Shows |
|---|---|---|
| **FORGE** | `demos/tmp-forge-live.html` | A factory that designs a multi-agent swarm from a plain-language description |
| **COMBAT** | `demos/tmp-combat-live.html` | A red team swarm vs. a blue team swarm — live adversarial AI exercise |
| **EVOLVE** | `demos/tmp-evolve-live.html` | An autonomous improvement loop: score the agents, rewrite the weakest one, rerun the test |

They are connected. FORGE builds swarms. COMBAT runs them. EVOLVE improves them. Import a COMBAT result into EVOLVE, refine the agent that failed, and send the improved version back.

---

## Three Ways to Engage

### Tier 1 — 15-Minute Observer

You don't need an API key. Every demo has a **DEMO MODE** button that plays back a pre-scripted run with no network calls.

1. Open `demos/tmp-combat-live.html` in your browser
2. Click **[ ◉ DEMO MODE ]** at the bottom
3. Select **IRONCLAD** and click **[ LAUNCH EXERCISE ]**
4. Watch the red and blue agents interact across six phases

Do the same for FORGE and EVOLVE. Total time: ~15 minutes. No signup, no cost.

### Tier 2 — 45-Minute Practitioner

You have an OpenRouter key and want to run live AI calls.

1. Read `ATTENDEE-SETUP.md` — it takes 5 minutes
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
ai-village-workshop/
├── README.md             (this file)
├── ATTENDEE-SETUP.md     (API key setup — all four provider options)
├── CLAUDE-CODE-SETUP.md  (use your Claude Code subscription via local helper — no separate API key)
├── OLLAMA-SETUP.md       (fully local, offline Ollama setup)
├── WORKSHOP-GUIDE.md     (paste into claude.ai for contextual help)
├── relay.py              (Claude Code relay — python3 relay.py; spawns `claude -p` per call)
├── demos/
│   ├── tmp-forge-live.html
│   ├── tmp-combat-live.html
│   └── tmp-evolve-live.html
└── labs/
    ├── LAB-1-FORGE.md    (30 min — forge a swarm for your domain)
    ├── LAB-2-COMBAT.md   (45 min — run both scenarios, compare blue detection)
    └── LAB-3-EVOLVE.md   (stretch — close the improvement loop)
```

---

## Cost Estimate

If you run all three labs with a live API key, expect to spend **$0.05–0.15** total on API calls. DEMO MODE is always free.

Recommended model: `anthropic/claude-sonnet-4-6` via OpenRouter.

---

## Getting Help

**During the session:** Talk to the presenter.

**Using an AI assistant:** Open `WORKSHOP-GUIDE.md` and paste its contents into claude.ai (or any chat LLM) before asking your question. The guide gives the AI full context about all three demos, provider options, error messages, and lab flow — so you'll get accurate, specific answers instead of generic troubleshooting advice.

**After the conference:** Open an issue at the GitHub link above.
