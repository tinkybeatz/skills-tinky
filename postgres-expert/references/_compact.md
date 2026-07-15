# PostgreSQL Expert — Compact Reference

## Types — Decision Matrix

| Need | Type |
|---|---|
| Auto-increment ID | `BIGINT GENERATED ALWAYS AS IDENTITY` |
| Distributed ID | `UUID` via `gen_random_uuid()` |
| Money | `NUMERIC(p,s)` — NEVER `MONEY` or `FLOAT` |
| Text | `TEXT` (not bare `VARCHAR`) |
| Timestamps | `TIMESTAMPTZ` — NEVER `TIMESTAMP` |
| Semi-structured | `JSONB` |
| Small sets | `TEXT[]` / `INTEGER[]` with GIN index |
| Periods | Range types (`TSTZRANGE`, `DATERANGE`) |
| Stable enum | `CREATE TYPE ... AS ENUM` |
| Volatile enum | `TEXT` + `CHECK` |
| Hierarchies | `ltree` extension |

## JSONB Rules

| Criteria | Use columns | Use JSONB |
|---|---|---|
| Known stable schema | Yes | No |
| FK/constraints needed | Yes | No |
| Frequent filtering | Yes (B-tree) | OK (expression index) |
| Variable structure | No | Yes |
| Joins on data | Yes | Avoid |

## Query Patterns

- **NOT IN vs NOT EXISTS:** ALWAYS use `NOT EXISTS`. `NOT IN` returns no rows if subquery contains NULL.
- **CTE (PG12+):** inlined by default. Force `MATERIALIZED` when referenced multiple times or bad planner estimates.
- **Recursive CTE:** always add cycle protection. `UNION` deduplicates; `UNION ALL` risks infinite loops.
- **LATERAL joins:** use for top-N per group, set-returning functions, JSONB unwrapping.
- **Materialized views:** require unique index for `REFRESH CONCURRENTLY`. No auto-refresh — use pg_cron.

## Performance Settings by Workload

| Setting | CRUD | Analytics | Write-heavy |
|---|---|---|---|
| `shared_buffers` | 25% RAM | 25% RAM | 25% RAM |
| `work_mem` | 8MB | 64-256MB | 8MB |
| `random_page_cost` | 1.1 (SSD) | 1.1 | 1.1 |
| Index strategy | B-tree on FK+filters | BRIN on dates | minimal |
| Autovacuum | default | default | aggressive (`cost_delay=0`) |

**Thresholds:** Cache hit > 99%, Index usage > 95%.

## Migration Patterns (Zero-Downtime)

| Operation | Pattern |
|---|---|
| Add column | `ADD COLUMN ... DEFAULT x NOT NULL` (instant PG11+) |
| Backfill | UPDATE by batches of 100k (short txns) |
| Rename column | New col + sync trigger + backfill + deploy new code + drop old |
| Change type (compatible) | Direct: `VARCHAR(N)->TEXT`, `VARCHAR(N)->VARCHAR(M>N)` |
| Change type (incompatible) | New col + conversion trigger + backfill + switch |
| Add NOT NULL | `ADD CHECK (col IS NOT NULL) NOT VALID` → `VALIDATE` → `SET NOT NULL` |
| Add index | `CREATE INDEX CONCURRENTLY` always. If fails: drop invalid, retry |
| Add constraint | `ADD CONSTRAINT ... NOT VALID` then `VALIDATE CONSTRAINT` |

**NEVER** `ALTER TABLE RENAME COLUMN` in production with running app.

## Docker Patterns

**postgresql.conf essentials:**
```
shared_buffers = 25% container RAM
effective_cache_size = 75% container RAM
work_mem = RAM / (max_connections * 4)
random_page_cost = 1.1
max_connections = 50 (low if PgBouncer)
wal_level = replica
log_min_duration_statement = 500
```

**PgBouncer:** 200 clients → 20 real connections. Mode `transaction`.

**Critical rules:**
- Never redeploy PG without verifying volume preservation
- Migrations must NOT go in `initdb.d` (runs once only)
- Healthcheck: `pg_isready -U user -d db`
- Backup: `pg_dump -Fc`, retain 7 days

## Extensions Quick Reference

| Need | Extension |
|---|---|
| Slow queries | `pg_stat_statements` (always in prod) |
| Fuzzy search | `pg_trgm` + GIN index |
| Semantic search / AI | `pgvector` (HNSW preferred) |
| Hierarchies | `ltree` |
| Geospatial | PostGIS |
| Cron in DB | `pg_cron` |
| Auto partition | `pg_partman` + `pg_cron` |
| Case-insensitive | `citext` |
| UUID v4 | Built-in `gen_random_uuid()` (PG13+) |
