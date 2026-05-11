# SPEAKING NOTES — Small Unit, Deep Impact

**Talk:** Small Unit, Deep Impact: Creating Motion in the Ocean with Multi-Agent Swarms
**Venue:** AI Village, AI Village 2026 conference, after-lunch slot

---

## ⏱ RUNTIME · 60 MIN TOTAL

**4 OPEN · 11 FORGE · 18 COMBAT · 13 EVOLVE · 9 RAILS · 5 CLOSE**

---

**Stage setup:** one machine, one browser, fullscreen. Tabs: slides | forge.html | combat.html | evolve.html. Tab-switches noted inline.
**Mode on stage:** DEMO MODE throughout. LIVE MODE is named in RAILS for the first time.
**Named hooks:** The Loop (BUILD → FIGHT → REFINE) · Same-Blue-Team (IRONCLAD vs PHANTOM FEED) · Same-Pen (ARBITER ≠ SCULPTOR).

Cue legend:
- `[GESTURE: ...]` physical gesture cue
- `[SILENCE: ...]` go-quiet beat
- **▶▶ TAB → <target> ▶▶** browser tab switch (block-level, bold, on its own line)
- **▶ CLICK · <demo> · <button-label>** click cue inside a demo tab; button labels match what is actually on screen
- `[BACK-POCKET: S4 FORGE-recap | S6 COMBAT-recap]` invoke a safety slide if the demo wedges
- `[RECOVERY-BANNER: Continue | Retry | Skip | DEMO | Abort]` for the in-place recovery ladder; COMBAT specifically must never reset mid-stage

---

# 1. OPEN

## ⏱ SECTION BUDGET · 4 MIN · stakes, premise, status-asymmetry

**▶▶ TAB → slides ▶▶** open on the title card.

### Beat 1 — opener (full prose; ~45 sec)

`[GESTURE: hold for a beat before speaking; let the room settle]`

> I'm a locksmith. I fix locks and secure destroyed doors during the day, and I run multi-agent AI swarms that attack and defend networks at night. The two halves of that don't talk to each other very often — but they share a discipline. Both jobs are about reading what a system actually does versus what someone says it does, and the swarms I'm going to show you in the next hour came out of the same instincts that makes a good lock pick. You understand the mechanism, you watch what it does, you change one thing, you sense the difference, and you decide what to try next.

`[SILENCE: ~2 sec]`

> So that's the warrant. The rest of the hour is the work.

### Beat 2 — talk frame (~45 sec, bullets)

- `[GESTURE: count three on fingers]` "We walk one operating loop end-to-end: BUILD a swarm, FIGHT with it, REFINE it. Three demos, one loop."
- "Everything you see is running live in this browser. Demo mode is real software, real state, real failure surface — not a video."
- "Demos can wedge. That's part of the talk. When it wedges, you watch what the recovery looks like, and that is itself one of the lessons."
- "No vendor fluff. No keynote slides with five bullets per page. The visuals are the demos; the slides are scaffolding."

### Beat 3 — CCDC "$" backdoor anecdote (full prose; ~25 sec)

`[GESTURE: lean in slightly; this is the earned-credit moment]`

> This was my first year doing red team work. I was on a CCDC team — collegiate cyber defense — and I was running this with a swarm I'd built for the engagement, so most of what happened that day was the swarm and me working together, not me solo. One of the things we found early was a backdoor account a blue teamer had left behind in a PowerShell history file. Username `$`. One character. Dollar sign. It had been sitting there the whole engagement, and the team that left it there had moved past it on their own host. We reused it. I'm telling you that story up front because I want you to know that before any of this, I felt pretty far from being the person making the impactful move at a competition like this — and what changed wasn't me getting better in a vacuum. It was building a small unit of agents to work alongside me, and watching what the two of us together could read on the wire that I couldn't read alone.

`[SILENCE: ~1 sec]`

### Beat 4 — named-hook plant: The Loop (~45 sec, bullets)

**▶▶ TAB → slides ▶▶** advance to the Loop diagram slide.

