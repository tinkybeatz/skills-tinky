# Standard: React Components & State Management — Sapain Borne

- Status: Active
- Version: 1.2.0
- Owner: Engineering Lead
- Approvers: Tech Lead
- Effective date: 2026-04-06
- Last review date: 2026-04-06

## Scope

All React code in the sapain-borne monorepo: `services/back-office/`, `src/renderer/`.

## Normative rules

### R-REACT-01 Function components only

Requirement:
- Components MUST be functions (not classes) `[SRC-001]`
- `React.FC` MUST NOT be used — use explicit props interfaces `[SRC-002]`

Rationale:
- React docs (2023+) teach exclusively with functions and hooks
- `React.FC` adds an unwanted implicit `children` and complicates typing

Enforcement:
- Review: reject class components and `React.FC`
- ESLint: no standard automated rule, manual check

Exceptions:
- Error Boundaries (React requires classes for `getDerivedStateFromError`). Use `react-error-boundary` rather than writing your own classes.

---

### R-REACT-02 Explicitly typed props

Requirement:
- Each component MUST have a named props interface `[SRC-001]`
- Props SHOULD use the `interface XxxProps` pattern (not inline)

Rationale:
- Readability, type reusability, auto-documentation via the IDE

Enforcement:
- Review: verify that complex inline props (>2 props) are extracted into an interface

Exceptions:
- Simple internal components with 1-2 inline props allowed.

---

### R-REACT-03 Hooks — fundamental rules

Requirement:
- Hooks MUST be called at the top level only (never in conditions, loops, nested functions) `[SRC-001]`
- Custom hooks MUST start with `use` `[SRC-001]`
- ESLint `react-hooks/rules-of-hooks` MUST be at `error` `[SRC-003]`
- ESLint `react-hooks/exhaustive-deps` MUST be at `warn` `[SRC-003]`

Rationale:
- Required by React for consistency in call order across renders
- `exhaustive-deps` prevents stale closures (silent bugs)

Enforcement:
- ESLint rules (automatic, blocking in CI)

Exceptions:
- None for `rules-of-hooks`. Disabling `exhaustive-deps` allowed with a justifying comment.

---

### R-REACT-04 Composition > HOCs > Render Props

Requirement:
- New reuse patterns MUST use hooks or composition via children/slots `[SRC-001]`
- HOCs SHOULD NOT be used in new code
- Render props MAY be used for inversion of control (headless UI)

Rationale:
- Hooks replace the majority of HOCs with better TS typing and no wrapper hell in DevTools

Enforcement:
- Review: challenge any new HOC

Exceptions:
- Third-party library HOCs (legacy withRouter, etc.) allowed temporarily.

---

### R-REACT-05 State colocation

Requirement:
- State MUST be placed as close as possible to its usage `[SRC-004]`
- Mandatory decision tree:

| Scope | Tool |
|---|---|
| A single component | `useState` / `useReducer` |
| Parent + direct children | Lift state up, props |
| Subtree (theme, auth) | React Context |
| Server / API data | TanStack Query |
| Global client state | Zustand with selectors |
| URL state | `useSearchParams` |

Rationale:
- Colocation reduces unnecessary re-renders and improves readability

Enforcement:
- Review: flag global state used by a single component

Exceptions:
- None.

---

### R-REACT-06 TanStack Query for server state

Requirement:
- Any data coming from an API MUST use TanStack Query (not `useEffect` + `useState`) `[SRC-005]`
- Pages MUST NOT contain `useEffect` + `api.get()` + `setLoading` for data fetching — use `useQuery` in a dedicated hook in `features/*/api/`
- A global `staleTime` MUST be configured (minimum 30 seconds) `[SRC-006]`
- Query keys MUST use the factory pattern (TkDodo) for consistency and targeted invalidation `[SRC-006]`
- Mutations MUST use `useMutation` with `onSuccess: () => queryClient.invalidateQueries(...)` to invalidate the cache
- `invalidateQueries` SHOULD be preferred over `setQueryData` (except for optimistic updates)

Mandatory query key factory pattern:
```typescript
// features/catalog/api/keys.ts
export const catalogKeys = {
  all: ["catalog"] as const,
  lists: () => [...catalogKeys.all, "list"] as const,
  listBySite: (siteId: string) => [...catalogKeys.lists(), siteId] as const,
};
```

Rationale:
- TanStack Query provides caching, deduplication, auto-refetch, pagination — reinventing these mechanisms is wasted time and a source of bugs
- `staleTime: 0` (the default) causes a refetch on every mount — a measured network impact of 80-95% excess requests
- Without TanStack Query, each sidebar → page navigation unmounts the component → loses state → refetches. With TanStack Query, data is served from the cache immediately

Enforcement:
- Review: reject `useEffect` + `fetch` + `useState` patterns for data fetching in pages and components
- CI: verify that the `QueryClient` has a `staleTime` > 0
- CI: grep — no `api.get` in `src/pages/`

Exceptions:
- SSE/WebSocket (server-push) — does not go through Query.

