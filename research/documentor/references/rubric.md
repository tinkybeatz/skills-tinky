# DOCUMENTOR — Detailed scoring grid (Step 4)

Complete reference for scoring sources. Consult this file whenever you're unsure
how to evaluate a source.

---

## 1. SIFT filter — Pre-screening (pass/fail)

Apply BEFORE any numeric scoring. The source is eliminated if any one of these
conditions is met:

| SIFT check                          | Reject if                                                       |
| ----------------------------------- | --------------------------------------------------------------- |
| **Stop** — immediate reaction       | The content triggers an emotional reaction without verification |
| **Investigate** — lateral reading   | Source absent from lateral results, or flagged unreliable       |
| **Find** — alternative coverage     | Source much inferior to others available on the same topic      |
| **Trace** — trace to the origin     | Cannot trace the claim back to a primary source                 |

**Special case — circular sourcing:**
Trace each critical claim back to its original source.
Reject if: Source A cites Source B which cites Source A, or if several sources
use identical phrasing with no identifiable common source.
Classic case: unsourced Wikipedia -> press article -> Wikipedia cites the article.

---

## 2. Relevance (0–35 points)

| Tier    | Points | Condition                                                                   |
| ------- | ------ | --------------------------------------------------------------------------- |
| High    | 28–35  | Directly answers 1+ sub-question · data specific to the topic               |
| Medium  | 15–27  | Addresses the topic but tangentially · useful context without a direct answer |
| Low     | 1–14   | Mentions the topic without usable factual contribution                      |
| None    | 0      | Off-topic despite shared keywords                                           |

**Adjustments:**

- +5 if the source covers an angle not found elsewhere (high marginal value)
- -5 if the source addresses only a minor aspect of the sub-question

---

## 3. Credibility (0–30 points)

### 3a — Base score by source type

| Tier | Type                     | Examples                                            | Base /30 |
| ---- | ------------------------ | --------------------------------------------------- | -------- |
| 1    | Primary source           | Raw data, legal text, original study                | 25       |
| 2    | Secondary peer-reviewed  | Meta-analysis, systematic review, reviewed article  | 22       |
| 3    | Secondary expert         | Institutional report, investigative journalism      | 18       |
| 4    | Edited / curated         | Reference press, encyclopedia, official docs        | 14       |
| 5    | Tertiary                 | Wikipedia, aggregators, popularized summaries       | 8        |
| 6    | Unverified               | Personal blog, forum, social media, press release   | 4        |

### 3b — Credibility modifiers (-5 to +5)

| Factor                                    | Modifier     |
| ----------------------------------------- | ------------ |
| Recognized expert author in the domain    | +3 to +5     |
| Solid references / bibliography           | +2           |
| Professional presentation, error-free     | +1           |
| Missing author or publication date        | -3 to -5     |
| Promotional / sponsored content           | -10 (auto)   |
| Persuasive tone, lack of nuance           | -3 to -5     |
| Author = company (no person)              | -3           |
| No cited sources                          | -3           |

### 3c — GRADE factors (final adjustment)

Inspired by the medical GRADE framework, these factors apply after the standard scoring:

**Downgrading factors:**

| Factor               | Signal                                       | Penalty  |
| -------------------- | -------------------------------------------- | -------- |
| Risk of bias         | Source financially tied to the topic evaluated | -5 to -10 |
| Inconsistency        | Contradicts other evidence without explanation | -5      |
| Indirectness         | Doesn't directly answer the sub-question     | -5 to -10 |
| Imprecision          | Vague, unquantified claims                   | -3 to -5 |
| Publication bias     | Selective reporting of positive results      | -5       |

**Upgrading factors:**

| Factor                     | Signal                                        | Bonus   |
| -------------------------- | --------------------------------------------- | ------- |
| Large effect magnitude     | Solid evidence, quantified data, large N      | +3 to +5 |
| Unfavorable residual bias  | Possible biases work against the thesis       | +3      |

---

## 4. Freshness (0–20 points)

### Decay grid by domain

