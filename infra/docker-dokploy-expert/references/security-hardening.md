# Docker Security & Hardening

## Table of contents

1. [Container hardening](#container-hardening)
2. [Image scanning](#image-scanning)
3. [Secrets management](#secrets)
4. [Network security](#network-security)
5. [Docker Bench for Security](#docker-bench-for-security)
6. [Production checklist](#production-checklist)

---

## Container hardening

### Complete config for a hardened service

```yaml
services:
  app:
    image: myregistry/myapp:1.2.3    # Pinned version, never :latest
    read_only: true                    # Read-only filesystem
    tmpfs:
      - /tmp                           # Only /tmp is writable
      - /var/run                       # For PID files if needed
    security_opt:
      - no-new-privileges:true         # Prevents sudo, setuid, etc.
    cap_drop:
      - ALL                            # Drops all Linux capabilities
    cap_add:
      - NET_BIND_SERVICE               # Only what's needed
    user: "1000:1000"                  # Non-root (UID:GID)
    deploy:
      resources:
        limits:
          memory: 1G                   # Memory limit (OOM-kill if exceeded)
          cpus: "2.0"                  # CPU limit
    logging:
      driver: json-file
      options:
        max-size: "10m"                # Log rotation
        max-file: "3"
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Linux capabilities

By default, Docker grants ~14 capabilities. Best practice: drop them all, then add back only what's necessary.

| Capability | Use |
|---|---|
| `NET_BIND_SERVICE` | Bind to ports < 1024 |
| `CHOWN` | Change file ownership |
| `SETUID` / `SETGID` | Change user (needed by some init systems) |
| `DAC_OVERRIDE` | Bypass file permissions |
| `SYS_PTRACE` | Debugging (NEVER in production) |

### Non-root execution

```dockerfile
# In the Dockerfile
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
# ... copy files with --chown=appuser:appgroup ...
USER appuser
```

If the base image doesn't support it, use `user: "1000:1000"` in the compose file.

---

## Image scanning

### Tools

| Tool | Command | Notes |
|---|---|---|
| **Docker Scout** | `docker scout cves myimage:latest` | Built into Docker Desktop/CLI |
| **Trivy** | `trivy image myimage:latest` | Open source (Aqua Security), scans OS + dependencies |
| **Grype** | `grype myimage:latest` | Open source (Anchore) |
| **Snyk** | `snyk container test myimage:latest` | Commercial, native CI/CD integration |

### CI/CD integration

```yaml
# GitHub Actions - scan with Trivy
- name: Scan Docker image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: myimage:${{ github.sha }}
    format: "sarif"
    output: "trivy-results.sarif"
    severity: "CRITICAL,HIGH"
    exit-code: "1"  # Fail the build on critical vulnerabilities
```

### Image best practices

- **Pin versions**: `node:20.11.1-alpine3.19`, not `node:20` or `node:latest`
- **Minimal images**: `alpine` (5MB), `slim` (50MB), `distroless` (Google, no shell)
- **Multi-stage builds**: copy only the necessary artifacts into the final image
- **No dev packages in production**: `npm ci --only=production`, `pip install --no-dev`
- **Scan regularly**: even existing images (new CVEs are published every day)

---

## Secrets

### Method hierarchy (most to least secure)

1. **Docker Swarm Secrets** — encrypted at rest, tmpfs, controlled access
2. **External Vault / Secret Manager** — (HashiCorp Vault, AWS Secrets Manager, etc.)
3. **Build-time secrets** (BuildKit `--mount=type=secret`) — not in the final image
4. **Secret files outside the repo** — `.env` in `.gitignore`, Dokploy File Mounts
5. **Environment variables** — visible in `docker inspect`, logs, process list

### Docker Swarm Secrets

```bash
# Create
echo "supersecretpassword" | docker secret create db_password -
printf "supersecretpassword" | docker secret create db_password -

# From a file
docker secret create tls_cert ./cert.pem
```

```yaml
services:
  app:
    secrets:
      - db_password
    environment:
      # The app reads the secret from the file
      DATABASE_PASSWORD_FILE: /run/secrets/db_password

secrets:
  db_password:
    external: true
```

The application must support reading from a file. Common pattern:
```javascript
const password = process.env.DATABASE_PASSWORD_FILE
  ? fs.readFileSync(process.env.DATABASE_PASSWORD_FILE, 'utf8').trim()
  : process.env.DATABASE_PASSWORD;
```

### Build-time secrets (BuildKit)

```dockerfile
# Dockerfile
RUN --mount=type=secret,id=npm_token \
    NPM_TOKEN=$(cat /run/secrets/npm_token) npm ci
```

```bash
# Build
docker build --secret id=npm_token,src=./.npmrc .
```

The secret is **never** in the final image or in any layer.

### Dokploy Build Secrets

In the Dokploy UI: Application → Environment → Build-time Secrets. They are passed as `--mount=type=secret` and do not persist in the image.

### What you must NEVER do

```dockerfile
# NEVER: the secret ends up in the image
ENV API_KEY=sk-live-xxx
COPY .env /app/.env
ARG SECRET_KEY
RUN echo $SECRET_KEY > /app/config
```

---

## Network security

### Segmentation

```yaml
networks:
  # Public network: connected to Traefik
  frontend:
    driver: bridge

  # Internal network: no Internet access
  backend:
    driver: bridge
    internal: true    # ← blocks all outbound access

  # Dokploy network: for Traefik routing
  dokploy-network:
    external: true
```

### Segmentation rules

| Service | Networks | Why |
|---|---|---|
| App (frontend) | dokploy-network + backend | Receives Traefik traffic + accesses the backend |
| API | dokploy-network + backend | Same |
| DB | backend only | No external access, not even the Internet |
| Redis | backend only | Same |
| Worker | backend only | No need to be routed by Traefik |
| Monitoring | monitoring (internal) + dokploy-network | Grafana reachable, Prometheus not |

### No `ports` unless necessary

```yaml
# BAD: exposes the port directly on the host
ports:
  - "5432:5432"   # PostgreSQL reachable from the Internet!

# GOOD: exposes only on the Docker network
expose:
  - "5432"
```

---

## Docker Bench for Security

Automated audit based on the CIS Docker Benchmark:

```bash
docker run --rm --net host --pid host \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /etc:/etc:ro \
  docker/docker-bench-security
```

Audited categories:
- Host configuration
- Docker daemon configuration
- Docker configuration files
- Container runtime
- Images and builds
- Docker Swarm

---

## Production checklist

### Images

- [ ] Pinned versions (no `:latest`)
- [ ] Multi-stage builds
- [ ] Minimal images (alpine/slim/distroless)
- [ ] Vulnerability scan in CI/CD
- [ ] `.dockerignore` configured

### Runtime

- [ ] Non-root (`USER` in Dockerfile or `user:` in compose)
- [ ] `read_only: true` + `tmpfs` for writable directories
- [ ] `security_opt: no-new-privileges:true`
- [ ] `cap_drop: ALL` + selective add-back
- [ ] Resource limits (memory + CPU)
- [ ] Log rotation (`max-size` + `max-file`)
- [ ] Health checks configured

### Network

- [ ] frontend/backend segmentation
- [ ] `internal: true` on backend networks
- [ ] `expose` instead of `ports`
- [ ] Security headers via Traefik middleware

### Secrets

- [ ] No secrets in source code or images
- [ ] Docker Swarm Secrets or an external secret manager
- [ ] Build-time secrets for CI/CD
- [ ] `.env` in `.gitignore`

### Data

- [ ] Named volumes for persistence
- [ ] Automated and tested backups
- [ ] No sensitive data in logs
