# Backend patterns — Detection reference

## Database queries

| Pattern to detect | Why it's a problem | Severity |
|---|---|---|
| N+1 queries (a loop that runs one query per iteration) | Latency scales linearly with the number of elements | Critical |
| `SELECT *` instead of selecting specific columns | Unnecessary data transfer, wasted memory | Medium |
| Queries without an index on the filtered/sorted columns | Full table scan, latency grows with size | High |
| No pagination on list endpoints | Memory and network load proportional to the total data | High |
| Transactions that are too long or nested | Lock contention, potential deadlocks | High |
| Queries inside loops (`for...of` with `await query`) | Sequential instead of batched, cumulative latency | Critical |

**How to search:** scan the repository/service/controller files,
look for ORM patterns (Prisma, TypeORM, Sequelize, Knex), identify loops
containing DB calls.

## API & Architecture

| Pattern to detect | Why it's a problem | Severity |
|---|---|---|
| Endpoints without caching (no HTTP cache headers, no application cache) | Every request recomputes everything from the DB | Medium |
| No compression (gzip/brotli) on responses | Wasted bandwidth, longer transfer time | Medium |
| Heavy middlewares applied globally (auth, verbose logging) | Overhead on every request, even those that don't need it | Low |
| Cascading synchronous API calls (waterfall) | Latency = sum of the calls instead of the max | High |
| No timeout on external calls (HTTP, DB) | A slow service blocks everything | High |
| Missing or duplicated payload validation | Either a crash on invalid input, or wasted CPU | Medium |

## Memory & Event Loop

| Pattern to detect | Why it's a problem | Severity |
|---|---|---|
| In-memory caches with no size limit (a Map/Object that keeps growing) | Progressive memory leak → OOM crash | Critical |
| Event listeners added without cleanup (`.on()` without `.off()`) | Memory leak + accumulated callbacks | High |
| `setInterval`/`setTimeout` without `clearInterval`/`clearTimeout` | Zombie timers, memory leak | High |
| Heavy synchronous operations on the main thread (crypto, JSON.parse of large payloads) | Blocks the event loop → every request waits | Critical |
| Unclosed streams (files, DB connections) | Exhausted file descriptors, memory leak | High |
| Global variables accumulating data | Never garbage collected | Medium |
