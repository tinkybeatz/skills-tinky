---
name: "brief-writer"
description: >
  Transform a DOCUMENTOR research report into a client-ready deliverable.
  Trigger when the user asks to: "brief", "reformat for the client",
  "turn it into a deliverable", "write up the brief", "client format",
  "write a brief", "make it client-ready", "prepare the deliverable",
  "creative brief", "brief créatif", "design brief", "brief design",
  or any phrasing implying transformation of research into a polished
  output for an external audience.
  Do not use for internal research — that's DOCUMENTOR's job.
---

# BRIEF-WRITER

Turn a DOCUMENTOR synthesis into a client deliverable, adapted to the
tone, format, and standards of your team.

Read `reference/voice.md` for tone and house conventions.

---

## Scope

**In scope:** reformatting, audience adaptation, plain-language rewrites,
structuring client deliverables, decision briefs, creative briefs,
design briefs.

**Out of scope:** sourcing research (that's DOCUMENTOR), inventing content
not present in the source report, adding unsourced claims.

---

## Structural principle — the Pyramid Principle

**Every brief follows the Pyramid Principle** (Barbara Minto, McKinsey):
recommendation first, supporting arguments next, data last.

> "You think from the bottom up, but you present from the top down."

Why: it respects the decision-maker's time, aligns with strategic thinking,
and signals conviction. This principle applies to **all** types of briefs,
not just executive briefs.

In practice: each section of the brief opens with its conclusion,
not with its context.

### The MECE rule

The key points, findings, options, or recommendations in a brief must be
**MECE** (Mutually Exclusive, Collectively Exhaustive):

- **Mutually Exclusive** — each bullet covers a distinct angle, with no
  overlap. If two bullets say the same thing from different angles,
  merge them.
- **Collectively Exhaustive** — the bullets, taken together, cover the topic.
  If a critical aspect of the DOCUMENTOR report appears in no bullet,
  add it.

**Quick test:** reread a section's bullets. If you can delete a bullet
without losing information → it's redundant. If a reader could ask an
obvious question that isn't covered → a bullet is missing.

---

## Step 0 — Identify the input and the audience

### Input

The brief-writer **always** receives a DOCUMENTOR report as input.
If no report is available in the conversation, ask the user to run a
DOCUMENTOR search first, or to provide the report to transform.

### Audience

Identify the target format among:

| Audience                         | Tone                                                | Structure                                                                 | Sources                                |
| -------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------- | -------------------------------------- |
| **Decision-maker client**        | Plain language, no technical jargon unless explained | Executive summary up top, actionable recommendations, technical appendices | In an appendix, not inline             |
| **Technical client**             | Jargon OK, maximum precision                        | Dense structure, raw data preserved, code/diagrams where relevant         | Inline, as in the DOCUMENTOR report    |
| **Designer / stakeholder brief** | Short, direct, action-oriented                      | Bullet points, no prose, only the decisions to be made                    | Omitted unless requested               |
| **Sales proposal**               | Professional, value-oriented                        | Context → Problem → Approach → Expected outcome → Next steps               | Woven in as proof of credibility       |
| **Creative brief**               | Evocative, inspiring, insight-driven                | GET-TO-BY framework: audience → target behavior → motivating insight      | Omitted — the source report is the record |
| **Design brief**                 | Precise, focused on specs and constraints           | Objective → Audience → Scope/deliverables → Guidelines → Constraints       | Omitted except visual references       |

If the audience isn't specified, ask.

---

## Step 1 — Extract the content from the report

From the DOCUMENTOR report:

1. **Identify the verified facts** — these are the foundations of the brief; preserve them
2. **Identify the derived recommendations** — reword them in client language
3. **Identify the assumptions** — flag or omit them depending on the audience
4. **Identify the contradictions** — handle them (simplify for a decision-maker, detail for a technical reader)
5. **Identify the confidence level** — it guides the tone (assertive if high, hedged if moderate)

**Absolute rule:** never add information absent from the source report.
If the brief needs more, request an additional DOCUMENTOR search rather
than inventing it.

---

## Step 2 — Apply the transformation rules

### 2a — Plain language (non-technical audiences)

- Replace jargon with everyday equivalents
- If a technical term is unavoidable, explain it in a parenthesis
- Remove source scores and methodological details
- Transform the DOCUMENTOR labels:
  - `Verified fact` → a direct statement with no label
  - `Derived recommendation` → "Our analysis indicates that..." or "Based on the sources reviewed..."
  - `Assumption` → "To be confirmed: ..." or omit if not critical

### 2b — Preserving traceability

Even in plain language, the brief must remain **traceable** back to the
source report:

- Keep a "Sources" section in an appendix (title + URL at minimum)
- State the date of the research and the overall confidence level
- If a claim is disputed in the report, hedge it in the brief
  (don't turn it into a certainty)

### 2c — Structure by audience

**Decision-maker client:**

```
1. Executive summary (3–5 lines, conclusion first)
2. Context (why this research)
3. Key findings (5–7 bullets max, factual)
4. Recommendations (actionable, conditional if needed)
5. Risks and limitations (what we don't know yet)
6. Next steps
Appendix: Sources reviewed
```

**Technical client:**

```
1. Summary (5–10 lines)
2. Detailed analysis (structured by sub-question)
3. Comparisons / tables where relevant
4. Technical recommendations
5. Limitations and gray areas
6. Sources (inline + listed at the end)
```

**Designer / stakeholder brief:**

```
• Decision to make: [direct statement]
• Context in 2 lines
• Options identified (bullets)
• Recommendation: [option + short justification]
• Main risk: [1 line]
```

**Sales proposal:**

```
1. Client context (reworded from the report)
2. Problem identified
3. Recommended approach (based on the findings)
4. Expected outcomes (sourced where possible)
5. Next steps / commitment
```

**Creative brief (GET-TO-BY framework):**

```
1. Background / Context (2-3 lines)
2. GET — the audience described evocatively (not a generic persona)
3. TO — the measurable target behavior (what we want them to do)
4. BY — the motivating insight (the "why" — not an observation, an insight)
5. Tone & guidelines (creative direction, not rigid constraints)
6. Deliverables and constraints
```

**Design brief (designers/devs):**

```
1. Project overview and objective (the "why" first)
2. Target audience and personas
3. Scope and expected deliverables (formats, dimensions, specs)
4. Brand guidelines / design system (visual references)
5. Technical constraints and budget
6. Timeline and milestones
```

---

## Step 3 — Apply the house tone

Load `reference/voice.md` for the tone conventions.
If the file doesn't exist yet, apply the defaults:

- **Direct, not corporate.** No "it should be noted that" or "it is worth pointing out"
- **Precise, not vague.** Quantify where possible, date it, source it
- **Honest about limitations.** Don't oversell the report's certainty
- **No unsourced superlatives.** "Market leader" only if a source says so
- **Active, not passive.** "We recommend" rather than "It is recommended"

---

## Step 4 — Validate, deliver, and offer the export

Before delivery, run the checklist in `reference/checklist.md`.
Items marked ★ are blocking — do not deliver if any of them fails.

Deliver the brief in the conversation, then offer:

> "Would you like me to save this brief to Notion?"

If yes → create the page via the Notion MCP with:

- Brief title
- Date
- Target audience (property)
- Link to the source DOCUMENTOR report if available

---

## Failure modes

| Failure                                             | Corrective action                                                          |
| --------------------------------------------------- | -------------------------------------------------------------------------- |
| No DOCUMENTOR report as input                       | Ask to run the search first                                                |
| Audience not identified                             | Ask before writing                                                         |
| Adding info absent from the report                  | Remove it and request a DOCUMENTOR follow-up                               |
| Tone too corporate / marketing                      | Reread Step 3, simplify                                                    |
| Overstated certainty on a moderate-confidence point | Reintroduce the source report's hedge                                      |
| Brief too long for the audience                     | Cut it — a decision-maker brief over 1 page is too long                    |
| Multiple objectives in a single brief               | Split into separate briefs — one brief = one objective                     |
| Conclusion buried at the end of the brief           | Apply the Pyramid Principle — recommendation up front                      |
| Vague objectives ("improve visibility")             | Reword as a measurable outcome or ask for specifics                        |
| Brief written for the approver, not the doer        | Match tone and detail to whoever _uses_ the brief, not who signs off       |
| Observation presented as insight (creative brief)   | An observation = "what is". An insight = "why". Reword it as the why       |

---

## Supporting resources

| File                     | When to read it                                        |
| ------------------------ | ------------------------------------------------------ |
| `reference/voice.md`     | **Always** — tone and house conventions                |
| `reference/checklist.md` | **Step 4** — validation before delivery                |
| `reference/examples.md`  | If unsure of the expected format for an audience type  |
