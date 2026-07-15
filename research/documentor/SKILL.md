---
name: "documentor"
description: >
  Use this skill for any web research, monitoring, source synthesis, information
  comparison, or production of documented and sourced deliverables.
  Trigger automatically when the user asks to: "research", "find", "search",
  "synthesize", "compare sources", "what is", "what's the state of",
  "monitor", "document", "analyze the market", "benchmark", or any phrasing
  implying factual research with citations. Applicable to technical, regulatory,
  scientific, and business topics. Do not use for pure content generation
  without factual grounding.
autoload:
  - references/few_shot.md
---

# DOCUMENTOR

A structured research profile that produces reliable, traceable, and actionable
syntheses from web and academic sources.

Read `references/context.md` at the start of each session to tailor the research
to the user's business context.

---

## Scope

**In scope:** web research, topic monitoring, source comparison, synthesis with
citations, competitive benchmarking.

**Out of scope:** inventing unverified facts, recommendations without sources,
reusing outdated information without checking the date.

---

## Step 0 — Mode selection

First, identify the mode that fits the request:

| Mode            | Signal                                               | Behavior                                                                        |
| --------------- | ---------------------------------------------------- | ------------------------------------------------------------------------------- |
| ⚡ **Quick**    | Simple, factual question, short answer expected      | 1 cycle, ≥ 3 sources, 3–5 line summary, no quality rubric                       |
| 📋 **Standard** | Monitoring, synthesis, multi-source comparison       | Full 6-step workflow, complete output format                                    |
| 🔬 **Deep**     | Report deliverable, academic research, client brief  | Multiple cycles required, academic sources required, long structured report     |

If the mode is not explicitly requested, infer it from context.
When in doubt between Standard and Deep, ask.

---

## Step 1 — Understand the request

- Identify the intent, context, constraints, and expected level of detail
- Extract keywords, synonyms, technical terms, and variants
- Turn vague requests into verifiable sub-questions
- Identify the **deliverable's audience**: internal use / end client / designer brief
  - Internal use → technical jargon allowed, sources visible, dense format
  - End client → plain language, executive summary up front, sources in appendix
  - Designer / stakeholder brief → short synthesis, actionable points only

### Issue Tree + MECE decomposition

Break the request down into an **Issue Tree**: a hierarchy of sub-questions
where each level is **MECE** (Mutually Exclusive, Collectively Exhaustive).

- **Mutually Exclusive** — each sub-question covers a distinct angle, with no
  overlap. If two sub-questions can be answered by the same sources, they overlap
  → merge or re-split them.
- **Collectively Exhaustive** — the set of sub-questions covers the entire topic.
  If a relevant aspect is covered by no sub-question, the tree is incomplete
  → add it.

**Quick MECE test:** every fact found during the research must fall into exactly
one sub-question. If it falls into two → overlap. If it falls into none →
coverage gap.

**Concrete example — MECE Issue Tree:**

```
Request: "How does crypto copy trading work?"

Issue Tree:
├── 1. Monitoring — How are target wallets identified and tracked?
├── 2. Detection — How are transactions detected in real time?
├── 3. Replication — How are trades copied technically?
├── 4. Execution — How are orders placed on DEXs/CEXs?
└── 5. Risks — What are the risks and limits of the system?

MECE test:
✓ ME: each stage of the pipeline is distinct
✓ CE: the full cycle is covered (from identification to execution + risks)
```

**Intermediate deliverable:** a research plan with 3 to 7 MECE sub-questions +
selected mode + identified audience

---

## Step 2 — Plan the research

Prepare the queries by applying the **multilingual strategy**:

| Topic type                                   | Priority language                             |
| -------------------------------------------- | --------------------------------------------- |
| Tech, AI, academic                           | 🇬🇧 English first, supplement in local language |
| EU/national regulation                       | 🇬🇧 English and the local language in parallel  |
| Local market, local competitive monitoring   | 🌍 Local language first                        |

Prepare base queries + boolean variants (`AND`, `OR`, `NOT`).
See `references/source.md` to target reliable sources by domain.

**Intermediate deliverable:** a list of queries by language and target source types

---

## Step 3 — Run the research

- Launch searches across multiple channels
- Capture essential metadata: author, date, institution, URL, document type

### Primary-source prioritization rule

**Always start with primary sources** (official docs, legal texts, original
studies, GitHub repos). Only drop down to Tier 4–6 sources (blogs, forums,
aggregators) when primary sources don't cover the topic.

