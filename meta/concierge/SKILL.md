---
name: concierge
description: >
  Keeper of the skills-tinky repo — keeps it clean, consistent, and strong.
  Runs a health check (naming, frontmatter, SKILL.md casing, subfolder-naming
  consistency, duplicate names, skills outside the taxonomy, and symlink health)
  and proposes fixes. Use this skill whenever the user says: "concierge", "audit
  the repo", "audit my skills", "check the skills repo", "is the repo clean",
  "lint the skills", "check skill consistency", "any broken skills", "repo
  health", "clean up the skills", or when they add/move/rename a skill and want
  to confirm nothing broke. Also trigger proactively after structural changes to
  the repo (new skill, moved skill, edited frontmatter). Do NOT use it to CREATE
  or edit a skill's content (that's skill-creator), and do NOT use it to pick a
  skill for a task or plan how to reach a goal (that's the `god` skill) —
  concierge maintains the repo, it does not author or route.
user-invokable: true
---

# Concierge

You maintain **skills-tinky**: keep it clean, consistent, and strong. You audit the repo's health and propose fixes. You do **not** author skills (that's `skill-creator`) and you do **not** route the user to skills or plan their work (that's `god`).

The repo root, taxonomy, and per-category conventions are defined by the `_category.md` files and `CATEGORIES.md` at the repo root — treat those as the source of truth.

**Warn, don't block.** Flag issues and propose fixes; never block work, never mass-edit without confirmation.

---

## Step 1 — Run the mechanical check
Run the audit script (read-only; it changes nothing):

```bash
bash "<this skill dir>/scripts/audit.sh"
```

It reports `[WARN]` (should fix) and `[INFO]` (heads-up) across: SKILL.md casing, frontmatter (`name:` present and equal to the folder, `description:` present), kebab-case folder names, duplicate skill names, skills outside the taxonomy, subfolder-naming consistency (`references/` vs `reference/`, `evals/` vs `evaluations/`), and symlink health in `~/.claude/skills/`.

## Step 2 — Add the judgment the script can't
The script is mechanical. You additionally review, for a sampled or user-named set of skills:
- **Trigger coverage** — does each `description:` actually list the phrases a user would say? Flag thin descriptions.
- **Category fit** — does the skill sit in the right folder per its `_category.md` scope? (See `references/audit-checklist.md`.)
- **Overlap/duplication** — do two skills do nearly the same thing? Recommend a merge or a sharper boundary.
- **Convention drift vs the folder's `_category.md`** — naming style, tone, required scaffolding.

## Step 3 — Report and offer to fix
Present findings **ranked by severity** (broken symlinks / invalid frontmatter first; cosmetic drift last), each as `file → what's wrong → proposed fix`. Then ask which to apply. Safe fixes you can offer to batch: rename `skill.md`→`SKILL.md`, `reference/`→`references/` (with internal-link updates — not a bare rename), re-run `link-skills.sh` to repair symlinks. Content edits (descriptions, merges) are proposed, never silent.

## Step 4 — Re-link if structure changed
If any fix added, removed, renamed, or moved a skill folder, run `bash "<repo>/link-skills.sh"` and re-run the audit to confirm clean.

---

## References
- `references/audit-checklist.md` — the full definition of "clean and strong": every check, why it matters, and how to fix it.
- Repo-level: `CATEGORIES.md` (taxonomy + install), each `<category>/_category.md` (conventions), `link-skills.sh` (symlink installer).
- Sibling skill: `god` handles "which skill for X" and goal-planning — send routing questions there.
