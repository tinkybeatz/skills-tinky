---
name: project-launcher
description: >-
  Guides the launch of a project — whether an internal product or a client engagement — through a 5-phase workflow (Framing / Discovery / MVP / PMF / Growth) that draws on the playbooks of Altman, Graham, Cagan, Ries, the Mom Test, Working Backwards, the Design Sprint, and Sean Ellis's 40% rule. Use this skill as soon as the user says: "launch a project", "kickoff", "how do I get started", "I have an idea", "validate an idea", "MVP", "PMF", "product-market fit", "discovery", "should I build X", "start a project", "launch", "go-to-market", "launch a product", "onboard a client", "first project", "from zero to one", "scope a project", "frame a project", "where do I start with my project", or any phrasing that involves the structured kickoff of a new project/product/feature/client engagement. Includes hard gates (≥5 Mom Test interviews before Phase 2, the 40% rule measured before declaring PMF) and warnings about the classic anti-patterns (schlep blindness, vanity metrics, founder mode break, premature hiring). Do NOT confuse with ceo-challenger (challenging existing decisions), architecture-conceptor (technical design), apply (backlog execution), generate-business-model (business model), senior-dev (implementation decisions). Covers the what / why / how-to-validate, not the how-to-code.
---

# Project Launcher

A structured workflow for moving from idea to PMF (Product-Market Fit). Five phases · explicit gates · documented anti-patterns · primary sources inline.

## When to trigger

Three families of cases:

1. **Internal product** — a new product, major feature, agentic side-project, internal SaaS
2. **Client engagement** — a new client project to frame, scope, and deliver (typical: AI automation, custom agent, data dashboard)
3. **Rough idea** — the user is thinking out loud and needs to structure things before deciding whether to build

**Redirect elsewhere if:**
- The user has decided and just wants the code → `senior-dev` or `architecture-conceptor`
- They're looking for a strategic challenge to a decision already made → `ceo-challenger`
- The idea is set but the business model is fuzzy → `generate-business-model`
- They want to execute a backlog that's already written → `apply`

---

## Step 0 — Identify the mode

Before diving in, ask explicitly if it isn't clear:

> **"Internal product mode or client engagement?"**

| Aspect | Product Mode | Client Mode |
|---|---|---|
| Phase 0 | PR/FAQ + Why Now | Brief + contractual scope + PR/FAQ co-written with the client |
| Phase 1 | 5-10 Mom Test interviews with prospects | Client discovery workshop (sprint 0) + interviews with end users |
| Phase 2 | 5-day MVP Sprint (GV) + DTNS | Deliverable MVP sprint + client demo validated |
| Phase 3 | 40% rule + Altman's 4Q | Retention on the delivered tool + client NPS |
| Phase 4 | NSM + growth experiments | Expansion / referral / public case study |

The backbone of the workflow is identical; only the deliverables and the people you talk to change.

---

## Phase 0 — Framing (1-2 days)

**Goal:** produce a written artifact that brings together the why, the who, and the when.

**Required deliverables:**

1. **1-page PR/FAQ** (Amazon Working Backwards) — a fictional press release exactly as you'd want to read it 12 months from now. PR ≤ 1 page, FAQ ≤ 5 pages. See `references/prfaq-template.md`.
2. **Why now?** — why this idea now, not three years ago, not three years from now. If there's no clear, differentiating answer → **red flag**.
3. **Schlep test** (Paul Graham) — what schleps (tedious, boring, thankless tasks) does this project involve? If the answer is "none", there are two possibilities: the idea is trivial OR it's schlep blindness. See `references/anti-patterns.md`.
4. **The desperate user** — describe ONE specific person (name, role, context) who *desperately* needs this. Not a generic persona. If the user isn't in the target group themselves, confirm they know at least 3 people who are.

**Gate Phase 0 → 1**: PR/FAQ reviewed by ≥ 1 person outside the project.
- Reaction "oh yeah, that's cool" → ❌ no tension, rework it
- Reaction "I want this now" → ✅ emotional tension, OK

---

## Phase 1 — User discovery (1-2 weeks)

**Goal:** confirm or disprove the desperate user's pain, BEFORE writing code.

**Required deliverables:**

1. **≥ 5 documented Mom Test interviews** — questions drawn from `references/mom-test-questions.md`. Three non-negotiable rules:
   - Talk about their life, not your idea
   - Ask about specifics in the past, not opinions about the future
   - Listen more than you talk
2. **Cagan's 4-risk map** — for each one, an assessed status:
   - **Value risk** — will they use it / pay for it? Signal: commitment in the Mom Test (time, money, reputation on the line)
   - **Usability risk** — can they understand it without heavy training?
   - **Feasibility risk** — can we build it in X time with the existing stack?
   - **Viability risk** — compatible with legal / sales / support / finance / AI ethics?
