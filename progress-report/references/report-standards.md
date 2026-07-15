# Progress Report Standards — Reference

Synthesis of a documentation report (April 2026, 50+ sources, 5 MECE agents).

## RAG Status — definitions

| Color | Meaning | Thresholds |
|---|---|---|
| **Green** | On track, no intervention | Variance < 5% |
| **Amber** | Attention required, action in progress | Variance 5-15% |
| **Red** | At risk, intervention needed | Variance > 15% |

Apply a RAG per dimension: Scope, Schedule, Cost, Quality, Risks.
Always accompany it with a comment + trend (↑↓→).

## Non-technical structure (3 pages max)

### Page 1 — Executive status
- Assertive title ("Invoices API delivered, onboarding blocked." — not "Status W17")
- RAG across 4 axes (scope, schedule, budget, risk)
- Executive summary: 3 sentences (state, trend, required decision)
- Achievements this period in business language (not technical)

### Page 2 — Schedule & budget
- Timeline of major milestones (planned vs actual)
- Budget consumed vs remaining (bar chart or simple table)
- Scope changes (change-request table with impact)

### Page 3 — Risks & next steps
- Top 3-5 risks with mitigation and owner
- Decisions required from the client (the most important section)
- Activities for the next period
- Legal notices / confidentiality

### Non-technical rules
- Business vocabulary only: "feature delivered" not "PR merged"
- Translate every advance into business impact
- No jargon: merge, refactor, CI/CD, endpoint = forbidden
- Visuals: RAG matrix, milestone timeline, budget bar chart
- Every problem presented with 2 options + recommendation

## Technical structure (no limit)

### Section 1 — Sprint overview
- Sprint goal + status
- Velocity (histogram of the last 5 sprints)
- Burndown/burnup of the current sprint
- Done / In progress / Blocked (with ticket links)

### Section 2 — Quality metrics
- Test coverage (% + trend)
- Build success rate
- Average PR review time
- Deploy frequency
- Open vs closed bugs

### Section 3 — Architectural changes
- ADRs made or to be made
- Dependencies added/updated
- Migrations in progress

### Section 4 — Technical debt
- Ratio of debt created vs paid down
- Priority debt tickets
- Estimated impact if left untreated

### Section 5 — Security & infra
- Vulnerabilities detected/fixed
- Uptime / incidents
- Monitoring alerts

### Section 6 — Technical risks
- External dependencies
- EOL / upgrades to plan
- Identified bottlenecks

### Section 7 — RAID log
- Risks, Assumptions, Issues, Dependencies
- Each item with owner, date, status

### Section 8 — Next steps
- Activities for the next period with estimated effort
- Value/Effort prioritization
- Technical decisions to make

## Cross-cutting principles

### Pyramid Principle
Conclusion first, then arguments, data last.
Each section title is an assertion, not a label.

### Anti-watermelon
Anchor statuses on objective metrics. If SPI < 0.9 = amber.
A project that is always green is suspicious.

### Bad News Early
Flag problems early. Every problem with 2 options + recommendation.

### 5-15 Rule
15 min to write, 5 min to read (for the non-technical version).

### Visualization (Tufte/Knaflic)
- High data-ink ratio, zero chartjunk
- Title = assertion ("3-day delay" not "Progress")
- Max 3 metrics per view
- Chart for trends, table for exact values
