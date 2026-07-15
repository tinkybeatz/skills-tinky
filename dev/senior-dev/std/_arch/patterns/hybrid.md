# Standard: Pattern — Hybrid + Cross-cutting Operations

- **Status:** Active
- **Version:** 1.0.0
- **Owner:** Engineering Lead
- **Effective date:** 2026-04-30

## Scope

Two topics in this file:

1. **Hybrid patterns** (a mix of several patterns) — the most frequent pattern in agency work (~80% of projects).
2. **Cross-cutting operations** — ops rules that apply to ALL patterns (modular monolith, microservices, serverless, hybrid).

## Core decisions

- **IaC** = OpenTofu (see ARC-OPS-02).
- **Platform < 10 services** = ECS Fargate / Cloud Run (see ARC-OPS-03).
- **Feature flags** = GrowthBook OSS (full system) or env vars (<5 simple flags) (see ARC-OPS-04).
- **Secrets** = cloud-native provider or Infisical (see `principles.md` ARC-PRI-05).
- **Observability** = Grafana Cloud LGTM by default (see `principles.md` ARC-PRI-07).
- **Async workers** = BullMQ (Node) or NATS JetStream (see ARC-HY-01).
- **Durable workflows** = Temporal or Inngest if needed.

---

## Section 1 — Hybrid patterns

### Dominant pattern: Modular Monolith + Async Workers (H1)

This is the default pattern for ~80% of client projects (see `decision-framework.md` ARC-DEC-05).

Structure:
- **Main monolith**: HTTP API + Postgres DB (single deployable).
- **Separate workers**: distinct processes that consume a queue for long jobs (AI inference, ETL, doc generation, outbound webhooks, batch processing).

### Pattern: Backend-for-Frontend (BFF, H2)

A dedicated backend per frontend surface (web, mobile, IoT). Relevant from 3+ heterogeneous surfaces onward. For 1-2 frontends, a single BFF is enough.

### Pattern: Selective microservices (H3)

A main monolith + 1 to 3 services extracted for an **explicit and measurable** reason: 10x differential scaling, incompatible runtime (Python ML vs Node API), dedicated team. Follows Strangler Fig.

---

## Normative rules — Hybrid patterns

### ARC-HY-01 — Async workers: queue + idempotency + DLQ mandatory

**Requirement:** Any system with async workers MUST have: `[SRC-001]`
- **Managed queue**: BullMQ (Redis, Node) OR NATS JetStream OR AWS SQS+SNS OR Inngest/Temporal for durability.
- **Idempotency keys** on every side-effect.
- **DLQ** + DLQ alerting + replay tooling.
- **Critical metrics**: `queue_depth` + `oldest_message_age` exposed in monitoring.

**Rationale:** without a DLQ, a poison message blocks the queue or causes silent loss. Without idempotency, platform retries cause double-processing.

**Enforcement:** architecture review + broker configuration audit.

### ARC-HY-02 — Single BFF as long as ≤ 2 surfaces

**Requirement:** A single BFF SHOULD be maintained as long as there are ≤ 2 client surfaces (the typical web + mobile). Multi-BFF (one per surface) ONLY from 3 heterogeneous surfaces (web + mobile + IoT, or web + mobile + browser extension). `[SRC-002]`

**Rationale:** a premature multi-BFF = code duplication between BFFs. A single BFF with per-client query/transformation (via headers or paths) covers most needs.

**Enforcement:** initial architecture review.

### ARC-HY-03 — No business logic in the BFF

**Requirement:** The BFF MUST remain a thin layer of **composition + transformation** (aggregating internal services, shaping payloads for the client). All business logic (rules, business validations, domain calculations) MUST NOT reside there. `[SRC-002]`

**Rationale:** the Newman / Calçado rule: *"one BFF per user experience"* — without this discipline, the BFF drifts into an aggregation monolith and everything gradually migrates into it.

**Enforcement:** BFF code review + regular audit.

### ARC-HY-04 — Strangler Fig with a legacy kill date

**Requirement:** Any migration from a legacy system (service extraction, major refactor, framework migration) MUST follow Strangler Fig + Branch by Abstraction. The opening ticket MUST include a **kill date** for the legacy code. `[SRC-003]`

**Rationale:** without a kill date, the legacy and the new coexist forever. This is the worst of both worlds: double maintenance, double attack surface, double debt.

**Enforcement:** ADR review + kill date tracking in the ticket.

### ARC-HY-05 — Selective microservices justified by a measurable constraint

