# GV Design Sprint — Detailed 5-day plan

Primary source: Jake Knapp, John Zeratsky, Braden Kowitz, *Sprint* (2016). https://www.thesprintbook.com/

A method created at Google Ventures, used to quickly validate new features/products through real user tests in one week.

---

## Prerequisite

**Team (Knapp recommends 7 people max):**
- 1 Decider (founder/CEO or product lead with final authority)
- 1 Designer
- 1 Engineer / tech lead
- 1 Marketing / UX
- 1 Customer expert (sales, support, or the customer themselves)
- 1-2 wild cards (a different discipline, a fresh perspective)

**Recruit Friday's testers STARTING MONDAY** — without 5 external testers on Friday, the whole sprint is pointless. Compensate by paying each tester $50-100 (massive ROI vs. a wasted sprint).

---

## Monday — Map & Target

**Morning (3h):**
- Define the long-term goal (1-3 years). What would be worse than arriving there and not being satisfied? List the sprint questions you hope to have answered in 6 months.
- Map the problem: user(s) → steps → end goal. A simple 5-15 box diagram.
- Ask the experts (1-on-1, 30 min each): what they know about the problem, the users, the competitors, and the tech.

**Afternoon (3h):**
- "How might we" notes: each participant writes questions on sticky notes during the expert interviews.
- Organize and vote (4 dots / person) on the most promising "How might we" notes.
- **Choose ONE single target user + ONE single moment on the map.** That's the sprint's target.

**Monday output:** the problem map + target user/moment + long-term goal.

---

## Tuesday — Sketch

**Morning (3h):**
- Lightning demos: each person presents 3 existing inspirations in 3 minutes. The goal: remix good ideas, not innovate from scratch.
- Silent individual notes on the inspirations.

**Afternoon (3h):**
- 4-step sketch (silent, individual):
  1. Notes (20 min) — re-read and synthesize
  2. Ideas (20 min) — doodle concepts
  3. Crazy 8s (8 min) — 8 rapid variations of the best concept (1 min/variation)
  4. Solution sketch (30 min) — 1 three-panel storyboard, presentable quality

**Tuesday output:** 1 detailed solution sketch / person (5-7 sketches total).

---

## Wednesday — Decide

**Morning (3h):**
- "Art museum": all the sketches on the wall, in silence.
- Heat map: each person places dots on the parts that appeal to them.
- Speed critique: for each sketch, 3 min of guided public discussion.
- Straw poll: everyone votes for their favorite sketch (1 dot).
- The **Decider** makes the final call (one or more winning sketches; no supermajority allowed — it's their decision).

**Afternoon (3h):**
- Combined storyboard: take the winning scenes and weave them into a 10-15 panel user journey.
- Decide on the prototype fidelity (mobile, web, clickable slides, paper brochure).
- List the assets needed for Thursday (copy, images, screens).

**Wednesday output:** storyboard + prototype plan.

---

## Thursday — Prototype ("fake it" philosophy)

**All day (8h):**
- "Realistic façade": no backend, no logic. Just enough for Friday's testers to click and believe it's real.
- Typical tools: clickable Figma, Keynote/Slides, a quick Webflow, Bubble for mockups, or even paper + pen for physical products.
- Divide the work: 1 Maker (assembles), 2 Stitchers (create the screens), 1 Writer (the copy), 1 Asset Collector (visuals), 1 Interviewer (prepares Friday's script).

**Trial run at the end of the day:** a full simulation of the test, debugging the UX bugs.

**Thursday output:** a working prototype for the 1-on-1 test on Friday.

---

## Friday — Test (the day that counts)

**Format:** 5 one-on-one interviews, 1h each, spaced through the day.

**Why 5?** Nielsen research: 5 testers reveal ~85% of UX problems. Beyond that = diminishing returns.

**Structure of one interview (1h):**

| Phase | Duration | What |
|---|---|---|
| Welcome | 5 min | Put them at ease, explain "we're testing the product, not you" |
| Context | 5 min | Mom Test questions about their life/current usage |
| Intro to the prototype | 3 min | "Here's X. Explore it, tell me what you think out loud." |
| Tasks | 30 min | Give concrete tasks, observe in silence (except a neutral prompt: "what are you looking for?") |
| Debrief | 15 min | Open questions: "If you had a magic wand, what would you change?" |

**Meanwhile, the rest of the team watches** (separate room, live transcription on a wall of sticky notes: 1 note per observation, per tester).

**End of day — 1h synthesis:**
- Read the wall of sticky notes
- Identify the patterns (≥ 3 of 5 testers = a pattern, < 3 = noise)
- Decide: Win (continue to build), Loss (pivot), Mixed (re-sprint on the gray areas)

**Friday output:** a clear decision + a list of patterns + the next step.

---

## Criteria to move from Phase 2 → Phase 3

- [ ] 5 external testers (not the team) have interacted with the prototype
- [ ] Patterns identified (≥ 3/5)
- [ ] At least 2 testers spontaneously asked "when does this ship?"
- [ ] A Win/Loss/Mixed decision made and documented
- [ ] A Build-Measure-Learn loop (Ries) planned for the following weeks

---

## Anti-patterns to avoid

| Anti-pattern | Consequence | Correction |
|---|---|---|
| "We didn't have time to recruit for Friday" | Sprint wasted | Recruit MONDAY morning as the top priority |
| The internal team tested instead | False signal | 5 external testers required, paid if necessary |
| Prototype too built-out on Thursday (a real backend) | Sprint stretches to 2-3 weeks | Strict "fake it" — façade, not function |
| Decider absent or indecisive | Wednesday's decision blocked | The Decider must be present all 5 days, no exception |
| > 7 people in the room | Endless discussions, slowdown | Hard cap of 7, the rest observe on Friday |
| No "How might we" on Monday | Sprint with no direction | Redo Monday before continuing |
</content>
