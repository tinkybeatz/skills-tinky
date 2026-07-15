# Senior Developer Output Rubric

Use this rubric to score senior-dev outputs. Total: 100 points.

## 1) Engineering Fit — 25 pts

How well does the solution match the real problem and constraints?

- **0-8:** Solution doesn't match the problem or violates stated constraints
- **9-16:** Partially aligned; key requirements or constraints are missing
- **17-25:** Fully aligned with objective, scope, and non-functional requirements

**Checklist:**

- [ ] Problem frame includes business intent, scope, constraints, and non-functional requirements
- [ ] Proposed solution addresses the stated objective
- [ ] Solution respects all stated constraints (latency, budget, timeline, etc.)
- [ ] Out-of-scope items are explicitly excluded

---

## 2) Technical Rigor and Trade-offs — 20 pts

Is the technical reasoning sound? Are trade-offs explicit and defensible?

- **0-6:** No meaningful options; trade-off reasoning absent or circular
- **7-13:** Some options discussed; comparison is weak or one-dimensional
- **14-20:** Strong option analysis with multi-dimensional comparison; finalists are justified

**Checklist:**

- [ ] At least 2 viable options generated (1 is low-complexity baseline)
- [ ] Comparison is multi-dimensional (complexity, reliability, scalability, cost, time, maintainability)
- [ ] Trade-offs are explicitly named (e.g., "we're optimizing for X at the cost of Y")
- [ ] Selected option has explicit justification vs. alternatives
- [ ] For high-impact decisions: 2+ independent technical reasons to recommend the choice

---

## 3) Validation Evidence — 20 pts

Are claims backed by reproducible checks or official references?

- **0-6:** Claims are unsupported; no checks or references provided
- **7-13:** Some checks or references; critical gaps remain
- **14-20:** Checks are mapped to acceptance criteria; evidence is traceable and reproducible

**Checklist:**

- [ ] Acceptance criteria are measurable (not vague aspirations)
- [ ] Acceptance criteria are mapped to concrete checks (tests, metrics, manual steps)
- [ ] All major claims are backed by evidence (code, documentation, test results, logs)
- [ ] Evidence is reproducible (can someone else verify it independently?)

---

## 4) Operational Safety and Maintainability — 20 pts

Does the plan account for rollback, observability, and long-term maintenance?

- **0-6:** Rollback undefined; observability absent; high maintenance burden
- **7-13:** Baseline safety present but weak risk handling or unclear rollback
- **14-20:** Explicit rollback, clear observability, risk ownership, maintainable design

**Checklist:**

- [ ] Rollback or containment plan is defined and low-effort
- [ ] Observability (logging, metrics, monitoring) is explicitly addressed
- [ ] Known risks are listed with severity, impact, and owner
- [ ] Design prioritizes maintainability (clear code, testability, debuggability)

---

## 5) Clarity and Actionability — 15 pts

Is the output clear enough for someone to execute immediately?

- **0-5:** Unclear; hard to extract action items
- **6-10:** Understandable but incomplete or poorly prioritized
- **11-15:** Clear, concise, prioritized, directly executable

**Checklist:**

- [ ] Next steps are concrete and prioritized
- [ ] Ownership is assigned (who owns each step?)
- [ ] Critical blockers are flagged
- [ ] Ambiguities are resolved or explicitly called out
- [ ] Reader can execute without coming back for clarification

---

## Hard Fail Conditions

Output fails regardless of total score if:

1. **Critical decision lacks trade-off analysis** — selected approach has no justification vs. alternatives
2. **Critical behavior change lacks validation strategy** — "we'll test this somehow" is not acceptable
3. **Release recommendation has no rollback path** — either define rollback or recommend no-go
4. **High-severity risk is buried or not owned** — must be surfaced explicitly with owner/mitigation

---

## Delivery Thresholds

- **80-100:** Production-ready output. Execute.
- **70-79:** Usable with explicit reservations. Flag gaps to user before proceeding.
- **< 70:** Iterate before closure. Gather more info or refine analysis.

---

## Scoring Example

**Output:** Recommendation to switch from monolithic service to microservices.

**Rubric assessment:**

- Engineering fit: Does it address the stated bottleneck (scaling)? Are you respecting timeline and team constraints? → 18/25
- Rigor and trade-offs: Did you compare monolith-refactor, async-redesign, and microservices? Are costs/risks clear? → 16/20
- Validation: Are acceptance criteria concrete (time-to-scale threshold)? Are you measuring the improvement? → 13/20
- Safety and maintainability: Is the rollback plan clear (revert to old service)? Are operational runbooks defined? → 17/20
- Clarity: Can an engineer read this and know exactly what to build and in what order? → 12/15

**Total: 76 / 100** — Usable but needs work. Specifically: tighten validation criteria (add concrete metrics), make team impact clearer, and define the operational runbook before launch.
