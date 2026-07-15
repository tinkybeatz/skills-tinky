# Rapport d'Analyse de Performance

## Resume executif

Perimetre analyse : back-office React (`services/back-office`) -- application SPA Vite + React 19 + TanStack Query + Zustand + Tailwind CSS, architecture Feature-Sliced Design (FSD).

Symptome rapporte : lenteur perceptible lors de la navigation entre les pages.

**17 findings identifies** : 2 Critical, 4 High, 8 Medium, 3 Low.

Top 3 recommandations :
1. **Supprimer les `console.log` de debug en production** (AuthGuard, EmployeesPage, Modal) -- ils bloquent le main thread a chaque render et navigation.
2. **Corriger le chargement des Google Fonts en render-blocking** -- 2 imports CSS externes non precharges qui retardent le FCP de 200-600ms.
3. **Stabiliser les references d'objets recrees a chaque render** dans AppLayout et les pages (sections, searchSource, columns) -- cause de re-renders en cascade sur toute la page.

## Score global

**62 / 100 -- Moyen** -- optimisations significatives necessaires

La base de code est bien structuree (lazy routes, React Query avec staleTime, Zustand avec selectors), mais plusieurs anti-patterns de performance s'accumulent et expliquent la sensation de lenteur a la navigation.

## Findings

### Frontend -- Bundle & Dependencies

#### [FND-001] Google Fonts charges via @import CSS (render-blocking)
- **Severite :** High
- **Effort :** Quick Win
- **Priorite :** 9
- **Localisation :** `services/back-office/src/app/styles/global.css:1-2`
- **Description :** Deux `@import url('https://fonts.googleapis.com/css2?...')` sont presentes dans le CSS global. Les `@import` CSS sont render-blocking : le navigateur doit telecharger le CSS Google Fonts avant de pouvoir parser le reste du stylesheet et commencer le rendu. Cela ajoute un aller-retour reseau supplementaire (DNS + TLS + HTTP) sur le chemin critique.
- **Impact estime :** FCP retarde de 200-600ms selon la connexion. FOIT (Flash of Invisible Text) pendant le chargement des fonts.
- **Recommandation :** Remplacer les `@import` par des `<link rel="preload" as="font">` dans `index.html`, ou mieux : self-host les fonts via `@fontsource/poppins` et `@fontsource/host-grotesk` (npm packages). Cela elimine le round-trip vers Google et permet le cache local.

#### [FND-002] CSP bloque les fonts Google mais le CSS les charge
- **Severite :** Medium
- **Effort :** Quick Win
- **Priorite :** 6
- **Localisation :** `services/back-office/index.html:6` + `services/back-office/src/app/styles/global.css:1-2`
- **Description :** Le Content-Security-Policy dans `index.html` definit `font-src 'self'` et `style-src 'self' 'unsafe-inline'` -- cela bloque les fonts et stylesheets provenant de `fonts.googleapis.com` et `fonts.gstatic.com`. Le CSS tente de charger des Google Fonts qui sont ensuite bloquees par la CSP, generant des erreurs console et un fallback sur les fonts systeme.
- **Impact estime :** Les fonts Poppins et Host Grotesk ne sont probablement pas appliquees en production si la CSP est strictement respectee.
- **Recommandation :** Self-host les fonts (recommande -- cf. FND-001), ou ajouter les domaines Google Fonts a la CSP.

#### [FND-003] lucide-react tree-shaking a verifier
- **Severite :** Low
- **Effort :** Quick Win
- **Priorite :** 3
- **Localisation :** `services/back-office/src/pages/dashboard/index.tsx:1`, `services/back-office/src/pages/admin/index.tsx:3`
- **Description :** `lucide-react` est importe avec des named imports. Avec Vite + ESM, le tree-shaking devrait fonctionner, mais il faut le verifier avec `npx vite-bundle-visualizer`.
- **Impact estime :** Potentiellement 50-150KB de bundle inutile si le tree-shaking echoue.
- **Recommandation :** Verifier via `npx vite-bundle-visualizer` apres un build.

