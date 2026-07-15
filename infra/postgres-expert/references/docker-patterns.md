# PostgreSQL in Docker — Patterns and configurations

## 1. Basic Docker Compose (dev)

```yaml
services:
  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: appdb
    ports:
      - "5432:5432"  # Expose only in dev
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./db/init:/docker-entrypoint-initdb.d  # Init scripts
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d appdb"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

volumes:
  pgdata:
```

---

## 2. Production Docker Compose (with PgBouncer)

```yaml
services:
  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: appdb
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./postgres.conf:/etc/postgresql/postgresql.conf
    command: postgres -c config_file=/etc/postgresql/postgresql.conf
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d appdb"]
      interval: 10s
      timeout: 5s
      retries: 5
    # NO exposed ports — only PgBouncer is reachable

  pgbouncer:
    image: edoburu/pgbouncer:latest
    restart: unless-stopped
    environment:
      DATABASE_URL: postgres://app:${POSTGRES_PASSWORD}@postgres:5432/appdb
      POOL_MODE: transaction
      MAX_CLIENT_CONN: 200
      DEFAULT_POOL_SIZE: 20
      MIN_POOL_SIZE: 5
    ports:
      - "6432:6432"  # Apps connect here
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  pgdata:
```

**Why PgBouncer:**
- PostgreSQL creates one process per connection (~10MB RAM each)
- When containerized, apps start/stop often → connection churn
- PgBouncer pools connections: 200 clients → 20 real connections
- `transaction` mode: the connection is returned to the pool at the end of each transaction

---

## 3. PostgreSQL configuration (postgresql.conf) for a container

```ini
# === Memory ===
shared_buffers = '256MB'          # 25% of the RAM allocated to the container
effective_cache_size = '768MB'    # 75% of the RAM allocated
work_mem = '8MB'                  # RAM / (max_connections * 4)
maintenance_work_mem = '128MB'

# === Connections ===
max_connections = 50              # Low if PgBouncer is in front (it handles pooling)
listen_addresses = '*'

# === WAL ===
wal_level = replica               # Needed for replication and PITR
max_wal_size = '1GB'
min_wal_size = '80MB'

# === Logging ===
logging_collector = on
log_directory = '/var/log/postgresql'
log_filename = 'postgresql-%Y-%m-%d.log'
log_min_duration_statement = 500  # Log queries > 500ms
log_statement = 'ddl'             # Log all DDL operations
log_connections = on
log_disconnections = on

# === Performance ===
random_page_cost = 1.1            # SSD (default 4.0 is for HDD)
effective_io_concurrency = 200    # SSD
default_statistics_target = 200   # Better planner estimates

# === Autovacuum ===
autovacuum = on
autovacuum_max_workers = 3
autovacuum_naptime = '1min'
autovacuum_vacuum_cost_delay = '2ms'
```

---

## 4. Init script (docker-entrypoint-initdb.d)

Scripts in this folder run **only on first startup** (when the data volume is empty). Order: alphabetical.

```sql
-- 001_extensions.sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 002_schemas.sql
CREATE SCHEMA IF NOT EXISTS app;
ALTER DATABASE appdb SET search_path TO app, public;
```

---

## 5. Automated backup in Docker

```yaml
services:
  pg-backup:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      PGHOST: postgres
      PGUSER: app
      PGPASSWORD: ${POSTGRES_PASSWORD}
      PGDATABASE: appdb
    volumes:
      - pgbackups:/backups
    entrypoint: /bin/sh
    command: >
      -c 'while true; do
        FILENAME="/backups/backup_$$(date +%Y%m%d_%H%M%S).dump";
        pg_dump -Fc -f "$$FILENAME" &&
        echo "Backup created: $$FILENAME" ||
        echo "Backup FAILED";
        find /backups -name "*.dump" -mtime +7 -delete;
        sleep 86400;
      done'
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  pgbackups:
```

---

## 6. Dokploy specifics

In Dokploy, PostgreSQL is deployed as a Docker Compose service:

1. Create a project → add a Compose service
2. Paste the docker-compose.yml (the prod version with PgBouncer if needed)
3. Configure the environment variables in the Dokploy UI
4. The `pgdata` volume is automatically persisted by Docker
5. Internal access: other services on the same Docker network reach it via `postgres:5432`
6. External access (debugging only): expose the port + IP whitelisting via Traefik

**Things to watch out for:**
- Never redeploy a PostgreSQL service without verifying that the volume is preserved
- Use `restart: unless-stopped` (not `always`, which restarts even after a `docker stop`)
- SQL migrations must NOT go in `docker-entrypoint-initdb.d` (which only runs on the first init) — use a separate migration system

---

## 7. Health checks and readiness

```yaml
# For services that depend on PostgreSQL
depends_on:
  postgres:
    condition: service_healthy
```

On the application side, check connectivity before starting:

```bash
# wait-for-pg.sh script
until pg_isready -h "$PGHOST" -p "$PGPORT" -U "$PGUSER"; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done
echo "PostgreSQL is ready"
```
