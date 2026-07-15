# Standard: Backend Performance Node.js / Fastify — Sapain Borne

- Status: Active
- Version: 1.0.0
- Owner: Engineering Lead
- Approvers: Tech Lead
- Effective date: 2026-04-22
- Last review date: 2026-04-22

## Scope

All Node.js backend services using Fastify in the sapain-borne monorepo. Covers the event loop, V8 garbage collection, system resources, HTTP metrics, Fastify mechanisms (serialization, validation, hooks), and async concurrency.

Out of scope: frontend services (covered by `PERFORMANCE.md`), infrastructure (Docker, reverse proxy, load balancer).

---

## Reference methodology

The criteria follow two complementary methodologies:

- **USE** (Utilization, Saturation, Errors) — Brendan Gregg `[SRC-001]` — for system resources
- **RED** (Rate, Errors, Duration) — Tom Wilkie `[SRC-002]` — for HTTP/service metrics

---

## Normative rules

---

### Event Loop & V8 Runtime

---

### R-BPERF-01 Event loop lag monitoring

Requirement:
- Event loop lag MUST be monitored via `monitorEventLoopDelay()` from `perf_hooks` `[SRC-003]`
- The histogram MUST expose the p50, p95, p99, and max percentiles `[SRC-003]`
- The resolution SHOULD be 20ms (the 10ms default is acceptable)
- Event loop lag p99 MUST be < 100ms under normal conditions `[SRC-004]`
- Event loop lag p99 > 500ms MUST trigger a critical alert `[SRC-004]`

Rationale:
- The event loop is the heart of Node.js. A lag > 100ms means callbacks wait more than 100ms before executing, which translates directly into user latency. A lag > 500ms indicates a severe block (synchronous operation, GC storm).

Enforcement:
- Monitoring: Prometheus metrics via `prom-client` or `@fastify/metrics`
- Alerting: thresholds in the alerting system (Grafana, PagerDuty, etc.)
- Review: verify that no blocking synchronous operation is introduced on the hot path

Exceptions:
- Startup operations (schema compilation, warm-up): lag tolerated during the first 30 seconds.

---

### R-BPERF-02 Event Loop Utilization (ELU)

Requirement:
- ELU MUST be monitored via `eventLoopUtilization()` from `perf_hooks` `[SRC-003]`
- ELU SHOULD stay < 0.7 under nominal conditions `[SRC-004]`
- ELU > 0.85 MUST trigger a warning `[SRC-004]`
- ELU MUST be measured as a delta between two snapshots (not as an absolute value)

Rationale:
- ELU measures the ratio of active time / (active + idle) of the event loop. An ELU of 0.85 means the event loop is busy 85% of the time — little headroom remains to absorb load spikes.

Enforcement:
- Monitoring: exposed via Prometheus metrics
- Alerting: warning threshold at 0.85

Exceptions:
- None.

---

### Garbage Collection & V8 Memory

---

### R-BPERF-03 GC monitoring

Requirement:
- GC events MUST be observed via `PerformanceObserver({ type: 'gc' })` `[SRC-003]`
- The following metrics MUST be exposed: duration by type (Major=1, Minor=2, Incremental=3), frequency, cumulative pause `[SRC-005]`
- Mutator utilization (mu) SHOULD be > 0.95 under nominal conditions `[SRC-005]`
- A mu < 0.5 MUST trigger a critical alert (GC consumes > 50% of CPU time) `[SRC-005]`

Rationale:
- GC pauses translate directly into latency spikes. A frequent Mark-Sweep that does not free memory is the classic sign of a memory leak.

Enforcement:
- Monitoring: GC metrics in the application dashboard
- Alerting: cumulative GC duration / interval
- Review: profiling with `--trace-gc` in staging environments

Exceptions:
- None.

---

### R-BPERF-04 Memory budgets

Requirement:
- `process.memoryUsage()` MUST be exposed (rss, heapTotal, heapUsed, external) `[SRC-004]`
- heapUsed MUST return to a stable baseline after a load spike (a sawtooth pattern is expected) `[SRC-005]`
- Monotonic growth of heapUsed over 15 minutes without returning to baseline MUST trigger a warning (probable leak) `[SRC-004]`
- RSS SHOULD stay < 80% of the memory allocated to the container `[SRC-006]`
- `--max-old-space-size` MUST be configured explicitly in the Dockerfiles/startup scripts `[SRC-006]`
- `--max-semi-space-size` SHOULD be set to 64MB for standard API services, 128MB for high-allocation services (SSR, large payloads) `[SRC-006]`

Rationale:
- Without explicit configuration, V8 in a container can use very low dynamic defaults (1-8MB semi-space), causing very frequent scavenges and a 5-10% throughput degradation. The Platformatic benchmark shows a 9.5% gain on p99 with 128MB Young Gen tuning.

