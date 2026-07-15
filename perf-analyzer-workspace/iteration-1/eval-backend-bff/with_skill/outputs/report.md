# Rapport d'Analyse de Performance

## Resume executif

**Perimetre analyse :** Service BFF (Backend For Frontend) -- `services/bff` -- un proxy Fastify avec gestion de sessions SQLite (sql.js en memoire), proxy API vers le backend, proxy SSE, authentification par cookie HttpOnly, et module de monitoring integre.

**Stack detecte :** Fastify 5.x, sql.js (SQLite in-memory avec persistence disque), Node.js 20, TypeScript, pas d'ORM classique.

**Findings :** 11 findings identifies -- 2 Critical, 4 High, 4 Medium, 1 Low.

**Top 3 recommandations :**
1. Ajouter des timeouts sur les appels `fetch` vers les services backend/auth (proxy et auth callback) -- risque de blocage complet du BFF si un service aval ne repond pas.
2. Remplacer les `Array.shift()` dans le monitoring par des structures circulaires -- O(n) sur chaque requete pour la collecte de metriques.
3. Activer la compression (gzip/brotli) sur les reponses Fastify -- bande passante gaspillee sur toutes les reponses JSON.

## Score global

**68 / 100 -- Moyen**

Le BFF est architecturalement sain (separation des responsabilites, session server-side, error handling global), mais plusieurs patterns de performance impactent la latence et la resilience sous charge : absence de timeouts sur les appels externes, structures de donnees lineaires dans le hot path du monitoring, absence de compression, et serialisation synchrone du body dans le proxy.

---

## Findings

### Backend -- API & Resilience

#### [FND-001] Absence de timeout sur les appels fetch du proxy API
- **Severite :** Critical
- **Effort :** Quick Win
- **Priorite :** 12
- **Localisation :** `services/bff/src/routes/proxy.ts:37-43`
- **Description :** L'appel `fetch(targetUrl, ...)` dans le handler `/bff/api/*` n'a aucun timeout. Si le backend service ne repond pas, le BFF reste bloque indefiniment, consommant une connexion et un slot d'event loop.
- **Impact estime :** Un service backend lent bloque progressivement toutes les requetes BFF -- effet cascade.
- **Recommandation :** Ajouter `signal: AbortSignal.timeout(15_000)` a l'appel fetch.

#### [FND-002] Absence de timeout sur l'appel fetch d'authentification (callback)
- **Severite :** Critical
- **Effort :** Quick Win
- **Priorite :** 12
- **Localisation :** `services/bff/src/routes/auth.ts:45-49`
- **Description :** L'appel `fetch` vers `/v1/auth/me` dans `/bff/auth/callback` n'a pas de timeout.
- **Impact estime :** Un service auth lent empeche tous les nouveaux logins.
- **Recommandation :** Ajouter `signal: AbortSignal.timeout(10_000)`.

#### [FND-003] Absence de timeout sur l'appel fetch de refresh de session
- **Severite :** High
- **Effort :** Quick Win
- **Priorite :** 9
- **Localisation :** `services/bff/src/middleware/session.ts:89-93`
- **Description :** L'appel fetch vers `/v1/auth/refresh` dans `doRefresh()` n'a pas de timeout. Le mutex `refreshLocks` limite l'impact par session, mais n'empeche pas le blocage initial.
- **Recommandation :** Ajouter `signal: AbortSignal.timeout(10_000)`.

#### [FND-009] Double serialisation du body dans le proxy API
- **Severite :** High
- **Effort :** Quick Win
- **Priorite :** 9
- **Localisation :** `services/bff/src/routes/proxy.ts:42`
- **Description :** Le proxy fait `JSON.stringify(request.body)` -- Fastify a deja parse le JSON entrant, donc on re-serialise inutilement. Pour un payload de 1MB, ca represente 10-15ms de CPU.
- **Recommandation :** Configurer `parseAs: 'string'` sur la route proxy, ou migrer vers `@fastify/http-proxy` pour un proxy transparent.

