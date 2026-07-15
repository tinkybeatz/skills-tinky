# Architecture Conceptor — Compact Reference

## Output Structure (mandatory)

1. Executive summary (selected direction)
2. Architecture framing (context, assumptions, constraints, quality priorities)
3. Conceptual model (boundary map + architecture views)
4. Option comparison table (trade-offs: performance, reliability, cost, modifiability)
5. Decision package (recommended + alternatives + rejection rationale)
6. Validation plan (measurable checkpoints)
7. Risks, limitations, rollback triggers
8. Confidence level: `low` | `medium` | `high`

## Quality Rubric (100 pts)

| Criterion | Points | Low (0-min) | Mid | High (max) |
|-----------|--------|-------------|-----|-------------|
| Fit to problem & constraints | 25 | Ignores key constraints | Partial alignment | Fully aligned with business, constraints, QA priorities |
| Evidence strength & traceability | 25 | Unsupported claims | Gaps in traceability | All critical claims backed by strong, traceable, independent sources |
| Trade-off rigor & decision quality | 20 | <3 options or no comparison | Vague trade-offs | >=3 options, explicit trade-offs, weighted scorecard |
| Clarity & actionability | 15 | Unclear, hard to act on | Missing steps | Clear, concise, prioritized, executable next steps |
| Limitations & risk transparency | 15 | Omitted/trivialized | Some risks, not prioritized | Explicit, prioritized, rollback triggers + ownership |

### Delivery Thresholds

| Score | Verdict |
|-------|---------|
| 80-100 | Strong deliverable |
| 70-79 | Usable with reservations |
| < 70 | Rerun analysis cycle |

### Hard Fail Conditions (reject regardless of score)

- Decision without >= 3 compared options
- Critical claim without >= 2 independent sources
- Recommendation without rollback triggers or validation plan
- Quality attribute priorities not established before option comparison
- Economic trade-offs entirely absent

## Source Tiers

| Tier | Type | Usage |
|------|------|-------|
| 1 (mandatory) | Cloud provider arch guidance, ISO 25010/42010, official framework docs, ADR formats, TOGAF/C4 | Architecture decisions, QA claims |
| 2 (supporting) | Peer-reviewed research, recognized books, published postmortems, arch case studies | Pattern selection, trade-off reasoning |
| 3 (context only) | Blog posts, talks, forums, vendor marketing, social media | Idea discovery only. NEVER sole evidence |

## Minimum Evidence Policy

- >= 5 relevant sources per decision package
- >= 1 formal standard or technical report per decision
- >= 2 independent sources per recommended approach
- Economic claims MUST reference measurable data (pricing, benchmarks, capacity models)

## Freshness Policy

- Cloud services/pricing: most recent official source + exact update date
- Patterns/principles: foundational references allowed, complement with >= 1 recent validation

## Source Rejection Rules

Reject when: no identifiable owner + no date | non-reproducible claims | purely anecdotal for critical decisions | circular citations | vendor benchmark without independent validation

## Citation Format

Each source: title, URL/path, publication date (when available), one-line relevance rationale.

## Reviewer Checklist

- [ ] Problem framed with explicit constraints and quality priorities?
- [ ] >= 3 viable architecture options compared?
- [ ] Critical claims backed by strong, traceable evidence?
- [ ] Weighted scorecard driving final recommendation?
- [ ] Trade-offs explicit and defensible?
- [ ] Risks prioritized with rollback triggers and owners?
- [ ] Validation plan with measurable checkpoints?
- [ ] Limitations and confidence level stated?
