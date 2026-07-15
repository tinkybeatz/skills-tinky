# Rapport d'Analyse de Performance

## Resume executif

Perimetre analyse : monorepo **sapain-borne** comprenant 6 services -- back-office (React/Vite/Tailwind), BFF (Fastify + SQLite sessions), backend (Node.js HTTP natif + PostgreSQL), auth (Fastify + PostgreSQL), email (Node.js worker + PostgreSQL), et un client Electron. Analyse statique complete du code source couvrant le frontend, le backend et les couches bas niveau (V8, allocation memoire, event loop).

**Bilan :** 18 findings identifies -- 1 Critical, 6 High, 8 Medium, 3 Low. Le codebase est globalement bien structure avec de bonnes pratiques (lazy loading, React Query avec staleTime, pool PG configure, outbox pattern, pino logger). Les problemes principaux se concentrent sur un pattern N+1 dans le repository accounts, l'absence de compression HTTP, et des console.log de debug laisses en production.

**Top 3 recommandations :**
1. Eliminer le pattern N+1 dans `listBySite` / `listAll` du repository accounts (Critical)
2. Supprimer les console.log de debug dans le back-office avant la MEP (High)
3. Ajouter la compression gzip/brotli sur le backend et le BFF (High)

## Score global

**72 / 100 -- Bon**

Le projet est dans un bon etat general. Les fondations architecturales sont solides (hexagonal architecture, event sourcing via outbox, lazy loading). Les problemes identifies sont majoritairement des quick wins ou des ameliorations medium qui ne necessitent pas de refactoring lourd.

---

## Findings

### Backend -- DB

#### [FND-001] Pattern N+1 dans `PgAccountRepository.listBySite()` et `listAll()`
- **Severite :** Critical
- **Effort :** Medium
- **Priorite :** 8
- **Localisation :** `services/backend/src/modules/accounts/repository.ts:127-149`
- **Description :** Les methodes `listBySite()` et `listAll()` executent d'abord une requete pour recuperer les comptes, puis appellent `loadAccountDetails()` pour chaque compte via `Promise.all(result.rows.map(...))`. Chaque appel a `loadAccountDetails` lance 2 requetes supplementaires (subscriptions + loyalty_wallets). Pour N comptes, cela genere 1 + 2N requetes SQL.
- **Impact estime :** Avec 100 comptes, cela produit 201 requetes SQL au lieu de 3. Sur `listAll()` qui a un LIMIT 500, le pire cas est 1001 requetes. Latence potentiellement >5s sous charge.
- **Recommandation :**
  ```sql
  -- Option 1 : JOINs
  SELECT a.*, s.subscription_id, ..., lw.loyalty_wallet_id, ...
  FROM accounts a
  LEFT JOIN subscriptions s ON s.account_id = a.account_id
  LEFT JOIN loyalty_wallets lw ON lw.account_id = a.account_id
  WHERE a.status = 'active'

  -- Option 2 : 2 requetes batch avec WHERE account_id = ANY($1)
  SELECT * FROM subscriptions WHERE account_id = ANY($1::uuid[])
  SELECT * FROM loyalty_wallets WHERE account_id = ANY($1::uuid[])
  ```

#### [FND-002] `markExpiredRequests()` appele systematiquement avant chaque lecture
- **Severite :** Medium
- **Effort :** Medium
- **Priorite :** 4
- **Localisation :** `services/backend/src/modules/registrations/repository/requestRepository.ts:96,133`
- **Description :** Les fonctions `findRequestByIdForKiosk` et `findRequestByTokenHash` appellent `markExpiredRequests(db)` avant chaque lecture. Cette fonction execute un UPDATE sur toutes les lignes expirees de la table.
- **Impact estime :** Chaque poll de statut par un kiosk declenche une ecriture supplementaire. Sous charge (10 kiosks pollant toutes les 2s), cela represente 300 UPDATEs/min.
- **Recommandation :** Deplacer `markExpiredRequests` dans un job periodique et filtrer les expirees en lecture avec `WHERE expires_at > NOW() OR status = 'completed'`.

