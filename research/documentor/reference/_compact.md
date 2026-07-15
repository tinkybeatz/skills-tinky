# Documentor — Compact Reference

## 1. SIFT Pre-Screen (pass/fail)

| Check | Reject if |
|---|---|
| **Stop** | Emotional reaction without verification |
| **Investigate** | Source absent from lateral results or flagged unreliable |
| **Find** | Source clearly inferior to alternatives on same topic |
| **Trace** | Cannot trace claim to a primary source |

**Circular sourcing** = automatic reject.

## 2. Scoring Profiles — Weight Matrix

| Dimension | default | academic | market | regulatory |
|---|---|---|---|---|
| Relevance | 35 | 25 | 30 | 30 |
| Credibility | 30 | 40 | 20 | 40 |
| Freshness | 20 | 15 | 35 | 20 |
| Info value | 15 | 20 | 15 | 10 |

### Decision Thresholds

| Profile | Retain | Reserve | Discard | Reject |
|---|---|---|---|---|
| default | >=80 | 60-79 | 40-59 | <40 |
| academic | >=80 | 65-79 | 50-64 | <50 |
| market | >=75 | 55-74 | 35-54 | <35 |
| regulatory | >=85 | 65-84 | 50-64 | <50 |

## 3. Source Tier Hierarchies

### default (Base /30)

| Tier | Type | Base |
|---|---|---|
| 1 | Primary (raw data, law text, original study) | 25 |
| 2 | Secondary peer-reviewed | 22 |
| 3 | Secondary expert (institutional report) | 18 |
| 4 | Edited/curated (reference press) | 14 |
| 5 | Tertiary (Wikipedia, aggregators) | 8 |
| 6 | Unverified (blog, forum, social) | 4 |

### academic (Base /40)

| Tier | Type | Base |
|---|---|---|
| 1 | Peer-reviewed, meta-analysis | 35 |
| 2 | Cited preprint | 28 |
| 3 | Institutional report | 22 |
| 4 | Uncited preprint, thesis | 15 |
| 5 | Science journalism | 8 |
| 6 | Blog, forum | 3 |

### regulatory (Base /40)

| Tier | Type | Base |
|---|---|---|
| 1 | Law text (EUR-Lex, official gazette) | 38 |
| 2 | Case law, authority decisions | 34 |
| 3 | Official guide (data-protection / cybersecurity authority) | 28 |
| 4 | Legal doctrine | 20 |
| 5 | Law firm analysis | 12 |
| 6 | General blog | 4 |

## 4. Freshness Decay

| Domain | Full | Half | Zero |
|---|---|---|---|
| Pricing, specs, API | <1mo | 1-3mo | >3mo |
| Tech news, AI | <6mo | 6-12mo | >18mo |
| Regulatory | <1yr | 1-3yr | >5yr |
| Established science | <2yr | 2-5yr | >8yr |
| Principles, history | Evergreen | — | — |

## 5. Credibility Modifiers

| Factor | Modifier |
|---|---|
| Recognized expert author | +3 to +5 |
| Solid references | +2 |
| Promotional/sponsored | -10 (auto) |
| Author = company (no byline) | -3 |
| No cited sources | -3 |
| Missing date | -5 Freshness (max 50%) |

## 6. Corroboration Levels

| Level | Condition | Confidence |
|---|---|---|
| Unconfirmed | 1 source | Low — flag |
| Corroborated | 2 independent sources | Moderate |
| Solidly established | 3+ independent, type diversity | High |
| Consensus | Cross-type concordance | Very high |

**NOT independent if:** same upstream source, near-identical phrasing, same org/funding, simultaneous publication.

## 7. Critical Behavioral Rules

| Rule | Description |
|---|---|
| No unsourced claims as fact | Filling gaps with plausible unsourced content is the worst failure |
| Empty report over fabricated | Honest "no sources found" with reasons = correct behavior |
| Never "X is better than Y" absolute | Always conditional: "according to [source], X suits [case] because [reason]" |
| Contradictory sources | Produce decision matrix with conditions, not a verdict |
| Issue Tree before research | MECE decomposition guides queries; flat lists are anti-pattern |
| Labeling mandatory | Every claim: `Verified fact` / `Derived recommendation` / `Hypothesis` |

## 8. Output Structure

```
1. Executive summary (5-10 lines)
2. Key points (each labeled: fact/recommendation/hypothesis, sourced inline)
3. Ranked sources (rank, score, justification, URL, date)
4. Contradictions / limits
5. Confidence level (justified)
6. Next steps
```
