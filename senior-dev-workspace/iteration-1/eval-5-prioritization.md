# Test Case 5: Technical Debt Prioritization

## Step 1: Problem Frame

**Objective:** Prioritize 12 technical debt items for a 2-week sprint.

**Backlog breakdown:**

- 3 database migrations
- 2 async refactors
- 4 test improvements
- 3 logging/observability upgrades

**Constraints:**

- Team capacity: 2 weeks
- Current state: 1–2 production incidents/week (mostly observability-related)
- No new features planned this sprint

**Key context:**

- Incident rate suggests observability gaps are operational pain
- Database migrations are likely performance-related or schema debt
- Async refactors may be quality or scalability debt
- Test improvements affect deployment confidence

**Key unknowns:**

- Impact of each debt item (time saved, incidents prevented, team velocity impact?)
- Effort estimation for each item?
- Business impact prioritization (is preventing incidents more valuable than tech velocity?)

---

## Step 2: Define Prioritization Model

I'll use a weighted scoring model with these dimensions:

| Dimension                   | Weight | Rationale                                                                    |
| --------------------------- | ------ | ---------------------------------------------------------------------------- |
| **Impact on reliability**   | 35%    | Incidents are business-critical; observability gaps directly cause incidents |
| **Impact on team velocity** | 25%    | Unblocking engineering capacity for features                                 |
| **Implementation effort**   | 25%    | Want to maximize items completed in 2 weeks                                  |
| **Risk if deferred**        | 15%    | Cost of pushing to next sprint                                               |

**Scoring:** 1–5 scale (1 = no impact, 5 = critical impact)

---

## Step 3: Assess Each Item

### Database Migrations (3 items)

**Migration 1: Add user_segment index**

- **Reliability impact:** 3 (improves query perf, but not preventing incidents)
- **Velocity impact:** 3 (faster queries = faster feature development)
- **Effort:** 2 (low: create index, test, deploy)
- **Deferral risk:** 2 (can defer 1 sprint without pain)
- **Score:** (3 × 0.35) + (3 × 0.25) + (4 × 0.25, inverted) + (2 × 0.15) = 1.05 + 0.75 + 1.0 + 0.3 = **3.1**

**Migration 2: Denormalize invoice_total in orders table**

