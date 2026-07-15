# Standard: Architecture, Testing & Tooling — Sapain Borne

- Status: Active
- Version: 1.0.0
- Owner: Engineering Lead
- Approvers: Tech Lead
- Effective date: 2026-04-06
- Last review date: 2026-04-06

## Scope

Frontend architecture, testing, and tooling in the sapain-borne monorepo.

## Normative rules

---

## Architecture

### R-ARCH-01 Feature-Sliced Design (FSD)

Requirement:
- Frontend code MUST follow the FSD 6-layer structure: `app → pages → widgets → features → entities → shared` `[SRC-001]`
- Each layer MUST import only lower layers (unidirectional imports) `[SRC-001]`
- `eslint-plugin-boundaries` MUST enforce the import rules `[SRC-002]`

Rationale:
- FSD is used by Yandex (150+ teams) and adopted by teams at Alibaba and Tinkoff. It provides structural guardrails that domain-driven folders lack.

Enforcement:
- ESLint `eslint-plugin-boundaries` (automatic, blocking in CI)
- Review: verify that a feature does not import from another feature

Exceptions:
- None. Extract into `shared/` if two features share code.

---

### R-ARCH-02 One barrel file per feature

Requirement:
- Each feature MUST have a single `index.ts` barrel file at its root `[SRC-002]`
- Nested barrel files (in a feature's subfolders) MUST NOT be used `[SRC-003]`

Rationale:
- The root barrel file defines the feature's public API. Nested barrels break tree-shaking and create circular dependencies.

Enforcement:
- Review: flag `index.ts` files in feature subfolders

Exceptions:
- None.

---

### R-ARCH-03 Naming conventions

Requirement:
- Components: PascalCase (`UserCard.tsx`) `[SRC-002]`
- Hooks: camelCase with a `use` prefix (`useAuth.ts`)
- Utilities: camelCase (`formatDate.ts`)
- Tests: co-located with a `.test` suffix (`UserCard.test.tsx`)
- Constants: SCREAMING_SNAKE_CASE for values (`MAX_RETRIES`)

Rationale:
- Standard convention of the React ecosystem — reduces onboarding friction

Enforcement:
- Review: verify naming

Exceptions:
- None.

---

### R-ARCH-04 Import ordering

Requirement:
- Imports SHOULD follow the order: React → third-party libraries → internal aliases (`@/`) → relative imports → types → styles `[SRC-004]`
- A sorting plugin SHOULD be configured (`eslint-plugin-simple-import-sort` or `@trivago/prettier-plugin-sort-imports`)

Rationale:
- Deterministic order, reduced git conflicts, readability

Enforcement:
- ESLint or Prettier plugin (automatic)

Exceptions:
- None.

---

## Testing

### R-TEST-01 Testing stack

Requirement:
- Vitest MUST be the test runner (not Jest) `[SRC-005]`
- React Testing Library MUST be used for component tests `[SRC-006]`
- MSW MUST be used for API mocking (no manual `fetch` mock) `[SRC-007]`

Rationale:
- Vitest is 2-10x faster than Jest on Vite, supports ESM natively, and shares the Vite config
- MSW intercepts at the network level — more realistic than manual mocks

Enforcement:
- CI: Vitest in the pipeline
- Review: reject `vi.mock('fetch')` or `jest.mock`

Exceptions:
- None.

---

### R-TEST-02 Test behavior, not implementation

Requirement:
- Tests MUST query by role, label, or text — not by `data-testid` (last resort) `[SRC-006]`
- `userEvent` MUST be preferred over `fireEvent` `[SRC-006]`
- Tests MUST NOT check internal state, isolated hook return values, or DOM structure `[SRC-008]`

Rationale:
- "The more your tests resemble the way your software is used, the more confidence they can give you." — Kent C. Dodds

Enforcement:
- Review: flag `getByTestId` when a role/label is possible, flag implementation tests

Exceptions:
- `data-testid` allowed when no role/label/text is applicable.

---

### R-TEST-03 Test coverage

Requirement:
- Overall coverage SHOULD be 70-80% `[SRC-008]`
- Critical paths (auth, data mutations) MUST have ≥ 90% coverage
- 100% coverage MUST NOT be a goal `[SRC-008]`

Rationale:
- 70-80% is the cost/benefit sweet spot. Beyond that, returns diminish and it encourages testing implementation.

Enforcement:
- CI: coverage report (v8 provider)
- Review: verify critical paths

Exceptions:
- Purely visual components (style wrappers) exempt from the 70% threshold.

---

### R-TEST-04 Test pyramid

Requirement:
- The distribution SHOULD follow: ~40% unit, ~50% integration, ~10% e2e `[SRC-006]`
- Integration tests (component + children + interactions) SHOULD be favored — the best confidence/effort ratio

Rationale:
- Unit tests alone do not guarantee integrated behavior. E2E tests are slow and brittle. Integration is the best compromise.

Enforcement:
- Review: verify the balance

Exceptions:
- None.

---

## Tooling

### R-TOOL-01 ESLint 9 flat config

Requirement:
- ESLint MUST use the flat config format (`eslint.config.js`) `[SRC-009]`
- The `.eslintrc` format MUST NOT be used (deprecated since ESLint 9, April 2024)

Rationale:
- The legacy format is deprecated. Flat config is the standard.

Enforcement:
- CI: ESLint in the pipeline

Exceptions:
- None.

---

### R-TOOL-02 Prettier for formatting only

Requirement:
- Prettier MUST handle formatting; ESLint MUST handle logic `[SRC-009]`
- `eslint-config-prettier` MUST be used to disable conflicting rules
- ESLint MUST NOT contain formatting rules (spacing, quotes, semicolons)

Rationale:
- The ESLint team itself deprecated all formatting rules. Separate the responsibilities.

Enforcement:
- CI: separate Prettier check + ESLint check

Exceptions:
- None.

---

### R-TOOL-03 Accessibility — WCAG 2.1 AA minimum

Requirement:
- `eslint-plugin-jsx-a11y` MUST be included in the ESLint config `[SRC-010]`
- Interactive components MUST use semantic HTML (`<button>`, not `<div onClick>`) `[SRC-010]`
- Images MUST have an `alt` attribute (informative or `alt=""` for decorative) `[SRC-010]`
- Inputs MUST have an associated `<label>` `[SRC-010]`
- Color contrast ratio MUST be ≥ 4.5:1 (normal text) or ≥ 3:1 (large text) `[SRC-011]`

Rationale:
- WCAG 2.1 AA is an international standard and a legal obligation in many jurisdictions

Enforcement:
- ESLint `jsx-a11y` (automatic)
- Review: verify semantic HTML and contrasts

Exceptions:
- None for the `jsx-a11y` rules. Contrast relaxed on non-text decorative elements.

---

### R-TOOL-04 Error Boundaries

Requirement:
- `react-error-boundary` MUST be used (no custom ErrorBoundary) `[SRC-012]`
- An ErrorBoundary MUST be placed at the root of the application
- An ErrorBoundary SHOULD be placed per feature/route
- Errors MUST be reported to a monitoring service (Sentry, etc.) via `onError`

Rationale:
- Without an ErrorBoundary, an error in one component crashes the whole application. Isolation per feature limits the blast radius.

Enforcement:
- Review: verify the presence of ErrorBoundaries
- Monitoring: alerts on captured errors

Exceptions:
- None for the root boundary.

---

### R-TOOL-05 Typed API errors

Requirement:
- The project MUST have a typed `ApiError` class with `status` and `code` `[SRC-013]`
- TanStack Query MUST configure a conditional retry: no retry on 4xx, retry on 5xx `[SRC-013]`

Rationale:
- Retrying a 404 or 403 is useless and wastes the network. Typed errors enable conditional handling on the UI side.

Enforcement:
- Review: verify the retry config in the QueryClient or per query

Exceptions:
- None.

---

## Enforcement summary

| Rule | Mechanism | Automated |
|---|---|---|
| R-ARCH-01 | eslint-plugin-boundaries | Yes |
| R-ARCH-02 | Review | No |
| R-ARCH-03 | Review | No |
| R-ARCH-04 | ESLint/Prettier plugin | Yes |
| R-TEST-01 | CI Vitest | Yes |
| R-TEST-02 | Review | No |
| R-TEST-03 | CI coverage report | Yes |
| R-TEST-04 | Review | No |
| R-TOOL-01 | CI ESLint | Yes |
| R-TOOL-02 | CI Prettier | Yes |
| R-TOOL-03 | ESLint jsx-a11y | Yes |
| R-TOOL-04 | Review | No |
| R-TOOL-05 | Review | No |

## Exceptions process

- Max 90 days, renewable with justification
- Approved by Tech Lead

## Metrics

| Metric | Baseline | Target | Measurement |
|---|---|---|---|
| Import boundary violations | 0 | 0 | ESLint CI |
| Test coverage (overall) | — | 70-80% | Vitest v8 |
| Test coverage (auth, mutations) | — | ≥ 90% | Vitest v8 |
| jsx-a11y errors | 0 | 0 | ESLint CI |
| ErrorBoundary placement | — | root + per-route | Review audit |

## Sources

- SRC-001 | Feature-Sliced Design spec | https://feature-sliced.design | Community | 2024 | 6-layer architecture
- SRC-002 | Bulletproof React | https://github.com/alan2207/bulletproof-react | Alan Alickovic | 2024 | Feature-based architecture
- SRC-003 | Vite/Rollup — Tree Shaking | https://rollupjs.org/introduction/#tree-shaking | Rollup | 2024 | Barrel files and tree-shaking
- SRC-004 | eslint-plugin-simple-import-sort | https://github.com/lydell/eslint-plugin-simple-import-sort | Community | 2024 | Import ordering
- SRC-005 | Vitest docs | https://vitest.dev | Vitest | 2024 | Test runner for Vite
- SRC-006 | Testing Library guiding principles | https://testing-library.com/docs/guiding-principles | Kent C. Dodds | 2024 | Test behavior not implementation
- SRC-007 | MSW docs | https://mswjs.io/docs | MSW | 2024 | API mocking at network level
- SRC-008 | Kent C. Dodds — Testing Implementation Details | https://kentcdodds.com/blog/testing-implementation-details | KCD | 2023 | Testing anti-patterns
- SRC-009 | ESLint flat config | https://eslint.org/docs/latest/use/configure/configuration-files | ESLint | 2024 | Config format
- SRC-010 | eslint-plugin-jsx-a11y | https://github.com/jsx-eslint/eslint-plugin-jsx-a11y | Community | 2024 | Accessibility linting
- SRC-011 | WCAG 2.1 | https://www.w3.org/TR/WCAG21 | W3C | 2018 | International accessibility standard
- SRC-012 | react-error-boundary | https://github.com/bvaughn/react-error-boundary | Brian Vaughn | 2024 | Error boundary library
- SRC-013 | TkDodo — React Query Error Handling | https://tkdodo.eu/blog/react-query-error-handling | Dominik Dorfmeister | 2024 | Typed errors + retry

## Change log

| Version | Date | Author | Description |
|---|---|---|---|
| 1.0.0 | 2026-04-06 | Claude Code | Initial standard from React+TS research report |
