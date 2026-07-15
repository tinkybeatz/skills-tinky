# Frontend patterns — Detection reference

## Bundle & Dependencies

| Pattern to detect | Why it's a problem | Severity |
|---|---|---|
| Importing whole heavy libraries (`import _ from 'lodash'`) | Loads the entire package instead of the submodule you use | High |
| Duplicate or outdated dependencies (moment.js, full lodash) | Needlessly bloated bundle | Medium |
| No code splitting on routes | All the JS loaded on first access | High |
| Heavy components not lazy-loaded (modals, datepickers, charts) | Block the initial load | Medium |
| Missing `sideEffects: false` in package.json | Prevents optimal tree shaking | Low |

**How to search:** read the imports in the entry files, check the bundler
config (Vite/Webpack), scan the `import` statements for non-tree-shakable patterns.

## React Performance

| Pattern to detect | Why it's a problem | Severity |
|---|---|---|
| Objects/arrays/functions created inline in JSX (`style={{...}}`, `onClick={() => ...}`) | New reference on every render → child re-renders | Medium |
| Components defined inside other components | Complete loss of state + re-mount on every parent render | Critical |
| Missing stable `key` on lists, or key={index} on dynamic lists | Incorrect DOM reconciliation, unnecessary re-renders | Medium |
| Context Provider at the root with a value that changes often | All consumers re-render on every change | High |
| `useEffect` with missing or overly broad dependencies | Infinite loops or stale effects | High |
| Large monolithic components (>300 lines) without memoization | Impossible to fine-tune re-renders | Medium |
| Data fetching in components without caching (no React Query/SWR) | Network requests on every mount, waterfalls | High |

**How to search:** scan the `.tsx`/`.jsx` files, check the component
structure, analyze the data-fetching patterns.

## Assets & Rendering

| Pattern to detect | Why it's a problem | Severity |
|---|---|---|
| Unoptimized images (PNG/JPG instead of WebP/AVIF) | Degraded LCP, wasted bandwidth | High |
| Images without explicit dimensions (width/height) | CLS — layout shift on load | High |
| Fonts not preloaded or too many variants loaded | FOIT/FOUT, degraded LCP | Medium |
| Non-critical CSS in the head (large blocking CSS files) | Render-blocking, delayed FCP | Medium |
| JS animations instead of CSS transforms/transitions | Jank — animations off the compositor thread | Medium |
