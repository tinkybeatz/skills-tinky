# Standard: Pattern — Serverless / FaaS / Edge

- **Status:** Active
- **Version:** 1.0.0
- **Owner:** Engineering Lead
- **Effective date:** 2026-04-30

## Scope

Every project that has adopted (partially or fully) the **serverless** pattern (FaaS, edge runtimes) AFTER validating `decision-framework.md` ARC-DEC-04 (a specific workload shape required).

⚠️ **Reminder**: serverless = a workload shape, **not a default**. It is NOT suitable for: steady-state workloads >50% duty cycle, strict latency <50ms, long-running >15min (Lambda) / >5min (Edge), unacceptable vendor lock-in.

## Core decisions

- **Edge V8 isolates** (Cloudflare Workers, Deno Deploy, Vercel Edge) for read-heavy global APIs.
- **AWS Lambda Node/Python** for AWS-native event-driven work.
- **AWS Lambda SnapStart** for Java/Python with cold-start constraints.
- **Connection pooler mandatory** (Hyperdrive, RDS Proxy, Neon, Supabase Pooler).
- **Observability**: OTel + Grafana Cloud LGTM (see `principles.md`).

---

## State of the art, 2026

- **Edge V8 isolates**: cold start ~5ms (Cloudflare Workers, Deno Deploy, Vercel Edge Runtime) `[SRC-001]`.
- **AWS Lambda SnapStart**: Java from ~5s to ~180ms, Python sub-200ms, .NET and Python GA late 2024 `[SRC-002]`.
- **Cloudflare Hyperdrive** GA 2024, free in 2025: global Postgres pool, -90% latency `[SRC-003]`.
- **Vercel Functions**: Edge Functions deprecated 2025 → Vercel Functions Node.js with Fluid Compute, 300s limit `[SRC-004]`.
- **Neon serverless driver**: 10,000 concurrent connections via PgBouncer `[SRC-005]`.

---

## Normative rules

### ARC-SL-01 — Connection pooler mandatory between FaaS and relational DB

**Requirement:** No FaaS handler MUST open a direct Postgres/MySQL connection. A connection pooler MUST be interposed: `[SRC-005]` `[SRC-003]`

| Target | Pooler |
|---|---|
| AWS Lambda + RDS Postgres/MySQL | RDS Proxy |
| Cloudflare Workers + remote Postgres | **Hyperdrive** |
| Workers / Edge + Neon | **Neon serverless driver** (HTTP/WebSocket) |
| Edge + Supabase | Supabase Pooler (PgBouncer) |

**Rationale:** each FaaS invocation = 1 open connection at worst. Without a pooler, Postgres saturates at `max_connections` (~100-500 depending on config) → `too many connections` errors → cascade.

**Enforcement:** initial architecture review + audit of the `pg`/`postgres-js` config in the code.

### ARC-SL-02 — Budget alerts + concurrency limits before prod

**Requirement:** Before going to prod, the project MUST configure: `[SRC-006]`
- **Budget alerts** on the platform side (AWS Cost Explorer, Cloudflare, Vercel usage).
- **Concurrency limits**: AWS Lambda reserved/provisioned concurrency, Cloudflare Worker rate limits, Vercel concurrency caps.

**Rationale:** unbounded spiky traffic can silently generate a 100x bill. Serverless bills by the millisecond — without a limit, the damage is irreversible.

**Enforcement:** deployment checklist + configuration audit in review.

### ARC-SL-03 — OpenTelemetry from the 1st deployment

**Requirement:** Every serverless handler MUST be instrumented with OpenTelemetry (propagated traces, structured JSON logs) **from the first deployment** — not as a post-mortem. `[SRC-007]`

**Rationale:** without distributed tracing, debugging a failure across 5 functions is impossible. An event-driven workflow without correlation = a guaranteed operational nightmare.

**Enforcement:** CI verifies the OTel SDK is present; structured JSON logs validated.

### ARC-SL-04 — Idempotency by design

**Requirement:** Every handler MUST be idempotent by design. The platform's automatic retries (Lambda DLQ, Workers retries, Step Functions catch) are the rule. An idempotency key (deduped header, conditional transaction) MUST be implemented on every side-effect. `[SRC-008]`

**Rationale:** the platform retries without asking permission. Without idempotency, silent double-charge / double-write.

**Enforcement:** mandatory code review + idempotency tests.

### ARC-SL-05 — Runtime choice by target latency

**Requirement:** The runtime SHOULD be chosen based on target latency and cold-start profile: `[SRC-001]` `[SRC-002]`

| Target latency | Runtime |
|---|---|
| Cold start < 50ms | Cloudflare Workers, Deno Deploy, Vercel Edge (V8 isolates) |
| Node.js / Python event-driven AWS | AWS Lambda Node/Python |
| Java / Python with cold-start constraint | AWS Lambda + **SnapStart** |
| .NET | AWS Lambda + SnapStart (GA late 2024) |

**Rationale:** V8 isolates have almost no cold start; Lambda Node is sub-1s; Java/.NET without SnapStart = 5s+ cold start = broken p99 SLA.

**Enforcement:** runtime ADR + cold-start metrics audit.

### ARC-SL-06 — Externalized stateful state

**Requirement:** No dependency on memory between invocations. All stateful state MUST be externalized: `[SRC-009]`
- **KV stores**: Cloudflare KV, AWS DynamoDB, Vercel KV.
- **Object storage**: R2, S3, GCS.
- **Distributed cache**: Redis (Upstash, Redis Cloud).
- **Stateful primitives**: Cloudflare Durable Objects, AWS Step Functions state.