**Anti-dilution rule:** if official documentation exists and covers the topic,
don't pad the corpus with community blogs that restate the same information.
Prefer 5 Tier 1–2 sources over 10 sources where half are Tier 4–6. One
well-exploited primary source beats three tertiary sources that paraphrase it.

**Primary-source temporal coverage rule:**
when a concept, pattern, or technology has an **identifiable author**, cover the
range of their publications: the founding article/document AND any significant
later updates or reformulations. One gives the principles, the other gives the
nuances — both are needed, neither replaces the other. Don't introduce a recency
bias (always preferring the latest text) or an age bias (ignoring the author's
evolving thinking).

**Minimum coverage rule (Standard & Deep):**

- At least 3 relevant sources
- At least 1 primary source when available — **if official documentation exists, it is mandatory**
- At least 2 independent sources for every high-impact claim

### "No reliable source found" rule 🚨

If after 2 research cycles no source reaches the 60/100 threshold:

1. **Never fill the gap with unsourced content** — even if plausible
2. Deliver an empty report with an explicit explanation:
   ```
   ⚠️ Research unsuccessful
   No reliable source (≥ 60/100) found after 2 cycles on: [topic]
   Identified reasons: [too recent / too niche / proprietary data / ...]
   Recommended alternatives: [specialized sources to consult manually]
   ```
3. Suggest a reformulation of the request or alternative access paths

---

## Step 4 — Evaluate and rank the results

Evaluation happens in 3 successive passes: filtering, scoring, corroboration.

- **Weights, thresholds, and grids** → defined in `references/scoring.md` (configurable profiles)
- **Detailed tiers per criterion** → `references/rubric.md`
- This section describes the **mechanisms** only.

### 4a — Pass 1: SIFT filter (pass/fail)

Before any scoring, apply the **SIFT** filter (Stop, Investigate, Find, Trace):

1. **Stop** — don't react to the content before verifying the source
2. **Investigate** — lateral reading: leave the source, check what
   _other sources_ say about it (reputation, funding, affiliations)
3. **Find** — is there better coverage of the same topic elsewhere?
4. **Trace** — trace each key claim back to its original source

**Immediate rejection if:** source known to be unreliable · no traceability
to an origin · circular sourcing detected (see 4d)

### 4b — Pass 2: Score out of 100

Load the scoring profile from `references/scoring.md`.
The active profile defines the **dimensions**, their **weights**, and the
freshness and credibility **grids**. If no profile is specified by the user,
use `default`.

Each source that passes the SIFT filter is scored out of 100 based on the active
profile's dimensions and weights. The standard dimensions are:

- **Relevance** — fit to the query, coverage of the sub-questions
- **Credibility** — source type (6-tier hierarchy), authority, objectivity, references
- **Freshness** — age vs. the domain's half-life (grid defined by profile)
- **Information value** — non-redundancy, depth, original data

Adjust the credibility score by **-5 to +5** based on: author credentials,
detected objectivity/bias, presentation quality, cited references.

### 4c — Pass 3: Cross-corroboration

After individual scoring, assess the **corroboration level** of each key claim:

| Level             | Condition                                                     | Effect                       |
| ----------------- | ------------------------------------------------------------- | ---------------------------- |
| Unconfirmed       | Single source                                                 | Flag `⚠️ single source`      |
| Corroborated      | 2 independent, concordant sources                             | Moderate confidence          |
| Solidly established| 3+ independent sources, type diversity                       | High confidence              |
| Consensus         | Concordance across different source types and perspectives    | Very high confidence         |

**Independence test** — two sources are NOT independent if:

- They cite the same single upstream source
- They use near-identical phrasing (likely common source)
- They come from the same organization / funding network
- They were published simultaneously (likely syndicated release)

### 4d — Bias and circular-sourcing detection

**Signals of promotional content** (penalty defined in the scoring profile):

- Author = company name, no identifiable person
- Persuasive tone geared toward product benefits, not informative
- No opposing viewpoints or stated limitations
- Labels: "Sponsored", "Partnership", "Brand content"

**Circular-sourcing detection:**

- Trace each critical claim back to its original source
- If Source B cites Source A, and Source A cites Source B → circular, reject
- If several sources use the exact same phrasing → a single source in disguise

**Rule:** for any critical claim, require at least one source that **predates**
the others and contains primary evidence.

### 4e — Thresholds and actions

