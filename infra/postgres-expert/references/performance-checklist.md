# PostgreSQL Performance Checklist

## Quick diagnostic

```sql
-- 1. Cache hit ratio (should be > 99%)
SELECT
  datname,
  ROUND(100.0 * blks_hit / NULLIF(blks_hit + blks_read, 0), 2) AS cache_hit_pct
FROM pg_stat_database
WHERE datname = current_database();

-- 2. Index usage ratio (should be > 95%)
SELECT
  schemaname, relname,
  ROUND(100.0 * idx_scan / NULLIF(seq_scan + idx_scan, 0), 2) AS idx_usage_pct,
  seq_scan, idx_scan
FROM pg_stat_user_tables
WHERE seq_scan + idx_scan > 100
ORDER BY idx_usage_pct ASC NULLS FIRST;

-- 3. Tables with the most dead tuples (need VACUUM)
SELECT
  schemaname, relname,
  n_dead_tup,
  n_live_tup,
  ROUND(100.0 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_pct,
  last_autovacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC
LIMIT 20;

-- 4. Slowest queries (requires pg_stat_statements)
SELECT
  queryid,
  LEFT(query, 80) AS query_preview,
  calls,
  ROUND(mean_exec_time::numeric, 2) AS avg_ms,
  ROUND(total_exec_time::numeric / 1000, 2) AS total_sec
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;

-- 5. Unused indexes (candidates for removal)
SELECT
  schemaname, relname, indexrelname,
  idx_scan,
  pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
AND schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_relation_size(indexrelid) DESC;

-- 6. Table and index sizes
SELECT
  relname,
  pg_size_pretty(pg_total_relation_size(relid)) AS total_size,
  pg_size_pretty(pg_relation_size(relid)) AS table_size,
  pg_size_pretty(pg_total_relation_size(relid) - pg_relation_size(relid)) AS index_size
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC
LIMIT 20;

-- 7. Active connections
SELECT
  state,
  COUNT(*) AS count,
  MAX(now() - query_start) AS max_duration
FROM pg_stat_activity
WHERE datname = current_database()
GROUP BY state;

-- 8. Lock waits
SELECT
  blocked.pid AS blocked_pid,
  blocked.query AS blocked_query,
  blocking.pid AS blocking_pid,
  blocking.query AS blocking_query
FROM pg_stat_activity blocked
JOIN pg_locks bl ON bl.pid = blocked.pid
JOIN pg_locks kl ON kl.locktype = bl.locktype
  AND kl.database IS NOT DISTINCT FROM bl.database
  AND kl.relation IS NOT DISTINCT FROM bl.relation
  AND kl.page IS NOT DISTINCT FROM bl.page
  AND kl.tuple IS NOT DISTINCT FROM bl.tuple
  AND kl.virtualxid IS NOT DISTINCT FROM bl.virtualxid
  AND kl.transactionid IS NOT DISTINCT FROM bl.transactionid
  AND kl.pid != bl.pid
JOIN pg_stat_activity blocking ON blocking.pid = kl.pid
WHERE NOT bl.granted;
```

## Checklist by use case

### Classic CRUD web app
- [ ] `shared_buffers` = 25% RAM
- [ ] `random_page_cost` = 1.1 (SSD)
- [ ] PgBouncer in `transaction` mode
- [ ] Index on every FK
- [ ] Index on frequently filtered columns (status, created_at, user_id)
- [ ] `pg_stat_statements` enabled
- [ ] Autovacuum active and not throttled
- [ ] Log queries > 500ms

### Reporting / Analytics
- [ ] Higher `work_mem` (64MB-256MB) for sorts and hash joins
- [ ] `effective_io_concurrency` = 200 (SSD)
- [ ] BRIN indexes on date columns
- [ ] Consider partitioning by date if > 100M rows
- [ ] Materialized views for frequent aggregations
- [ ] Dedicated read replica for reporting

### Write-heavy (queues, logs, events)
- [ ] Increased `max_wal_size` (2-4GB)
- [ ] Aggressive autovacuum (`autovacuum_vacuum_cost_delay = 0`)
- [ ] Batch inserts instead of row-by-row
- [ ] `UNLOGGED TABLE` if data loss is acceptable (e.g. cache, sessions)
- [ ] Partitioning + DROP PARTITION for purging (instead of DELETE)
- [ ] `synchronous_commit = off` if losing 1-2 seconds of data is acceptable

### JSONB-heavy
- [ ] GIN index on the JSONB columns that are queried
- [ ] `jsonb_path_ops` for `@>` queries only (more compact than the default GIN)
- [ ] Extract frequently filtered fields into dedicated columns
- [ ] Do not store large blobs in JSONB (use separate columns)
