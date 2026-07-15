---
name: "perf-analyzer"
description: >
  In-depth performance analysis of an existing codebase (web frontend + Node.js backend)
  that produces a structured report with prioritized recommendations, covering algorithmic
  complexity (time/space Big O), V8 stack/heap analysis, concurrency patterns, and the
  performance impact of design patterns.
  Use this skill whenever the user mentions: performance, perf audit, slowness,
  optimization, bundle size, Core Web Vitals, API response time, memory leak, slow queries,
  N+1, profiling, Lighthouse, algorithmic complexity, Big O, "it's slow", "it's laggy",
  "we need to optimize", or any request to analyze or improve an application's speed.
  Also relevant when the user shares a Lighthouse report, a screenshot of the
  DevTools Performance panel, or mentions degraded monitoring metrics.
---

# Performance Analyzer

Performance analysis skill for web codebases (frontend) and backends (Node.js/TypeScript).
Produces a structured report with scored findings and prioritized recommendations.

**In scope:**
- Static analysis of frontend code (React, CSS, assets, bundle)
- Static analysis of backend code (Node.js, DB queries, API, caching)
- Algorithmic complexity analysis (time and space, Big O)
- Low-level analysis (V8/JIT, stack/heap, allocation, GC)
- Concurrency, parallelism, and race condition analysis
- Assessment of the performance impact of design patterns
- Production of a structured report with scoring, prioritization, and validation tools

**Out of scope:**
- Running runtime benchmarks (but it does recommend which ones to run)
- Analysis of production metrics (APM, logs) — unless provided
- Infrastructure optimization (CDN, scaling) — limited to code

---

## Detailed references

The pattern tables and detailed tools live in `references/`.
Read the relevant file during the matching phase.

| File | Content | When to read it |
|---|---|---|
| `references/patterns-frontend.md` | Bundle, React, and Assets patterns with severities | Phase 2 — Frontend analysis |
| `references/patterns-backend.md` | DB, API, and Memory/Event Loop patterns | Phase 3 — Backend analysis |
| `references/low-level.md` | V8/JIT, GC allocation, data locality, serialization, event loop | Phase 3bis — Low-level analysis |
| `references/complexity.md` | Time/space Big O, V8 stack/heap memory model, JS operations reference | Phase 3ter — Algorithmic complexity |
| `references/concurrency-architecture.md` | Node.js concurrency, race conditions, design patterns & perf | Phase 3quater — Concurrency & architecture |
| `references/toolbox.md` | All validation tools with commands, quick selection matrix | Phase 5 — Tools recommended in the report |
| `references/thresholds.md` | Core Web Vitals, RAIL, Lighthouse weights, cyclomatic complexity, JS Big O | All phases — reference thresholds |

---

## Analysis workflow

### Phase 0 — Scoping

1. **Scope**: the entire codebase, a specific service, or a single critical path?
2. **Symptoms**: observed slowness or a preventive audit?
3. **Stack**: frontend framework, backend runtime, ORM, bundler

If the scope isn't specified, analyze everything, starting with the critical paths.

### Phase 1 — Codebase reconnaissance

Explore the structure before analyzing:
1. Read `package.json` (root + workspaces) → dependencies, scripts, bundler
2. Identify the structure: monorepo? services? shared libs?
3. Locate the configs: webpack/vite, tsconfig, eslint
4. Identify the entry points: routes, API endpoints, main

This phase tailors the analysis to the actual stack rather than applying generic rules.

### Phase 1bis — Analysis specific to the detected framework

Every framework has its own performance patterns, pitfalls, and dedicated tools.
Once the stack is identified, apply an analysis specific to the detected
framework(s) **in addition to** the generic patterns of the following phases.

The idea: the generic patterns (N+1, allocation, Big O) apply everywhere.
But each framework adds its own abstraction layer that introduces specific
problems you only find by knowing the framework internals.

**For each detected framework, analyze:**

1. **Rendering / execution model** — how the framework handles requests or rendering.
   Every framework has a lifecycle with specific hot spots.
   - React: reconciliation (virtual DOM diff), hooks lifecycle, Fiber scheduler
   - Next.js/Remix: SSR hydration cost, RSC streaming, static vs dynamic rendering
   - Vue: reactivity system (Proxy-based), computed caching, watchEffect cleanup
   - Angular: change detection (zone.js), OnPush strategy, lazy modules
   - Fastify: encapsulation, plugin system, JSON schema serialization
   - Express: linear middleware stack, no native schema validation
   - NestJS: DI container overhead, interceptors chain, Guards execution order

