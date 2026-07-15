# Docker & Dokploy Expert — Compact Reference

## 1. Compose Patterns

### Network Rules

| Network | Config | Purpose |
|---|---|---|
| `dokploy-network` | `external: true` | Traefik routing (MANDATORY for exposed services) |
| `backend` | `internal: true` | DB/Redis/workers — no internet access |
| `monitoring` | `internal: true` | Prometheus/cAdvisor internal |

### Healthchecks

| Service | Test command | start_period |
|---|---|---|
| PostgreSQL | `pg_isready -U app` | 30s |
| Redis | `redis-cli ping` | — |
| RabbitMQ | `rabbitmq-diagnostics check_running` | 60s |
| Elasticsearch | `curl -sf http://localhost:9200/_cluster/health` | 60s |
| Web app | `wget --spider -q http://localhost:<PORT>/health` | 40s |

### Key Patterns

| Pattern | Compose key | Constraint |
|---|---|---|
| Init/Migration | `depends_on.migrate.condition: service_completed_successfully` | Compose v2.20+ |
| Sidecar (logs) | Shared named volume `:ro` on sidecar | — |
| Worker | Same image, different `command`, no `dokploy-network` | `restart: unless-stopped` |

### Resource Limits (defaults)

| Service | Memory | CPUs |
|---|---|---|
| Web app | 1G | 2.0 |
| Worker | 512M | 1.0 |
| PostgreSQL | 512M-1G | — |
| Redis | 256M | — |

## 2. Security Hardening

### Hardened Service Template

```yaml
image: registry/app:1.2.3          # pinned tag, NEVER :latest
read_only: true
tmpfs: [/tmp, /var/run]
security_opt: [no-new-privileges:true]
cap_drop: [ALL]
cap_add: [NET_BIND_SERVICE]        # only what's needed
user: "1000:1000"
logging: { driver: json-file, options: { max-size: "10m", max-file: "3" } }
```

### Secrets Hierarchy (most to least secure)

1. Docker Swarm Secrets (`/run/secrets/<name>`, encrypted at rest)
2. External secret manager (Vault, AWS SM)
3. BuildKit `--mount=type=secret` (build-time only)
4. `.env` file (in `.gitignore`) / Dokploy File Mounts
5. Environment variables (visible in `docker inspect`) — AVOID

### Network Segmentation Rules

- `expose` (internal) over `ports` (host-bound) — ALWAYS
- DB/Redis/Queue: `backend` only, never `dokploy-network`
- Only Traefik-routed services join `dokploy-network`

### Production Checklist

- [ ] Pinned image versions, multi-stage, alpine/slim/distroless
- [ ] Vuln scan in CI (`trivy image --severity CRITICAL,HIGH --exit-code 1`)
- [ ] Non-root, read_only, no-new-privileges, cap_drop ALL
- [ ] Resource limits (mem+cpu), log rotation, healthchecks
- [ ] Network segmentation, `internal: true` on backend nets
- [ ] No secrets in source/images, `.env` in `.gitignore`

## 3. Swarm Cluster

### Zero-Downtime Deploy Config

```yaml
deploy:
  replicas: 2
  update_config:
    parallelism: 1
    delay: 10s
    failure_action: rollback
    order: start-first          # KEY for zero-downtime
    monitor: 30s
  rollback_config:
    parallelism: 0
    order: stop-first
```

### Placement

| Constraint | Example |
|---|---|
| Role | `node.role == worker` |
| Label | `node.labels.zone == eu-west` |
| Spread | `preferences: [{spread: node.labels.zone}]` |

## 4. Traefik / Dokploy

### Minimal Labels to Expose a Service

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.NAME.rule=Host(`app.example.com`)"
  - "traefik.http.routers.NAME.entrypoints=websecure"
  - "traefik.http.routers.NAME.tls.certresolver=letsencrypt"
  - "traefik.http.services.NAME.loadbalancer.server.port=3000"
```

Router/service names must be **unique** across infra. Convention: `{project}-{service}`.

### Middleware Patterns

| Middleware | Key labels |
|---|---|
| HTTP→HTTPS redirect | `redirectscheme.scheme=https`, `redirectscheme.permanent=true` |
| Rate limit | `ratelimit.average=100`, `ratelimit.burst=50` |
| Basic auth | `basicauth.users=admin:$$apr1$$...` (escape `$` as `$$`) |
| IP whitelist | `ipallowlist.sourcerange=10.0.0.0/8,...` |
| Chain | `routers.NAME.middlewares=redirect-https,ratelimit,compress,security` |

### Security Headers (production)

```yaml
- "traefik.http.middlewares.security.headers.stsSeconds=31536000"
- "traefik.http.middlewares.security.headers.contentTypeNosniff=true"
- "traefik.http.middlewares.security.headers.frameDeny=true"
- "traefik.http.middlewares.security.headers.browserXssFilter=true"
```

## 5. Troubleshooting

### Exit Code Decision Tree

| Exit | Cause | Fix |
|---|---|---|
| 0 | Normal exit | CMD terminates — check entrypoint |
| 1 | App error | `docker logs --tail 50` |
| 137 | OOM Kill | Increase `deploy.resources.limits.memory` |
| 143 | SIGTERM | Normal shutdown by Docker |

### 502 Bad Gateway (most common)

1. App listens on `127.0.0.1` instead of `0.0.0.0` — **#1 cause**
2. Wrong port in `loadbalancer.server.port` label
3. Container not on `dokploy-network`
4. App not ready (`start_period` too short)

Framework bind fixes: Next.js `-H 0.0.0.0` | Express `listen(port, '0.0.0.0')` | Vite `--host 0.0.0.0` | Django `0.0.0.0:8000` | Rails `-b 0.0.0.0` | Go `":8080"`

### SSL Not Generating

- DNS A record must point to server BEFORE adding domain
- Port 80 must be open (HTTP-01 challenge)
- Rate limit: max 5 certs/domain/week
- Wildcard requires DNS challenge, not HTTP

### Diagnostic Commands

```bash
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
docker logs --tail 100 -t <container>
docker inspect <c> | jq '.[0].State.OOMKilled'
docker stats --no-stream
docker exec <c> ss -tlnp                 # verify bind address
```
