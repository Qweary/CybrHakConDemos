# LAB-1 — Forge Your Own Swarm

**Time: ~30 minutes | Select your provider and confirm your key is loaded (see docs/attendee/first-run.md for all options)**

---

## What This Lab Does

You're going to describe something you actually do — a real workflow, a real security function, a real operational domain — and watch the framework design a multi-agent AI system for it from scratch.

The FORGE demo runs a 9-phase pipeline:

| Phase | Agent | What Happens |
|---|---|---|
| P1 | Oppenheimer (Director) | Analyzes your domain, identifies the workflow stages |
| P1b | Lattice | Vector Readiness Assessment — does this domain benefit from a knowledge store? |
| P2 | Domain Advisor | Designs the micro-specialization map — which agents, what each one does |
| P2b | T2→Lattice | Translates the advisor's library spec into a vector collection design |
| **P2c** | **Operator Gate** | **⬥ Interactive pause — read the T2 + Lattice output and click [ ✓ APPROVE ] to continue** |
| P3 | Curie (Research) | Identifies current tooling and techniques for your domain |
| P3b | Fermi (Fabrication) | Builds each agent: name, role, system prompt, tool requirements |
| P4 | Geiger + Bohr (QA) | Validates agents for domain accuracy, structural completeness, and design principles |
| P5 | Packaging | Produces the final swarm package with README and deployment instructions |

---

## Exercise

### Step 1: Open the Demo

Open `http://localhost:3001/forge.html` in your browser (run `python3 relay.py` from the workshop root first if you haven't yet). Or open `web/forge.html` directly via `file://`. Select your provider and confirm your key is loaded (see `docs/attendee/first-run.md`). Enable **[ ⏸ STEP MODE ]** if you want to pause between phases and read each one before continuing.

### Step 2: Write Your Brief

Click **CUSTOM** in the preset selector. A text area appears. Write 2–4 sentences describing:

- What domain or function you work in
- What the main workflow looks like (the steps you repeat)
- What the hardest or most time-consuming part is

**Examples to adapt:**

> I run vulnerability assessments for mid-size enterprise clients. The workflow goes from scoping to recon to scanning to exploitation to reporting. The hardest part is triage — deciding which findings are actually exploitable vs. theoretical.

> I'm a SOC analyst. My day is: ingest alerts, triage, investigate, escalate or close. The bottleneck is context — I spend most of my time trying to understand if an alert is real before I can act on it.

> I do bug bounty on web apps. I start with recon, move to manual testing of auth and business logic, then do a final API-focused sweep before writing the report. The part that takes longest is the auth testing — it's too manual.

You don't have to use security examples. This works for any domain.

### Step 3: Launch and Observe

Click **[ ⚛ INITIATE FISSION ]** (the button is labeled **[ ▶ RUN DEMO ]** if you have DEMO MODE turned on). Watch each phase run.

> **Phase 2c — Operator Gate:** The pipeline pauses here and shows you the T2 Advisor's micro-specialization map and Lattice's vector collection design. Read them, then click **[ APPROVE — PROCEED TO FABRICATION ]** (or modify the spec first, or skip the vector layer). This is the only interactive pause in the pipeline.

Key things to notice:

- How does Oppenheimer decompose your description into workflow stages?
- What names does Fermi give the agents? Do they feel right for your domain?
- Read one or two of the fabricated system prompts — are the tool requirements and domain constraints accurate?
- What does Geiger flag? Does it catch anything Fermi missed?

### Step 4: Reflect

After the run completes, answer these questions (write them down or just think through them):

1. **Decomposition accuracy**: Did the Phase 1 analysis correctly identify the stages of your workflow? What did it miss or get wrong?

2. **Agent design**: Look at the fabricated agents. If you were actually going to use this swarm, which agent would you want to refine first? Why?

3. **System prompt quality**: Pick one fabricated agent and read its full system prompt. Is it specific enough to be useful, or is it too generic? What would you add?

4. **What's missing**: What coordination mechanism would this swarm need that isn't in the fabricated output? (Think about: how do agents hand off state? what shared context do they need? what do they do when they disagree?)

5. **Deploy question**: If you extracted this swarm package and actually ran it, what would be the first real-world test you'd run it against?

---

## If You Have Time: Run It Again

Try a second preset — pick **RED**, **BLUE**, or **INFRA** and run it in Demo Mode (no API cost). Compare how the agent decomposition differs between your custom domain and the pre-built preset. Notice that the agent count, specialization depth, and tool requirements shift significantly based on the domain's coordination complexity.

---

## What Comes Next

The swarm FORGE produces is a starting point, not a finished product. LAB-3-EVOLVE.md shows you the improvement loop: run an exercise, score the agents, rewrite the one that failed, rerun. After several cycles, the agents are tuned to your actual operational conditions rather than the framework's initial best guess.

The forge output from this lab can be pasted into EVOLVE's CUSTOM mode if you want to try the improvement loop on your own swarm.
