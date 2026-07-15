# Category: meta

**Scope.** Skills that manage Claude Code itself, this skills repo, or the skill/agent-authoring toolchain. Not domain work — these operate *on* the tooling. Belongs here: skill/agent creation, CLAUDE.md engineering, session handover, eval/benchmark harnesses, repo maintenance, and goal-routing/planning across the repo. Does NOT belong: anything that produces a domain deliverable (code, docs, designs).

**Naming.** Descriptive noun or artifact-oriented — `skill-creator`, `claude-md-architect`, `session-handover`.

**Tone & audience.** Precise and technical, written for the repo maintainer (you). Assumes familiarity with Claude Code internals.

**Required scaffolding.** `references/` for templates/conventions loaded on demand. May read/write config files (`CLAUDE.md`, `settings.json`, `~/.claude/`).

**Default frontmatter.**
```yaml
name: <folder-name>
description: <what it does + trigger phrases>
user-invokable: true
```

**Skills here.** skill-creator · claude-md-architect · session-handover · llm-lab · concierge · god
