# Langfuse — Configuration reference

## Role in the lab

Langfuse captures every LLM trace that passes through LiteLLM. It provides:
- End-to-end tracing (prompt → response, with latency and cost)
- Prompt versioning and playground
- Metrics per model, per skill, per time period
- Full data ownership (self-hosted, MIT)

## Docker Compose (Langfuse v3)

```yaml
langfuse:
  image: langfuse/langfuse:3
  ports:
    - "3000:3000"
  environment:
    - DATABASE_URL=postgresql://langfuse:langfuse@langfuse-postgres:5433/langfuse
    - CLICKHOUSE_URL=http://langfuse-clickhouse:8123
    - REDIS_HOST=langfuse-redis
    - REDIS_PORT=6379
    - S3_ENDPOINT=http://langfuse-minio:9000
    - S3_ACCESS_KEY_ID=minioadmin
    - S3_SECRET_ACCESS_KEY=minioadmin
    - S3_BUCKET_NAME=langfuse
    - NEXTAUTH_SECRET=langfuse-secret-CHANGE-ME
    - NEXTAUTH_URL=http://localhost:3000
    - SALT=salt-CHANGE-ME
  depends_on:
    langfuse-postgres:
      condition: service_healthy
    langfuse-clickhouse:
      condition: service_healthy
    langfuse-redis:
      condition: service_healthy
  networks:
    - llm-lab

langfuse-postgres:
  image: postgres:16-alpine
  environment:
    POSTGRES_DB: langfuse
    POSTGRES_USER: langfuse
    POSTGRES_PASSWORD: langfuse
  ports:
    - "5433:5432"  # Different port from the LiteLLM Postgres
  volumes:
    - langfuse-pg-data:/var/lib/postgresql/data
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U langfuse"]
    interval: 5s
    timeout: 3s
    retries: 5
  networks:
    - llm-lab

langfuse-clickhouse:
  image: clickhouse/clickhouse-server:24
  volumes:
    - langfuse-ch-data:/var/lib/clickhouse
  healthcheck:
    test: ["CMD", "wget", "--spider", "-q", "http://localhost:8123/ping"]
    interval: 5s
    timeout: 3s
    retries: 5
  networks:
    - llm-lab

langfuse-redis:
  image: redis:7-alpine
  healthcheck:
    test: ["CMD", "redis-cli", "ping"]
    interval: 5s
    timeout: 3s
    retries: 5
  networks:
    - llm-lab

langfuse-minio:
  image: minio/minio
  command: server /data --console-address ":9001"
  environment:
    MINIO_ROOT_USER: minioadmin
    MINIO_ROOT_PASSWORD: minioadmin
  volumes:
    - langfuse-minio-data:/data
  networks:
    - llm-lab
```

## Integration with LiteLLM

The integration is automatic via LiteLLM callbacks.

In `litellm-config.yaml`:
```yaml
litellm_settings:
  success_callback: ["langfuse"]
  failure_callback: ["langfuse"]
```

In `.env`:
```bash
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=http://langfuse:3000
```

The Langfuse API keys are created in the UI: `http://localhost:3000` → Settings → API Keys.

## First startup

1. `docker compose up langfuse langfuse-postgres langfuse-clickhouse langfuse-redis langfuse-minio`
2. Open `http://localhost:3000`
3. Create an admin account
4. Settings → API Keys → Create a key pair
5. Copy `pk-lf-...` and `sk-lf-...` into `.env`
6. Restart LiteLLM to load the keys

## What we observe

| Metric | Usefulness in the lab |
|--------|-----------------------|
| **Latency per model** | Compare response time local vs cloud |
| **Input/output tokens** | Identify models that are too verbose |
| **Cost per request** | Optimize routing (local = free, cloud = paid) |
| **Traces per skill** | See what each skill generates on which model |
| **Error rate** | Detect models that are unstable on certain prompts |

## Recommended dashboards

After a few days of use, create views:
- **Monthly cost per provider** (cloud vs local)
- **p50/p95 latency per model**
- **Request volume per skill**
- **Success/failure rate per model**
