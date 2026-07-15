# Validation toolbox

Concrete tools to **validate findings** and **measure the impact** of fixes.
Embedded principle: static analysis identifies **risks**, only runtime
measurement confirms a **real problem**.

---

## Frontend — Web Vitals & Lighthouse

| Tool | What it measures | Command / Usage |
|---|---|---|
| **Lighthouse CLI** | Overall score, LCP, TBT, CLS, FCP, SI | `npx lighthouse <url> --output=json --output=html` |
| **Lighthouse CI** | Regressions between commits/PRs | `npm i -g @lhci/cli && lhci autorun` |
| **PageSpeed Insights** | Core Web Vitals field + lab data | Google API |
| **web-vitals** (JS lib) | LCP, INP, CLS, FCP, TTFB in prod (RUM) | `npm i web-vitals` → `onLCP(console.log)` |
| **Sitespeed.io** | Complete open-source suite, Grafana | `npx sitespeed.io <url>` |

**Workflow:** Lighthouse CLI locally → Lighthouse CI in the pipeline → web-vitals in prod.

## Frontend — Bundle & Assets

| Tool | What it measures | Command / Usage |
|---|---|---|
| **webpack-bundle-analyzer** | Bundle treemap (stat/parsed/gzip) | `npx webpack-bundle-analyzer stats.json` |
| **vite-bundle-visualizer** | Treemap for Vite | `npx vite-bundle-visualizer` |
| **bundlesize** | CI guardrail: fail if > threshold | `npx bundlesize` |
| **source-map-explorer** | Which lines contribute to the size | `npx source-map-explorer bundle.js` |
| **import-cost** (VS Code) | Size of each import inline | VS Code extension |
| **depcheck** | Unused dependencies | `npx depcheck` |

## Frontend — React Runtime

| Tool | What it measures | Command / Usage |
|---|---|---|
| **React DevTools Profiler** | Render time, number of renders, re-render cause | Browser extension → Profiler |
| **React Performance Tracks** | React events in the Chrome Performance panel | Chrome DevTools → Performance |
| **`<Profiler>` component** | Programmatic render measurement of a subtree | `<Profiler id="X" onRender={cb}>` |
| **React Compiler** | Automatic memoization at build time | Babel/Vite plugin (stable Oct 2025) |
| **why-did-you-render** | Logs avoidable re-renders with the reason | `npm i @welldone-software/why-did-you-render` |

## Backend — Load Testing

| Tool | What it measures | Command / Usage |
|---|---|---|
| **autocannon** | Throughput, p50/p95/p99 latency | `npx autocannon -c 100 -d 30 http://localhost:3000/api` |
| **k6** | Scriptable load testing, scenarios, CI/CD | `k6 run script.js` |
| **Artillery** | HTTP, WebSocket, YAML scenarios | `npx artillery run scenario.yml` |
| **wrk** | Raw HTTP benchmark (C, ultra performant) | `wrk -t4 -c100 -d30s http://localhost:3000/api` |
| **clinic doctor** | Diagnoses event loop delay, GC, I/O | `npx clinic doctor -- node server.js` |

**Workflow:** clinic doctor diagnostic → autocannon benchmark → k6/Artillery load in CI.

## Backend — CPU Profiling & Flame Graphs

| Tool | What it measures | Command / Usage |
|---|---|---|
| **Clinic Flame** | Interactive CPU flame graphs | `npx clinic flame -- node server.js` |
| **Node.js --prof** | Built-in V8 profiler (sampling ticks) | `node --prof server.js` then `node --prof-process isolate-*.log` |
| **Chrome DevTools CPU** | Interactive flame chart profiling | `node --inspect server.js` → chrome://inspect |
| **0x** | Zero-config flame graphs | `npx 0x server.js` |
| **perf_hooks** (built-in) | High-resolution measurement | `performance.mark('start')` ... `performance.measure()` |

## Backend — Memory & GC

| Tool | What it measures | Command / Usage |
|---|---|---|
| **Clinic Heap Profiler** | Allocations per function | `npx clinic heapprofiler -- node server.js` |
| **Chrome Heap Snapshot** | Retained objects, retention tree | `node --inspect` → Memory → Heap Snapshot |
| **Clinic Bubbleprof** | Async operations, delays, I/O bottlenecks | `npx clinic bubbleprof -- node server.js` |
| **--heapsnapshot-signal** | On-demand snapshot via signal | `node --heapsnapshot-signal=SIGUSR2 server.js` |
| **--trace-gc** | Logs every GC collection | `node --trace-gc server.js` |
| **process.memoryUsage()** | Heap used/total, RSS | Integrate into `/health` or a timer |

## V8 Engine Internals

| Flag | What it measures | Command |
|---|---|---|
| **--trace-deopt** | Every deoptimization | `node --trace-deopt server.js 2>&1 \| grep deopt` |
| **--trace-opt** | TurboFan optimizations | `node --trace-opt server.js 2>&1 \| grep <fn>` |
| **--trace-ic** | Inline caches (mono→poly→mega) | `node --trace-ic server.js` |
| **--trace-maps** | Hidden class transitions | `node --trace-maps server.js` |
| **v8-deopt-viewer** | Web UI for deopt logs | `npx v8-deopt-viewer server.js` |

⚠️ These flags generate a lot of logs. Always filter on the function of interest.

## Microbenchmarks

| Tool | Usage | Command |
|---|---|---|
| **tinybench** | Precise microbenchmarks (stats, percentiles) | `npm i tinybench` — programmatic API |
| **bench-node** | Integrated into the Node.js test runner | `import { Suite } from 'bench-node'` |
| **perf_hooks** | High-resolution measurement with no dependency | `performance.now()` or `performance.timerify(fn)` |

**V8 pitfalls:** uniform data (optimism), dead code elimination (consume the result),
execution order (randomize or use separate processes).

## ESLint — Static analysis

| Plugin | What it detects | Installation |
|---|---|---|
| **eslint-plugin-react-perf** | Inline JSX objects/arrays/functions | `npm i -D eslint-plugin-react-perf` |
| **ESLint complexity** | Cyclomatic complexity > threshold | `"complexity": ["warn", 10]` |
| **React Compiler ESLint** | Props/state mutations | Included in React 19.2+ |
| **no-floating-promises** | Un-awaited promises | `@typescript-eslint/eslint-plugin` |

---

## Quick selection matrix

| Finding type | Validation tool | What you check |
|---|---|---|
| Bundle too large | vite-bundle-visualizer | Size before/after |
| React re-renders | React DevTools Profiler + why-did-you-render | Number of renders before/after |
| N+1 queries | autocannon + ORM logging | Queries and p95 latency |
| Memory leak | --trace-gc + Heap Snapshot (2 snapshots) | Ratchet vs sawtooth pattern |
| Blocked event loop | clinic doctor | Delay before/after |
| V8 deoptimization | --trace-deopt filtered | Deopt disappears after the fix |
| Slow hot path | tinybench / bench-node | Ops/sec before/after |
| API response time | autocannon -c 100 -d 30s | p95 latency before/after |
| LCP / CLS / INP | Lighthouse CLI + web-vitals | Scores before/after |
| Slow JSON | perf_hooks timerify | Duration in ms before/after |
