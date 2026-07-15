# Standard: Architecture Principles

- **Status:** Active
- **Version:** 1.0.0
- **Owner:** Engineering Lead
- **Approvers:** Tech Lead
- **Effective date:** 2026-04-30
- **Last review date:** 2026-04-30

## Scope

Every project — frontend, backend, scripts, infra, agentic AI. These rules are **invariant**: they apply regardless of the chosen stack or the selected architecture pattern.

For pattern-specific rules: `patterns/modular-monolith.md`, `patterns/microservices.md`, `patterns/serverless.md`, `patterns/hybrid.md`. For the decision framework: `decision-framework.md`.

## Core decisions (not up for debate)

1. **IaC** = OpenTofu (see ARC-PRI-06).
2. **Observability** = Grafana Cloud LGTM by default, OpenTelemetry instrumentation (see ARC-PRI-07).
3. **Secrets** = cloud-native provider or Infisical (see ARC-PRI-05).

---

## Normative rules

### ARC-PRI-01 — Tooled boundaries

**Requirement:** Every module or service boundary MUST be enforced by automated tooling in CI (linter, ArchUnit, Packwerk, eslint-plugin-boundaries, dependency-cruiser, Nx). A documentation-only boundary is forbidden. `[SRC-001]`

**Rationale:** without tooling, human discipline drifts within 6 months (Shopify Packwerk retrospective). Boundaries are the first line of defense against the ball-of-mud.

**Enforcement:** presence of a boundary linter in CI (automated check).

### ARC-PRI-02 — Exclusive data ownership per bounded context

**Requirement:** A piece of data MUST belong to a single bounded context, which is its sole source of truth. No schema shared for cross-domain writes. Cross-context consumption happens via API or event, never by SQL join. `[SRC-002]`

**Rationale:** DDD corollary — *"microservices only work well if you come up with good, stable boundaries between the services"* (Fowler). Sharing schemas creates de facto coupling that prevents independent evolution.

**Enforcement:** architecture review (initial ADR), SQL audit in CI.

**Exceptions:** cross-service reads via read-only replicas or CDC allowed as a documented transition (ADR + kill date).

### ARC-PRI-03 — Stateless services + explicit state

**Requirement:** Every service MUST be stateless. All persistent state MUST be stored in an explicit backing service (relational DB, cache, queue, object store). `[SRC-003]`

**Rationale:** 12-factor VI. Enables horizontal scaling, deployment without data loss, reproducible debugging.

**Enforcement:** architecture review + tests validating restart without state loss.

### ARC-PRI-04 — Idempotency on external boundaries

**Requirement:** Every mutating endpoint exposed to a third-party client (HTTP, webhook, message bus, payment) MUST accept an `Idempotency-Key` header. Every message consumer MUST deduplicate by `event_id` at minimum. `[SRC-004]`

**Rationale:** automatic retries (clients, platforms, message brokers) are the rule, not the exception. Without idempotency, silent double-charge in production.

**Enforcement:** mandatory review on every mutating HTTP handler and async consumer.

**Exceptions:** pure read (GET) endpoints are exempt.

### ARC-PRI-05 — Secrets in a dedicated vault

**Requirement:** No secret (API key, password, certificate, token) MUST reside in the repo. Storage MUST be in a dedicated vault: cloud-native provider (AWS Secrets Manager / GCP Secret Manager / Azure Key Vault) or Infisical (multi-cloud / self-host). Automatic rotation MUST be configured for long-lived secrets (DB, vendor API keys). `[SRC-005]`

**Rationale:** 12-factor III. Cleartext secrets in the repo = an inevitable breach at the first fork or repo leak.

