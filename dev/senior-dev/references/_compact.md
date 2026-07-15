# Senior Dev — Compact Reference

## Workflow (6 Steps)

| Step | Activity | Tier coverage |
|------|----------|---------------|
| 0 | Discover project standards | All tiers |
| 1 | Frame engineering problem | Deep only |
| 2 | Evaluate solution options | Standard + Deep |
| 3 | Plan implementation & validation | Standard + Deep |
| 4 | Execute, test, verify quality | Standard + Deep |
| 5 | Review, learn, iterate | Deep only |

**Standard tier = Steps 0 + 2 + 3 + 4. Quick tier = skip workflow entirely.**

### Step 0 — Standards loading order

1. Load `std/_shared/` (always)
2. Detect project from cwd or explicit arg, load `std/<project>/`
3. Scan repo: `CLAUDE.md` > `docs/decisions/` > `docs/stds/` > `docs/INIT.md` > `docs/CONSTRAINT.md` > tooling configs
4. **Project-local overrides bundled standards on conflict**
5. Surface conflicts with user request explicitly

### Step 1 — Problem framing checklist

- [ ] Business intent
- [ ] Scope boundaries (in vs out)
- [ ] Non-functional requirements (latency, throughput, reliability, scale, cost)
- [ ] Constraints (regulatory, architectural, team, stack)
- [ ] Dependencies and risks
- [ ] Surface what's missing before proceeding

### Step 2 — Option evaluation

- Minimum 2 viable options; 1 must be low-complexity baseline
- Dimensions: complexity, reliability, scalability, maintainability, time-to-deliver, cost, resource budget
- Per option ask: network round-trips? allocations? failure mode under load?
- Reject poor cost/benefit. Be explicit about constraint violations.

### Step 3 — Implementation plan requirements

- [ ] Incremental steps with acceptance criteria (verifiable)
- [ ] Test coverage for every behavior change
- [ ] Rollback plan for every release
- [ ] Acceptance criteria mapped to concrete checks

### Step 4 — Test form selection

| Context | Test form |
|---------|-----------|
| Pure logic | Unit test |
| DB queries/migrations | Integration test against real DB |
| HTTP endpoints / API contracts | Request-level test |
| Multi-service flow | Manual e2e or scripted scenario |
| UI behavior | Manual test + visual verification |
| Race conditions / concurrency | Stress test or targeted repro |
| Config / env / deployment | Smoke test in target environment |

After every implementation step: `tsc --noEmit` then pertinent test form. Critical paths: test failure modes too.

### Step 5 — Iterate if

- Acceptance criteria partially validated
- Risk unclear
- Quality score < 80/100

---

## Output Contract

### Quick (no marker, < 10 lines)

```
**Decision:** [1-2 sentences]
**Confidence:** low / medium / high — [1 phrase]
```

No Next line. Self-contained.

### Standard (state marker + 5 sections + Next)

```
[Standard · Step X/4 · <activity> · <project>]
1. Applicable Standards
2. Decision (2-3 sentences)
3. Trade-offs (comparison table)
4. Implementation Plan (steps + acceptance criteria + rollback)
5. Risks (top 2-3, severity + mitigation)
-> Next: [single concrete action] · or: [alternative]
```

### Deep (state marker + 7 sections + Decision Log + Next)

```
[Deep · Step X/6 · <activity> · <project>]
1. Applicable Standards
2. Executive Summary (2-3 sentences)
3. Technical Decisions (option + trade-offs + justification)
4. Implementation Plan (steps + acceptance criteria + tests + release gates)
5. Validation Evidence (checks run + results + failures)
6. Risks and Limitations (unknowns + severity/owner/mitigation)
7. Confidence (low/medium/high + rationale)
Decision Log: [ADR proposal]
-> Next: [action or handoff]
```

### Next line rules

- **Mandatory** for Standard and Deep
- Must propose forward motion (concrete action)
- Never: "let me know", "think about it", or omit entirely

---

## Decision Log (ADR)

- Path: `docs/decisions/NNNN-kebab-title.md`
- Length: 15-25 lines max
- Required fields: Date, Status (Accepted/Superseded), Context (3-5 lines), Decision (2-3 lines), Alternatives considered (1 line each + rejection reason), Kill criterion

| Situation | Behavior |
|-----------|----------|
| No `docs/decisions/` exists | Propose bootstrap, never auto-execute |
| `docs/decisions/` exists | Write next ADR automatically (unless user said "skip ADR") |
| New decision supersedes old | Mark old as `Status: Superseded by NNNN` |
| New decision refines old | Add `Refines: NNNN`, keep old Accepted |

---

## Handoffs

| Direction | Rule |
|-----------|------|
| From architecture-conceptor | Treat upstream decision as constraint. Do not re-debate. |
| To apply | Propose explicitly: "Hand off to apply for backlog + execution?" |
| Back to architecture-conceptor | Surface if question is architectural, not implementation. Let user choose. |

