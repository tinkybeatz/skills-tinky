# Standard: SKILL OUTPUT FORMAT

- Status: Active
- Version: 1.0.0
- Owner: Platform Team
- Approvers: Platform Team
- Effective date: 2026-04-26
- Last review date: 2026-04-26

## Purpose

Ensure that the outputs of the project's skills are parsable by the
deterministic ingestion module (`vault_ingest.py`) for storage in the
knowledge base. Without this standard, the parser loses the title, the tags,
or the structure — and ingestion produces incomplete or misclassified pages.

## Scope

Applies to: all skills that produce text reports (documentor, senior-dev,
architecture-conceptor, pentest-audit, adr-writer, blog-writer, research-brief,
srs-writer, etc.).

Out of scope: skills that produce non-text artifacts (design-prompt-generator,
slide-generator, pdf-generator).

## Normative Rules

### R-OUT-01 — H1 title required

Requirement:
- Every output MUST start with a `# Title` heading within the first 5 lines `[SRC-001]`
- The title MUST describe the content (not the skill or the mode)
- The title MUST be between 5 and 80 characters

Rationale:
- `vault_ingest._extract_title()` looks for the first H1/H2 in the first 20 lines. Without a structured title, the parser falls back to the first bold text or the first line — unpredictable results.

Enforcement:
- Manual review when skills are modified

Exceptions:
- Quick/ephemeral skills (< 5 lines): no H1 required

---

### R-OUT-02 — Sections structured as H2

Requirement:
- The content MUST be organized into `## Section name` sections `[SRC-001]`
- Each section SHOULD cover a single topic
- Subsections use `###`, never `####` or deeper

Rationale:
- The compressor (`_compress_content`) keeps every line starting with `#`. Well-structured headers = reliable compression. `####` and deeper add noise with no parsing gain.

Enforcement:
- Manual review

Exceptions:
- None

---

### R-OUT-03 — Structured facts, no long prose

Requirement:
- Factual information MUST use bullet points (`- `) or tables `[SRC-002]`
- Prose paragraphs SHOULD NOT exceed 3 sentences
- Every critical fact MUST be on its own line (not buried in a paragraph)

Rationale:
- The compressor keeps bullets, tables, and bold text. Prose paragraphs > 3 sentences are truncated to the first sentence. An important fact in the 4th sentence of a paragraph will be lost.

Enforcement:
- Instruction in each SKILL.md

Exceptions:
- blog-writer (prose is the final product, not a technical report)

---

### R-OUT-04 — Labelling of assertions

Requirement:
- High-impact assertions SHOULD carry an explicit label `[SRC-003]`:
  - `**Fact**:` or `**Verified fact**:` — directly sourced assertion
  - `**Recommendation**:` or `**Derived recommendation**:` — constructed inference
  - `**Hypothesis**:` — unconfirmed supposition
- Labels MUST be in bold at the start of the line, followed by `:` and the content

Rationale:
- The parser can extract and classify assertions by type. A fact without a label is indistinguishable from an opinion — ingestion loses traceability.

Enforcement:
- Already applied by documentor and senior-dev. To be propagated to the other skills.

Exceptions:
- Conversational skills (vulgarize, ceo-challenger): labels not required

---

### R-OUT-05 — Tables in standard Markdown pipe format

Requirement:
- Tables MUST use the Markdown pipe format (`| col | col |`) `[SRC-001]`
- The separator line (`|---|---|`) MUST be present
- Cells MUST NOT contain line breaks

Rationale:
- The compressor keeps every line starting with `|`. HTML tables, ASCII art, or tables without a separator are not recognized and are treated as prose (= potentially removed).

Enforcement:
- The chat renderer (table.py) already depends on this format

Exceptions:
- None

---

### R-OUT-06 — Code blocks with a language

Requirement:
- Code blocks MUST use triple backticks with the language specified `[SRC-001]`
- Format: ` ```python `, ` ```yaml `, ` ```bash `, ` ```typescript `, etc.
- Code blocks MUST NOT be nested