#### [FND-010] Reponse proxy lue en entier en memoire (res.text())
- **Severite :** High
- **Effort :** Medium
- **Priorite :** 6
- **Localisation :** `services/bff/src/routes/proxy.ts:50`
- **Description :** `await res.text()` buffer l'integralite de la reponse backend en RAM. Le proxy SSE utilise correctement le streaming avec `pipe()`, mais le proxy API standard ne le fait pas.
- **Impact estime :** Consommation memoire proportionnelle aux reponses + TTFB degrade.
- **Recommandation :** Streamer via `Readable.fromWeb(res.body)` ou migrer vers `@fastify/reply-from`.

### Backend -- Memory & Event Loop

#### [FND-004] Array.shift() sur les timestamps de monitoring -- O(n) dans le hot path
- **Severite :** High
- **Effort :** Medium
- **Priorite :** 6
- **Localisation :** `services/bff/src/modules/monitoring/service.ts:191-193`
- **Description :** `pruneRecentRequestTimestamps()` utilise `Array.shift()` en boucle while -- O(n) par shift. Appele a chaque requete. A 200 req/s avec ~12000 elements, c'est ~2.4M d'operations memoire par seconde.
- **Recommandation :** Utiliser un ring buffer pre-alloue ou `splice(0, idx)` en une seule operation.

#### [FND-005] Array.shift() sur recentDurationsMs
- **Severite :** Medium
- **Effort :** Quick Win
- **Priorite :** 6
- **Localisation :** `services/bff/src/modules/monitoring/service.ts:167`
- **Description :** Meme pattern que FND-004 mais plafonne a 400 elements -- impact plus modere.
- **Recommandation :** Ring buffer de taille fixe (Float64Array de 400).

#### [FND-006] Map refreshLocks globale sans limite de taille
- **Severite :** Medium
- **Effort :** Quick Win
- **Priorite :** 6
- **Localisation :** `services/bff/src/middleware/session.ts:13`
- **Description :** Combine avec l'absence de timeout (FND-003), les promesses de refresh s'accumulent en memoire si le service auth est bloque.
- **Recommandation :** Le fix de FND-003 resout l'essentiel. En complement, ajouter un guard `if (refreshLocks.size > 1000) return null`.

#### [FND-007] Persistence SQLite synchrone (writeFileSync) toutes les 10 secondes
- **Severite :** Medium
- **Effort :** Medium
- **Priorite :** 4
- **Localisation :** `services/bff/src/session/store.ts:187-193`
- **Description :** `db.export()` + `fs.writeFileSync()` bloque l'event loop. Pour >10000 sessions, le blocage peut atteindre 10-50ms.
- **Recommandation :** Remplacer par `fs.writeFile` async avec atomic rename (write to .tmp + rename).

#### [FND-008] Absence de compression HTTP (gzip/brotli)
- **Severite :** Medium
- **Effort :** Quick Win
- **Priorite :** 6
- **Localisation :** `services/bff/src/index.ts`
- **Description :** Aucune compression configuree. Les reponses JSON se compressent a 70-85%.
- **Recommandation :** `pnpm add @fastify/compress` puis `await app.register(fastifyCompress, { global: true })`.

#### [FND-011] Tri du tableau de durations a chaque getSummary()
- **Severite :** Low
- **Effort :** Quick Win
- **Priorite :** 3
- **Localisation :** `services/bff/src/modules/monitoring/service.ts:210`
- **Description :** Spread + sort de 400 elements a chaque appel monitoring (1x/5s). Impact marginal.
- **Recommandation :** Acceptable en l'etat. Si le buffer grossit, utiliser quickselect O(n).

---

## Matrice de priorisation