| Domain                            | Half-life    | 20/20 if      | 10/20 if  | 0/20 if   |
| --------------------------------- | ------------ | ------------- | --------- | --------- |
| Pricing, product specs, API       | 1–4 weeks    | < 1 month     | 1–3 months | > 3 months |
| Tech news, AI                     | 3–6 months   | < 6 months    | 6–12 months | > 18 months |
| Regulatory / legislative          | 1–3 years    | < 1 year      | 1–3 years | > 5 years |
| Established scientific research    | 2–5 years    | < 2 years     | 2–5 years | > 8 years |
| Principles, definitions, history  | Evergreen    | No decay      | —         | —         |

### Additional rules

- **Always check** whether a more recent version of the same source exists
- If all sources found exceed the domain's half-life: flag `⚠️ outdated corpus`
- An old source cited as a historical reference keeps its value → don't penalize
- Missing publication date: automatically assign 5/20 max

---

## 5. Information value (0–15 points)

| Tier    | Points | Condition                                                                |
| ------- | ------ | ------------------------------------------------------------------------ |
| High    | 12–15  | Original data, novel analysis, an angle not covered by the others        |
| Medium  | 6–11   | Useful contribution but partially redundant with other retained sources  |
| Low     | 1–5    | Restates already-covered information, little marginal value              |
| None    | 0      | 100% redundant with an already better-scored source                      |

**Anti-redundancy rule:** if two sources say the same thing with a similar score,
retain the one with the better credibility score. Don't artificially inflate the
source count with editorial duplicates.

---

## 6. Cross-corroboration (post-scoring)

After individual scoring, assess the corroboration of each **key claim**:

| Level              | Condition                                                     | Confidence       |
| ------------------ | ------------------------------------------------------------- | ---------------- |
| Unconfirmed        | Single source                                                 | Low — flag       |
| Corroborated       | 2 independent, concordant sources                             | Moderate         |
| Solidly established | 3+ independent sources, type diversity                       | High             |
| Consensus          | Concordance across source types and different perspectives    | Very high        |

### Independence test

Two sources are **NOT independent** if:

- They cite the same single upstream source (wire service, press release)
- They use near-identical phrasing (likely copy or common source)
- They come from the same organization or funding network
- They were published simultaneously (likely syndication)
- One is a summary/reformulation of the other

### Arbitrating contradictions

When sources contradict each other:

1. **Investigate why**: difference in date? in definition? in scope?
2. **Weight**: prioritize the source that is (a) more primary, (b) more recent,
   (c) more methodologically rigorous, (d) of independent origin
3. **Consensus rule**: if 3+ independent sources agree and 1 diverges,
   investigate the outlier but lean toward the consensus
4. **Balance rule**: if sources split ~50/50,
   mark the claim as `⚠️ contested` — don't pick a side
5. **Never resolve** by personal opinion or by a simple majority without
   verifying the sources' independence

---

## 7. Decision thresholds

| Total score /100 | Action                                                           |
| ---------------- | ---------------------------------------------------------------- |
| ≥ 80             | Retain — high confidence                                         |
| 60–79            | Retain with caveats — seek corroboration if it's a key claim     |
| 40–59            | Discard — unless it's the only existing source, then flag        |
| < 40             | Reject systematically                                            |

---

## 8. Bias detection — Automatic signals

### Promotional content (penalty -10 Credibility)

- Author = company name, no identifiable person
- Persuasive tone geared toward product benefits
- No opposing viewpoints or stated limitations
- Labels: "Sponsored", "Partnership", "Brand content", "Paid post"
- URL redirected to an unexpected domain
- Call-to-action embedded in "informative" content

### Astroturfing (penalty: rejection)

- Identical or near-identical phrasing across supposedly independent sources
- Activity concentrated during office hours (non-organic pattern)
- Recent accounts with no history, active on a single topic
- No transparency about funding or affiliation

### Self-published leaderboards and benchmarks

- Benchmarks published by the creator of the product evaluated: Credibility max 20/30
- Always look for an independent reproduction
- Flag the potential bias explicitly in the deliverable
