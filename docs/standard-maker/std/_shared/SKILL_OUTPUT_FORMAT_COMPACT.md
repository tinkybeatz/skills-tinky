# Skill Output Format — Quick Reference

Rules for all skill outputs. Ensures knowledge-base ingestion works.

## Structure

- MUST start with `# Title` in first 5 lines (5-80 chars)
- MUST use `## Section` headers (not `####` or deeper)
- Facts as bullet points (`- `), not buried in prose
- Paragraphs max 3 sentences

## Labels (for key claims)

- `**Fact**:` — sourced assertion
- `**Recommendation**:` — derived inference
- `**Hypothesis**:` — unconfirmed

## Tables

```
| Col A | Col B |
|---|---|
| val | val |
```
Separator `|---|---|` required. No newlines in cells.

## Code blocks

Always specify language: ` ```python `, ` ```yaml `, etc. Never nest.

## Sources

Inline: `[Title](URL)`. Recap table at end for Standard/Deep.

## Forbidden

- No HTML tags
- No YAML frontmatter (`---`)
- No underline headers (`===`)
- No emojis in headers
- No lines > 500 chars
