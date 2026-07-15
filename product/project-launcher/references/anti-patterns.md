# Launch anti-patterns — detection & correction

Sources:
- CB Insights — [483 startup post-mortems](https://www.cbinsights.com/research/startup-failure-post-mortem/) — primary data
- Sam Altman — Startup Playbook
- Paul Graham — Schlep Blindness, Founder Mode

---

## Top causes of startup death (CB Insights, base of 483 cases)

| Cause | % of cases | Phase affected |
|---|---|---|
| No product-market fit | 43% | Phase 3 |
| Bad timing | 29% | Phase 0 |
| Unsustainable unit economics | 19% | Phase 4 |
| Not the right team | 23% | All |
| Inability to market | 14% | Phase 4 |
| Inflexible / no customer feedback | 14% | Phase 1 |
| Ran out of cash | (where these stories end) | Phase 4 |

**Takeaway:** death rarely comes from a single cause. The patterns below are the canonical paths toward those causes.

---

## 1. Schlep blindness

**Source:** Paul Graham, *Schlep Blindness* (2012). https://paulgraham.com/schlep.html

**Definition:** the unconscious tendency to filter out ideas that involve boring, tedious, or thankless tasks. The brain literally doesn't see them.

**Detection signal:**
- The user says "it's easy, you just have to [...]"
- No schlep listed in Phase 0
- The idea seems "too obvious to not have been done already"

**Correction:** ask explicitly, *"What are the 5 schleps you'll have to deal with? (legal, support, legacy sales integrations, data quality, business edge cases...)"*. If the list is empty or < 3 items → red flag.

**Quote:** *"Schleps are not merely inevitable, but pretty much what business consists of."* — Graham

---

## 2. Vanity metrics

**Source:** Altman Playbook, Eric Ries (Lean Startup), Sean Ellis.

**Definition:** metrics that always go up but don't reflect the value delivered. They give a false sense of progress.

**Examples:**
- Total signups (without retention)
- Total downloads
- Page views, sessions
- Unqualified MAU
- Twitter followers
- "Press mentions"

**Detection signal:**
- The proposed NSM is in the list above
- The dashboard the team looks at has no cohort retention
- The company story is about "X users acquired", not "Y users still active after Z months"

**Correction:** replace each vanity metric with its retention-driven version. For example: "signups" → "users still active at D30 / signups".

---

## 3. Big launch / press release strategy

**Source:** Altman Playbook.

**Definition:** betting on a big launch (TechCrunch, ProductHunt, a marquee partnership) to take off.

**Altman quote:** *"Press releases are easier to write than code. Beware of 'big press launches' — they effectively never work."*

**Detection signal:**
- The user is planning a ProductHunt launch before Phase 3
- Marketing budget > 5x the product budget
- The acquisition strategy relies on "the launch buzz"

**Correction:** go back to manual acquisition (Graham, *DTNS*) — DM, personal email, coffee, intros. Stripe and Airbnb did it.

---

## 4. Hiring before PMF

**Source:** Altman Playbook, *"Don't do it"* (on hiring).

**Definition:** hiring to "scale" before you have the PMF signal.

**Consequence:** organizational inertia, high fixed cost, difficulty pivoting.

**Altman quote:** *"Hire as late as possible. Once you're obviously winning, they'll want to come join you."*

**Detection signal:**
- The team proposes a hiring plan before the 40% rule is measured
- Justification: "we need seniors to scale"
- Burn rate triples before market validation

**Correction:** use short-term freelancers instead. Only hire after PMF is validated (40% rule + Altman's 4Q).

---

## 5. Founder mode break (= premature manager mode)

**Source:** Paul Graham, *Founder Mode* (2024). https://paulgraham.com/foundermode.html

**Definition:** delegating fully (manager mode) before ~50 people. Brian Chesky (Airbnb) showed that this approach (advised by VCs) **degrades** results at small/medium scale.

**Detection signal:**
- The founder no longer holds skip-level meetings
- The founder no longer touches the product
- The founder no longer talks to customers
- "I delegate the product to my CPO" while the company has < 50 people

**Correction:** return to founder mode rituals (weekly skip-level, weekly founder product review, occasional founder interventions in code/support, founder takes customer calls).

**Graham quote:** *"What works for managers doesn't necessarily work for founders [...] founders feel like they're being gaslit from both sides — by the people telling them they have to run their companies like managers, and by the people working for them when they do."*

---

## 6. Skip discovery (Phase 1)

**Source:** Mom Test (Fitzpatrick), CB Insights (14%: "inability to gather customer feedback"), Altman.

**Definition:** skipping Phase 1 (user discovery) because you "know the market".

**Detection signal:**
- The user wants to start coding without having done any interviews
- Justification: "I've got 10 years in the field"
- Or: "I've already talked to lots of people"

**Correction:** Mom Test rule 2 — opinions ≠ behavior. Altman quote: *"value what they actually do."* Ask for 5 documented interviews with verbatim quotes.

---

## 7. Doing too many things

**Source:** Altman Playbook.

**Quote:** *"A very, very common cause of startup death is doing too many of the wrong things."*

**Detection signal:**
- The roadmap contains > 5 priority features in parallel
- The team is working on a product + a side-product + a service at the same time
- Every meeting adds a new feature to the roadmap

**Correction:** a written kill list. One thing at a time. *"Don't let your company start doing the next thing until you've dominated the first thing."* — Altman.

---

## 8. Founder personal branding pre-PMF

**Source:** Altman Playbook.

**Quote:** *"Founders with publicists almost always fail."*

**Definition:** spending founder time at conferences, panels, Twitter threads, podcast interviews — before you have PMF.

**Detection signal:**
- > 4h/week of founder time on "personal branding"
- Conference appearances while the company has < 100 customers
- The founder optimizes their LinkedIn bio more often than the NSM

**Correction:** return to the product and the customers. Personal branding will come naturally once there are results to share.

---

## 9. Bad co-founder

**Source:** Altman Playbook, CB Insights ("not the right team" 23%).

**Altman quote:** *"Cofounder breakups are one of the leading causes of death for early startups."*

**Hierarchy:** good co-founder > solo > bad co-founder.

**Detection signal:**
- Structural conflicts over the vision in the first 3 months
- Reluctance about the equity split (Altman recommends near-equal + 1 extra share to break deadlocks)
- Co-founders who didn't know each other before the project

**Correction:** hard to fix mid-course. Prevention: Altman recommends 1+ year of relationship pre-project, and "trial periods" for the first hires you'd consider as co-founders.

---

## Reporting format used by the skill

When an anti-pattern is detected during an interaction:

```
🚨 Anti-pattern detected: [name]

Signal: [what was said / observed]
Source: [Graham / Altman / CB Insights / ...]
Risk: [consequence]
Proposed correction: [concrete action]

Do you want me to continue anyway, or fix this first?
```

The user can **always override** the warning, but the skill must log it in the output for later traceability.
</content>