Enforcement:
- CI: verify the presence of the V8 flags in the Dockerfiles or the `start` scripts
- Monitoring: memory metrics in the dashboard
- Alerting: threshold on monotonic heapUsed growth

Exceptions:
- Serverless environments (Lambda, Cloud Functions): the V8 flags are not always configurable — document the limitation.

---

### System Resources (USE Method)

---

### R-BPERF-05 CPU

Requirement:
- Process CPU usage MUST be monitored via `process.cpuUsage()` `[SRC-003]`
- Sustained CPU usage > 70% MUST trigger a warning `[SRC-004]`
- Sustained CPU usage > 90% MUST trigger a critical alert `[SRC-004]`
- Any CPU-intensive operation (crypto, parsing JSON > 1MB, compression) MUST be moved into a Worker Thread `[SRC-007]`

Rationale:
- Node.js is single-threaded. CPU at 90% means the event loop starves — requests pile up, latency explodes in a cascade.

Enforcement:
- Monitoring: process + system CPU metrics
- Review: flag CPU-bound operations in the main thread
- Benchmark: verify with `autocannon` that CPU stays < 70% at the target throughput

Exceptions:
- Startup operations (schema compilation, warm-up) tolerated above the thresholds.

---

### R-BPERF-06 File Descriptors and Active Handles

Requirement:
- The number of active handles SHOULD be monitored `[SRC-001]`
- Connections (DB, Redis, HTTP clients) MUST use a connection pool with a configured max size `[SRC-001]`
- EMFILE/ENFILE errors MUST be alerted immediately `[SRC-001]`
- `ulimit -n` SHOULD be configured to >= 65535 in production `[SRC-001]`

Rationale:
- File descriptors are a finite resource. An unbounded pool or unclosed connections saturate the FDs and cause cascading failures across all I/O.

Enforcement:
- Monitoring: active handles counter
- Infra: ulimit configuration in the Dockerfiles/systemd

Exceptions:
- None.

---

### HTTP Metrics (RED Method)

---

### R-BPERF-07 Per-endpoint latency

Requirement:
- Latency MUST be measured in percentiles: p50, p95, p99 `[SRC-002]`
- Latency MUST NOT be measured only as an average `[SRC-004]`
- Each endpoint MUST have its own latency metrics (not only a global metric) `[SRC-002]`
- The latency SLO MUST be defined per endpoint or per endpoint category

Rationale:
- The average hides outliers. A p50 of 50ms with a p99 of 2s means 1% of users wait 40x longer — invisible in the average.

Enforcement:
- Monitoring: Prometheus histogram per Fastify route
- Plugin: `@fastify/metrics` or equivalent
- Review: verify that new endpoints are covered

Exceptions:
- Healthcheck endpoints are exempt from the SLO.

---

### R-BPERF-08 Throughput and error rate

Requirement:
- The rate (req/s) MUST be monitored per endpoint `[SRC-002]`
- The 5xx error rate MUST be < 1% under nominal conditions `[SRC-002]`
- A 5xx error rate > 5% MUST trigger a critical alert
- The 4xx error rate SHOULD be monitored separately (no automatic alert, but visibility)

Rationale:
- The error rate is the most immediate signal of degradation. The rate helps detect traffic anomalies (DDoS, bot, client regression).

Enforcement:
- Monitoring: Prometheus counters per status code
- Alerting: thresholds on the 5xx / total ratio

Exceptions:
- None.

---

### Fastify-specific

---

### R-BPERF-09 Mandatory output schemas

Requirement:
- Each Fastify route MUST define a `response` schema in its route options `[SRC-008]`
- The schema MUST cover at least status code 200 (or the main expected status) `[SRC-008]`
- Schemas MUST use JSON Schema (compatible with `fast-json-stringify`) `[SRC-008]`

Rationale:
- Without an output schema, Fastify uses the standard `JSON.stringify()`. With a schema, it uses `fast-json-stringify`, which pre-compiles serialization — the official Fastify docs report a "drastic" throughput gain. This is the most accessible and most under-exploited performance lever.

Enforcement:
- Lint: custom ESLint rule or review checklist
- Review: verify the presence of `response` in each route option
- CI: a validation script that scans for routes without an output schema

Exceptions:
- Streaming routes (SSE, WebSocket) or routes returning binary files.

---

### R-BPERF-10 Input validation via JSON Schema

Requirement:
- Each route accepting a body, querystring, or params MUST define a validation schema `[SRC-008]`
- Validation MUST use the built-in Ajv compiler (no manual validation in the handler) `[SRC-008]`
- Async validation ($async Ajv) MUST NOT be used in schemas (DoS risk) `[SRC-008]`
- `allErrors` MUST stay at `false` (the Fastify default — stop at the first error) `[SRC-008]`

