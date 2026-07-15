# DOCUMENTOR — Reliable source base by domain

A directory of reference sources organized by domain.
Enrich it as you research. Prioritize these sources before generic results.

---

## Regulation & law (EU/France)

| Source             | URL                        | Type      | Notes                                     |
| ------------------ | -------------------------- | --------- | ----------------------------------------- |
| EUR-Lex            | https://eur-lex.europa.eu  | Official  | EU legislative texts, primary reference   |
| Légifrance         | https://legifrance.gouv.fr | Official  | French law, consolidated texts            |
| CNIL               | https://cnil.fr            | Official  | GDPR, AI, personal data                   |
| ANSSI              | https://anssi.fr           | Official  | Cybersecurity, standards                  |
| European Parliament | https://europarl.europa.eu | Official  | EU legislative positions                  |

---

## Artificial intelligence & tech

| Source                      | URL                                                   | Type        | Notes                                                       |
| --------------------------- | ----------------------------------------------------- | ----------- | ----------------------------------------------------------- |
| Anthropic (blog)            | https://anthropic.com/news                            | Primary     | Claude, constitutional AI, safety                           |
| OpenAI (blog)               | https://openai.com/blog                               | Primary     | GPT, research updates                                       |
| Google DeepMind             | https://deepmind.google/discover/blog                 | Primary     | Gemini, fundamental research                                |
| Hugging Face Blog           | https://huggingface.co/blog                           | Specialized | Open source, benchmarks                                     |
| Arxiv (cs.AI)               | https://arxiv.org/list/cs.AI/recent                   | Academic    | Preprints, recent research                                  |
| Papers With Code            | https://paperswithcode.com                            | Academic    | Benchmarks + implementations                                |
| The Batch (DeepLearning.AI) | https://deeplearning.ai/the-batch                     | Newsletter  | Weekly AI digest                                            |
| Weaviate Blog — IR metrics  | https://weaviate.io/blog/retrieval-evaluation-metrics | Specialized | Precision@K, Recall@K, MAP, NDCG with Python examples (RAG) |
| Pinecone — Offline Eval IR  | https://www.pinecone.io/learn/offline-evaluation/     | Specialized | Detailed comparison of offline IR metrics                   |

---

## Market & tech business (France)

| Source               | URL                          | Type            | Notes                             |
| -------------------- | ---------------------------- | --------------- | --------------------------------- |
| Frenchweb            | https://frenchweb.fr         | Trade press     | Startups, fundraising, French tech |
| Maddyness            | https://maddyness.com        | Trade press     | French startup ecosystem          |
| Les Echos Start      | https://lesechos.fr/start-up | Press           | Business, financing               |
| Malt Blog            | https://blog.malt.com        | Specialized     | Freelancing, the tech labor market |
| LinkedIn (search)    | https://linkedin.com         | Professional social | Positioning, market signals   |

---

## Academic & scientific

| Source                         | URL                                                                       | Type       | Notes                                                                  |
| ------------------------------ | ------------------------------------------------------------------------- | ---------- | ---------------------------------------------------------------------- |
| Google Scholar                 | https://scholar.google.com                                                | Search engine | Broad access to the academic base                                   |
| Semantic Scholar               | https://semanticscholar.org                                               | Search engine | AI-powered, citations                                               |
| PubMed                         | https://pubmed.ncbi.nlm.nih.gov                                           | Official   | Life sciences                                                          |
| JSTOR                          | https://jstor.org                                                         | Archive    | Humanities and social sciences                                         |
| ResearchGate                   | https://researchgate.net                                                  | Community  | Article access, author contact                                         |
| Wikipedia — IR eval measures   | https://en.wikipedia.org/wiki/Evaluation_measures_(information_retrieval) | Tertiary   | Stable overview of Precision/Recall/NDCG/MAP, well sourced             |
| ERIC — Questioning CRAAP (PDF) | https://files.eric.ed.gov/fulltext/EJ1329588.pdf                          | Academic   | Empirical comparison of CRAAP vs. other frameworks, student data       |
| ACM Queue — USE Method         | https://queue.acm.org/detail.cfm?id=2413037                               | Peer-rev.  | Brendan Gregg — USE methodology published in ACM Queue                 |
| arXiv — Service Mesh MTLS      | https://arxiv.org/html/2411.02267v1                                       | Preprint   | Independent reproducible benchmark Istio vs Linkerd vs Consul (2024)   |

---

## Development & open source

