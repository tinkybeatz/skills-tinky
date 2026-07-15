# Standard: TypeScript Configuration & Typing — Sapain Borne

- Status: Active
- Version: 1.0.0
- Owner: Engineering Lead
- Approvers: Tech Lead
- Effective date: 2026-04-06
- Last review date: 2026-04-06

## Scope

All React+TypeScript projects in the sapain-borne monorepo: `services/back-office/`, future frontend services.

Out of scope: Node.js backend services (they have their own CommonJS tsconfig).

## Normative rules

### R-TS-01 Strict mode mandatory

Requirement:
- tsconfig.json MUST include `"strict": true` `[SRC-001]`
- `"noUncheckedIndexedAccess"` MUST be `true` `[SRC-002]`
- `"noFallthroughCasesInSwitch"` MUST be `true`
- `"noImplicitOverride"` MUST be `true`

Rationale:
- `strict: true` enables `strictNullChecks`, `noImplicitAny`, etc. — eliminates entire categories of runtime errors at compile-time
- `noUncheckedIndexedAccess` forces handling of `T | undefined` on array access, avoiding `TypeError` in production

Enforcement:
- CI: `tsc --noEmit` in the pipeline (blocking)
- Review: verify that the options are not disabled individually

Exceptions:
- None. Strict mode is non-negotiable.

---

### R-TS-02 Bundler module resolution

Requirement:
- `"moduleResolution"` MUST be `"Bundler"` for Vite projects `[SRC-003]`
- `"module"` MUST be `"ESNext"`
- `"isolatedModules"` MUST be `true` (required by esbuild/SWC)
- `"verbatimModuleSyntax"` SHOULD be `true` `[SRC-003]`

Rationale:
- `"Bundler"` (TS 5.0+) matches Vite's actual resolution — other modes force workarounds
- `verbatimModuleSyntax` enforces `import type { Foo }`, guaranteeing correct tree-shaking

Enforcement:
- CI: `tsc --noEmit` validates the config
- Review: verify tsconfig/vite.config consistency

Exceptions:
- None for Vite projects.

---

### R-TS-03 Explicit type imports

Requirement:
- Type imports MUST use `import type { ... }` `[SRC-003]`
- ESLint MUST enforce `@typescript-eslint/consistent-type-imports` at `error` `[SRC-004]`

Rationale:
- Guarantees correct erasure by esbuild/SWC — produces smaller bundles
- Makes explicit what is runtime vs compile-time

Enforcement:
- ESLint rule `@typescript-eslint/consistent-type-imports: error` (automatic)
- CI: blocking lint

Exceptions:
- None.

---

### R-TS-04 Path aliases

Requirement:
- Projects MUST use the `@/*` alias for `src/*` `[SRC-005]`
- Aliases MUST be mirrored in `vite.config.ts` via `resolve.alias` or `vite-tsconfig-paths`
- Relative imports going up more than 2 levels (`../../../`) SHOULD use the `@/` alias

Rationale:
- Readability: `@/shared/api/client` vs `../../../shared/api/client`
- Consistency between TypeScript and the bundler

Enforcement:
- Review: flag relative imports > 2 levels
- The build fails if the alias is not configured on both sides

Exceptions:
- Relative imports in the same folder or direct parent allowed.

---

### R-TS-05 No explicit any

Requirement:
- `any` SHOULD NOT be used in application code `[SRC-001]`
- ESLint MUST configure `@typescript-eslint/no-explicit-any: warn`
- Any remaining `any` MUST have a `// eslint-disable-next-line` comment with justification

Rationale:
- `any` disables type-checking and propagates silently through the codebase

Enforcement:
- ESLint rule `@typescript-eslint/no-explicit-any: warn`
- Review: every lint suppression must be justified

Exceptions:
- Interop code with untyped libraries (with a comment).

---

## Enforcement summary

| Rule | Mechanism | Automated |
|---|---|---|
| R-TS-01 | `tsc --noEmit` CI | Yes |
| R-TS-02 | `tsc --noEmit` CI | Yes |
| R-TS-03 | ESLint `consistent-type-imports` | Yes |
| R-TS-04 | Build failure + review | Partial |
| R-TS-05 | ESLint `no-explicit-any` | Yes |

## Exceptions process

- Max 90 days, renewable with justification
- Approved by Tech Lead
- Recorded in an inline comment with an expiration date

## Metrics

| Metric | Baseline | Target | Measurement |
|---|---|---|---|
| `any` count in the codebase | — | <5 | `grep -r "any" --include="*.ts" --include="*.tsx"` |
| TypeScript errors in CI | 0 | 0 | `tsc --noEmit` exit code |

## Sources

- SRC-001 | TypeScript Handbook — strict mode | https://www.typescriptlang.org/tsconfig#strict | Microsoft | 2024 | Official reference
- SRC-002 | TypeScript Handbook — noUncheckedIndexedAccess | https://www.typescriptlang.org/tsconfig#noUncheckedIndexedAccess | Microsoft | 2024 | Prevents undefined access
- SRC-003 | TypeScript 5.0 Release Notes | https://devblogs.microsoft.com/typescript/announcing-typescript-5-0/ | Microsoft | 2023 | moduleResolution Bundler, verbatimModuleSyntax
- SRC-004 | typescript-eslint consistent-type-imports | https://typescript-eslint.io/rules/consistent-type-imports/ | typescript-eslint | 2024 | Rule documentation
- SRC-005 | Vite docs — TypeScript | https://vitejs.dev/guide/features.html#typescript | Vite | 2024 | Path aliases config

## Change log

| Version | Date | Author | Description |
|---|---|---|---|
| 1.0.0 | 2026-04-06 | Claude Code | Initial standard from React+TS research report |
