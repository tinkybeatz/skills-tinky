# TASKER Rubric

## Goal

Evaluate whether a `TASKER` output delivers backlog items with clear scope control, complete acceptance coverage, and auditable evidence.
Total score: 100 points.

## Scoring grid

### 1) Alignment with backlog objective and scope — 20 pts

- 0-6: scope does not match backlog intent
- 7-13: partial scope alignment, important drift or gaps
- 14-20: clear and controlled alignment with backlog objective/scope

### 2) Acceptance criteria coverage and correctness — 25 pts

- 0-8: criteria missing or weakly validated
- 9-16: partial criteria coverage with unresolved ambiguity
- 17-25: full criteria mapping and explicit pass/fail validation

### 3) Evidence quality and traceability — 20 pts

- 0-6: claims with weak or missing evidence
- 7-13: mixed evidence quality or incomplete traceability
- 14-20: strong, reproducible evidence linked to each critical claim

### 4) Standards, associated audits, and test compliance — 20 pts

- 0-6: required standards/audits/tests not addressed
- 7-13: partial compliance with residual critical gaps
- 14-20: required standards, associated audits, and tests fully covered and reported

### 5) Transparency of risks, limitations, and next actions — 15 pts

- 0-5: risks/limitations are unclear or missing
- 6-10: basic transparency, but mitigation lacks precision
- 11-15: explicit residual risk, clear limitations, actionable next steps

## Delivery thresholds

- 80-100: robust output, closure candidate
- 70-79: usable with explicit reservations
- < 70: another execution iteration is required

## Hard fail conditions

Any of the following should trigger rejection regardless of total score:

- item executed without passing readiness gate
- closure claimed while one or more acceptance criteria remain unvalidated
- critical completion claims without direct evidence artifacts
- required standards coverage ignored for the backlog item
- required standard marked compliant without associated audit verification

## Reviewer checklist

- Does execution stay within the approved backlog scope?
- Is each acceptance criterion explicitly validated with pass/fail status?
- Is evidence reproducible and easy to trace?
- Are required standards, associated audits, and tests clearly covered?
- Are limitations and risks explicit with concrete next actions?
