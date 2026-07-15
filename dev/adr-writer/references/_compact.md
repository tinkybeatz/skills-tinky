# ADR Writer — Compact Reference

## Template Selection

| Situation | Template |
|-----------|----------|
| Project with no existing ADRs | Default |
| Simple decision, few options | Nygard minimal |
| Complex decision, 3+ serious options | MADR 4.0 |
| Project with existing ADRs | Adapt to the format in place |

## Template: Default

```
# ADR-NNNN: [Noun-phrase title]

**Date:** YYYY-MM-DD
**Status:** proposed | accepted | deprecated | superseded by ADR-NNNN
**Confidence:** high | medium | low
**Deciders:** [names or roles]

## Context
[Factual, neutral, technical/business/team/time constraints]

## Decision Drivers
- [Key factor 1-N]

## Considered Options
1. **[Option A]** — [short description]
2. **[Option B]** — [short description]
3. **[Option C]** — [short description]

## Decision
We will [decision in active voice].
[Justification tied to the drivers. Why not the others.]

## Consequences
### Positive
### Negative
### Neutral

## Links
```

## Template: Nygard (minimal)

```
# ADR-NNNN: [Title]
**Status:** proposed | accepted | deprecated | superseded by ADR-NNNN

## Context
## Decision
We will [decision].
## Consequences
```

## Template: MADR 4.0 (complete)

```
# [Short title: problem + solution]
**Date:** YYYY-MM-DD
**Status:** proposed | accepted | deprecated | superseded by ADR-NNNN

## Context and Problem Statement
## Decision Drivers
## Considered Options
## Decision Outcome
Chosen option: "[Option N]", because [justification tied to the drivers].
### Confirmation
[How to validate the decision]
### Consequences
- Good, because [...]
- Bad, because [...]
- Neutral, because [...]
## Pros and Cons of the Options
### [Option 1-N]
- Good, because [...]
- Bad, because [...]
## More Information
```

## Naming Convention

- Format: `ADR-NNNN` (zero-padded 4 digits)
- Title: noun phrase describing the decision
- File: stored in `docs/adr/`

## Status Lifecycle

`proposed` -> `accepted` -> (`deprecated` | `superseded by ADR-NNNN`)

When superseding: update old ADR status to "superseded by ADR-NNNN".

## Validation Checklist

- [ ] Context is factual and neutral (no judgment)
- [ ] Decision drivers are explicit
- [ ] >= 2 options considered (3 for MADR)
- [ ] Decision in active voice ("We will...")
- [ ] Justification tied to the drivers
- [ ] Positive, negative, and neutral consequences kept separate
- [ ] Links to docs/RFCs/issues/superseded ADRs
- [ ] Correct status
- [ ] Date filled in (Default and MADR)
- [ ] Confidence level (Default only)

## Foundational ADR-0001

Offer this when creating an ADR folder. Content: the decision to use ADRs in Markdown under `docs/adr/`, versioned with the source code.

## Special Modes

- **Supersede**: create a new ADR + update the old ADR's status
- **Backfill**: document an implicit decision already in place, and note in the context that it is a backfill