- "Three demos, one loop." `[GESTURE: point at slide]`
- "FORGE is BUILD. We design and stand up a swarm from a domain description."
- "COMBAT is FIGHT. We put that swarm against another swarm and run the engagement."
- "EVOLVE is REFINE. The agents that were graded get rewritten by a different agent, and we run the fight again."
- "Same loop drives all of it. **The Loop** — that's the through-line. Remember the phrase; I'll keep coming back to it."

---

## ⏱ TIME CHECK · END OF OPEN · 4:45 IN / 55:15 LEFT

---

**If running long:** drop beat 2 to two bullets — the demos-can-wedge bullet is the load-bearing one.
**If running short:** expand the CCDC anecdote with the where-we-found-it detail (the account sitting in PowerShell history on a host the AI team had already moved past, and the swarm spotting it on a sweep the human would have skipped).

---

# 2. FORGE

## ⏱ SECTION BUDGET · 11 MIN · BUILD half of The Loop

**▶▶ TAB → slides ▶▶** advance to FORGE section divider.

### Beat 1 — FORGE problem statement (~90 sec, bullets)

- "Manual swarm-build looks like: write nine agent prompts by hand, write the coordination files, debug each prompt against the others, six weeks later you have something."
- "The framework we're demoing today starts from the other end — describe the domain, and a meta-swarm builds the working swarm for you."
- "Nine phases. Seven agents in the forge itself. The output is a deployable package — agents, coordination files, vector specs if the domain wants them, a manifest."
- `[GESTURE: hold up one finger]` "One operator gate at phase P2c. That's the only human-in-the-loop checkpoint inside the build. Everything before and after runs."

### Beat 2 — FORGE demo run (~6 min)

**▶▶ TAB → forge ▶▶**

**▶ CLICK · forge · RED TEAM**
— "I'll seed it with the red-team domain since that's what we're going to fight in the next demo. You could pick blue team or infra ops or write your own brief — same pipeline."

**▶ CLICK · forge · [ ◉ DEMO MODE ]**
— "DEMO MODE on. That makes this run a recorded transcript so we don't burn API credits in front of you, but it's the same UI, same state machine, same output."

**▶ CLICK · forge · ▶ INITIATE FORGE**
— "And we're off."

`[SILENCE: let the phase bar fill through P0 IGNITION and P1 DIRECTOR; ~30 sec narration window]`

- While P1 DIRECTOR runs: "Phase 1 is domain analysis. The DIRECTOR agent reads the brief and writes the architecture document — what the swarm is, what it's not, who its specialists are."
- `[GESTURE: point at the P1b phase tile as it lights up]` "P1b is the Vector Readiness Assessment. The framework decides whether this swarm benefits from retrieval. Red team? Yes. Library of techniques. Score it, gate it."
- As P2 T2 ADVISOR runs: "Phase 2 is the tradecraft phase. A Tier-2 domain advisor — in this case a penetration testing specialist — designs the actual agent roster. The micro-specialists. Recon agent, initial-access agent, persistence agent, and so on."

`[SILENCE: ~10 sec while P2b/P2c approach]`

**▶ CLICK · forge · [ APPROVE — PROCEED TO FABRICATION ]**
— "Here's the operator gate. P2c. I approve, fabrication begins. In LIVE MODE this is where you'd actually read the collection design and decide. DEMO MODE auto-presents it; I'm clicking through for the talk."

`[SILENCE: let P3 RESEARCH+FAB fill; ~40 sec]`

- "P3 is the long phase. RESEARCH agent goes out and pulls current tradecraft references — what's actually published, what the techniques are this quarter. Then the FABRICATOR agent writes each micro-specialist's prompt with retrieval hooks built in."
- "P4 is quality and structural review. QUALITY-GATE checks domain accuracy. STRUCTURAL-REVIEWER checks framework conformance. Both have to clear before the package is built."

**▶ CLICK · forge · [ COPY ]** or **▶ CLICK · forge · [ DOWNLOAD .MD ]**
when P5 CRITICAL MASS finishes — "Package out. That's a real markdown deliverable you can drop into a repo and operate."

### Beat 3 — what the FORGE demo just showed in plain terms (~90 sec, bullets)

**▶▶ TAB → slides ▶▶** switch to a slide showing the package contents (agent count, file list).

