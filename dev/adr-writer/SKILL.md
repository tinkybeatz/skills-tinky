---
name: "adr-writer"
description: >
  Write structured, traceable, immutable Architecture Decision Records (ADRs).
  Use this skill whenever the user asks to: draft an ADR, write an ADR,
  document an architecture decision, create a decision record, add an ADR to
  the project, supersede an existing ADR, backfill an undocumented technical
  decision, or any request that involves producing a formatted ADR document.
  Also trigger when the user says: "write the ADR", "document this decision",
  "ADR for", "decision record", "add an ADR", "supersede the ADR",
  "backfill this decision", "formalize this decision as an ADR". Do NOT use it
  to analyze trade-offs or compare options (that is architecture-conceptor).
  Do NOT use it to create standards (that is standard-maker).
---

# ADR Writer

You write Architecture Decision Records — short, immutable documents that
capture a single significant architectural decision along with its context,
rationale, and consequences.

An ADR is not a spec. It is a conversation with a future developer who will
wonder "why did we make this choice".

---

## Operating modes

| Mode | Signal | What it produces |
|---|---|---|
| **Write** | "write an ADR for...", "ADR about..." | A complete, formatted ADR |
| **Backfill** | "document this existing decision", "backfill" | An ADR for a decision that is already implemented |
| **Supersede** | "supersede ADR-XXX", "this decision replaces..." | A new ADR + a status update on the old one |
| **Review** | "review this ADR", "look over this ADR" | Structured feedback on an existing ADR |

---

## Step 0 — Detect the project

Before writing, identify:

1. **The target repo** — where to store the ADR (`docs/adr/`, `doc/adr/`, `docs/decisions/`)
2. **The existing ADRs** — read the folder to learn the last number in use and the format in place
3. **The template in use** — if ADRs already exist, follow their exact format

If no ADR folder exists, propose `docs/adr/` and create the folder.
If no ADR exists yet, use the default template (see `references/templates.md`).

---

## Step 1 — Frame the decision

Extract from the conversation context, or ask:

- **What decision?** — the concrete technical choice
- **Why now?** — the trigger (incident, new requirement, technical debt)
- **What constraints?** — budget, timeline, team, legacy, compliance
- **What alternatives were considered?** — at least 2
- **Who is affected?** — the impacted stakeholders

If the user already used `architecture-conceptor` earlier in the conversation,
reuse the trade-off analysis context instead of asking again.

For **Backfill** mode, also ask:
- When was the decision made?
- Is it still valid, or already being questioned?

---

## Step 2 — Write the ADR

Apply these writing rules (drawn from Nygard, Fowler, AWS):

### Substance rules

1. **1 ADR = 1 decision.** Never put several decisions in one document.
2. **Write the "why", not the "how".** The focus is on the rationale.
3. **Neutral language in the Context.** Present the facts and forces at play without judgment.
4. **Active voice in the Decision.** "We will..."
5. **Exhaustive consequences.** Positive, negative, AND neutral.
6. **Inverted pyramid.** Most important information first.

### Form rules

7. **Naming**: `NNNN-title-with-dashes.md` (e.g. `0012-use-postgres-for-event-store.md`)
8. **Sequential numbers**, never reused, even when an ADR is superseded.
9. **Length**: 1-2 pages max. Link out to external documents when more detail is needed.
10. **Markdown** is mandatory, no complex formatting.
11. **Complete sentences.** No telegraphic bullet points — write the way you would talk to a colleague.

### Governance rules

12. **Immutability.** An accepted ADR is never modified. You supersede it.
13. **Statuses**: `proposed` → `accepted` → `deprecated` / `superseded by ADR-NNNN`
14. **Bidirectional link** when one ADR supersedes another.

Use the template defined in `references/templates.md`.

---

## Step 3 — Validate

Before delivering, run through this checklist:

| # | Criterion | Pass? |
|---|---|---|
| 1 | The title describes the decision, not the problem | |
| 2 | The context presents the forces without bias | |
| 3 | The decision is in active voice ("We will...") | |
| 4 | At least 2 alternatives are documented | |
| 5 | The consequences cover positive + negative + neutral | |
| 6 | The confidence level is explicit | |
| 7 | The naming follows the NNNN-title.md format | |
| 8 | The number is the next one in the sequence | |
| 9 | The length stays under 2 pages | |
| 10 | No section is empty or a placeholder | |

If a criterion fails, fix it before delivering. Do not deliver an incomplete ADR.

---

## Step 4 — Deliver

1. Write the ADR file into the project folder
2. Print a short summary:
   ```
   ADR-NNNN: [Title]
   Status: proposed
   Decision: [1-line summary]
   Stored: docs/adr/NNNN-title.md
   ```
3. In **Supersede** mode: update the status of the old ADR
4. Offer: "Would you like me to add it to the commit?"

---

## Review mode

When the user submits an existing ADR for review, evaluate it against the
Step 3 checklist plus these additional criteria:

| Criterion | Points |
|---|---|
| Clarity of the rationale | 25 |
| Completeness of the alternatives | 20 |
| Quality of the consequences | 20 |
| Neutrality of the context | 15 |
| Form and conventions | 20 |

Score >= 80: solid ADR, ready to accept.
Score 60-79: minor fixes suggested.
Score < 60: rewrite recommended.

---

## Failure modes and recovery

| Problem | Action |
|---|---|
| Vague decision ("we should use X") | Ask for the context, constraints, and alternatives before writing |
| No alternatives documented | Refuse to write without at least 2 alternatives. Suggest using architecture-conceptor first |
| ADR too long (> 2 pages) | Move the details into linked documents. Keep the ADR concise |
| ADR / spec / RFC confusion | Refocus: an ADR captures a decision that was made, not a detailed design |
| No ADR folder in the project | Offer to create `docs/adr/` with a foundational ADR-0001 |
| Existing format differs from the default template | Adapt to the format in place, do not force a template change |
| Decision already covered by an existing ADR | Flag the duplicate, offer to supersede if the decision has evolved |

---

## References

| File | When to read it |
|---|---|
| `references/templates.md` | Step 2 — for the exact template to use |
| `references/examples.md` | When you need to calibrate tone and depth |
