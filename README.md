# README - Skills locaux

Ce document couvre les skills presents **en dur** dans ce dossier, c'est-a-dire les dossiers qui contiennent un `SKILL.md`.

Au `2026-06-10`, cela represente **83 skills locaux**.

## Scope

Inclus :

- `adapt`
- `adr-writer`
- `anamnese-dentaire`
- `animate`
- `apartment-finder`
- `apply`
- `architecture-conceptor`
- `audit`
- `blog-writer`
- `bolder`
- `brief-writer`
- `cdc-builder`
- `ceo-challenger`
- `change-advisor`
- `clarify`
- `claude-md-architect`
- `colorize`
- `comptabilite`
- `conseiller-juridique`
- `contract-forge`
- `critique`
- `delight`
- `design-prompt-generator`
- `discord-server-architect`
- `distill`
- `docker-dokploy-expert`
- `documentor`
- `extract`
- `falco-rule-architect`
- `figma`
- `figma-implement-design`
- `friction-auditor`
- `frontend-design`
- `game-server-product-orchestrator`
- `generate-business-model`
- `github-assistant`
- `harden`
- `linear-project-manager`
- `llm-lab`
- `meeting-prep`
- `mobile-responsive`
- `normalize`
- `notion-knowledge-capture`
- `notion-meeting-intelligence`
- `notion-organizer`
- `notion-research-documentation`
- `notion-spec-to-implementation`
- `obsidian-memory`
- `onboard`
- `optimize`
- `pca-pra-builder`
- `pentest-audit`
- `perf-analyzer`
- `polish`
- `postgres-expert`
- `product-advisor`
- `progress-report`
- `project-launcher`
- `prospector`
- `quieter`
- `research-brief`
- `reparation-electronique`
- `sales-writer`
- `selinux-expert`
- `senior-dev`
- `skill-creator`
- `sonar-expert`
- `sprint-review`
- `srs-writer`
- `standard-maker`
- `sysadmin-expert`
- `teach-impeccable`
- `tenere-mechanic`
- `test-writer`
- `twitter-wakr`
- `vulgarize`
- `wakr-ansible-infra`
- `wakr-business-plan-maker`
- `wakr-deploy`
- `wakr-pdf-generator`
- `wakr-process`
- `wakr-seo-report-maker`
- `wakr-slide-generator`

Exclus :

- les skills systeme Codex dans `~/.codex/skills/.system`
- les dossiers sans `SKILL.md` standard, comme `youtube-analyzer` qui contient `skill.md`

Commande pour regenerer l'inventaire :

```sh
for d in *; do
  if [ -d "$d" ] && [ ! -L "$d" ] && [ -f "$d/SKILL.md" ]; then
    printf '%s\n' "$d"
  fi
done | sort
```

## Regle simple pour bien utiliser un skill

Un skill donne de bons resultats quand la demande contient 5 choses :

1. **L'objectif** : ce que tu veux obtenir, pas juste le sujet.
2. **Le contexte** : projet, audience, stack, pays, contraintes, deadline.
3. **Les inputs** : URL, fichier, repo, extrait, chiffres, capture, brief.
4. **Le format de sortie** : memo, tableau, decision, spec, PDF, slides, checklist.
5. **Le critere de succes** : comparer, prioriser, decider, corriger, livrer.

Template de prompt utile :

```text
Utilise $skill pour [objectif].
Contexte : [projet / audience / stack / zone geographique].
Inputs : [fichiers / liens / contraintes].
Sortie attendue : [format].
Definition de fini : [decision, rapport, code, plan, etc.].
```

## Regles d'efficacite transverses

- Donne la **decision a prendre** quand tu demandes une analyse.
- Donne la **sortie exacte** quand tu demandes un livrable.
- Donne la **profondeur** attendue : rapide, standard, deep.
- Donne les **contraintes reelles** : budget, delai, techno imposee, pays, taille d'equipe.
- Donne les **artefacts bruts** plutot qu'un resume si tu les as.
- Enchaine les skills quand le workflow l'exige au lieu de demander un skill trop large.

## Comment utiliser `wakr-process`

`wakr-process` n'est pas un skill "plus intelligent" que les autres. C'est un
**chef d'orchestre** pour les taches complexes qui demandent plusieurs skills,
plusieurs etapes, ou plusieurs sous-problemes a coordonner.

