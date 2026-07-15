# ARCHITECTURE_CONCEPTOR Rubric

## Goal

Evaluate whether an `ARCHITECTURE_CONCEPTOR` output is well-framed, evidence-based, and produces actionable architecture decisions.
Total score: 100 points.

## Scoring grid

### 1) Fit to problem and constraints - 25 pts

- 0-8: architecture does not address the stated problem or ignores key constraints
- 9-16: partially aligned, some constraints or quality priorities missing
- 17-25: fully aligned with business objective, constraints, and quality attribute priorities

### 2) Evidence strength and traceability - 25 pts

- 0-8: claims unsupported or based on weak/undated sources
- 9-16: some evidence present but gaps in traceability or source quality
- 17-25: all critical claims backed by strong, traceable, independent sources

### 3) Trade-off rigor and decision quality - 20 pts

- 0-6: fewer than 3 options or no meaningful comparison
- 7-13: options compared but trade-offs are vague or incomplete
- 14-20: at least 3 options with explicit, defensible trade-offs and weighted scorecard

### 4) Clarity and actionability - 15 pts

- 0-5: unclear structure, hard to act on
- 6-10: understandable but missing steps or poorly prioritized
- 11-15: clear, concise, prioritized, directly executable next steps

### 5) Limitations and risk transparency - 15 pts

- 0-5: risks and limitations omitted or trivialized
- 6-10: some risks identified but not prioritized or owned
- 11-15: risks explicit, prioritized, with rollback triggers and ownership

## Delivery thresholds

- 80-100: strong deliverable
- 70-79: usable with explicit reservations
- < 70: rerun analysis cycle

## Hard fail conditions

Any of the following should trigger rejection regardless of total score:

- Architecture decision without at least 3 compared options
- Critical claim without at least 2 independent sources
- Recommendation without rollback triggers or validation plan
- Quality attribute priorities not established before option comparison
- Economic trade-offs entirely absent from decision rationale

## Reviewer checklist

- Is the problem framed with explicit constraints and quality priorities?
- Are at least 3 viable architecture options produced and compared?
- Are critical claims backed by strong, traceable evidence?
- Is there a weighted scorecard driving the final recommendation?
- Are trade-offs explicit and defensible?
- Are risks prioritized with rollback triggers and owners?
- Is there a validation plan with measurable checkpoints?
- Are limitations and confidence level stated transparently?
