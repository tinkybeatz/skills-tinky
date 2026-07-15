# Audit de Performance Complet -- Sapain Borne

**Date :** 15 avril 2026
**Scope :** Monorepo `sapain-borne` (back-office, bff, backend, auth, email)
**Objectif :** Identifier les goulots d'etranglement et risques de performance avant mise en production

---

## Synthese executive

Le projet est globalement bien structure avec une architecture hexagonale propre, des patterns de resilience (circuit breaker, retry, outbox), et un bon usage du lazy loading cote frontend. Cependant, plusieurs problemes de performance meritent une attention immediate avant la mise en production, principalement autour des **requetes SQL N+1**, de l'**absence de cache applicatif**, de l'**absence de compression HTTP**, et de la **session store SQLite du BFF**.

### Scoring par domaine

| Domaine | Note | Priorite |
|---------|------|----------|
| Requetes SQL / Base de donnees | 5/10 | CRITIQUE |
| Cache applicatif | 3/10 | CRITIQUE |
| Compression HTTP / Reseau | 4/10 | HAUTE |
| Session Store BFF (SQLite) | 5/10 | HAUTE |
| Frontend (React) | 7/10 | MOYENNE |
| Workers & Background Jobs | 8/10 | BASSE |
| Docker / Infrastructure | 7/10 | MOYENNE |
| Resilience inter-services | 9/10 | BASSE |

---

## 1. CRITIQUE -- Requetes SQL N+1 et sous-requetes correlees

**Fichier :** `services/backend/src/modules/admin/queries.ts`

`querySitesOverview()` (lignes 37-52) execute **6 sous-requetes scalaires correlees par site** :
```sql
SELECT s.site_id, s.name,
  (SELECT COUNT(*) FROM kiosks k WHERE k.site_id = s.site_id),
  (SELECT COUNT(*) FROM kiosks k WHERE k.site_id = s.site_id AND k.status = 'active'),
  (SELECT COUNT(*) FROM program_catalog_items p WHERE p.site_id = s.site_id ...),
  (SELECT COUNT(DISTINCT a.account_id) FROM subscriptions sub JOIN accounts a ...),
  (SELECT COUNT(*) FROM subscriptions sub WHERE sub.site_id = s.site_id ...),
  (SELECT COUNT(*) FROM registration_requests rr WHERE rr.site_id = s.site_id ...)
FROM sites s
```

Pour 10 sites, cela genere potentiellement **60 requetes imbriquees**. PostgreSQL peut parfois optimiser, mais ce n'est pas garanti, surtout avec la jointure `COUNT(DISTINCT) ... JOIN accounts`.

`queryKiosksBySite()` (lignes 100-114) execute **2 sous-requetes correlees par kiosque** sur `kiosk_event_inbox` (table potentiellement volumineuse).

`queryPlatformStats()` (lignes 201-212) execute **8 COUNT(*)** dans un seul SELECT -- full table scans a chaque appel dashboard.

**Recommandation :** Remplacer par des CTEs/LEFT JOINs. Ajouter un index partiel pour les requetes temporelles sur `kiosk_event_inbox`. Considerer une vue materialisee pour `queryPlatformStats`.

**Impact estime :** Gain de 50-80% sur le temps de reponse du dashboard admin.

---

## 2. CRITIQUE -- Absence totale de cache applicatif

Aucun service n'utilise de cache en memoire ou distribue. Chaque requete API declenche un aller-retour complet vers PostgreSQL, meme pour des donnees rarement modifiees :
- Catalogue de programmes (change 1-2x/semaine)
- Configuration de site (change rarement)
- Stats dashboard (`queryPlatformStats` -- pourrait etre cache 30-60s)
- Validation API keys kiosk (`kioskAuthService.authenticate` -- hash + lookup DB a chaque requete kiosk)

**Recommandation :** Cache TTL en memoire (simple Map + TTL) pour `authenticate()` (5 min), `queryPlatformStats` (30-60s), catalogue (5 min invalide sur mutation). Le `staleTime: 30_000` du frontend (fichier `services/back-office/src/app/providers/index.tsx`) est un bon debut.

**Impact estime :** Reduction de 60-90% des requetes DB pour les endpoints de lecture frequents.

---

## 3. HAUTE -- Absence de compression HTTP (gzip/brotli)

Aucun service backend n'utilise de compression. Recherche de "gzip", "compression", "brotli", "compress" dans les services : zero resultat pertinent.

- **Backend** (`services/backend/src/infra/http/server.ts`) : serveur HTTP natif Node.js, pas de middleware
- **BFF** (`services/bff/src/index.ts`) : Fastify sans `@fastify/compress`
- **Auth** (`services/auth/src/infra/http/server.ts`) : Fastify sans `@fastify/compress`
- **Back-office** en prod : servi par `serve` (nixpacks.toml) qui supporte gzip -- OK cote frontend

**Recommandation :** Ajouter `@fastify/compress` au BFF et Auth. Pour le backend (node:http natif), configurer la compression au niveau Traefik.

**Impact estime :** Reduction de 70-80% de la taille des reponses JSON.

---

## 4. HAUTE -- Session Store BFF sur SQLite WASM (sql.js)

**Fichier :** `services/bff/src/session/store.ts`

Le BFF utilise **sql.js** (SQLite WASM) avec persistance disque toutes les 10s. Problemes :

1. **`this.db.export()` + `fs.writeFileSync`** (ligne 188-189) : bloquent l'event loop. L'export serialise la DB entiere en memoire, puis writeFileSync fait un I/O bloquant.
2. **Pas de scalabilite horizontale** : sessions locales a une instance.
3. **`get()` met a jour `last_activity` a chaque lecture** (ligne 140) : declenchant dirty flag et ecriture.
4. **Fenetre de perte de donnees** : 10s entre persistances.