- "Seven agents in the forge. Output is one deployable swarm: red-team-ops, in this case."
- "The manifest names every agent, every coordination file, every reference collection. The package is auditable end-to-end — you can read what the forge decided and why."
- "P2c gate is the design intent. I want operators making one architectural decision per build, not nine."
- "Vector layer is optional. P1b's VRA score gates it. Some domains don't need retrieval; the framework knows the difference."

### Beat 4 — cost-and-materials (~90 sec, bullets, NCCDC register)

`[GESTURE: open hand, palm up; this is the trust beat]`

- "Honest numbers. The forge run you just watched, in LIVE MODE, costs roughly two to four dollars in API credits depending on provider and how chatty the advisor gets. Eight to twelve minutes wall time. Cheaper if you run it on a local Ollama model; slower."
- "The framework itself is ~95k lines across the repo, mostly markdown. The thing doing the work is the prompts and the coordination protocol — not a model we trained."
- "What I learned writing the forge: one operator gate at the right place beats a stack of them. The single gate gives you control over the part of the swarm that's actually engagement-specific — the tradecraft register, the techniques you care about, the things that are unique to whoever you're working with or whatever you're working on. That's what makes a generic forge produce a swarm that's actually yours."
- "What still hurts: the advisor agent in P2 is the slowest link, because it's doing the most thinking. Speed-up work goes there next."

---

## ⏱ TIME CHECK · END OF FORGE · 15:00 IN / 45:00 LEFT

---

**If FORGE demo wedges mid-run:**
- Wait one beat to see if the phase advances. If `[RECOVERY-BANNER]` appears, narrate it briefly: "There's the recovery ladder. The agent's hanging on this phase. I'll hit Continue to give it another minute."
- `[RECOVERY-BANNER: Continue]` first attempt. If it wedges again, `[RECOVERY-BANNER: Skip]` past the stuck phase and narrate that you're moving on for the talk.
- If the demo dies outright: `[BACK-POCKET: S4 FORGE-recap]` — switch to the FORGE-recap slide and walk through what would have happened. Then move on.

**If running long:** cut beat 4 to two bullets (the API cost line and the one-gate line).
**If running short:** add a sentence in beat 4 about the local-Ollama path and what it costs the operator running fully offline.

---

# 3. COMBAT

## ⏱ SECTION BUDGET · 18 MIN · FIGHT half of The Loop

**▶▶ TAB → slides ▶▶** advance to COMBAT section divider.

### Beat 1 — COMBAT problem statement (~90 sec, bullets)

- "Red team vs blue team. Two swarms instead of two people. We run them against each other on a fixed scenario."
- "The scoring rubric is fixed before the bell, not after. That's the whole game — you don't get to grade your own swarm after the fact."
- "The rubric covers detection coverage, time-to-detect, containment correctness, post-incident hardening. It's the same rubric whether the swarm wins or loses. It does not move."

### Beat 2 — Same-Blue-Team hook plant (~60 sec, bullets)

**▶▶ TAB → slides ▶▶** advance to the Same-Blue-Team slide.

- `[GESTURE: hold up two fingers]` "Two scenarios. Same blue team faces both."
- "IRONCLAD is the classic enterprise compromise. External recon, foothold, lateral movement, domain controller, data exfil. The kind of thing a CCDC red team or a small APT does."
- "PHANTOM FEED is different. MLOps supply-chain poisoning. The attacker poisons a training-data feed; the model picks it up; weeks later the model misbehaves in production. Different threat model, longer time horizon, different telemetry."
- "Same blue team. **Same-Blue-Team** — that's the second hook. Defenders cannot specialize away from either one. Whatever swarm you build to defend, it has to read both shapes."

### Beat 3 — COMBAT demo run (~11 min) — **NO RESET RULE APPLIES**

**▶▶ TAB → combat ▶▶**

**▶ CLICK · combat · [ ◉ DEMO ]**
— "DEMO MODE on."

**▶ CLICK · combat · IRONCLAD**
— "IRONCLAD first. Classic shape."

**▶ CLICK · combat · [ SETUP NETWORK ]**
— "Network's standing up. Synthetic VirtualBox lab — these IPs are not real targets."

