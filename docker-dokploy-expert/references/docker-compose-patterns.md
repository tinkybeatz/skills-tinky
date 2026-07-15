# Docker Compose Patterns for Dokploy

## Table of contents

1. [Web App + DB + Cache](#web-app--db--cache)
2. [Web App + DB + Cache + Queue + Worker](#full-stack-with-queue)
3. [Monitoring Stack (Prometheus + Grafana)](#monitoring-stack)
4. [ELK / EFK Stack (Centralized logging)](#elk-stack)
5. [Database Replication (PostgreSQL Primary-Replica)](#db-replication)
6. [Init Containers (Migrations)](#init-containers)
7. [Sidecar Pattern](#sidecar-pattern)

---

## Web App + DB + Cache

The baseline pattern for the majority of web applications.

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    expose:
      - "3000"
    environment:
      - DATABASE_URL=postgresql://app:${DB_PASSWORD}@db:5432/app
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: "2.0"
        reservations:
          memory: 256M
    networks:
      - dokploy-network
      - backend

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    deploy:
      resources:
        limits:
          memory: 512M
    networks:
      - backend

  redis:
    image: redis:7-alpine
    command: redis-server --maxmemory 128mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          memory: 256M
    networks:
      - backend

networks:
  dokploy-network:
    external: true
  backend:
    internal: true

volumes:
  postgres_data:
  redis_data:
```

---

## Full Stack with Queue

Adds RabbitMQ (or BullMQ via Redis) and background-processing workers.

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    expose:
      - "3000"
    environment:
      - DATABASE_URL=postgresql://app:${DB_PASSWORD}@db:5432/app
      - REDIS_URL=redis://redis:6379
      - RABBITMQ_URL=amqp://guest:${RABBITMQ_PASSWORD}@rabbitmq:5672
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: "2.0"
    networks:
      - dokploy-network
      - backend

  worker:
    build:
      context: .
      dockerfile: Dockerfile
    command: ["node", "dist/worker.js"]
    environment:
      - DATABASE_URL=postgresql://app:${DB_PASSWORD}@db:5432/app
      - REDIS_URL=redis://redis:6379
      - RABBITMQ_URL=amqp://guest:${RABBITMQ_PASSWORD}@rabbitmq:5672
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 512M
          cpus: "1.0"
    restart: unless-stopped
    networks:
      - backend

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    deploy:
      resources:
        limits:
          memory: 1G
    networks:
      - backend

  redis:
    image: redis:7-alpine
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          memory: 384M
    networks:
      - backend

  rabbitmq:
    image: rabbitmq:3.13-management-alpine
    environment:
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASSWORD}
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "check_running"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 60s
    deploy:
      resources:
        limits:
          memory: 512M
    networks:
      - backend
    # Expose the management UI via Traefik if needed:
    # labels:
    #   - "traefik.enable=true"
    #   - "traefik.http.routers.rabbitmq.rule=Host(`rabbitmq.example.com`)"
    #   - "traefik.http.services.rabbitmq.loadbalancer.server.port=15672"

networks:
  dokploy-network:
    external: true
  backend:
    internal: true

volumes:
  postgres_data:
  redis_data:
  rabbitmq_data:
```

---

## Monitoring Stack

Prometheus + Grafana + cAdvisor + Node Exporter to monitor the infrastructure.

```yaml
services:
  prometheus:
    image: prom/prometheus:v2.51.0
    volumes:
      - ../files/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"
      - "--storage.tsdb.retention.time=30d"
      - "--web.console.libraries=/etc/prometheus/console_libraries"
      - "--web.console.templates=/etc/prometheus/consoles"
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:9090/-/healthy"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 1G
    networks:
      - monitoring
      - dokploy-network

  grafana:
    image: grafana/grafana:10.4.0
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
      - GF_USERS_ALLOW_SIGN_UP=false
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 512M
    networks:
      - monitoring
      - dokploy-network
    # Traefik labels to expose Grafana
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.grafana.rule=Host(`grafana.example.com`)"
      - "traefik.http.routers.grafana.entrypoints=websecure"
      - "traefik.http.routers.grafana.tls.certresolver=letsencrypt"
      - "traefik.http.services.grafana.loadbalancer.server.port=3000"

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:v0.49.1
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    privileged: true
    deploy:
      resources:
        limits:
          memory: 256M
    networks:
      - monitoring

  node-exporter:
    image: prom/node-exporter:v1.7.0
    pid: host
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - "--path.procfs=/host/proc"
      - "--path.sysfs=/host/sys"
      - "--path.rootfs=/rootfs"
    deploy:
      resources:
        limits:
          memory: 128M
    networks:
      - monitoring

networks:
  monitoring:
    internal: true
  dokploy-network:
    external: true

volumes:
  prometheus_data:
  grafana_data:
```

**prometheus.yml file to place in `../files/`:**
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "cadvisor"
    static_configs:
      - targets: ["cadvisor:8080"]

  - job_name: "node-exporter"
    static_configs:
      - targets: ["node-exporter:9100"]
```

---

## ELK Stack

Elasticsearch + Kibana for centralized logging.

```yaml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.12.0
    environment:
      - node.name=es01
      - cluster.name=docker-cluster
      - discovery.type=single-node
      - bootstrap.memory_lock=true
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms1g -Xmx1g"
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    volumes:
      - es_data:/usr/share/elasticsearch/data
    healthcheck:
      test: ["CMD-SHELL", "curl -sf http://localhost:9200/_cluster/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 60s
    deploy:
      resources:
        limits:
          memory: 2G
    networks:
      - logging

  kibana:
    image: docker.elastic.co/kibana/kibana:8.12.0
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    depends_on:
      elasticsearch:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "curl -sf http://localhost:5601/api/status || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 120s
    deploy:
      resources:
        limits:
          memory: 1G
    networks:
      - logging
      - dokploy-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.kibana.rule=Host(`kibana.example.com`)"
      - "traefik.http.routers.kibana.entrypoints=websecure"
      - "traefik.http.routers.kibana.tls.certresolver=letsencrypt"
      - "traefik.http.services.kibana.loadbalancer.server.port=5601"

networks:
  logging:
    internal: true
  dokploy-network:
    external: true

volumes:
  es_data:
```

---

## DB Replication

PostgreSQL Primary-Replica with Bitnami images.

```yaml
services:
  pg-primary:
    image: bitnami/postgresql:16
    environment:
      - POSTGRESQL_REPLICATION_MODE=master
      - POSTGRESQL_REPLICATION_USER=repl_user
      - POSTGRESQL_REPLICATION_PASSWORD=${REPL_PASSWORD}
      - POSTGRESQL_USERNAME=app
      - POSTGRESQL_PASSWORD=${DB_PASSWORD}
      - POSTGRESQL_DATABASE=app
    volumes:
      - pg_primary_data:/bitnami/postgresql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          memory: 1G
    networks:
      - backend

  pg-replica:
    image: bitnami/postgresql:16
    environment:
      - POSTGRESQL_REPLICATION_MODE=slave
      - POSTGRESQL_MASTER_HOST=pg-primary
      - POSTGRESQL_REPLICATION_USER=repl_user
      - POSTGRESQL_REPLICATION_PASSWORD=${REPL_PASSWORD}
      - POSTGRESQL_PASSWORD=${DB_PASSWORD}
    depends_on:
      pg-primary:
        condition: service_healthy
    volumes:
      - pg_replica_data:/bitnami/postgresql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 1G
    networks:
      - backend

networks:
  backend:
    internal: true

volumes:
  pg_primary_data:
  pg_replica_data:
```

---

## Init Containers

Pattern for running migrations before the application starts.

```yaml
services:
  migrate:
    build:
      context: .
      dockerfile: Dockerfile
    command: ["npm", "run", "migrate"]
    environment:
      - DATABASE_URL=postgresql://app:${DB_PASSWORD}@db:5432/app
    depends_on:
      db:
        condition: service_healthy
    restart: "no"
    networks:
      - backend

  app:
    build:
      context: .
      dockerfile: Dockerfile
    depends_on:
      migrate:
        condition: service_completed_successfully
      db:
        condition: service_healthy
    # ... rest of app config
    networks:
      - dokploy-network
      - backend
```

`service_completed_successfully` (Compose v2.20+): the main service starts only if the migration container exited with code 0.

---

## Sidecar Pattern

Helper containers that share a volume or a network with the main service.

### Log shipper

```yaml
services:
  app:
    build: .
    volumes:
      - app_logs:/var/log/app
    networks:
      - backend

  log-shipper:
    image: grafana/promtail:2.9.0
    volumes:
      - app_logs:/var/log/app:ro
      - ../files/promtail-config.yml:/etc/promtail/config.yml:ro
    depends_on:
      - app
    deploy:
      resources:
        limits:
          memory: 128M
    networks:
      - backend

volumes:
  app_logs:
```

### Config reloader

```yaml
services:
  app:
    build: .
    volumes:
      - config:/app/config:ro

  config-reloader:
    image: jimmidyson/configmap-reload:v0.9.0
    args:
      - --volume-dir=/config
      - --webhook-url=http://app:3000/-/reload
    volumes:
      - config:/config:ro
```