2. **Native framework optimizations** — check whether they're being used.
   Every framework provides built-in optimization mechanisms. Not using them
   when they exist is often more expensive than writing custom code.
   - React: `React.memo`, `useMemo`, `useCallback`, `React.lazy`, Suspense, `useTransition`, React Compiler
   - Next.js: `next/image`, `next/font`, ISR, `generateStaticParams`, route segment config
   - Fastify: JSON Schema response serialization (`fast-json-stringify`), `@fastify/compress`, route-level hooks
   - Prisma: `include` vs separate queries, `select` to limit columns, `$queryRaw` for hot paths

3. **Known framework anti-patterns** — patterns documented as problematic.
   These patterns are often subtle because the code compiles/works, but performance
   degrades silently.
   - React: components defined inside other components, Context that re-renders everything, useEffect without cleanup
   - Next.js: `use client` too high in the tree (bundles everything client-side), fetch without cache in SSR, layouts that re-render
   - Fastify: unencapsulated plugins that pollute the global scope, missing JSON Schema (falls back to slow JSON.stringify)
   - Prisma: `findMany` without `take` (no LIMIT), deep nested `include` (JOIN explosion), no `$transaction` on multiple writes

4. **Build / runtime configuration** — the framework's perf options.
   - Vite: `build.rollupOptions.output.manualChunks`, `optimizeDeps.include`, `build.sourcemap`
   - Webpack: `splitChunks`, `TerserPlugin`, `cache: filesystem`
   - TypeScript: `skipLibCheck`, `incremental`, `isolatedModules`
   - Node.js: `--max-old-space-size`, `--max-semi-space-size`, UV_THREADPOOL_SIZE

**Don't try to cover everything** — focus on the frameworks actually
present in the codebase. If the project uses React + Fastify, analyze those two
in depth rather than skimming 10 frameworks.

5. **Documentor lookup for lesser-known or recent frameworks** —
   If the codebase uses a framework whose performance patterns aren't
   well understood (a niche framework, a very recent version with new APIs,
   or an uncommon technology like Solid, Qwik, Hono, Bun, Deno Fresh, etc.),
   **use the Documentor skill** to look up the performance best practices
   specific to that framework before continuing the analysis.

   Trigger Documentor when:
   - The detected framework isn't in the list above (React, Next.js, Vue, Angular, Fastify, Express, NestJS, Prisma)
   - The framework version is very recent (e.g. React 19+ with the Compiler, Next.js 15+ with Server Actions)
   - The user reports a framework-specific problem that the generic patterns don't cover

   Suggested Documentor query:
   `"Performance best practices and known anti-patterns for [framework] [version].
   Look for: native framework optimizations, rendering/execution patterns,
   build configuration, dedicated profiling tools, and performance pitfalls
   documented in recent changelogs."`

   Fold the results into the Phase 1bis analysis before continuing.

### Phase 2 — Frontend analysis

→ **Read `references/patterns-frontend.md`** for the detection tables.

Go through the frontend code looking for problems in:
- **Bundle & Dependencies**: heavy imports, missing code splitting, tree shaking
- **React Performance**: re-renders, unstable refs, Context cascade, data fetching
- **Assets & Rendering**: images, fonts, blocking CSS, animations

**How to search:** read the entry-point imports, check the bundler config,
scan the `.tsx`/`.jsx` files for React patterns, check `index.html` for assets.

### Phase 3 — Backend analysis

→ **Read `references/patterns-backend.md`** for the detection tables.

Analyze the backend code looking for:
- **DB queries**: N+1, SELECT *, missing indexes, pagination, await+query loops
- **API & Architecture**: cache, compression, timeouts, waterfall, middlewares
- **Memory & Event Loop**: unbounded caches, listeners without cleanup, synchronous ops

**How to search:** scan the repositories/services/controllers, look for ORM patterns,
identify loops containing DB or HTTP calls.

### Phase 3bis — Low-level analysis (macro & micro-optimization)

→ **Read `references/low-level.md`** for the detection tables.

Goes beyond application-level patterns to examine the V8 runtime. This layer makes
the difference between "correct" code and performant code — the approach comes from the
embedded/C world, where every CPU cycle counts.

**Relevant when:** identified hot paths, large datasets (>10k), heavy load (>100 req/s),
batch/streaming, unexplained latency despite "clean" application code.

Covers: V8/JIT (hidden classes, deopt), allocation/GC (young/old gen pressure),
data locality (AoS vs SoA), serialization/I/O, cooperative event loop.

**Principle:** focus on **hot paths** only. Optimizing code that runs once
at startup is pointless. Measure first, optimize second.

### Phase 3ter — Algorithmic complexity analysis

→ **Read `references/complexity.md`** for the tables and the reference.

Assesses time complexity (Big O) and space complexity (stack vs heap) of the algorithms.
The JS runtime hides complexity but doesn't eliminate it.