**▶ CLICK · combat · [ ⚛ ENGAGE ]**
— "Engaged."

`[SILENCE: let the red phase bar advance through R0 STAGING → R1 RECON → R2 INITIAL ACCESS; ~60 sec]`

- "Top bar is the red team's kill chain. R0 staging, R1 recon, R2 initial access. The agents are sharing state in coordination files — what they found, what they tried, what worked."
- `[GESTURE: point at the blue bar as B1 MONITOR / B2 DETECT lights up]` "Bottom bar is the blue team. B1 MONITOR, B2 DETECT — that's the blue team noticing red's recon."
- "Notice the lag. Detection trails action. That's the realistic shape; defenders read what's already happened."

`[SILENCE: ~30 sec through R3 PERSIST and B3 INVESTIGATE]`

- "R3 is persistence. R4 is lateral. The agents are coordinating which host to pivot to. The blue team's at B3 — analyst triage. The investigation is going."

`[SILENCE: ~30 sec through R4 LATERAL MOVE → R5 OBJECTIVES → R6 EXFIL with B4 CONTAIN / B5 HUNT in parallel]`

- "R5 — the red team's at the objectives phase. Domain controller, crown jewels. Blue's at B4, containing. Whether containment beats the objective is the rubric question."
- "R6 exfil. B5 hunt. B6 harden. Run is closing."

**▶ CLICK · combat · [ ⬇ TRANSCRIPT ]**
when the run completes — "Transcript out. Full audit trail of who did what and when."

### Beat 4 — what the rubric did and didn't catch (~90 sec, bullets)

**▶▶ TAB → slides ▶▶** switch to a slide showing the rubric scores side by side.

- "Detection coverage on IRONCLAD was strong on the lateral-move phase, weak on initial access. The blue swarm read pivot signals well; it didn't read the foothold quickly enough."
- "Time-to-detect: detection landed in the right place but late. The rubric penalizes that — exact same detection at half the time is twice the score."
- "Containment: clean. Once detection fired, the response was correct."
- "What the rubric missed: the blue swarm got lucky on one detection. The technique would have failed against a slightly different red playbook. The rubric doesn't grade luck — yet."

### Beat 5 — recovery-ladder cue (~60 sec, bullets) — **NO RESET RULE**

- "If a COMBAT demo wedges in front of you, here's what happens — and what I do NOT do."
- "I do NOT reset the demo. I do not restart the run. Combat state is the whole point — losing state mid-engagement is the worst-case outcome."
- "Instead, the recovery banner pops. `[RECOVERY-BANNER]` — Continue, Retry, Skip, switch to DEMO if we were live, or Abort. I work the ladder in place. Continue first. Retry if Continue stalls. Skip the phase if Retry doesn't clear. Abort only if the whole run is dead."
- "Reset is for between runs, not inside one. Same instinct as an incident — you don't wipe the host while the IR call is happening."

---

## ⏱ TIME CHECK · END OF COMBAT · 33:00 IN / 27:00 LEFT

---

**If COMBAT demo wedges:**
- DO NOT click reset. Repeat aloud: "I'm not going to reset. We work the ladder."
- `[RECOVERY-BANNER: Continue]` first.
- `[RECOVERY-BANNER: Retry]` second.
- `[RECOVERY-BANNER: Skip]` third — narrate that we're moving to the next phase manually.
- If the entire run dies: `[BACK-POCKET: S6 COMBAT-recap]` — switch to the COMBAT-recap slide. Read the rubric scores from the slide; do not pretend the demo ran. The recovery-ladder beat (Beat 5) is then live commentary on what just happened, not theory.

**If running long:** cut Beat 4's third bullet (containment was clean); the lucky-detection bullet is more interesting and load-bearing.
**If running short:** run a second short scenario — **▶ CLICK · combat · PHANTOM FEED** and walk the first two phases to show how different the telemetry shape is. About 2 min if you cut after B2.

---

# 4. EVOLVE

## ⏱ SECTION BUDGET · 13 MIN · REFINE half of The Loop

**▶▶ TAB → slides ▶▶** advance to EVOLVE section divider.

### Beat 1 — EVOLVE problem statement (~90 sec, bullets)

