# Test Case 4: Architecture Trade-off — Scaling Strategy

## Step 1: Problem Frame

**Objective:** Choose a scaling strategy to support 3x traffic growth in 6 months.

**Current state:**

- Single database server
- Monolithic service architecture

**Constraints:**

- Team size: 5 engineers (limited capacity for operational complexity)
- Budget: unconstrained (not a limiting factor)
- Operational complexity: _primary concern_
- Timeline: 6 months before hitting limits

**Non-functional requirements:**

- Must scale to 3x current traffic
- Maintain < 100ms p99 latency
- Support 99.9% availability

**Key unknowns:**

- Current database bottleneck (CPU, disk I/O, memory)?
- Read/write ratio (determines caching effectiveness)?
- Hot spots vs. evenly distributed load?

---

## Step 2: Evaluate Solution Options

### Option A: Vertical Scaling (Baseline / Minimal Risk)

**Approach:** Upgrade to larger database server (bigger CPU, more RAM, faster disk).

**Complexity:** Low

- No code changes
- No architectural decisions
- Proven operational model

**Cost:** ~$500–2000/month (larger managed DB instance)

**Time-to-value:** 2 weeks (provisioning + testing + deployment)

**Reliability:** Immediate improvement; proven approach

**Operational burden:** Minimal (managed service handles upgrades)

**Scalability ceiling:** ~5–10x before hitting the limit again

**Cons:**

- Single point of failure (single server still)
- Cache behavior unchanged (working set must fit in memory)
- At 6x traffic, must revisit (not a long-term solution)

---

### Option B: Read Replicas + Caching (Moderate Risk)

**Approach:**

1. Add read-only database replica(s)
2. Implement query routing (reads → replica, writes → primary)
3. Add caching layer (Redis) for frequently accessed data

**Complexity:** Medium

- Routing logic (queries to replica or cache)
- Replica lag handling (eventual consistency)
- Cache coherency (invalidate on writes)
- Small schema changes may be needed

**Cost:** ~$2000–3000/month (replicas + managed cache)

**Time-to-value:** 4 weeks

- Week 1: Set up replicas + cache infrastructure
- Week 2: Application changes for routing
- Week 3: Testing and chaos scenarios
- Week 4: Canary deployment

**Reliability:** Replica lag introduces eventual consistency (1–5s typical)

**Operational burden:** Moderate

- Monitor replica lag (alert if diverges)
- Cache invalidation logic (can be error-prone)
- Plan for replica failure scenarios

**Scalability ceiling:** ~15–20x (load-balanced across replicas + cache hits)

**Cons:**

- Team needs to understand replication and caching (knowledge gap)
- Replica lag is a constraint for some operations
- Still hitting single primary bottleneck for writes

---

### Option C: Service Decomposition (High Risk / Best Long-term)

**Approach:**

1. Extract user/identity service → separate database
2. Keep transaction service on current database
3. Async communication between services (queues or events)
4. Scale each service independently

**Complexity:** High

- Requires significant refactoring
- Distributed tracing, monitoring
- Cross-service consistency challenges
- Deployment complexity (N services vs. 1)

**Cost:** ~$3000–5000/month (additional managed services, queues, monitoring)

**Time-to-value:** 12–16 weeks

- Phase 1 (4 weeks): User service extraction
- Phase 2 (4 weeks): Async patterns implementation
- Phase 3 (4 weeks): Testing and monitoring
- Phase 4 (2 weeks): Canary rollout

**Reliability:** Higher operational surface (more components to fail)

**Operational burden:** High

- Service-to-service communication monitoring
- Distributed tracing setup
- Handling cross-service failures (cascade, retry logic)
- Deployment orchestration

**Scalability ceiling:** 100x+ (horizontal scaling at service level)

**Cons:**

- Team needs microservices expertise (not guaranteed with 5 engineers)
- Long implementation timeline (12+ weeks)
- More failure modes to debug / test

---

## Step 3: Comparison Table

| Dimension             | Option A (Vertical) | Option B (Replicas+Cache)   | Option C (Microservices)   |
| --------------------- | ------------------- | --------------------------- | -------------------------- |
| Complexity            | Low                 | Medium                      | High                       |
| Cost                  | $500–2k/mo          | $2–3k/mo                    | $3–5k/mo                   |
| Time-to-value         | 2 weeks             | 4 weeks                     | 12–16 weeks                |
| Scalability (3x goal) | ✅ Easy             | ✅ Medium (replicas needed) | ✅ Designed for it         |
| Scalability (6x+)     | ⚠️ Needs revisit    | ✅ ~20x ceiling             | ✅ 100x+ potential         |
| Operational burden    | Low                 | Medium                      | High                       |
| Team learning curve   | None                | Medium (replication, cache) | High (distributed systems) |
| Immediate to 3x       | ✅ Yes (weeks)      | ✅ Yes (weeks)              | ❌ No (months)             |
| Production-proven     | ✅ Yes              | ✅ Yes                      | ⚠️ Team unproven           |
| Risk of failure       | Low                 | Medium                      | High                       |

