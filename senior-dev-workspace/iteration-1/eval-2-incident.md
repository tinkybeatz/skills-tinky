# Test Case 2: Production Incident Remediation — Execution

## Step 1: Problem Frame

**Incident Summary:**

- Service: Checkout (payment processing)
- Symptom: Request timeouts during peak traffic (7 PM window)
- Frequency: 3 times in 2 weeks
- Duration: 10-15 minutes per incident
- Root cause identified: Database connection pool exhaustion
- Tolerance: **Zero tolerance for checkout failures**

**Scope:**

- Immediate: Resolve current instability
- Medium-term: Durable fix addressing root cause

**Constraints:**

- Zero downtime for production
- Minimal time to containment (incidents are ongoing risk)
- Must support peak traffic without intervention

**Current options being considered:**

1. Rollback latest changes
2. Quick fix to connection pool size

**Key unknowns:**

- Why did connection pool exhaust now? (Recent code change, traffic spike, resource contention?)
- What was the pool size before, and what changed?
- Are all services affected or just checkout?
- Is the pool misconfigured or is it a code leak (connections not released)?

---

## Step 2: Root Cause Investigation & Hypothesis Ranking

### Hypothesis 1: Connection Leak in Recent Code (High Confidence)

**Evidence:**

- Timing coincides with recent code review branch (checkout refactor)
- New retry logic could hold connections longer
- "Connection pool exhaustion" is typically a leak, not traffic spike

**Test:** Check if connections are being released properly after retries. Look at connection lifetime metrics or code review for explicit `.close()` calls.

**Mitigation:** If confirmed, rollback is fast (1-2 min) and safe.

---

### Hypothesis 2: Legitimate Traffic Spike Without Capacity

**Evidence:**

- Occurs at 7 PM (evening peak)
- No recent traffic forecasting data

**Test:** Compare connection count at incident time vs. baseline. If 5x higher, examine traffic pattern change.

**Mitigation:** Increase pool size as quick fix; plan capacity analysis for long-term.

---

### Hypothesis 3: Database Performance Regression (Medium Confidence)

**Evidence:**

- Slow queries hold connections longer
- Recent schema change or missing index could cause this

**Test:** Check database slow query log. Look for queries taking > 1s that didn't before.

**Mitigation:** Identify and optimize slow query; add index if needed.

---

### Ranking

1. **Hypothesis 1 (connection leak):** 65% confidence — most common cause; timing fits recent code
2. **Hypothesis 2 (traffic spike):** 20% confidence — possible but would happen on non-peak days too
3. **Hypothesis 3 (query perf):** 15% confidence — contributing factor but typically not sole cause

---

## Step 3: Containment Strategy Decision

**Decision: Investigate while applying immediate containment (not rollback immediately)**

**Rationale:**

- Rolling back loses recent feature work without knowing if it's the cause
- Increasing pool size buys time for investigation (low-risk, instant)
- If investigation confirms leak, rollback is straightforward
- If traffic spike, we learn that and rightsize for future

**Containment steps:**

1. Immediately increase connection pool size by 50% (e.g., 20 → 30 connections)
2. Deploy to production (5-10 min, no restart needed if using dynamic config)
3. Monitor for 24 hours; if incidents stop, escalate investigation; if they recur, proceed to rollback
4. In parallel, audit connection handling in recent code

---

## Step 4: Investigation Plan (Parallel)

### Immediate (next 1 hour)

1. **Pull production connection metrics:**
   - Current active connections at 7 PM incident time vs. baseline
   - Connection lifetime histogram (are connections stuck?)
   - Query duration at incident time

2. **Audit recent code changes:**
   - Review checkout refactor for connection handling
   - Look for `.close()`, `.release()`, or try-finally blocks
   - Check if retry logic properly cleans up connections

3. **Check database slow query log:**
   - Any queries > 1s during incident window?
   - Compare to baseline

### Follow-up (if pool increase doesn't fix it)

- Enable connection pool debug logging
- Trace a single request to see where it hangs
- If still uncertain: rollback and apply again, measure difference

---

## Step 5: Durable Fix Plan

### If Root Cause = Connection Leak

**Fix:**

- Ensure all connection usages are in try-finally or using-block (depending on language)
- Specific fix in retry logic: wrap retries in proper cleanup

**Validation:**

- Code review of connection handling
- Integration test that exercises retry logic and verifies connections are released
- Load test showing no connection creep under sustained retries

**Regression protection:**

- Add monitoring alert: "Active connections > 80% of pool size"
- Add test: "Repeated failed connections should not exhaust pool"

