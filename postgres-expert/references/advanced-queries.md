# Advanced query patterns and PostgreSQL features

## JIT (Just-In-Time Compilation)

**What it is:** LLVM compilation of expressions and tuple deforming into native machine code at runtime. Enabled by default since PG12 when the estimated cost exceeds `jit_above_cost`.

**When to use it:** Long-running analytical queries processing millions of rows.

**When to disable it:**
```sql
-- OLTP workloads where JIT overhead > the gain
SET jit = off;
```

**Pitfalls:** JIT compilation time can make short OLTP queries slower. Monitor with EXPLAIN (the JIT section shows compilation time vs execution time).

---

## Parallel Queries

**What it is:** PostgreSQL can parallelize seq scans, aggregations, hash joins, and B-tree index scans across multiple workers.

**Config:**
```
max_parallel_workers_per_gather = 2-4  -- workers per query
max_worker_processes = 8               -- total system workers
max_parallel_workers = 8               -- workers available for queries
min_parallel_table_scan_size = 8MB     -- trigger threshold
```

**When it does not work:**
- Inside a transaction with a cursor or `FOR UPDATE`
- Tables below the `min_parallel_table_scan_size` threshold
- Functions marked `PARALLEL UNSAFE`

---

## CTEs: Materialized vs Not Materialized

Since PG12, CTEs are inlined by default (optimized like subqueries).

```sql
-- Inlined (default PG12+) — the planner optimizes across the CTE
WITH active_users AS (
  SELECT * FROM users WHERE active = true
)
SELECT * FROM active_users WHERE created_at > '2025-01-01';

-- Forced materialized — executed once, result stored in memory
WITH active_users AS MATERIALIZED (
  SELECT * FROM users WHERE active = true
)
SELECT * FROM active_users WHERE created_at > '2025-01-01';
```

**When to materialize:**
- The CTE is referenced multiple times in the query
- To work around a bad planner estimate
- The CTE has side effects (INSERT/UPDATE/DELETE)

**Pitfalls:** Recursive CTEs (`WITH RECURSIVE`) are always materialized.

---

## Recursive CTEs

```sql
-- Organization hierarchy
WITH RECURSIVE org_tree AS (
  -- Base: the root manager
  SELECT id, name, manager_id, 0 AS depth, ARRAY[id] AS path
  FROM employees WHERE manager_id IS NULL

  UNION ALL

  -- Recursion: the subordinates
  SELECT e.id, e.name, e.manager_id, t.depth + 1, t.path || e.id
  FROM employees e
  JOIN org_tree t ON e.manager_id = t.id
  WHERE e.id != ALL(t.path)  -- cycle protection
)
SELECT * FROM org_tree ORDER BY path;
```

**Use cases:** Hierarchies, bill of materials, graph traversal, transitive closure, series generation.

**PG14+:** `CYCLE` clause for automatic cycle detection:
```sql
WITH RECURSIVE ... CYCLE id SET is_cycle USING path
```

**Pitfalls:** `UNION` deduplicates (safe but slow); `UNION ALL` does not deduplicate (fast but risks an infinite loop). Performance degrades on deep/wide recursion — consider ltree for pure hierarchies.

---

## Window Functions

```sql
-- Top 3 orders per customer
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY amount DESC) AS rn
  FROM orders
) ranked WHERE rn <= 3;

-- Running total
SELECT date, amount,
  SUM(amount) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM daily_sales;

-- Comparison with the previous value
SELECT date, amount,
  LAG(amount) OVER (ORDER BY date) AS previous_amount,
  amount - LAG(amount) OVER (ORDER BY date) AS diff
FROM daily_sales;
```

**Main functions:** `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `NTILE()`, `LAG()`, `LEAD()`, `FIRST_VALUE()`, `LAST_VALUE()`, `SUM/AVG/COUNT OVER()`.

**Pitfalls:** Each distinct `OVER()` can trigger a separate sort — consolidate with `WINDOW w AS (...)`. Window functions run after WHERE/GROUP BY but before ORDER BY/LIMIT.

---

## LATERAL Joins

```sql
-- Top 3 orders per customer (alternative to window functions)
SELECT c.name, o.*
FROM customers c
CROSS JOIN LATERAL (
  SELECT * FROM orders
  WHERE customer_id = c.id
  ORDER BY amount DESC
  LIMIT 3
) o;