---

## Step 4: Decision Matrix

**Scoring:** 1–5 scale (1 = worst, 5 = best) weighted by priority

| Criterion (weight)          | Priority | Option A         | Option B         | Option C         |
| --------------------------- | -------- | ---------------- | ---------------- | ---------------- |
| Solves 3x scaling (20%)     | Critical | 5 (2x weight)    | 5 (2x weight)    | 5 (2x weight)    |
| Operational risk (25%)      | Critical | 5 (1.25x weight) | 3 (1.25x weight) | 1 (1.25x weight) |
| Team capacity (20%)         | High     | 5 (1x weight)    | 3 (1x weight)    | 2 (1x weight)    |
| Time-to-value (15%)         | High     | 5 (1x weight)    | 4 (1x weight)    | 2 (1x weight)    |
| Long-term scalability (20%) | High     | 2 (1x weight)    | 4 (1x weight)    | 5 (1x weight)    |
| **TOTAL SCORE**             | —        | **4.15**         | **3.75**         | **2.65**         |

---

## Step 5: Selected Option and Justification

**Selected: Option B (Read Replicas + Caching)**

### **Justification:**

1. **Meets immediate 3x goal** within reasonable timeline (4 weeks vs. 2 for vertical)
2. **Low-medium operational complexity** — team can manage with targeted training; not as risky as microservices for a 5-person team
3. **Proven pattern** — replicas + caching is industry-standard; lower failure risk
4. **Pragmatic middle ground** — balances speed-to-market with long-term flexibility

### **Trade-offs we accept:**

