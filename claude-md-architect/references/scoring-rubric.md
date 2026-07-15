# CLAUDE.md scoring rubric (out of 100)

A weighted 9-dimension rubric. Overall score = rounded weighted sum.

## Weighting table

| # | Dimension | Weight | Calculation |
|---|---|---|---|
| 1 | Size | 15 | See grid A |
| 2 | Instructional density | 10 | See grid B |
| 3 | Specificity (verifiability) | 15 | See grid C |
| 4 | Token cost | 10 | See grid D |
| 5 | Anti-duplication | 10 | See grid E |
| 6 | WHAT/WHY/HOW coverage | 10 | See grid F |
| 7 | Imports vs inline | 10 | See grid G |
| 8 | Compaction survival | 10 | See grid H |
| 9 | Practical test | 10 | See grid I |
| | **Total** | **100** | |

---

## Grid A — Size (15 pts)

| Lines | Pts | Note |
|---|---|---|
| ≤ 60 | 15 | Community optimum |
| 61–120 | 12 | Good |
| 121–200 | 8 | Acceptable (Anthropic limit) |
| 201–300 | 4 | Risk of degraded adherence |
| > 300 | 0 | Refactor mandatory |

## Grid B — Instructional density (10 pts)

Ratio = `(number of imperative bullets) / (number of non-empty lines excluding headings)`.

| Ratio | Pts |
|---|---|
| ≥ 0.6 | 10 |
| 0.4–0.6 | 7 |
| 0.2–0.4 | 4 |
| < 0.2 | 0 (too narrative) |

## Grid C — Specificity / verifiability (15 pts)

Count vague directives: "follow best practices", "write good code", "be careful", "format properly", "be consistent", etc.

| # of vague directives | Pts |
|---|---|
| 0 | 15 |
| 1 | 10 |
| 2 | 5 |
| ≥ 3 | 0 |

**Verifiability test**: can you write a test or a grep to confirm the rule is being followed? If not → vague.

## Grid D — Estimated token cost (10 pts)

Approximation: `tokens ≈ characters / 4`.

| Tokens | Pts |
|---|---|
| ≤ 600 | 10 (excellent) |
| 601–1200 | 7 |
| 1201–2000 | 4 (borderline) |
| > 2000 | 0 (too costly on every session) |

## Grid E — Anti-duplication (10 pts)

If the adjacent ecosystem is provided (skills, rules, MEMORY.md), grep for CLAUDE.md rules elsewhere.

| Duplicated lines detected | Pts |
|---|---|
| 0 | 10 |
| 1–2 | 6 |
| 3–5 | 3 |
| > 5 | 0 |

If the ecosystem isn't provided → default score = 7 (impossible to verify).

## Grid F — WHAT/WHY/HOW coverage (10 pts)

| Axes present | Pts |
|---|---|
| 3/3 | 10 |
| 2/3 | 6 |
| 1/3 | 3 |
| 0/3 | 0 |

- **WHAT** = stack, structure, working language
- **WHY** = project purpose, business constraints
- **HOW** = commands, conventions, "always do X"

## Grid G — Imports vs inline (10 pts)

Count inline code blocks > 5 lines.

| Blocks > 5 lines | Pts |
|---|---|
| 0 | 10 |
| 1 | 7 |
| 2 | 4 |
| ≥ 3 | 0 |

Prefer `@path/to/file` or `file:line` over long snippets.

## Grid H — Compaction survival (10 pts)

| Primary location | Pts |
|---|---|
| Project root (`./CLAUDE.md` or `./.claude/CLAUDE.md`) | 10 |
| User global (`~/.claude/CLAUDE.md`) | 10 (equivalent reload) |
| Subdirectory | 5 (lazy-load only) |
| Mix of root + subdirectories | 8 |

## Grid I — Practical test (10 pts)

Run this mentally: "If I ask Claude to `summarize your constraints for this project`, could it cite every rule?"

| Summary coverage | Pts |
|---|---|
| 100% of rules would be cited | 10 |
| 70–99% | 7 |
| 40–69% | 4 |
| < 40% | 0 (CLAUDE.md drowned) |

If this test can't be run empirically, judge qualitatively based on structural clarity.

---

## Interpreting the overall score

| Score | Verdict | Action |
|---|---|---|
| 85–100 | Excellent | No changes recommended |
| 70–84 | Good | A few targeted adjustments |
| 50–69 | Average | Partial refactor (top 3 issues) |
| 30–49 | Weak | Major refactor recommended |
| < 30 | Critical | Clean slate + WHAT/WHY/HOW rebuild |

---

## Recommended reporting format

```markdown
## 📊 Overall score: 67/100 — Average

| Dimension | Score | Target | Status |
|---|---|---|---|
| Size | 8/15 | < 60 lines | ⚠️ 142 lines |
| Instructional density | 4/10 | ≥ 60% bullets | ❌ ratio 0.31 |
| Specificity | 10/15 | 0 vague | ⚠️ 1 vague directive (l.47) |
| Token cost | 4/10 | < 600 tokens | ⚠️ ~1450 tokens |
| Anti-duplication | 6/10 | 0 duplicated lines | ⚠️ 2 lines (see skill X) |
| WHAT/WHY/HOW | 6/10 | 3/3 axes | ⚠️ WHY missing |
| Imports vs inline | 7/10 | 0 blocks > 5L | ⚠️ 1 block l.78–95 |
| Compaction survival | 10/10 | Root | ✅ |
| Practical test | 12/10... wait, don't exceed | | |
```
