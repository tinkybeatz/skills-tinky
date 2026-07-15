# Standard: Architecture Decision Framework

- **Status:** Active
- **Version:** 1.0.0
- **Owner:** Engineering Lead
- **Approvers:** Tech Lead
- **Effective date:** 2026-04-30
- **Last review date:** 2026-04-30

## Scope

Every structuring architecture choice on a project: pattern choice (monolith / microservices / serverless / hybrid), major stack choice, large refactor, service extraction, legacy migration.

This document provides the **normative criteria** for defending a choice to a client CTO. The `MUST` rules are not opinions — they are sourced conclusions (Fowler, Newman, Richardson, ThoughtWorks Radar, AWS).

---

## Reference position (sourced)

These quotes frame all the decisions below:

- **Fowler — MonolithFirst**: *"Almost all the successful microservice stories have started with a monolith that got too big and was broken up, and almost all the cases where a system was built as a microservice system from scratch has ended up in serious trouble."* `[SRC-001]`
- **ThoughtWorks Radar**: microservices remain in **Trial**, never **Adopt** — *"the costs and downsides of the approach and the level of organizational maturity needed to execute on the approach are the reason that microservices will quite likely never move into Adopt."* `[SRC-002]`
- **Newman 2nd ed. (2021)**: a dedicated chapter, *"The Monolith Is Rarely the Enemy"*. `[SRC-003]`
- **DHH (2025)**: *"the majestic monolith remains undefeated for the vast majority of web apps. Replacing method calls with network calls makes everything harder, slower, and more brittle. It should be the absolute last resort."* `[SRC-004]`
- **Amazon Prime Video (2023)**: moved from microservices back to a monolith with **-90% cost**. `[SRC-005]`

**Derived position**: default = modular monolith. Any deviation requires a justified ADR.

---

## Decision Matrix

| Criterion | Modular Monolith (default) | Microservices | Serverless / FaaS | Hybrid |
|---|---|---|---|---|
| **Team size** | 1-30 devs, 1-5 teams | >30 devs with truly independent teams | Any size for targeted workloads | 5-50 devs |
| **Required ops maturity** | Low/medium OK | **High** (mature CI/CD, observability, on-call rotation) | Low OK (managed) | Medium |
| **Load / RPS** | Up to thousands of RPS on a scaled instance | Justified for **differential** scaling per domain | Bursty, < 50% duty cycle | Steady core + spiky periphery |
| **Cost profile** | Predictable, low opex | High ("microservice premium") | High $/req above 50k sustained req/day | Optimized per workload |
| **Time to market** | Fast (MVP in weeks) | Slow (CI/obs/deploy setup) | Very fast for simple cases | Medium |
| **Compliance forcing isolation** | OK with partitioned schema | Justified (PCI scope reduction, HIPAA) | OK if provider is compliant | Case by case |
| **Domain stability** | Boundaries can move without drama | **Boundaries must be stable** | Stable stateless functions | Mixed |

---

## Normative rules

### ARC-DEC-01 — Default = Modular Monolith

**Requirement:** Every new project MUST start as a **modular monolith** unless a written justification to the contrary exists in an initial ADR. The default is never "microservices ready" nor "full serverless". `[SRC-001]` `[SRC-003]` `[SRC-004]`

**Rationale:** Fowler, Newman 2nd ed., and DHH converge. ThoughtWorks Radar has kept microservices in Trial for 10 years. The operational cost of microservices ("microservice premium") is underestimated by default.

**Enforcement:** initial architecture review by Tech Lead; absence of a deviation ADR = default applied.

### ARC-DEC-02 — Microservices: 5 simultaneous "pro" signals required

**Requirement:** Choosing microservices MUST require the following **5 simultaneous "pro" signals**, documented in an ADR:

1. Truly autonomous teams, with independent deploy needed (Conway).
2. Domains with **measured** differential scaling (one sub-domain 100x the other).
3. Mature ops: per-service CI/CD, OTel observability in place, existing on-call rotation.
4. Stable, proven boundaries (ideally post-monolith).
5. Compliance forcing isolation (PCI cardholder data env, HIPAA).

If **even one** signal is missing → modular monolith. `[SRC-001]` `[SRC-003]`

**Rationale:** without these 5 signals, the project ends up a distributed monolith — the worst of both worlds.

**Enforcement:** ADR review by Tech Lead, explicit validation of the 5 signals.

**Exceptions:** none. If the ADR cannot document the 5 signals, the standard mandates a modular monolith.

### ARC-DEC-03 — Microservices anti-signals = automatic rejection

**Requirement:** Microservices MUST NOT be chosen if **even one** of the following anti-signals is present:

- Team < 10 devs.
- No dedicated ops platform (CI/CD, observability, on-call).
- Unproven domain boundaries (greenfield product).
- Need for cross-service transactions identified at design time.
- E2E testing required to ship (= distributed monolith).
- Observed lockstep deployments (services that always deploy together).

`[SRC-006]`

**Rationale:** these signals indicate a premature or unsuitable split. Cargo-cult microservices = guaranteed failure for an agency.

**Enforcement:** architecture review + regular audit (reversal ADR if signals appear post-decision).

### ARC-DEC-04 — Serverless: workload-shape only

**Requirement:** Serverless / FaaS MUST be chosen ONLY if:
- Bursty / event-driven workload (webhooks, cron, occasional ETL, stream processing).
- Duty cycle < 10%.
- Statelessness is possible.
- Cold start is tolerable (200-500ms acceptable, or Edge V8 isolates < 50ms).

