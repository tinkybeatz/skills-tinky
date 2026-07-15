# Agile metrics guide — sprint-review reference

Adapted from a research report (April 2026, 30+ sources).

## Progress metrics

### The 4 essential metrics

| Metric | Measures | Interpretation |
|---|---|---|
| **Throughput** | Items delivered/sprint | Actual capacity |
| **Cycle Time** | "In Progress" → "Done" | Workflow efficiency |
| **Velocity** | Story points/sprint (3-5 sprint average) | Planning the next sprint |
| **WIP** | Tasks in progress at once | Focus — Little's Law: Lead Time = WIP / Throughput |

### Burnup > Burndown

The burnup makes scope creep visible (the scope line rises). Anti-patterns: a flat line = a blockage, a steep drop at the end of the sprint = batching.

### Monte Carlo Forecasting

| Percentile | Use |
|---|---|
| P50 | Median — 1 chance in 2 |
| P85 | **Recommended for external commitments** |
| P95 | Contractual deadlines |

Data required: 10+ sprints of historical throughput.

## Prioritization

### RICE (recommended default)

Score = (Reach × Impact × Confidence) / Effort

### WSJF (sequencing)

WSJF = Cost of Delay / Job Size — the job with the highest ratio goes first.

### Value/Effort matrix

- **Quick Wins**: high value, low effort → first
- **Big Bets**: high value, high effort → plan
- **Fill-ins**: low value, low effort → if time allows
- **Money Pits**: low value, high effort → eliminate

## Estimation

- **Story Points**: Fibonacci, precision for sprint planning
- **T-Shirt Sizing**: XS-XL, high-level roadmap
- **No-Estimates**: throughput-based, requires disciplined splitting

## Delivery quality

### Definition of Done — typical criteria

- Code reviewed and merged
- Tests pass (unit + integration)
- No regressions
- Documentation updated if needed
- Deployable to production

### Technical quality metrics

| Metric | Target | How to measure |
|---|---|---|
| Test coverage | > 80% of critical lines | `vitest --coverage` |
| Post-deploy bugs | < 1 per sprint | Ticket tracking |
| Review time | < 24h | Measure PR open → merge |
| Technical debt | 10-20% of the sprint | Items tagged "tech-debt" |
| Build time | < 5 min | CI pipeline |

## Change management

### Rolling Wave Planning

Detailed in the short term, high-level in the long term, re-planned iteratively.

### Backlog Refinement

- 10% of the sprint's capacity
- 30-40 items refined (1.5-2× velocity)
- Weekly review, monthly cleanup

### Now / Next / Later

| Column | Commitment |
|---|---|
| **Now** | Committed, acceptance criteria defined |
| **Next** | Likely, being shaped |
| **Later** | Flexible, assumptions to validate |

## Decision-making

### Timeboxing

1. Define the decision
2. Set a maximum discussion window
3. A decision owner decides if there is no consensus
4. Document the decision + conditions for revisiting it

### Technical debt — classification

| Type | Action |
|---|---|
| Prudent & Deliberate | Acceptable — document it |
| Prudent & Inadvertent | Normal — refactor |
| Reckless & Deliberate | Dangerous — avoid |
| Reckless & Inadvertent | Training needed |
</content>
