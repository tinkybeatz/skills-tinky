# Standard: Pattern — Modular Monolith

- **Status:** Active
- **Version:** 1.0.0
- **Owner:** Engineering Lead
- **Effective date:** 2026-04-30

## Scope

Every project that has adopted the **modular monolith** pattern (the default per `decision-framework.md` ARC-DEC-01).

A modular monolith = a single deployable artifact, organized into **modules with explicit boundaries** (packages, namespaces, DB schemas) with import rules and internal APIs — as opposed to the "ball-of-mud monolith" and to distributed microservices.

## Core decisions

- **Containerized platform**: ECS Fargate / Cloud Run for deployment (`hybrid.md` ARC-OPS-XX).
- **Async workers**: BullMQ (Node task queues) or NATS JetStream, separate from the HTTP process (`patterns/hybrid.md`).

---

## Landmark references, 2026

- **Shopify Core**: ~2.8M LoC Ruby, 500k commits, Black Friday 2024 = 173 billion requests, peak 284M req/min `[SRC-001]`.
- **GitHub.com**: Rails monolith ~2M LoC, 1000+ engineers, 20 deploys/day `[SRC-002]`.
- **Stripe**: ~15M LoC Ruby + Sorbet, monolith maintained up to >3000 engineers `[SRC-003]`.
- **Basecamp / DHH**: "The Majestic Monolith" (2016), "The Citadel" (2020) `[SRC-004]`.
- **Richardson 2024**: "Modular monolith patterns for fast flow" `[SRC-005]`.

---

## Normative rules

### ARC-MM-01 — Default on projects < 10 devs

**Requirement:** Every new client project < 10 devs MUST start as a modular monolith unless a written justification to the contrary (ADR + the 5 "pro" signals in `decision-framework.md` ARC-DEC-02). `[SRC-005]` `[SRC-006]`

**Rationale:** a corollary of ARC-DEC-01 applied to the typical team size (agency + freelancers).

**Enforcement:** initial architecture review.

### ARC-MM-02 — Automated boundary enforcement in CI

**Requirement:** Boundaries between modules MUST be enforced by automated tooling in CI from commit zero. Human discipline alone is forbidden. Allowed tooling by stack: `[SRC-001]` `[SRC-007]`