### Frontend -- React Performance

#### [FND-004] console.log de debug laisses dans des composants critiques (hot path)
- **Severite :** Critical
- **Effort :** Quick Win
- **Priorite :** 12
- **Localisation :** `services/back-office/src/features/auth/ui/AuthGuard.tsx:9`, `services/back-office/src/pages/employees/index.tsx:21-23,30,42-44,48-49`, `services/back-office/src/shared/ui/Modal.tsx:64,67`
- **Description :** De nombreux `console.log` sont presents dans des composants qui s'executent a chaque navigation (AuthGuard) ou a chaque render (EmployeesPage avec 8 console.log, Modal). `console.log` est synchrone et bloque le main thread. AuthGuard est le wrapper de toutes les routes authentifiees, donc il re-render a chaque changement de route.
- **Impact estime :** 5-20ms bloques par navigation. Impact cumulatif significatif.
- **Recommandation :** Supprimer tous les `console.log` de debug, ou les wrapper derriere `import.meta.env.DEV`.

#### [FND-005] Objet `sections` recree a chaque render dans AppLayout
- **Severite :** High
- **Effort :** Quick Win
- **Priorite :** 9
- **Localisation :** `services/back-office/src/app/layouts/AppLayout.tsx:23-28`
- **Description :** Le tableau `sections` est recalcule a chaque render via `.map().filter()`. AppLayout est le layout permanent -- il re-render a chaque changement de route via `<Outlet />`. Chaque re-render cree de nouvelles references, causant un re-render complet de `<Sidebar>` (~200 lignes de JSX, NavLinks, SVG icons).
- **Impact estime :** Re-render de Sidebar a chaque navigation. Contribue directement a la sensation de lenteur.
- **Recommandation :** `useMemo(() => rawSections.map(...).filter(...), [rawSections, role])`.

#### [FND-006] Objets `user` recrees inline dans AppLayout
- **Severite :** Medium
- **Effort :** Quick Win
- **Priorite :** 6
- **Localisation :** `services/back-office/src/app/layouts/AppLayout.tsx:42-48,58-62`
- **Description :** L'objet `user` passe a `<Sidebar>` et `<TopBar>` est cree inline dans le JSX (deux fois). Chaque render cree 2 nouveaux objets, declenchant un re-render de Sidebar et TopBar.
- **Recommandation :** Memoiser avec `useMemo`.

#### [FND-007] `searchSource` objet recree a chaque render dans EmployeesPage
- **Severite :** High
- **Effort :** Quick Win
- **Priorite :** 9
- **Localisation :** `services/back-office/src/pages/employees/index.tsx:62-83`
- **Description :** L'objet `searchSource` est une variable locale dans le corps du composant, recree a chaque render avec une nouvelle closure sur `employees`.
- **Recommandation :** `useMemo<SearchSource>(() => ({...}), [employees])`.

#### [FND-008] `columns` array recree a chaque render dans EmployeeTable et ProgramsPage
- **Severite :** Medium
- **Effort :** Medium
- **Priorite :** 4
- **Localisation :** `services/back-office/src/features/manage-employees/ui/EmployeeTable.tsx:120-233`, `services/back-office/src/pages/programs/index.tsx:95-187`
- **Description :** Le tableau `columns` est recree a chaque render. Chaque keystroke dans le champ de recherche force un re-render complet de DataTable.
- **Recommandation :** `useMemo` avec les dependances necessaires (editingId, saving, etc.).

#### [FND-009] SearchProvider Context a la racine avec state qui change souvent
- **Severite :** Medium
- **Effort :** Medium
- **Priorite :** 4
- **Localisation :** `services/back-office/src/shared/search/SearchProvider.tsx:58-206`
- **Description :** La valeur du context est un objet recree a chaque render du provider (pas de `useMemo`), forcant un re-render de tous les consumers a chaque frappe.
- **Recommandation :** Memoiser la valeur du context, ou migrer vers Zustand.

