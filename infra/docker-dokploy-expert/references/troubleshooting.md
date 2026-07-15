# Docker & Dokploy Troubleshooting Guide

## Table of contents

1. [Decision tree by symptom](#decision-tree)
2. [502 Bad Gateway](#502-bad-gateway)
3. [SSL / Certificates](#ssl--certificates)
4. [Container in a restart loop](#restart-loop)
5. [Failed or slow build](#build-issues)
6. [Volumes and data](#volumes-and-data)
7. [Networking and connectivity](#networking)
8. [Performance and resources](#performance)
9. [Swarm-specific](#swarm)
10. [Dokploy-specific](#dokploy)
11. [Diagnostic commands](#diagnostic-commands)

---

## Decision tree

```
App not responding?
├── 502 Bad Gateway → "502 Bad Gateway" section
├── 503 Service Unavailable → Container not healthy / no replica
├── 404 Not Found → Wrong domain or path in the Traefik labels
├── ERR_CONNECTION_REFUSED → Port not exposed or Traefik down
├── ERR_SSL_PROTOCOL_ERROR → SSL not configured or DNS not propagated
└── Timeout → App too slow to respond, check health + resources

Container crashing?
├── Exit 0 → App shuts down normally (CMD terminates)
├── Exit 1 → Error in the app (check logs)
├── Exit 137 → OOM Kill (increase memory limit)
├── Exit 143 → SIGTERM received (normal shutdown by Docker)
└── Restart loop → Failing health check or missing dependency

Build failing?
├── Out of memory → Build too heavy, use external CI/CD
├── Network error → DNS resolution in the build, proxy/firewall
├── Permission denied → Wrong user/group in the Dockerfile
└── Layer cache miss → Order of instructions in the Dockerfile
```

---

## 502 Bad Gateway

This is the most common error on Dokploy. It means Traefik receives the request but cannot forward it to the container.

### Causes (by frequency)

**1. The app listens on 127.0.0.1 instead of 0.0.0.0**

This is the #1 cause. Inside a container, `127.0.0.1` is the container's loopback, not the host's. Traefik cannot reach it.

```bash
# Check
docker exec <container> netstat -tlnp 2>/dev/null || \
docker exec <container> ss -tlnp

# Should show 0.0.0.0:<port>, not 127.0.0.1:<port>
```

**Fixes by framework:**
- **Next.js**: `next start -H 0.0.0.0`
- **Express**: `app.listen(3000, '0.0.0.0')`
- **Vite**: `vite --host 0.0.0.0`
- **Django**: `python manage.py runserver 0.0.0.0:8000`
- **Rails**: `rails server -b 0.0.0.0`
- **Go**: `http.ListenAndServe(":8080", handler)`

**2. Wrong port in the Traefik labels**

```yaml
# The port in the label must match the port the app listens on
labels:
  - "traefik.http.services.myapp.loadbalancer.server.port=3000"
```

**3. The container is not on dokploy-network**

```yaml
networks:
  - dokploy-network  # REQUIRED for Traefik to route
```

**4. The app hasn't finished starting**

The health check hasn't passed yet, or `start_period` is too short.

```yaml
healthcheck:
  start_period: 60s  # Increase if the app takes a while to start
```

**5. The app crashes on startup**

```bash
docker logs <container> --tail 50
```

---

## SSL / Certificates

### The certificate won't generate

1. **DNS not propagated**: the DNS A record must point to the server BEFORE adding the domain
   ```bash
   # Check
   dig +short app.example.com
   # Should return your server's IP
   ```

2. **Port 80 blocked**: Let's Encrypt's HTTP-01 challenge needs port 80 open

3. **Let's Encrypt rate limit**: max 5 certificates per domain per week. Use staging first:
   ```
   --certificatesresolvers.letsencrypt.acme.caserver=https://acme-staging-v02.api.letsencrypt.org/directory
   ```

4. **Wildcard**: the HTTP challenge doesn't work for `*.example.com`; you need a DNS challenge

### Expired certificate

Traefik renews automatically. If it doesn't work:
```bash
# Check the acme.json file
docker exec <traefik-container> cat /letsencrypt/acme.json | jq '.[] | .Certificates[].domain'

# Force a renewal: remove the domain's entry from acme.json and restart Traefik
```

---

## Restart Loop

The container restarts in a loop (status: `Restarting`).

### Diagnosis

```bash
# See the status and exit code
docker ps -a --filter "name=myapp"

# Logs from the last crash
docker logs --tail 50 <container>

# Inspect (OOMKilled, RestartCount, etc.)
docker inspect <container> | jq '.[0].State'
```

### Exit 137 (OOM Kill)

The container exceeded its memory limit and was killed by the kernel.

```bash
# Confirm
docker inspect <container> | jq '.[0].State.OOMKilled'
# true = OOM kill confirmed
```

**Fix**: increase `deploy.resources.limits.memory` or optimize the app's memory usage.

### Failing health check

If the health check fails, Swarm stops and restarts the container.

```bash
# See the health status
docker inspect <container> | jq '.[0].State.Health'
```

**Common fixes:**
- Increase `start_period` (the app doesn't have time to start)
- Increase `timeout` (the health check is too fast)
- Check that the health check command works (`docker exec <container> <health-command>`)

### Missing dependency

The app starts before the DB is ready.

```yaml
depends_on:
  db:
    condition: service_healthy  # Waits for the DB's health check to pass
```

---

## Build Issues

### Build freezes the server

Nixpacks and Buildpacks builds are very heavy on CPU/RAM.

**Solution**: build in CI/CD, not on the production server.

### Slow build (no cache)

Check the order of instructions in the Dockerfile:
```dockerfile
# GOOD: dependencies stay cached when only the code changes
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# BAD: everything is recomputed on every code change
COPY . .
RUN npm ci && npm run build
```

### Network error during the build

```bash
# Test DNS resolution in the build
docker build --network host .

# Or configure an npm mirror
RUN npm config set registry https://registry.npmmirror.com
```

---

## Volumes and data

### Files gone after redeploy

With Auto Deploy enabled, Dokploy runs a `git clone` that wipes the repo directory.

**Solutions:**
- **File Mounts**: Advanced → File Mounts (persistent)
- **Relative bind mounts**: `../files/my-data:/app/data` (persists outside the repo)
- **Named volumes**: always persistent

### Invalid volume (container won't start)

Swarm silently refuses to start a container with an invalid mount.

```bash
# Check Swarm errors
docker service ps --no-trunc <service>
# Look for "mount" in the error messages
```

### Restore data from a volume

```bash
# Copy from a volume to the host
docker run --rm -v myvolume:/data -v $(pwd):/backup alpine \
  tar czf /backup/backup.tar.gz -C /data .

# Restore
docker run --rm -v myvolume:/data -v $(pwd):/backup alpine \
  sh -c "cd /data && tar xzf /backup/backup.tar.gz"
```

---

## Networking

### Containers can't see each other

```bash
# Check they're on the same network
docker network inspect <network-name> | jq '.[0].Containers'

# Test DNS resolution
docker exec <container-A> ping <service-B-name>
# or
docker exec <container-A> nslookup <service-B-name>
```

### DNS won't resolve

Containers on the default `bridge` network do NOT have DNS resolution. You need a user-defined network.

### Port already in use

```bash
# Find what's using the port
lsof -i :80
# or
ss -tlnp | grep :80
```

---

## Performance

### Identify a resource-hungry container

```bash
# Real-time stats
docker stats --no-stream

# Custom format
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}"
```

### Disk full

```bash
# Space used by Docker
docker system df

# Breakdown by type
docker system df -v

# Selective cleanup
docker image prune -a --filter "until=168h"   # Images > 7 days
docker container prune                          # Stopped containers
docker builder prune -a                         # Build cache
```

---

## Swarm

### Service won't start

```bash
# See the deployment errors
docker service ps --no-trunc <service>

# Common causes:
# - "no suitable node" → placement constraint not satisfied
# - "image not found" → registry not configured on the worker
# - "mount error" → invalid volume or bind mount
```

### Worker node unreachable

```bash
# Check the nodes
docker node ls

# If a node is "Down":
# 1. Check network connectivity
# 2. Check that Docker is running on the worker
# 3. Port 2377 open (manager-worker communication)
```

---

## Dokploy

### UI inaccessible

```bash
# Check that the Dokploy containers are running
docker ps --filter "name=dokploy"

# If the internal DB is in recovery (disk full):
docker system prune -a
docker restart dokploy
```

### Logs not visible

- `container_name` set in the compose → remove it
- The app runs on a worker different from the manager → known Dokploy limitation

### Auto Deploy doesn't trigger

1. Check that the branch in Dokploy matches the branch you pushed
2. Check that the webhook is configured (GitHub Settings → Webhooks)
3. Test the webhook manually via the URL shown in the deployment logs

---

## Diagnostic commands

### Quick commands

```bash
# Overview
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Size}}"

# Logs with timestamps
docker logs --tail 100 -t <container>

# Follow logs in real time
docker logs -f <container>

# Inspect a container
docker inspect <container> | jq '.[0].State'
docker inspect <container> | jq '.[0].NetworkSettings.Networks'
docker inspect <container> | jq '.[0].Mounts'

# Enter a container
docker exec -it <container> sh

# Resource stats
docker stats --no-stream

# Network
docker network ls
docker network inspect <network>

# Disk
docker system df
docker volume ls

# Swarm
docker node ls
docker service ls
docker service ps <service>
docker service logs <service>
```

### Full diagnostic script

Use `scripts/docker-inspect.sh` for automated diagnostics:

```bash
~/.claude/skills/docker-dokploy-expert/scripts/docker-inspect.sh overview
~/.claude/skills/docker-dokploy-expert/scripts/docker-inspect.sh health
~/.claude/skills/docker-dokploy-expert/scripts/docker-inspect.sh network
~/.claude/skills/docker-dokploy-expert/scripts/docker-inspect.sh resources
~/.claude/skills/docker-dokploy-expert/scripts/docker-inspect.sh logs <container>
```