#### [FND-003] `SELECT *` sur des fonctions SQL dans les routes kiosks et site-config
- **Severite :** Low
- **Effort :** Quick Win
- **Priorite :** 3
- **Localisation :** `services/backend/src/modules/site-config/routes.ts:28,62,123` et `services/backend/src/modules/kiosks/queries.ts:37,45,56,82`
- **Description :** Utilisation de `SELECT * FROM function_name(...)` au lieu de selectionner les colonnes specifiques.
- **Recommandation :** Specifier les colonnes attendues.

### Backend -- API

#### [FND-004] Absence de compression HTTP (gzip/brotli) sur tous les services
- **Severite :** High
- **Effort :** Quick Win
- **Priorite :** 9
- **Localisation :** `services/backend/src/infra/http/server.ts`, `services/bff/src/index.ts`, `services/auth/src/infra/http/server.ts`
- **Description :** Aucun des services n'active la compression des reponses.
- **Impact estime :** Les reponses JSON non compressees, reduction potentielle de 70-80%.
- **Recommandation :** BFF/Auth: `@fastify/compress`. Backend: `zlib.createGzip()` ou reverse proxy.

#### [FND-005] Route matching O(n) sur chaque requete dans le backend
- **Severite :** Low
- **Effort :** Quick Win
- **Priorite :** 3
- **Localisation :** `services/backend/src/infra/http/server.ts:119-121`
- **Description :** Routing via `routes.find()` lineaire. Negligeable avec ~30 routes.
- **Recommandation :** Passer a un `Map<string, RouteDefinition>` quand le nombre de routes augmentera.

#### [FND-006] `res.end` monkey-patching pour capture de payload
- **Severite :** Medium
- **Effort :** Medium
- **Priorite :** 4
- **Localisation :** `services/backend/src/infra/http/server.ts:170-179`
- **Description :** Monkey-patche `res.end` pour capturer le payload + JSON.parse supplementaire sur chaque reponse.
- **Recommandation :** Refactorer pour un pattern explicite `{ status, payload }`.

### Backend -- Memory

#### [FND-007] SSEBroadcaster ring buffer sans limite temporelle
- **Severite :** Medium
- **Effort :** Quick Win
- **Priorite :** 6
- **Localisation :** `services/backend/src/modules/alerting/sseBroadcaster.ts:85-88`
- **Description :** Ring buffer de 1000 evenements sans TTL.
- **Recommandation :** Ajouter un TTL de 1h sur les evenements bufferises.

#### [FND-008] RegistrationSSEHub sans limite de connexions par registrationRequestId
- **Severite :** Medium
- **Effort :** Quick Win
- **Priorite :** 6
- **Localisation :** `services/backend/src/modules/registrations/sseHub.ts:23-37`
- **Description :** Nombre illimite de connexions SSE par ID. Risque DoS.
- **Recommandation :** Limiter a max 5 connexions par ID + HTTP 429.

#### [FND-009] `pgAlertListener` cree un Pool de taille 1 isole
- **Severite :** Low
- **Effort :** Quick Win
- **Priorite :** 3
- **Localisation :** `services/backend/src/modules/alerting/pgAlertListener.ts:21`
- **Description :** Pool PG dedie pour LISTEN/NOTIFY. Correct mais a documenter.

### Backend -- Low-Level (Event Loop)

#### [FND-010] Boucle sequentielle `for...of` avec `await` dans le reconciliation worker
- **Severite :** High
- **Effort :** Quick Win
- **Priorite :** 9
- **Localisation :** `services/backend/src/infra/worker/reconciliationWorker.ts:70-93`
- **Description :** Webhooks appeles sequentiellement. 20 users = 100s au lieu de ~5s.
- **Recommandation :** `runWithConcurrency(missing, handler, 5)`