3. **Top 3 critical hypotheses** — framed as "If [X] then [Y]", testable in Phase 2.

**Hard gate Phase 1 → 2**: refuse to move forward if:
- < 5 documented Mom Test interviews (quote, context, commitment), OR
- The 4 risks aren't all assessed (an unassessed risk ≠ resolved, but it must have a status)

Message to display:
> ⚠️ Phase 2 blocked: you're missing [X interviews / Y risks]. You'll discover a viability/feasibility risk in Phase 3 — and it costs 10x more then than it does before building.

---

## Phase 2 — MVP Sprint (5 days)

**Goal:** a prototype tested in real conditions. Not a finished product.

**Format:** Google Ventures Design Sprint (Knapp 2016). See `references/sprint-5days.md`.

| Day | Activity | Output |
|---|---|---|
| Monday | Map the problem, choose the target | Long-term goal + chosen scope |
| Tuesday | Inspiration + sketching solutions | 1 detailed sketch / person |
| Wednesday | Critique + storyboard | Step-by-step storyboard |
| Thursday | Façade prototype (no backend) | Testable prototype |
| **Friday** | **Test with 5 real customers** | Synthesis of reactions |

**In parallel with the sprint:**

- **Recruit the first users manually** (Graham, *Do Things That Don't Scale*) — DM, personal email, coffee, door-to-door. No ads, no growth marketing. If it "doesn't scale", that's exactly the point. Stripe, Airbnb, and Pinterest all did it.
- **Build-Measure-Learn loop (Ries)** active from Friday evening on — each cycle ≤ 1 week. Team metric: how many complete cycles in 4 weeks?

**Gate Phase 2 → 3**: prototype tested with ≥ 5 real customers (not the internal team, not family). Bonus signal: ≥ 2 customers come back on their own to ask for v2.

---

## Phase 3 — Measuring PMF (4 to 12 weeks)

**Goal:** make the "PMF reached or not" signal binary. Get out of the subjective.

**Required deliverables:**

1. **Sean Ellis 40% survey** — *"How would you feel if you could no longer use X?"*
   - Choices: Very disappointed / Somewhat disappointed / Not disappointed
   - Target: **≥ 40% Very disappointed**
   - See `references/pmf-survey.md`
2. **Altman's 4 questions** — documented yes/no answers:
   - Do users use it more than once?
   - Are they fanatics?
   - Would they be devastated if the company shut down?
   - Do they recommend it without being asked?
3. **Vohra framework (if <40%)** — segment the "very disappointed", understand their job-to-be-done, double down on that segment. Superhuman: 22% → 58% in less than a year with this method.
4. **NSM (North Star Metric)** defined — ONE stable metric that captures the core value delivered. **Must be retention-driven**. Not signups, not page views, not an unqualified total user count.

**Hard gate Phase 3 → 4**: refuse to declare PMF if:
- The 40% rule hasn't been measured, OR
- The NSM = a vanity metric (signups, views, total users without retention)

Message to display:
> ⚠️ PMF not validated: [40% rule missing / NSM = signups / other]. Run the Ellis survey before scaling — otherwise you'll hire / raise on a false signal.

**Pivot vs. persevere decision:**

- ≥ 40% overall → **persevere**, move to Phase 4
- < 40% but an isolable, highly enthusiastic segment → **pivot toward that segment** (Vohra)
- < 40% with no clear segment → **full product pivot** (Lean Startup)

---

## Phase 4 — Growth & Focus (ongoing)

**Goal:** don't lose momentum after PMF. Altman: *"Never lose momentum."*

**Ongoing deliverables:**

1. **NSM tracked weekly, displayed visibly** — Airbnb: posted on the fridge, above the desks, in the bathrooms. The metric has to be impossible to ignore.
2. **Anti-distraction kill list** — a written list of the opportunities you turned down. Conferences, partnerships, press tours, side-features. If the item doesn't serve the NSM within 90 days, kill it.
3. **Growth experiments ranking** — a stack of tests ranked by effort/impact. Test ads, referral, content, and sales in parallel. No "strategic deals" before 100 paying customers.
4. **Founder mode rituals** (Graham 2024) — skip-level meetings, weekly demos, founder reviews of the product, occasional founder interventions in the code/support. Keep these up until ~50 people.

**Anti-patterns to flag on an ongoing basis** (see `references/anti-patterns.md`):

- "Growth via partnerships/big deal" → almost never works at early stage
- "Press launch" → false signal, no retention
- "Hire to scale" prematurely → irreversible inertia
- "Founder personal branding" → *"founders with publicists almost always fail"* (Altman)
- "Full delegation before 50 people" → founder mode break (Graham 2024)

---

## Hard rules — automatic gates

The skill must explicitly refuse to move forward and explain why:

| Gate | Refuse if | Message |
|---|---|---|
| Phase 1 → 2 | < 5 documented Mom Test interviews | "You don't have the data to decide what to build. Mom Test before code." |
| Phase 1 → 2 | Cagan's 4 risks not assessed | "A hidden risk in Phase 3 = 10× more expensive than before building." |
| Phase 2 → 3 | < 5 real (external) customer tests | "The internal team isn't a sample. Get out of the building." |
| Phase 3 → 4 | 40% rule not measured | "Subjective PMF = not PMF. Run the Ellis survey." |
| Phase 3 → 4 | NSM = vanity metric | "Vanity metric. The NSM must be retention-driven." |
| Any phase | Full delegation before 50 people | "Graham 2024: founder mode (skip-level, hands-on) > manager mode below 50." |
| Phase 0 | No schlep identified | "If it's easy, it's either trivial or it's schlep blindness. Keep looking." |
| Phase 4 | Hiring before PMF | "Altman: hire as late as possible. Use short-term freelancers instead." |

---

## Expected output format

For each interaction with the skill, structure it like this:

```
## Mode identified
[Internal product | Client engagement]

## Current phase
[0 Framing | 1 Discovery | 2 MVP Sprint | 3 PMF | 4 Growth]

## Deliverables status
- [✅/❌] deliverable 1
- [✅/❌] deliverable 2
...

## Gate to next phase
[✅ or ❌ with a concrete reason]

## Anti-patterns detected
- [pattern] (primary source)

## Concrete next actions
1. [short, measurable action, with a deadline]
2. ...
```

---

## Primary sources (≥ 88/100)

- Sam Altman — [Startup Playbook](https://playbook.samaltman.com/)
- Paul Graham — [Do Things That Don't Scale](https://paulgraham.com/ds.html), [Schlep Blindness](https://paulgraham.com/schlep.html), [Founder Mode](https://paulgraham.com/foundermode.html)
- Marty Cagan / SVPG — [Product Model Concepts](https://www.svpg.com/product-model-concepts/)
- Rob Fitzpatrick — [The Mom Test](https://www.momtestbook.com/)
- Eric Ries — [Lean Startup principles](https://theleanstartup.com/principles)
- Jake Knapp — [GV Design Sprint](https://www.gv.com/sprint/)
- Bryar/Carr — [Working Backwards PR/FAQ](https://workingbackwards.com/concepts/working-backwards-pr-faq-process/)
- Sean Ellis — [40% rule / North Star Metric](https://growthmethod.com/the-north-star-metric/)
- Rahul Vohra — [Superhuman PMF Engine](https://review.firstround.com/how-superhuman-built-an-engine-to-find-product-market-fit/)
- CB Insights — [483 startup post-mortems](https://www.cbinsights.com/research/startup-failure-post-mortem/)

---

## Failure modes & recovery

| Failure | Corrective action |
|---|---|
| User skips Phase 0 (no PR/FAQ) | Ask them to write it before continuing. Template in `references/prfaq-template.md` |
| "No time for 5 interviews" | Remind them of CB Insights: 43% of startup deaths = no PMF. Cost of one interview ≈ 30 min |
| Refuses the 40% rule ("too much friction") | Propose a minimum viable version: 20 respondents, 1 Typeform question, 5 min |
| Proposed NSM = signups/views | Refuse, propose 3 retention-driven alternatives suited to the case |
| Mode misidentified | Ask again explicitly before continuing |
| "I know the market, skip Phase 1" | Mom Test rule 2: opinions ≠ behavior. Altman: *"value what they actually do."* |
| Idea passes the PR/FAQ but not the schlep test | Either trivial or schlep blindness — dig deeper, don't validate Phase 0 |
| Wants to hire before PMF | Altman: *"hire as late as possible"*. Use short-term freelancers instead |
| Drifts into "founder personal branding" mode | Cite Altman: *"founders with publicists almost always fail"*. Refocus on product/users |
| The user doesn't place themselves in a phase | Infer it from context; if impossible, ask them at most 3 questions |

---

## Supporting resources

| File | When to read it |
|---|---|
| `references/playbook-altman.md` | All phases, exact Altman quotes by topic |
| `references/mom-test-questions.md` | Phase 1, a ready-to-use bank of questions |
| `references/prfaq-template.md` | Phase 0, Amazon PR/FAQ template with an example |
| `references/sprint-5days.md` | Phase 2, detailed Monday→Friday plan |
| `references/pmf-survey.md` | Phase 3, Ellis 40% template + Vohra framework |
| `references/anti-patterns.md` | All phases, 9 anti-patterns with source and detection signal |
</content>
</invoke>
