#!/usr/bin/env bash
# pg-inspect.sh — Read-only PostgreSQL inspector for the postgres-expert skill
# Usage: ./pg-inspect.sh <command> [args...]
# Requires: psql, DATABASE_URL env var or --url argument
#
# Commands:
#   schema              Full schema dump (tables, columns, types, constraints, indexes)
#   schema <table>      Schema for a specific table
#   tables              List all tables with row counts and sizes
#   indexes [table]     List indexes (optionally for a specific table)
#   constraints [table] List constraints (optionally for a specific table)
#   stats               Performance stats (cache hit, dead tuples, connections)
#   slow-queries        Top 20 slow queries (requires pg_stat_statements)
#   locks               Current lock waits
#   activity            Active connections and queries
#   explain <query>     EXPLAIN ANALYZE a query (read-only)
#   sample <table> [n]  Sample rows from a table (default 5)
#   query <sql>         Execute a read-only SQL query
#   extensions          List installed extensions
#   version             PostgreSQL version and config summary

set -euo pipefail

# Parse --url argument or use DATABASE_URL
DB_URL="${DATABASE_URL:-}"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --url)
      DB_URL="$2"
      shift 2
      ;;
    *)
      break
      ;;
  esac
done

if [[ -z "$DB_URL" ]]; then
  echo "ERROR: No database connection. Set DATABASE_URL or pass --url <connection_string>" >&2
  exit 1
fi

COMMAND="${1:-help}"
shift || true

# Read-only psql wrapper
run_sql() {
  psql "$DB_URL" -X -A -t --pset=footer=off -c "SET TRANSACTION READ ONLY; $1" 2>&1
}

# Formatted psql (with headers, aligned)
run_sql_fmt() {
  psql "$DB_URL" -X --pset=footer=off -c "SET TRANSACTION READ ONLY; $1" 2>&1
}

