# Docker Standards — LLM Lab

Docker and Docker Compose standards specific to the lab's AI infrastructure.
For generic Docker standards, see the `docker-dokploy-expert` skill.

---

## Core principles

### 1. Ollama outside Docker, everything else inside

Ollama runs **natively on macOS** to access the Metal GPU. All the other services
(LiteLLM, Langfuse, OpenClaw, Postgres, Redis, etc.) run in Docker.

Docker → Ollama communication goes through `host.docker.internal:11434`.
Always declare `extra_hosts` on the services that talk to Ollama:

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

### 2. A dedicated network, not the default one

All the lab services share a bridge network named `llm-lab`.
Never use Docker Compose's `default` network — it is ephemeral
and makes inter-service debugging harder.

```yaml
networks:
  llm-lab:
    driver: bridge
    name: llm-lab
```

### 3. No `ports` unless strictly necessary

Only the services you access from the host expose `ports`:
- LiteLLM `:4000` — gateway API (used by OpenClaw, scripts, evals)
- Langfuse `:3000` — web UI (dashboard)
- OpenClaw `:3007` — UI/API (optional if terminal only)

Internal services (Postgres, Redis, ClickHouse, MinIO) use `expose`
and communicate over the `llm-lab` network by service name.

---

## docker-compose.yml standards

### Versioning and images

```yaml
# ALWAYS pin image versions
# Never :latest outside the initial prototyping phase
services:
  litellm:
    image: ghcr.io/berriai/litellm:main-v1.67.0    # ✅ Pinned
  postgres:
    image: postgres:16-alpine                        # ✅ Major pinned
  redis:
    image: redis:7-alpine                            # ✅ Major pinned

  # ❌ Avoid
  litellm:
    image: ghcr.io/berriai/litellm:latest
```

### Mandatory health checks

Every service must have a health check. Without one, `depends_on`
with `condition: service_healthy` does not work, and the startup order
is non-deterministic.

```yaml
# Postgres pattern
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
  interval: 5s
  timeout: 3s
  retries: 5
  start_period: 10s

# Redis pattern
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 5s
  timeout: 3s
  retries: 5

# HTTP service pattern
healthcheck:
  test: ["CMD", "wget", "--spider", "-q", "http://localhost:PORT/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s

# ClickHouse pattern
healthcheck:
  test: ["CMD", "wget", "--spider", "-q", "http://localhost:8123/ping"]
  interval: 5s
  timeout: 3s
  retries: 5
```

### Startup order

Use `depends_on` with `condition: service_healthy` to guarantee
startup order. Data services (Postgres, Redis, ClickHouse)
start before the application services.

```yaml
litellm:
  depends_on:
    litellm-postgres:
      condition: service_healthy
    litellm-redis:
      condition: service_healthy

langfuse:
  depends_on:
    langfuse-postgres:
      condition: service_healthy
    langfuse-clickhouse:
      condition: service_healthy
    langfuse-redis:
      condition: service_healthy
```

### Named volumes for data

All persistent data goes into a named Docker volume.
No bind mounts for database data — only for configs.

```yaml
volumes:
  # Persistent data → named volumes
  litellm-pg-data:
  langfuse-pg-data:
  langfuse-ch-data:
  langfuse-minio-data:

services:
  litellm-postgres:
    volumes:
      - litellm-pg-data:/var/lib/postgresql/data    # ✅ Named volume

  litellm:
    volumes:
      - ./litellm-config.yaml:/app/config.yaml:ro   # ✅ Read-only bind mount for config
```

### Resource limits

On the Mac Studio M3 Ultra (96 GB RAM, 28 cores), the memory budget for Docker
is about 20-25 GB max (the rest for macOS + Ollama + loaded models).

```yaml
services:
  litellm:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: "4.0"
        reservations:
          memory: 512M

  litellm-postgres:
    deploy:
      resources:
        limits:
          memory: 1G

  litellm-redis:
    deploy:
      resources:
        limits:
          memory: 256M

  langfuse:
    deploy:
      resources:
        limits:
          memory: 2G

  langfuse-clickhouse:
    deploy:
      resources:
        limits:
          memory: 4G        # ClickHouse is memory-hungry

  langfuse-postgres:
    deploy:
      resources:
        limits:
          memory: 1G

  langfuse-redis:
    deploy:
      resources:
        limits:
          memory: 256M

  langfuse-minio:
    deploy:
      resources:
        limits:
          memory: 512M

  openclaw:
    deploy:
      resources:
        limits:
          memory: 2G
```

Approximate total budget: ~13 GB for the full stack.

---

## Security standards

### Secrets and environment variables

```bash
# .env — NEVER commit to Git
# Add .env to .gitignore

# API keys
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Internal secrets (generated with openssl rand -hex 32)
LITELLM_MASTER_KEY=sk-...
LANGFUSE_NEXTAUTH_SECRET=...
LANGFUSE_SALT=...

# DB passwords (generated, not defaults)
LITELLM_PG_PASSWORD=...
LANGFUSE_PG_PASSWORD=...
```

Provide a `.env.example` with placeholders (never real values):