-- Unnest a JSONB array per row
SELECT u.id, u.name, t.tag
FROM users u
CROSS JOIN LATERAL jsonb_array_elements_text(u.tags) AS t(tag);
```

**When to use it:** Top-N per group (with LIMIT), calling set-returning functions with parameters, unwrapping JSONB/arrays.

**Pitfalls:** Can generate nested loops if not controlled well — check EXPLAIN.

---

## NOT IN vs NOT EXISTS

```sql
-- DANGEROUS: if the subquery returns a NULL, nothing matches
SELECT * FROM orders WHERE customer_id NOT IN (SELECT id FROM inactive_customers);

-- SAFE: correct behavior even with NULLs
SELECT * FROM orders o
WHERE NOT EXISTS (SELECT 1 FROM inactive_customers ic WHERE ic.id = o.customer_id);
```

**Rule:** Always prefer `NOT EXISTS` over `NOT IN` with a subquery. Same performance, correct behavior guaranteed.

---

## Materialized Views

```sql
CREATE MATERIALIZED VIEW mv_daily_stats AS
SELECT date_trunc('day', created_at) AS day,
  COUNT(*) AS total_orders,
  SUM(amount) AS total_amount
FROM orders
GROUP BY 1;

-- Index for queries against the view
CREATE UNIQUE INDEX idx_mv_daily_stats_day ON mv_daily_stats (day);

-- Refresh without blocking reads
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_stats;
```

**When to use it:** Expensive aggregations that do not need to be real-time, dashboards, caching FDW data.

**Pitfalls:**
- `REFRESH ... CONCURRENTLY` requires a unique index on the view
- No automatic refresh — use pg_cron
- The data always lags behind the source table

---

## Foreign Data Wrappers (FDW)

```sql
CREATE EXTENSION postgres_fdw;

CREATE SERVER remote_db
  FOREIGN DATA WRAPPER postgres_fdw
  OPTIONS (host 'remote-host', dbname 'other_db', port '5432');

CREATE USER MAPPING FOR app_user
  SERVER remote_db
  OPTIONS (user 'remote_user', password 'xxx');

CREATE FOREIGN TABLE remote_orders (
  id BIGINT, customer_id BIGINT, amount NUMERIC
) SERVER remote_db OPTIONS (table_name 'orders');

-- Usable like a local table
SELECT * FROM remote_orders WHERE customer_id = 42;
```

**Use cases:** Cross-database queries, gradual migration, data federation, access to MySQL/MongoDB/CSV.

**Pitfalls:**
- WHERE pushdown is limited — complex predicates are evaluated locally after fetching all rows
- No cross-database MVCC guarantee
- Combine with materialized views to cache remote data

---

## LISTEN/NOTIFY

```sql
-- Listener side (connected app)
LISTEN order_created;

-- Sender side (trigger or application)
NOTIFY order_created, '{"order_id": 123, "amount": 45.99}';
-- or
SELECT pg_notify('order_created', '{"order_id": 123}');
```

**Use cases:** Cache invalidation, job queue signaling, real-time updates to the app.

**Pitfalls:**
- Notifications are lost if no one is listening at the time they are sent
- Does NOT work with PgBouncer in transaction mode (the connection is shared)
- Payload limited to 8000 bytes (use JSON)
- No persistence — for reliable messaging, combine with a queue table

---

## Upgrade Strategies

### pg_upgrade (in-place)
```bash
# Preliminary check
pg_upgrade --old-datadir=/old --new-datadir=/new --check

# Upgrade with hard links (near-instant)
pg_upgrade --old-datadir=/old --new-datadir=/new --link

# Mandatory post-upgrade
vacuumdb --all --analyze-in-stages
```

**Downtime:** Minutes with `--link`, hours without. Always `ANALYZE` after an upgrade.

### Logical replication upgrade (near-zero downtime)
1. Install the new version in parallel
2. Configure logical replication old → new
3. Wait for it to catch up
4. Switch the application connections over
5. PG17: `pg_createsubscriber` simplifies creating a logical replica from a physical standby

### Dump/restore
The slowest but most compatible. Required for very old versions or when pg_upgrade is not feasible.

---

## Notable PG17 features

| Feature | Description |
|---|---|
| Incremental backup | Native support in pg_basebackup (no more need for external tools) |
| Logical replication failover slots | `sync_replication_slots` syncs logical slots to the standbys |
| `pg_createsubscriber` | Creates a logical replica from a physical standby |
| `JSON_TABLE()` | JSON → relational conversion |
| `MERGE RETURNING` | MERGE with a RETURNING clause |
| EXPLAIN SERIALIZE/MEMORY | Deeper query analysis |
| Parallel BRIN builds | Building BRIN indexes in parallel |
| `pg_wait_events` | System view for wait event analysis |
| IN() optimization | Better use of B-trees for IN() lists |
