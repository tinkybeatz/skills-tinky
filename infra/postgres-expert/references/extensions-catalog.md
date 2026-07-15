# PostgreSQL extension catalog

## Essential extensions (enable in production)

### pg_stat_statements
**What it is:** Tracks execution statistics for all SQL queries (calls, total time, rows, buffers).

**When to use it:** Always in production. It is the first tool for identifying slow or overly frequent queries.

**Setup:**
```
-- postgresql.conf
shared_preload_libraries = 'pg_stat_statements'
-- Requires a restart

CREATE EXTENSION pg_stat_statements;
```

**Useful query:**
```sql
SELECT queryid, LEFT(query, 80) AS query,
  calls, ROUND(mean_exec_time::numeric, 2) AS avg_ms,
  ROUND(total_exec_time::numeric / 1000, 2) AS total_sec
FROM pg_stat_statements
ORDER BY total_exec_time DESC LIMIT 20;
```

**Pitfalls:** Reset periodically with `pg_stat_statements_reset()` to avoid unbounded growth. PG17 adds more detailed stats.

---

### pgAudit
**What it is:** Detailed audit logging for compliance (SOX, HIPAA, PCI-DSS). Logs SELECT, DML, DDL, ROLE.

**When to use it:** Regulated environments that require an audit trail.

**Setup:**
```
shared_preload_libraries = 'pgaudit'
pgaudit.log = 'write, ddl, role'
```

**Pitfalls:** Logging all SELECTs generates a massive volume. Start with `write, ddl, role`. The logs go into standard PostgreSQL logging — configure rotation.

---

## Extensions for search and text

### pg_trgm
**What it is:** Trigram similarity. Supports `%` (similarity), `<->` (word_similarity), and GIN/GiST indexing for `LIKE '%pattern%'`.

**When to use it:** Fuzzy search, autocomplete, `LIKE/ILIKE` that cannot use a standard B-tree.

**Example:**
```sql
CREATE EXTENSION pg_trgm;
CREATE INDEX idx_users_name_trgm ON users USING gin (name gin_trgm_ops);

-- Fuzzy search
SELECT * FROM users WHERE name % 'Cristoph' ORDER BY similarity(name, 'Cristoph') DESC;

-- LIKE with an index
SELECT * FROM users WHERE name ILIKE '%pont%';
```

**Pitfalls:** Trigram GIN indexes can be large on long TEXT columns. Tune `pg_trgm.similarity_threshold` to control sensitivity.

---

### citext
**What it is:** Case-insensitive TEXT type. Comparisons and indexing are case-insensitive without needing `lower()`.

**When to use it:** Emails, usernames, any column that needs case-insensitive uniqueness.

```sql
CREATE EXTENSION citext;
ALTER TABLE users ALTER COLUMN email TYPE citext;
-- The unique index works natively as case-insensitive
```

**Pitfalls:** Behavior depends on the locale. Slightly slower than TEXT + an expression index.

---

### ltree
**What it is:** A type for hierarchical paths: `Europe.France.Paris`. Supports `@>`, `<@` and GiST indexing.

**When to use it:** Category trees, organizational hierarchies, file paths.

```sql
CREATE EXTENSION ltree;
ALTER TABLE categories ADD COLUMN path ltree;

-- All descendants of Europe.France
SELECT * FROM categories WHERE path <@ 'Europe.France';
```

**Pitfalls:** Labels are limited to alphanumerics + underscore (no hyphens).

---

## Extensions for AI and vectors

### pgvector
**What it is:** Vector similarity search for AI/ML embeddings. Supports L2, inner product, and cosine with IVFFlat and HNSW indexes.

**When to use it:** RAG, semantic search, recommendations, anything using embeddings.

```sql
CREATE EXTENSION vector;
ALTER TABLE documents ADD COLUMN embedding vector(1536);

-- HNSW index (recommended for most cases)
CREATE INDEX idx_docs_embedding ON documents
  USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);

-- Cosine similarity search
SELECT * FROM documents
ORDER BY embedding <=> '[0.1, 0.2, ...]'::vector
LIMIT 10;
```

