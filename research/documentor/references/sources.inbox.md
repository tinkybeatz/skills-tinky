# DOCUMENTOR — Sources Inbox

A buffer file populated automatically after every DOCUMENTOR session.
**Do not edit manually** — this file is managed by the skill.

Review it periodically (weekly recommended) and migrate the validated entries
to `source.md`, then empty this file.

---

## How to run the review

For each entry:

- ✅ Validate → copy into the right section of `source.md`, delete here
- ❌ Reject → delete without migrating
- 🔁 Defer → leave in place for the next review

For proposed new categories (🆕):

- If you validate the category → create the section in `source.md` and migrate the sources
- If you reject it → reclassify the sources into an existing category or delete them

---

## Entries awaiting validation

### 🆕 Motorcycle travel / off-road / trail
> Rationale: new domain — specialized adventure/trail motorcycling sources, GPX, trail regulations. Fits neither AI/tech nor EU regulation.

| Title | URL | Date discovered | Score /100 | Justification |
|---|---|---|---|---|
| Trans Euro Trail France (official) | https://transeurotrail.org/france/ | 2026-04-26 | 85 | Primary GPX trail source for Europe, updated April 2026 |
| Adventure Country Tracks (official) | https://adventurecountrytracks.com/ | 2026-04-26 | 85 | Primary ACT source, member GPX trails |
| Codever — motorized trail rights | https://www.codever.fr/ | 2026-04-26 | 80 | Reference association for motorized green-lane recreation (FR) |
| Carrant.org — TET field reports | https://carrant.org/category/road-trip/rallyes-autres/trans-euro-trail/ | 2026-04-26 | 72 | Experienced rider blog, TET reports section by section |

### 🔍 To classify
| Title | URL | Date discovered | Score /100 | Presumed domain |
|---|---|---|---|---|
| GearJunkie — Triumph Scrambler 400X review | https://gearjunkie.com/motors/all-terrain-vehicle/triumph-scrambler-400-x-review | 2026-04-26 | 78 | US off-road motorcycle press |
| Sénat — motorized traffic on rural paths | https://www.senat.fr/questions/base/2000/qSEQ001128905.html | 2026-04-26 | 88 | FR regulation — rural paths |
| Trail Adventure Magazine | https://trailadventuremag.fr/ | 2026-04-26 | 72 | Specialized FR motorcycle-travel press |

<!-- New sources will be appended here automatically by the skill -->
<!-- Existing-category format: -->
<!--
### [Existing category name]
| Title | URL | Date discovered | Score /100 | Justification |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

