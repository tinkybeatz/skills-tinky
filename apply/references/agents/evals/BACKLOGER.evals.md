# BACKLOGER Evaluation Set

## Objective

Validate that `BACKLOGER` consistently transforms source reports into evidence-backed, structured, and execution-ready backlogs.

## Evaluation protocol

For each test case:

1. Run one full backloger cycle (intake, evidence validation, backlog structuring, sequencing, readiness gate, review).
2. Produce output using the required contract.
3. Score with `BACKLOGER.rubric.md`.
4. Record pass/fail and failure reasons.

Pass criteria:

- score >= 80
- no hard fail condition

## Test cases

### TC-01 Architecture report to backlog

Prompt:

- "Transform the architecture-conceptor ADR output into an execution backlog for the payment module refactoring."

Expected:

- each backlog item traceable to a specific ADR decision
- dependency matrix reflecting migration-before-refactor order
- all `Now` items marked `Ready` with testable acceptance criteria

### TC-02 Senior-dev incident analysis to backlog

Prompt:

- "Create a backlog from the senior-dev post-mortem on the RLS authentication bypass."

Expected:

- fix items extracted: SQL migration, function ownership, test coverage, monitoring
- evidence linking each item to post-mortem findings
- sequence: DB fix first, then code, then tests, then monitoring
- risk flagged for production data access during migration

### TC-03 Vague brief rejection

Prompt:

- "Transform this brief into tasks." (brief contains only high-level goals, no specific decisions)

Expected:

- explicit `blocked` decision at evidence validation step
- list of missing elements with specific clarification questions
- no backlog items generated until clarification is provided

### TC-04 Large scope overflow management

Prompt:

- "Create a backlog from this 20-point architecture redesign report."

Expected:

- max 10 items in `Now`, remainder in `Next`/`Later`
- explicit rationale for horizon assignment
- no quality reduction on `Now` items despite volume pressure

### TC-05 Circular dependency detection

Prompt:

- "Build a backlog where module A depends on module B's API, and module B depends on module A's schema migration."

Expected:

- circular dependency detected and flagged
- proposed resolution (merge, interface contract, or phased split)
- no sequencing that assumes both can proceed independently

## Reporting template

Use this after each evaluation run:

```md
## Eval Report - <TC-ID>

- Date:
- Evaluator:
- Final score:
- Hard fail: yes|no

### Criterion scores

- Source report alignment:
- Evidence and traceability:
- Backlog item completeness:
- Sequencing and readiness:
- Risk and limitation transparency:

### Outcome

- Pass|Fail

### Notes

- Strengths:
- Weaknesses:
- Fix actions:
```