**Requirement:** Any extraction of a service from a monolith MUST be justified in an ADR by a measurable constraint: `[SRC-004]`
- A component that scales 10x differently from the monolith (required RPS / CPU / memory measurement).
- An incompatible tech stack (e.g., ML inference Python/CUDA vs Node API).
- A dedicated team with independent deploy needed.
- Compliance forcing isolation (PCI scope reduction).

**Rationale:** extraction without a constraint = cargo-cult + distributed monolith.

**Enforcement:** mandatory ADR review; the extraction PR MUST cite the constraint.

---

## Section 2 — Cross-cutting operations

Apply to all patterns. Rules prefixed `ARC-OPS`.

### ARC-OPS-01 — Trunk-based development

**Requirement:** Every project MUST adopt trunk-based development: `[SRC-005]`
- PR < 400 LOC.
- Merge in < 24h.
- Short branches (never > 2 days).
- DORA metrics measured from project 1 (deployment frequency + lead time minimum).

**Rationale:** trunk-based correlates with DORA top performers. Long-lived branches = merge conflicts + fragmented QA.

**Enforcement:** GitHub branch protection + PR size audit in CI.

### ARC-OPS-02 — IaC = OpenTofu by default

**Requirement:** All production infra MUST be in IaC. **OpenTofu** is the default tool. Terraform allowed on explicit client constraint. Pulumi acceptable if the stack is 100% TypeScript and the team is aligned. `[SRC-006]`

**Rationale:** OpenTofu = the Linux Foundation fork of Terraform, free and open (vs Terraform BSL since August 2023). 100% syntax compatibility — no reason to pay for Terraform for agency use.

**Enforcement:** IaC repo review + drift detection in CI (`tofu plan` must return *no changes*).

### ARC-OPS-03 — Containerized platform < 10 services

**Requirement:** The default containerized platform SHOULD be: `[SRC-007]`

| # services | Platform |
|---|---|
| < 10 | **ECS Fargate / Cloud Run** (managed, low-ops) |
| ≥ 10 | **Kubernetes + Argo CD** (GitOps) |

**Rationale:** K8s is overkill below 10 services for an agency's size. The K8s investment (control plane, mesh, GitOps) pays off from 10+ services.

**Enforcement:** a platform ADR at project creation.

### ARC-OPS-04 — Feature flags: GrowthBook or env vars

**Requirement:** `[SRC-008]`
- **< 5 simple boolean flags** without targeting → env vars acceptable (`if (process.env.FEATURE_X === 'true')`).
- **Full system required** (admin UI, targeting rules, A/B testing, real-time updates) → **GrowthBook** (OSS, self-host Docker).
- LaunchDarkly allowed only if the client pays and volume justifies it.
- A **standardized in-house system** MUST NOT be built.

**Rationale:** GrowthBook OSS is free + self-hostable = covers all needs (flags + A/B testing). No reason to reinvent an in-house system.

**Enforcement:** a feature-flags ADR if a full system is required.

### ARC-OPS-05 — Mandatory cloud tagging

**Requirement:** Every deployed cloud resource MUST be tagged with: `project`, `client`, `env` (`prod`/`staging`/`dev`/`preview`), `owner`. Merging an IaC PR MUST be refused if the tags are missing. `[SRC-009]`

**Rationale:** without tagging, FinOps is impossible (no cost per project / per client). Tagging = the basis of any cost strategy.

**Enforcement:** Terraform/OpenTofu lint (tflint) + blocking CI step.

### ARC-OPS-06 — Infracost in CI + cloud budget alerts

