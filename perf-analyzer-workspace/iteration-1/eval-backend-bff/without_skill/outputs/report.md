# Audit de Performance -- Service BFF (services/bff)

**Date :** 2026-04-15  
**Service :** `@sapain/bff` v0.1.0  
**Stack :** Fastify 5.6, Node.js 20, sql.js (SQLite in-memory/WASM), TypeScript  
**Scope :** Analyse statique du code source -- pas de profiling runtime  

---

## Resume executif

Le BFF est un service leger (~11 fichiers TS) qui fait proxy entre le front-end SPA et les services backend/auth. L'architecture est saine (Fastify, session server-side, SSE streaming), mais plusieurs patterns dans le code introduisent de la latence evitable sur chaque requete API proxifiee. Les problemes identifies sont principalement lies a : (1) le session store SQLite synchrone qui bloque l'event loop, (2) l'absence de connection pooling configure sur les appels HTTP sortants, et (3) des copies memoire inutiles dans le proxy.

**Impact estime :** Les corrections proposees pourraient reduire la latence p95 des requetes proxifiees de 30 a 60%, selon la charge.

---

## Problemes identifies

### P1 -- CRITIQUE : Session store SQLite synchrone bloque l'event loop

**Fichier :** `services/bff/src/session/store.ts`

sql.js execute toutes les requetes SQL de maniere **synchrone** sur le thread principal (c'est du SQLite compile en WASM, pas du natif). Chaque appel a `store.get()` fait un `SELECT` + un `UPDATE` du `last_activity`, et c'est appele sur **chaque requete authentifiee** via le middleware session.

En plus, `persist()` fait `db.export()` (serialise toute la DB WASM en buffer) + `fs.writeFileSync()` toutes les 10 secondes -- doublement bloquant.

**Recommandations :**
1. **Immediat :** Remplacer `fs.writeFileSync` dans `persist()` par `fs.promises.writeFile`
2. **Court terme :** Migrer vers `better-sqlite3` (natif, ~10x plus rapide que sql.js WASM)
3. **Moyen terme :** Utiliser un simple `Map<string, SessionData>` en memoire -- pour du key-value lookup single-instance, c'est plus performant que toute DB SQL

### P2 -- MAJEUR : Pas de configuration d'Agent HTTP / connection pooling

**Fichiers :** `services/bff/src/routes/proxy.ts`, `services/bff/src/routes/auth.ts`, `services/bff/src/middleware/session.ts`

Tous les `fetch()` vers le backend et auth utilisent le dispatcher par defaut de Node.js sans configuration explicite. Il n'y a aucun controle sur le nombre max de connexions simultanees, les timeouts de connexion, ou le pipelining.

**Recommandation :** Creer un `undici.Pool` par service cible avec des limites de connexions explicites (`connections: 20`, `keepAliveTimeout: 30_000`) et le passer comme `dispatcher` dans chaque `fetch()`.

### P3 -- MAJEUR : Double buffering dans le proxy API

**Fichier :** `services/bff/src/routes/proxy.ts` (lignes 37-51)

```ts
const body = await res.text();  // lit TOUT le body en string
return reply.send(body);        // re-encode en buffer
```

Le body entier est buffered en memoire comme string avant d'etre renvoye. Pour les reponses volumineuses, c'est de la memoire gaspillee et de la latence TTFB ajoutee.

**Recommandation :** Streamer directement : `reply.send(res.body)` -- Fastify 5 supporte les `ReadableStream` nativement.

### P4 -- MAJEUR : Re-serialisation JSON inutile du body de requete

**Fichier :** `services/bff/src/routes/proxy.ts` (ligne 42)

```ts
body: JSON.stringify(request.body)  // Fastify a deja parse le JSON, on le re-serialise
```

Cycle parse/stringify inutile sur chaque requete POST/PUT/PATCH.

**Recommandation :** Configurer un content-type parser qui garde le body brut (`parseAs: "buffer"`), ou migrer vers `@fastify/http-proxy` / `fastify-reply-from`.

### P5 -- MODERE : Aucun timeout sur les appels proxy vers le backend

**Fichier :** `services/bff/src/routes/proxy.ts`

Les `fetch()` vers le backend n'ont aucun timeout. Si le backend est lent, les requetes client restent ouvertes indefiniment, consommant memoire et file descriptors.

**Recommandation :** Ajouter `signal: AbortSignal.timeout(15_000)` sur chaque appel proxy.

### P6 -- MODERE : Health checks non caches dans le monitoring

**Fichier :** `services/bff/src/modules/monitoring/service.ts` (lignes 257-289)

Chaque appel a `/bff/monitoring/summary` fait 2 requetes HTTP sortantes (health check auth + backend). Le dashboard poll toutes les 5s.

**Recommandation :** Cacher les resultats avec un TTL de 15 secondes.

### P7 -- MODERE : Array.shift() O(n) dans le monitoring

**Fichier :** `services/bff/src/modules/monitoring/service.ts` (ligne 167)

`recentDurationsMs.shift()` est O(n). Avec `buildTrafficSummary()` qui fait une copie + sort a chaque appel, c'est du CPU gaspille sous charge.

**Recommandation :** Utiliser un ring buffer circulaire.

### P8 -- MINEUR : Pas de compression des reponses

**Fichier :** `services/bff/src/routes/proxy.ts`

Le proxy ne forward pas `Accept-Encoding` et ne compresse pas les reponses sortantes.

**Recommandation :** Ajouter `@fastify/compress`.

### P9 -- MINEUR : Pas de timeout sur le refresh token

**Fichier :** `services/bff/src/middleware/session.ts` (ligne 89)

L'appel `fetch(/v1/auth/refresh)` n'a pas de timeout. Si le service auth est lent, toutes les requetes de la session bloquent (le mutex empile les waiters).

**Recommandation :** `signal: AbortSignal.timeout(5_000)` dans `doRefresh()`.

### P10 -- MINEUR : Pas de forwarding des headers de cache

**Fichier :** `services/bff/src/routes/proxy.ts`

Les headers `Cache-Control`, `ETag`, `Last-Modified` du backend ne sont pas forwardes. Chaque requete refait un round-trip complet.

**Recommandation :** Forward ces headers pour permettre le caching navigateur.

---

## Plan d'action prioritise

| Priorite | Probleme | Effort | Impact |
|----------|----------|--------|--------|
| 1 | P3 -- Streamer les reponses proxy | Faible (5 lignes) | Fort |
| 2 | P4 -- Eviter re-serialisation JSON | Faible | Modere |
| 3 | P5 -- Timeouts sur les appels proxy | Faible (1 ligne) | Fort |
| 4 | P2 -- Agent HTTP avec connection pooling | Moyen | Fort |
| 5 | P1 -- Migrer sql.js vers better-sqlite3 ou Map | Moyen | Fort |
| 6 | P8 -- Compression (fastify/compress) | Faible | Modere |
| 7 | P9 -- Timeout sur le refresh | Faible | Modere |
| 8 | P6 -- Cache des health checks | Faible | Faible |
| 9 | P10 -- Forward headers de cache | Faible | Modere |
| 10 | P7 -- Ring buffer metriques | Faible | Negligeable |

## Quick wins (< 1h)

1. Remplacer `res.text()` par `reply.send(res.body)` dans le proxy
2. Ajouter `AbortSignal.timeout(15_000)` sur tous les `fetch()` proxy
3. Ajouter `AbortSignal.timeout(5_000)` dans `doRefresh()`
4. Remplacer `writeFileSync` par `fs.promises.writeFile` dans `persist()`
5. Ajouter `@fastify/compress`

## Amelioration strategique

La migration vers `@fastify/http-proxy` ou `fastify-reply-from` (plugin officiel Fastify pour le proxying) eliminerait les problemes P2, P3, P4, P8, P10 d'un seul coup. C'est la recommandation moyen terme la plus impactante.

## Note sur l'architecture

Le BFF est bien structure : separation des concerns claire, session server-side securisee, SSE streaming correct via `http.request` + `pipe`, monitoring integre. Les problemes identifies sont des optimisations classiques pour un proxy Node.js, pas des defauts d'architecture.
