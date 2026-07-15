# Architecture Standards

This folder contains the **cross-cutting** architecture standards, applicable to any client project regardless of the stack or pattern chosen.

## A 3-level convention

The team operates as an **agency**, not a single-product company. Unlike Shopify (an imposed Rails monolith), GitHub, or Basecamp, the team works with different stacks and constraints for each client. The standard therefore does **not** fix a default stack. Instead, it standardizes **three independent levels**:

```
_arch/
├── principles.md           # Level 1: invariants (apply everywhere)
├── decision-framework.md   # Level 2: how to choose the pattern by context
└── patterns/               # Level 3: rules specific to the chosen pattern
    ├── modular-monolith.md
    ├── microservices.md
    ├── serverless.md
    └── hybrid.md
```

### Level 1 — `principles.md` (12 invariant rules)

Rules that apply to **every** project, regardless of stack: tooled boundaries, data ownership, statelessness, idempotency, OTel observability, resilience, secrets, IaC, ADRs.

**Always loaded** by `/senior-dev` at Step 0.

### Level 2 — `decision-framework.md` (8 rules + decision matrix)

Criteria for choosing between patterns based on client context: team size, ops maturity, load, cost profile, time-to-market, compliance, domain stability.

**Reference position**: default = modular monolith. Microservices = exception (5 simultaneous "pro" signals required). Serverless = specific workload shape. Hybrid = dominant pattern in 80% of projects.

**Loaded** when an architecture decision is at stake (ADR, initial project choice, major refactor).

### Level 3 — `patterns/*.md` (rules per chosen pattern)

For each pattern: when to use it, how to do it well, documented anti-patterns, specific rules.

**Loaded** based on the pattern present in the repo (detection: `package.json` workspaces, `docker-compose.yml`, IaC files, repo structure).

## Why no imposed stack?

Serious agencies (ThoughtWorks, OCTO, Pivotal pre-Broadcom) standardize the **properties** every deliverable must respect, never the **stacks**. What survives a client handover: portability (12-factor + IaC + containers), readability (READMEs, ADRs, runbooks), testability (green build), baseline security (secrets, dependencies).

## Locked-in decisions

These decisions are fixed for every project as of 2026-04-30:

| # | Topic | Decision |
|---|---|---|
| 1 | IaC default | **OpenTofu** (Linux Foundation, Terraform fork) |
| 2 | Platform < 10 services | **ECS Fargate / Cloud Run** |
| 3 | Queue/workflow | **NATS JetStream** (pub/sub) + **BullMQ** (Node task queues); Temporal/Inngest if durability needed |
| 4 | Feature flags | **GrowthBook** (OSS) for a full system; env vars for <5 simple flags |
| 5 | Secrets | **Cloud-native provider** (AWS/GCP/Azure); Infisical if multi-cloud |
| 6 | Observability | **Grafana Cloud LGTM**; Datadog if the client pays |
| 7 | Messaging broker | **NATS JetStream**; Kafka for high-volume streaming |

## Loading rules for `/senior-dev`

To add in `senior-dev/SKILL.md` Step 0:
- `_arch/principles.md` — ALWAYS loaded.
- `_arch/decision-framework.md` — loaded if an architecture decision is at stake.
- `_arch/patterns/<X>.md` — loaded based on the pattern detected in the repo.

## Source

Standards generated from Deep-mode research (4 parallel agents, 50+ primary sources: Fowler, Newman, Richardson, ThoughtWorks Radar, AWS Builders' Library, OpenTelemetry, CNCF, Shopify, GitHub, Stripe, DHH).