case "$COMMAND" in

  schema)
    TABLE="${1:-}"
    if [[ -n "$TABLE" ]]; then
      echo "=== Schema for table: $TABLE ==="
      run_sql_fmt "
        SELECT column_name, data_type,
          CASE WHEN character_maximum_length IS NOT NULL
               THEN data_type || '(' || character_maximum_length || ')'
               WHEN numeric_precision IS NOT NULL
               THEN data_type || '(' || numeric_precision || ',' || COALESCE(numeric_scale,0) || ')'
               ELSE data_type END AS full_type,
          is_nullable, column_default,
          CASE WHEN is_generated = 'ALWAYS' THEN 'GENERATED' ELSE '' END AS generated
        FROM information_schema.columns
        WHERE table_name = '$TABLE' AND table_schema NOT IN ('pg_catalog', 'information_schema')
        ORDER BY ordinal_position;
      "
      echo ""
      echo "=== Constraints ==="
      run_sql_fmt "
        SELECT tc.constraint_name, tc.constraint_type,
          string_agg(kcu.column_name, ', ' ORDER BY kcu.ordinal_position) AS columns,
          CASE WHEN tc.constraint_type = 'FOREIGN KEY'
               THEN ccu.table_name || '(' || ccu.column_name || ')'
               ELSE '' END AS references_to
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
          ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema
        LEFT JOIN information_schema.constraint_column_usage ccu
          ON tc.constraint_name = ccu.constraint_name AND tc.table_schema = ccu.table_schema
        WHERE tc.table_name = '$TABLE' AND tc.table_schema NOT IN ('pg_catalog', 'information_schema')
        GROUP BY tc.constraint_name, tc.constraint_type, ccu.table_name, ccu.column_name;
      "
      echo ""
      echo "=== Indexes ==="
      run_sql_fmt "
        SELECT indexname, indexdef
        FROM pg_indexes
        WHERE tablename = '$TABLE' AND schemaname NOT IN ('pg_catalog', 'information_schema');
      "
      echo ""
      echo "=== Check constraints ==="
      run_sql_fmt "
        SELECT conname, pg_get_constraintdef(oid) AS definition
        FROM pg_constraint
        WHERE conrelid = '$TABLE'::regclass AND contype = 'c';
      "
    else
      echo "=== Full Schema ==="
      run_sql_fmt "
        SELECT t.table_name,
          string_agg(
            c.column_name || ' ' ||
            CASE WHEN c.character_maximum_length IS NOT NULL
                 THEN c.data_type || '(' || c.character_maximum_length || ')'
                 ELSE c.data_type END ||
            CASE WHEN c.is_nullable = 'NO' THEN ' NOT NULL' ELSE '' END,
            ', ' ORDER BY c.ordinal_position
          ) AS columns
        FROM information_schema.tables t
        JOIN information_schema.columns c ON t.table_name = c.table_name AND t.table_schema = c.table_schema
        WHERE t.table_schema NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
          AND t.table_type = 'BASE TABLE'
        GROUP BY t.table_name
        ORDER BY t.table_name;
      "
    fi
    ;;

  tables)
    echo "=== Tables with sizes and row estimates ==="
    run_sql_fmt "
      SELECT
        schemaname || '.' || relname AS table_name,
        pg_size_pretty(pg_total_relation_size(relid)) AS total_size,
        pg_size_pretty(pg_relation_size(relid)) AS table_size,
        pg_size_pretty(pg_total_relation_size(relid) - pg_relation_size(relid)) AS index_size,
        n_live_tup AS estimated_rows,
        n_dead_tup AS dead_rows
      FROM pg_stat_user_tables
      ORDER BY pg_total_relation_size(relid) DESC;
    "
    ;;

  indexes)
    TABLE="${1:-}"
    WHERE_CLAUSE=""
    if [[ -n "$TABLE" ]]; then
      WHERE_CLAUSE="AND tablename = '$TABLE'"
    fi
    echo "=== Indexes ==="
    run_sql_fmt "
      SELECT
        schemaname, tablename, indexname,
        pg_size_pretty(pg_relation_size(indexrelid)) AS size,
        idx_scan AS scans,
        idx_tup_read AS tuples_read
      FROM pg_stat_user_indexes
      JOIN pg_indexes USING (schemaname, tablename, indexname)
      WHERE schemaname NOT IN ('pg_catalog', 'information_schema') $WHERE_CLAUSE
      ORDER BY pg_relation_size(indexrelid) DESC;
    "
    ;;

  constraints)
    TABLE="${1:-}"
    WHERE_CLAUSE=""
    if [[ -n "$TABLE" ]]; then
      WHERE_CLAUSE="WHERE conrelid = '${TABLE}'::regclass"
    fi
    echo "=== Constraints ==="
    run_sql_fmt "
      SELECT conrelid::regclass AS table_name,
        conname, contype,
        pg_get_constraintdef(oid) AS definition
      FROM pg_constraint
      $WHERE_CLAUSE
      ORDER BY conrelid::regclass::text, contype, conname;
    "
    ;;

  stats)
    echo "=== Cache Hit Ratio ==="
    run_sql_fmt "
      SELECT datname,
        ROUND(100.0 * blks_hit / NULLIF(blks_hit + blks_read, 0), 2) AS cache_hit_pct
      FROM pg_stat_database
      WHERE datname = current_database();
    "
    echo ""
    echo "=== Table Stats (top 20 by dead tuples) ==="
    run_sql_fmt "
      SELECT relname, n_live_tup, n_dead_tup,
        ROUND(100.0 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_pct,
        last_autovacuum, last_autoanalyze
      FROM pg_stat_user_tables
      WHERE n_dead_tup > 0
      ORDER BY n_dead_tup DESC
      LIMIT 20;
    "
    echo ""
    echo "=== Index Usage (low usage = candidates for removal) ==="
    run_sql_fmt "
      SELECT relname, indexrelname, idx_scan,
        pg_size_pretty(pg_relation_size(indexrelid)) AS size
      FROM pg_stat_user_indexes
      WHERE idx_scan < 10
      ORDER BY pg_relation_size(indexrelid) DESC
      LIMIT 20;
    "
    ;;

  slow-queries)
    echo "=== Top 20 Slowest Queries (pg_stat_statements) ==="
    run_sql_fmt "
      SELECT queryid, LEFT(query, 120) AS query,
        calls, ROUND(mean_exec_time::numeric, 2) AS avg_ms,
        ROUND(total_exec_time::numeric / 1000, 2) AS total_sec,
        rows
      FROM pg_stat_statements
      WHERE dbid = (SELECT oid FROM pg_database WHERE datname = current_database())
      ORDER BY mean_exec_time DESC
      LIMIT 20;
    " 2>&1 || echo "pg_stat_statements not installed. Run: CREATE EXTENSION pg_stat_statements;"
    ;;

  locks)
    echo "=== Current Lock Waits ==="
    run_sql_fmt "
      SELECT blocked.pid AS blocked_pid,
        LEFT(blocked.query, 80) AS blocked_query,
        blocked.wait_event_type,
        blocking.pid AS blocking_pid,
        LEFT(blocking.query, 80) AS blocking_query,
        now() - blocked.query_start AS wait_duration
      FROM pg_stat_activity blocked
      JOIN pg_locks bl ON bl.pid = blocked.pid AND NOT bl.granted
      JOIN pg_locks kl ON kl.locktype = bl.locktype
        AND kl.database IS NOT DISTINCT FROM bl.database
        AND kl.relation IS NOT DISTINCT FROM bl.relation
        AND kl.pid != bl.pid AND kl.granted
      JOIN pg_stat_activity blocking ON blocking.pid = kl.pid;
    "
    ;;

  activity)
    echo "=== Active Connections ==="
    run_sql_fmt "
      SELECT pid, usename, client_addr, state,
        now() - query_start AS duration,
        LEFT(query, 100) AS query
      FROM pg_stat_activity
      WHERE datname = current_database()
      ORDER BY
        CASE state WHEN 'active' THEN 0 ELSE 1 END,
        query_start;
    "
    ;;

  explain)
    QUERY="$*"
    if [[ -z "$QUERY" ]]; then
      echo "ERROR: Usage: pg-inspect.sh explain <query>" >&2
      exit 1
    fi
    echo "=== EXPLAIN ANALYZE (read-only) ==="
    # Wrap in read-only transaction + rollback for safety
    psql "$DB_URL" -X -c "
      BEGIN;
      SET TRANSACTION READ ONLY;
      EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) $QUERY;
      ROLLBACK;
    " 2>&1
    ;;

  sample)
    TABLE="${1:-}"
    LIMIT="${2:-5}"
    if [[ -z "$TABLE" ]]; then
      echo "ERROR: Usage: pg-inspect.sh sample <table> [limit]" >&2
      exit 1
    fi
    echo "=== Sample from $TABLE (LIMIT $LIMIT) ==="
    run_sql_fmt "SELECT * FROM $TABLE LIMIT $LIMIT;"
    ;;

  query)
    SQL="$*"
    if [[ -z "$SQL" ]]; then
      echo "ERROR: Usage: pg-inspect.sh query <sql>" >&2
      exit 1
    fi
    run_sql_fmt "$SQL"
    ;;

  extensions)
    echo "=== Installed Extensions ==="
    run_sql_fmt "SELECT extname, extversion, extnamespace::regnamespace AS schema FROM pg_extension ORDER BY extname;"
    ;;

  version)
    echo "=== PostgreSQL Version ==="
    run_sql "SELECT version();"
    echo ""
    echo "=== Key Settings ==="
    run_sql_fmt "
      SELECT name, setting, unit, short_desc
      FROM pg_settings
      WHERE name IN (
        'shared_buffers', 'effective_cache_size', 'work_mem', 'maintenance_work_mem',
        'max_connections', 'max_parallel_workers_per_gather', 'random_page_cost',
        'wal_level', 'max_wal_size', 'autovacuum', 'jit',
        'ssl', 'password_encryption', 'log_min_duration_statement'
      )
      ORDER BY name;
    "
    ;;

  help|*)
    cat <<'USAGE'
pg-inspect.sh — Read-only PostgreSQL inspector

Usage: pg-inspect.sh [--url <connection_string>] <command> [args...]

Commands:
  schema              Full schema (all tables)
  schema <table>      Detailed schema for one table
  tables              Tables with sizes and row counts
  indexes [table]     Index list with usage stats
  constraints [table] Constraint list
  stats               Performance stats (cache, dead tuples, unused indexes)
  slow-queries        Top 20 slow queries (requires pg_stat_statements)
  locks               Current lock waits
  activity            Active connections
  explain <query>     EXPLAIN ANALYZE (read-only, auto-rollback)
  sample <table> [n]  Sample rows (default 5)
  query <sql>         Execute read-only SQL
  extensions          Installed extensions
  version             PG version and key settings

Environment:
  DATABASE_URL        PostgreSQL connection string (or use --url)
USAGE
    ;;
esac
