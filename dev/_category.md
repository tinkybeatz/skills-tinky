# Category: dev

**Scope.** Core software-engineering capabilities: architecture & design decisions, writing/executing code, testing, code review, version control, architecture decision records. Reusable across ANY project — project-specific rules come from that project's `CLAUDE.md`, not from the skill. Does NOT belong: ops/deploy/DB (→ `infra`), UI work (→ `design`), formal document generation (→ `docs`), product strategy (→ `product`).

**Naming.** Verb-first or role-based — `test-writer`, `senior-dev`, `architecture-conceptor`, `adr-writer`.

**Tone & audience.** Senior engineer. Concise, production-minded, opinionated on trade-offs. Reads project context before acting.

**Required scaffolding.** `references/` for standards/rubrics; `agents/` where a skill delegates to subagents.

**Default frontmatter.**
```yaml
name: <folder-name>
description: <what it does + trigger phrases, incl. common English + any French equivalents>
user-invokable: true
```

**Skills here.** senior-dev · architecture-conceptor · apply · test-writer · github-assistant · change-advisor · perf-analyzer · adr-writer