#### [FND-010] DashboardGrid utilise `key={i}` (index comme key)
- **Severite :** Medium
- **Effort :** Quick Win
- **Priorite :** 6
- **Localisation :** `services/back-office/src/shared/ui/DashboardGrid.tsx:16-38`
- **Description :** `key={i}` empeche React de reconcilier correctement si les rows changent.
- **Recommandation :** Ajouter un `id` aux `LayoutRow`.

#### [FND-011] Fonctions inline onClick dans le dashboard
- **Severite :** Low
- **Effort :** Quick Win
- **Priorite :** 3
- **Localisation :** `services/back-office/src/pages/dashboard/index.tsx:57-61`
- **Description :** Arrow functions inline dans les onClick des ActionCard.
- **Recommandation :** Acceptable en l'etat.

### Frontend -- Assets & Rendering

#### [FND-012] Navigation icons definies comme composants fonctionnels dans le config
- **Severite :** Medium
- **Effort :** Medium
- **Priorite :** 4
- **Localisation :** `services/back-office/src/shared/config/navigation.tsx:115-386`
- **Description :** ~15 composants SVG custom (270 lignes) alors que `lucide-react` est deja une dependance. Overhead de reconciliation sur toutes ces instances a chaque render de Sidebar.
- **Recommandation :** Unifier sur `lucide-react`.

#### [FND-013] Sidebar CSS `backdrop-blur-sm` sur le mobile overlay
- **Severite :** Low
- **Effort :** Quick Win
- **Priorite :** 3
- **Localisation :** `services/back-office/src/shared/ui/Sidebar.tsx:62`
- **Description :** `backdrop-blur-sm` declenche un filtre GPU. Peut causer du jank sur mobile bas de gamme.
- **Recommandation :** Remplacer par `bg-black/40` sans blur sur mobile.

### Frontend -- Data Fetching & State

#### [FND-014] useSSE re-souscrit si addAlert change de reference
- **Severite :** Medium
- **Effort :** Quick Win
- **Priorite :** 6
- **Localisation :** `services/back-office/src/shared/hooks/useSSE.ts:49,117`
- **Description :** Le useEffect depend de `[user, queryClient, addAlert]`. Si le store est reconstruit (HMR), l'EventSource est ferme et reouvert.
- **Recommandation :** Utiliser des refs pour addAlert et queryClient, garder `[user]` seul comme dep.

#### [FND-015] useSessionCheck revalidate potentiellement instable
- **Severite :** High
- **Effort :** Quick Win
- **Priorite :** 9
- **Localisation :** `services/back-office/src/features/auth/hooks/useSessionCheck.ts:21-46`
- **Description :** `revalidate` est un `useCallback([setUser, logout])`. Si ces refs changeaient, un double appel API `/bff/auth/me` se declencherait, prolongeant le spinner de chargement.
- **Recommandation :** `useCallback(fn, [])` car setUser et logout sont stables Zustand.

#### [FND-016] Recherche SearchSource filtre client complet
- **Severite :** Medium
- **Effort :** Quick Win
- **Priorite :** 6
- **Localisation :** `services/back-office/src/pages/employees/index.tsx:67-82`
- **Description :** Filtre le tableau `employees` complet cote client a chaque recherche.
- **Recommandation :** Acceptable. Passer a une recherche API-side si le volume augmente.

#### [FND-017] Intl formatters instancies dans les fonctions cell
- **Severite :** Medium
- **Effort :** Quick Win
- **Priorite :** 6
- **Localisation :** `services/back-office/src/pages/programs/index.tsx:248-265`
- **Description :** `Intl.NumberFormat` et `Intl.DateTimeFormat` crees a chaque appel de cell (~0.5ms chacun). Pour 50 lignes : ~50ms bloques.
- **Recommandation :** Hoister les formatters en module-scope.

## Matrice de priorisation