#### [FND-011] Handlers outbox sequentiels
- **Severite :** Medium
- **Effort :** Quick Win
- **Priorite :** 6
- **Localisation :** `services/backend/src/shared/eventBus.ts:233-235`
- **Description :** Handlers executes sequentiellement — throughput penalise.
- **Recommandation :** Evaluer si parallelisable, sinon documenter.

### Frontend -- Bundle

#### [FND-012] Absence de `sideEffects: false` dans les package.json
- **Severite :** Low
- **Effort :** Quick Win
- **Priorite :** 3
- **Localisation :** `services/back-office/package.json`
- **Description :** Tree-shaking sous-optimal.
- **Recommandation :** Ajouter `"sideEffects": false`.

### Frontend -- React

#### [FND-013] `console.log` de debug en production
- **Severite :** High
- **Effort :** Quick Win
- **Priorite :** 9
- **Localisation :** `services/back-office/src/pages/employees/index.tsx:21-23,27,42-44,49,51`, `Modal.tsx:62,66`, `AuthGuard.tsx:9`
- **Description :** 12+ console.log de debug. Synchrones, serialisation couteuse.
- **Recommandation :** Supprimer ou utiliser `import.meta.env.DEV ? console.log : () => {}`.

#### [FND-014] searchSource recree a chaque render
- **Severite :** High
- **Effort :** Quick Win
- **Priorite :** 9
- **Localisation :** `services/back-office/src/pages/employees/index.tsx:62-83`
- **Description :** Nouvel objet a chaque render, re-enregistrement dans SearchProvider.
- **Recommandation :** `useMemo` avec `[employees]` comme dependance.

#### [FND-015] columns array sans useMemo dans EmployeeTable
- **Severite :** Medium
- **Effort :** Quick Win
- **Priorite :** 6
- **Localisation :** `services/back-office/src/features/manage-employees/ui/EmployeeTable.tsx:120-233`
- **Description :** 300+ closures recreees a chaque keystroke.
- **Recommandation :** `useMemo` avec `[editingId, editFirstName, editLastName, saving]`.

#### [FND-016] Inline arrow functions dans EmployeesPage
- **Severite :** Medium
- **Effort :** Quick Win
- **Priorite :** 6
- **Localisation :** `services/back-office/src/pages/employees/index.tsx:209-265`
- **Description :** Callbacks inline recreant des references.
- **Recommandation :** Extraire avec `useCallback`.

### Frontend -- Assets

#### [FND-017] Sourcemaps desactives en production
- **Severite :** Medium
- **Effort :** Quick Win
- **Priorite :** 6
- **Localisation :** `services/back-office/vite.config.ts:33`
- **Description :** `sourcemap: false` rend le debugging prod impossible.
- **Recommandation :** `sourcemap: 'hidden'` + upload vers Sentry.

### Backend -- Low-Level (Serialisation)

#### [FND-018] console.log/error dans auth au lieu de pino
- **Severite :** High
- **Effort :** Quick Win
- **Priorite :** 9
- **Localisation :** `services/auth/src/modules/auth/service.ts:181,184,210,366,767,977`, `services/auth/src/modules/gdpr/worker.ts:59,64,73`
- **Description :** console.log synchrone sur hot path auth. Pino est 5-10x plus rapide.
- **Recommandation :** Migrer vers pino.

---

## Matrice de priorisation

