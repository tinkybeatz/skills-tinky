# Standards Library

This folder contains reusable engineering standards, organized by project.

## Structure

```
std/
├── README.md            # This file
├── _shared/             # Standards shared across all projects
│   └── security.md
├── sapain-borne/        # Standards specific to the sapain-borne project
│   ├── backend.md
│   ├── frontend.md
│   └── deployment.md
└── other-project/       # Another project
    └── api.md
```

## How to add standards

1. Create a folder named after the project (or use `_shared/` for cross-cutting standards)
2. Create one `.md` file per domain (backend, frontend, api, security, testing, etc.)
3. The `/senior-dev` skill loads them automatically during Step 0

## Standard file format

```markdown
# [Domain] Standards — [Project]

## Mandatory rules
- ...

## Conventions
- ...

## Anti-patterns to avoid
- ...
```
