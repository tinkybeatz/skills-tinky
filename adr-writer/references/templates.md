# ADR Writer — Templates

## Default template

A hybrid Nygard + MADR template, tuned for a small, agile team.
Use this template unless the project already has a format in place.

```markdown
# ADR-NNNN: [Noun-phrase title describing the decision]

**Date:** YYYY-MM-DD
**Status:** proposed | accepted | deprecated | superseded by ADR-NNNN
**Confidence:** high | medium | low
**Deciders:** [names or roles of the deciders]

## Context

[Factual, neutral description of the problem and the forces at play.
 Include the technical, business, team, and time constraints.
 Present the facts without judgment — the reader should be able to form
 their own opinion before reading the decision.]

## Decision Drivers

- [Key factor 1]
- [Key factor 2]
- [Key factor 3]

## Considered Options

1. **[Option A]** — [short description]
2. **[Option B]** — [short description]
3. **[Option C]** — [short description]

## Decision

We will [decision in active voice].

[Justification: why this option and not the others.
 Link explicitly to the decision drivers.]

## Consequences

### Positive

- [Positive consequence 1]
- [Positive consequence 2]

### Negative

- [Negative consequence 1 + mitigation if applicable]
- [Negative consequence 2]

### Neutral

- [Neutral impact or accepted trade-off]

## Links

- [Link to doc, RFC, issue, superseded ADR, etc.]
```

---

## Nygard template (minimal)

For simple decisions or projects that prefer something lightweight.

```markdown
# ADR-NNNN: [Title]

**Status:** proposed | accepted | deprecated | superseded by ADR-NNNN

## Context

[Forces at play, problem to solve.]

## Decision

We will [decision].

## Consequences

[All consequences: positive, negative, neutral.]
```

---

## MADR 4.0 template (complete)

For complex decisions with a detailed analysis of the options.
Use it when there are 3+ serious options to compare.

```markdown
# [Short title covering the problem and the solution]

**Date:** YYYY-MM-DD
**Status:** proposed | accepted | deprecated | superseded by ADR-NNNN

## Context and Problem Statement

[Description of the problem in 2-5 sentences.]

## Decision Drivers

- [Driver 1]
- [Driver 2]

## Considered Options

- [Option 1]
- [Option 2]
- [Option 3]

## Decision Outcome

Chosen option: "[Option N]", because [justification tied to the drivers].

### Confirmation

[How to validate that the decision produces the expected results.]

### Consequences

- Good, because [positive consequence]
- Bad, because [negative consequence]
- Neutral, because [neutral impact]

## Pros and Cons of the Options

### [Option 1]

- Good, because [argument]
- Bad, because [argument]

### [Option 2]

- Good, because [argument]
- Bad, because [argument]

### [Option 3]

- Good, because [argument]
- Bad, because [argument]

## More Information

[Links, references, additional context.]
```

---

## Template selection rules

| Situation | Template |
|---|---|
| Project with no existing ADRs | Default |
| Simple decision, few options | Nygard minimal |
| Complex decision, 3+ serious options | MADR 4.0 |
| Project with existing ADRs in another format | Adapt to the format in place |

---

## Foundational ADR-0001 (optional)

When initializing an ADR folder in a project, offer to create a first,
self-referential ADR:

```markdown
# ADR-0001: Use Architecture Decision Records

**Date:** [today's date]
**Status:** accepted
**Confidence:** high
**Deciders:** [team]

## Context

The architectural decisions made in this project are not documented.
When a new member joins the team or a decision needs to be reconsidered,
the original context and rationale are lost.

## Decision Drivers

- Preservation of institutional knowledge
- Onboarding of new members
- Traceability of technical choices

## Considered Options

1. **ADRs in the repo** — Markdown files versioned with the code
2. **Confluence/Notion wiki** — centralized documentation outside the repo
3. **No documentation** — the status quo

## Decision

We will use Architecture Decision Records stored as Markdown files
in `docs/adr/` and versioned with the source code.

## Consequences

### Positive

- Decisions are traceable and versioned alongside the code
- The lightweight format (1-2 pages) encourages documentation
- New members can read the history of the choices made

### Negative

- Initial overhead for every significant decision
- Requires team discipline to keep up the habit

### Neutral

- ADRs do not replace specs or detailed RFCs

## Links

- Michael Nygard, "Documenting Architecture Decisions" (2011)
- MADR 4.0 — https://adr.github.io/madr/
```
