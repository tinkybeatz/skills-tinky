# DOCUMENTOR — Scoring profiles

Configuration file for the weights, thresholds, and grids used in Step 4.
Each profile is self-contained: it defines everything the scoring needs.

**Profile selection:**

- If the user specifies a profile → use it
- Otherwise → infer from context (domain, mode, request type)
- When in doubt → `default`
- The user can request a custom profile at any time

---

## Profile: `default`

Use: general research, standard monitoring, multi-source comparison.

### Dimensions and weights

| Dimension               | Weight | Sub-dimensions                                                  |
| ----------------------- | ------ | --------------------------------------------------------------- |
| Relevance               | 35     | Fit to the query · coverage of the sub-questions                |
| Credibility             | 30     | Source type · authority · objectivity · presence of references  |
| Freshness               | 20     | Age vs. the domain's half-life                                  |
| Information value       | 15     | Non-redundancy · depth · original data                          |

### Source-type hierarchy (Credibility)

| Tier | Type                     | Examples                                            | Base /30 |
| ---- | ------------------------ | --------------------------------------------------- | -------- |
| 1    | Primary source           | Raw data, legal text, original study                | 25       |
| 2    | Secondary peer-reviewed  | Meta-analysis, systematic review, reviewed article  | 22       |
| 3    | Secondary expert         | Institutional report, investigative journalism      | 18       |
| 4    | Edited / curated         | Reference press, encyclopedia, official docs        | 14       |
| 5    | Tertiary                 | Wikipedia, aggregators, popularized summaries       | 8        |
| 6    | Unverified               | Personal blog, forum, social media, press release   | 4        |

### Freshness grid

| Domain                            | Full score if | Half score if | Zero if   |
| --------------------------------- | ------------- | ------------- | --------- |
| Pricing, product specs, API       | < 1 month     | 1–3 months    | > 3 months |
| Tech news, AI                     | < 6 months    | 6–12 months   | > 18 months |
| Regulatory / legislative          | < 1 year      | 1–3 years     | > 5 years |
| Established scientific research    | < 2 years     | 2–5 years     | > 8 years |
| Principles, definitions, history  | No decay      | —             | —         |

### Automatic penalties

| Signal                          | Penalty                |
| ------------------------------- | ---------------------- |
| Promotional content detected    | -10 Credibility        |
| Author = company, no byline     | -3 Credibility         |
| Missing publication date        | -5 Freshness (max 50%) |
| No cited sources                | -3 Credibility         |

### GRADE factors

| Downgrading factor   | Penalty  |
| -------------------- | -------- |
| Risk of bias         | -5 to -10 |
| Inconsistency        | -5       |
| Indirectness         | -5 to -10 |
| Imprecision          | -3 to -5 |
| Publication bias     | -5       |

| Upgrading factor           | Bonus   |
| -------------------------- | ------- |
| Large effect magnitude     | +3 to +5 |
| Unfavorable residual bias  | +3      |

### Thresholds

| Score | Action                                            |
| ----- | ------------------------------------------------- |
| >= 80 | Retain, high confidence                           |
| 60–79 | Retain with caveats, seek corroboration           |
| 40–59 | Discard unless it's the only available source, flag |
| < 40  | Reject systematically                             |

---

## Profile: `academic`

Use: scientific research, deep report, literature review.
Prioritizes methodological rigor and peer-reviewed traceability.

### Dimensions and weights

| Dimension               | Weight | Notes                                         |
| ----------------------- | ------ | --------------------------------------------- |
| Relevance               | 25     | Less dominant — broad context is accepted     |
| Credibility             | 40     | Top priority on peer review                   |
| Freshness               | 15     | Less critical except in fast-moving fields    |
| Information value       | 20     | Original data and reproducibility             |

### Source-type hierarchy (Credibility)

| Tier | Type                                        | Base /40 |
| ---- | ------------------------------------------- | -------- |
| 1    | Original peer-reviewed study, meta-analysis | 35       |
| 2    | Cited preprint (arxiv with citations)       | 28       |
| 3    | Institutional report (WHO, NIST, etc.)      | 22       |
| 4    | Uncited preprint, thesis                    | 15       |
| 5    | Science journalism article                  | 8        |
| 6    | Blog, forum, LinkedIn post                  | 3        |

### Freshness grid

| Domain                          | Full score if | Half score if | Zero if  |
| ------------------------------- | ------------- | ------------- | -------- |
| ML/AI, crypto, fast-moving      | < 6 months    | 6–18 months   | > 2 years |
| Computer science, engineering   | < 2 years     | 2–5 years     | > 7 years |
| Hard sciences (physics, bio)    | < 3 years     | 3–8 years     | > 12 years |
| Humanities                      | < 5 years     | 5–15 years    | > 20 years |
| Theoretical foundations         | No decay      | —             | —        |

### Automatic penalties

Same as `default` plus:

