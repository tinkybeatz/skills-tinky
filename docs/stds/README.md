# Standards

Normative documents for this repo. A standard is a technical contract: numbered rules with
MUST/SHOULD keywords, a stated enforcement mechanism per rule, a conformance checklist, and a
change log. Authored and amended with the `standard-maker` skill.

> **This folder is not a skill category.** `docs/` doubles as the skill category for
> document-deliverable skills (`srs-writer`, `cdc-builder`, …) *and* as the home of `stds/`.
> `stds/` contains no `SKILL.md` and is skipped by the taxonomy audit.

| Standard | Rules | Governs |
|---|---|---|
| [`PROJECT_CONTEXT_SKILL.md`](PROJECT_CONTEXT_SKILL.md) | `PCS-1`…`PCS-11` | Skills that carry one project's context for the awareness router: placement, naming, required files, the self-enrich boundary, registration, and the optional external mirror. Reference implementation: `foleon/foleon-ripley`. |
| [`CHEAT_SHEET.md`](CHEAT_SHEET.md) | `CHS-1`…`CHS-12` | What may be written to a human-facing cheat-sheet database and how: admission gates, closed field set, symptom-indexed titles, length and voice caps, decay policy, review gate. Reference implementation: the Foleon `Findings` database in Notion, written by `foleon/foleon-cheatsheet`. |

The two compose: PCS-11 permits a project-context skill to mirror findings to one external
surface, and `CHEAT_SHEET.md` governs what that surface may contain.

## Referenced from

- [`README.md`](../../README.md) → "Project awareness"
- [`foleon/_category.md`](../../foleon/_category.md) → architecture standard + mirror
- [`meta/skill-creator/references/taxonomy-and-placement.md`](../../meta/skill-creator/references/taxonomy-and-placement.md) → project-context skills
- [`meta/concierge/scripts/audit.sh`](../../meta/concierge/scripts/audit.sh) → checks PCS-2, PCS-3, PCS-9

## Conventions

- Filename `UPPERCASE_SNAKE_CASE.md`; rule IDs are a short prefix plus a number (`PCS-4`, `CHS-8`).
- Rule IDs are **stable** — never renumbered, never reused after removal.
- Versioned in the file's header table (`MAJOR.MINOR.PATCH`): PATCH = wording, MINOR = rule added or
  changed, MAJOR = scope change or rule removal. Every change gets a change-log row.
- A rule prefix must not collide with an identifier used elsewhere in the system. `CHS-n` names a
  *rule*; `CS-nn` names a *row* in the cheat-sheet database — deliberately different prefixes.