| # | Finding | Severite | Effort | Priorite | Categorie |
|---|---------|----------|--------|----------|-----------|
| 1 | FND-004 console.log debug | Critical | Quick Win | 12 | React |
| 2 | FND-001 Google Fonts render-blocking | High | Quick Win | 9 | Assets |
| 3 | FND-005 sections recrees AppLayout | High | Quick Win | 9 | React |
| 4 | FND-007 searchSource recree | High | Quick Win | 9 | React |
| 5 | FND-015 useSessionCheck instable | High | Quick Win | 9 | Data Fetching |
| 6 | FND-002 CSP vs Google Fonts | Medium | Quick Win | 6 | Assets |
| 7 | FND-006 user inline AppLayout | Medium | Quick Win | 6 | React |
| 8 | FND-010 key={index} DashboardGrid | Medium | Quick Win | 6 | React |
| 9 | FND-014 useSSE deps instables | Medium | Quick Win | 6 | Data Fetching |
| 10 | FND-016 Recherche client | Medium | Quick Win | 6 | Data Fetching |
| 11 | FND-017 Intl formatters | Medium | Quick Win | 6 | React |
| 12 | FND-008 columns array | Medium | Medium | 4 | React |
| 13 | FND-009 SearchProvider context | Medium | Medium | 4 | React |
| 14 | FND-012 Icons SVG custom | Medium | Medium | 4 | Assets |
| 15 | FND-003 lucide tree-shaking | Low | Quick Win | 3 | Bundle |
| 16 | FND-011 onClick inline | Low | Quick Win | 3 | React |
| 17 | FND-013 backdrop-blur mobile | Low | Quick Win | 3 | Assets |

## Quick Wins (a faire immediatement)

1. **FND-004** Supprimer les console.log (AuthGuard, EmployeesPage, Modal)
2. **FND-001** Self-host les fonts via @fontsource/poppins
3. **FND-002** Corriger la CSP dans index.html
4. **FND-005** useMemo sur sections dans AppLayout
5. **FND-006** Memoiser userProps dans AppLayout
6. **FND-007** Memoiser searchSource dans EmployeesPage
7. **FND-015** Stabiliser revalidate dans useSessionCheck
8. **FND-017** Hoister les Intl formatters en module-scope

## Recommandations a moyen terme

1. **FND-008 + FND-009** Memoiser columns arrays et valeur SearchProvider context
2. **FND-012** Remplacer composants SVG custom par lucide-react

## Refactorings structurels

Aucun refactoring lourd necessaire. A surveiller :
- SearchProvider Context -> Zustand si d'autres consumers sont ajoutes
- DataTable -> @tanstack/react-virtual si les tableaux depassent ~100 lignes

## Metriques a surveiller

- Core Web Vitals : LCP < 2.5s, INP < 200ms, CLS < 0.1
- Navigation timing : temps entre clic sidebar et premier paint de la page cible
- Bundle size : dist/ parsed + gzip
- Re-render count : React DevTools Profiler sur Sidebar/TopBar

## Outils recommandes

| Outil | Usage | Commande |
|---|---|---|
| React DevTools Profiler | Confirmer re-renders Sidebar/TopBar | Extension Chrome > Profiler |
| vite-bundle-visualizer | Tree-shaking lucide-react | `npx vite-bundle-visualizer` |
| Lighthouse CLI | FCP, LCP, TBT, CLS | `npx lighthouse http://localhost:3100 --output=html` |
| why-did-you-render | Re-renders evitables | `npm i @welldone-software/why-did-you-render` |
| web-vitals | RUM staging | `npm i web-vitals` |

## Plan de validation

1. **React DevTools Profiler** -> Re-renders Sidebar/TopBar pendant navigation -> Objectif : 0 si props inchangees
2. **Supprimer console.log** -> Mesurer INP -> Objectif : < 150ms
3. **Self-host fonts** -> FCP Lighthouse -> Objectif : < 1.5s (4G simule)
4. **vite-bundle-visualizer** -> Taille lucide-react -> Objectif : < 30KB gzip
5. **Apres quick wins** -> Lighthouse global -> Objectif : Performance score > 85