### Quand l'utiliser

Utilise `wakr-process` quand la demande ressemble a :

- une tache **cross-service** : front + back + DB + tests
- un chantier avec **plusieurs livrables** : analyse, implementation, verification, restitution
- une execution qui combine **recherche + decision + code + synthese**
- un besoin de **decomposition explicite** avant d'agir
- une mission ou tu veux que plusieurs skills soient **routes proprement** sans tout faire a la main

Exemples typiques :

- `Utilise $wakr-process pour decomposer et executer l'ajout d'un module de facturation sur le front, le back et la base.`
- `Utilise $wakr-process pour orchestrer un audit perf puis appliquer les quick wins les plus surs.`
- `Utilise $wakr-process pour gerer ce chantier multi-skills et me livrer une synthese finale.`

### Quand ne pas l'utiliser

Ne l'utilise pas pour :

- une tache simple mono-skill
- une simple question de knowledge
- une modification locale evidente dans un seul fichier
- un besoin ou tu sais deja exactement quel skill appeler directement

Dans ces cas-la, appelle le skill cible sans orchestration.

### Le bon format de prompt

Pour qu'il fonctionne bien, donne-lui :

1. **L'objectif final** : ce qui doit etre vraiment livre.
2. **Le perimetre** : services, repo, dossiers, environnement.
3. **Les contraintes** : delai, risque acceptable, tests, budget, profondeur.
4. **Les sorties attendues** : code, rapport, plan, PDF, synthese, checklist.
5. **Les garde-fous** : "pas de challenge", "pas de PDF", "pas de tests" si necessaire.

Template utile :

```text
Utilise $wakr-process pour [objectif complexe].
Perimetre : [services / repo / fichiers / environnement].
Contraintes : [deadline / risque / profondeur / tests / budget].
Livrables attendus : [code / rapport / synthese / PDF].
Definition de fini : [ce qui doit etre termine a la fin].
```

Exemple concret :

```text
Utilise $wakr-process pour ajouter un module kiosks.
Perimetre : backend Node, frontend React, schema Postgres, tests.
Contraintes : pas de regression auth, tests obligatoires, profondeur standard.
Livrables attendus : code, tests, synthese finale.
Definition de fini : le module est implemente, verifie et resume proprement.
```

### Ce qu'il fait concretement

Quand tu l'appelles bien, `wakr-process` suit cette logique :

1. **Charge le contexte** : memoire, learnings, standards, catalogue de skills, projet courant.
2. **Decompose la tache** en sous-taches claires avec priorites et dependances.
3. **Attribue un skill par sous-tache** au lieu de melanger tous les skills partout.
4. **Te montre la decomposition** avant execution.
5. **Lance ou execute** chaque sous-tache selon le bon mode.
6. **Coordonne les resultats** puis produit une synthese consolidee.
7. **Optionnellement** genere un PDF de restitution via `wakr-pdf-generator`.

La sortie attendue n'est donc pas juste "du code". C'est souvent :

- un tableau de decomposition
- des sous-taches routees vers les bons skills
- des executions paralleles ou sequentielles selon le cas
- une synthese finale exploitable

### Comment il fonctionne en interne

Le point cle est qu'il distingue **2 modes d'execution**.

**Mode Agent**

Ce mode sert aux taches independantes qui lisent, analysent, auditent ou
produisent un artefact sans muter directement le codebase.

Cas typiques :

- recherche avec `documentor`
- audit avec `perf-analyzer` ou `pentest-audit`
- generation de PDF
- revue ou synthese autonome

Dans ce mode, `wakr-process` peut lancer plusieurs agents en parallele tant
qu'il n'y a pas de dependances fortes.

**Mode Directive**

Ce mode sert aux taches qui modifient reellement le code ou dependent du
contexte deja accumule dans l'execution principale.

Cas typiques :

- implementation
- refactoring
- edition de fichiers
- verification sequentielle

Dans ce mode, le process ne "pretend" pas utiliser un skill. Il doit suivre
un protocole visible :

1. lire le `SKILL.md` du skill cible
2. afficher les directives retenues
3. executer en appliquant ces directives
4. ecrire les tests via `test-writer` apres toute vraie ecriture de code, sauf exception explicite

Autrement dit, `wakr-process` ne remplace pas les skills. Il les **charge et
les applique methodiquement**.