**Enforcement:** [Gitleaks](https://github.com/gitleaks/gitleaks) as a pre-commit hook + audit in CI.

### ARC-PRI-06 — IaC for all production infrastructure

**Requirement:** All production infrastructure (compute, network, DB, DNS, certificates, IAM) MUST be described in IaC. **OpenTofu** is the default tool; Terraform allowed on explicit client constraint. Every environment MUST be reproducible from code in under 1 hour. `[SRC-006]`

**Rationale:** "ClickOps" (manual config via consoles) prevents client handover, disaster recovery, and infra code review. IaC = agency portability.

**Enforcement:** infra review = PR review. Automatic drift detection in CI (`tofu plan` must return *no changes*).

### ARC-PRI-07 — OpenTelemetry observability

**Requirement:** Every production service MUST be instrumented with OpenTelemetry (traces + metrics + structured JSON logs). Context propagation MUST follow W3C Trace Context. Logs MUST include `trace_id`, `span_id`, `service.name`, `service.version`. **Default backend: Grafana Cloud LGTM**. Datadog allowed if the client pays and volume justifies it. `[SRC-007]`

**Rationale:** OTel = CNCF Incubating standard, ~50% cloud-native adoption (CNCF). Without propagation, distributed debugging is impossible. Without JSON logs, parsing is impossible. A vendor-neutral SDK = no re-instrumentation when switching tools.

**Enforcement:** presence of the OTel SDK in every prod service, verified in CI.

### ARC-PRI-08 — Explicit timeouts and retries

**Requirement:** Every outbound call (HTTP, DB, message bus, RPC) MUST have an explicit timeout (never infinite). Every retry MUST use exponential backoff **with jitter** and a bounded max attempts. `[SRC-008]`

**Rationale:** without jitter, retry storms cause cascading collapse (AWS Builders' Library). Without a timeout, a slow downstream service blocks the entire chain.

**Enforcement:** code review + custom lint detecting calls without a timeout.

**Reasonable defaults:** 5s timeout for user-facing APIs, 30s for background jobs, 3 retries with ±50% jitter, 10s max cumulative.

### ARC-PRI-09 — RED + USE metrics

**Requirement:** Every exposed endpoint SHOULD have RED metrics (Rate, Errors, Duration). Every critical infra resource SHOULD have USE metrics (Utilization, Saturation, Errors). `[SRC-009]`

**Rationale:** RED (Tom Wilkie / Grafana Labs) covers the service level; USE (Brendan Gregg) covers the resource level. The two are complementary, not interchangeable.

**Enforcement:** initial dashboard review + alerts on p99 + error rate.

### ARC-PRI-10 — Versioned public APIs

**Requirement:** Every public API SHOULD be versioned (path `/v1`, header, or query param). Backward compatibility SHOULD be maintained for N-1. A written deprecation policy MUST exist before any breaking change. `[SRC-010]`

**Rationale:** a client in production cannot migrate instantly. Without a deprecation policy, service disruption at the next release.

**Enforcement:** OpenAPI 3.1 + [oasdiff](https://github.com/oasdiff/oasdiff) blocking in CI on breaking changes.

### ARC-PRI-11 — Circuit breaker in production

**Requirement:** Every inter-service call in production SHOULD be protected by a circuit breaker (closed / open / half-open). Allowed libraries: resilience4j (Java), Polly (.NET), opossum (Node). `[SRC-008]`

**Rationale:** without a circuit breaker, a downstream failure causes a cascade. With one, the failing service is isolated for N seconds, then progressively re-tested.

**Enforcement:** code review + `circuit_breaker_state` metrics exposed in monitoring.

### ARC-PRI-12 — ADRs and runbooks

**Requirement:** Every structuring decision (pattern choice, stack choice, major trade-off, vendor lock-in > 2 person-months to migrate) MUST be documented in an ADR ([adr.github.io](https://adr.github.io/)). Every production service MUST have a runbook (deployment, rollback, common incidents, contacts). `[SRC-011]`

**Rationale:** agency-specific — code readable by a third party at month +12. ADR + runbook = what survives a client handover.

**Enforcement:** mandatory review at service creation; deployment checklist.

---

## Enforcement summary

| Mechanism | Rules covered | Auto |
|---|---|---|
| Boundary linter (Packwerk, eslint-plugin-boundaries, dependency-cruiser) | ARC-PRI-01 | Yes |
| Gitleaks pre-commit + CI audit | ARC-PRI-05 | Yes |
| `tofu plan` drift detection in CI | ARC-PRI-06 | Yes |
| OTel SDK presence check in CI | ARC-PRI-07 | Yes |
| oasdiff breaking change detection | ARC-PRI-10 | Yes |
| Architecture review (initial ADR) | ARC-PRI-02, 03, 04, 12 | Manual |
| Code review (PR) | ARC-PRI-08, 09, 11 | Manual |

## Exceptions process

- Max 90 days, renewable once with written justification.
- Approved by Tech Lead.
- Recorded in an ADR or inline comment (`// EXCEPTION ARC-PRI-XX: <reason> — expires 2026-MM-DD`).

## Sources

- `[SRC-001]` Shopify — Enforcing Modularity with Packwerk: https://shopify.engineering/enforcing-modularity-rails-apps-packwerk
- `[SRC-002]` Fowler — MonolithFirst / BoundedContext: https://martinfowler.com/bliki/MonolithFirst.html
- `[SRC-003]` 12-factor app (open-sourced 2024-11): https://12factor.net/
- `[SRC-004]` Stripe — Designing robust APIs with idempotency: https://stripe.com/blog/idempotency
- `[SRC-005]` 12-factor III + AWS Secrets Manager docs: https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html
- `[SRC-006]` OpenTofu (Linux Foundation): https://opentofu.org/
- `[SRC-007]` OpenTelemetry (CNCF): https://opentelemetry.io/ + https://www.cncf.io/projects/opentelemetry/
- `[SRC-008]` AWS Builders' Library — Timeouts/retries/backoff with jitter: https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
- `[SRC-009]` Grafana Labs — RED Method (Tom Wilkie): https://grafana.com/blog/the-red-method-how-to-instrument-your-services/
- `[SRC-010]` OpenAPI 3.1 spec: https://spec.openapis.org/oas/v3.1.0 + oasdiff: https://github.com/oasdiff/oasdiff
- `[SRC-011]` ADR (Architecture Decision Records): https://adr.github.io/

## Change log

| Version | Date | Author | Description |
|---|---|---|---|
| 1.0.0 | 2026-04-30 | Team | Initial — from Deep-mode research (4 parallel agents, 50+ primary sources) + internal decisions (OpenTofu, Grafana Cloud LGTM, cloud-native secrets). |
