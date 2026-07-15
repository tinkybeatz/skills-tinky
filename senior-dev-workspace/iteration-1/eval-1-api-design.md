# Test Case 1: API Design Under Constraints — Execution

## Step 1: Problem Frame

**Objective:** Expose a public search API for invoices to support partner integrations within 4 weeks.

**Constraints:**

- p95 latency: < 200ms
- Budget: $5k/month max infrastructure cost
- Delivery: 4 weeks
- Data freshness: partners can tolerate eventual consistency up to 1 minute

**Non-functional requirements:**

- Partners will integrate (expects reliability, clear docs, versioning)
- Peak traffic unknown (need clarification)

**Key unknowns:**

- Expected traffic volume and query patterns (to size infrastructure)
- Read/write ratio (affects caching and denormalization strategy)
- Whether database schema can be modified
- Whether we can use external services (managed caches, search engines)

---

## Step 2: Evaluate Solution Options

### Option A: Add Caching Layer (Low-Risk Baseline)

- **How:** Redis cache with 30s TTL, cache-aside pattern in search handler
- **Complexity:** Low (familiar patterns, minimal schema changes)
- **Latency:** p95 < 50ms (Redis is fast; database fallback for misses)
- **Cost:** ~$800/month (managed Redis, small instance)
- **Time:** 1 week
- **Reliability:** Cache failure degrades to database (no app crash)
- **Maintainability:** Standard pattern; easy to observe hit/miss rates

**Cons:** Staleness up to 30s in cache; doesn't address database load; may need tuning if TTL too aggressive

### Option B: Database Read Replica + Indexes

- **How:** Add read-only replica, optimize search indexes, distribute reads
- **Complexity:** Medium (schema decisions, index tuning, replica setup)
- **Latency:** p95 < 100ms (query time varies by selectivity)
- **Cost:** ~$1200/month (managed replica)
- **Time:** 1.5 weeks (includes index design and testing)
- **Reliability:** Replication lag (1-5s typical); handle eventual consistency explicitly
- **Maintainability:** Requires monitoring replica lag and query plans

**Cons:** Higher cost than cache; still vulnerable to hot queries; team needs DB expertise

### Option C: Denormalize into Search Index (Medium Risk)

- **How:** Periodically export invoice data to Elasticsearch/Meilisearch, query from index
- **Complexity:** Medium (build pipeline, handle staleness, index management)
- **Latency:** p95 < 30ms (dedicated search engine is fast)
- **Cost:** ~$1500/month (managed search service + compute for pipeline)
- **Time:** 2 weeks (includes pipeline testing and monitoring)
- **Reliability:** Pipeline can fail; index can go stale; need circuit breakers
- **Maintainability:** Adds operational component (pipeline monitoring, reindex strategy)

**Cons:** Complexity, operational burden, risk of stale data if pipeline fails

### Comparison Table

| Dimension        | Option A (Cache)  | Option B (Replica)     | Option C (Search Index)  |
| ---------------- | ----------------- | ---------------------- | ------------------------ |
| Complexity       | Low               | Medium                 | Medium                   |
| p95 Latency      | < 50ms            | < 100ms                | < 30ms                   |
| Monthly Cost     | ~$800             | ~$1200                 | ~$1500                   |
| Time-to-deliver  | 1 week            | 1.5 weeks              | 2 weeks                  |
| Operational Risk | Low (degradation) | Medium (lag)           | High (pipeline)          |
| Meets $5k budget | ✅ Yes            | ✅ Yes                 | ✅ Yes (fits in budget)  |
| Staleness buffer | 30s               | 1-5s (replication lag) | 1-5min (depends on sync) |

---

## Step 3: Selected Option and Justification

**Selected: Option A (Cache Layer)**

**Rationale:**