Rationale:
- Ajv compiles schemas at startup into ultra-fast functions. Manual validation in the handler is slower and more fragile. The `allErrors: true` option lets an attacker send a huge payload to force full validation.

Enforcement:
- Review: verify that each route with input has a schema
- CI: a script to detect routes without a schema

Exceptions:
- File upload routes (multipart): schema on the metadata, not the binary.

---

### R-BPERF-11 Hooks — scope and discipline

Requirement:
- Global hooks (registered on the root instance) MUST be limited to the strict minimum: logging, auth, CORS, metrics `[SRC-009]`
- Business hooks MUST be encapsulated in their plugin/feature (not on the root instance) `[SRC-009]`
- Each hook SHOULD be measured (execution time) in staging `[SRC-009]`
- Hooks MUST NOT contain CPU-intensive operations or blocking I/O

Rationale:
- Fastify hooks execute serially in the request lifecycle. A global hook runs on EVERY request. A 5ms slow hook on an instance with 10 global hooks adds 50ms of incompressible latency.

Enforcement:
- Review: verify the scope of hooks (global vs encapsulated)
- Profiling: measure hooks in staging with tracing

Exceptions:
- None.

---

### Concurrency & Async Patterns

---

### R-BPERF-12 Backpressure on streams

Requirement:
- Any use of Node.js Streams MUST respect backpressure signals (`drain`, `pause`, `resume`) `[SRC-010]`
- `highWaterMark` SHOULD be configured between 64KB and 512KB depending on the use case `[SRC-010]`
- Streams of large data (files, DB cursors) MUST use the native pipe/pipeline (no manual reading) `[SRC-010]`

Rationale:
- Without backpressure, a fast producer drowns a slow consumer — memory grows unbounded, the GC goes wild (75 collections/min instead of 36), and the process OOMs.

Enforcement:
- Review: verify stream patterns, flag `.on('data')` without backpressure handling
- Test: load test with large payloads

Exceptions:
- Streams of guaranteed small size (< 1MB total): backpressure optional.

---

### R-BPERF-13 Bounded concurrency

Requirement:
- Concurrent calls to external services MUST be bounded (explicit max concurrency) `[SRC-011]`
- `Promise.all()` on collections of variable size MUST use a concurrency limiter (`p-limit`, `p-map`, or a custom pool) `[SRC-011]`
- Requests to external services MUST have an explicit timeout `[SRC-011]`
- A circuit breaker SHOULD be implemented for critical dependencies `[SRC-011]`

Rationale:
- Unbounded concurrency is Node.js's most insidious problem. A `Promise.all(urls.map(fetch))` on 10,000 URLs creates 10,000 simultaneous connections, saturating the FDs, the GC, and probably the target service. A latency increase in a dependency causes a CPU increase in the caller (more in-flight requests = more objects = more GC).

Enforcement:
- Review: flag `Promise.all()` on collections of unbounded size
- Review: verify the presence of timeouts on HTTP/DB calls
- Test: load test simulating a slow dependency

Exceptions:
- None.

---

### R-BPERF-14 Worker Threads for CPU-bound work

Requirement:
- CPU-bound operations (hashing, compression, parsing large JSON, calculations) MUST be executed in Worker Threads `[SRC-007]`
- The number of workers SHOULD be = number of CPU cores - 1 `[SRC-007]`
- Worker <-> main thread communication SHOULD minimize transfers (use SharedArrayBuffer or transferable objects when possible) `[SRC-007]`

Rationale:
- A CPU-bound operation in the main thread blocks the event loop for its entire duration. 100ms of CPU-bound work = 100ms of lag for ALL pending requests.

Enforcement:
- Review: flag CPU-bound operations in route handlers
- Profiling: flamegraph in staging to identify CPU hotspots

Exceptions:
- Operations < 5ms: the worker serialization overhead would exceed the gain.

---

### Benchmarking & Load Testing

---

### R-BPERF-15 Baseline benchmark

Requirement:
- Each service MUST have a load-test script with `autocannon` `[SRC-012]`
- The benchmark MUST measure: req/s, latency p50/p95/p99, errors, memory, CPU `[SRC-012]`
- The baseline MUST be recorded and updated on every architecture change `[SRC-012]`
- A regression of > 10% on throughput or > 20% on p99 MUST be investigated before merge

Rationale:
- The Fastify docs say it explicitly: "you should always benchmark if performance matters to you". Synthetic benchmarks (46k req/s Fastify) do not represent real load. Only an application benchmark with your routes, your schemas, and your dependencies gives a useful measurement.

Enforcement:
- CI: an optional benchmark script (non-blocking, but results archived)
- Review: comparison with the baseline for performance-impacting PRs