```bash
# .env.example — Template, copy to .env and fill in
ANTHROPIC_API_KEY=sk-ant-CHANGE-ME
OPENAI_API_KEY=sk-CHANGE-ME
LITELLM_MASTER_KEY=sk-CHANGE-ME
LANGFUSE_NEXTAUTH_SECRET=GENERATE-WITH-openssl-rand-hex-32
LANGFUSE_SALT=GENERATE-WITH-openssl-rand-hex-32
LITELLM_PG_PASSWORD=GENERATE-STRONG-PASSWORD
LANGFUSE_PG_PASSWORD=GENERATE-STRONG-PASSWORD
```

### Internal network

Databases and support services must NOT be reachable
from outside the Docker network:

```yaml
# ❌ Bad — Postgres reachable from the host
litellm-postgres:
  ports:
    - "5432:5432"

# ✅ Good — Postgres only on the internal network
litellm-postgres:
  expose:
    - "5432"
  networks:
    - llm-lab
```

Exception: Langfuse Postgres on `:5433` can be exposed temporarily
for debugging, but not during normal operation.

### Read-only files

Configuration files mounted as bind mounts must be read-only:

```yaml
volumes:
  - ./litellm-config.yaml:/app/config.yaml:ro     # :ro = read-only
  - ./langfuse-config:/app/config:ro
```

---

## Naming standards

### Services

Prefix services with their "group" to avoid collisions:

```yaml
services:
  # LiteLLM group
  litellm:            # Main service
  litellm-postgres:   # Its database
  litellm-redis:      # Its cache

  # Langfuse group
  langfuse:           # Main service
  langfuse-postgres:  # Its database (different port!)
  langfuse-clickhouse:
  langfuse-redis:
  langfuse-minio:

  # Standalone
  openclaw:
```

### Volumes

Same naming convention as the services:

```yaml
volumes:
  litellm-pg-data:
  langfuse-pg-data:
  langfuse-ch-data:
  langfuse-minio-data:
```

### Ports

Each service has its assigned port, documented in a single place:

| Service | Host port | Internal port | Usage |
|---------|-----------|---------------|-------|
| Ollama (native) | 11434 | — | Inference API |
| LiteLLM | 4000 | 4000 | Gateway API |
| Langfuse | 3000 | 3000 | Observability UI + API |
| OpenClaw | 3007 | 3007 | Skill runtime |
| LiteLLM Postgres | — | 5432 | Internal DB |
| Langfuse Postgres | — | 5432 | Internal DB |
| Langfuse ClickHouse | — | 8123 | Analytics |
| Langfuse MinIO | — | 9000 | Object storage |

---

## Operational standards

### Start and stop

```bash
# Start the whole lab
docker compose -f ~/llm-lab/docker-compose.yml up -d

# Start a specific group (profiles)
docker compose up -d litellm litellm-postgres litellm-redis

# Stop cleanly
docker compose down

# Stop AND delete volumes (full reset)
docker compose down -v     # ⚠️ Destructive — data loss
```

### Logs

```bash
# Logs for one service
docker compose logs litellm --tail 50 -f

# All logs
docker compose logs --tail 20 -f

# Logs with timestamps
docker compose logs -t litellm
```

### Updating a service

```bash
# 1. Check the changelog for the new version
# 2. Update the tag in docker-compose.yml
# 3. Pull and restart
docker compose pull litellm
docker compose up -d litellm

# 4. Check the logs
docker compose logs litellm --tail 20
```

### Data backup

```bash
# Postgres backup (LiteLLM)
docker compose exec litellm-postgres pg_dump -U litellm litellm > backup-litellm-$(date +%F).sql

# Postgres backup (Langfuse)
docker compose exec langfuse-postgres pg_dump -U langfuse langfuse > backup-langfuse-$(date +%F).sql

# Back up all volumes (via docker cp or a volume mount)
```

### Quick monitoring

```bash
# Service status
docker compose ps

# Resource usage
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Docker disk space
docker system df
```

---

## Anti-patterns to avoid

| Anti-pattern | Why it's a problem | Alternative |
|--------------|--------------------|-------------|
| `container_name` in the compose | Prevents scaling, breaks Dokploy logs | Let Docker name it automatically |
| `:latest` on images | Not reproducible, silent breaking changes | Pin the version |
| `restart: always` | Infinite restart loop if the config is broken | `restart: unless-stopped` |
| Postgres without a health check | `depends_on` doesn't guarantee the DB is ready | Always `pg_isready` |
| Bind mount for DB data | POSIX permissions, no native Docker backup | Named volumes |
| Sensitive env vars in the compose | Visible in `docker inspect` | `.env` file + `.gitignore` |
| A single network for everything | No segmentation | One network per logical group |
| No resource limits | One OOM service takes down the whole host | `deploy.resources.limits` |
| `docker compose up` without `-d` | Blocks the terminal, stops on ctrl+c | Always `-d` in production |

---

## Validation template

Before considering a `docker-compose.yml` ready, check:

- [ ] Every image has a pinned version
- [ ] Every service has a health check
- [ ] `depends_on` with `condition: service_healthy` everywhere
- [ ] No `container_name`
- [ ] Named volumes for persistent data
- [ ] Bind mounts as `:ro` for configs
- [ ] Resource limits on every service
- [ ] Secrets in `.env`, never in the compose
- [ ] `.env.example` provided with placeholders
- [ ] Dedicated `llm-lab` network, no `default` network
- [ ] `extra_hosts` for the services that talk to Ollama
- [ ] Ports exposed only for services reachable from the host
