# Concurrency, parallelism & architecture

## Node.js concurrency patterns

Node.js is single-threaded — the event loop is a cooperative scheduler. But it offers
several parallelism mechanisms, each with its own cost and constraints.

| Mechanism | When to use it | Cost | Common pitfalls |
|---|---|---|---|
| **Event loop (async/await)** | I/O-bound (HTTP, DB, files) | Near-zero | Blocking the loop = blocking everything. Rule: no CPU op >50ms without yielding |
| **Worker threads** | CPU-bound (crypto, parsing, image) | Structured-clone serialization, ~1-5ms/message | For I/O = waste. `SharedArrayBuffer` + `Atomics` for shared memory |
| **Cluster / child_process** | Horizontal multi-core scaling | Full fork, unshared memory, IPC overhead | No shared memory → no race conditions, but memory cost × N |
| **Promise.all / allSettled** | Bounded I/O concurrency | All promises at once | Without a pool (p-limit), 1000 requests = 1000 open connections |
| **Streams (pipeline)** | Large volumes, constant memory | Stream API overhead | Ignoring backpressure = unbounded memory accumulation |

### Concurrency anti-patterns

| Pattern to detect | Problem | Severity |
|---|---|---|
| Sequential `await` on independent operations in `for...of` | Latency = sum instead of max | High |
| `Promise.all` without a pool on a large number of promises | File descriptor saturation, memory spike | High |
| Worker threads for I/O-bound tasks | Serialization overhead with no benefit | Low |
| Missing `AbortController` on concurrent operations | Ghost operations that keep running after timeout/navigation | Medium |
| Hand-rolled mutex (Promise + flag) without timeout | If the lock is never released, the whole chain waits forever | High |
| Shared state modified from async callbacks without coordination | Subtle race conditions — execution order not guaranteed | High |

---

## Race conditions & concurrent access

In Node.js, race conditions come from the **interleaving** of async callbacks,
not from multi-threading. The code between two `await`s is atomic, but the state can
change between two awaits.

| Pattern to detect | Concrete example | Severity |
|---|---|---|
| Non-atomic read-modify-write with an `await` between read and write | `const val = await db.get(key); val.count++; await db.set(key, val);` — between get and set, another callback can modify the data | High |
| Cache invalidation race | Request A reads DB (stale), Request B updates DB + invalidates cache, Request A writes the stale data into the cache | Medium |
| SSE/WebSocket without cleanup in useEffect | If the component unmounts during the connection, the listener stays active | Medium |
| Concurrent upload/processing without idempotence | Two uploads of the same file = duplicates in the DB | High if applicable |

**How to search:** read-modify-write patterns crossing an `await`, caches without
coordination, event listeners without cleanup, mutating operations from concurrent callbacks.

---

## Design patterns & performance impact

The goal isn't to judge the patterns, but to identify when a pattern is
used on a hot path with a disproportionate cost.

| Pattern | Performance cost | When it becomes a problem | Alternative on hot path |
|---|---|---|---|
| **Observer / EventEmitter** | O(n) per notification | >100 listeners on a frequent event (>100/s) | Batching, or a direct call if there's a single consumer |
| **Middleware chain** | O(m) per request | Heavy middlewares applied globally | Scope them to the routes that need them (Fastify hooks) |
| **Repository + DTO mapping** | O(n) allocations — 3 objects per DB row | Lists >100 items = 300+ allocations | Return DB rows directly if the format matches |
| **Strategy** (runtime polymorphism) | O(1) + possible V8 deopt if >4 strategies | V8 megamorphism | Pre-resolve at init, use concrete functions on hot paths |
| **Distributed Pub/Sub** (DB polling/Redis) | Polling latency + network overhead | Polling < 1s on large volumes = constant DB load | Push (PG LISTEN/NOTIFY, Redis Pub/Sub), outbox pattern |
| **Hexagonal architecture** | port → adapter → infra indirections | Unnecessary copies/allocations between layers on hot paths | Pass references instead of DTOs when the format is identical |