Exceptions:
- Low-traffic internal services (< 10 req/s): an initial benchmark is enough, no continuous CI.

---

## Enforcement summary

| Rule | Mechanism | Automated |
|---|---|---|
| R-BPERF-01 | Monitoring + alerting | Yes |
| R-BPERF-02 | Monitoring + alerting | Yes |
| R-BPERF-03 | Monitoring + alerting | Yes |
| R-BPERF-04 | CI (Dockerfile check) + monitoring | Partial |
| R-BPERF-05 | Monitoring + alerting | Yes |
| R-BPERF-06 | Monitoring + infra config | Partial |
| R-BPERF-07 | Monitoring (Prometheus) | Yes |
| R-BPERF-08 | Monitoring + alerting | Yes |
| R-BPERF-09 | Review + CI script | Partial |
| R-BPERF-10 | Review + CI script | Partial |
| R-BPERF-11 | Review + profiling | No |
| R-BPERF-12 | Review + load test | No |
| R-BPERF-13 | Review | No |
| R-BPERF-14 | Review + profiling | No |
| R-BPERF-15 | CI benchmark script | Partial |

## Exceptions process

- Max 90 days, renewable with justification
- Approved by Tech Lead

## Metrics

| Metric | Baseline | Target | Measurement |
|---|---|---|---|
| Event loop lag p99 | — | < 100ms | `monitorEventLoopDelay()` |
| Event loop utilization | — | < 0.7 nominal | `eventLoopUtilization()` |
| GC mutator utilization | — | > 0.95 | `--trace-gc` / PerformanceObserver |
| Monotonic heap growth > 15min | 0 | 0 | Monitoring alert |
| Sustained CPU usage | — | < 70% | `process.cpuUsage()` |
| HTTP latency p99 (per endpoint) | — | Per SLO | Prometheus histogram |
| 5xx error rate | — | < 1% | Prometheus counter |
| Routes without output schema | — | 0 | CI scan |
| Routes without input schema | — | 0 | CI scan |
| Benchmark baseline regression | — | < 10% throughput, < 20% p99 | `autocannon` |

## Sources

- SRC-001 | Brendan Gregg — USE Method | https://www.brendangregg.com/usemethod.html | Primary (author) | Evergreen | Utilization/Saturation/Errors methodology
- SRC-002 | Tom Wilkie — RED Method | https://thenewstack.io/monitoring-microservices-red-method/ | Press | 2015 | Rate/Errors/Duration for microservices
- SRC-003 | Node.js — Performance measurement APIs | https://nodejs.org/api/perf_hooks.html | Primary (official docs) | 2026 | monitorEventLoopDelay, eventLoopUtilization, PerformanceObserver GC
- SRC-004 | Last9 — Node.js Key Metrics | https://last9.io/blog/node-js-key-metrics/ | Expert secondary | 2025 | Thresholds and monitoring best practices
- SRC-005 | Node.js — GC Traces | https://nodejs.org/learn/diagnostics/memory/using-gc-traces | Primary (official docs) | 2026 | GC diagnostics, mutator utilization, leak patterns
- SRC-006 | Platformatic — V8 GC Tuning | https://blog.platformatic.dev/optimizing-nodejs-performance-v8-memory-management-and-gc-tuning | Expert secondary | 2025 | Matteo Collina, Fastify semi-space benchmarks
- SRC-007 | Node.js — Worker Threads | https://nodejs.org/api/worker_threads.html | Primary (official docs) | 2026 | Worker Threads API
- SRC-008 | Fastify — Validation and Serialization | https://fastify.dev/docs/v4.29.x/Reference/Validation-and-Serialization/ | Primary (official docs) | 2025 | Ajv, fast-json-stringify, output schema
- SRC-009 | Fastify — Lifecycle & Hooks | https://fastify.dev/docs/latest/Reference/Lifecycle/ | Primary (official docs) | 2025 | Hook execution order, encapsulation
- SRC-010 | Node.js — Backpressuring in Streams | https://nodejs.org/learn/modules/backpressuring-in-streams | Primary (official docs) | 2026 | Backpressure patterns, highWaterMark
- SRC-011 | Voxer Engineering — Backpressure in Node.js | https://engineering.voxer.com/2013/09/16/backpressure-in-nodejs/ | Expert secondary | 2013 (evergreen) | Unbounded concurrency, limiting patterns
- SRC-012 | Fastify — Benchmarks | https://fastify.dev/benchmarks/ | Primary (official docs) | 2025 | autocannon methodology, synthetic benchmark

## Change log

| Version | Date | Author | Description |
|---|---|---|---|
| 1.0.0 | 2026-04-22 | Claude Code | Initial standard from performance research report |
