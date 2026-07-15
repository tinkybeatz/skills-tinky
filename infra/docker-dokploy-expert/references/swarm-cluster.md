# Docker Swarm & Multi-node Cluster in Dokploy

## Table of contents

1. [Swarm architecture in Dokploy](#architecture)
2. [Multi-node setup](#setup)
3. [Overlay Networks](#overlay-networks)
4. [Secrets & Configs](#secrets--configs)
5. [Deployment strategies](#deployment-strategies)
6. [Placement & Constraints](#placement)
7. [Rolling Updates & Rollbacks](#rolling-updates)
8. [Cluster monitoring](#cluster-monitoring)
9. [Maintenance & Cleanup](#maintenance--cleanup)

---

## Architecture

```
┌──────────────────────────┐     ┌──────────────────────┐
│     Manager Node         │     │     Worker Node 1    │
│  ┌──────────────────┐    │     │  ┌────────────────┐  │
│  │    Dokploy UI    │    │     │  │   App replica   │  │
│  │  Postgres (int)  │    │     │  │   Worker proc   │  │
│  │     Redis        │    │     │  └────────────────┘  │
│  │    Traefik       │    │     │                      │
│  │  Swarm Manager   │    │     │   Swarm Worker       │
│  └──────────────────┘    │     └──────────────────────┘
│                          │
│  Docker Registry ←───────┼─────── Pull images
└──────────────────────────┘
```

**Fundamental rules:**
- The **manager** runs Dokploy + Traefik + the Swarm control plane
- The **workers** run only the application containers
- A **registry** is required (Docker Hub, GHCR, ECR...) so the workers can pull the images
- Images must be **pre-built** (no `build:` in Swarm stacks)
- The architecture (amd64/arm64) must be **identical** on all nodes

---

## Setup

### Initialization (already done by Dokploy)

Dokploy initializes the Swarm automatically at install time. On some VPS providers you have to specify the IP:

```bash
# The Dokploy installer does this, but in case of trouble:
ADVERTISE_ADDR=<SERVER_PUBLIC_IP> curl -sSL https://dokploy.com/install.sh | sh
```

### Add a worker

1. In the Dokploy UI → Settings → Servers → Add Node
2. Copy the join command shown
3. On the worker server:

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh

# Join the Swarm
docker swarm join --token <WORKER-TOKEN> <MANAGER-IP>:2377
```

4. The node appears in the Dokploy interface

### Add a manager (high availability)

```bash
# On the existing manager, get the manager token
docker swarm join-token manager

# On the new node
docker swarm join --token <MANAGER-TOKEN> <MANAGER-IP>:2377
```

**Recommendation**: 3 or 5 managers (an odd number for Raft quorum). Never more than 7.

### Configure the registry

In Dokploy Settings → Docker Registry:
- Docker Hub: username + token
- GHCR: username + personal access token
- AWS ECR: access key + secret key + region

---

## Overlay Networks

In Swarm mode, bridge networks don't span nodes. You need overlay networks.

```yaml
networks:
  app-network:
    driver: overlay
    encrypted: true       # Encrypts inter-node traffic
    attachable: true      # Lets standalone containers connect to it
```

### Ingress network

The `ingress` network is created automatically by Swarm. It handles the **routing mesh**: any node can accept traffic for any service, even if that service isn't running on that node.

### DNS and service discovery

- Service names are resolved automatically via Swarm's internal DNS
- By default: VIP-based load balancing (one virtual IP per service, IPVS distributes)
- Alternative: `endpoint_mode: dnsrr` for DNS round-robin (useful for some clients)

```yaml
services:
  app:
    deploy:
      endpoint_mode: vip  # Default, recommended
```

---

## Secrets & Configs

### Secrets (sensitive data)

```bash
# Create a secret
echo "my_db_password" | docker secret create db_password -
docker secret create tls_cert ./cert.pem

# List
docker secret ls

# Inspect (does NOT show the contents)
docker secret inspect db_password
```

```yaml
services:
  app:
    secrets:
      - db_password
      - source: tls_cert
        target: /app/cert.pem
        mode: 0400

secrets:
  db_password:
    external: true
  tls_cert:
    external: true
```

Secrets are:
- Encrypted at rest in the Raft log
- Mounted in tmpfs at `/run/secrets/<name>`
- Sent only to the nodes running tasks that use them

### Configs (non-sensitive data)

```bash
docker config create nginx_conf ./nginx.conf
```

```yaml
services:
  proxy:
    configs:
      - source: nginx_conf
        target: /etc/nginx/nginx.conf

configs:
  nginx_conf:
    external: true
```

---

## Deployment strategies

### Zero-downtime (start-first)

```yaml
deploy:
  replicas: 2
  update_config:
    parallelism: 1          # 1 container at a time
    delay: 10s               # 10s between each update
    failure_action: rollback # Auto rollback on failure
    order: start-first       # Starts the new one BEFORE stopping the old
    monitor: 30s             # Monitors for 30s after startup
    max_failure_ratio: 0.1   # Tolerates 10% failures
  rollback_config:
    parallelism: 0           # Roll back all at once
    order: stop-first
```

**`order: start-first`** is the key to zero-downtime: the new container starts and passes its health check BEFORE the old one is stopped.

### Restart policy

```yaml
deploy:
  restart_policy:
    condition: on-failure    # Restart only on error (not on exit 0)
    delay: 5s
    max_attempts: 3
    window: 120s             # Window over which attempts are counted
```

### Deployment modes

| Mode | Behavior | Use |
|---|---|---|
| `replicated` (default) | N instances spread across the nodes | The majority of services |
| `global` | 1 instance per node | Monitoring agents, log shippers |

```yaml
deploy:
  mode: global  # or replicated (default)
```

---

## Placement

### Constraints

```yaml
deploy:
  placement:
    constraints:
      - node.role == worker          # Workers only
      - node.labels.zone == eu-west  # Custom label on the node
      - node.hostname == server-01   # Specific node
```

### Node labels

```bash
# Add a label to a node
docker node update --label-add zone=eu-west node-01
docker node update --label-add type=gpu node-02

# List the labels
docker node inspect --pretty node-01
```

### Preferences (soft constraints)

```yaml
deploy:
  placement:
    preferences:
      - spread: node.labels.zone  # Spread across zones
```

---

## Rolling Updates

### From the CLI

```bash
# Update a service's image
docker service update --image myapp:2.0 mystack_api

# Rollback
docker service rollback mystack_api

# See the state of the rolling update
docker service ps mystack_api
```

### From Dokploy

Dokploy handles rolling updates automatically when you redeploy. The `deploy.update_config` configuration in the compose file controls the behavior.

### Monitoring the rollout

```bash
# See all tasks (including the old ones)
docker service ps --no-trunc mystack_api

# Service logs during the rollout
docker service logs -f mystack_api
```

---

## Cluster monitoring

### Node status

```bash
docker node ls
# ID    HOSTNAME    STATUS    AVAILABILITY    MANAGER STATUS
# xxx   manager-01  Ready     Active          Leader
# yyy   worker-01   Ready     Active
# zzz   worker-02   Ready     Active
```

### Service status

```bash
# All services
docker service ls

# Detail of a service
docker service inspect --pretty mystack_api

# Tasks of a service
docker service ps mystack_api
```

### Draining a node (maintenance)

```bash
# Put a node into maintenance (tasks migrate to other nodes)
docker node update --availability drain worker-01

# Bring it back into service
docker node update --availability active worker-01
```

---

## Maintenance & Cleanup

### Automatic cleanup

Dokploy does **not** automatically clean up storage on the workers. Set up a cron job:

```bash
# On each worker, crontab:
0 3 * * * docker system prune -af --filter "until=168h" > /dev/null 2>&1
```

This removes unused images/containers/networks older than 7 days.

### Manual cleanup

```bash
# See Docker disk usage
docker system df

# Aggressive cleanup (removes everything not in use)
docker system prune -a --volumes

# Targeted cleanup
docker image prune -a --filter "until=168h"   # Images > 7 days
docker container prune                          # Stopped containers
docker volume prune                             # Orphaned volumes
```

### Remove a node

```bash
# From the node to remove
docker swarm leave

# If it's a manager
docker swarm leave --force

# From another manager: remove the node from the list
docker node rm <node-id>
```