Thresholds are defined in the active profile (`references/scoring.md`).
Flag any contested, unconfirmed, or single-source information.

---

## Step 5 — Synthesize and deliver

- Structure the answer around the sub-questions
- Cite sources **inline** for every critical claim (not just at the end of the report)
- Make contradictions explicit
- Adapt the level of jargon and length to the identified audience (Step 1)

### Mandatory fact / interpretation labeling (Standard & Deep)

Every key point in the deliverable **must** carry an explicit label:

- **`Verified fact`** — a claim directly sourced from a primary or peer-reviewed
  secondary document. Always accompanied by the inline source.
- **`Derived recommendation`** — an interpretation or inference built from
  several facts. Must mention the facts it derives from.
- **`Hypothesis`** — an assumption not confirmed by the sources. Must be flagged
  as such and accompanied by a confidence level.

**Rule:** never present a derived recommendation as a fact.
If the boundary is fuzzy, label it as a `derived recommendation`.
A missing label is a deliverable failure.

---

## Step 6 — Iterate if needed

Run another cycle if coverage is insufficient, contradictions remain unresolved,
or the sources are too weak or too old.

**Stopping condition:** overall score ≥ 80/100 · no critical point without a reliable source

---

## Step 7 — Post-delivery hook

### 7a — Notion export

After every Standard or Deep delivery, systematically offer:

> "Would you like me to save this report to Notion?"

If yes → use the Notion MCP to create a page in the appropriate space with a
title, date, executive summary, and ranked sources.

---

### 7b — Automatic source-base update

After every delivery, identify all sources that scored ≥ 75/100 and are absent
from `references/source.md`. Silently append them to
`references/sources.inbox.md` following the rules below.

#### Rule 1 — Adding to an existing category

Add to an existing category if **all** of these conditions are true:

- The source covers a domain **already named** in `source.md`
  (e.g. "Artificial intelligence & tech", "EU/national regulation")
- The source's topic fits **without forcing** into the category definition
- The existing category has **fewer than 12 entries** (beyond that, consider a subcategory)

Entry format:

```
| [Title] | [URL] | [Date discovered] | [Score /100] | [1-line justification] |
```

#### Rule 2 — Creating a new category

Create a new category if **at least one** of these criteria is true:

- The source covers a domain **absent** from `source.md` (new emerging topic)
- The source belongs to an existing domain but with a **radically different angle**
  (e.g. an "AI & labor law" source belongs neither in "AI & tech" nor in "Regulation")
- **3 or more sources** with the same orphan angle have accumulated in the inbox
  → this signals that a category is structurally missing

New-category format in the inbox:

```
### 🆕 [Proposed category name]
> Rationale: [why this category doesn't fit the existing ones]
| Title | URL | Date | Score | Justification |
```

#### Rule 3 — Ambiguous cases

If the source could belong to two existing categories:

- Place it in the category whose **main topic** it covers, not the secondary one
- Add a note: `⚠️ Possible overlap with [other category]`

If the domain is new but **only one source** illustrates it:

- Don't create a category — append to `sources.inbox.md` under `### 🔍 To classify`
- Wait for a second source to confirm the need for a category

#### Rule 4 — What we never add

- Sources < 75/100
- Duplicates of a URL already in `source.md` or `sources.inbox.md`
- Sources without a verifiable URL
- Promotional sources (credibility score ≤ 10/30 automatically)

#### End-of-session signal

At the end of a delivery, systematically display:

```
📚 Source base updated
→ [N] new source(s) added to sources.inbox.md
→ [N] in existing categor(ies): [list]
→ [N] new categor(ies) proposed: [list]
→ [N] source(s) placed in "To classify"
Remember to promote sources.inbox.md → source.md at your next review.
```

If 0 new sources: display nothing.

---

## Source credibility rules

**Systematic checks (Step 4b):**

- Authority: recognized institution, author with verifiable credentials
- Traceability: publication date, cited references, visible methodology
- Independence: no financial/editorial tie to the other cited sources
- Consistency: the claims hold up under lateral reading (SIFT)

**Penalties and GRADE factors** → defined in the active scoring profile
(`references/scoring.md`). Do not hardcode values here.

---

## Output format

### ⚡ Quick mode

```
Direct answer (3–5 lines)
Sources: [title] — [URL] — [date]
Confidence: low / medium / high
```

### 📋 Standard & 🔬 Deep mode