| Signal                                  | Penalty         |
| --------------------------------------- | --------------- |
| Benchmark self-published by the creator | max 20/40 Cred. |
| No methodology section                  | -10 Credibility |
| N < 30 without justification            | -5 Credibility  |

### Thresholds

| Score | Action                                                   |
| ----- | -------------------------------------------------------- |
| >= 80 | Retain, high confidence                                  |
| 65–79 | Retain if corroborated by at least 1 peer-reviewed source |
| 50–64 | Discard except in an exploratory context, flag           |
| < 50  | Reject                                                   |

---

## Profile: `market`

Use: competitive monitoring, market benchmarking, player analysis.
Prioritizes freshness and completeness of the landscape.

### Dimensions and weights

| Dimension               | Weight | Notes                                               |
| ----------------------- | ------ | --------------------------------------------------- |
| Relevance               | 30     | Coverage of the competitive landscape               |
| Credibility             | 20     | Less critical — a wider variety of sources accepted |
| Freshness               | 35     | Top priority — the market moves fast                |
| Information value       | 15     | Unique signals, data not found elsewhere            |

### Source-type hierarchy (Credibility)

| Tier | Type                                       | Base /20 |
| ---- | ------------------------------------------ | -------- |
| 1    | Analyst report (Gartner, Forrester)        | 18       |
| 2    | Trade press (TechCrunch, industry press)   | 15       |
| 3    | The player's official website              | 12       |
| 4    | LinkedIn, Crunchbase, public data          | 9        |
| 5    | Forum, Reddit, Hacker News                 | 5        |
| 6    | Anonymous or unverifiable source           | 2        |

### Freshness grid

| Domain                  | Full score if | Half score if | Zero if   |
| ----------------------- | ------------- | ------------- | --------- |
| Positioning, pricing    | < 3 months    | 3–6 months    | > 9 months |
| Fundraising, M&A        | < 6 months    | 6–12 months   | > 18 months |
| Sector trends           | < 1 year      | 1–2 years     | > 3 years |

### Automatic penalties

Same as `default` plus:

| Signal                          | Penalty                |
| ------------------------------- | ---------------------- |
| Undated financial data          | -10 Freshness          |
| Source = the competitor evaluated | -5 Credibility (bias) |

### Thresholds

| Score | Action                                           |
| ----- | ------------------------------------------------ |
| >= 75 | Retain, high confidence                          |
| 55–74 | Retain if corroborated or a unique angle         |
| 35–54 | Discard except for an exclusive market signal, flag |
| < 35  | Reject                                           |

---

## Profile: `regulatory`

Use: regulatory monitoring, compliance, legal analysis.
Prioritizes source authority and textual precision.

### Dimensions and weights

| Dimension               | Weight | Notes                                                       |
| ----------------------- | ------ | ----------------------------------------------------------- |
| Relevance               | 30     | Applicable to the precise legal case                        |
| Credibility             | 40     | Top priority — only official sources are authoritative      |
| Freshness               | 20     | Important, but the law consolidates slowly                  |
| Information value       | 10     | Less critical — precision beats originality                 |

### Source-type hierarchy (Credibility)

| Tier | Type                                        | Base /40 |
| ---- | ------------------------------------------- | -------- |
| 1    | Legal text (EUR-Lex, official gazette)      | 38       |
| 2    | Case law, authority decisions               | 34       |
| 3    | Official guide (data-protection / cybersecurity authority) | 28 |
| 4    | Legal doctrine (specialized journal)        | 20       |
| 5    | Law firm analysis, legal press              | 12       |
| 6    | General article, blog                       | 4        |

### Freshness grid

| Domain                          | Full score if | Half score if | Zero if      |
| ------------------------------- | ------------- | ------------- | ------------ |
| Text in force (consolidated)    | Evergreen     | —             | If repealed  |
| Interpretation / case law       | < 2 years     | 2–5 years     | > 8 years    |
| Bills, consultations            | < 6 months    | 6–18 months   | > 2 years    |

### Automatic penalties

Same as `default` plus:

| Signal                                  | Penalty         |
| --------------------------------------- | --------------- |
| Analysis without citing the legal text  | -10 Credibility |
| Confusing a bill with an adopted law    | -15 Relevance   |

### Thresholds

| Score | Action                                          |
| ----- | ----------------------------------------------- |
| >= 85 | Retain, high confidence                         |
| 65–84 | Retain if corroborated by an official source    |
| 50–64 | Discard except for signals of change, flag      |
| < 50  | Reject                                          |

---

## Creating a custom profile

The user can request a custom profile. Minimal structure:

```markdown
## Profile: `name`

Use: [1-line description]

### Dimensions and weights

| Dimension | Weight | Notes |
(total = 100)

### Source-type hierarchy

| Tier | Type | Base /[credibility weight] |

### Freshness grid

| Domain | Full score if | Half score if | Zero if |

### Automatic penalties (optional)

| Signal | Penalty |

### Thresholds

| Score | Action |
```

Dimensions can be renamed, added, or removed.
Only constraint: the weights must total 100.
