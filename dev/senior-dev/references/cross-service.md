# Cross-Service Development — Reference Guide

Read this file when the task spans 2+ services, when adding a new service,
or when reviewing inter-service communication.

---

## Table of contents

1. Coupling taxonomy (Newman)
2. The boundary test
3. Contract-first design
4. Header propagation patterns
5. Anti-pattern catalog
6. Solo-dev pragmatism guide
7. Sources

---

## 1. Coupling taxonomy

Sam Newman (Building Microservices, 2nd ed., 2021) identifies four types of coupling.
Only domain coupling is acceptable — the other three are defects.

| Type | Definition | Example | Severity |
|---|---|---|---|
| **Domain coupling** | Service A calls B because B owns a capability A needs | BFF calls support service to list tickets | Acceptable |
| **Implementation coupling** | Service A knows B's internal structure (DB schema, internal types) | Support service hardcodes BFF header names in business logic | Defect |
| **Temporal coupling** | Service A requires B to be available simultaneously | BFF waits for auth service response before serving any request | Defect (mitigate with circuit breaker) |
| **Deployment coupling** | Changing A forces coordinated deployment of B | Changing a shared enum requires deploying both services | Defect |

**The test:** "Can I deploy service A without touching service B?" If no, you have
coupling beyond domain coupling.

---

## 2. The boundary test

Before writing cross-service code, apply this checklist:

- [ ] **Contract defined first?** Is the API shape (request/response) documented
      or at least TypeScript-typed at the boundary before implementation begins?
- [ ] **Boundary extraction?** Does the downstream service extract context (user ID,
      role, email) from headers **once** in a middleware, or is `req.headers['x-...']`
      scattered throughout?
- [ ] **Independent deploy?** Can this change be deployed to one service without
      requiring a simultaneous deploy of the other?
- [ ] **Independent test?** Can each service be tested in isolation with mocked
      HTTP responses from the other?
- [ ] **Who owns authorization?** Is fine-grained access control in the service
      that owns the data, not in the gateway?

---

## 3. Contract-first design

### For REST APIs (synchronous)

Define the interface before implementing either side:

```typescript
// Contract: what the support service expects
// This lives at the service boundary (middleware/types), not deep in business logic
interface TicketListRequest {
  // Query params
  status?: "open" | "in_progress" | "waiting" | "resolved" | "closed";
  limit?: number;
}

interface TicketListContext {
  // Extracted from headers at boundary
  userEmail?: string;
  userRole?: string;
  isAdmin: boolean;
}
```

The key: both the producer and consumer agree on this shape. The producer
extracts raw headers into a typed `TicketListContext` once, at the boundary.
Business logic works with the typed object, never with raw headers.

### For headers (identity propagation)

The BFF injects, the downstream service defines its own interface:

```
BFF sends:           Downstream service defines:
x-user-id      →     RequestContext.userId
x-user-email   →     RequestContext.userEmail
x-user-role    →     RequestContext.userRole
x-request-id   →     RequestContext.requestId (infra, pass-through)
```

If the BFF renames a header, only the downstream service's boundary middleware
changes — not its business logic.

### What to share vs. what to duplicate

| OK to share | NOT OK to share |
|---|---|
| API spec (OpenAPI, TypeScript interface at boundary) | Internal domain types |
| Infra utilities (logging, tracing, HTTP client) | Business logic |
| Enum values defined in the contract | Enum values defined in a DB constraint |
| Error code conventions | Internal error handling |

---

## 4. Header propagation patterns

### Pattern: Extract at boundary

The downstream service reads headers once and creates an internal context:

```typescript
// middleware/requestContext.ts — runs once per request
function extractRequestContext(request: FastifyRequest): RequestContext {
  return {
    userId: (request.headers["x-user-id"] as string) ?? undefined,
    userEmail: (request.headers["x-user-email"] as string) ?? undefined,
    userRole: (request.headers["x-user-role"] as string) ?? undefined,
    requestId: (request.headers["x-request-id"] as string) ?? "unknown",
    isAdmin: ADMIN_ROLES.has(request.headers["x-user-role"] as string ?? ""),
  };
}

// Route handler — uses typed context, never raw headers
async function listTickets(ctx: RequestContext, filters: TicketFilters) {
  const where = ctx.isAdmin ? {} : { email: ctx.userEmail };
  // ...
}
```

### Anti-pattern: Headers in business logic