**Time complexity:** identify when actual complexity diverges from what's expected
(Array.includes inside a loop = O(n×m), repeated sort on stable data, shift O(n), etc.)

**Space complexity:** analyze what goes on the stack vs the heap, predict GC
pressure, identify leak risks (long-lived closures, deep recursion, Old Gen
accumulation, strings concatenated in a loop).

**Mandatory annotation:** every algorithmic finding must state
`Complexity: O(current) → O(after fix)`.

### Phase 3quater — Concurrency, parallelism & architecture

→ **Read `references/concurrency-architecture.md`** for the detection tables.

Analyzes the concurrency patterns and architectural choices that affect
performance. The same fundamental problems as in embedded systems (concurrent access,
starvation, contention, deadlocks) but with different mechanisms (event loop, workers, cluster).

**Concurrency:** sequential vs parallel await, Promise.all without a pool, misused
worker threads, missing AbortController, mutex without timeout.

**Race conditions:** read-modify-write across an await, cache invalidation races,
missing SSE/WebSocket cleanup, concurrent operations without idempotence.

**Design patterns:** real cost on hot paths — Observer O(n), middleware chain O(m),
Repository+DTO = 3 allocations/row, Strategy = V8 megamorphism risk, Pub/Sub = polling
vs push, Hexagonal = copies between layers.

### Phase 4 — Scoring & Prioritization

Each finding is scored along two axes:

**Severity (user impact):**
| Level | Definition | Score |
|---|---|---|
| Critical | Crash, freeze, >5s of latency | 4 |
| High | >1s of latency, visible jank | 3 |
| Medium | Measurable but not immediately perceptible | 2 |
| Low | Technical optimization, marginal impact | 1 |

**Fix effort:**
| Level | Definition | Score |
|---|---|---|
| Quick Win | < 30 min, localized, low risk | 1 |
| Medium | 1-4h, multi-file | 2 |
| Heavy | > 4h, refactoring, regression risk | 3 |

**Priority = Severity × (4 - Effort)**

Critical quick wins (score 12) = urgent. Low-impact refactorings (score 1) = later.

### Phase 5 — Report generation

→ **Read `references/toolbox.md`** for the validation tools to include.
→ **Read `references/thresholds.md`** for the reference thresholds.

The report follows this exact structure:

```markdown
# Performance Analysis Report

## Executive summary
[3-5 lines: scope, findings by severity, top 3 recommendations]

## Overall score
[Score /100 — 90-100 Excellent, 70-89 Good, 50-69 Average, <50 Critical]

## Findings

### [Category]

#### [FND-001] Descriptive title
- **Severity:** Critical | High | Medium | Low
- **Effort:** Quick Win | Medium | Heavy
- **Priority:** [score]
- **Location:** `path/file.ts:line`
- **Description:** [problem and why]
- **Complexity:** [if applicable — O(current) → O(after), stack/heap space]
- **Estimated impact:** [concrete effect]
- **Recommendation:** [action + code example if relevant]

## Prioritization matrix
[Table sorted by descending priority]

## Quick Wins (do immediately)
## Medium-term recommendations
## Structural refactorings
## Metrics to monitor
## Recommended tools
[For each finding, the validation tool — see the selection matrix in toolbox.md]

## Validation plan
[Sequence of tools: baseline → fix → re-measure → expected threshold]
```

**Available categories:** Frontend (Bundle | React | Assets), Backend (DB | API | Memory),
Low-Level (V8 | Allocation | Data | Serialization | EventLoop),
Complexity (Temporal | Spatial), Concurrency (Race | Parallelism),
Architecture (Pattern).

---

## Failure modes & recovery

| Failure | Corrective action |
|---|---|
| Codebase too large | Ask for the critical paths, start with the entry points |
| Unrecognized stack | Adapt the patterns, flag the limitations |
| No problem detected | Say so explicitly — don't invent findings |
| Ambiguous findings | Mark "To verify" + suggest runtime profiling |
| Runtime metrics contradict the static analysis | Prioritize the runtime — static analysis identifies risks, the runtime shows the real problems |
| More than 30 findings | Top 15 by priority in the report, the rest in an appendix |

---

## Best practices

- **Always read the code** before concluding — context > pattern matching
- **Contextualize** — an N+1 on a once-a-day endpoint ≠ an N+1 on the busiest one
- **Be specific** — "Convert hero.png (2.4MB) → WebP ~200KB" > "Optimize the images"
- **Don't over-optimize** — if it's readable and fast enough, don't recommend micro-optimizations
- **Give code examples** — a 5-line before/after > a paragraph of explanation
- **Annotate complexity** — every algorithmic finding must show O(before) → O(after)