**Requirement:** `[SRC-010]`
- [Infracost](https://www.infracost.io/) MUST be configured in CI on every IaC repo, commenting each PR with a cost estimate.
- Cloud budget alerts MUST be configured at account creation (AWS Budgets, GCP Billing alerts, Azure Cost Management).

**Rationale:** without cost visibility, a bill surprise in month 2-3. Infracost in PRs = cost-aware code review.

**Enforcement:** Infracost CI step + cloud account setup audit.

### ARC-OPS-07 — Preview environments per PR

**Requirement:** Every PR SHOULD create an ephemeral preview environment (Vercel Preview, Render Preview, Railway PR env, Neon DB branching). The preview env MUST expire after 7 days. The DB MUST be seeded (never prod data). `[SRC-011]`

**Rationale:** a preview env = review on a real environment without polluting prod. A pattern adopted massively in 2025-2026.

**Enforcement:** GitHub Actions auto-creation + cleanup.

### ARC-OPS-08 — Prod data outside prod: forbidden except with masking

**Requirement:** Production data MUST NOT be copied to dev/staging without masking. If needed for debugging, use: Snaplet (Neon), Tonic.ai, Postgres Anonymizer. `[SRC-012]`

**Rationale:** GDPR art. 5 (minimization). Prod data in dev = an inevitable breach at the next dev repo leak.

**Enforcement:** data-export process review + GDPR audit.

### ARC-OPS-09 — Contract testing for public + internal APIs

**Requirement:** `[SRC-013]`
- **Public API**: OpenAPI 3.1 + [oasdiff](https://github.com/oasdiff/oasdiff) blocking in CI on breaking changes.
- **Internal service-to-service** (if microservices): Pact (REST) or Buf breaking check (gRPC) in CI.

**Rationale:** breaking changes in prod = broken clients. Detection in CI = before merge.

**Enforcement:** blocking CI step.

---

## Deferred-activation rules (trigger above thresholds)

| Rule / Tool | Activation trigger |
|---|---|
| **Backstage / Port (IDP)** | From **20 devs** or **10 concurrent active projects** |
| **Score (workload portability)** | Evaluate if **3+ deployment targets** (AWS + GCP + edge) |
| **Schema registry (Confluent / Apicurio)** | As soon as a project uses **Kafka** or **multi-producer pub/sub** |
| **Service mesh (Istio Ambient / Cilium)** | From **30+ services** or a need for uniform **mTLS** / fine-grained policies |
| **Tail-based sampling OTel** | From **10+ services** in prod |

---

## Enforcement summary

| Mechanism | Rules covered | Auto |
|---|---|---|
| GitHub branch protection + PR size lint | ARC-OPS-01 | Yes |
| `tofu plan` drift detection | ARC-OPS-02 | Yes |
| tflint tagging check | ARC-OPS-05 | Yes |
| Infracost CI | ARC-OPS-06 | Yes |
| Preview env auto-creation | ARC-OPS-07 | Yes |
| oasdiff / Pact / Buf in CI | ARC-OPS-09 | Yes |
| DLQ + idempotency audit | ARC-HY-01 | Manual |
| BFF code review | ARC-HY-02, 03 | Manual |
| ADR review (Strangler kill date, extraction) | ARC-HY-04, 05 | Manual |
| GDPR data-masking audit | ARC-OPS-08 | Manual |

## Sources

- `[SRC-001]` BullMQ: https://docs.bullmq.io/ + Inngest: https://www.inngest.com/ + Temporal: https://docs.temporal.io/
- `[SRC-002]` Newman — BFF pattern: https://samnewman.io/patterns/architectural/bff/ + Phil Calçado (SoundCloud 2015): https://philcalcado.com/2015/09/18/the_back_end_for_front_end_pattern_bff.html
- `[SRC-003]` Fowler — StranglerFigApplication: https://martinfowler.com/bliki/StranglerFigApplication.html + Branch by Abstraction: https://martinfowler.com/bliki/BranchByAbstraction.html
- `[SRC-004]` Newman — Monolith to Microservices: https://samnewman.io/books/monolith-to-microservices/
- `[SRC-005]` DORA / dora.dev: https://dora.dev/research/ + trunkbaseddevelopment.com: https://trunkbaseddevelopment.com/
- `[SRC-006]` OpenTofu: https://opentofu.org/
- `[SRC-007]` ECS Fargate / Cloud Run docs + CNCF Annual Survey 2024
- `[SRC-008]` GrowthBook: https://www.growthbook.io/ + OpenFeature (CNCF): https://openfeature.dev/
- `[SRC-009]` FinOps Foundation: https://www.finops.org/framework/ + FOCUS spec: https://focus.finops.org/
- `[SRC-010]` Infracost: https://www.infracost.io/
- `[SRC-011]` Vercel Preview: https://vercel.com/docs/deployments/preview-deployments + Neon branching: https://neon.tech/docs/introduction/branching
- `[SRC-012]` GDPR art. 5: https://gdpr-info.eu/art-5-gdpr/ + Snaplet: https://snaplet.dev/
- `[SRC-013]` OpenAPI 3.1 + oasdiff: https://github.com/oasdiff/oasdiff + Pact: https://docs.pact.io/

## Change log

| Version | Date | Author | Description |
|---|---|---|---|
| 1.0.0 | 2026-04-30 | Team | Initial — from Deep-mode research, Agent D (Hybrid + Cross-cutting Operations). |