- **Reliability impact:** 2 (perf improvement, not reliability)
- **Velocity impact:** 4 (commonly calculated field, speeds up several queries)
- **Effort:** 4 (medium: schema change, backfill, test)
- **Deferral risk:** 1 (doesn't hurt if deferred)
- **Score:** (2 × 0.35) + (4 × 0.25) + (1 × 0.25) + (1 × 0.15) = 0.7 + 1.0 + 0.25 + 0.15 = **2.1**

**Migration 3: Archive old transaction logs (data retention)**

- **Reliability impact:** 2 (table bloat could slow queries eventually)
- **Velocity impact:** 1 (low direct benefit)
- **Effort:** 3 (medium: archive script, verify, monitor)
- **Deferral risk:** 3 (bloat grows; becomes urgent in 2–3 sprints)
- **Score:** (2 × 0.35) + (1 × 0.25) + (2 × 0.25) + (3 × 0.15) = 0.7 + 0.25 + 0.5 + 0.45 = **1.9**

---

### Async Refactors (2 items)

**Async 1: Email sending to async queue**

- **Reliability impact:** 4 (blocking email sends can timeout requests)
- **Velocity impact:** 3 (faster request handling, better UX)
- **Effort:** 3 (medium: add queue, worker, error handling)
- **Deferral risk:** 4 (becoming user-facing issue)
- **Score:** (4 × 0.35) + (3 × 0.25) + (2 × 0.25) + (4 × 0.15) = 1.4 + 0.75 + 0.5 + 0.6 = **3.25**

**Async 2: Payment webhook processing async**

- **Reliability impact:** 5 (webhook timeouts = "ghost" payments)
- **Velocity impact:** 2 (indirect benefit)
- **Effort:** 4 (high: complex error handling, idempotency, retry)
- **Deferral risk:** 5 (critical path; high risk)
- **Score:** (5 × 0.35) + (2 × 0.25) + (1 × 0.25) + (5 × 0.15) = 1.75 + 0.5 + 0.25 + 0.75 = **3.25**

---

### Test Improvements (4 items)

**Test 1: Add integration tests for payment flow**

- **Reliability impact:** 5 (prevents regressions in critical path)
- **Velocity impact:** 3 (faster deployment, less review time)
- **Effort:** 3 (medium: test setup, mocking, cases)
- **Deferral risk:** 4 (high: every release is risky without these)
- **Score:** (5 × 0.35) + (3 × 0.25) + (2 × 0.25) + (4 × 0.15) = 1.75 + 0.75 + 0.5 + 0.6 = **3.6**

**Test 2: Improve E2E test coverage (checkout flow)**

- **Reliability impact:** 4 (catches user-facing regressions)
- **Velocity impact:** 2 (review time savings)
- **Effort:** 4 (high: writing + maintaining E2E tests)
- **Deferral risk:** 2 (useful but not critical)
- **Score:** (4 × 0.35) + (2 × 0.25) + (1 × 0.25) + (2 × 0.15) = 1.4 + 0.5 + 0.25 + 0.3 = **2.45**

**Test 3: Load testing for peak scenarios**

- **Reliability impact:** 3 (identifies scalability limits)
- **Velocity impact:** 1 (indirect)
- **Effort:** 3 (medium: infrastructure, scripts)
- **Deferral risk:** 2 (can defer if not hitting limits soon)
- **Score:** (3 × 0.35) + (1 × 0.25) + (2 × 0.25) + (2 × 0.15) = 1.05 + 0.25 + 0.5 + 0.3 = **2.1**

**Test 4: Unit test coverage improvements (general)**

- **Reliability impact:** 2 (helps but not preventing incidents)
- **Velocity impact:** 2 (minor velocity gain)
- **Effort:** 2 (low: straightforward test adding)
- **Deferral risk:** 1 (can always improve coverage)
- **Score:** (2 × 0.35) + (2 × 0.25) + (3 × 0.25) + (1 × 0.15) = 0.7 + 0.5 + 0.75 + 0.15 = **2.1**

---

### Logging/Observability (3 items)

**Obs 1: Structured logging for payment flows**

- **Reliability impact:** 5 (debugging incidents is 10x faster with structured logs)
- **Velocity impact:** 3 (faster incident response = less firefighting)
- **Effort:** 2 (low: standard boilerplate, easy to deploy)
- **Deferral risk:** 4 (each incident is harder to debug without this)
- **Score:** (5 × 0.35) + (3 × 0.25) + (3 × 0.25) + (4 × 0.15) = 1.75 + 0.75 + 0.75 + 0.6 = **3.85**

**Obs 2: Add distributed tracing (critical path)**

- **Reliability impact:** 4 (latency debugging, cross-service visibility)
- **Velocity impact:** 4 (drastically faster incident diagnosis)
- **Effort:** 4 (high: instrumentation, agent setup, dashboard)
- **Deferral risk:** 3 (not immediate, but limits scale)
- **Score:** (4 × 0.35) + (4 × 0.25) + (1 × 0.25) + (3 × 0.15) = 1.4 + 1.0 + 0.25 + 0.45 = **3.1**

**Obs 3: Custom alerting for payment failures**

- **Reliability impact:** 5 (catch payment failures immediately)
- **Velocity impact:** 2 (mostly ops benefit)
- **Effort:** 1 (low: query + threshold, easy setup)
- **Deferral risk:** 5 (currently only discovered by customers)
- **Score:** (5 × 0.35) + (2 × 0.25) + (4 × 0.25) + (5 × 0.15) = 1.75 + 0.5 + 1.0 + 0.75 = **4.0**

---

## Step 4: Ranked Scores (All Items)

| Item                                   | Category  | Score    | Effort | Rationale                                                               |
| -------------------------------------- | --------- | -------- | ------ | ----------------------------------------------------------------------- |
| **Custom alerting (payment failures)** | Obs       | **4.0**  | ⭐     | Highest impact, lowest effort. Catch payment failures immediately.      |
| **Structured logging (payment flows)** | Obs       | **3.85** | ⭐⭐   | Critical for incident debugging. 1–2 incidents/week → direct ROI.       |
| **Integration tests (payment)**        | Test      | **3.6**  | ⭐⭐   | Prevents regressions in critical path. High reliability impact.         |
| **Email async**                        | Async     | **3.25** | ⭐⭐   | Improves reliability; prevents request timeouts. Med effort.            |
| **Payment webhook async**              | Async     | **3.25** | ⭐⭐⭐ | Critical reliability, but high effort. Consider splitting or deferring. |
| **Distributed tracing**                | Obs       | **3.1**  | ⭐⭐⭐ | Valuable but high effort; defer if time-constrained.                    |
| **Add user_segment index**             | Migration | **3.1**  | ⭐     | Quick win; small perf boost.                                            |
| **Denormalize invoice_total**          | Migration | **2.1**  | ⭐⭐   | Medium effort, low reliability impact; can defer.                       |
| **E2E checkout tests**                 | Test      | **2.45** | ⭐⭐⭐ | High effort; prioritize unit/integration first.                         |
| **Load testing**                       | Test      | **2.1**  | ⭐⭐   | Useful but can defer if no immediate scaling concerns.                  |
| **Unit test coverage**                 | Test      | **2.1**  | ⭐     | Always good; low priority vs. others.                                   |
| **Archive transaction logs**           | Migration | **1.9**  | ⭐⭐   | Deferred pain; not urgent this sprint.                                  |

---

## Step 5: Top 3 Recommendation

**Selection criteria:** Maximize impact while fitting in 2 weeks (balance effort).

### **PICK 1: Custom alerting for payment failures** (Score: 4.0, Effort: LOW)

- **Why:** Highest combined impact (reliability + effort ratio); directly addresses incident rate
- **Scope:** Add alerts for failed payment transitions, retry exhaustion
- **Effort estimate:** 2–3 days
- **Expected outcome:** Catch payment failures before customers complain

### **PICK 2: Structured logging for payment flows** (Score: 3.85, Effort: LOW-MEDIUM)

- **Why:** Enables faster incident debugging; directly improves oncall experience
- **Scope:** Add structured logs for payment state transitions, errors, timeouts
- **Effort estimate:** 3–4 days
- **Expected outcome:** Incident diagnosis time 10x faster

### **PICK 3: Integration tests for payment** (Score: 3.6, Effort: MEDIUM)

- **Why:** High reliability impact; unblocks confident payment changes
- **Scope:** Happy path + error scenarios (declined card, timeout, network errors)
- **Effort estimate:** 4–5 days
- **Expected outcome:** Deploy payment changes with confidence; fewer regressions

**Total effort:** 9–12 days in a 10-day sprint (conservative estimate + buffer)

---

## Step 6: Why NOT the Others (and Deferral Risk)

| Item                  | Score | Why deferred                                             | Deferral cost                                         | Next review       |
| --------------------- | ----- | -------------------------------------------------------- | ----------------------------------------------------- | ----------------- |
| Email async           | 3.25  | Defer for a sprint; low-medium risk                      | Minority of timeouts are email; acceptable            | Sprint N+1        |
| Payment webhook async | 3.25  | Too high effort (⭐⭐⭐) for combined sprint; split work | Risk remains high; escalate if incidents              | Sprint N+1 or N+2 |
| Distributed tracing   | 3.1   | High effort (⭐⭐⭐); lower ROI than logging/alerting    | Cross-service latency blind spots; acceptable for now | Sprint N+2        |
| User_segment index    | 3.1   | Can defer; low-priority perf improvement                 | Query perf slight; not blocking                       | Sprint N+1        |

**Deferral strategy:**

- Items 1–3 (pick picks): Do this sprint
- Payment webhook async: Escalate to product/leadership if incidents recur; may prioritize in sprint N+1
- Others: Backlog for sprint N+1

---

## Step 7: Implementation Plan (Sprint N)

### Week 1

**Mon–Tue: Custom alerting (payment failures)**

- Engineer A: Set up alert rules in monitoring platform
- Engineer B: Validate alerts with test scenarios
- Acceptance: Alerts fire on failed payment transitions, visible to team
- Deployment: Monday EOD, live by Tuesday EOD

**Wed–Fri: Structured logging (payment flows)**

- Engineer A + B: Add structured logs to payment service
- QA: Validate log output and format
- Acceptance: All payment events logged with trace ID, state, errors
- Deployment: Friday EOD

### Week 2

**Mon–Wed: Integration tests (payment)**

- Engineer A: Happy path + common error cases
- Engineer B: Edge cases (timeout, network errors, retries)
- QA: Coverage review
- Acceptance: 85%+ test pass rate, coverage of all error paths

**Wed–Fri: Buffer + validation + documentation**

- All: Verify all items in production
- A: Documentation for new alerts and logs
- B: Update runbooks with new observability

---

## Step 8: Success Criteria

After sprint completion, measure:

| Success Criterion                  | How to measure                                          | Target                                               |
| ---------------------------------- | ------------------------------------------------------- | ---------------------------------------------------- |
| Incident detection speed           | MTTR for payment failures                               | 50% reduction (currently: 30min → target: 15min)     |
| Incident root cause identification | Time to identify "why" in payment incidents             | Improved by 5x (manual log search → structured logs) |
| Deployment confidence              | Number of payment-related regressions after tests added | 0 regressions in next 4 releases                     |
| Team satisfaction                  | Oncall feedback on observability                        | Net positive feedback                                |

---

## Step 9: Confidence

**Level: HIGH**

**Rationale:**

- ✅ Prioritization model is transparent and weighted by business impact
- ✅ Top 3 picks directly address current pain (1–2 incidents/week)
- ✅ Effort estimates are realistic; fits in 2 weeks
- ✅ Deferral strategy is explicit; deferred items are lower-risk
- ⚠️ Payment webhook async remains high-risk; revisit next sprint if incidents escalate

**What would increase confidence:**

- Confirmation that team agrees with reliability/velocity weights
- If payment incidents reduce after alerting + logging deployed

---

## Next Steps

1. **[EOD today] Share prioritization to team for sign-off** — confirm scoring is acceptable — **Owner: Eng lead** — **Est: 1–2 hours**
2. **[Tomorrow] Break down top 3 into concrete tasks** — assign owners, estimate daily breakdown — **Owner: Eng lead** — **Est: 2–3 hours**
3. **[Sprint start] Execute in order** — Week 1: alerting & logging; Week 2: tests — **Owner: Team** — **Est: 2 weeks**
4. **[EOD sprint] Validate success criteria** — measure incident response improvement — **Owner: Eng lead + Ops** — **Est: 1–2 hours**
5. **[Sprint N+1] Revisit deferral list** — prioritize email async, payment async, or new work — **Owner: Eng lead** — **Est: 1 sprint** ●

---

## Summary

**Top 3 for this sprint:**

1. Custom alerting for payment failures (4.0 score, quick win)
2. Structured logging for payment flows (3.85 score, incident debugging)
3. Integration tests for payment (3.6 score, deployment confidence)

**Expected outcome:** 50% faster incident detection and diagnosis, zero payment regressions in next releases.

**Deferral risk:** Payment webhook async remains high-risk; revisit in sprint N+1 or if incidents increase.