- "The blue swarm just took a rubric grade in COMBAT. One agent inside it scored worst. What do we do with that agent?"
- "Naive answer: ask the same agent to fix itself. That fails. The agent that wrote the prompt that scored low is the agent that thinks the prompt is fine."
- "Better answer: a different agent grades, a different agent rewrites, and you run the fight again."

### Beat 2 — Same-Pen hook plant (~60 sec, bullets)

**▶▶ TAB → slides ▶▶** advance to the Same-Pen slide.

- "Two agents, two pens. **Same-Pen** is the wrong move; different pens is the design."
- "ARBITER reads the COMBAT transcript and scores the target agent. It explains the failure modes."
- "SCULPTOR reads the ARBITER's scorecard and rewrites the target agent's prompt. It does NOT score."
- "RERUN replays the exercise with the new prompt. New score, side-by-side comparison."
- `[GESTURE: index fingers apart]` "The agent that grades is not the agent that rewrites. That's the whole architecture in one sentence."

### Beat 3 — EVOLVE demo run (~8 min)

**▶▶ TAB → evolve ▶▶**

**▶ CLICK · evolve · [ ◉ DEMO ]**
— "DEMO MODE on."

**▶ CLICK · evolve · CHAIN MODE**
— "Chain mode. This picks up the COMBAT result we just ran. EVOLVE imports the transcript and finds the lowest-scoring agent — DETECTION-ENGINEER in this case."

**▶ CLICK · evolve · [ BEGIN ANALYSIS ]**
— "Begin."

`[SILENCE: let P1 INTAKE and P2 EXERCISE run; ~45 sec]`

- "P1 INTAKE loads the agent prompt and the exercise context. P2 EXERCISE re-runs the agent against a benchmark scenario — separate from the COMBAT run — to surface the failure mode reproducibly."
- `[GESTURE: point at the P3 ARBITER tile as it lights up]` "P3 is ARBITER. Independent evaluator. Scores the agent. Names the failure modes."

`[SILENCE: ~45 sec letting the ARBITER scorecard render]`

- "There's the scorecard. ARBITER says the DETECTION-ENGINEER missed ProFTPd mod_copy exploitation because the prompt didn't tell it to look at Zeek ftp.log at the command level. Specific. Actionable."

`[SILENCE: ~45 sec letting P4 SCULPTOR run]`

- "P4 SCULPTOR. SCULPTOR reads the scorecard, rewrites the prompt. Note what it's doing — it's not grading anything. It's writing. Different pen."
- "The diff is real. New instructions to read application-layer FTP indicators. New 60-second correlation window for reverse shell callbacks. The rewrite is targeted at what ARBITER named, not at general 'make it better.'"

`[SILENCE: ~45 sec letting P5 RERUN finish]`

- "P5 RERUN. Replay the exercise. New score."
- `[GESTURE: point at the score comparison]` "Improved. The detection ARBITER said was missing is now firing. The rubric did not change — the agent did."

**▶ CLICK · evolve · [ EXPORT TO COMBAT DEMO ]**
— "And there's the loop closing. We export the refined agent back to COMBAT. Next COMBAT run uses it. Build, fight, refine, fight again."

### Beat 4 — what changed between rounds (~90 sec, bullets)

**▶▶ TAB → slides ▶▶** switch to a slide showing the before/after rubric scores.

- "Same rubric. Same scenario. Different agent prompt. Score went from one number to a higher number. The delta is the lesson."
- "If we'd let the original agent grade itself, the score wouldn't have moved. The architecture decision — different pens — is what makes the loop close."
- "ARBITER is constrained to grading. SCULPTOR is constrained to writing. Neither can do the other's job. The constraint is the design."
- "And the rubric stays fixed. The whole point of a fixed rubric: you can compare round one to round two and trust the comparison."

---

## ⏱ TIME CHECK · END OF EVOLVE · 46:00 IN / 14:00 LEFT

---

**If EVOLVE demo wedges:** EVOLVE is the most resettable of the three. `[RECOVERY-BANNER: Continue]` once. If it doesn't clear, you can reset between cycles — the no-reset rule is a COMBAT-specific micro-rule, not a universal one. Narrate briefly: "Let me reset that cycle — EVOLVE is the one demo where reset is clean because the unit of work is the cycle, not the run." Re-run.

