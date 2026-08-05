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
| [`CHEAT_SHEET.md`](CHEAT_SHEET.md) | `CHS-1`…`CHS-11` | What may be written to a human-facing cheat-sheet **page** and how: five admission gates (including "not already said"), one bullet per fact under an existing heading, length judged by the fact not a word count, voice, and a conversational review gate before any write. No database. Reference implementation: the `Foleon - Cheat Sheet` Notion page, written by `foleon/foleon-cheatsheet`. |

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
  *rule in this standard* — there is no separate per-item ID namespace, since v2.0.0 removed the
  database that once needed one (a database row is a page; see `CHEAT_SHEET.md`'s v2.0.0 changelog
  entry).
