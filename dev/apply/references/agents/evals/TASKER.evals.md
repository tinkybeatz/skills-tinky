# TASKER Evaluation Set

## Objective

Validate that `TASKER` consistently executes backlog items with full acceptance coverage, standards-to-audits compliance, and auditable closure evidence.

## Evaluation protocol

For each test case:

1. Run one full execution cycle (intake gate, planning, implementation summary, validation, close/iterate decision).
2. Produce output using the required `TASKER` contract.
3. Score with `TASKER.rubric.md`.
4. Record pass/fail and failure reasons.

Pass criteria:

- score >= 80
- no hard fail condition

## Test cases

### TC-01 Ready backlog item complete execution

Prompt:

- "Execute BLG-003 from `/docs/backlogs/BACKLOG_PHASE1_FOUNDATION.md`."

Expected:

- mandatory readiness check passed
- complete criteria-to-test mapping
- explicit validation matrix
- closure decision with evidence

### TC-02 Non-ready item gate enforcement

Prompt:

- "Execute US-021 from backlog Z. Dependencies are undefined."

Expected:

- `blocked` decision at intake
- no implementation performed
- explicit missing fields and owner request
- clear next action for backlog refinement

### TC-03 Standards coverage verification

Prompt:

- "Close BLG-012 and confirm standards compliance."

Expected:

- standards list extracted from backlog traceability
- associated audit artifacts identified for each applicable standard
- evidence mapped to required rule coverage and associated audit checks
- no closure if required checks are missing

### TC-04 Partial test failure handling

Prompt:

- "Finalize US-009. Unit tests pass but integration tests fail."

Expected:

- explicit `iterate` decision
- failed criteria and risk impact documented
- mitigation steps and verification target defined

### TC-05 Scope drift pressure test

Prompt:

- "While executing BLG-006, include an additional dashboard feature not in scope."

Expected:

- explicit out-of-scope detection
- defer or split extra request with traceable rationale
- preserve original item execution integrity

### TC-06 Missing audit association gate

Prompt:

- "Close BLG-011. Standards are checked but no associated audits are documented."

Expected:

- explicit refusal to close
- missing standard-to-audit links listed
- decision set to `iterate` until audit verification is provided

## Reporting template

Use this after each evaluation run:

```md
## Eval Report - <TC-ID>

- Date:
- Evaluator:
- Final score:
- Hard fail: yes|no

### Criterion scores

- Backlog objective and scope alignment:
- Acceptance criteria coverage:
- Evidence quality and traceability:
- Standards, associated audits, and test compliance:
- Risk and limitation transparency:

### Outcome

- Pass|Fail

### Notes

- Strengths:
- Weaknesses:
- Fix actions:
```
