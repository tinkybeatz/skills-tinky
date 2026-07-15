# Standard: Frontend Performance — Sapain Borne

- Status: Active
- Version: 1.0.0
- Owner: Engineering Lead
- Approvers: Tech Lead
- Effective date: 2026-04-06
- Last review date: 2026-04-06

## Scope

All React frontend code in the sapain-borne monorepo. Covers bundle size, rendering, Web Vitals, memory, and network.

## Normative rules

### R-PERF-01 Bundle size budget

Requirement:
- Initial JS (gzip) MUST be < 200 KB, SHOULD be < 100 KB `[SRC-001]`
- Total JS (lazy-loaded, gzip) MUST be < 1 MB `[SRC-001]`
- Any dependency addition > 10 KB gzip MUST be justified in the PR `[SRC-002]`

Rationale:
- On a median mobile device, parsing 1 MB of JS takes 2-4 seconds. On low-end devices, 5-8 seconds.

Enforcement:
- CI: `vite-bundle-visualizer` on each build, alert if the threshold is exceeded
- Review: check new dependencies via bundlephobia.com

Exceptions:
- Critical features requiring a heavy library — justification + mandatory lazy-loading.

---

### R-PERF-02 Per-route code splitting

Requirement:
- Each route MUST be lazy-loaded via `React.lazy()` + `Suspense` `[SRC-003]`
- Heavy components (editors, charts, complex modals) SHOULD be lazy-loaded `[SRC-003]`

Rationale:
- Highest ROI, lowest effort. Reduces the initial bundle by 50-80%.

Enforcement:
- Review: verify that pages are not imported statically in the router

Exceptions:
- The login page (the first page seen) may be included in the initial bundle.

---

### R-PERF-03 No premature memoization

Requirement:
- `React.memo`, `useMemo`, `useCallback` SHOULD NOT be used by default `[SRC-004]`
- Memoization MUST be justified by a measurement in the React Profiler
- `React.memo` SHOULD be used when: the component is > 1ms in the Profiler AND the parent re-renders frequently AND props are stable

Rationale:
- React is fast. The shallow comparison of React.memo has a cost. Memoizing a leaf component < 0.5ms is counterproductive.

Enforcement:
- Review: flag `React.memo` on trivial components, ask for the Profiler measurement

Exceptions:
- Lists with > 100 items: memoizing the item component is allowed without a prior measurement.

---

### R-PERF-04 Virtualization of long lists

Requirement:
- Lists > 100 items MUST be virtualized `[SRC-005]`
- TanStack Virtual SHOULD be the library used
- Infinite scroll MUST be combined with virtualization

Rationale:
- Without virtualization: 10,000 items = ~800ms initial render, ~200 MB DOM. With it: ~5ms, ~2 MB.

Enforcement:
- Review: flag `.map()` on collections potentially > 100 items without virtualization

Exceptions:
- Fixed-size lists with a known bound (< 50 items max possible).

---

### R-PERF-05 Web Vitals — targets

Requirement:
- INP MUST be ≤ 200ms `[SRC-006]`
- LCP SHOULD be ≤ 2.5s `[SRC-006]`
- CLS MUST be ≤ 0.1 `[SRC-006]`
- `useTransition` SHOULD be used for heavy interactions (filtering, sorting) `[SRC-003]`

Rationale:
- INP (which replaced FID in March 2024) measures ALL interactions. `useTransition` reduces INP by 30-60% on interaction-heavy UIs.

Enforcement:
- Monitoring: the `web-vitals` library in production
- Review: flag synchronous `setState` on heavy operations (filtering large lists)

Exceptions:
- LCP > 2.5s acceptable for client-only SPAs (no SSR). Monitor and improve.

---

### R-PERF-06 Lightweight dependencies

Requirement:
- `moment.js` MUST NOT be used — use `date-fns` or `dayjs` `[SRC-002]`
- The full `lodash` MUST NOT be imported — use `lodash-es` (tree-shakable) or native JS `[SRC-002]`
- Any dependency MUST be checked on bundlephobia.com before adding

Rationale:
- moment (~72 KB) → dayjs (~2.5 KB) = 97% savings. lodash (~72 KB) → native = 100%.

Enforcement:
- CI: scan for imports of blacklisted packages
- Review: check for lightweight alternatives

Exceptions:
- None for moment.js and the full lodash.

---

### R-PERF-07 Effect cleanup

Requirement:
- Every `useEffect` with an event listener, timer, fetch, or subscription MUST return a cleanup function `[SRC-007]`
- Fetches MUST use `AbortController` for cancellation `[SRC-007]`
- Components MUST work correctly in React Strict Mode (double mount/unmount in dev)

Rationale:
- Effects without cleanup cause memory leaks, state updates on unmounted components, and subtle production bugs

Enforcement:
- ESLint `react-hooks/exhaustive-deps` (partial)
- Review: verify cleanup on every useEffect

Exceptions:
- Mount-only effects (`[]` deps) with no external resource to clean up.

---

## Enforcement summary

| Rule | Mechanism | Automated |
|---|---|---|
| R-PERF-01 | CI bundle check | Yes |
| R-PERF-02 | Review | No |
| R-PERF-03 | Review | No |
| R-PERF-04 | Review | No |
| R-PERF-05 | web-vitals monitoring | Partial |
| R-PERF-06 | CI import scanner + review | Partial |
| R-PERF-07 | Review | No |

## Exceptions process

- Max 90 days, renewable with justification
- Approved by Tech Lead

## Metrics

| Metric | Baseline | Target | Measurement |
|---|---|---|---|
| Initial JS (gzip) | ~103 KB | < 100 KB | `vite build` output |
| INP p75 | — | ≤ 200ms | web-vitals in production |
| CLS | — | ≤ 0.1 | web-vitals in production |
| Blacklisted dependencies | 0 | 0 | CI scan |

## Sources

- SRC-001 | Alex Russell — Web Performance Budgets | 2024 | Chrome team, budget size reference
- SRC-002 | Bundlephobia | https://bundlephobia.com | Community | 2024 | Dependency size checker
- SRC-003 | React docs — Code Splitting, useTransition | https://react.dev | Meta | 2024
- SRC-004 | Dan Abramov — Before You memo() | https://overreacted.io/before-you-memo/ | 2021 | When not to memoize
- SRC-005 | TanStack Virtual docs | https://tanstack.com/virtual | 2024 | Headless virtualization
- SRC-006 | web.dev — Core Web Vitals | https://web.dev/articles/vitals | Google | 2024 | INP, LCP, CLS thresholds
- SRC-007 | React docs — Synchronizing with Effects | https://react.dev/learn/synchronizing-with-effects | Meta | 2024 | Cleanup patterns

## Change log

| Version | Date | Author | Description |
|---|---|---|---|
| 1.0.0 | 2026-04-06 | Claude Code | Initial standard from React+TS research report |
