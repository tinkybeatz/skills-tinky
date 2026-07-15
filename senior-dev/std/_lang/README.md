# Language Standards

Cross-cutting standards per **programming language**, independent of the project.

## Convention

- One file per language: `typescript.md`, `python.md`, `go.md`, etc.
- The name MUST match the language detected by `senior-dev` at Step 0.
- Detection: `tsconfig.json` → `typescript`, `pyproject.toml`/`requirements.txt` → `python`, `go.mod` → `go`, `Cargo.toml` → `rust`.

## Scope

- **Include**: universal language rules (typing, modules, error handling, anti-patterns).
- **Exclude**: framework-specific rules (React, FastAPI, gRPC) or project-specific rules (put those in `<project>/`).
- **Exclude**: cross-language rules (security, secrets) → `_shared/`.

## Format

Lightweight format (language standards are loaded automatically, keep them concise):

```markdown
# [Language] Standards

## Mandatory rules (MUST)
- R-XX-01 ... [why, in 1 line]

## Conventions (SHOULD)
- ...

## Anti-patterns (NEVER)
- ...
```

For standards that require formal traceability (sources, change log, metrics), see the project format used in `<project>/`.
