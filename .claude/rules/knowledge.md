# skills-tinky — project knowledge (discoveries log)

Append non-obvious findings here as you learn them: gotchas, implicit conventions,
architectural "why"s, sharp edges. Keep entries short and dated. When this file grows
heavy, run `/claude-md-architect` (refactor mode) to promote stable facts into the
root `CLAUDE.md` and prune the rest.

Format: `- YYYY-MM-DD — <finding>`

## Discoveries
- 2026-08-20 — **`shaping_overrun` measures elapsed days from the *cycle start*, not from when a
  topic entered shaping — so it is permanently on for short appetites.** A quarter of a 1w appetite
  is 1.75 days, so a `shaping` topic warns from day 2 of an 8-week cycle and never stops; by the
  end of week 1 every topic warns. The doc records no "entered shaping" date, so this cannot be
  fixed without a new field. It is harmless in `cycle.py status` (asked for, read in context) and
  becomes wallpaper the moment anything surfaces it unsolicited — which is why
  `cycle-queue-check.py` gates it behind a one-shot marker per topic. General rule: an always-on
  nudge doesn't just get ignored, it drags the useful nudge in the same hook down with it.
- 2026-08-20 — **Notion rewrites content on the way out, and `foleon-cycle`'s reconcile reads task
  text back as authoritative — so any Notion-side rewrite is a silent local corruption.** It
  autolinks anything domain-shaped (`gtm.md` → `[gtm.md](http://gtm.md)`) and escapes metacharacters
  (`~` → `\~`). `difflib.get_close_matches` at 0.8 then matches the autolinked line to the original
  and reconcile applies it as a *retitle*. Fixed with `unautolink()` in `parse_mirror_tasks`, which
  unwraps only links whose URL is the link text plus a scheme. The general rule: normalise on the
  read, never in the merge — and never style anything the parser reads back (CYC-15), since a
  `{color=}` on a to-do line is swallowed into the task's text the same way.
- 2026-08-12 — `cheatsheet-queue-append.py` must ignore its own bookkeeping. Marking a
  ripley finding `sheet: no` is a write to `knowledge.md`, so it re-queued the finding
  that was just rejected — and since the Stop hook nudges on any non-empty queue, every
  rejection re-armed the nudge next session. Fixed by comparing the Edit's
  `old_string`/`new_string` (a `sheet:`-only delta is skipped); the git diff can't be
  used for this, as it is taken against HEAD and still carries every uncommitted finding.
- 2026-07-20 — This repo is the home of the **project-awareness system**: the
  SessionStart hook lives in `hooks/session-claude-md-check.sh` and is wired from the
  user's global `~/.claude/settings.json`. Docs in `README.md` → "Project awareness".