| Source                   | URL                           | Type      | Notes                                    |
| ------------------------ | ----------------------------- | --------- | ---------------------------------------- |
| GitHub (official repos)  | https://github.com            | Primary   | Source code, changelogs, issues          |
| MDN Web Docs             | https://developer.mozilla.org | Official  | Web standards, browser API               |
| Official documentation   | (per technology)              | Primary   | Always prioritize the official docs      |
| Stack Overflow           | https://stackoverflow.com     | Community | Use with caution, check dates            |
| Dev.to                   | https://dev.to                | Community | Technical articles, tutorials            |

---

## Information Retrieval & source evaluation

> Methods for evaluating the relevance and credibility of web sources — qualitative frameworks (CRAAP, SIFT, E-E-A-T) and quantitative metrics.

| Source                                      | URL                                                                      | Type        | Notes                                                                  |
| ------------------------------------------- | ------------------------------------------------------------------------ | ----------- | ---------------------------------------------------------------------- |
| In the Library with the Lead Pipe           | https://www.inthelibrarywiththeleadpipe.org/2021/dismantling-evaluation/ | Academic    | Critique of CRAAP/SIFT, proposes a more robust proactive approach      |
| ETBI Digital Library — SIFT (Four Moves)    | https://library.etbi.ie/sources2/sift                                    | Educational | Practical explanation of SIFT with a comparison to CRAAP               |
| Toloka — Search relevance age of AI         | https://toloka.ai/blog/search-relevance/                                 | Specialized | Hybrid human + automatic evaluation, limits of metrics                 |
| Wikipedia — CRAAP Test                      | https://en.wikipedia.org/wiki/CRAAP_test                                 | Tertiary    | History, description, and limits (Blakeslee, 2004)                     |

---

## Consulting & strategic frameworks

> Methodologies for structuring thinking and communication in consulting (MECE, Pyramid Principle, issue trees).

| Source                                | URL                                                                                                                                       | Type        | Notes                                                     |
| ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ----------- | --------------------------------------------------------- |
| McKinsey Alumni — Barbara Minto (MECE)| https://www.mckinsey.com/alumni/news-and-events/global-news/alumni-news/barbara-minto-mece-i-invented-it-so-i-get-to-say-how-to-pronounce-it | Primary     | Interview with the inventor of the MECE framework         |
| Analyst Academy — Slide structure MBB | https://www.theanalystacademy.com/consulting-slide-structure/                                                                             | Educational | Analysis of BCG/McKinsey/Bain slides with Pyramid Principle |
| Slideworks — Pyramid Principle        | https://slideworks.io/resources/the-pyramid-principle-mckinsey-toolbox-with-examples                                                      | Educational | Before/after on an insurance case                         |

---

## DevOps, SRE & Observability

> Monitoring, distributed observability (metrics/logs/traces), SRE, SLO/SLI, and service mesh.

| Source                                 | URL                                                                                         | Type       | Notes                                                                 |
| -------------------------------------- | ------------------------------------------------------------------------------------------- | ---------- | --------------------------------------------------------------------- |
| Google SRE Book — Monitoring           | https://sre.google/sre-book/monitoring-distributed-systems/                                 | Primary    | Chapter 6, original source of the Four Golden Signals                 |
| Google SRE Workbook — Implementing SLOs| https://sre.google/workbook/implementing-slos/                                              | Primary    | Modern SLO practice + multi-burn-rate alerting                        |
| Google SRE Workbook — Alerting on SLOs | https://sre.google/workbook/alerting-on-slos/                                               | Primary    | Multiwindow multi-burn-rate alerting technique                        |
| OpenTelemetry — Documentation          | https://opentelemetry.io/docs/                                                              | Primary    | CNCF standard metrics/logs/traces, SDKs 12+ languages, OTLP protocol  |
| Brendan Gregg — USE Method             | https://www.brendangregg.com/usemethod.html                                                 | Primary    | Utilization/Saturation/Errors methodology by the author              |
| Prometheus                             | https://prometheus.io/docs/                                                                 | Primary    | Open-source metrics standard, PromQL, CNCF graduated                  |
| Grafana Labs — LGTM stack              | https://grafana.com/docs/                                                                   | Official   | Loki/Grafana/Tempo/Mimir, unified self-hosted stack                   |
| The New Stack — RED Method             | https://thenewstack.io/monitoring-microservices-red-method/                                 | Press      | RED method by Tom Wilkie (Weaveworks 2015) — Rate/Errors/Duration     |
| Istio — Service Mesh docs              | https://istio.io/latest/docs/                                                               | Official   | CNCF service mesh, Envoy telemetry, mTLS                              |

---

## Usage rules for this base

1. These sources are **starting points** — don't limit yourself to them if the research requires it
2. **Always check the date** of the page consulted, even on reliable sources
3. A reliable source can contain low-quality articles — evaluate **each article**, not the source as a whole
4. Enrich this file after each research session with newly validated sources