```
1. Executive summary     — 5 to 10 lines (adapted to the audience)
2. Key points            — each point labeled:
                            • Verified fact: [claim] ([inline source])
                            • Derived recommendation: [claim] (derived from [facts])
                            • Hypothesis: [claim] (confidence: [level])
3. Ranked sources        — rank, score, justification, link, date
4. Contradictions        — identified limits, gray areas
5. Confidence level      — low / medium / high + justification
6. Next steps            — if residual uncertainty
```

---

## Quality rubric (Standard & Deep)

| Criterion                  | Points |
| -------------------------- | ------ |
| Fit to the question        | 30     |
| Evidence quality           | 25     |
| Information freshness       | 15     |
| Clarity and structure      | 15     |
| Transparency about limits  | 15     |

**Thresholds:** `≥ 80` robust deliverable · `70–79` deliverable with caveats · `< 70` rerun

---

## Failure modes & recovery

| Failure                                 | Corrective action                                                                                                    |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Request too vague                       | Reframe with explicit constraints, ask for the mode                                                                  |
| No reliable source                      | Apply the "no source" rule (Step 3)                                                                                  |
| Contradictory sources, no arbitration   | Add primary and independent sources                                                                                  |
| Outdated corpus                         | Tighten the time window, search in English                                                                           |
| Over-reliance on one source family      | Separate established facts / unresolved points                                                                       |
| Audience misidentified                  | Reread Step 1, adjust the format before delivery                                                                     |
| Dilution by Tier 4–6 sources            | Apply the anti-dilution rule (Step 3): prune tertiary sources when primaries cover the topic                         |
| Fact / interpretation mixed             | Reread Step 5: every point must carry an explicit label (`verified fact`, `derived recommendation`, `hypothesis`)    |
| Sources cited in a block, not inline    | Attach each claim to its source in the text, not just in an appendix                                                 |

---

## Supporting resources

Read the relevant file only if the context requires it:

| File                   | When to read it                                            |
| ---------------------- | ----------------------------------------------------------- |
| `references/context.md` | **Always** — the user's business context                    |
| `references/source.md`  | Step 2 — to target the right sources by domain              |
| `references/scoring.md` | Step 4 — scoring profiles (weights, thresholds, grids)      |
| `references/rubric.md`  | Step 4 — detailed tiers per criterion, advanced mechanisms  |
| `references/example.md` | If the expected behavior is unclear for a request type      |
| `references/evals.md`   | After modifying the skill — to validate the behavior        |

---

## Examples (few-shot)

### Example A — EU regulation (Issue Tree)

**Input:** "What is the current state of the AI Act for a startup?"
→ Standard mode · Audience: internal use · Languages: local + EN

**MECE Issue Tree:**
```
AI Act for a startup
├── 1. Legislative status (in force / timeline)
├── 2. System classification (risk levels)
├── 3. Concrete obligations (per risk level)
├── 4. Startup impact (compliance costs, SME exemptions)
└── 5. Gray areas (diverging interpretations between states)
```
→ Priority sources: EUR-Lex, europa.eu, national data-protection authority
→ MECE test: each article of the law falls into exactly one branch

### Example B — Technical / academic (Issue Tree)

**Input:** "What recent methods improve RAG?"
→ Deep mode · Audience: internal use · Language: EN first

**MECE Issue Tree:**
```
RAG improvements
├── 1. Retrieval (chunking, embeddings, reranking)
├── 2. Augmentation (prompt engineering, context)
├── 3. Generation (fine-tuning, chain-of-thought)
├── 4. Evaluation (metrics, benchmarks)
└── 5. Architecture (hybrid search, graph RAG, agentic RAG)
```
→ Arxiv, Papers With Code, Anthropic/Google blogs
→ Compare ≥ 3 publications · state the level of evidence and reproducibility

### Example C — Market monitoring

**Input:** "Which agentic AI agencies exist in the market in 2025?"
→ Standard mode · Audience: internal use · Language: local first

**MECE Issue Tree:**
```
Agentic AI agencies in the market
├── 1. Natively agentic agencies (founded on this positioning)
├── 2. Repositioned agencies (IT services firms / digital agencies that pivoted)
├── 3. Positioning and offerings (services provided, pricing)
├── 4. Size and maturity (headcount, clients, tenure)
└── 5. Differentiation vs. your company (overlap, complementarity)
```
→ LinkedIn, freelance marketplaces, tech press, agency websites
→ Rank by similarity to your company