Rationale:
- The compressor tracks the `in_code_block` state via the triple backticks. Improperly closed or nested backticks break the tracking, and the rest of the document is treated as code (= no compression).

Enforcement:
- Lint by the chat renderer (code.py)

Exceptions:
- None

---

### R-OUT-07 — Sources with inline URLs

Requirement:
- Sources SHOULD be cited inline using the Markdown link format: `[Title](URL)` `[SRC-003]`
- A summary table of sources SHOULD be present at the end of the report for the Standard and Deep modes

Rationale:
- Inline links survive compression (the compressor keeps bullets containing bold text or links). A block of sources at the end of the document without inline links = the facts in the body lose their traceability after compression.

Enforcement:
- Already applied by documentor. To be propagated.

Exceptions:
- Skills without external research (adr-writer, test-writer)

---

### R-OUT-08 — Formatting prohibitions

Requirement:
- Outputs MUST NOT contain `[SRC-001]`:
  - HTML (`<div>`, `<br>`, `<table>`)
  - YAML frontmatter (`---\nkey: value\n---`) — reserved for the knowledge base
  - Underline headers (`===` or `---` beneath the text)
  - Emojis in headers (`## 🔥 Title` — breaks the slug)
  - Lines longer than 500 characters without a break (breaks the chat split)

Rationale:
- The parser strips YAML frontmatter if it finds any. If a skill produces some, the content after the frontmatter is treated as the start of the document — the title is lost. Underline headers are not detected by the `startswith("#")` regex. HTML is ignored by the compressor.

Enforcement:
- Review + vault_ingest tests

Exceptions:
- None

---

## Enforcement Summary

| Rule | Mechanism | Automated |
|---|---|---|
| R-OUT-01 | SKILL.md instructions + review | No |
| R-OUT-02 | SKILL.md instructions + review | No |
| R-OUT-03 | SKILL.md instructions | No |
| R-OUT-04 | SKILL.md instructions (documentor, senior-dev) | No |
| R-OUT-05 | Chat table renderer validation | Partial |
| R-OUT-06 | Chat code renderer validation | Partial |
| R-OUT-07 | SKILL.md instructions | No |
| R-OUT-08 | vault_ingest.py (strips YAML frontmatter) | Partial |

## Metrics

| Metric | Baseline | Target | Measurement |
|---|---|---|---|
| Ingestion success rate | Unknown | > 95% | Pages with valid title + >=2 tags after ingest |
| Compression ratio | ~30% | 20-40% | Output size / input size in knowledge-base pages |
| Title extraction accuracy | Unknown | 100% | Manual audit on 20 ingestions |

## Quick Reference Card

```
# Report title (required, 5-80 chars)

## Section 1

- **Fact**: sourced assertion ([source](url))
- **Recommendation**: inference (derived from: facts above)
- Unlabelled point (OK for minor facts)

## Section 2

| Column A | Column B |
|---|---|
| value | value |

Short text (max 3 sentences per paragraph).

## Sources

| # | Source | Date |
|---|---|---|
| 1 | [Title](url) | YYYY-MM-DD |
```

## Sources

- SRC-001 | vault_ingest.py | `internal path to vault_ingest.py` | Internal | 2026-04-26 | Deterministic parser that defines what is parsed and what is lost
- SRC-002 | Karpathy LLM Wiki | `https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f` | Karpathy | 2025 | Knowledge → wiki compression pattern
- SRC-003 | Documentor SKILL.md | `~/.claude/skills/documentor/SKILL.md` | Internal | 2026 | Fact/Recommendation/Hypothesis labelling convention already in production

## Change Log

| Version | Date | Author | Description |
|---|---|---|---|
| 1.0.0 | 2026-04-26 | Platform Team | Initial release — 8 rules aligned with vault_ingest.py parser |
