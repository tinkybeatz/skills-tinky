---
name: feature-pm
description: >-
  Spins up a dedicated PM session for ONE fio feature: writes the feature's brief from the
  current PM session's context, opens a new herdr tab named after the feature, starts Claude
  Code in it as `pm-<slug>`, and hands it the brief. The new PM runs the same parallel-dev loop
  (fio's CLAUDE.md + CLAUDE.local.md) but only for that feature, with its own decisions and
  agenda under `docs/roadmap/features/<slug>/`. For bigger, experimental work (a whole feature's
  discussion and experimentation), not one ticket. Explicit invocation only: `/feature-pm`
  followed by a free-text description of the feature. Requires running inside herdr
  (HERDR_ENV=1) and the fio repo.
disable-model-invocation: true
user-invokable: true
---

# feature-pm

Gaël types `/feature-pm <what the feature is about>`. You are the **main PM** (the session it
was typed in). You write a brief, open a herdr tab, start a new Claude PM in it, and hand over.
The new session is the **feature PM**: one feature, its own context, same loop rules.

Explicit invocation only. Never run this because a message mentions a feature or a new topic.

## Preconditions

- `test "${HERDR_ENV:-}" = 1`. If not, say "not running inside herdr" and stop.
- The fio main checkout is `/Users/gaeldelouis/Documents/GAEL/FOLEON-DEV/fio`. The feature PM
  starts there, never in a worktree.
- `docs/roadmap/` is local and gitignored there. Feature folders live under it and are never
  committed.

## 1. Name it

Derive a slug from Gaël's text: kebab-case, 3-24 chars, `[a-z][a-z0-9-]*`, the feature's noun
("realtime-collab", "brand-kit-export"). The herdr agent name is `pm-<slug>` (must match
`[a-z][a-z0-9_-]{0,31}`). If `docs/roadmap/features/<slug>/` already exists, or
`herdr agent list` shows `pm-<slug>`, stop and tell Gaël: a PM for it already exists.

Don't ask Gaël to confirm the name. Say it in the final report.

## 2. Write the brief

Create `docs/roadmap/features/<slug>/` with three files:

- `brief.md` from [`references/brief-template.md`](references/brief-template.md). Fill every
  section from what this session knows, `docs/roadmap/decisions.md`, `agenda.md`, the
  roadmap docs and Jira. Gaël's words go in **The ask verbatim**. If a section has nothing, write
  "none known yet", never leave it out. Cite paths, ticket keys and PR numbers; no essays.
- `decisions.md`: a heading and one line, "Rulings for <slug>. Newest last."
- `agenda.md`: a heading, plus any open questions you already know.

If the context needed is more than you hold, dispatch ONE read-only Explore agent to gather it
(code areas, related tickets). Never more: the machine crashes on memory.

**RD block.** Reserve 5 ids for the feature PM from the free part of RD-300-399: check
`docs/roadmap/ripley-deviations.md` on origin/main, every open PR body, and every other
`docs/roadmap/features/*/brief.md`. Write the block into the brief. Allocate nothing else.

## 3. Launch

Run [`scripts/launch.sh`](scripts/launch.sh) `<slug>`. It:

1. creates a tab in the caller's workspace (`--cwd` fio, `--label <slug>`, `--no-focus`);
2. starts `claude` in its root pane as `pm-<slug>` (`-n "PM <slug>"`, Opus);
3. sends the kickoff prompt pointing at the brief;
4. prints the tab id and the pane id.

If it fails, report the herdr error verbatim and stop. Never retry by creating a second tab;
close the half-made one with `herdr tab close <tab_id>` first.

## 4. Book it, report it

- Append to the main `docs/roadmap/agenda.md`:
  `- <date> · Feature PM pm-<slug> launched (tab <tab_id>). Brief: docs/roadmap/features/<slug>/brief.md.`
- Report to Gaël in three lines: the tab label, the agent name, and the brief path.
  Nothing else.

## Talking between PMs

- Main → feature: `herdr agent prompt pm-<slug> "<text>"`.
- Feature → Gaël: in its own tab. It never writes the main `decisions.md` or `agenda.md`;
  a ruling that affects other work goes to Gaël in one line, and the main PM records it.

## Failure modes

- **Two PMs, one machine.** Each feature PM dispatches agents the others can't see. The brief
  caps it at one heavy job (dev agent, test agent, browser tests, push hook) at a time and a
  `memory_pressure` check (>= 25 % free) before every dispatch. Never relax that in a brief.
- **Scope bleed.** A feature PM touching tickets or PRs outside its feature. The brief names
  what's in; everything else is out, including other feature PMs' work.
- **RD collisions.** Two PMs allocating the same id. Only the reserved block is theirs.
- **Duplicate tab.** A failed launch retried by hand leaves two tabs. Close before retrying.
- **Stale brief.** The brief is a snapshot. The feature PM's own `decisions.md` overrides it.
