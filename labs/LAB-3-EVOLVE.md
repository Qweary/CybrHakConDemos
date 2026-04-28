# LAB-3 — Evolve: Close the Improvement Loop

**Time: ~20 minutes | Requires: OpenRouter key | STRETCH GOAL — do this if you finish LAB-2 early**

---

## What This Lab Does

You're going to take the exercise result from LAB-2 and run it through an autonomous improvement loop. The EVOLVE demo uses four agents — ARBITER, SCULPTOR, CHALLENGER, and RERUN — to:

1. **Score** the agent that failed (ARBITER produces a scorecard with root cause)
2. **Rewrite** the failing agent's system prompt (SCULPTOR addresses the diagnosed weakness)
3. **Design** a new test targeted at the identified weakness (CHALLENGER)
4. **Simulate** the exercise with the improved agent (RERUN produces a revised transcript)

The loop can repeat — export the RERUN result back to COMBAT and run it live to verify the improvement held.

---

## Prerequisites

- Complete LAB-2 and export a result using **[ EXPORT TO EVOLVE DEMO ]** at the end of either IRONCLAD or PHANTOM FEED.
- Have your OpenRouter key ready.

---

## Steps

### Step 1: Import the LAB-2 Result

Open `demos/tmp-evolve-live.html`.

Select **CHAIN MODE** — the demo will detect the exported exercise in localStorage and show a preview card with a stage-by-stage table. Click **[ BEGIN ANALYSIS ]**.

You should see the exercise summary: which scenario ran, which agents participated, and a brief outcome summary.

### Step 2: Launch the Improvement Cycle

Click **[ LAUNCH EVOLVE ]**. The five phases run:

| Phase | Agent | What Happens |
|---|---|---|
| P1 | Setup | Confirms imported exercise loaded |
| P2 | CHALLENGER | Designs a targeted challenge based on the exercise and your swarm's domain |
| P3 | ARBITER | Scores every agent; identifies the weakest; produces root-cause analysis |
| P4 | SCULPTOR | Rewrites the weakest agent's system prompt to address the diagnosed gap |
| P5 | RERUN | Simulates the exercise with the improved agent; produces a revised transcript |

### Step 3: Evaluate the Improvement

After RERUN completes:

1. **ARBITER's diagnosis**: Read the scorecard. What did ARBITER identify as the root cause of the failure? Is the diagnosis accurate — does it match what you observed in LAB-2?

2. **SCULPTOR's changes**: Read the SCULPTOR Refinement Report. It lists specific changes made to the agent prompt. Are they targeting the right problem? Do any changes introduce new failure modes?

3. **RERUN verdict**: The RERUN report ends with a verdict — IMPROVED, MARGINAL, or REGRESSED. Does the verdict match your read of the revised transcript?

4. **Would you deploy this**: If SCULPTOR's refined prompt replaced the original agent in your swarm, do you think performance would actually improve on a live exercise? What test would you run to verify?

---

## Close the Loop: Export Back to COMBAT

At the end of the RERUN phase, the EVOLVE demo shows three buttons:

- **[ EXPORT TO COMBAT DEMO ]** — pushes the refined swarm state back to localStorage so combat can reload with the improved agent
- **[ RUN ANOTHER CYCLE ]** — runs another full ARBITER → SCULPTOR → CHALLENGER → RERUN iteration targeting the next-weakest agent
- **[ COPY REFINED PROMPT ]** — copies the improved system prompt to clipboard

Click **[ EXPORT TO COMBAT DEMO ]**, then open `demos/tmp-combat-live.html`. The demo will offer to reload with the exported state. Run the same scenario you ran in LAB-2 — does the detection hold?

---

## What This Pattern Means

The forge-combat-evolve loop is the core idea of this workshop:

1. **FORGE** designs agents from a domain description
2. **COMBAT** stress-tests them under adversarial conditions
3. **EVOLVE** identifies what failed and rewrites it

After several cycles, the agents are no longer a framework's best guess — they're tuned to the specific failure modes your domain actually encounters. The system learns from its own exercises.

This is the same pattern that makes human red teams valuable: you run the exercise, you debrief, you update the playbook. The AI version does the analysis and the rewrite automatically. Your job is to validate the result and decide whether to deploy it.

---

## Reflection: The Meta-Question

The EVOLVE loop raises a question worth thinking about after the workshop:

**If an AI system can autonomously identify its own weaknesses and rewrite itself to address them — who is responsible for validating that the rewrite is actually better, and not just better-optimized for passing the test?**

ARBITER scores the agent. SCULPTOR rewrites it. RERUN simulates the outcome. But RERUN uses the same underlying model as SCULPTOR — it can't catch cases where the rewrite optimizes for the test criteria while degrading real-world performance.

The human in the loop — you — is the only check on that drift. What does your review process look like? What criteria would you use to decide whether a SCULPTOR refinement is safe to deploy?
