# Standard: TypeScript — Language

- **Status:** Active
- **Version:** 2.0.0
- **Owner:** Engineering Lead
- **Approvers:** Tech Lead
- **Effective date:** 2026-04-30
- **Last review date:** 2026-04-30

## Scope

Every `.ts` / `.tsx` file in a project (frontend, backend, scripts, tooling).
Out of scope: framework-specific rules (detailed React 19 patterns, Vite/Next configs) → `std/<project>/`.

## Core decisions (not up for debate)

1. **ESLint** flat config + `typescript-eslint` v8 = default. Biome forbidden (TS-AP-15).
2. **`throw` + global middleware** = standard error handling. No standardized Result/Either.
3. **No ORM** (TS-AP-14). Raw SQL + `Kysely` if a pure query builder is needed.

---

## Normative rules — MUST

### TS-CFG-01 — TSConfig extends `@tsconfig/strictest`

**Requirement:** `tsconfig.json` MUST include `"extends": "@tsconfig/strictest"` (enables `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, `noUnusedLocals/Parameters`, `isolatedModules`, `skipLibCheck`). `[SRC-001]`
**Rationale:** a maintained upstream rather than an in-house config that drifts. All future TS strict-mode options are auto-inherited.
**Enforcement:** tsconfig review + `tsc --noEmit` in CI.
**Exceptions:** none on a new project. Legacy project migration: 90 days max.

### TS-CFG-02 — `verbatimModuleSyntax: true` everywhere

**Requirement:** `verbatimModuleSyntax: true` MUST be enabled. `importsNotUsedAsValues` is forbidden (removed in TS 5.5). `[SRC-002]`
**Rationale:** full predictability of the JS output, eliminates CJS/ESM dual-emit bugs, consistent with Node strip-types.
**Enforcement:** config lint + review.

### TS-CFG-03 — `target: ES2022` minimum

**Requirement:** `compilerOptions.target` MUST be `"ES2022"` or newer. `[SRC-003]`
**Rationale:** eliminates the `__awaiter`, `__extends`, `__assign`, regenerator helpers. All relevant 2026 runtimes (Node 20+, Safari 16+, Chrome 100+) support ES2022.
**Enforcement:** tsconfig review.

### TS-CFG-04 — `moduleResolution: "bundler"` forbidden for published libs

**Requirement:** Libraries published to npm MUST use `module: "node18"` (or newer) + `moduleResolution: "node18"` (or newer). `bundler` is *infectious* and produces code that only works in bundlers. `[SRC-004]`
**Rationale:** native Node consumers would not be able to import the lib.
**Enforcement:** review + import test in the CI release.

### TS-VAL-01 — Runtime validation at external boundaries

**Requirement:** Every external boundary (HTTP body, query params, env vars, message bus, FS, untyped DB output) MUST be validated via a Standard Schema-compatible schema (Zod / Valibot / ArkType). `[SRC-005]`
**Rationale:** TS has total type erasure — no check survives at runtime. No validation = a silent runtime bug.
**Enforcement:** mandatory review on every HTTP handler, env loader, message consumer.

### TS-VAL-02 — Env vars via `@t3-oss/env-core`

**Requirement:** Loading env vars MUST go through `@t3-oss/env-core` (server/client separation, leak prevention via Proxy). `[SRC-006]`
**Rationale:** prevents server-side env leaks into client bundles, forces explicit validation at boot.
**Enforcement:** review + grep for direct `process.env` (warn).

### TS-LINT-01 — ESLint flat config mandatory

**Requirement:** Every project MUST use ESLint flat config (`eslint.config.js` / `.mjs`). The legacy `.eslintrc.*` is forbidden (will be removed in ESLint v10). `[SRC-007]`
**Rationale:** long-term official support; the `tseslint.config()` helper has been available since typescript-eslint v8.
**Enforcement:** presence of the file verified in CI (lint step).

### TS-LINT-02 — Minimal `typescript-eslint` preset

**Requirement:** The ESLint config MUST include at minimum the `recommended-type-checked` + `stylistic` presets. `[SRC-008]`
**Rationale:** covers the core type-aware rules (`no-floating-promises`, `no-misused-promises`, etc.).
**Enforcement:** ESLint config review.

### TS-LINT-03 — Non-negotiable rules at `error`

**Requirement:** The following rules MUST be at `error`: `no-floating-promises`, `no-misused-promises`, `switch-exhaustiveness-check`, `ban-ts-comment`, `no-explicit-any`, `consistent-type-imports`, `no-unnecessary-type-assertion`. `[SRC-008]`
**Rationale:** these rules catch production bugs (a forgotten promise, an incomplete switch, a superfluous cast).
**Enforcement:** blocking lint in CI.

### TS-CI-01 — `tsc --noEmit` blocking in CI

**Requirement:** The CI pipeline MUST run `tsc --noEmit` (with `--incremental` + `tsBuildInfoFile` cache) in parallel with the build. An error = merge blocked. `[SRC-009]`
**Rationale:** only `tsc` validates types; esbuild/SWC/Vite do single-file transpilation without type-checking.
**Enforcement:** blocking GitHub Actions / GitLab CI step.

### TS-CI-02 — `type-coverage --at-least 99 --strict`

**Requirement:** The CI pipeline MUST run `type-coverage --at-least 99 --strict`. `[SRC-010]`
**Rationale:** measures the % of typed identifiers (non-`any`). The 99% threshold tolerates justified `any` at boundaries.
**Enforcement:** blocking CI step.
**Exceptions:** legacy project in migration: temporary 90% threshold, renewable for 90 days.

### TS-CI-03 — Pre-commit + pre-push hooks

**Requirement:** The repo MUST configure husky + lint-staged. Pre-commit = ESLint on staged files. Pre-push = `tsc --noEmit` on the full project. `[SRC-011]`
**Rationale:** catches errors before push, without slowing down the commit.
**Enforcement:** presence of `.husky/` + `lint-staged` in `package.json`.

### TS-REACT-01 — `forwardRef` prohibited on React ≥ 19

**Requirement:** On React ≥ 19, `ref` MUST be declared as a normal prop; `forwardRef` is forbidden (deprecated). Migrate existing code via codemod. `[SRC-012]`
**Rationale:** the official React 19 API; `forwardRef` adds needless indirection.
**Enforcement:** custom lint + review.

### TS-REACT-02 — Serializable server→client props (RSC)

**Requirement:** Any prop crossing the server→client boundary (React Server Components) MUST be strictly serializable. No functions, classes, instances, or non-serialized Dates. `[SRC-013]`
**Rationale:** the technical contract of RSC; a violation = an opaque runtime error.
**Enforcement:** review + lint `@next/no-async-client-component` or equivalent.

### TS-DI-01 — Manual DI by default

**Requirement:** On a project < 50 services, dependency injection MUST be done via manual constructor. `tsyringe`/`awilix` allowed beyond 50 services. NestJS only if the whole app is NestJS. `[SRC-014]`
**Rationale:** readability, no magic, no superfluous `__decorate` helpers.
**Enforcement:** initial architecture review.

---

## Normative rules — SHOULD

### TS-PAT-01 — `unknown` at boundaries + type guards
**Requirement:** Any externally sourced data SHOULD be typed `unknown` then narrowed via a user-defined `is` type guard. `[SRC-015]`
**Enforcement:** review + lint `no-explicit-any`.

### TS-PAT-02 — Discriminated unions + exhaustiveness check
**Requirement:** Model states/variants via discriminated unions; end each `switch` with `const _: never = x;` (or `assertNever(x)`). `[SRC-016]`
**Enforcement:** lint `switch-exhaustiveness-check`.

### TS-PAT-03 — Branded types for primitive IDs
**Requirement:** Every primitive ID shared between domains (`UserId`, `OrgId`, `Email`) SHOULD be a branded type. Prefer `type-fest` `Tagged<>`. `[SRC-017]`
**Rationale:** avoids passing an `OrderId` where a `UserId` is expected. Zero runtime cost.

### TS-PAT-04 — Systematic `import type { ... }`
**Requirement:** Type-only imports SHOULD use `import type`. `[SRC-008]`
**Enforcement:** lint `consistent-type-imports: error`.

### TS-PAT-05 — `#field` rather than the `private` keyword
**Requirement:** On target ES2022+, private fields SHOULD use the ECMA `#field` syntax rather than the TS `private` keyword. `[SRC-018]`
**Rationale:** true runtime privacy, ECMA alignment, no perf difference on a modern target.

### TS-PERF-01 — Full initialization in the constructor (V8 shape)
**Requirement:** All properties of an object/class SHOULD be initialized in the constructor. NEVER `delete obj.x` on a hot path. `[SRC-019]`
**Rationale:** maintains a stable V8 hidden class; late mutation or `delete` breaks optimizations.

### TS-CFG-05 — `erasableSyntaxOnly` for Node strip-types
**Requirement:** If the project targets Node `--experimental-strip-types`, `erasableSyntaxOnly: true` SHOULD be enabled. `[SRC-020]`
**Rationale:** forbids `enum`, runtime `namespace`, parameter properties, `import =` — exactly the incompatible constructs.

### TS-CFG-06 — Project references from 5+ packages
**Requirement:** Monorepos with ≥ 5 typed packages SHOULD use project references (`composite: true`) + `tsc --build`. `[SRC-021]`
**Rationale:** incremental type-checking, topological ordering, `tsBuildInfoFile` cache.

### TS-CFG-07 — `skipLibCheck` by role
**Requirement:** `skipLibCheck: true` SHOULD be enabled on apps. `false` SHOULD be enforced in the CI release for published libs. `[SRC-022]`
**Rationale:** ~2-3× gain on heavy projects; published libs must guarantee cross-typings consistency.

### TS-VAL-03 — Validator choice by context
**Requirement:** Valibot SHOULD be preferred for validators shipped to the browser/edge (~1.37 kB vs ~17 kB Zod). Zod v4 for a standard Node backend. ArkType / TypeBox on measured hot paths (3-4× faster). `[SRC-023]`

### TS-ERR-01 — `throw` + global middleware as the default
**Requirement:** Business errors SHOULD propagate via `throw`; a global middleware handler (Express/Fastify/Hono) catches them and formats the response. No standardized Result/Either. `[SRC-024]`
**Rationale:** simplicity, varied projects, non-FP-aligned teams. A Result type is allowed locally in shared libs if justified.

### TS-DB-01 — Raw SQL, no ORM
**Requirement:** DB access SHOULD use native drivers (`pg`, `postgres-js`, `mysql2`, `better-sqlite3`) + manual types. `Kysely` allowed if a pure query builder is needed. `[SRC-025]`
**Rationale:** a team decision — ORMs (Prisma, Drizzle, TypeORM) are forbidden (TS-AP-14).

### TS-REACT-03 — TanStack Query v5 + `queryOptions()`
**Requirement:** Server state SHOULD be managed by TanStack Query v5; queries SHOULD be declared via the `queryOptions()` helper for typed queryKey/queryFn sharing. `[SRC-026]`

### TS-REACT-04 — `cva` + `tailwind-merge` + Radix `asChild`
**Requirement:** Component variants SHOULD use `cva` (`class-variance-authority`) + `tailwind-merge`. The polymorphic pattern SHOULD use `asChild` (Radix Slot) rather than an `as` prop. `[SRC-027]`

### TS-TOOL-01 — `ts-reset` in application code only
**Requirement:** `ts-reset` SHOULD be installed in all application code. It MUST NOT be included in a shared lib (pollutes consumers). `[SRC-028]`

### TS-TOOL-02 — `type-fest` as the canonical source
**Requirement:** Utility types SHOULD come from `type-fest` rather than being reinvented locally. `[SRC-017]`

---

## Anti-patterns — MUST NOT

| ID | Rule | Enforcement | Source |
|---|---|---|---|
| TS-AP-01 | Explicit `any` (except a justified `// eslint-disable-next-line` + comment) | lint `no-explicit-any: error` | `[SRC-008]` |
| TS-AP-02 | `enum` (numeric or string) — prefer `as const` + `typeof X[keyof typeof X]` | lint `no-restricted-syntax` | `[SRC-029]` |
| TS-AP-03 | `const enum` (incompatible with `isolatedModules`) | lint `no-restricted-syntax` | `[SRC-030]` |
| TS-AP-04 | `namespace Foo {}` (except `declare namespace` for third-party ambient typings) | lint `no-namespace` | `[SRC-031]` |
| TS-AP-05 | `// @ts-ignore` (use `// @ts-expect-error` with a description) | lint `ban-ts-comment: error` | `[SRC-008]` |
| TS-AP-06 | `experimentalDecorators` + `emitDecoratorMetadata` on new code (except NestJS/TypeORM legacy) | tsconfig review | `[SRC-032]` |
| TS-AP-07 | Types `Object`, `Function`, `{}` (use `Record<string, unknown>` or a precise signature) | lint `no-restricted-types` | `[SRC-029]` |
| TS-AP-08 | `as Foo` to bypass an error; `!` non-null without a proven invariant | review | `[SRC-029]` |
| TS-AP-09 | I-prefix on interfaces (`IUser`) | review + custom lint | `[SRC-029]` |
| TS-AP-10 | `delete obj.x` on a hot path (breaks the V8 hidden class) | review | `[SRC-019]` |
| TS-AP-11 | Stitches or styled-components on new projects (deprecated/maintenance mode) | architecture review | `[SRC-033]` |
| TS-AP-12 | `tsgo` / typescript-go (TS 7 preview) in prod until GA is announced | build review | `[SRC-034]` |
| TS-AP-13 | Node `--strip-types` in a production build without a prior `tsc --noEmit` | CI review | `[SRC-020]` |
| TS-AP-14 | ORM (Prisma, Drizzle, TypeORM, Sequelize, MikroORM) | architecture review | Team decision |
| TS-AP-15 | Biome — use ESLint flat config + typescript-eslint v8 | tooling review | Team decision |

---

## Enforcement summary

| Mechanism | Rules covered | Auto |
|---|---|---|
| `tsc --noEmit` CI | TS-CFG-01..07, TS-CI-01 | Yes |
| `type-coverage` CI | TS-CI-02 | Yes |
| ESLint (flat config + typescript-eslint v8) | TS-LINT-01..03, TS-PAT-04, TS-AP-01, 02, 03, 04, 05, 07 | Yes |
| Husky + lint-staged hooks | TS-CI-03 | Yes |
| Architecture review | TS-DI-01, TS-DB-01, TS-AP-11, 14, 15 | Manual |
| Code review (PR) | TS-PAT-01..03, 05, TS-PERF-01, TS-AP-06, 08, 09, 10, 12, 13 | Manual |

## Exceptions process

- Max 90 days, renewable once with written justification.
- Approved by Tech Lead.
- Recorded in an inline comment (`// EXCEPTION TS-XX-YY: <reason> — expires 2026-MM-DD`) or an ADR if cross-cutting.
- Legacy projects in migration: degraded thresholds allowed on TS-CI-02 (type-coverage) — 90% for 90 days.

## Metrics

| Metric | Baseline | Target | Measurement |
|---|---|---|---|
| `any` count in the codebase | — | < 1% | `type-coverage --strict` |
| TS errors in CI | 0 | 0 | `tsc --noEmit` exit code |
| Type coverage | — | ≥ 99% | `type-coverage --at-least 99` |
| Unhandled promises | — | 0 | lint `no-floating-promises` |

## Sources

- `[SRC-001]` @tsconfig/strictest — https://www.npmjs.com/package/@tsconfig/strictest
- `[SRC-002]` TypeScript 5.0 release notes (verbatimModuleSyntax) — https://devblogs.microsoft.com/typescript/announcing-typescript-5-0/
- `[SRC-003]` Why increase your tsconfig target — https://www.learningtypescript.com/articles/why-increase-your-tsconfig-target
- `[SRC-004]` TS Choosing Compiler Options — https://www.typescriptlang.org/docs/handbook/modules/guides/choosing-compiler-options.html
- `[SRC-005]` TS Handbook (type erasure) — https://www.typescriptlang.org/docs/handbook/
- `[SRC-006]` t3-env docs — https://env.t3.gg/docs/core
- `[SRC-007]` ESLint v9 migration guide — https://eslint.org/docs/latest/use/configure/migration-guide
- `[SRC-008]` typescript-eslint configs & rules — https://typescript-eslint.io/users/configs/
- `[SRC-009]` esbuild caveats (no type-check) — https://esbuild.github.io/content-types/#typescript-caveats
- `[SRC-010]` type-coverage — https://github.com/plantain-00/type-coverage
- `[SRC-011]` husky — https://typicode.github.io/husky/
- `[SRC-012]` React 19 forwardRef deprecation — https://react.dev/reference/react/forwardRef
- `[SRC-013]` React Server Components — https://react.dev/reference/rsc/server-components
- `[SRC-014]` tsyringe — https://github.com/microsoft/tsyringe
- `[SRC-015]` TS Narrowing handbook — https://www.typescriptlang.org/docs/handbook/2/narrowing.html
- `[SRC-016]` Fullstory exhaustiveness checking — https://www.fullstory.com/blog/discriminated-unions-and-exhaustiveness-checking-in-typescript/
- `[SRC-017]` type-fest — https://github.com/sindresorhus/type-fest
- `[SRC-018]` puruvj — `private` vs `#` perf — https://www.puruvj.dev/blog/js-class-private-vs-ts-private
- `[SRC-019]` Mathias Bynens — Shapes & ICs — https://mathiasbynens.be/notes/shapes-ics
- `[SRC-020]` TS 5.8 release notes (erasableSyntaxOnly) — https://devblogs.microsoft.com/typescript/announcing-typescript-5-8/
- `[SRC-021]` TS Project References — https://www.typescriptlang.org/docs/handbook/project-references.html
- `[SRC-022]` TSConfig skipLibCheck — https://www.typescriptlang.org/tsconfig/skipLibCheck.html
- `[SRC-023]` PkgPulse Valibot vs Zod v4 (2026) — https://www.pkgpulse.com/guides/valibot-vs-zod-v4-typescript-validator-2026
- `[SRC-024]` Team decision (2026-04-30) — no standardized Result/Either
- `[SRC-025]` Team decision (2026-04-30) — no ORM
- `[SRC-026]` tkdodo — query options API — https://tkdodo.eu/blog/the-query-options-api
- `[SRC-027]` cva docs — https://cva.style/docs
- `[SRC-028]` ts-reset — https://www.totaltypescript.com/ts-reset
- `[SRC-029]` Google TS Style Guide — https://google.github.io/styleguide/tsguide.html
- `[SRC-030]` TS Issue #41641 (deprecate const enum) — https://github.com/microsoft/TypeScript/issues/41641
- `[SRC-031]` typescript-eslint no-namespace — https://typescript-eslint.io/rules/no-namespace/
- `[SRC-032]` TS 5.0 decorators — https://devblogs.microsoft.com/typescript/announcing-typescript-5-0/
- `[SRC-033]` Stitches archived / styled-components maintenance mode — https://github.com/stitchesjs/stitches
- `[SRC-034]` TS 7 progress Dec 2025 — https://devblogs.microsoft.com/typescript/progress-on-typescript-7-december-2025/

## Change log

| Version | Date | Author | Description |
|---|---|---|---|
| 2.0.0 | 2026-04-30 | Team | Full rewrite from Deep-mode research (4 parallel agents, 35+ primary sources) + internal decisions (no-ORM, ESLint locked, throw + global middleware). 46 ID-tracked rules (15 MUST, 16 SHOULD, 15 MUST NOT). |
| 1.0.0 | 2026-04-30 | Team | Initial — 5 universal MUST + 5 SHOULD language rules (before in-depth research). |