---

## Cross-Service Rules

### Coupling taxonomy

| Type | Acceptable? |
|------|-------------|
| Domain coupling | Yes |
| Implementation coupling | Defect |
| Temporal coupling | Defect (mitigate: circuit breaker) |
| Deployment coupling | Defect |

**Deploy test:** "Can I deploy A without touching B?" If no = coupling defect.

### Boundary checklist

- [ ] Contract defined first (typed API shape before implementation)
- [ ] Headers extracted once in middleware, never in business logic
- [ ] Independent deploy
- [ ] Independent test (mocked HTTP)
- [ ] Authorization in the service that owns the data

### Sharing rules

| OK to share | NOT OK to share |
|-------------|-----------------|
| API spec / boundary types | Internal domain types |
| Infra utilities (logging, tracing) | Business logic |
| Contract enum values | DB-constraint enum values |
| Error code conventions | Internal error handling |

### Anti-patterns

| Anti-pattern | Fix |
|--------------|-----|
| Distributed monolith | Contract-first; independent pipelines |
| Shared database | DB per service; API or events for data |
| Chatty services | BFF aggregation or CQRS read models |
| Leaking internals | Map to/from internal at boundary |
| Shared domain types | Each service owns its types; contract types only at boundary |

### Solo-dev pragmatism

**Enforce:** typed boundary middleware, independent deploys, read downstream contract before coding upstream.
**Relax:** Pact testing, full event-driven arch, separate repos, separate API gateway.

---

## Low-Level Lens

### Silent checklist (before any recommendation)

- [ ] Network round-trips per user action?
- [ ] Timeout x concurrency = pool exhaustion risk?
- [ ] Where is state held? Failure mode if that location fails?
- [ ] Backpressure: producer faster than consumer?

### Resource reasoning test

| Question | What it catches |
|----------|-----------------|
| Worst-case memory consumption? Bounded? | Unbounded buffer crash |
| Who owns this resource? When freed? | Pool/handle/listener leaks |
| Two things happen simultaneously? | Race conditions |
| Failure mode: crash, hang, or corrupt? | Silent corruption (fail-fast preferred) |

### Surface low-level perspective when

- Discussing performance, scaling, resource budgets
- Adding a dependency (what does it do at syscall level?)
- Debugging production issues
- Someone says "just add a queue/cache/service"

---

## Quality Rubric (100 pts)

| Dimension | Points | Key criteria |
|-----------|--------|-------------|
| Engineering Fit | 25 | Problem frame complete; solution matches objective + constraints |
| Technical Rigor & Trade-offs | 20 | 2+ options (1 low-complexity); multi-dimensional comparison; explicit justification |
| Validation Evidence | 20 | Measurable acceptance criteria; mapped to concrete checks; reproducible |
| Operational Safety | 20 | Rollback defined; observability addressed; risks listed with severity/owner |
| Clarity & Actionability | 15 | Concrete next steps; ownership assigned; blockers flagged; no clarification needed |

### Hard fail conditions (override total score)

1. Critical decision lacks trade-off analysis
2. Critical behavior change lacks validation strategy
3. Release recommendation has no rollback path
4. High-severity risk buried or unowned

### Delivery thresholds

| Score | Action |
|-------|--------|
| 80-100 | Execute |
| 70-79 | Flag gaps to user before proceeding |
| < 70 | Iterate before closure |

---

## Special Scenarios

### Incident / Production Regression

1. Require reproducibility or explicit investigation plan
2. Rank root-cause hypotheses with evidence + confidence
3. Decide containment: fix-forward or rollback with rationale
4. Plan durable fix (not just patch) with regression protection
5. Define: targeted tests, monitoring additions, runbook updates

### Code Review / Release Readiness

1. Prioritize by risk (bugs > regressions > operational failures > style)
2. Check acceptance criteria coverage
3. Block if critical checks fail or rollback undefined
4. Severity-ranked actions (must-fix vs nice-to-have)
5. Clear go/no-go verdict with rationale

### Prioritization

1. Define transparent model (impact, risk, effort, strategic fit)
2. Score each option
3. Explain trade-offs (optimizing for X at cost of Y)
4. Surface risks of deferring non-selected items

---

## Consensus & Mentoring

**Consensus process:** 1:1 with opposition first, find middle ground, presell 24h before meeting, frame for decision maker (recommendation + cost of action/inaction + risks + consensus status).

| Pattern | Use |
|---------|-----|
| Async RFC | Default |
| Structured meeting | 5+10+20+5+5 min |
| Disagree and commit | State concern, then commit fully |
| Override | Only if most senior + time-critical safety |
| Compromise (default) | Minimum change for both concerns |
| Escalate | After failed consensus; frame as differing risk models |

**Mentoring:** ask questions (not answers), structure growth (3-5 concrete skills), bi-weekly 1:1s, advocate quarterly. Green flag: mentee mentors someone else.
