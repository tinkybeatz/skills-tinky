# BACKLOGER Rubric

## Goal

Evaluate whether a `BACKLOGER` output accurately transforms a source report into a structured, evidence-backed, and execution-ready backlog.
Total score: 100 points.

## Scoring grid

### 1) Alignment with source report intent — 25 pts

- 0-8: weak linkage to report decisions, items invented or misinterpreted
- 9-16: partially aligned, some report decisions missing or distorted
- 17-25: all report decisions accurately extracted, scope matches report intent

### 2) Evidence quality and decision traceability — 25 pts

- 0-8: items lack source references, assumptions not flagged
- 9-16: mixed traceability, some items without evidence links
- 17-25: every item traceable to source report section and codebase reference

### 3) Backlog item completeness — 20 pts

- 0-6: mandatory fields missing, acceptance criteria absent or untestable
- 7-13: most fields present, some criteria vague or untestable
- 14-20: all mandatory fields present, acceptance criteria are concrete and verifiable

### 4) Sequencing, dependency clarity, and readiness — 15 pts

- 0-5: no dependency analysis, sequence unclear or contradictory
- 6-10: partial dependency mapping, some ordering issues
- 11-15: clear dependency matrix, logical sequence, readiness gate applied to all `Now` items

### 5) Transparency of risks and limitations — 15 pts

- 0-5: risks and unknowns missing or vague
- 6-10: basic risk listing with limited impact framing
- 11-15: explicit assumptions, dependency risks, source report gaps, and mitigation direction

## Delivery thresholds

- 80-100: robust output, ready for TASKER handoff
- 70-79: usable with explicit reservations, may need user clarification
- < 70: rerun extraction and restructuring before handoff

## Hard fail conditions

Any of the following should trigger rejection regardless of total score:

- backlog items invented from assumptions not present in source report
- `Now` items without testable acceptance criteria
- circular dependencies not detected or flagged
- no evidence linking items to source report decisions
- blocked evidence validation ignored (proceeding despite vague source)

## Reviewer checklist

- Does every backlog item trace back to a specific source report decision?
- Are acceptance criteria concrete and testable (not vague aspirations)?
- Is the dependency matrix complete and free of circular dependencies?
- Are `Now` items validated against the Definition of Ready?
- Are risks, assumptions, and source report gaps explicitly documented?
- Is the execution sequence logically sound (foundations before dependents)?