### Le challenge produit

Par defaut, `wakr-process` peut lancer `product-advisor` avant execution pour
challenger la demande et detecter :

- les impacts directs
- les impacts indirects
- les dependances oubliees
- les risques produit
- les enrichissements a faible effort

Ce challenge est surtout utile quand la tache touche :

- plusieurs services
- un schema de base de donnees
- l'authentification ou l'autorisation

Tu peux le skipper si tu veux aller droit au but sur une tache purement
technique mono-service, ou si tu precises explicitement `pas de challenge`.

### Le modele de coordination

Le fonctionnement normal ressemble a ca :

1. des sous-taches d'exploration ou d'analyse partent en **parallele**
2. leurs resultats reviennent dans le contexte principal
3. les sous-taches de code passent en **sequence**
4. les tests sont ecrits et verifies apres les blocs de code importants
5. une synthese finale consolide le tout

Donc `wakr-process` est particulierement bon quand il faut faire :

- explorer puis implementer
- analyser puis prioriser puis executer
- faire travailler plusieurs skills sans perdre la coherence d'ensemble

### Ce qu'il ne faut pas attendre de lui

`wakr-process` a des limites claires :

- il ne rend pas un mauvais skill miraculeusement bon
- il n'est pas fait pour remplacer un appel direct a `senior-dev`, `documentor` ou `apply` sur une tache simple
- il plafonne en pratique autour de **6 sous-taches/agents simultanes**
- il depend de la qualite des sorties des skills sous-jacents

En bref :

- si tu veux **orchestrer**, utilise `wakr-process`
- si tu veux **faire une seule chose clairement definie**, appelle le skill specialise

### Raccourcis de prompts utiles

- `Utilise $wakr-process pour decomposer cette demande en sous-taches puis executer seulement les P0.`
- `Utilise $wakr-process pour orchestrer ce chantier, avec challenge produit avant execution.`
- `Utilise $wakr-process pour gerer cette tache cross-service sans PDF final.`
- `Utilise $wakr-process pour coordonner les skills necessaires puis me livrer une synthese actionnable.`

## Chaines de skills qui marchent bien

- `documentor -> brief-writer` : recherche sourcee puis livrable client.
- `research-brief` : version compacte du chainage ci-dessus en une seule demande.
- `product-advisor -> generate-business-model` : clarifier la valeur produit puis choisir un modele de monetisation.
- `architecture-conceptor -> adr-writer` : arbitrer les options puis figer la decision dans un ADR.
- `senior-dev -> apply -> change-advisor` : decision technique, execution, verification pre-deploiement.
- `contract-forge -> test-writer` : poser les contrats partages puis verrouiller les parcours critiques.
- `prospector -> sales-writer` : trouver des leads puis rediger l'outreach.
- `documentor -> generate-business-model -> wakr-pdf-generator` : recherche, modele economique, export client.
- `meeting-prep -> wakr-slide-generator` : cadrage de reunion puis deck.
- `sprint-review -> apply` : bilan du recent travail puis passage a l'execution.
- `progress-report -> wakr-pdf-generator` : rapport d'avancement puis export PDF client.

## Catalogue

### Recherche, synthese, livrables

