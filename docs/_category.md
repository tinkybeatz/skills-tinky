# Category: docs

**Scope.** Generate formal written deliverables where the *output is a structured document*: specifications, engineering standards, requirement docs, reports, and records. If the primary artifact is a document, it belongs here — even if the subject is dev or product. Does NOT belong: the underlying capability (deciding an architecture → `dev`; product analysis → `product`).

**Naming.** `<artifact>-writer` / `<artifact>-builder` — `srs-writer`, `cdc-builder`, `brief-writer`, `standard-maker`, `progress-report`, `sprint-review`.

**Tone & audience.** Professional technical writer. Clear structure, templates, consistent formatting; the reader is usually a human stakeholder.

**Required scaffolding.** `references/` for templates and worked examples; `assets/templates/` where a fill-in document skeleton helps.

**Default frontmatter.**
```yaml
name: <folder-name>
description: <what it does + trigger phrases>
user-invokable: true
```

**Skills here.** srs-writer · cdc-builder · brief-writer · standard-maker · progress-report · sprint-review
