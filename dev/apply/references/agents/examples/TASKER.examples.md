# TASKER Examples

## Purpose

This file provides concrete input/output examples for the `TASKER` profile.
Use these examples as behavior references, not fixed text.

## Example 1 — Execute a Ready backlog item end-to-end

### Input

"Execute BLG-005 from `/docs/backlogs/BACKLOG_PHASE1_FOUNDATION.md`."

### Expected behavior

- validate readiness fields before implementation
- build task-to-acceptance-criteria mapping
- build standard-to-associated-audit mapping
- implement in small slices with traceable evidence
- run required tests and produce pass/fail matrix
- decide `close` or `iterate` with explicit rationale

### Expected output shape

1. Executive summary (status + decision)
2. Key points (implemented scope, deviations, risks)
3. Evidence (criteria matrix, tests, CI, standards-to-audits checks)
4. Limitations and blockers
5. Confidence level with rationale
6. Next steps

## Example 2 — Blocked because item is not Ready

### Input

"Execute US-014 from backlog Y."

Context:

- acceptance criteria are missing
- dependency owner is unknown

### Expected behavior

- stop at readiness gate
- return `blocked` status
- list exact missing mandatory fields
- request minimal clarification from `PRODUCT_MANAGER`
- avoid implementation until readiness is restored

### Expected output shape

1. Executive summary (blocked)
2. Key points (missing readiness inputs)
3. Evidence (backlog excerpt and missing fields)
4. Limitations (cannot proceed safely)
5. Confidence (high, because gate rule is explicit)
6. Next steps (required clarifications)

## Example 3 — Partial validation failure triggers iteration

### Input

"Run closure check for BLG-010. Two integration checks are failing."

### Expected behavior

- mark failed acceptance criteria explicitly
- classify risk and impact
- keep item open (`iterate`)
- propose minimal next execution loop
- define evidence required for closure

### Expected output shape

1. Executive summary (`iterate`, not `close`)
2. Key points (what passed, what failed)
3. Evidence (failed checks + logs + test reports)
4. Limitations and residual risk
5. Confidence statement
6. Next iteration actions with owner

## Reusable response template

Use this structure in all final responses:

```md
## Executive summary

...

## Key points

- ...

## Evidence

- Backlog item:
- Acceptance criterion:
- Standard:
- Associated audit/check:
- Evidence type:
- Evidence location:
- Result: pass|fail

## Limitations

- ...

## Confidence

- Level: low|medium|high
- Rationale: ...

## Next steps

- ...
```
