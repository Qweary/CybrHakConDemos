# Slide Content Spec — "Small Unit, Deep Impact"

AI Village 2026 · hour-long after-lunch talk · 13 slide specs (11 visible + 2 back-pocket)

This is the slide content specification consumed by S+3 to build the reveal.js deck. Every slide here is one frame on screen. Operator drives tab-switching between this deck and the three demo tabs (forge.html / combat.html / evolve.html). The deck does not embed or proxy the demos; slides are scaffolding between demo runs.

Companion artifact: SPEAKING-NOTES.md (drafted in parallel by SMYTH-A; cue-line reconciliation across both files is Neo's S+2 close).

---

## Aesthetic spec

Values below are extracted from the demo CSS at /home/qweary/Desktop/CybrHakConDemos-pr-prep/web/ — read-from-source, not from memory. Memory's notes are consistent with what was read.

- **Background:** `--bg: #040407` (matches index.html and forge.html — the first demo tab the audience sees). combat.html and evolve.html run a slightly deeper `#020208`; the variance is below visual threshold under projection. Use `#040407` for deck baseline. Surface for operator iteration if a pixel-exact match to combat is preferred — alternative branch: `#020208` for tighter combat continuity at the cost of FORGE-tab continuity.
- **Panel background:** `--bp: #07070e` for any inset boxes / diagram backgrounds.
- **Borders:** `--bdr: #0e0e1c` (forge/index) — 1px solid, no rounding except where demos use `border-radius: 2px` on recovery banners (reproduce that exact 2px radius for the back-pocket recovery-styled slides).
- **Primary text (amber):** `--a: #f0a500` for chapter-divider titles and primary on-slide labels; `--am: #d08800` for subtitle / muted-amber labels. Glow on titles: `text-shadow: 0 0 10px rgba(240,165,0,.38)` (matches `--ga` from index.html).
- **Body text (off-white):** `--w: #d4d4e8` for body copy on slides that have body copy.
- **Section accent colors** (use sparingly — these are the "section tag" colors, one per section, matching the demo tab the section will tab to):
  - FORGE: amber `--a: #f0a500` (forge.html's primary)
  - COMBAT: red `--r: #ff1744` (combat.html banner color) and blue `#4fc3f7` (blue-team color) for any red-vs-blue diagrams
  - EVOLVE: purple `--p: #ce93d8` (evolve card color from index.html, matches evolve's identity tint)
  - RAILS: amber `--am: #d08800` (muted; RAILS is the structural-grounding section, not a hype color)
- **Typography:** Share Tech Mono for body and section labels; Orbitron 900 for chapter-divider titles and the title card. Both fonts are already loaded on demo pages via Google Fonts — reveal.js HTML build links the same family.
- **Size hierarchy:** title card ~64px Orbitron / chapter dividers ~48px Orbitron / mid-section labels ~24px Share Tech Mono / body ~18–22px Share Tech Mono. Letter-spacing on Orbitron blocks: 3px (matches demo hdr `.ht` style).
- **Slide aspect ratio:** 16:9.
- **Transitions:** instant cut (`transition: 'none'` in reveal.js config). No fade, no slide-in.
- **Scanline overlay:** consider reproducing the demo's `body::after` scanline (`repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,0,0,.055) 3px,rgba(0,0,0,.055) 4px)`) as a global reveal.js overlay for kayfabe-aesthetic continuity. Operator-iterable; the scanline is a strong continuity move but may read as visual noise under projector compression. Default ON; allow off in S+3 dry-run review.
- **Cursor blink:** chapter-divider slides MAY end the title with a blinking `█` block-cursor character (CSS `animation: blink .8s infinite` per demo `.pstat.active-r`). Operator-iterable. Default OFF on title card (clean opener); default ON on the chapter dividers as a "the section is live" cue.
- **No bullet points anywhere.** Every slide is one of: (a) chapter title + diagram, (b) a single concrete quote or payoff line, (c) a structural visualization (phase bar, role-separation, rubric structure). No summarizing-bulleted-recaps — the demos and the speaker carry the recap; slides do not.
- **Back-pocket placement:** S4 and S6 sit at the END of the deck (after S11), at addressable routes `#/forge-recap` and `#/combat-recap`. Forward-arrow nav from S11 does NOT advance into the recap slides; they only display when the operator types the route or clicks a hidden bookmark. This protects against accidental reveal during the live talk.

---

## Visible sequence (11 slides)

### S1 — Title card

- **Section anchor:** OPEN
- **Title:** SMALL UNIT, DEEP IMPACT
- **On-slide text:**
  ```
  SMALL UNIT, DEEP IMPACT
  Creating Motion in the Ocean with Multi-Agent Swarms

  AI VILLAGE · 2026
  ```
  Subtitle line in `--am`; village/year line in `--gr: #8080aa`, smaller. ~18 words on-slide.
- **Visual artifacts needed:** Centered text only. Optional: a single faint `█` cursor at end of subtitle line (default OFF on title; clean opener).
- **What operator says when slide goes up:** Slide is up from before the operator starts. Operator's opening line lands without slide reference: "I'm Qweary. Day job, locksmith. Night job, this." (or whichever status-asymmetry opening SMYTH-A drafts in OPEN beat 1). Slide functions as backdrop, not as content.
- **When slide is dismissed:** Operator advances to S2 at the named-hook plant — when they say something on the order of "the whole talk is one loop — build, fight, refine." Advance is forward-only.
- **Time-budget:** ~3 min visible (most of OPEN's 4 min).

---

### S2 — The Loop (named-hook plant)

- **Section anchor:** OPEN → FORGE transition
- **Title:** (none on slide — the diagram IS the slide)
- **On-slide text:**
  ```
  BUILD ─→ FIGHT ─→ REFINE
                          ╰────────────╯
                          (and back to BUILD)
  ```
  Three labels in `--a` amber, large Orbitron 900, arranged horizontally. Arrow from REFINE looping back to BUILD drawn with ASCII (`╰─→─╯`) or with a styled SVG curve in the S+3 build — operator preference, default ASCII for terminal-aesthetic. ~9 words on-slide.
- **Visual artifacts needed:** Three labels + the loop arrow. No icons. No animation on first land; if the deck allows, a one-shot draw-in of the loop-back arrow when the operator presses space is acceptable but not required.
- **What operator says when slide goes up:** "The whole talk is one loop. Build a swarm. Fight with it. Refine what broke. And back to build." The slide plants the structural promise for the rest of the talk.
- **When slide is dismissed:** Operator tab-switches to forge.html tab when ready to start FORGE. The cue line is on the order of "Let's start with build."
- **Time-budget:** ~1 min visible (last beat of OPEN).

---

### S3 — FORGE chapter divider

- **Section anchor:** FORGE start
- **Title:** FORGE
- **On-slide text:**
  ```
  FORGE                            █
  ─── BUILD ───
  9 phases · domain in · swarm out
  ```
  FORGE title in `--a` amber Orbitron 900 ~64px with `--ga` glow. "BUILD" subtitle in `--am` muted amber. The tagline line in `--w` off-white, smaller. Cursor block at end of title. ~13 words on-slide.
- **Visual artifacts needed:** Optional small phase-bar visualization underneath the tagline — 9 cells in a row, sized like the forge.html phase bar, each cell labeled P1 / P2 / ... / P9 in `#484870` (matches forge inactive-phase color). The phase bar is decorative continuity; it does NOT advance during the demo (operator tab-switches to forge.html for the real bar). If the S+3 build is time-constrained, omit the phase bar — the title + tagline carry the slide.
- **What operator says when slide goes up:** "FORGE. The build half. Nine phases. You describe a domain in plain language; you get a deployable swarm package out the other end. Watch." Then tab-switch to forge.html.
- **When slide is dismissed:** Immediately after the cue line above. Operator's next action is tab-switching to forge.html and clicking [DEMO MODE].
- **Time-budget:** ~30 sec visible (chapter divider; the demo carries FORGE).

---

### S4 — COMBAT chapter divider (Same-Blue-Team hook plant)

- **Section anchor:** COMBAT start
- **Title:** COMBAT
- **On-slide text:**
  ```
  COMBAT                           █
  ─── FIGHT ───
  same blue team · two threat models
  IRONCLAD   //   PHANTOM FEED
  ```
  COMBAT title in `--r: #ff1744` red Orbitron 900 ~64px with red glow (`0 0 10px rgba(255,23,68,.45)` — matches combat card hover). "FIGHT" subtitle in `--rm: #e02040`. The "same blue team / two threat models" line in `--w` off-white. The "IRONCLAD // PHANTOM FEED" line as two boxes side-by-side, IRONCLAD bordered in red `--r`, PHANTOM FEED bordered in red `--r` with a subtle dashed border indicating "unauthorized." ~14 words on-slide.
- **Visual artifacts needed:** Title block + two side-by-side scenario boxes. IRONCLAD box (solid border) labeled "AUTHORIZED · enterprise compromise." PHANTOM FEED box (dashed border) labeled "UNAUTHORIZED · MLOps supply chain." Same-blue-team line spans across both boxes. No icons.
- **What operator says when slide goes up:** "COMBAT. Two swarms — red and blue — run a six-phase adversarial exercise. The blue team is the same blue team. The threat model changes. IRONCLAD: enterprise compromise, the blue team is in scope. PHANTOM FEED: MLOps supply-chain poisoning, the blue team is NOT in scope and has to figure out it's being attacked from data it never asked for." This plants the Same-Blue-Team hook for the EVOLVE callback later.
- **When slide is dismissed:** Tab-switch to combat.html when operator says "Watch IRONCLAD first." Forward-only from here through the COMBAT section.
- **Time-budget:** ~1 min visible.

---

### S5 — Rubric structure (COMBAT mid-section)

- **Section anchor:** COMBAT mid
- **Title:** RUBRIC
- **On-slide text:** (slide is largely diagram; text is sparse)
  ```
  RUBRIC

  scored against a rubric
  fixed before the bell, not after.
  ```
  RUBRIC label in `--am` muted amber, smaller than chapter-divider titles. The two-line quote in `--w` off-white, Share Tech Mono ~28px, second line indented to match prose-quote style. The quote is verbatim from the locked v7 blurb. ~12 words on-slide.
- **Visual artifacts needed:** Rubric-structure visualization beneath the quote. ASCII table or styled HTML table showing the rubric structure — 4–5 categories scored 0–10, with sample category labels drawn from combat.html's actual ARBITER scorecard format:
  ```
  ┌──────────────────────────────┬───────┐
  │ DETECTION COVERAGE            │  ?/10 │
  │ TIME-TO-DETECT                │  ?/10 │
  │ ANALYST WORKFLOW FIDELITY     │  ?/10 │
  │ ARTIFACT QUALITY              │  ?/10 │
  │ ROOT-CAUSE ATTRIBUTION        │  ?/10 │
  └──────────────────────────────┴───────┘
                                  TOTAL  ?/50
  ```
  Category labels above are placeholders — S+3 should pull the actual category labels from combat.html's `## ARBITER SCORECARD` blocks (line ~721, ~839, ~957 in combat.html). The "?/10" cells are intentionally empty — the slide visualizes the STRUCTURE of the rubric, not a specific score. The point lands when the slide says "the cells are empty because the rubric is fixed before either team runs."
- **What operator says when slide goes up:** "How do we know who won? You don't ask the blue team. You don't ask the red team. You score both of them against a rubric — and the rubric was written before either team ran. Same rubric, both scenarios. The cells you see are empty here on purpose." Then a beat, then either tab back to combat.html for a SCORE PANEL reveal or continue narration into S6.
- **When slide is dismissed:** Forward to S6 (EVOLVE divider) OR back to combat.html tab for a second IRONCLAD-vs-PHANTOM-FEED segment if operator runs both COMBAT scenarios mid-section. Forward-only through slide sequence — slide does not allow back-nav to S4.
- **Time-budget:** ~1–2 min visible across the COMBAT section.

---

### S6 — EVOLVE chapter divider (Same-Pen hook plant)

- **Section anchor:** EVOLVE start
- **Title:** EVOLVE
- **On-slide text:**
  ```
  EVOLVE                           █
  ─── REFINE ───
  same pen · different hand
  the agent that grades is not the agent that rewrites.
  ```
  EVOLVE title in `--p: #ce93d8` purple Orbitron 900 ~64px with purple glow `--gp`. "REFINE" subtitle in muted purple `#9e6cb0`. The "same pen / different hand" line in `--w` off-white. The "the agent that grades is not the agent that rewrites" line is verbatim from locked v7 blurb, in `--w` off-white slightly smaller. ~18 words on-slide.
- **Visual artifacts needed:** Title block + the two-line callout. No diagram on this slide — the diagram lives on S7.
- **What operator says when slide goes up:** "EVOLVE. The refine half. The agent that scored your blue team — that's the same agent that's going to score the rewrite. But it's not the agent that does the rewriting. Same pen, different hand. The grader doesn't get to mark its own paper." Plants the Same-Pen hook.
- **When slide is dismissed:** Advance to S7 when operator says something on the order of "Here's how the cycle runs."
- **Time-budget:** ~45 sec visible.

---

### S7 — ARBITER / SCULPTOR / RERUN cycle (EVOLVE mid-section)

- **Section anchor:** EVOLVE mid
- **Title:** THE CYCLE
- **On-slide text:**
  ```
  THE CYCLE

      ARBITER  ──score──→  SCULPTOR  ──rewrite──→  RERUN
         ↑                                            │
         └────────────re-score────────────────────────┘

  rubric fixed before the bell.
  ```
  Three role labels in `--p: #ce93d8` purple Orbitron 700, equal weight (the role separation is the point — none of the three roles is hierarchically above the others). Arrows in `--am` muted amber. The closing tagline "rubric fixed before the bell." in `--w` off-white. ~12 words on-slide.
- **Visual artifacts needed:** ASCII or vector diagram showing three boxes labeled ARBITER, SCULPTOR, RERUN with arrows: ARBITER → SCULPTOR (labeled "score" — the trigger to rewrite is ARBITER's verdict), SCULPTOR → RERUN (labeled "rewrite" — the artifact passed to RERUN is the rewritten prompt), RERUN → ARBITER (labeled "re-score" — the cycle closes when ARBITER scores the new run). The "rubric fixed before the bell" annotation sits beneath the diagram, NOT inside it. The cycle's role separation is load-bearing: ARBITER does not rewrite; SCULPTOR does not score; RERUN does not judge. State this in S+3 implementation comments next to the diagram so the visual reproduces the three-role separation cleanly.

  Branch for operator iteration: alternative could be a code-mock of a rubric-fixed evaluation step (a snippet of the ARBITER prompt's scoring criteria literally fixed before the cycle begins). The role-separation diagram is the recommended choice because Same-Pen is a structural hook and the diagram visualizes the structure; the code-mock would be a separate teaching angle. Default to the diagram; surface code-mock alternative in S+3 dry-run for operator iteration.
- **What operator says when slide goes up:** "ARBITER scores the blue team. Reads the same rubric that scored the live exercise. SCULPTOR takes ARBITER's findings and rewrites the weakest agent's prompt. RERUN replays the same exercise — same input, new prompt — and we get a new score. Same rubric. Same blue team. Different hand on the pen."
- **When slide is dismissed:** Tab-switch to evolve.html when operator says "Let me show you a cycle running."
- **Time-budget:** ~1–2 min visible across EVOLVE section.

---

### S8 — Rubric, persisted (scoring structure detail)

- **Section anchor:** EVOLVE mid (paired with S7)
- **Title:** WHY THE RUBRIC SURVIVES
- **On-slide text:**
  ```
  WHY THE RUBRIC SURVIVES

  round 1 :  rubric →  exercise →  ARBITER score
  round 2 :  SAME rubric →  rerun  →  ARBITER score
  round 3 :  SAME rubric →  rerun  →  ARBITER score

  the score is the diff. the rubric is the bell.
  ```
  Header in `--am`. Three round-lines in `--w` off-white, monospaced alignment. "SAME" in `--p` purple, capitalized for emphasis. Closing line in `--a` amber, slightly larger. ~26 words on-slide — this slide is denser than the others by design, because it carries the punchline of why the rubric-fixed-before-the-bell discipline matters.
- **Visual artifacts needed:** Just the structured text. No diagram. The repeating "SAME rubric" is the visual point — three rows, same column-1 value, different column-3 values (the scores).

  Branch for operator iteration: this slide may be redundant with S7 + speaker narration. If S+3 dry-run determines the speaker carries this point without slide support, S8 drops and the deck goes to 10 visible. Default keep — the slide is the only place "the score is the diff. the rubric is the bell." appears on-screen, and that tagline is operator-voice-load-bearing. Surface in dry-run for keep/drop decision.
- **What operator says when slide goes up:** "Round one, round two, round three — same rubric on every run. The scores move; the rubric does not. The score is the diff between the agent's behavior in round N and round N-plus-one. The rubric is the bell that says where the round starts."
- **When slide is dismissed:** Forward to S9 when operator transitions from EVOLVE narration to the RAILS section.
- **Time-budget:** ~1 min visible.

---

### S9 — RAILS chapter divider

- **Section anchor:** RAILS start
- **Title:** RAILS
- **On-slide text:**
  ```
  RAILS                            █
  ─── HOW THIS RUNS ───
  DEMO MODE  //  LIVE MODE
  ```
  RAILS title in `--am: #d08800` muted amber Orbitron 900 — RAILS is the structural-grounding section so the title is intentionally less hot than the FORGE / COMBAT / EVOLVE titles. "HOW THIS RUNS" subtitle in `--gr` muted gray. The DEMO MODE / LIVE MODE line as two pills, side-by-side, matching the index.html landing page's `.pill` styling — DEMO MODE pill bordered in `--g` green (`#00e676`), LIVE MODE pill bordered in `--a` amber. ~9 words on-slide.
- **Visual artifacts needed:** Two pill-shaped tags reproducing index.html's intro `.pill` style. DEMO MODE pill green-bordered, label "DEMO MODE · no key, no cost." LIVE MODE pill amber-bordered, label "LIVE MODE · real models, your provider, your key."
- **What operator says when slide goes up:** "RAILS. How this actually runs. Two modes. DEMO MODE — pre-recorded transcripts play back inside each demo. No key, no cost. That's what you saw today. LIVE MODE — real models, your choice of provider, your key stays in your browser. You can run all three demos on your laptop tonight."
- **When slide is dismissed:** Advance to S10 when operator transitions into limits / authorization beat.
- **Time-budget:** ~3 min visible across RAILS section.

---

### S10 — Authorization preamble / limits (A14 anti-marker LIVES HERE)

- **Section anchor:** RAILS mid
- **Title:** LIMITS
- **On-slide text:**
  ```
  LIMITS

  the swarm needs a written authorization scope.
  the swarm refuses targets outside it.
  the rubric does not score "should this be done."

  not a product. not a service. not a vendor.
  ```
  LIMITS header in `--am` muted amber. The three lines on what the swarm needs/does/doesn't in `--w` off-white. The closing three-fragment line in `--a` amber, slightly emphasized — this is the A14 anti-doomer-vendor-tone anti-marker, the load-bearing line on this slide and arguably the load-bearing line of the deck for stance-credibility. The fragments mirror the locked-v7 cadence ("No vendor fluff. Come watch the first rounds.") — three short declarative negations, no hedging. ~29 words on-slide.
- **Visual artifacts needed:** Just structured text. Optional: faint `[AUTHORIZATION SCOPE]` header decoration at the top in the same style as combat.html's section banners, but operator-iterable; default off (the slide's words carry it).
- **What operator says when slide goes up:** "Three things. The swarm needs a written authorization scope before it runs — same as a pen-test engagement, same as a CCDC playbook, same as your day job's change-management. The swarm refuses targets outside its scope; we built that gate at the framework level, not at the agent level. And the rubric scores how well the agents did, not whether the work should have been done. That's the human's call, every time." Beat. "This is not a product. Not a service. Not a vendor. It's a framework you can run on a laptop. The repo is public, the demos are public, the docs are public."
- **When slide is dismissed:** Advance to S11 (closing card) when operator hits the closing beat.
- **Time-budget:** ~3 min visible — the longest dwell of any slide in the deck. RAILS is where the doomer-vendor-tone risk is highest, and the slide is the structural anchor that prevents drift.

---

### S11 — Closing card

- **Section anchor:** CLOSE
- **Title:** (none — the closing line IS the slide)
- **On-slide text:**
  ```
  small unit.
  deep impact.

  no vendor fluff. come watch the first rounds.
  ```
  Two-line title fragment ("small unit. / deep impact.") in `--a` amber Orbitron 900 ~48px, lowercased deliberately for register continuity with the locked-v7-blurb's lowercase closing. Closing line in `--w` off-white Share Tech Mono ~24px. ~12 words on-slide.

  **Operator iteration surface — proposed closing line:** "no vendor fluff. come watch the first rounds." is taken verbatim from the locked v7 blurb's closing pair, which the operator has signed off across seven iterations. Alternative branches for iteration: (a) just "come watch the first rounds." standalone (shorter, hits register without the negation); (b) "small unit. deep impact. that's the whole pitch." (callback to title, anti-vendor by structural understatement); (c) the verbatim locked-v7-pair as drafted above (recommended — preserves the operator's signed-off phrasing and lands the deck's payoff in operator-village voice). Default to (c); surface (a) and (b) in S+3 dry-run for operator iteration.

  The talk title ("Small Unit, Deep Impact: Creating Motion in the Ocean with Multi-Agent Swarms") does NOT appear in full on this slide — the title-card S1 carried it; the closing card drops the subtitle to keep the closing visual register punchy.
- **Visual artifacts needed:** Centered text only. Optional: a single non-blinking `█` block-cursor at end of closing line (slide is the talk's terminus; cursor static, not blinking — the prompt does not advance after this).
- **What operator says when slide goes up:** Slide goes up at the closing beat. Operator's last line lands at the same time as the slide reveal: "Small unit. Deep impact. No vendor fluff — come watch the first rounds in the village." Beat. "Thanks." (or whichever sign-off SMYTH-A drafts in CLOSE.)
- **When slide is dismissed:** Slide stays up through Q&A. Does not advance to back-pocket slides (those are at routes the audience cannot navigate to from this slide).
- **Time-budget:** ~5 min visible (CLOSE + Q&A buffer).

---

## Back-pocket slides (out of visible sequence)

These two slides exist at addressable routes (`#/forge-recap` and `#/combat-recap`). Forward-arrow navigation from S11 does NOT advance into them — they are reached only by typing the route or via a hidden operator-only bookmark. They are placed at the END of the reveal.js deck (after S11) so accidental keyboard nav cannot reveal them during the talk.

Both back-pocket slides are **FORWARD recovery slides, not backward reset slides**. If the operator reaches one, the operator does NOT return to the preceding chapter divider afterward — the operator narrates the recap, then tab-switches forward to the next section's chapter divider. The COMBAT-no-reset micro-rule applies: never tab back to the COMBAT setup slide mid-section even if the demo wedges. The back-pocket S6 is the forward escape hatch, not a reset.

### S4 — FORGE-recap (back-pocket)

- **Section anchor:** BACK-POCKET (used if forge.html demo wedges)
- **Title:** FORGE — WHAT THE DEMO WOULD HAVE SHOWN
- **On-slide visualization:** A simplified 9-phase diagram (P1 / P2 / ... / P9 cells in a single row, matching forge.html's `.pbar` style at line 31 of forge.html CSS), with three or four phase labels filled in:
  - P1 — DOMAIN ANALYSIS
  - P3 — ROSTER DESIGN
  - P6 — AGENT FABRICATION
  - P9 — PACKAGE EMITTED

  Other phases shown as cells without labels — the visualization is "you would have watched these nine cells light up in sequence; here is the shape of what fills each one." Below the phase bar, a single artifact pill: `[ swarm package · agents/ + commands/ + manifest ]`.
- **What operator says — 90-sec recap script (verbatim prose, the operator delivers this if FORGE wedges):**

  > Okay — the FORGE demo wedged. Here's what you would have seen.
  >
  > You give it a domain. Plain language. "Red team operations." "Bug bounty triage." "Forensic accounting." Doesn't matter. It analyzes the domain in phase one — what the workflow actually looks like, what the seams are, where one role hands off to the next. Phase two it goes and reads the right reference material; phase three it designs the roster — usually six to ten agents, each one narrow.
  >
  > Phases four through six it writes the agent prompts. One at a time. Each prompt gets a structural review before the next one starts.
  >
  > Phases seven and eight it builds the coordination scaffolding — the files the agents read and write to talk to each other. That's the part most multi-agent setups skip and then regret. Coordination is the thing that decides whether your six agents are a swarm or just six chatbots in a trenchcoat.
  >
  > Phase nine it emits the package. Directory you can extract, push to a repo, run on its own. Agents folder. Commands folder. Manifest at the root. The lot.
  >
  > And that's what you would have watched. About four minutes in DEMO MODE; about fifteen in LIVE MODE depending on the model. That's the BUILD half of The Loop. That's what a swarm forge produces — package, agents, manifest, the lot.
  >
  > Now let's get to FIGHT.

  (224 words. Natural-narration pace ~150wpm = ~90 sec.) The closing two sentences land the named-hook plant that the demo run was supposed to plant ("the BUILD half of The Loop, what a swarm forge produces — package, agents, manifest, the lot"). After speaker delivers the closing line, tab-switch FORWARD to S4 (COMBAT divider). Do not tab back to S3.

- **Cue points annotated in script:**
  - Pause beat after "wedged" (acknowledge the situation, then move on — do not apologize or backtrack).
  - Slight emphasis on "phase nine it emits the package" (this is the equivalent of the demo's final reveal).
  - "trenchcoat" gets a small grin if the room is with you (anti-vendor levity); skip if room is reading dry.

### S6 — COMBAT-recap (back-pocket)

- **Section anchor:** BACK-POCKET (used if combat.html demo wedges)
- **Title:** COMBAT — WHAT THE DEMO WOULD HAVE SHOWN
- **On-slide visualization:** A two-row phase bar matching combat.html's `.phases` structure (red row 6 cells above blue row 6 cells, separated by the diagonal red→blue gradient divider from combat.html line 56). Cells labeled with combat's phase names — RED row: RECON · ACCESS · PRIVESC · CRED · LATERAL · OBJECTIVE; BLUE row: TELEMETRY · DETECT · CONTAIN · IR · ROOT · REPORT. Beneath the phase bar, a small score panel sketch (sized like combat.html's SCORE panel) with category cells showing dashes for unscored values:
  ```
  IRONCLAD          ?/50    PHANTOM FEED      ?/50
  detection cov   :   -      detection cov   :   -
  time-to-detect  :   -      time-to-detect  :   -
  workflow        :   -      workflow        :   -
  artifact        :   -      artifact        :   -
  root-cause      :   -      root-cause      :   -
  ```
- **What operator says — 90-sec recap script (verbatim prose, the operator delivers this if COMBAT wedges):**

  > Okay — COMBAT wedged. Here's the fight you would have watched.
  >
  > Two swarms, six phases each, side by side. Red team on top: recon, access, privesc, credentials, lateral, objective. Blue team below: telemetry, detect, contain, IR, root-cause, report. They run in parallel. Red moves; blue sees something or doesn't. Every phase produces evidence — log lines, alert text, IR notes, the things a real analyst would write down.
  >
  > We run two scenarios back-to-back, same blue team both times. IRONCLAD is the easy one — sort of. Enterprise compromise. ProFTPd exploit, credential reuse, lateral to a domain controller, exfil. Blue team is in scope and knows the network. They should catch it; the question is how cleanly.
  >
  > PHANTOM FEED is the hard one. MLOps supply-chain attack. The blue team is NOT in scope — they're a customer of a poisoned model, downstream of an attack they don't know happened upstream. They have to figure out they're being attacked from data they never asked for. Most blue teams haven't trained for this; we wrote the scenario because it's the threat shape that's coming whether the industry is ready or not.
  >
  > Both runs get scored against the same rubric — the one you saw a slide of. Five categories, ten points each. ARBITER, who is its own agent, applies the rubric. Same rubric, both scenarios, scored by a rubric fixed before the bell, not after.
  >
  > That's the FIGHT half — Same-Blue-Team faces both IRONCLAD authorized and PHANTOM FEED unauthorized, scored by a rubric fixed before the bell.
  >
  > Now let's get to REFINE.

  (273 words. Natural-narration pace ~150wpm = ~110 sec — slightly over the 90-sec target. Acceptable: COMBAT is the longest section in the talk and a longer recap is proportional. Alternative: drop the "Most blue teams haven't trained for this..." sentence to bring it under 90 sec. Surface in dry-run for operator iteration on length.) The closing two sentences land the named-hook plant that the demo run was supposed to plant ("the FIGHT half — Same-Blue-Team faces both IRONCLAD authorized and PHANTOM FEED unauthorized, scored by a rubric fixed before the bell"). After speaker delivers the closing line, tab-switch FORWARD to S6 (EVOLVE divider). Do not tab back to S4 or S5.

- **Cue points annotated in script:**
  - "wedged" — same beat as FORGE recap, no apology.
  - Slight emphasis on "Same blue team both times" (this is the Same-Blue-Team hook).
  - "the threat shape that's coming whether the industry is ready or not" — this is a stakes line. Deliver matter-of-fact, not doomer-tone. The line works because it's flat; if it sounds rehearsed-portentous, cut it on the next telling.
  - "fixed before the bell, not after" — verbatim locked-v7 cadence; deliver clean, no irony.