| # | Finding | Severite | Effort | Priorite | Categorie |
|---|---------|----------|--------|----------|-----------|
| 1 | FND-004 Compression HTTP | High | Quick Win | 9 | Backend -- API |
| 2 | FND-010 Reconciliation sequentielle | High | Quick Win | 9 | Backend -- EventLoop |
| 3 | FND-013 console.log debug front | High | Quick Win | 9 | Frontend -- React |
| 4 | FND-014 searchSource sans memo | High | Quick Win | 9 | Frontend -- React |
| 5 | FND-018 console.log auth | High | Quick Win | 9 | Backend -- Serialisation |
| 6 | FND-001 N+1 accounts | Critical | Medium | 8 | Backend -- DB |
| 7 | FND-007 SSE sans TTL | Medium | Quick Win | 6 | Backend -- Memory |
| 8 | FND-008 SSEHub sans limite | Medium | Quick Win | 6 | Backend -- Memory |
| 9 | FND-011 Handlers outbox seq | Medium | Quick Win | 6 | Backend -- EventLoop |
| 10 | FND-015 columns sans memo | Medium | Quick Win | 6 | Frontend -- React |
| 11 | FND-016 Inline arrows | Medium | Quick Win | 6 | Frontend -- React |
| 12 | FND-017 Sourcemaps | Medium | Quick Win | 6 | Frontend -- Assets |
| 13 | FND-002 markExpired | Medium | Medium | 4 | Backend -- DB |
| 14 | FND-006 Monkey-patch res.end | Medium | Medium | 4 | Backend -- API |
| 15 | FND-003 SELECT * | Low | Quick Win | 3 | Backend -- DB |
| 16 | FND-005 Route O(n) | Low | Quick Win | 3 | Backend -- API |
| 17 | FND-009 Pool PG LISTEN | Low | Quick Win | 3 | Backend -- Memory |
| 18 | FND-012 sideEffects | Low | Quick Win | 3 | Frontend -- Bundle |

## Quick Wins (a faire immediatement)

1. **FND-013** -- Supprimer console.log debug front
2. **FND-018** -- Migrer console vers pino dans auth
3. **FND-004** -- @fastify/compress
4. **FND-014** -- useMemo searchSource
5. **FND-010** -- Paralleliser reconciliation
6. **FND-015** -- useMemo columns
7. **FND-007** -- TTL ring buffer SSE
8. **FND-008** -- Limite connexions SSE

## Recommandations a moyen terme

- **FND-001** -- Refactorer N+1 accounts (2-4h)
- **FND-002** -- Deplacer markExpiredRequests en cron (1-2h)
- **FND-006** -- Supprimer monkey-patching res.end (2-4h)

## Refactorings structurels

Aucun refactoring lourd necessaire. Si trafic >100 req/s : envisager Fastify pour le backend + cache applicatif Redis.

## Metriques a surveiller

- Core Web Vitals (LCP, INP, CLS) -- seuils : LCP < 2.5s, INP < 200ms, CLS < 0.1
- API response time p95 sur `/v1/backend/accounts/*`
- Memory heap usage trend
- Bundle size (parsed + gzip)
- PostgreSQL connections actives
- Outbox event processing latency

## Outils recommandes

| Finding | Outil de validation | Commande |
|---------|-------------------|----------|
| FND-001 | PostgreSQL EXPLAIN ANALYZE | `EXPLAIN ANALYZE SELECT ... FROM accounts a LEFT JOIN subscriptions s ...` |
| FND-004 | curl header check | `curl -sI -H "Accept-Encoding: gzip" http://localhost:3000/v1/backend/accounts` |
| FND-013/018 | ESLint no-console | `eslint --rule '{"no-console": "error"}' services/` |
| FND-014/015 | React DevTools Profiler | Extension navigateur |
| Bundle | vite-bundle-visualizer | `npx vite-bundle-visualizer` |
| Load test | autocannon | `npx autocannon -c 50 -d 30 http://localhost:3000/v1/backend/accounts` |
| Memory | clinic doctor | `npx clinic doctor -- node services/backend/dist/index.js` |

## Plan de validation

1. **Baseline** : `npx vite-bundle-visualizer` + `npx autocannon -c 50 -d 30` + `EXPLAIN ANALYZE`
2. **Post Quick Wins** : curl compression + ESLint no-console + React DevTools Profiler
3. **Post FND-001** : EXPLAIN ANALYZE (1-3 queries) + autocannon p95 < 100ms
4. **Monitoring continu** : web-vitals RUM + metriques outbox