### If Root Cause = Traffic Spike

**Fix:**

- Increase pool size permanently (from 20 to 30–40 based on measured load)
- Understand traffic growth (is this expected? One-time? Recurring?)

**Validation:**

- Production load test under forecasted peak (2x current)
- Verify no connection exhaustion at peak

**Regression protection:**

- Capacity planning: map traffic growth to connection/database resource needs
- Add dashboard showing connection usage % trending over time

### If Root Cause = Query Performance

**Fix:**

- Identify slow query; either optimize or add index

**Validation:**

- Confirm query is now < 100ms
- Re-run production load test; latency should improve

**Regression protection:**

- Add slow query alert: "Queries > 1s should be exceptional"
- Regular query analysis (weekly slow query review)

---

## Step 6: Validation Strategy

### Immediate (Post-Containment Deployment)

| Check                                | Target                                 | How                               | Owner     |
| ------------------------------------ | -------------------------------------- | --------------------------------- | --------- |
| Pool increase deployed               | Production running with 30 connections | Verify via config check           | DevOps    |
| No errors from pool increase         | Same error rate as before              | Monitor app error rate for 1 hour | Eng + Ops |
| Connection count stable              | Active connections don't breach 80%    | Metrics dashboard                 | Ops       |
| Incident doesn't recur at 7 PM today | No timeout alerts                      | Alert manager, on-call review     | Ops       |

### Investigation Phase

| Check                 | Target                          | How                        | Owner    |
| --------------------- | ------------------------------- | -------------------------- | -------- |
| Root cause identified | Confirmed hypothesis            | Analysis report + evidence | Eng lead |
| Fix validated         | Code and DB changes pass checks | Perf test, code review     | Eng + QA |
| Regression test added | New test prevents this incident | Test suite updated         | QA       |
| Monitoring in place   | Alert fires if pattern recurs   | Alert config updated       | Ops      |

---

## Step 7: Risks and Mitigation

### Residual Risks

| Risk                                            | Severity | Impact                            | Mitigation                                                  | Owner    |
| ----------------------------------------------- | -------- | --------------------------------- | ----------------------------------------------------------- | -------- |
| Incident recurs after pool increase             | High     | More checkout failures            | Rollback button ready; investigation priority order defined | Eng lead |
| Fix is incomplete (leak persists, just delayed) | Medium   | Issue recurs at higher load soon  | Comprehensive code audit, not just quick fix                | Eng lead |
| Fleet-wide deployment of fix is slow            | Medium   | Downtime if all services affected | Use feature flag or gradual rollout                         | DevOps   |

---

## Step 8: Next Steps (Prioritized)

1. **[IMMEDIATE - 5 min] Deploy pool increase to production** — increase connections 20 → 30 — **Owner: DevOps** — **Blocks: incident stabilization**
2. **[PARALLEL - ongoing] Monitor for 24 hours** — watch incident recurrence — **Owner: On-call** — **Blocks: decision to escalate**
3. **[PARALLEL - 1 hour] Audit checkout refactor** — review connection handling in recent code — **Owner: Eng lead** — **Blocks: root cause ID**
4. **[By tomorrow] Root cause analysis complete** — hypothesis confirmed or ruled out — **Owner: Eng lead** — **Blocks: durable fix**
5. **[By end of sprint] Durable fix deployed + validated** — no incident recurrence for 1 week — **Owner: Eng + QA** — **Blocks: closure**
6. **[Ongoing] Capacity planning** — forecast connection needs for 2x traffic growth — **Owner: Eng + Ops** — **Blocks: future scaling**

---

## Confidence

**Level: Medium**

**Rationale:**

- ✅ Immediate containment is low-risk (can revert easily)
- ✅ Investigation plan is systematic (hypothesis ranking, tests defined)
- ⚠️ Root cause not yet confirmed (multiple hypotheses possible)
- ⚠️ Time pressure (each incident is business impact)

**What would increase confidence:**

- Swift confirmation of root cause (connection metrics + code audit)
- Historical data showing no similar incidents before recent change

**What would decrease confidence:**

- If root cause remains unknown after 24 hours
- If multiple services are affected (suggests systemic issue, not code leak)

---

## Decision Summary

**Immediate action:** Increase connection pool size 50% and monitor.
**Investigation:** Parallel search for root cause (connection leak most likely).
**Follow-up:** Either fix the leak or scale for traffic; regression protection mandatory in both cases.
**Rollback:** Always ready (feature flag or revert).