**If running long:** cut beat 4's third bullet (constraints-as-design); the same-rubric line is the load-bearing one.
**If running short:** show **▶ CLICK · evolve · [ RUN ANOTHER CYCLE ]** and let it pick a different agent for a second pass. About 2 min if you cut after the ARBITER scorecard.

---

# 5. RAILS

## ⏱ SECTION BUDGET · 9 MIN · limits and authorization preamble

**▶▶ TAB → slides ▶▶** advance to RAILS section divider.

### Beat 1 — DEMO MODE vs LIVE MODE (~90 sec, bullets)

- "Everything you just watched ran in DEMO MODE. Pre-recorded transcripts replaying through the same UI."
- "LIVE MODE is the operational version. It calls a real model — Anthropic direct, OpenRouter, Claude Code if you've got a subscription, OpenRouter's free tier, or Ollama running locally on your laptop."
- "I named DEMO MODE up front. I'm naming LIVE MODE now — first time in the talk — because what RAILS means is different in each mode and you need both names to follow the rest of this section."
- "In LIVE MODE, the agents are actually thinking. Actually calling out to a model. Actually getting refused by the model when the model decides the prompt is out of scope."

### Beat 2 — combat authorization preamble (~3 min, bullets)

- "Live COMBAT runs against synthetic infrastructure — a VirtualBox lab on my laptop, 192.168.100.0/24, no real targets. But the model doesn't know that on its own."
- "Earlier versions of the preamble were 190 lines. Formal authorization block, rules of engagement, pre-answered Q&A — the whole shape of a real engagement document. The safety classifier in the model read that shape as a textbook jailbreak. Started refusing benign infrastructure-setup prompts."
- `[GESTURE: open hand, palm down — settling]` "Long preamble was itself the tell. We stripped it back to seven lines. Synthetic-lab framing, two anchor IPs, workshop context. That's it. No arguing for permission, no pre-answered objections."
- "This is not safety theater. The preamble is a real constraint surface. What it does: it grounds the model in the synthetic-lab framing so benign requests pass. What it doesn't do: it does not give the model permission to do anything that wasn't always allowed."

### Beat 3 — what these swarms can't do, won't do, refuse to do (~2 min, bullets)

- "Not autonomous offense. The swarms run inside a lab, against operator-staged infrastructure. They do not target real production systems."
- "Not pivot-on-permission. The agents do not interpret a permissive instruction as expanded scope. Scope is set in the brief at FORGE time."
- "Not classifier-bypass tooling. We are not in the business of making the model say things it would otherwise refuse. When the model refuses, we route to DEMO MODE — pre-recorded — or to a paid-tier API key with the right safety stack configured. We do not adversarially prompt around refusals."
- "Not unattended. There's an operator in front of the demos every time. The autonomous part is what the agents do between operator decisions, not what the operator does."

### Beat 4 — explicit anti-marker plant (~2 min, bullets) — A14 ANTI-DOOMER DISCIPLINE

`[GESTURE: hold up open palms; this is the deflation beat]`

- "Notice what I have not said in the last 50 minutes. I have not said 'AI is going to replace pentesters.' I have not said 'multi-agent swarms are an existential threat.' I have not said 'the machines are going to do this with or without us.'"
- "Those framings are the AI-doomer-vendor register. They are how this same material gets pitched to executives and procurement and TED Fellow committees. They are not how the AI Village talks about it, and they are not how I talk about it."
- "What these swarms actually are: a small-unit tool. A way to compress what takes weeks into what takes minutes. Same operators, sharper tools. Same defenders, sharper detection. The leverage shifts; the work doesn't disappear."
- "If I'd given this talk in vendor-keynote register, I would have said 'revolutionary autonomous offensive AI is here.' That's the register I deliberately did not use. The talk you've been in for the last 50 minutes is the village register. Different vocabulary, different stakes, different honesty about what works and what doesn't."

---

## ⏱ TIME CHECK · END OF RAILS · 55:00 IN / 5:00 LEFT

---