| Skill | Cas d'usage | Prompt efficace | Pour etre efficace |
| --- | --- | --- | --- |
| `documentor` | Recherche sourcee, benchmark, veille, comparaison | `Utilise $documentor pour comparer 5 outils de monitoring Node en Europe, sources primaires si possible, avec recommandation finale.` | Preciser periode, geographie, criteres de comparaison, niveau de profondeur et format de sortie. |
| `brief-writer` | Transformer un rapport de recherche en livrable client | `Utilise $brief-writer pour transformer ce rapport en brief client decideur de 1 page avec recommandations.` | Fournir le rapport source et l'audience cible. Sans audience, le rendu sera moins net. |
| `research-brief` | Faire recherche + brief client en une seule demande | `Utilise $research-brief pour produire un brief client technique sur l'etat du RAG open source en 2026.` | Dire tout de suite l'audience, sinon tu perds un aller-retour. |
| `meeting-prep` | Preparer un call, workshop, steering, comite | `Utilise $meeting-prep pour preparer un steering client de 45 min dont l'objectif est de faire valider la roadmap.` | Donner l'objectif de decision, les participants, le niveau de tension et les risques politiques. |
| `blog-writer` | Article technique en FR, ton maker, contenu publiable | `Utilise $blog-writer pour ecrire un article sur les agents MCP en partant de ces notes.` | Fournir angle, audience, these, exemples concrets et ce qui doit etre assume ou evite. |
| `youtube-analyzer` | Transcription et synthese de video YouTube | `Utilise $youtube-analyzer pour resumer cette video en 10 points actionnables et extraire les citations utiles.` | Donner l'URL, l'objectif de lecture et le format de sortie attendu. |
| `progress-report` | Generer un rapport d'avancement client et/ou technique | `Utilise $progress-report pour produire le rapport d'avancement de cette semaine pour le client et l'equipe.` | Donner la periode, le repo/projet, l'audience et si tu veux la version client, technique ou les deux. |
| `wakr-pdf-generator` | Export PDF brande Wakr d'un rapport deja structure | `Utilise $wakr-pdf-generator pour transformer ce rapport final en PDF client.` | Ne pas lui demander de faire la recherche ou la redaction de fond. Lui donner un contenu deja propre. |
| `wakr-slide-generator` | Creer un deck PDF brande Wakr | `Utilise $wakr-slide-generator pour generer un deck 16:9 de 8 slides pour ce kickoff client.` | Donner l'histoire a raconter, le public, le nombre de slides et la conclusion a faire passer. |
| `notion-organizer` | Ranger, structurer, exporter dans Notion | `Utilise $notion-organizer pour classer ce brief et ce rapport dans le workspace client X.` | Dire ou le contenu doit vivre si tu le sais deja. Sinon fournir le contexte client/projet. |

### Strategie, business, vente

| Skill | Cas d'usage | Prompt efficace | Pour etre efficace |
| --- | --- | --- | --- |
| `ceo-challenger` | Challenger une roadmap, une feature, un pivot | `Utilise $ceo-challenger pour challenger l'idee d'ajouter un module analytics a notre produit.` | Lui demander un verdict, pas un brainstorm sans fin. Donner cout, pari et opportunite alternative. |
| `product-advisor` | Structurer un produit, trouver les bonnes features et prioriser | `Utilise $product-advisor pour me dire quelles features construire ensuite sur cette app SaaS.` | Donner le job utilisateur, la cible, les contraintes, la traction actuelle et la decision a prendre. |
| `generate-business-model` | Construire ou comparer un modele economique | `Utilise $generate-business-model pour proposer 3 modeles de monetisation pour cette app B2B.` | Fournir produit, cible, geographie, traction, canal d'acquisition et contraintes de pricing. |
| `prospector` | Trouver des prospects via Google Maps et leurs sites | `Utilise $prospector pour trouver 20 agences immobilieres parisiennes avec un site faible.` | Donner niche, ville, volume de leads et type de faiblesse recherchee. |
| `sales-writer` | Cold email, relance, pitch, reponse a objection | `Utilise $sales-writer pour rediger un email de prospection a partir de cette fiche prospect.` | Donner ICP, contexte du lead, angle d'attaque, CTA et ton voulu. |
| `sprint-review` | Faire un bilan d'avancement et prioriser la suite | `Utilise $sprint-review pour analyser les 2 dernieres semaines du projet et proposer les prochaines priorites.` | Donner repo, PR, periode, objectifs du sprint et audience du rapport. |
| `design-prompt-generator` | Produire un prompt detaille pour un outil de generation UI | `Utilise $design-prompt-generator pour generer un prompt de landing page fintech premium.` | Dire la cible, la vibe, les sections, les references visuelles et les contraintes du framework. |
| `twitter-wakr` | Draft, reponses, veille et analyse X/Twitter pour Wakr | `Utilise $twitter-wakr pour preparer 5 posts sur les agents IA cette semaine.` | Fournir angle editorial, objectif, sujets interdits et si c'est du draft ou de la publication. |

### Engineering, architecture, qualite