**Recommandation court terme :** Remplacer `writeFileSync` par `writeFile` async. Throttle le `last_activity` update (seuil 60s). **Moyen terme :** Migrer vers `better-sqlite3` (deja dans les deps root) ou PostgreSQL pour les sessions.

---

## 5. MOYENNE -- Frontend : optimisations manquantes

**Fichier :** `services/back-office/index.html`

1. **Pas de preload des fonts** : Poppins et Host Grotesk declarees dans `tailwind.config.js` mais aucun `<link rel="preload">` ni `<link rel="preconnect">`. Causera FOIT/FOUT.
2. **Tailwind safelist trop large** (`tailwind.config.js` lignes 4-18) : 17 classes en safelist empechent le tree-shaking.
3. **Inline SVG icons dans EmployeeTable** (`services/back-office/src/features/manage-employees/ui/EmployeeTable.tsx` lignes 304-332) : `EditIcon`, `MailIcon`, `TrashIcon` recrees a chaque rendu. A 50+ employes = 150+ instances.
4. **Closures non memoizees** dans les callbacks onChange de `FilterBar` (ligne 265).

**Points positifs :** Lazy loading complet via `React.lazy()`, bon usage de `useMemo` pour filtering/sorting, `staleTime: 30_000` sur le QueryClient.

**Impact estime :** Amelioration du LCP de 200-500ms (fonts).

---

## 6. MOYENNE -- Outbox Worker : index manquant pour la purge

**Fichier :** `services/backend/src/infra/worker/outboxWorker.ts` (lignes 93-115)

L'index `idx_outbox_unprocessed` couvre `WHERE processed_at IS NULL`, mais la purge filtre `WHERE processed_at IS NOT NULL AND processed_at < ...` -- cet index ne couvre pas la purge.

**Recommandation :** `CREATE INDEX CONCURRENTLY idx_outbox_purge ON outbox_events (processed_at) WHERE processed_at IS NOT NULL;`

---

## 7. MOYENNE -- Proxy BFF : double serialisation JSON

**Fichier :** `services/bff/src/routes/proxy.ts` (lignes 37-52)

Le proxy parse le JSON (Fastify), puis le re-serialise (`JSON.stringify(request.body)`) pour le backend. Overhead CPU inutile.

**Recommandation :** Configurer un content type parser qui garde le body comme string brute, ou streamer directement.

---

## 8. BASSE -- Reconciliation Worker sequentiel

**Fichier :** `services/backend/src/infra/worker/reconciliationWorker.ts` (lignes 70-94)

Webhook re-trigger sequentiel (`for...of` avec `await`). Le pattern `runWithConcurrency` existe deja dans `eventBus.ts` et pourrait etre reutilise.

---

## 9. BASSE -- SSE Broadcaster : ring buffer sans TTL

**Fichier :** `services/backend/src/modules/alerting/sseBroadcaster.ts`

Ring buffer (1000 items max) sans purge par age. Evenements anciens restent en memoire indefiniment si le debit est faible.

---

## 10. Points positifs (bonnes pratiques deja en place)

1. **Lazy loading complet** des pages React avec `React.lazy()` et `Suspense`
2. **TanStack Query** avec `staleTime: 30_000` et `retry: 1`
3. **Outbox pattern** avec concurrence bornee et dead-letter handling
4. **Circuit breaker + resilient fetch** (`packages/shared-infra/src/circuitBreaker.ts`)
5. **Pool PG** correctement configure (`max: 10`, idle timeout 30s, connection timeout 5s)
6. **Multi-stage Docker builds** avec images slim et `USER node`
7. **Exponential backoff** sur tous les workers
8. **Body size limit** (1 MB dans `readJsonBody`)
9. **RLS** avec `withTenant()` pour l'isolation multi-site
10. **Graceful shutdown** sur tous les services
11. **API client robuste** (`services/back-office/src/shared/api/client.ts`) avec retry, timeout, jitter, et gestion 401 centralisee

---

## Plan d'action priorise

### Avant mise en prod (~6h)

| # | Action | Effort | Impact |
|---|--------|--------|--------|
| 1 | Reecrire `querySitesOverview` et `queryKiosksBySite` avec CTEs | 2h | Critique |
| 2 | Cache TTL memoire pour `authenticate()` et `queryPlatformStats` | 3h | Critique |
| 3 | Remplacer `writeFileSync` par `writeFile` async dans session store BFF | 30min | Haute |
| 4 | Ajouter `@fastify/compress` au BFF et Auth | 30min | Haute |
| 5 | Ajouter `<link rel="preload">` fonts dans `index.html` | 15min | Moyenne |

### Sprint suivant (J+14)

| # | Action | Effort | Impact |
|---|--------|--------|--------|
| 6 | Eliminer double serialisation JSON dans le proxy BFF | 2h | Moyenne |
| 7 | Ajouter index `idx_outbox_purge` | 15min | Moyenne |
| 8 | Paralleliser reconciliation worker | 1h | Basse |
| 9 | Migrer session store sql.js vers better-sqlite3 | 4h | Haute |
| 10 | Nettoyer safelist Tailwind | 30min | Basse |

### Backlog technique

| # | Action | Effort |
|---|--------|--------|
| 11 | Vue materialisee pour stats dashboard | 4h |
| 12 | Migrer sessions vers PostgreSQL (scale horizontal) | 8h |
| 13 | TTL sur ring buffer SSE | 1h |
| 14 | Metriques Prometheus (p50/p95/p99 par endpoint) | 8h |
| 15 | Compression Traefik si pas deja configuree | 1h |