- Eventual consistency (1–5s); acceptable because most queries don't need strict consistency
- Replica monitoring overhead; worth it for 3x scale capability
- Eventually need to revisit after 5–10x growth; acceptable (not today's problem)

### **Trade-offs we reject:**

- Option A: Too short-lived; revisiting within 1–2 years is costly
- Option C: Too risky for a 5-person team without microservices experience; timeline too long for immediate need

### **Why not Option C (Microservices)?**

Microservices are powerful but:

- **Team risk:** 5 engineers + distributed systems complexity = likely to overshoot
- **Timeline:** 12+ weeks doesn't meet the 3x growth timeline
- **Operational surface:** More services = more on-call burden (team already stretched)
- **Better timing:** After 5–10x growth, revisit decomposition when team can absorb it

**Recommendation:** Plan Option B now; make decomposition decision in 12 months when team size/capability increases.

---

## Step 6: Implementation Plan

### Phase 1: Infrastructure and Setup (2 weeks)

**Step 1.1: Set up read replica**

- Provision read-only database replica (same instance size as primary)
- Configure replication (auto-backup + streaming)
- Acceptance criteria: Replica lag < 100ms under normal load

**Step 1.2: Set up caching infrastructure**

- Provision managed Redis (medium instance)
- Configure persistence and failover
- Acceptance criteria: Cache availability SLA >= 99.9%

**Step 1.3: Establish monitoring baseline**

- Metrics: Replica lag, cache hit ratio, query latency, CPU usage
- Acceptance criteria: All metrics visible in dashboard

---

### Phase 2: Application Changes (2 weeks)

**Step 2.1: Implement query routing**

- Code: Add logic to route SELECT queries to replica, UPDATE/DELETE/INSERT to primary
- Acceptance criteria: No performance regression on primary writes

**Step 2.2: Add caching layer**

- Code: Cache-aside pattern for frequent queries (likely invoices, user profiles)
- Acceptance criteria: Cache hit ratio > 70% on replay traffic

**Step 2.3: Handle replica lag explicitly**

- Code: For operations requiring fresh data, bypass cache/replica and hit primary
- Acceptance criteria: Consistency tests show no stale data on critical paths

---

### Phase 3: Testing and Validation (1.5 weeks)

**Step 3.1: Unit and integration tests**

- Test routing logic (correct endpoint for each query type)
- Test cache behavior (hit, miss, invalidation)
- Test replica lag handling
- Acceptance criteria: 90%+ test pass rate

**Step 3.2: Chaos testing**

- Replica fails → reads fall back to primary
- Cache fails → queries fall back to replica
- Primary slow → reads use replica as escape hatch
- Acceptance criteria: All scenarios handled gracefully

**Step 3.3: Load testing**

- Simulate 3x current load
- Measure: latency (p50, p95, p99), error rate, CPU usage
- Acceptance criteria:
  - p99 latency < 100ms (current baseline maintained)
  - Error rate < 0.1%
  - CPU usage on primary < 70%

---

### Phase 4: Canary Deployment (0.5 weeks)

**Step 4.1: Canary rollout**

- Enable read-replica queries on 10% traffic (2 hours)
- Monitor for errors and latency
- Expand to 50% (2 hours)
- Expand to 100% (if metrics are good)

**Step 4.2: Rollback plan**

- Feature flag to disable replica routing (instant)
- Instant fallback to single-primary model
- Estimated rollback time: < 5 minutes

---

## Step 7: Validation Evidence

| Phase  | Check                     | Status | Evidence                |
| ------ | ------------------------- | ------ | ----------------------- |
| Setup  | Replica replication lag   | TBD    | Ops monitoring          |
| Setup  | Cache availability SLA    | TBD    | Infrastructure test     |
| Code   | Query routing logic       | TBD    | Unit + integration test |
| Code   | Cache hit ratio > 70%     | TBD    | Load test metrics       |
| Code   | Replica lag handling      | TBD    | Integration test        |
| Chaos  | Replica failure handling  | TBD    | Chaos test report       |
| Chaos  | Cache failure handling    | TBD    | Chaos test report       |
| Load   | p99 latency < 100ms at 3x | TBD    | Load test report        |
| Load   | Error rate < 0.1%         | TBD    | Load test report        |
| Canary | 10% canary, no errors     | TBD    | Production metrics      |
| Canary | 100% deployment, stable   | TBD    | 24-hour monitoring      |

---

## Step 8: Risks and Mitigations

| Risk                                      | Severity | Impact                                          | Mitigation                                             | Owner    |
| ----------------------------------------- | -------- | ----------------------------------------------- | ------------------------------------------------------ | -------- |
| Replica lag causes stale reads            | Medium   | Business logic errors if used on critical paths | Explicit bypass for fresh reads; tests verify          | Eng      |
| Cache invalidation bugs                   | Medium   | Incorrect data served; hard to debug            | Unit tests for all invalidation paths; monitoring      | Eng      |
| Team learning curve (replication/caching) | Low      | Implementation slower than estimated            | Training session, documentation, pair up with expert   | Eng lead |
| Operational monitoring blind spots        | Low      | Miss issues until escalated                     | Build observability upfront; runbook for common issues | Ops      |

---

## Step 9: Confidence

**Level: MEDIUM-HIGH**

**Rationale:**

- ✅ Read replicas + caching are proven patterns
- ✅ 4-week timeline is realistic with a focused 5-person team
- ✅ Risk is manageable (chaos tests + rollback flag)
- ⚠️ Team hasn't done distributed reads before (minor learning curve)
- ⚠️ Actual 3x traffic behavior unknown (could expose unforeseen bottlenecks)

**What would increase confidence:**

- Confirmed that read/write ratio favors replicas (measure current ratio first)
- Load test replica + cache behavior at 3x under actual workload

**What would decrease confidence:**

- If 50%+ of queries require fresh reads (caching effectiveness drops)
- If team has zero prior experience with replicas

---

## Next Steps (Prioritized)

1. **[This week] Measure current read/write ratio and query patterns** — understand if replicas are effective — **Owner: Eng lead** — **Est: 1 day** — **Blocks: Phase 1 decisions**
2. **[This week] Prototype replica setup in staging** — verify lag and failover behavior — **Owner: DevOps** — **Est: 2 days** — **Blocks: Phase 1 go-live**
3. **[Week 1–2] Execute Phase 1 (infrastructure)** — replicas + cache ready — **Owner: DevOps + Eng** — **Est: 2 weeks**
4. **[Week 2–4] Execute Phase 2–3 (code + tests)** — application changes + validation — **Owner: Eng + QA** — **Est: 3 weeks**
5. **[Week 4] Execute Phase 4 (canary)** — production rollout — **Owner: Eng + DevOps + Ops** — **Est: 1 week**
6. **[Ongoing] Monitor 3x traffic readiness** — monthly capacity planning — **Owner: Ops + Eng** — **Est: 1 hour/week**

**Timeline to 3x-ready: 4–5 weeks.**

---

## Summary

**Strategy: Read Replicas + Caching**

- Meets 3x scaling goal with moderate risk
- Keeps operational complexity manageable for a 5-person team
- Fast timeline (4 weeks) vs. microservices (12+ weeks)
- Plan for next evolution (microservices) in 12 months at 5–10x growth