---

### R-REACT-07 Zustand for global client state

Requirement:
- Zustand MUST be used for global client state (not Redux, not Context for frequent state) `[SRC-007]`
- Stores MUST use selectors: `useStore((s) => s.field)` not `useStore()` `[SRC-007]`
- Stores MUST be split by domain (not one giant store)
- The `devtools` middleware SHOULD be enabled in development

Rationale:
- Zustand < 2kb vs Redux Toolkit ~35kb. Minimal API, excellent TS support
- Without a selector, the whole store re-renders all consumers

Enforcement:
- Review: flag `useStore()` without a selector, flag monolithic stores

Exceptions:
- None.

---

### R-REACT-08 Context API — strict limits

Requirement:
- React Context MUST NOT be used as a state manager `[SRC-004]`
- Context SHOULD be limited to low-change-frequency data: theme, locale, auth status
- Context MUST NOT contain data that changes on every keystroke, scroll, or interaction

Rationale:
- Each value change re-renders ALL the context's consumers — a structural performance problem

Enforcement:
- Review: flag any Context with frequent updates

Exceptions:
- None.

---

### R-REACT-09 Storybook mandatory for UI components

Requirement:
- Every UI component in `shared/ui/` or `features/*/ui/` MUST have a co-located `.stories.tsx` file (same folder as the component)
- Stories MUST use the CSF3 format (export const + typed Meta)
- Each component MUST have at least a `Default` story
- Components with distinct visual states (loading, error, empty) SHOULD have one story per state
- Stories MUST NOT import from higher layers in the FSD architecture

Rationale:
- The Storybook catalog lets you visually validate components in isolation, test edge cases (long text, empty states), and document variants
- Co-location ensures the story stays up to date when the component changes — if it's far away, it gets forgotten

Naming convention:
- File: `[Component].stories.tsx`
- Title: `shared/[Component]` or `features/[feature-name]/[Component]`
- Stories named by state: `Default`, `Loading`, `Empty`, `Error`, `WithLongContent`, etc.

Enforcement:
- Review: verify that a new UI component comes with its story
- CI: glob check — every `.tsx` in `*/ui/` (excluding `index.tsx` and `*.stories.tsx`) must have a corresponding `.stories.tsx`

Exceptions:
- Trivial wrapper components (re-export, layout without props) MAY omit the story with justification in the PR.

---

## Enforcement summary

| Rule | Mechanism | Automated |
|---|---|---|
| R-REACT-01 | Review | No |
| R-REACT-02 | Review | No |
| R-REACT-03 | ESLint react-hooks | Yes |
| R-REACT-04 | Review | No |
| R-REACT-05 | Review | No |
| R-REACT-06 | Review + CI | Partial |
| R-REACT-07 | Review | No |
| R-REACT-08 | Review | No |
| R-REACT-09 | Review + CI glob | Partial |

## Exceptions process

- Max 90 days, renewable with justification
- Approved by Tech Lead
- Recorded in a PR comment

## Metrics

| Metric | Baseline | Target | Measurement |
|---|---|---|---|
| `useEffect` + `fetch` patterns | — | 0 | Grep in the codebase |
| `useStore()` without a selector | — | 0 | Grep pattern |
| Class components | — | 0 (except ErrorBoundary) | Grep `extends Component` |
| UI components without a story | — | 0 | Glob `*/ui/*.tsx` without a corresponding `.stories.tsx` |

## Sources

- SRC-001 | React docs (react.dev) | https://react.dev/learn | Meta | 2024 | Hooks, composition, functional components
- SRC-002 | React TypeScript Cheatsheet | https://react-typescript-cheatsheet.netlify.app/ | Community | 2024 | React.FC anti-pattern
- SRC-003 | eslint-plugin-react-hooks | https://www.npmjs.com/package/eslint-plugin-react-hooks | Meta | 2024 | Rules of hooks enforcement
- SRC-004 | Kent C. Dodds — State Colocation | https://kentcdodds.com/blog/state-colocation-will-make-your-react-app-faster | KCD | 2023 | Colocation principle
- SRC-005 | TanStack Query docs | https://tanstack.com/query/latest | Tanner Linsley | 2024 | Server state management
- SRC-006 | TkDodo — Effective React Query Keys | https://tkdodo.eu/blog/effective-react-query-keys | Dominik Dorfmeister | 2024 | Key factories, staleTime
- SRC-007 | Zustand docs | https://docs.pmnd.rs/zustand | pmndrs | 2024 | Client state, selectors

## Change log

| Version | Date | Author | Description |
|---|---|---|---|
| 1.2.0 | 2026-04-08 | Claude Code | Strengthened R-REACT-06: mandatory query key factories, no useEffect+api.get in pages, useMutation pattern |
| 1.1.0 | 2026-04-08 | Claude Code | Added R-REACT-09: mandatory Storybook for UI components |
| 1.0.0 | 2026-04-06 | Claude Code | Initial standard from React+TS research report |