| Skill | Cas d'usage | Prompt efficace | Pour etre efficace |
| --- | --- | --- | --- |
| `senior-dev` | Decision technique a enjeu, options, rollout, review | `Utilise $senior-dev pour choisir entre queue Redis et cron simple pour ce workflow.` | Donner volume, SLA, contraintes operatoires, risques acceptables et criteres de choix. |
| `architecture-conceptor` | Concevoir une architecture ou rediger un ADR | `Utilise $architecture-conceptor pour proposer l'architecture d'un backend multi-tenant.` | Demander explicitement les options comparees, les trade-offs et la recommandation. |
| `adr-writer` | Rediger un ADR propre, traceable et compatible avec le repo | `Utilise $adr-writer pour documenter la decision de passer au BFF en ADR.` | Donner la decision, le contexte, les alternatives considerees et le dossier ADR du projet s'il existe deja. |
| `apply` | Transformer un rapport/ADR/brief en execution concrete | `Utilise $apply pour implementer les decisions de ce rapport senior-dev.` | Lui donner un livrable source clair. C'est un skill d'execution, pas de cadrage initial. |
| `change-advisor` | Evaluer si un changement est safe avant merge/deploiement | `Utilise $change-advisor pour evaluer le risque de ce deploy en production.` | Donner nature du changement, surface d'impact, rollback possible, monitoring disponible et fenetre de tir. |
| `contract-forge` | Synchroniser les contrats API et eliminer la duplication de types | `Utilise $contract-forge pour mettre en place des shared contracts entre le front et le back.` | Donner la stack TypeScript, l'architecture du repo, les schemas existants et si tu veux du client genere ou aussi des hooks. |
| `github-assistant` | Explorer un repo GitHub, lister issues/PRs et faire de la review | `Utilise $github-assistant pour analyser ce repo GitHub et lister les PRs ouvertes.` | Donner le repo `owner/name` ou dire clairement que tu parles de tes repos GitHub. |
| `skill-creator` | Creer ou ameliorer un skill/agent | `Utilise $skill-creator pour creer un skill qui audite des briefs commerciaux.` | Preciser le comportement attendu, les triggers, les exemples et la mesure de qualite. |
| `reparation-electronique` | Diagnostiquer cartes PCB, composants et pannes d'electronique de puissance | `Utilise $reparation-electronique pour analyser cette carte de deshumidificateur : bip au branchement, pas d'affichage.` | Fournir photos recto/verso, symptome exact, reference PCB, marquages composants et mesures deja faites. |
| `srs-writer` | Produire un vrai document de requirements | `Utilise $srs-writer pour rediger un SRS de cette fonctionnalite de paiement.` | Donner perimetre, audience, contraintes non fonctionnelles, exclusions et priorites. |
| `standard-maker` | Ecrire ou auditer un standard engineering | `Utilise $standard-maker pour definir un standard de review PR pour l'equipe.` | Demander des regles testables, pas des principes vagues. Donner contexte d'equipe et niveau d'enforcement. |
| `test-writer` | Ajouter des tests unitaires/integration TypeScript/React | `Utilise $test-writer pour ajouter des tests sur ce formulaire React.` | Donner le comportement critique a couvrir et la stack de test existante. |
| `vulgarize` | Expliquer clairement un concept technique | `Utilise $vulgarize pour m'expliquer la difference entre CQRS et event sourcing.` | Dire le niveau cible, ce qui n'est pas compris et si tu veux analogies, schema ou comparaison. |
| `wakr-process` | Orchestrer une tache complexe multi-skills avec delegation et synthese | `Utilise $wakr-process pour decomposer ce chantier cross-service et coordonner les skills necessaires.` | A reserver aux taches complexes avec plusieurs sous-taches ou plusieurs skills. Donner l'objectif final, les contraintes et ce qui doit etre livre. |

### Produit, frontend, perf, securite, infra

