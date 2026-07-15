# Standard: Pattern — Microservices

- **Status:** Active
- **Version:** 1.0.0
- **Owner:** Engineering Lead
- **Effective date:** 2026-04-30

## Scope

Every project that has adopted the **microservices** pattern AFTER validating `decision-framework.md` ARC-DEC-02 (5 simultaneous "pro" signals required).

⚠️ **Reminder**: microservices = **exception**, not default. If the project does not validate the 5 "pro" signals, fall back to `patterns/modular-monolith.md`.

## Core decisions

- **Platform**: ECS Fargate / Cloud Run below 10 services; K8s + Argo CD beyond (ARC-MS-12).
- **Messaging broker**: NATS JetStream by default; Kafka only for high-volume event streaming (ARC-MS-09).
- **Durable workflows**: Temporal or Inngest if needed.
- **Observability**: Grafana Cloud LGTM + OTel.

---

## Normative rules

### Service boundaries & DDD

### ARC-MS-01 — One service = one validated DDD bounded context

**Requirement:** Each service MUST correspond to a **DDD bounded context validated with the business** (established ubiquitous language). Pure technical splitting (by layer, by framework) MUST NOT be used. `[SRC-001]` `[SRC-002]`

**Rationale:** Newman: *"the strongest indicator of a service boundary is a bounded context"*. Technical splitting cuts across domains and prevents any refactor.

**Enforcement:** architecture review + an initial ADR documenting the bounded contexts.

### ARC-MS-02 — Right-sized services

**Requirement:** A service MUST be **replaceable in 2 weeks** by a team (Newman 2nd ed.). If two services always deploy together, they are one — they MUST be merged. `[SRC-002]`

**Rationale:** services too fine-grained (nano-services) = latency dominated by the network, ops cost > value. Services too large = back to the monolith.

**Enforcement:** deployment-frequency audit per service; detection of lockstep deployments.

### ARC-MS-03 — Strangler Fig for migration from a monolith

**Requirement:** Any extraction from a monolith MUST follow the **Strangler Fig** + **Branch by Abstraction** pattern, never a big bang. The opening ticket MUST include the legacy **kill date**. `[SRC-003]`

**Rationale:** without Strangler Fig + kill date, the legacy and the new coexist forever = the worst of both worlds.

**Enforcement:** initial ADR + kill date tracking.

### Data consistency

### ARC-MS-04 — Strict database-per-service

**Requirement:** Each service MUST own its schema/database, accessed exclusively via its API. No other service MUST write to this schema. Cross-service reads MUST go only through the API or documented read-only replicas. `[SRC-004]`

**Rationale:** a database shared for writes = schema coupling + coupled deployments = distributed monolith.

**Enforcement:** DB IAM audit (each service has its own user with access limited to its schema).

**Exceptions:** "shared database read-only via replicas/CDC" tolerated as a documented transition (ADR + kill date).

### ARC-MS-05 — Outbox pattern for publishing events

**Requirement:** Any event publication after a DB write MUST use the **transactional outbox pattern**: an `outbox` table in the same transaction as the business write + an async relay that publishes to the bus. Alternative: CDC via Debezium reading the Postgres WAL. `[SRC-005]`

**Rationale:** "write to the DB then publish to the bus" without an outbox = zero guarantee (a crash in between = a silently lost event).

**Enforcement:** code review + audit for the outbox table's presence in every event-producing service.

### ARC-MS-06 — Saga for multi-service consistency

**Requirement:** Any consistency between services that would have required a distributed transaction MUST use a **saga**. **Orchestration by default** (Temporal, AWS Step Functions, Camunda); choreography only for trivial flows (≤3 services) AND an events-experienced team. 2PC / XA MUST NOT be used. `[SRC-006]`

**Rationale:** orchestration = explicit readability, easier to modify. Choreography = loose coupling but scattered logic, risk of event cycles.

**Enforcement:** architecture review + an ADR for each complex saga.

### ARC-MS-07 — CQRS / Event Sourcing justified in an ADR

