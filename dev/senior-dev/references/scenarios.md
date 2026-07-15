# Special Scenarios

## Incident or Production Regression

When analyzing a recurrent issue or incident:

1. **Require reproducibility** — either a reproducible failing signal or an explicit investigation plan
2. **Rank root-cause hypotheses** with evidence and confidence for each
3. **Decide containment** — fix-forward or rollback, with rationale and impact analysis
4. **Plan the durable fix** — not just the quick patch; address the root cause with regression protection
5. **Define regression protection** — targeted tests, monitoring additions, runbook updates

## Code Review and Release Readiness

When asked to review a change or assess release readiness:

1. **Prioritize by risk** — bugs, regressions, operational failures first; style last
2. **Check acceptance criteria coverage** — do the tests validate all stated requirements?
3. **Block if critical checks fail** or if rollback is undefined
4. **Provide severity-ranked actions** — what must be fixed vs. what's nice-to-have
5. **Give clear go/no-go verdict** with rationale

## Prioritization and Trade-offs

When asked to prioritize work (e.g., "which of these 5 items should we do first?"):

1. Define a transparent prioritization model (impact, risk, effort, strategic fit)
2. Score each option against the model
3. Explain trade-offs (optimizing for what, accepting what downside)
4. Surface risks of deferring non-selected items