**Rationale:** FaaS invocations = ephemeral processes, never a guarantee of reuse. Shared memory = intermittent prod bugs.

**Enforcement:** code review (no mutable globals).

### ARC-SL-07 — Vendor abstraction if migration risk

**Requirement:** If the client is at risk of multi-cloud migration or a vendor change, the code SHOULD be abstracted behind an agnostic framework: [Hono](https://hono.dev/), [sst](https://sst.dev/), [serverless framework](https://www.serverless.com/). `[SRC-010]`

**Rationale:** the Lambda / Workers / Vercel / Azure Functions APIs are incompatible. API-specific lock-in = costly migration at the end of an engagement.

**Enforcement:** architecture review + vendor lock-in ADR (see `decision-framework.md` ARC-DEC-07).

### ARC-SL-08 — No long-lived WebSocket/SSE without a dedicated primitive

**Requirement:** Classic FaaS (Lambda, standard Cloud Functions) MUST NOT be used for WebSocket / SSE / long-lived connections. Use only the dedicated primitives: `[SRC-011]`
- **Cloudflare Durable Objects** for stateful at edge.
- **AWS API Gateway WebSocket** + Lambda.
- **AWS AppSync** for GraphQL subscriptions.

**Rationale:** Lambda max 15min, Workers max 30s per invocation for non-WebSocket HTTP requests. Long-lived without a primitive = guaranteed failure.

**Enforcement:** architecture review + an ADR for any real-time need.

### ARC-SL-09 — No sustained-CPU workload on per-ms billing

**Requirement:** CPU-intensive workloads with **>30% of time in sustained compute** MUST NOT be deployed on per-ms-billed FaaS. Switch to a container (ECS Fargate, Cloud Run, Fly.io) or a VM. `[SRC-012]`

**Rationale:** beyond a certain continuous RPS, Lambda can be 78x more expensive than Fargate (see TechPlained 2026). FaaS is optimized for bursty, not steady-state.

**Enforcement:** initial ADR with workload analysis (estimated duty cycle) + cost audit after 1 month in prod.

### ARC-SL-10 — No greenfield "full serverless" without experience

**Requirement:** Starting a greenfield product "full serverless" (Lambda + DynamoDB + Step Functions + EventBridge end-to-end) MUST NOT be proposed if the client team has never operated a distributed stack. Prefer a modular monolith + targeted extraction. `[SRC-013]`

**Rationale:** a 100% serverless stack = difficult distributed tracing, complex debugging, hidden operational debt. Not transferable to a client without experience.

**Enforcement:** architecture challenge during pre-project; rejection if there is no signal of experience.

---

## Common pitfalls

| Pitfall | Symptom | Mitigation |
|---|---|---|
| Ignored cold starts | Broken p99 SLA on Java/.NET | ARC-SL-05 (SnapStart or V8 isolates) |
| Postgres connection pool exhaustion | `too many connections`, cascading retries | ARC-SL-01 (mandatory pooler) |
| Cost exploding under load | 10x bill in month 2 vs month 1 | ARC-SL-02 (budget alerts) + ARC-SL-09 |
| Missing distributed tracing | Event-driven workflow impossible to debug | ARC-SL-03 (OTel from day 1) |
| API-specific vendor lock-in | Migration impossible at end of engagement | ARC-SL-07 (Hono/sst) + signed ADR |
| Ignored runtime limits | Unexpected timeouts, fetch limit, no Node APIs | Audit platform limits before prod `[SRC-004]` |
| Durable Objects with open connections | Exhausts the Hyperdrive pool | Architecture review |

---

## Enforcement summary

| Mechanism | Rules covered | Auto |
|---|---|---|
| OTel SDK presence audit | ARC-SL-03 | Yes |
| Budget alerts + concurrency limits audit | ARC-SL-02 | Yes (checklist) |
| Pooler config audit | ARC-SL-01 | Manual |
| Idempotency tests | ARC-SL-04 | Yes |
| Cost monitoring + duty cycle audit | ARC-SL-09 | Manual |
| Architecture review (ADR) | ARC-SL-05, 06, 07, 08, 10 | Manual |

## Sources

- `[SRC-001]` Cloudflare Workers / V8 isolates: https://workers.cloudflare.com/
- `[SRC-002]` AWS Lambda SnapStart: https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html
- `[SRC-003]` Cloudflare Hyperdrive: https://developers.cloudflare.com/hyperdrive/
- `[SRC-004]` Vercel Functions Limitations: https://vercel.com/docs/functions/limitations
- `[SRC-005]` Neon serverless driver: https://neon.com/docs/serverless/serverless-driver + Survive thousands of connections: https://neon.com/blog/survive-thousands-connections
- `[SRC-006]` AWS — Lambda Reserved Concurrency: https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html
- `[SRC-007]` OpenTelemetry: https://opentelemetry.io/
- `[SRC-008]` Stripe — idempotency: https://stripe.com/blog/idempotency
- `[SRC-009]` Cloudflare Durable Objects: https://blog.cloudflare.com/introducing-workers-durable-objects/
- `[SRC-010]` Hono framework: https://hono.dev/ + sst: https://sst.dev/
- `[SRC-011]` Cloudflare Durable Objects (stateful primitive)
- `[SRC-012]` TechPlained — Serverless vs Containers (2026): https://www.techplained.com/serverless-vs-containers
- `[SRC-013]` Fowler — MonolithFirst: https://martinfowler.com/bliki/MonolithFirst.html

## Change log

| Version | Date | Author | Description |
|---|---|---|---|
| 1.0.0 | 2026-04-30 | Team | Initial — from Deep-mode research, Agent B (Serverless / FaaS / Edge). |