**Requirement:** CQRS and Event Sourcing MUST be justified in an ADR by an explicit business constraint: `[SRC-007]`
- CQRS: read load ≫ write load with query patterns incompatible with the write model, OR a need for multiple read models (search, analytics, mobile).
- Event Sourcing: finance, legal audit, real-time collaboration.

**Rationale:** Fowler: *"useful in some places but not others… many disasters have come from people imagining it as a top-level architecture"*. Documented pitfalls: event versioning, costly replay, difficult ad-hoc queries.

**Enforcement:** mandatory ADR review + Tech Lead signature.

### ARC-MS-08 — Eventual consistency explained to the business

**Requirement:** Any eventual consistency exposed to the user SHOULD be explained in business terms (e.g., "the order is confirmed, stock will update in X seconds"). NEVER hide the asynchrony behind a synchronous UI that lies. `[SRC-002]`

**Rationale:** a user who sees their action "succeed" then comes back and sees the state not updated = loss of trust.

**Enforcement:** UX review + optimistic UI design patterns + reconciliation.

### Communication

### ARC-MS-09 — Async events by default between domains

**Requirement:** Communication between services SHOULD be **asynchronous (events)** by default between domains; sync (REST/gRPC) ONLY for user-facing, query-driven paths. `[SRC-002]`

| Comm type | Default stack |
|---|---|
| Async pub/sub (low-latency) | **NATS JetStream** |
| Async task queue (Node) | **BullMQ** (Redis) |
| Durable workflow (long-running, persistent retries) | **Temporal** or **Inngest** |
| High-volume event streaming (long replay) | Kafka (only if justified) |
| Public sync API | REST + OpenAPI 3.1 |
| Internal high-perf sync | gRPC + Protobuf |

**Rationale:** cascading sync calls between services = maximum fragility. Async events = temporal decoupling, natural buffering, resilience by design.

**Enforcement:** architecture review + an ADR for any inter-service sync choice.

### ARC-MS-10 — Idempotency + DLQ mandatory

**Requirement:** Every async consumer MUST be idempotent (deduplication by `event_id` or `Idempotency-Key`) and MUST have a **Dead Letter Queue** + DLQ alerting + replay tooling. `[SRC-008]`

**Rationale:** without a DLQ, a poison message blocks the queue or causes silent loss. Without idempotency, double-processing on retry.

**Enforcement:** mandatory architecture review; broker configuration audit (DLQ present).

### ARC-MS-11 — Client resilience (timeouts, retries+jitter, circuit breaker)

**Requirement:** Every inter-service sync endpoint MUST have: `[SRC-009]`
- An explicit timeout (never infinite, reasonable default 5s).
- Exponential retry **with jitter** (bounded max attempts, default 3).
- A circuit breaker (closed/open/half-open) — libs: resilience4j (Java), Polly (.NET), opossum (Node).
- Bulkheads to isolate resource pools.

**Rationale:** AWS Builders' Library: without jitter, retry storms cause a thundering herd. Without a circuit breaker, a downstream failure causes a cascade.

**Enforcement:** code review + `circuit_breaker_state` metrics exposed in monitoring.

### Deployment & ops

### ARC-MS-12 — Default platform by number of services

**Requirement:** The default containerized platform SHOULD be: `[SRC-010]`

| # services | Platform |
|---|---|
| < 10 | **ECS Fargate / Cloud Run** (managed, low-ops) |
| ≥ 10 | **Kubernetes + Argo CD** (GitOps) |

**Rationale:** K8s is overkill below 10 services for an agency's size. Beyond that, the K8s investment (control plane, service mesh, GitOps) starts to pay off.

**Enforcement:** a platform ADR at project creation.

### ARC-MS-13 — Independent CI/CD per service + contract tests

**Requirement:** Each service MUST have independent CI/CD (its own pipeline, decoupled deployment). Contracts between consumer and producer MUST be tested via **Pact** (REST) or **Buf breaking** (gRPC). Heavy pyramid E2E tests MUST NOT be used as a release gate. `[SRC-011]`

**Rationale:** E2E tests = re-coupling, distributed monolith. Contract testing = a gate at each service's build independently.