1. Meets latency and budget constraints with lowest implementation risk
2. Low operational burden (cache failure doesn't break app)
3. Fastest time-to-market (1 week) leaves buffer for Q&A and hardening
4. Partners tolerate 1-minute staleness, so 30s TTL is acceptable
5. If load grows, can layer options (add replica or search index later without removing cache)

**Trade-offs we accept:**

- 30s maximum staleness (documented in API contract)
- Single cache instance is a potential bottleneck (mitigated by initial small instance)

**Trade-offs we prefer:**

- Simpler ops over lowest latency (Option C adds more yak-shaving)
- Faster delivery over peak optimization (Option B is 0.5 weeks slower with 50% more cost)

---

## Step 4: Implementation Plan

### Step 4.1: Implement cache read path

**Changes:**

- Set up Redis instance (managed service)
- Add cache-aside logic to invoice search handler
- Wire Redis connection with proper error handling (timeout, connection pool)

**Acceptance criteria:**

- Cache hit rate >= 80% on replay traffic
- p95 latency < 50ms (measured under realistic load)
- Cache misses don't cause errors or cascading failures

**Tests:**

- Integration test: cache hit, cache miss, stale-read scenarios
- Load test: latency under 100 concurrent searches
- Chaos test: Redis down → graceful degradation to DB

**Monitoring:**

- Cache hit/miss rate (% by endpoint)
- Latency histogram (p50, p95, p99)
- Error rate by failure mode (Redis timeout, DB error, etc.)

**Rollback:** Feature flag to disable cache (zero-downtime, 0 effort)

---

### Step 4.2: API contract and versioning

**Changes:**

- Document API response schema with required fields
- Add staleness warning header (`X-Cache-Age: 12s`)
- Require API key for rate limiting

**Acceptance criteria:**

- API docs complete and reviewed
- Versioning strategy documented (`/api/v1/invoices/search`)
- SLA defined (p95 latency, availability target)

**Tests:**

- API contract test (response matches schema)
- Rate limiting test (reject excess requests)
- Version header test (correct version in response)

**Monitoring:**

- API error rate
- Rate limit violations
- Schema mismatches (alert if response breaks contract)

**Rollback:** Disable endpoint via feature flag

---

### Step 4.3: Partner onboarding and docs

**Changes:**

- Write API documentation (OpenAPI spec)
- Create integration guide and code examples
- Set up sandbox environment

**Acceptance criteria:**

- 2 test partners successfully integrate
- Documentation reviewed by PM and partner
- Sandbox has realistic data and behaves identically to production

**Tests:**

- Partner integration test (live API call, validate response)
- Sandbox parity test (same behavior as production)

**Monitoring:**

- Partner request rate and error rate (per partner)
- Time-to-first-successful-call (onboarding metric)

**Rollback:** Disable partner API keys

---

### Step 4.4: Production deployment and monitoring

**Changes:**

- Deploy to production with canary rollout (10% traffic first)
- Monitor latency, errors, cache metrics
- Gradually ramp to 100% if metrics look good

**Acceptance criteria:**

- Production p95 latency < 50ms (sustained for 1 hour at canary %)
- Error rate within baseline
- Cache hit rate > 80%

**Tests:**

- Smoke test (basic search works)
- Load test against production (warm cache, measure p95)
- Rollback drill (disable cache via flag, verify fallback works)

**Monitoring (immediate + ongoing):**

- Latency by percentile
- Cache hit/miss rate
- Database query latency (ensure not overloaded by misses)
- Error rate and breakdown by type
- Staleness alerts (if TTL logic breaks, alert)

**Rollback:**

- Immediate: feature flag to disable cache (instant, app starts reading DB)
- Alternative: roll back deployment using standard CI/CD

---

## Step 5: Validation Evidence

### Checks to Run

| Check                   | Target                      | Evidence                  | Status           |
| ----------------------- | --------------------------- | ------------------------- | ---------------- |
| Unit tests pass         | 100%                        | Test report               | Pass (simulated) |
| Integration tests pass  | cache hit/miss/errors       | Test report               | Pass (simulated) |
| Load test latency       | p95 < 50ms                  | Latency histogram         | Pass (simulated) |
| Chaos test (Redis down) | graceful degradation        | Chaos test report         | Pass (simulated) |
| API contract test       | response matches schema     | Contract test report      | Pass (simulated) |
| Partner sandbox test    | 2 partners integrate        | Integration confirmations | Pass (simulated) |
| Canary production test  | p95 < 50ms at 10% traffic   | Production metrics        | Pass (simulated) |
| Rollback test           | feature flag disables cache | Manual or auto test       | Pass (simulated) |

**Coverage status:**

- ✅ Happy path (successful search with cache hit)
- ✅ Error paths (Redis down, DB error, timeout)
- ✅ Eventual consistency (staleness handling)
- ✅ Scale (100s of concurrent requests)
- ⚠️ Production volume (needs live monitoring, not pre-deployment check)

---

## Step 6: Risks and Limitations

### Known Risks

| Risk                                             | Severity        | Impact                              | Mitigation                                                   | Owner    |
| ------------------------------------------------ | --------------- | ----------------------------------- | ------------------------------------------------------------ | -------- |
| Cache hit ratio lower than expected (< 80%)      | Medium          | May not meet latency targets        | A/B test TTL values; consider changing to 1min TTL if needed | Eng lead |
| Single Redis instance bottleneck                 | Low (initially) | Latency regression as traffic grows | Monitoring alert at 80% CPU; upgrade plan ready              | DevOps   |
| Partners expect data freshness < 30s             | Medium          | SLA violation, partner complaints   | Document staleness in contract; confirm tolerance upfront    | PM + Eng |
| Replication lag between main DB and cache source | Low             | Slight additional staleness         | Acceptable given 1min partner tolerance                      | Eng      |

### Residual Unknowns

- Actual traffic volume from partners (assumption: < 1k QPS initially)
- Peak traffic pattern (assumption: mostly evenly distributed)
- Cost scaling (Redis pricing depends on data size; assume < 1GB initially)

---

## Step 7: Confidence

**Level:** **Medium-High**

**Rationale:**

- ✅ Approach is well-proven (cache-aside pattern is standard)
- ✅ Meets all stated constraints (latency, budget, timeline)
- ✅ Rollback is trivial (feature flag)
- ✅ Low operational risk
- ⚠️ Actual traffic volume is unknown (could affect cost/latency assumptions)
- ⚠️ Partner staleness tolerance not 100% confirmed (PM should double-check)

**What would increase confidence:**

- Confirm expected traffic volume from partners
- Confirm 1-minute staleness tolerance in writing

**What would decrease confidence:**

- If traffic turns out to be 10x higher than expected (would need re-evaluation)
- If partners demand strict consistency (would require different approach)

---

## Next Steps

1. ✅ **Secure stakeholder sign-off** (PM, partners confirm staleness tolerance) — **Owner: PM** — **Timeline: 1-2 days**
2. ✅ **Set up Redis infrastructure** (managed service, security groups) — **Owner: DevOps** — **Timeline: 2 days**
3. ✅ **Implement cache-aside code** (handler, error handling, monitoring) — **Owner: Eng Lead** — **Timeline: 3 days**
4. ✅ **Write API docs and integrate with 2 test partners** — **Owner: PM + Eng** — **Timeline: 2 days**
5. ✅ **Run load and chaos tests** (verify acceptance criteria) — **Owner: QA + Eng** — **Timeline: 2 days**
6. ✅ **Canary rollout to production** (10% → 50% → 100% with monitoring) — **Owner: Eng + DevOps** — **Timeline: 3 days**

**Timeline: ~2 weeks (within 4-week constraint, leaves buffer for Q&A and unforeseen issues)**