<!-- Proposed new-category format: -->
<!--
### 🆕 [Proposed category name]
> Rationale: [why this category doesn't fit the existing ones]
| Title | URL | Date discovered | Score /100 | Justification |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

<!-- Orphan sources (single domain, no confirmed category yet): -->
<!--
### 🔍 To classify
| Title | URL | Date discovered | Score /100 | Presumed domain |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

### 🆕 Mobile UX, Accessibility & Responsive Design

> Rationale: A cross-cutting domain (touch ergonomics, mobile accessibility, animation, responsive typography) absent from the current base. 10+ Tier 1-2 sources identified in this session.

| Title                                           | URL                                                                                | Date discovered | Score /100 | Justification                                             |
| ----------------------------------------------- | ---------------------------------------------------------------------------------- | --------------- | ---------- | --------------------------------------------------------- |
| NNg — Hamburger Menus and Hidden Navigation     | nngroup.com/articles/hamburger-menus/                                              | 2026-04-17      | 88         | Study of 179 participants, primary discoverability data   |
| NNg — Bottom Sheets UX Guidelines               | nngroup.com/articles/bottom-sheet/                                                 | 2026-04-17      | 85         | Primary guidelines for the bottom-sheet pattern           |
| NNg — Scrolling and Attention (eye-tracking)    | nngroup.com/articles/scrolling-and-attention/                                      | 2026-04-17      | 90         | Eye-tracking 57,453 fixations, primary data               |
| NNg — Touch Target Size                         | nngroup.com/articles/touch-target-size/                                            | 2026-04-17      | 87         | Research-based touch-target recommendations               |
| Smashing Magazine — Accessible Tap Target Sizes | smashingmagazine.com/2023/04/accessible-tap-target-sizes-rage-taps-clicks/         | 2026-04-17      | 82         | Cheatsheet of sizes by screen zone (Hoober data)          |
| Smashing Magazine — The Thumb Zone              | smashingmagazine.com/2016/09/the-thumb-zone-designing-for-mobile-users/            | 2026-04-17      | 85         | Synthesis of Hoober's 1,333 observations                  |
| React Aria — Interactions                       | react-spectrum.adobe.com/react-aria/interactions.html                              | 2026-04-17      | 90         | Accessible hooks usePress/useLongPress/useHover           |
| FullStory — Consumer Mobile Frustration 2025    | fullstory.com/consumer-mobile-frustration-is-rising-and-its-costing-brands/        | 2026-04-17      | 85         | 14B sessions analyzed, rage/dead/error clicks             |
| Think with Google — Page Load Time Statistics   | thinkwithgoogle.com/marketing-strategies/app-and-mobile/page-load-time-statistics/ | 2026-04-17      | 88         | Deep neural network bounce/conversion, 53% abandon >3s    |
| Baymard Institute — Cart Abandonment Rate       | baymard.com/lists/cart-abandonment-rate                                            | 2026-04-17      | 90         | Meta-analysis of 49 studies, mobile/desktop abandon rates |
| Baymard Institute — Line Length Readability     | baymard.com/blog/line-length-readability                                           | 2026-04-17      | 85         | Large-scale research on CPL and readability               |
| web.dev — Rendering Performance                 | web.dev/articles/rendering-performance                                             | 2026-04-17      | 92         | Canonical reference for the CSS render pipeline (Paul Lewis) |
| web.dev — prefers-reduced-motion                | web.dev/articles/prefers-reduced-motion                                            | 2026-04-17      | 85         | Reduced-motion implementation patterns                    |
| Vaul — Drawer Component                         | vaul.emilkowal.ski/                                                                | 2026-04-17      | 80         | Unstyled drawer on Radix, used by Linear/Vercel           |
| Utopia — Fluid Type Scale Calculator            | utopia.fyi/type/calculator/                                                        | 2026-04-17      | 78         | clamp() calculation tool for fluid typography             |

### 🆕 LLM Infrastructure & Inference

> Rationale: A new domain covering inference engines, multi-model gateways, and LLM orchestration — fits neither "AI & tech" (research/models) nor "DevOps" (classic infra)
> | Title | URL | Date discovered | Score /100 | Justification |
> |---|---|---|---|---|
> | LiteLLM — Official documentation | https://docs.litellm.ai/ | 2026-04-21 | 92 | Reference LLM gateway, 100+ providers, OSS, primary docs |
> | LeetLLM — Inference Engine Comparison 2026 | https://leetllm.com/blog/llm-inference-engine-comparison-2026 | 2026-04-21 | 85 | Independent benchmarks vLLM/SGLang/TensorRT/Ollama with concrete figures |
> | RelayPlane — LLM Gateway Comparison 2026 | https://relayplane.com/blog/llm-gateway-comparison-2026 | 2026-04-21 | 78 | Structured comparison of LLM gateways, self-published but factual |

### 🆕 LLM Evaluation & Testing

> Rationale: A specific domain of automated LLM and AI-pipeline evaluation in CI/CD — distinct from "Information Retrieval & source evaluation", which concerns evaluating the credibility of web sources
> | Title | URL | Date discovered | Score /100 | Justification |
> |---|---|---|---|---|
> | DeepEval — GitHub | https://github.com/confident-ai/deepeval | 2026-04-21 | 88 | Reference LLM eval framework, 50+ metrics, OSS, pytest-native |
> | Braintrust — AI Evals for CI/CD | https://www.braintrust.dev/articles/best-ai-evals-tools-cicd-2025 | 2026-04-21 | 75 | Detailed comparison of eval tools in CI/CD with concrete examples |

### Artificial intelligence & tech

| Title                                        | URL                                                                                    | Date discovered | Score /100 | Justification                                                            |
| -------------------------------------------- | -------------------------------------------------------------------------------------- | --------------- | ---------- | ------------------------------------------------------------------------ |
| o-mega.ai — Agent Frameworks Comparison 2026 | https://o-mega.ai/articles/langgraph-vs-crewai-vs-autogen-top-10-agent-frameworks-2026 | 2026-04-21      | 80         | Exhaustive comparison of the top 10 agent frameworks with a decision matrix |
| Red Hat — Building AI agents with MCP        | https://developers.redhat.com/articles/2026/01/08/building-effective-ai-agents-mcp     | 2026-04-21      | 82         | MCP + agents guide by Red Hat, secondary expert source                   |

### 🆕 AI Agent Tooling & Standards

> Rationale: A specific domain covering instruction standards for AI agents (AGENTS.md, Agent Skills), cross-tool configuration, and prompt-engineering patterns for agents — distinct from "AI & tech" (research/models) and "DevOps" (infra)
> | Title | URL | Date discovered | Score /100 | Justification |
> |---|---|---|---|---|
> | Anthropic — Equipping Agents with Agent Skills | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | 2026-04-21 | 92 | Anthropic engineering blog, design rationale of progressive disclosure |
> | Tessl — AGENTS.md Open Standard | https://tessl.io/blog/the-rise-of-agents-md-an-open-standard-and-single-source-of-truth-for-ai-coding-agents/ | 2026-04-21 | 75 | Historical context of the open AGENTS.md standard, Linux Foundation |
| AGENTS.md — official specification (Linux Foundation) | https://agents.md/ | 2026-04-30 | 95 | Official open standard, Agentic AI Foundation governance, 60k+ adopting repos |
| ETH Zurich — AGENTbench empirical study | https://arxiv.org/html/2601.20404v1 | 2026-04-30 | 92 | Empirical study of 138 Python tasks, 4 agents: LLM-gen -3% / human +4% |
| Empirical study — 2303 agent context files | https://arxiv.org/html/2511.12884v1 | 2026-04-30 | 92 | Analysis of 1925 repos, classification into 16 categories, security/perf gap |
| InfoQ — Reassessing AGENTS.md value | https://www.infoq.com/news/2026/03/agents-context-file-value-review/ | 2026-04-30 | 85 | Tech-press synthesis of the ETH study with expert perspectives |
| DeepLearning.ai — Cutting through OpenClaw hype | https://www.deeplearning.ai/the-batch/cutting-through-the-openclaw-and-moltbook-hype/ | 2026-04-30 | 88 | Critical analysis by Andrew Ng's team, OpenClaw/SOUL.md security |
| GitHub aaronjmars/soul.md | https://github.com/aaronjmars/soul.md | 2026-04-30 | 82 | Primary source of the SOUL.md concept (creator), 399 stars |

### Artificial intelligence & tech

| Title                                      | URL                                                  | Date discovered | Score /100 | Justification                                             |
| ------------------------------------------ | ---------------------------------------------------- | --------------- | ---------- | --------------------------------------------------------- |
| Simon Willison — Claude Skills are Awesome | https://simonwillison.net/2025/Oct/16/claude-skills/ | 2026-04-21      | 75         | Advanced-user perspective on Claude Code skills           |

### 🔍 To classify

| Title                                  | URL                                                                       | Date discovered | Score /100 | Presumed domain                                                        |
| -------------------------------------- | ------------------------------------------------------------------------- | --------------- | ---------- | ---------------------------------------------------------------------- |
| Confident AI — LLM Observability Tools | https://www.confident-ai.com/knowledge-base/top-7-llm-observability-tools | 2026-04-21      | 76         | LLM Observability (overlap with DevOps/SRE or a new LLM Infra category) |

### 🆕 PostgreSQL & databases

> Rationale: New domain — specialized PostgreSQL sources (official docs, internals MVCC/VACUUM, tuning, HA, monitoring). Fits neither "DevOps/SRE" (too broad) nor "AI/tech". 20+ Tier 1-3 sources identified in this research session.

| Title | URL | Date discovered | Score /100 | Justification |
|---|---|---|---|---|
| PostgreSQL Official Docs (v16/v17) | https://www.postgresql.org/docs/17/ | 2026-04-27 | 98 | Absolute source of truth — chapters Indexes, MVCC, Routine Vacuuming, Storage, runtime-config-* |
| PostgreSQL Release Notes | https://www.postgresql.org/docs/release/ | 2026-04-27 | 96 | Feature/default inflection points by version (CTE inlining 12, Memoize 14, pg_stat_io 16, JSON_TABLE 17) |
| PostgreSQL Wiki — Don't Do This | https://wiki.postgresql.org/wiki/Don't_Do_This | 2026-04-27 | 88 | Community-curated anti-patterns (SERIAL→IDENTITY, ENUM, pg_dump, types) |
| PostgreSQL Wiki — Tuning Your Server | https://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server | 2026-04-27 | 85 | Official community tuning guide |
| Hironobu Suzuki — Internals of PostgreSQL | https://www.interdb.jp/pg/ | 2026-04-27 | 92 | The only public deep dive on tuple structure, FSM, VM, HOT, MVCC |
| depesz (Hubert Lubaczewski) | https://www.depesz.com | 2026-04-27 | 88 | "Waiting for PostgreSQL X" series + commit-by-commit analysis |
| explain.depesz.com | https://explain.depesz.com/ | 2026-04-27 | 85 | Canonical EXPLAIN analysis tool (JSON input) |
| Crunchy Data Blog | https://www.crunchydata.com/blog | 2026-04-27 | 85 | Greg Smith, Jonathan Katz, Paul Ramsey — tuning & internals |
| EDB Blog | https://www.enterprisedb.com/blog | 2026-04-27 | 85 | Performance/HA posts, Bruce Momjian talks |
| Bruce Momjian Presentations | https://momjian.us/main/presentations.html | 2026-04-27 | 85 | Internals & performance by a longtime committer |
| Cybertec Blog | https://www.cybertec-postgresql.com/en/blog/ | 2026-04-27 | 82 | Schönig, Albe — pg_squeeze, MVCC, HA |
| Citus / Microsoft Postgres Blog | https://www.citusdata.com/blog | 2026-04-27 | 80 | Marco Slot, Craig Kerstiens — sharding, distributed Postgres |
| Percona PostgreSQL Blog | https://www.percona.com/blog/category/postgresql/ | 2026-04-27 | 78 | Jobin Augustine, Avinash Vallarapu — perf & ops |
| Robert Haas Blog | http://rhaas.blogspot.com | 2026-04-27 | 82 | Committer perspective on internals |
| Markus Winand — use-the-index-luke.com | https://use-the-index-luke.com/ | 2026-04-27 | 85 | Keyset pagination, indexing fundamentals (reference) |
| Andres Freund — Talks | https://anarazel.de/talks/ | 2026-04-27 | 85 | JIT (author), threading, AIO Postgres |
| Postgres.fm Podcast | https://postgres.fm/ | 2026-04-27 | 78 | Samokhvalov & Christofides — operational deep dives |
| Postgres Weekly Newsletter | https://postgresweekly.com | 2026-04-27 | 75 | Weekly monitoring of the PG ecosystem |
| PgBouncer Documentation | https://www.pgbouncer.org | 2026-04-27 | 88 | Primary docs for connection pooling (transaction/session/statement) |
| pgBackRest Documentation | https://pgbackrest.org | 2026-04-27 | 88 | Production-grade OSS backup (reference) |
| Patroni Documentation | https://patroni.readthedocs.io | 2026-04-27 | 85 | De facto HA orchestrator |
| pg_repack | https://reorg.github.io/pg_repack/ | 2026-04-27 | 80 | Online table rewrite (NTT) — bloat without VACUUM FULL |
| pg_squeeze | https://github.com/cybertec-postgresql/pg_squeeze | 2026-04-27 | 78 | Alternative to pg_repack via logical decoding (Cybertec) |
| pg_wait_sampling | https://github.com/postgrespro/pg_wait_sampling | 2026-04-27 | 78 | Low-cost wait_event profiling |
| PgCat | https://github.com/postgresml/pgcat | 2026-04-27 | 75 | Rust pooler ex-Instacart, multi-shard, prepared stmts |
| pgBadger | https://github.com/darold/pgbadger | 2026-04-27 | 80 | Reference Perl log analyzer |
| pgwatch2 (Cybertec) | https://github.com/cybertec-postgresql/pgwatch2 | 2026-04-27 | 78 | Time-series monitoring + Grafana |
| pgstattuple (extension) | https://www.postgresql.org/docs/17/pgstattuple.html | 2026-04-27 | 88 | Exact bloat measurement (full / approx) |
| ioguix bloat estimation queries | https://github.com/ioguix/pgsql-bloat-estimation | 2026-04-27 | 80 | Canonical bloat-estimation queries via catalogs |
| pgtune | https://pgtune.leopard.in.ua | 2026-04-27 | 70 | Baseline config — not a substitute for benchmarking |
| Cahill, Röhm, Fekete — SSI paper SIGMOD 2008 | https://drkp.net/papers/ssi-vldb12.pdf | 2026-04-27 | 95 | Academic foundation of Serializable Snapshot Isolation |

### 🆕 macOS Automation & Scripting (osascript / AppleScript / JXA)

> Rationale: A cross-cutting domain covering native macOS automation via the Open Scripting Architecture (osascript, AppleScript, JXA, Shortcuts) and its integration with the agentic AI ecosystem (MCP servers, Claude Desktop). Fits neither "AI & tech" (models/research) nor "DevOps" (infra). 12 Tier 1-2 sources identified.

| Title | URL | Date discovered | Score /100 | Justification |
|---|---|---|---|---|
| Apple — Mac Automation Scripting Guide | https://developer.apple.com/library/archive/documentation/LanguagesUtilities/Conceptual/MacAutomationScriptingGuide/HowMacScriptingWorks.html | 2026-04-30 | 95 | Primary Apple docs, canonical reference for OSA / AppleScript / JXA |
| Apple QA1888 — Sandboxing & Automation | https://developer.apple.com/library/archive/qa/qa1888/_index.html | 2026-04-30 | 92 | Official spec for TCC, AppleEvents, `com.apple.security.scripting-targets` entitlements |
| Claude Code — Hooks guide (Anthropic) | https://code.claude.com/docs/en/hooks-guide | 2026-04-30 | 90 | Primary Anthropic docs — using osascript in Claude Code hooks |
| Eclectic Light — TCC explainer (Howard Oakley, Nov 2025) | https://eclecticlight.co/2025/11/08/explainer-permissions-privacy-and-tcc/ | 2026-04-30 | 88 | macOS security reference, current on TCC in Sequoia/Sonoma |
| JXA-Cookbook (GitHub Wiki) | https://github.com/JXA-Cookbook/JXA-Cookbook/wiki | 2026-04-30 | 85 | The most complete community JXA cookbook (System Events, ObjC bridge) |
| steipete/macos-automator-mcp | https://github.com/steipete/macos-automator-mcp | 2026-04-30 | 85 | Reference osascript MCP server, 200+ pre-written recipes |
| macosxautomation.com (Sal Soghoian) | https://www.macosxautomation.com/applescript/notes/index.html | 2026-04-30 | 82 | Historical reference by the creator of AppleScript at Apple |
| Scripting OS X — Return of JXA (Armin Briegel, 2021) | https://scriptingosx.com/2021/11/the-unexpected-return-of-javascript-for-automation/ | 2026-04-30 | 80 | macOS admin authority, status of JXA in the Shortcuts era |
| achiya-automation/safari-mcp | https://github.com/achiya-automation/safari-mcp | 2026-04-30 | 80 | Production Safari implementation + osascript pooling benchmarks |
| Scripting OS X — Avoiding Privacy Requests (2020) | https://scriptingosx.com/2020/09/avoiding-applescript-security-and-privacy-requests/ | 2026-04-30 | 78 | TCC in an enterprise / MDM context |
| macOS26/Agent | https://github.com/macOS26/Agent | 2026-04-30 | 78 | Native Mac multi-LLM agent integrating osascript end-to-end |
| Picus Security — MITRE T1059.002 AppleScript | https://www.picussecurity.com/resource/blog/t1059-002-applescript | 2026-04-30 | 76 | Offensive-security angle, relevant for client EDR deployment |

---

## Review history

| Date       | Entries validated | New categories                                                                                                        | Entries rejected |
| ---------- | ----------------- | --------------------------------------------------------------------------------------------------------------------- | ---------------- |
| 2025-03-24 | 0 (pending)       | 🆕 Information Retrieval & source evaluation                                                                          | 0                |
| 2026-03-25 | 0 (pending)       | 🆕 Consulting & strategic frameworks                                                                                  | 0                |
| 2026-04-10 | 18 validated      | ✅ Information Retrieval & source evaluation · ✅ Consulting & strategic frameworks · 🆕 DevOps, SRE & Observability | 0                |