**Enforcement:** blocking CI step Pact/Buf + pipeline architecture audit.

### ARC-MS-14 — OTel observability + tail-based sampling

**Requirement:** All prod services MUST be instrumented with OpenTelemetry (see `principles.md` ARC-PRI-07). From **10+ services**, **tail-based sampling** SHOULD be configured via the OTel Collector: 100% of errors + slow requests, 1-5% nominal. `[SRC-012]`

**Rationale:** head-based sampling loses rare errors. Observability cost can reach 20-30% of the cloud bill at scale (the Coinbase $65M Datadog case) — smart sampling is essential.

**Enforcement:** OTel Collector config in review.

---

## Documented anti-patterns

| Anti-pattern | Symptom | Source |
|---|---|---|
| **Distributed monolith** | Services deployed together, e2e tests mandatory, shared DB schemas | `[SRC-013]` |
| **Nano-services** | Service = 1 endpoint, latency dominated by network | `[SRC-014]` |
| **Abusive shared kernel** | Common lib with business logic → de facto coupling | `[SRC-002]` |
| **Sync chaining** | A → B → C → D sync = cascading failure | `[SRC-002]` |
| **No DLQ** | Poison message blocks the queue or silent loss | `[SRC-008]` |
| **Single shared DB read+write** | Maximum coupling | `[SRC-004]` |

---

## Enforcement summary

| Mechanism | Rules covered | Auto |
|---|---|---|
| Pact / Buf breaking in CI | ARC-MS-13 | Yes |
| OTel + tail-based sampling | ARC-MS-14 | Partial |
| DLQ + idempotency audit | ARC-MS-10 | Manual |
| DB IAM audit (database-per-service) | ARC-MS-04 | Manual |
| Architecture review (ADR) | ARC-MS-01, 02, 03, 06, 07, 12 | Manual |
| Code review (PR) | ARC-MS-05, 08, 09, 11 | Manual |

## Sources

- `[SRC-001]` Fowler — BoundedContext: https://martinfowler.com/bliki/BoundedContext.html
- `[SRC-002]` Newman — Building Microservices 2nd ed (2021): https://samnewman.io/books/building_microservices_2nd_edition/
- `[SRC-003]` Fowler — StranglerFigApplication: https://martinfowler.com/bliki/StranglerFigApplication.html
- `[SRC-004]` Richardson — Database per Service pattern: https://microservices.io/patterns/data/database-per-service.html
- `[SRC-005]` Richardson — Transactional Outbox pattern: https://microservices.io/patterns/data/transactional-outbox.html
- `[SRC-006]` Richardson — Saga pattern: https://microservices.io/patterns/data/saga.html + AWS Saga prescriptive guidance
- `[SRC-007]` Fowler — CQRS: https://martinfowler.com/bliki/CQRS.html + EventSourcing: https://martinfowler.com/eaaDev/EventSourcing.html
- `[SRC-008]` AWS — DLQ best practices: https://docs.aws.amazon.com/lambda/latest/dg/invocation-async.html
- `[SRC-009]` AWS Builders' Library — Timeouts/retries/backoff with jitter: https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
- `[SRC-010]` CNCF Annual Survey 2024 + Cloud Run / ECS Fargate docs
- `[SRC-011]` Pact docs: https://docs.pact.io/ + Buf breaking: https://buf.build/docs/breaking/overview
- `[SRC-012]` OpenTelemetry Sampling: https://opentelemetry.io/docs/concepts/sampling/ + Honeycomb cost observability: https://www.honeycomb.io/blog/cost-observability
- `[SRC-013]` Richardson — Services + E2E testing = monolith: https://microservices.io/post/architecture/2024/03/29/services-with-end-to-end-testing-equals-monolith.html
- `[SRC-014]` microservices.io anti-patterns: https://microservices.io/post/antipatterns/2019/01/07/microservices-antipatterns.html

## Change log

| Version | Date | Author | Description |
|---|---|---|---|
| 1.0.0 | 2026-04-30 | Team | Initial — from Deep-mode research, Agent C (Microservices, 6 sub-axes). |