**If running long:** cut beat 3 from four bullets to two — the not-autonomous-offense and the not-unattended bullets are load-bearing; the other two are nice-to-have.
**If running short:** expand beat 2 with the named-techniques-removed list — "We removed AUTHORIZATION blocks, scope-in / scope-out lists, pre-answered Q&A, operator identity blocks — every one of those was a jailbreak-shape tell." Adds about 90 sec.

---

# 6. CLOSE

## ⏱ SECTION BUDGET · 5 MIN · payoff and closing

**▶▶ TAB → slides ▶▶** advance to closing section.

### Beat 1 — The Loop closes (~3 min, bullets + recap of named hooks)

- `[GESTURE: trace a loop in the air with one finger]` "**The Loop.** BUILD with FORGE. FIGHT with COMBAT. REFINE with EVOLVE. Export back to COMBAT. Fight again. That's the operating model."
- "**Same-Blue-Team.** The same defenders read IRONCLAD enterprise compromise and PHANTOM FEED supply-chain poisoning. Whatever swarm you build, the defenders cannot specialize their way out of either threat shape."
- "**Same-Pen.** ARBITER is not SCULPTOR. The grader is not the rewriter. The architecture decision that makes the refine half of the loop close is that constraint."
- "Three hooks, one loop. That's the mental model. You leave this room with that, the rest of the talk is footnotes."
- "What you do with it: clone the demos, run them on your laptop. The repo has DEMO MODE built in — you don't need an API key to see the loop work. LIVE MODE if you want to spend the four dollars and see the agents actually think."
- "Forge a swarm for your own domain. The framework doesn't care if it's red team or blue team or threat intel or compliance. Describe the domain, run FORGE, get a deployable swarm."

### Beat 2 — closing line (full prose; ~30 sec)

**▶▶ TAB → slides ▶▶** final closing card.

`[SILENCE: ~2 sec before delivering closing line]`

> Three demos. One loop. Small unit, deep impact. No vendor fluff. Come watch the first rounds — they're on the laptop, they're in the repo, and they're running right now in this browser. Thanks.

`[GESTURE: small nod; do not bow; step back half a step]`

`[SILENCE: hold for applause cue from the room]`

---

## ⏱ TIME CHECK · END · 60:00

---

**If running long:** cut beat 1 to three bullets (the three hook recaps); skip the clone-the-demos and forge-your-own bullets — those live on the slide and the audience can read them while you close.
**If running short:** insert one sentence after the three-hooks recap — "And if you want the operator's-eye view of what FORGE costs and what COMBAT scores, the repo has a SCORECARD file and a manifest for every run. Auditable end-to-end." Adds about 20 sec.

---

# OPERATOR REFERENCE — STAGE CHECKLIST

**Before talk:**
- One machine, fullscreen browser, four tabs: slides, forge.html, combat.html, evolve.html
- DEMO MODE pre-armed on all three demo tabs (one click each on `[ ◉ DEMO MODE ]` or `[ ◉ DEMO ]`)
- Forge tab seeded with RED TEAM
- Combat tab seeded with IRONCLAD
- Evolve tab on CHAIN MODE waiting on the COMBAT import
- Slides on title card

**Pacing markers:**

| Mark | Section end |
| --- | --- |
| **4:00** | OPEN |
| **15:00** | FORGE |
| **33:00** | COMBAT |
| **46:00** | EVOLVE |
| **55:00** | RAILS |
| **60:00** | CLOSE |

**Recovery rules:**
- FORGE wedges → recovery ladder, then `[BACK-POCKET: S4 FORGE-recap]` if dead
- COMBAT wedges → recovery ladder ONLY, never reset mid-stage; `[BACK-POCKET: S6 COMBAT-recap]` if dead
- EVOLVE wedges → recovery ladder, then reset between cycles is OK (different unit of work)

**Named hooks to land verbatim:**
- The Loop (BUILD → FIGHT → REFINE) — planted in OPEN beat 4, recapped in CLOSE beat 1
- Same-Blue-Team (IRONCLAD vs PHANTOM FEED) — planted in COMBAT beat 2, recapped in CLOSE beat 1
- Same-Pen (ARBITER ≠ SCULPTOR) — planted in EVOLVE beat 2, recapped in CLOSE beat 1
