# BACKLOGER Examples

## Purpose

This file provides concrete input/output examples for the `BACKLOGER` profile.
Use these examples as behavioral references, not fixed text to copy.

## Example 1 — Architecture report to execution backlog

### Input

"Transform the architecture-conceptor ADR on payment module refactoring into an execution backlog."

### Expected behavior

- extract each architecture decision as a candidate backlog item
- validate feasibility against current codebase (check existing files, patterns, tests)
- structure items with full mandatory fields from BACKLOG_STANDARD
- sequence based on dependency graph (schema migration before service refactoring)
- flag risks (data migration, API contract breaking changes)

### Expected output shape

1. Executive summary (report type, item count, estimated effort)
2. Key points (critical path, major dependencies, sequencing rationale)
3. Evidence (ADR section references + codebase file references)
4. Limitations (assumptions about existing data, untested migration paths)
5. Confidence level with rationale
6. Next steps (user confirmation, then TASKER handoff)

Full backlog with items, dependency matrix, and global risks.

## Example 2 — Senior-dev post-mortem to fix backlog

### Input

"Create a backlog from the senior-dev analysis of the RLS authentication bypass incident."

### Expected behavior

- extract fix items: SQL migration, function ownership change, test coverage, monitoring
- link each item to specific post-mortem findings (evidence traceability)
- sequence: database fix first (foundation), then code changes, then tests, then monitoring
- flag risk: production data access during migration requires coordination
- acceptance criteria tied to verifiable checks (query returns expected results, tests pass)

### Expected output shape

1. Executive summary with incident context and fix scope
2. Key points (4 items, strict sequence, 1 risk requiring coordination)
3. Evidence map (post-mortem section → backlog item → codebase file)
4. Limitations (monitoring depends on infrastructure access not yet confirmed)
5. Confidence: high for DB/code fixes, medium for monitoring
6. Next steps: confirm with user, then hand off to TASKER

## Example 3 — Blocked due to vague source report

### Input

"Transform this brief into tasks." (brief contains only "improve user experience" and "increase performance" with no specifics)

### Expected behavior

- stop at evidence validation step (Step 2)
- do NOT generate backlog items from assumptions
- list exactly what is missing (specific decisions, affected components, success criteria, measurements)
- ask targeted clarification questions
- provide no backlog until clarification arrives

### Expected output shape

1. Executive summary: "Blocked — source report lacks actionable decisions"
2. Key points: list of missing elements
3. Evidence: none extractable from source
4. Limitations: cannot proceed without clarification
5. Confidence: N/A
6. Next steps: 4-5 specific clarification questions for the user

## Reusable response template

Use this structure in all final responses:

```md
## Executive summary

...

## Key points

- ...

## Evidence

- [Source report section](reference) - relevance rationale
- [Codebase file](path) - feasibility confirmation

## Limitations

- ...

## Confidence

- Level: low|medium|high
- Rationale: ...

## Next steps

- ...

## Backlog

### Execution sequence
1. BLG-001 — ...
2. BLG-002 — ...

### Items
[full items with mandatory fields]

### Dependency matrix
[table]

### Global risks
[list]
```
