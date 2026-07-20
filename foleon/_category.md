# Category: foleon

**Scope.** Everything that is **only** relevant to Foleon work — the `ripley` monorepo and anything Foleon-specific. Holds project context (stack, architecture, conventions, gotchas) and Foleon-only capabilities that would make no sense in another project. This is deliberately a **work silo, kept out of the shared Foleon codebase**: the knowledge lives here, in skills you own, not in `ripley`'s checkout for other devs to inherit. Does NOT belong: reusable, cross-project engineering skills — those stay in `dev/`, `infra/`, etc., regardless of which project happens to use them.

**Naming.** Prefix everything with `foleon-` — `foleon-ripley`, `foleon-<capability>`. Keeps names globally unique in the flat symlink dir and signals the silo at a glance.

**Tone & audience.** Written for you, working on Foleon. May reference internal Foleon / ripley specifics — package names, app boundaries, conventions — directly.

**Required scaffolding.** `references/` for project knowledge that grows over time (e.g. `references/knowledge.md` as a self-enriching discoveries log). Minimal otherwise.

**Architecture standard (required).** Every project-context skill here (one that carries a specific repo's context for the awareness router) **MUST** follow [`docs/stds/PROJECT_CONTEXT_SKILL.md`](../docs/stds/PROJECT_CONTEXT_SKILL.md): `SKILL.md` + `references/project-facts.md` + `references/knowledge.md`, registered in `hooks/awareness-ignore.txt` as `<repo> -> <skill>`. `foleon-ripley` is the reference implementation.

**Default frontmatter.**
```yaml
name: <folder-name>
description: <what it does + trigger phrases, incl. "ripley", "foleon", app names like "editor"/"viewer">
user-invokable: true
```

**Skills here.** foleon-ripley (project-context skill for the `ripley` monorepo)