Serverless MUST NOT be chosen for:
- Steady-state workload > 50% duty cycle (Lambda becomes ~78x more expensive than Fargate at a sustained 400 RPS).
- Strict latency < 50ms required.
- Long-running > 15 min (Lambda limit) or > 5 min (Workers/Edge).
- Unacceptable vendor lock-in for the client.

`[SRC-007]`

**Rationale:** per-ms billing = cost explodes under sustained load. Cold starts break p99 SLA on heavy runtimes. API-specific vendor lock-in = costly migration.

**Enforcement:** initial ADR with workload analysis (estimated duty cycle, target latency).

### ARC-DEC-05 — Hybrid pattern acceptable as default

**Requirement:** The **modular monolith + async workers** pattern (H1) SHOULD be accepted as a healthy default for the majority of client products (~80% of cases). `[SRC-008]`

**Rationale:** a stable, synchronous business core (monolith) + event-driven or batch periphery (BullMQ / Inngest / Temporal workers) covers most cases (AI inference, ETL, doc generation, webhooks).

**Enforcement:** a "default architecture" ADR at project start.

### ARC-DEC-06 — Inverse Conway maneuver

**Requirement:** The split into services SHOULD align with the client's **future** target organization (at 12-24 months), not the current organization if it is transitory. `[SRC-009]`

**Rationale:** Conway's Law — the delivered architecture reflects the organization. Aligning to the current org if it will change = a guaranteed refactor.

**Enforcement:** challenge the proposed client split during pre-project.

### ARC-DEC-07 — Vendor lock-in made explicit in an ADR

**Requirement:** Any technology choice that would cost **>2 person-months** to migrate (proprietary managed DB, API-specific FaaS, Step Functions, DynamoDB single-table, etc.) MUST be documented in an ADR signed by the client. `[SRC-010]`

**Rationale:** a client surprised by migration cost at the end of an engagement = a broken relationship. The standard mandates upfront transparency.

**Enforcement:** ADR review by Tech Lead + client signature required for going to prod.

**Exceptions:** none on any significant vendor lock-in.

### ARC-DEC-08 — Reversibility preferred under uncertainty

**Requirement:** When domain uncertainty is high (greenfield, MVP, product validation), reversible choices SHOULD be preferred over irreversible ones. **Module** boundaries (cheap to move) > **service** boundaries (nearly irreversible). `[SRC-001]`

**Rationale:** Newman: *"any refactoring of functionality between services is much harder than it is in a monolith"*. Reversing a module boundary = `git mv` + linter update. Reversing a service boundary = data migration + deploy + downtime.

**Enforcement:** architecture review + a systematic question in the ADR: "what happens if this boundary has to move in 6 months?".

---

## Agency-specific pitfalls

### P1 — Cargo-cult microservices

The client says "we want microservices, it's modern." Standard response: explicitly challenge with the decision matrix, show the opex cost (a quantified estimate), propose a modular monolith as a defensible alternative.

### P2 — Distributed monolith

Symptoms (detect by the 3rd release): services that deploy together, e2e tests mandatory to ship, synchronous cross-service chattiness, deploy A blocks deploy B. → a merge ADR.

### P3 — Silent serverless lock-in

Lambda + DynamoDB + Step Functions + EventBridge = enormous migration cost. Make it explicit in the initial ADR that this choice is non-portable, and get it signed.

### P4 — Stack imposed by history

The client has an internal team in .NET / Java / PHP. Forcing Node / Go = failure at handover. Default: adapt the stack to the client, keep the principles (`principles.md`) invariant.

---

## Sources

- `[SRC-001]` Fowler — MonolithFirst: https://martinfowler.com/bliki/MonolithFirst.html
- `[SRC-002]` ThoughtWorks Radar — Microservices: https://www.thoughtworks.com/radar/techniques/microservices
- `[SRC-003]` Newman — Building Microservices 2nd ed (2021): https://samnewman.io/books/building_microservices_2nd_edition/
- `[SRC-004]` DHH (X 2025) — Majestic Monolith remains undefeated: https://x.com/dhh/status/1981342407129235683
- `[SRC-005]` Amazon Prime Video — Scaling and reducing cost by 90%: https://www.primevideotech.com/video-streaming/scaling-up-the-prime-video-audio-video-monitoring-service-and-reducing-costs-by-90
- `[SRC-006]` Richardson — Services + E2E testing = monolith: https://microservices.io/post/architecture/2024/03/29/services-with-end-to-end-testing-equals-monolith.html
- `[SRC-007]` TechPlained — Serverless vs Containers (2026): https://www.techplained.com/serverless-vs-containers
- `[SRC-008]` Richardson — Modular monolith patterns for fast flow (2024): https://microservices.io/post/architecture/2024/09/09/modular-monolith-patterns-for-fast-flow.html
- `[SRC-009]` Fowler — Conway's Law: https://martinfowler.com/bliki/ConwaysLaw.html
- `[SRC-010]` MDPI 2024 — Cloud Vendor Lock-In Prediction Framework: https://www.mdpi.com/2227-7390/12/3/387

## Change log

| Version | Date | Author | Description |
|---|---|---|---|
| 1.0.0 | 2026-04-30 | Team | Initial — from Deep-mode research + sourced reference position Fowler/Newman/Richardson/ThoughtWorks/DHH. |