| # | Finding | Severite | Effort | Priorite | Categorie |
|---|---------|----------|--------|----------|-----------|
| 1 | FND-001 -- Pas de timeout sur fetch proxy API | Critical | Quick Win | 12 | Backend -- API |
| 2 | FND-002 -- Pas de timeout sur fetch auth callback | Critical | Quick Win | 12 | Backend -- API |
| 3 | FND-009 -- Double serialisation du body proxy | High | Quick Win | 9 | Backend -- API |
| 4 | FND-003 -- Pas de timeout sur fetch refresh session | High | Quick Win | 9 | Backend -- API |
| 5 | FND-008 -- Absence de compression HTTP | Medium | Quick Win | 6 | Backend -- API |
| 6 | FND-005 -- Array.shift() sur recentDurationsMs | Medium | Quick Win | 6 | Backend -- Memory |
| 7 | FND-006 -- refreshLocks Map sans limite | Medium | Quick Win | 6 | Backend -- Memory |
| 8 | FND-004 -- Array.shift() sur timestamps monitoring | High | Medium | 6 | Backend -- Memory |
| 9 | FND-010 -- Reponse proxy lue en entier en memoire | High | Medium | 6 | Backend -- API |
| 10 | FND-007 -- writeFileSync dans persist() | Medium | Medium | 4 | Backend -- Event Loop |
| 11 | FND-011 -- Tri array a chaque getSummary() | Low | Quick Win | 3 | Backend -- Low-Level |

## Quick Wins (a faire immediatement)

1. **FND-001 + FND-002 + FND-003 -- Ajouter `AbortSignal.timeout()` sur tous les fetch** (30 min)
2. **FND-009 -- Eviter la double serialisation dans le proxy** (20 min)
3. **FND-008 -- Activer la compression Fastify** (10 min)
4. **FND-005 + FND-006 -- Micro-fixes monitoring + refreshLocks** (15 min)

## Recommandations a moyen terme

1. **FND-004 -- Ring buffer pour les timestamps de monitoring** (1-2h)
2. **FND-010 -- Streaming des reponses proxy** via `@fastify/reply-from` (2-3h) -- elimine aussi FND-009
3. **FND-007 -- Persistence asynchrone de la session DB** (1-2h)

## Refactorings structurels

Aucun refactoring lourd necessaire. La migration du proxy vers `@fastify/http-proxy` / `@fastify/reply-from` est le changement avec le meilleur ROI global (~3h pour eliminer FND-009 + FND-010 d'un coup).

## Metriques a surveiller

- **API response time p95** -- Objectif < 200ms hors latence backend
- **Memory heap usage trend** -- Pattern sawtooth attendu, ratchet = fuite
- **Event loop delay** -- `perf_hooks.monitorEventLoopDelay()`, p99 < 50ms
- **Session store size** -- Anticiper l'impact de `db.export()`

## Outils recommandes

| Finding | Outil de validation | Ce qu'on verifie |
|---|---|---|
| FND-001/002/003 | `autocannon -c 100 -d 30` | Latence p95, comportement backend lent |
| FND-004/005 | `clinic flame -- node dist/index.js` | Hot functions flame graph |
| FND-007 | `clinic doctor -- node dist/index.js` | Event loop delay |
| FND-008 | `curl -H "Accept-Encoding: gzip" -v` | Header Content-Encoding |
| FND-009/010 | `autocannon` + `curl -w "%{time_starttransfer}"` | TTFB et throughput |

## Plan de validation

1. **Baseline** : `npx autocannon -c 50 -d 30 http://localhost:3000/bff/api/v1/backend/healthz`
2. **Appliquer Quick Wins** (FND-001 a FND-003, FND-008, FND-009)
3. **Re-mesurer** : meme commande autocannon
4. **Profiling CPU** : `npx clinic flame -- node dist/index.js` pendant autocannon
5. **Memory** : `node --trace-gc dist/index.js` pendant charge -- pauses GC < 10ms
6. **Streaming** : apres `@fastify/reply-from`, mesurer TTFB avec `curl -w "%{time_starttransfer}\n"`