| Skill | Cas d'usage | Prompt efficace | Pour etre efficace |
| --- | --- | --- | --- |
| `mobile-responsive` | Adapter un composant React existant au mobile | `Utilise $mobile-responsive pour corriger ce wizard desktop-first sur smartphone.` | Pointer le composant, les breakpoints problematiques et les interactions tactiles critiques. |
| `perf-analyzer` | Audit de performance front/back et recommandations priorisees | `Utilise $perf-analyzer pour analyser les lenteurs de cette app Next.js + API Node.` | Donner metriques, symptomes, pages lentes, screenshots Lighthouse ou traces si tu les as. |
| `pentest-audit` | Audit securite d'une app, API ou infra applicative | `Utilise $pentest-audit pour auditer cette API interne et produire un rapport de risques.` | Cadrer le perimetre autorise, l'environnement et le niveau de profondeur attendu. |
| `docker-dokploy-expert` | Dockerfile, compose, Dokploy, reverse proxy, deploy VPS | `Utilise $docker-dokploy-expert pour fiabiliser ce deploy multi-services sur Dokploy.` | Donner architecture cible, services, volumes, domaines, reverse proxy et contraintes de zero-downtime. |
| `postgres-expert` | Migrations, modelisation, perf SQL, backup/restore, infra Postgres | `Utilise $postgres-expert pour optimiser cette requete lente et proposer les index utiles.` | Donner schema, requetes reelles, plan `EXPLAIN` si possible et contexte de charge. |
| `llm-lab` | Infra LLM multi-modeles, evals, routing, observabilite | `Utilise $llm-lab pour ajouter un nouveau modele local au lab et le comparer a GPT.` | Dire l'objectif exact : cout, latence, qualite, portabilite de skill ou pipeline autonome. |

### Ops internes, legal, finance, vie perso

| Skill | Cas d'usage | Prompt efficace | Pour etre efficace |
| --- | --- | --- | --- |
| `comptabilite` | Analyser des releves, KPI, cash, categories de depenses | `Utilise $comptabilite pour analyser ce CSV bancaire et sortir les KPI du mois.` | Fournir les exports bruts, la periode, le type d'entite et la question de gestion a trancher. |
| `conseiller-juridique` | Orientation juridique/fiscale pour structure FR | `Utilise $conseiller-juridique pour comparer dividendes vs salaire en SASU.` | Donner la forme juridique, le pays, les montants et l'objectif de decision. |
| `apartment-finder` | Recherche locative FR/NL avec scoring | `Utilise $apartment-finder pour trouver un T2 a Paris 11e sous 1800 euros.` | Donner budget max reel, quartiers, dealbreakers, must-haves et horizon de demenagement. |

## Quand ne pas utiliser le mauvais skill

- Ne demande pas a `brief-writer` de faire la recherche : utilise `documentor` d'abord.
- Ne demande pas a `sales-writer` de trouver des prospects : utilise `prospector`.
- Ne demande pas a `apply` de choisir une architecture : utilise `senior-dev` ou `architecture-conceptor`.
- Ne demande pas a `adr-writer` de comparer des options : utilise `architecture-conceptor` d'abord.
- Ne demande pas a `wakr-pdf-generator` de produire le fond du document : donne-lui un contenu deja stabilise.
- Ne demande pas a `conseiller-juridique` de faire du rapprochement bancaire : utilise `comptabilite`.
- Ne demande pas a `github-assistant` de modifier ton code local : il sert a interagir avec GitHub.
- Ne demande pas a `wakr-process` d'orchestrer une tache simple mono-skill : appelle directement le skill cible.
- Ne demande pas a `vulgarize` de prendre une decision d'architecture : utilise `senior-dev`.

## Raccourci de choix

Si tu hesites entre plusieurs skills, pars de la sortie que tu veux :

- **Je veux savoir** -> `documentor`
- **Je veux cadrer le produit** -> `product-advisor`
- **Je veux expliquer** -> `vulgarize`
- **Je veux decider** -> `senior-dev` ou `ceo-challenger`
- **Je veux documenter une decision** -> `adr-writer`
- **Je veux formaliser** -> `srs-writer` ou `standard-maker`
- **Je veux synchroniser mes contrats/types** -> `contract-forge`
- **Je veux executer** -> `apply`
- **Je veux piloter une grosse tache multi-skills** -> `wakr-process`
- **Je veux verifier avant prod** -> `change-advisor`
- **Je veux explorer GitHub** -> `github-assistant`
- **Je veux faire un point d'avancement** -> `progress-report`
- **Je veux livrer au client** -> `brief-writer`, `wakr-pdf-generator`, `wakr-slide-generator`
- **Je veux vendre** -> `prospector`, `sales-writer`, `twitter-wakr`

## Note pratique

Le meilleur levier n'est pas de "mieux prompter" abstraitement. Le meilleur levier est de donner :

- le bon skill
- le bon input brut
- la bonne audience
- la bonne definition de fini

Si ces 4 points sont clairs, la plupart des skills du dossier deviennent predictibles et tres efficaces.
