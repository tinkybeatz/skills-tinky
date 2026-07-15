# Rapport d'analyse de performance -- Back-Office React (services/back-office)

**Date :** 15 avril 2026
**Scope :** `services/back-office/src/` -- application React 19 + Vite 6 + TanStack Query 5 + Zustand 5 + Tailwind CSS 3

---

## Resume executif

L'application est globalement bien architecturee (lazy-loading des routes, code-splitting, Zustand avec selectors). Cependant, plusieurs problemes concrets expliquent la sensation de lenteur lors de la navigation entre pages. Les causes principales sont : des re-renders en cascade provoques par le layout, des objets recrees a chaque render, des console.log en production, et une absence de memoisation sur les composants lourds.

---

## 1. Problemes identifies

### 1.1 [CRITIQUE] Re-renders en cascade dans AppLayout

**Fichier :** `src/app/layouts/AppLayout.tsx`

Le composant `AppLayout` contient le `<Outlet />` (toutes les pages). A chaque navigation, l'AppLayout se re-rend, et avec lui **toute la Sidebar et la TopBar**, car :

- Les objets `sections` et `user` sont recrees a chaque render (lignes 23-28 et 30-37). Ces objets sont passes comme props a `<Sidebar>` et `<TopBar>`, qui re-rendent systematiquement meme si les donnees n'ont pas change.
- `rawSections.map(...)` cree un nouveau tableau a chaque render sans `useMemo`.
- L'objet `user` (initials, name, email, badge) est un nouvel objet literal a chaque render.

**Impact :** Chaque changement de page re-rend Sidebar + TopBar + leurs sous-arbres complets.

**Recommandation :** Memoiser avec `useMemo` + ajouter `React.memo` sur `Sidebar` et `TopBar`.

### 1.2 [CRITIQUE] console.log en production -- travail synchrone bloquant

**Fichiers concernes :**
- `src/features/auth/ui/AuthGuard.tsx` (ligne 9) -- execute a chaque render du guard, donc a chaque navigation
- `src/pages/employees/index.tsx` (lignes 21-23, 42-44, 48-49) -- 7 console.log par render
- `src/shared/ui/Modal.tsx` (ligne 63) -- a chaque ouverture/fermeture de modal

**Impact :** `console.log` est synchrone et bloquant. Avec la serialisation d'objets (window.location, searchParams), cela ajoute du travail sur le thread principal a chaque navigation.

### 1.3 [MAJEUR] searchSource recree a chaque render dans EmployeesPage et AdminDashboard

**Fichiers :** `src/pages/employees/index.tsx` (lignes 62-83), `src/pages/admin/index.tsx` (lignes 32-49)

L'objet `searchSource` est recree a chaque render, passe a `useRegisterSearch` qui appelle `registerSource` et `setActiveSource`, declenchant potentiellement des re-renders dans le SearchProvider.

### 1.4 [MAJEUR] Sidebar : useEffect ferme le menu mobile a chaque navigation

**Fichier :** `src/shared/ui/Sidebar.tsx` (lignes 50-53) -- un `useEffect` sur `location.pathname` avec ESLint desactive.

### 1.5 [MAJEUR] DataTable : calculs non memoises

**Fichier :** `src/shared/ui/DataTable.tsx` -- `splitColumnsForMobile(columns)` et `buildGridTemplate(columns)` sont appeles a chaque render sans memoisation.

### 1.6 [MAJEUR] EmployeeTable : columns recree a chaque render

**Fichier :** `src/features/manage-employees/ui/EmployeeTable.tsx` (lignes 120-233) -- le tableau `columns` capture l'etat d'edition et est reconstruit a chaque frappe dans le champ de recherche.

### 1.7 [MOYEN] useSSE : invalidation de queries trop large

**Fichier :** `src/shared/hooks/useSSE.ts` -- `queryClient.invalidateQueries({ queryKey: ["alerts"] })` sans `exact: true` invalide toutes les queries prefixees par "alerts".

### 1.8 [MOYEN] CustomerDashboard : rows recalculees a chaque render

**Fichier :** `src/pages/dashboard/index.tsx` -- `commonRows` et les widget builders creent du JSX a chaque render.

### 1.9 [MOYEN] SearchProvider : race condition sur les recherches

**Fichier :** `src/shared/search/SearchProvider.tsx` -- les `Promise.allSettled` lancees ne sont pas annulees quand une nouvelle recherche demarre.

### 1.10 [MOYEN] Absence de prefetching sur les routes

Aucun prefetching des chunks de pages n'est configure. Chaque clic attend le telechargement + parsing du chunk.

### 1.11 [MINEUR] Tailwind safelist trop large dans `tailwind.config.js`

### 1.12 [MINEUR] Pas de `React.memo` sur les composants de cellule du DataTable

### 1.13 [MINEUR] Vite build sans strategie de chunking (pas de `manualChunks` dans `vite.config.ts`)

---

## 2. Points positifs (a conserver)

- **Code-splitting** : toutes les pages sont `lazy()` avec `<Suspense>`
- **TanStack Query** : `staleTime: 30_000` et `refetchOnWindowFocus: false`
- **Zustand** : selectors granulaires, pas de re-render global
- **alertStore** : utilisation de `useShallow` pour les selectors filtrants
- **API client** : retry intelligent avec backoff exponentiel, timeout, gestion 401
- **SSE** : reconnexion avec backoff exponentiel
- **Session check** : revalidation au `visibilitychange`

---

## 3. Plan d'action priorise

| # | Priorite | Action | Effort | Impact |
|---|----------|--------|--------|--------|
| 1 | CRITIQUE | Memoiser `sections`/`user` dans AppLayout + `React.memo` Sidebar/TopBar | 30 min | Elimine re-renders shell a chaque navigation |
| 2 | CRITIQUE | Supprimer/conditionner les console.log | 15 min | Supprime travail synchrone |
| 3 | MAJEUR | Memoiser `searchSource` dans les pages | 20 min | Evite re-enregistrements SearchProvider |
| 4 | MAJEUR | Memoiser `columns` dans EmployeeTable et ProgramsPage | 30 min | Evite re-renders DataTable |
| 5 | MAJEUR | Memoiser `gridStyle`/`mobile` dans DataTable | 15 min | Reduit travail par render |
| 6 | MOYEN | Ajouter `exact: true` aux invalidations SSE | 10 min | Evite refetchs en cascade |
| 7 | MOYEN | Prefetching routes au hover dans Sidebar | 30 min | Navigation instantanee |
| 8 | MOYEN | Configurer `manualChunks` dans Vite | 15 min | Meilleur caching vendors |

**Temps total : ~3h pour les items 1-8**