| Stack | Tool |
|---|---|
| Ruby | [Packwerk](https://github.com/Shopify/packwerk) with `enforce_privacy: true` + `enforce_dependencies: true` |
| TypeScript / JS | [eslint-plugin-boundaries](https://github.com/javierbrea/eslint-plugin-boundaries), [dependency-cruiser](https://github.com/sverweij/dependency-cruiser), [Nx enforce-module-boundaries](https://nx.dev/docs/features/enforce-module-boundaries) |
| Java | ArchUnit |
| Go | `internal/` packages |
| Python | [import-linter](https://github.com/seddonym/import-linter) |

**Rationale:** Shopify Packwerk retrospective: without tooling, architectural drift within 6 months. The boundary checker fails the build.

**Enforcement:** blocking CI step (lint check).

### ARC-MM-03 — Modules by bounded context, not technical layers

**Requirement:** Modules MUST be defined by **business bounded contexts** (Billing, Auth, Catalog, Inventory). Splitting by technical layers (`controllers/`, `services/`, `models/`) is forbidden. `[SRC-005]`

**Rationale:** technical splitting cuts across domains, which prevents any clean future extraction. Business splitting prefigures a future decomposition if needed.

**Enforcement:** initial architecture review + repo structure audit.

### ARC-MM-04 — Explicit public APIs per module

**Requirement:** Each module MUST expose an **explicit public API** via a single `index` / `facade` / `__init__.py` file. The rest of the module MUST be private (not importable from outside the module). `[SRC-001]`

**Rationale:** without a facade, any internal symbol becomes accessible and ends up referenced everywhere. The boundary linter verifies that cross-module imports go only through the facade.

**Enforcement:** custom lint (Packwerk `enforce_privacy`, eslint-plugin-boundaries `element-types`).

### ARC-MM-05 — Dedicated Postgres schemas per bounded context

**Requirement:** Each bounded context SHOULD have its own Postgres schema. Cross-context FKs SHOULD be forbidden. Cross-context consumption happens via the module's API or an in-process event. `[SRC-005]`

**Rationale:** a single schema with FKs everywhere = a future decomposition nightmare. Separate schemas on the same cluster = logical isolation without the operational cost of multiple clusters.

**Enforcement:** SQL migration review + custom lint (dependency-cruiser on cross-module model imports).

**Exceptions:** very small projects (<3 contexts, <6 month lifecycle) may share a schema as a documented transition.

### ARC-MM-06 — Strict static typing on dynamic languages

**Requirement:** On Ruby / Python / TypeScript, strict static typing SHOULD be mandatory from the start: `[SRC-003]`

| Language | Tool |
|---|---|
| Ruby | [Sorbet](https://sorbet.org/) (`# typed: true` minimum, `# typed: strict` target) or RBS |
| Python | [pyright](https://github.com/microsoft/pyright) (strict mode) or mypy strict |
| TypeScript | `strict: true` (see `_lang/typescript.md` TS-CFG-01) |

**Rationale:** Stripe explicitly justified Sorbet by the need to maintain a 15M LoC monolith. Without typing, refactoring is painful above 100k LoC.

**Enforcement:** blocking type-checker in CI.

### ARC-MM-07 — Inter-module communication via interfaces or in-process events

**Requirement:** When temporal coupling becomes heavy (a module waits on another), communication SHOULD go through an **in-process event bus** (internal pub/sub) rather than a direct call. `[SRC-005]`

**Rationale:** prefigures a later extraction (the in-process bus becomes an external broker). Decouples modules in terms of lifecycle.

**Enforcement:** architecture review on observed coupling cases.

### ARC-MM-08 — No unscoped shared mutable state

**Requirement:** Global singletons, process-wide caches not scoped by module, and `globals` MUST NOT be used. Every cache MUST be scoped by module or externalized (Redis). `[SRC-008]`

**Rationale:** unscoped shared mutable state creates invisible dependencies between modules — module A can break module B without touching its code.

**Enforcement:** code review + custom lint detecting global patterns.

### ARC-MM-09 — No microservices "by anticipation"

**Requirement:** Starting with microservices "to be ready" MUST NOT be a valid justification. The project MUST start as a modular monolith; service extraction follows `decision-framework.md` ARC-DEC-02 (5 "pro" signals required). `[SRC-006]` `[SRC-009]`

**Rationale:** Fowler, Newman, and Richardson converge: extract after you understand the boundaries, never before.

**Enforcement:** initial architecture review, rejection of a greenfield microservices ADR without the 5 signals.

### ARC-MM-10 — ADR before any service extraction

**Requirement:** Any extraction of a module into a separate service MUST have an ADR documenting: `[SRC-010]`
- The signal that justifies the extraction (measured differential scaling, incompatible runtime, dedicated team).
- The API contract of the new service.
- The coexistence plan during migration (Strangler Fig).
- The kill date of the code in the monolith.

**Rationale:** without an ADR + kill date, the two coexist forever (Strangler anti-pattern).

**Enforcement:** architecture review by Tech Lead.

---

## Common pitfalls

| Pitfall | Symptom | Mitigation |
|---|---|---|
| Human discipline without tooling | Architectural drift within 6 months | ARC-MM-02 (linter in CI) |
| Shared mutable state | Tests pass in isolation but break in suite | ARC-MM-08 (review + scoping) |
| Monolithic DB with FKs everywhere | Future decomposition impossible | ARC-MM-05 (schemas per context) |
| Modules by technical layers | Future extraction cuts across domains | ARC-MM-03 (business modules) |
| God-modules (Auth, User, Notifications) | Referenced everywhere, become a bottleneck | Split into sub-modules or extract |
| No typing on a dynamic language | Painful refactor above 100k LoC | ARC-MM-06 (Sorbet/pyright/TS strict) |

---

## Migration from a legacy "ball-of-mud monolith"

For an existing monolith without boundaries:

1. **Document the violations** (Packwerk `--add` mode, dependency-cruiser audit).
2. **Freeze new violations** (CI blocks additions, not existing ones).
3. **Reduce progressively** by bounded context: extract the simplest first.
4. **Ratchet**: with each reduction PR, tighten the threshold.
5. **Target**: zero violations in 6-12 months.

`[SRC-007]` (Shopify Packwerk technique).

---

## Enforcement summary

| Mechanism | Rules covered | Auto |
|---|---|---|
| Boundary linter in CI | ARC-MM-02, 04 | Yes |
| Type-checker in CI | ARC-MM-06 | Yes |
| Cross-schema import lint | ARC-MM-05 | Partial |
| Architecture review (ADR) | ARC-MM-01, 03, 09, 10 | Manual |
| Code review (PR) | ARC-MM-07, 08 | Manual |

## Sources

- `[SRC-001]` Shopify — Enforcing Modularity with Packwerk: https://shopify.engineering/enforcing-modularity-rails-apps-packwerk
- `[SRC-002]` Building GitHub with Ruby and Rails: https://github.blog/engineering/architecture-optimization/building-github-with-ruby-and-rails/
- `[SRC-003]` Why did Stripe build Sorbet? — Lethain: https://lethain.com/stripe-sorbet/
- `[SRC-004]` DHH — The Majestic Monolith: https://signalvnoise.com/svn3/the-majestic-monolith/
- `[SRC-005]` Richardson — Modular monolith patterns for fast flow (2024): https://microservices.io/post/architecture/2024/09/09/modular-monolith-patterns-for-fast-flow.html
- `[SRC-006]` Fowler — MonolithFirst: https://martinfowler.com/bliki/MonolithFirst.html
- `[SRC-007]` Shopify — Packwerk Retrospective: https://shopify.engineering/a-packwerk-retrospective
- `[SRC-008]` 12-factor app — VI Processes: https://12factor.net/processes
- `[SRC-009]` Newman — Monolith to Microservices: https://samnewman.io/books/monolith-to-microservices/
- `[SRC-010]` Fowler — StranglerFigApplication: https://martinfowler.com/bliki/StranglerFigApplication.html

## Change log

| Version | Date | Author | Description |
|---|---|---|---|
| 1.0.0 | 2026-04-30 | Team | Initial — from Deep-mode research, Agent B (Modular Monolith). |
