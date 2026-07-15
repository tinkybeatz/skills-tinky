# Pre-deploy checklists by risk level

## Score 1-4 — Low risk (auto-approve)

No checklist needed. Deploy.

---

## Score 5-9 — Medium risk (light checklist, ~2 min)

- [ ] TypeScript compiles (`tsc --noEmit`)
- [ ] Tests pass (`vitest run` / `jest`)
- [ ] The diff contains no secrets (`.env`, credentials, API keys)
- [ ] Rollback plan identified (usually `git revert`)
- [ ] Existing monitoring will cover the change

---

## Score 10-15 — High risk (full checklist, ~5 min)

### Pre-deploy
- [ ] TypeScript compiles
- [ ] Tests pass (unit + integration)
- [ ] Review of the full diff (not just the modified files — the dependencies too)
- [ ] Rollback plan documented and tested in staging
- [ ] DB migration tested in staging with realistic volume
- [ ] No concurrent deployment (check the change schedule)
- [ ] Deployment during off-peak hours if possible
- [ ] Monitoring and alerts verified for the key metrics

### Cool-down (1h minimum between the end of review and deploy)
The cool-down is not bureaucracy — it is a cognitive circuit breaker. After spending time
preparing a deploy, confirmation bias ("everything's fine, I checked everything") is at its
peak. The cool-down creates a break that lets you come back with fresh eyes.

### Immediate post-deploy (T+1h)
- [ ] Manual smoke test on the affected flows
- [ ] Error rate stable (no spike)
- [ ] p95 latency stable
- [ ] Clean logs (no unexpected stack traces)

---

## Score 16-25 — Critical risk (full investigation)

### Pre-investigation
- [ ] All the items from score 10-15
- [ ] Explicitly list what could go wrong (failure modes)
- [ ] For each failure mode: what signal would detect it? in how much time?
- [ ] Plan B if the rollback does not work

### Progressive deploy strategy
- [ ] Feature flag or canary configured
- [ ] Phase 1: deployment to a single pod/instance
- [ ] Phase 2 (T+30min if OK): 50% of traffic
- [ ] Phase 3 (T+2h if OK): 100%
- [ ] Go/no-go criteria for each phase (quantitative metrics, not "looks OK")

### Communication
- [ ] Stakeholders notified (if applicable)
- [ ] Maintenance window communicated (if downtime is possible)
- [ ] Communication channel identified for incidents

### Post-deploy
- [ ] T+1h: metrics
- [ ] T+24h: trends
- [ ] T+7d: formal PIR
- [ ] Lessons fed back into the risk scoring (learning loop)

---

## ECAB Template — Emergency change (~1 min)

When the dev says "it's urgent, I have to deploy now":

```
## ECAB Express

**Why it's urgent:** [ongoing incident / security flaw / ...]
**What happens if we do NOT deploy now:** [concrete impact]
**Impact of the change:** [1-5]
**Rollback:** [how]
**Recommendation:** DEPLOY | HOLD

Note: retrospective mandatory within 48h.
```

The ECAB does not skip the assessment — it compresses it. Urgency is no excuse to skip thinking
about the rollback. Historically, emergency changes have the highest failure rate (ITIL data)
precisely because the assessment is rushed.