```typescript
// DON'T — this scatters BFF-specific knowledge throughout the service
async function listTickets(request) {
  const userEmail = request.headers["x-user-email"]; // coupling!
  const role = request.headers["x-user-role"];         // coupling!
  const isAdmin = role === "super_admin";              // coupling!
  // ...
}
```

### Correlation headers (infrastructure)

`x-request-id`, `x-trace-id`, `traceparent` (W3C Trace Context) are infrastructure
concerns. They SHOULD be propagated transparently by every service. They are not
domain data — they don't belong in a RequestContext type (or they go in a
separate InfraContext).

---

## 5. Anti-pattern catalog

### 5a. Distributed monolith

**Symptom:** Your CI/CD deploys 3 services atomically. Changing a feature
requires PRs in 2+ repos/directories.

**Fix:** Define contracts first. Each service evolves independently against
the contract. Break the atomic deployment — each service has its own pipeline.

### 5b. Shared database

**Symptom:** Two services query the same table.

**Fix:** Database per service. If service A needs data from service B, call B's API
or subscribe to B's events. Data duplication is acceptable — coupling is not.

### 5c. Chatty services

**Symptom:** The BFF makes 5 sequential calls to assemble one page.

**Fix:** API composition at the BFF (aggregate in one endpoint), or CQRS read
models that pre-join data. Also consider: does this need to be separate services?

### 5d. Leaking internals

**Symptom:** Service A knows that service B stores roles in a `role` column
with values `super_admin`, `franchise_admin`. If B renames a role, A breaks.

**Fix:** The contract defines the role vocabulary. Both services map to/from
their internal representations at the boundary.

### 5e. Shared domain types

**Symptom:** A `packages/shared/types.ts` file imported by both the BFF
and the support service. Changing a field requires updating both.

**Fix:** Each service defines its own types. The shared types are the
**contract types** defined in the API spec — not internal domain types.
If you must share, version the package strictly (semver).

---

## 6. Solo-dev pragmatism guide

You're one person building 4 services. Full Netflix-scale decoupling
is overkill. Here's the pragmatic hierarchy:

### What to enforce (cheap, high-value)

1. **Contract at the boundary.** Each service has a typed middleware that
   extracts context from headers. Business logic never reads raw headers.
   Cost: 20 minutes per service. Saves hours of debugging when headers change.

2. **Independent deployability.** Each service deploys on its own schedule.
   If deploying the BFF forces a support service redeploy, that's a bug.
   Cost: just discipline. Don't batch cross-service changes in one commit.

3. **Read the downstream contract before coding upstream.** Check what the
   API actually expects (see CLAUDE.md rule). Don't guess enum values.

### What to relax (expensive, low-value at this scale)

1. **Consumer-driven contract testing (Pact).** You're both the consumer and
   provider. Integration tests that hit real endpoints are simpler.

2. **Full event-driven architecture.** Synchronous HTTP with circuit breakers
   is easier to reason about for a solo dev. Use events only for truly async
   workflows (email, background jobs).

3. **Separate repos per service.** A monorepo with service directories is
   pragmatic. You get atomic commits when needed, shared CI config, and
   easy contract validation. Extract repos when you have multiple developers.

4. **API gateway as a separate product (Kong, Envoy).** Your BFF IS the
   gateway. That's fine at this scale.

### The "would I deploy this to Netflix?" filter

If you catch yourself building infrastructure that only makes sense at
1000x your scale, stop. Ask: "What's the simplest thing that works for
1-3 services with 1 developer?" That's your answer.

---

## 7. Sources

| Source | Author | Type |
|---|---|---|
| Building Microservices (2nd ed.) | Sam Newman, O'Reilly 2021 | Book (industry standard) |
| Microservices Patterns | Chris Richardson, Manning 2018 | Book (industry standard) |
| "Microservices" article | Fowler & Lewis, 2014 | Blog (de facto standard) |
| "Monolith First" | Martin Fowler, 2015 | Blog (authoritative) |
| Release It! (2nd ed.) | Michael Nygard, Pragmatic 2018 | Book (stability patterns) |
| Learning Domain-Driven Design | Vladik Khononov, O'Reilly 2021 | Book (bounded contexts) |
| Consumer-Driven Contracts | Ian Robinson, 2006 | Paper/pattern |
| BFF pattern | Phil Calcado, SoundCloud 2015 | Blog (pattern origin) |
| OpenAPI Specification | Linux Foundation | Open standard |
