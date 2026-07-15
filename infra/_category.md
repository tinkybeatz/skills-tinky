# Category: infra

**Scope.** The systems *around* the code: ops, deployment, servers/sysadmin, databases, security auditing, and static-analysis/quality tooling. Belongs here: containerization & deploy, Linux/Windows admin, DB expertise, pentest/security review, Sonar-style quality config. Does NOT belong: application code itself (→ `dev`).

**Naming.** `<tool>-expert` or capability — `docker-dokploy-expert`, `sysadmin-expert`, `postgres-expert`, `sonar-expert`, `pentest-audit`.

**Tone & audience.** Ops/SRE mindset: safety-first, idempotent, explicit about blast radius and rollback. Never runs destructive actions without confirmation.

**Required scaffolding.** `references/` for config templates and standards; `scripts/` for helpers. Keep secrets out — reference env vars, never literals.

**Default frontmatter.**
```yaml
name: <folder-name>
description: <what it does + trigger phrases>
user-invokable: true
```

**Skills here.** docker-dokploy-expert · sysadmin-expert · postgres-expert · sonar-expert · pentest-audit
