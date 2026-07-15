# Traefik — Advanced Configuration for Dokploy

## Table of contents

1. [Traefik architecture in Dokploy](#architecture)
2. [Basic labels](#basic-labels)
3. [Middlewares](#middlewares)
4. [SSL / Let's Encrypt](#ssl)
5. [Wildcard SSL (DNS Challenge)](#wildcard-ssl)
6. [Traefik Dashboard](#traefik-dashboard)
7. [Load Balancing](#load-balancing)
8. [WebSocket Support](#websocket)
9. [Security headers](#security-headers)

---

## Architecture

Dokploy installs Traefik as a system container on `dokploy-network`. Traefik listens on ports 80 and 443 and routes traffic to the containers via Docker labels.

```
Client → :443 → Traefik (SSL termination) → dokploy-network → Container:port
```

Traefik in Dokploy uses the **Docker provider**: it watches container labels to configure routing dynamically. No static config file is needed for routes.

---

## Basic labels

### Expose a service

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.myapp.rule=Host(`app.example.com`)"
  - "traefik.http.routers.myapp.entrypoints=websecure"
  - "traefik.http.routers.myapp.tls.certresolver=letsencrypt"
  - "traefik.http.services.myapp.loadbalancer.server.port=3000"
```

### Path-based routing

```yaml
labels:
  - "traefik.http.routers.api.rule=Host(`example.com`) && PathPrefix(`/api`)"
  - "traefik.http.routers.frontend.rule=Host(`example.com`) && PathPrefix(`/`)"
```

### Multi-domain

```yaml
labels:
  - "traefik.http.routers.myapp.rule=Host(`app.example.com`) || Host(`www.example.com`)"
```

### Naming routers/services

Each router and service must have a **unique name** across the entire Traefik infrastructure. Recommended convention: `{project}-{service}`.

---

## Middlewares

Middlewares transform requests between the entrypoint and the backend service.

### Redirect HTTP → HTTPS

```yaml
labels:
  # HTTP router that redirects
  - "traefik.http.routers.myapp-http.rule=Host(`app.example.com`)"
  - "traefik.http.routers.myapp-http.entrypoints=web"
  - "traefik.http.routers.myapp-http.middlewares=redirect-https"
  - "traefik.http.middlewares.redirect-https.redirectscheme.scheme=https"
  - "traefik.http.middlewares.redirect-https.redirectscheme.permanent=true"

  # Main HTTPS router
  - "traefik.http.routers.myapp.rule=Host(`app.example.com`)"
  - "traefik.http.routers.myapp.entrypoints=websecure"
  - "traefik.http.routers.myapp.tls.certresolver=letsencrypt"
```

### Rate Limiting

```yaml
labels:
  - "traefik.http.middlewares.ratelimit.ratelimit.average=100"
  - "traefik.http.middlewares.ratelimit.ratelimit.burst=50"
  - "traefik.http.middlewares.ratelimit.ratelimit.period=1m"
  - "traefik.http.routers.myapp.middlewares=ratelimit"
```

### Basic Auth

```bash
# Generate the hash (htpasswd)
htpasswd -nb admin mysecretpassword
# Result: admin:$apr1$...
# In the labels, escape the $ as $$
```

```yaml
labels:
  - "traefik.http.middlewares.auth.basicauth.users=admin:$$apr1$$..."
  - "traefik.http.routers.myapp.middlewares=auth"
```

### IP Whitelist

```yaml
labels:
  - "traefik.http.middlewares.ipwhitelist.ipallowlist.sourcerange=10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"
  - "traefik.http.routers.admin.middlewares=ipwhitelist"
```

### Compression (gzip)

```yaml
labels:
  - "traefik.http.middlewares.compress.compress=true"
  - "traefik.http.routers.myapp.middlewares=compress"
```

### Strip Prefix

Useful for microservices with path-based routing:

```yaml
labels:
  - "traefik.http.middlewares.strip-api.stripprefix.prefixes=/api"
  - "traefik.http.routers.api.middlewares=strip-api"
  # /api/users → the backend receives /users
```

### Retry

```yaml
labels:
  - "traefik.http.middlewares.retry.retry.attempts=3"
  - "traefik.http.middlewares.retry.retry.initialinterval=100ms"
```

### Middleware chain

```yaml
labels:
  - "traefik.http.routers.myapp.middlewares=redirect-https,ratelimit,compress,security-headers"
```

---

## SSL

### Automatic Let's Encrypt (HTTP Challenge)

This is the default mode in Dokploy. It works when:
- The domain points to the server (DNS A record configured)
- Port 80 is open (for the HTTP-01 challenge)

The config is managed by Dokploy at the Traefik container level. For applications, you just use the certresolver in the labels:

```yaml
labels:
  - "traefik.http.routers.myapp.tls.certresolver=letsencrypt"
```

### Custom certificates

Uploadable via the Dokploy UI (Settings > Certificates). Then configure the router to use the certificate:

```yaml
labels:
  - "traefik.http.routers.myapp.tls=true"
  # The certificate is configured in Traefik's dynamic config
```

---

## Wildcard SSL

Required for `*.example.com`. Needs a **DNS Challenge** instead of the HTTP Challenge.

### With Cloudflare

Environment variables to add to the Traefik container (via Dokploy Settings > Traefik):

```
CF_API_EMAIL=your@email.com
CF_DNS_API_TOKEN=your-cloudflare-api-token
```

Additional Traefik config:
```
--certificatesresolvers.letsencrypt.acme.dnschallenge=true
--certificatesresolvers.letsencrypt.acme.dnschallenge.provider=cloudflare
--certificatesresolvers.letsencrypt.acme.dnschallenge.resolvers=1.1.1.1:53,8.8.8.8:53
```

Then in the service's labels:
```yaml
labels:
  - "traefik.http.routers.myapp.tls.certresolver=letsencrypt"
  - "traefik.http.routers.myapp.tls.domains[0].main=example.com"
  - "traefik.http.routers.myapp.tls.domains[0].sans=*.example.com"
```

### With Route53 (AWS)

Environment variables:
```
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=eu-west-1
AWS_HOSTED_ZONE_ID=...
```

Provider: `route53`

---

## Traefik Dashboard

The dashboard is available for monitoring and debugging.

```yaml
# In the Traefik config
command:
  - "--api.dashboard=true"
  - "--api.insecure=false"

labels:
  - "traefik.http.routers.dashboard.rule=Host(`traefik.example.com`)"
  - "traefik.http.routers.dashboard.service=api@internal"
  - "traefik.http.routers.dashboard.entrypoints=websecure"
  - "traefik.http.routers.dashboard.tls.certresolver=letsencrypt"
  - "traefik.http.routers.dashboard.middlewares=auth"
  - "traefik.http.middlewares.auth.basicauth.users=admin:$$apr1$$..."
```

Always protect the dashboard with auth + IP whitelist in production.

---

## Load Balancing

### Sticky sessions

Useful for apps with server-side state:

```yaml
labels:
  - "traefik.http.services.myapp.loadbalancer.sticky.cookie=true"
  - "traefik.http.services.myapp.loadbalancer.sticky.cookie.name=srv_id"
  - "traefik.http.services.myapp.loadbalancer.sticky.cookie.httponly=true"
  - "traefik.http.services.myapp.loadbalancer.sticky.cookie.secure=true"
```

### Traefik-level health check

```yaml
labels:
  - "traefik.http.services.myapp.loadbalancer.healthcheck.path=/health"
  - "traefik.http.services.myapp.loadbalancer.healthcheck.interval=10s"
  - "traefik.http.services.myapp.loadbalancer.healthcheck.timeout=3s"
```

---

## WebSocket

Traefik supports WebSockets natively. If the app uses a specific path:

```yaml
labels:
  - "traefik.http.routers.ws.rule=Host(`app.example.com`) && PathPrefix(`/ws`)"
  - "traefik.http.routers.ws.entrypoints=websecure"
  - "traefik.http.routers.ws.tls.certresolver=letsencrypt"
  - "traefik.http.services.ws.loadbalancer.server.port=3000"
```

For long-lived connections, adjust the timeouts:

```yaml
labels:
  - "traefik.http.middlewares.ws-timeout.buffering.maxRequestBodyBytes=0"
  - "traefik.http.middlewares.ws-timeout.buffering.memRequestBodyBytes=0"
```

---

## Security headers

A complete set of recommended headers for production:

```yaml
labels:
  # HSTS (force HTTPS)
  - "traefik.http.middlewares.security.headers.stsSeconds=31536000"
  - "traefik.http.middlewares.security.headers.stsIncludeSubdomains=true"
  - "traefik.http.middlewares.security.headers.stsPreload=true"

  # XSS and clickjacking protections
  - "traefik.http.middlewares.security.headers.contentTypeNosniff=true"
  - "traefik.http.middlewares.security.headers.frameDeny=true"
  - "traefik.http.middlewares.security.headers.browserXssFilter=true"

  # Referrer
  - "traefik.http.middlewares.security.headers.referrerPolicy=strict-origin-when-cross-origin"

  # Content Security Policy (adapt to the project)
  - "traefik.http.middlewares.security.headers.contentSecurityPolicy=default-src 'self'"

  # Permissions Policy
  - "traefik.http.middlewares.security.headers.permissionsPolicy=camera=(), microphone=(), geolocation=()"

  # Apply
  - "traefik.http.routers.myapp.middlewares=security"
```