**Pitfalls:**
- HNSW is memory-intensive at build time (`maintenance_work_mem` matters)
- IVFFlat needs training data; HNSW is preferred (better recall, no training)
- pgvectorscale (Timescale) adds StreamingDiskANN for better performance at scale

---

## Extensions for time management and partitioning

### pg_cron
**What it is:** A cron scheduler built into PostgreSQL. Schedules SQL jobs with cron syntax.

**When to use it:** Automated DB maintenance, periodic aggregation, partition management.

```sql
CREATE EXTENSION pg_cron;

-- VACUUM ANALYZE every night at 3 AM
SELECT cron.schedule('nightly-vacuum', '0 3 * * *', 'VACUUM ANALYZE');

-- Purge old jobs every Sunday
SELECT cron.schedule('weekly-purge', '0 4 * * 0',
  $$DELETE FROM email_jobs WHERE status = 'sent' AND processed_at < NOW() - INTERVAL '30 days'$$);
```

**Pitfalls:** Runs as a background worker on a single database (the one where it is installed). Jobs must be idempotent. Long-running jobs can overlap.

---

### pg_partman
**What it is:** Automated partition management: creating future partitions, detaching/dropping old ones according to retention policies.

**When to use it:** Any partitioned table where manual creation/deletion is tedious (time-series).

```sql
CREATE EXTENSION pg_partman;

-- Configure automatic management
SELECT partman.create_parent(
  p_parent_table := 'public.events',
  p_control := 'created_at',
  p_type := 'range',
  p_interval := '1 month',
  p_premake := 3
);

-- With pg_cron for maintenance
SELECT cron.schedule('partman-maintenance', '0 1 * * *',
  $$SELECT partman.run_maintenance()$$);
```

**Pitfalls:** Configure `premake` (how many partitions to create ahead) and retention correctly. Works well with pg_cron for scheduling.

---

## Geospatial extensions

### PostGIS
**What it is:** ~1000 spatial functions, GEOMETRY/GEOGRAPHY types, GiST/SP-GiST indexes for geographic queries.

**When to use it:** Location-based applications, distance calculations, polygons, routing.

```sql
CREATE EXTENSION postgis;

-- Distance between two points
SELECT ST_Distance(
  ST_MakePoint(2.3522, 48.8566)::geography,  -- Paris
  ST_MakePoint(-0.5792, 44.8378)::geography   -- Bordeaux
) / 1000 AS distance_km;
```

**Pitfalls:** GEOGRAPHY (spheroidal, precise) is slower than GEOMETRY (planar). Choose the right SRID.

---

## Crypto and security extensions

### pgcrypto
**What it is:** Cryptographic functions: `gen_random_bytes()`, `crypt()/gen_salt()` for password hashing, `pgp_sym_encrypt/decrypt` for symmetric encryption.

**When to use it:** Password hashing, encryption of PII at rest.

**Pitfalls:** Key management is the real challenge — keys in SQL queries show up in the logs. Use keys on the application side.

---

## Monitoring extensions

### TimescaleDB
**What it is:** A time-series extension: hypertables (automatic partitioning), compression (up to 90%), continuous aggregates, retention policies.

**When to use it:** IoT, metrics, logs, financial time-series — any append-heavy, time-ordered workload.

**Pitfalls:** License changed (TSL for some features). Compression is columnar and immutable (decompress to modify). Continuous aggregates have a refresh delay.

---

## Quick decision matrix

| Need | Extension |
|---|---|
| Identify slow queries | pg_stat_statements |
| Fuzzy search / autocomplete | pg_trgm |
| Semantic search / AI | pgvector |
| Hierarchies / trees | ltree |
| Geolocation | PostGIS |
| Compliance audit | pgAudit |
| Cron jobs in the DB | pg_cron |
| Automatic partition management | pg_partman |
| Time-series at scale | TimescaleDB |
| Case-insensitive emails | citext |
| Encryption at rest | pgcrypto |
| UUID v4 (PG13+) | None (built-in `gen_random_uuid()`) |
