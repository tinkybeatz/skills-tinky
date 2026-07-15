# ADR Writer — Examples

Calibration examples for tone, depth, and format.

---

## Example A — Classic technical decision (default template)

```markdown
# ADR-0003: Use PostgreSQL as primary event store

**Date:** 2025-06-15
**Status:** accepted
**Confidence:** high
**Deciders:** Backend team

## Context

Our application needs to persist domain events for audit trail and event
replay capabilities. The current system stores events as JSON blobs in
MongoDB, which causes issues with querying historical events and enforcing
schema consistency. We process approximately 50k events/day with peaks
at 200k during month-end reconciliation.

The team has strong PostgreSQL expertise but limited MongoDB operational
experience. Our infrastructure already runs managed PostgreSQL instances
on our hosting provider.

## Decision Drivers

- Query flexibility for historical event analysis
- Schema enforcement and data integrity
- Team expertise and operational confidence
- Cost of infrastructure change

## Considered Options

1. **Keep MongoDB** — continue with current setup, add indexes for query perf
2. **Migrate to PostgreSQL with JSONB** — store events in PG using JSONB columns
3. **Dedicated event store (EventStoreDB)** — purpose-built solution

## Decision

We will migrate the event store to PostgreSQL using JSONB columns for
event payloads with a typed events table schema.

PostgreSQL gives us the query flexibility we need for historical analysis
while leveraging existing team expertise and infrastructure. The JSONB
approach preserves schema flexibility for event payloads while the
surrounding table enforces consistency on metadata (event type, timestamp,
aggregate ID, version).

EventStoreDB was rejected because the operational overhead of a new
database technology outweighs its benefits at our current scale.

## Consequences

### Positive

- Team can use familiar SQL tooling for event queries and analytics
- Existing monitoring, backup, and HA setup extends to the event store
- JSONB indexing enables efficient queries on event payload fields

### Negative

- Migration requires careful data transfer with zero-downtime strategy
- PostgreSQL is not optimized for append-only workloads like EventStoreDB
- JSONB queries are slower than native document queries for deeply nested data

### Neutral

- At 50k events/day, both PostgreSQL and MongoDB handle the load comfortably
- We accept the trade-off of less specialized tooling for operational simplicity

## Links

- RFC-0012: Event store migration plan
- ADR-0001: Use Architecture Decision Records
```

---

## Example B — Superseded decision (Supersede mode)

```markdown
# ADR-0007: Switch from REST to gRPC for inter-service communication

**Date:** 2025-09-20
**Status:** accepted
**Confidence:** medium
**Deciders:** Platform team

## Context

ADR-0004 established REST as the inter-service protocol. Since then,
the number of internal services grew from 3 to 8, and latency-sensitive
paths now chain 4+ service calls. JSON serialization overhead and lack
of streaming support are measurable bottlenecks (p99 latency increased
from 120ms to 340ms over 6 months).

External-facing APIs remain REST — this decision concerns internal
service-to-service communication only.

## Decision Drivers

- p99 latency reduction on critical paths
- Type safety across service boundaries
- Streaming support for real-time data flows
- Migration cost and team learning curve

## Considered Options

1. **Optimize existing REST** — compression, connection pooling, caching
2. **gRPC for internal services** — protobuf serialization, HTTP/2
3. **GraphQL federation** — unified graph for inter-service queries

## Decision

We will adopt gRPC with Protocol Buffers for all new inter-service
communication, and progressively migrate existing REST internal endpoints.

The protobuf schema provides compile-time type safety across services.
HTTP/2 multiplexing and binary serialization address the latency concerns
directly. GraphQL was rejected because it solves a different problem
(flexible client queries) and adds complexity without addressing serialization
performance.

## Consequences

### Positive

- Binary serialization reduces payload size by ~60% vs JSON
- HTTP/2 streaming enables real-time data flows without WebSocket workarounds
- Proto files serve as living API contracts with backward compatibility rules

### Negative

- Team needs to learn protobuf schema design and gRPC patterns
- Debugging is harder — binary payloads are not human-readable without tooling
- Dual protocol support during migration adds temporary complexity

### Neutral

- External APIs stay REST — no client-facing changes

## Links

- Supersedes: ADR-0004 (status updated to "superseded by ADR-0007")
- Benchmark results: docs/benchmarks/rest-vs-grpc-2025-09.md
```

---

## Example C — Backfill of an implicit decision

```markdown
# ADR-0010: Use Tailwind CSS as the primary styling approach

**Date:** 2025-11-01
**Status:** accepted
**Confidence:** high
**Deciders:** Frontend team

## Context

This ADR backfills a decision made in March 2025 when the frontend
project was initialized. Tailwind CSS was adopted without formal
documentation. New team members have asked why we use utility classes
instead of CSS modules or styled-components, and some PRs introduced
inconsistent styling approaches.

Documenting this decision now to establish clarity and prevent drift.

## Decision Drivers

- Consistency across the frontend codebase
- Speed of development for UI components
- Design system alignment (tokens map to Tailwind config)
- Bundle size and performance

## Considered Options

1. **Tailwind CSS** — utility-first, configured with design tokens
2. **CSS Modules** — scoped CSS per component
3. **styled-components** — CSS-in-JS with runtime

## Decision

We will use Tailwind CSS as the sole styling approach for all frontend
components. Custom CSS is only permitted for animations and third-party
component overrides, and must be placed in dedicated files.

## Consequences

### Positive

- Single consistent approach across all components
- Design tokens defined once in tailwind.config.js
- No runtime CSS overhead — styles are purged at build time

### Negative

- Long class strings can reduce template readability
- Learning curve for developers unfamiliar with utility-first CSS

### Neutral

- Decision was already de facto in place — this ADR formalizes it

## Links

- Original project setup: commit abc123 (March 2025)
- ADR-0001: Use Architecture Decision Records
```
