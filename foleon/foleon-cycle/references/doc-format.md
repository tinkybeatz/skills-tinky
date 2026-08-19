# Doc format — the exact skeleton

CYC-2 fixes this shape so a hook, a script, and a human can all read the same file without a parser.
`python3 scripts/cycle.py validate` enforces everything mechanical here.

## Skeleton

```markdown
# Cycle 2026-C4
Dates: 2026-08-18 → 2026-09-26 · Status: active

## [fio] PDF export
Outcome: A reader can download the doc as a PDF that matches the on-screen layout.
Appetite: 2w (fixed) · First cut: nested-table layout → flatten to single level
No-gos: no print-stylesheet editor, no per-block overrides
Done when: merged to main and demoed to design
Open questions: does ripley's export share the extraction path?

### scope: extraction pipeline — downhill
- [x] walk the doc tree into blocks
- [ ] map blocks to PDF primitives
- [ ] ~ warn on unsupported block

### scope: table pagination — uphill
(no tasks yet — the approach isn't known)

## [ripley] search relevance
Outcome: Searching a doc title ranks that doc first.
Appetite: 3d (fixed) · First cut: fuzzy matching → exact title only
No-gos: no new index
Done when: merged

### scope: title boost — top

## Dev log
- 2026-08-19 [fio] extraction pipeline → block walker done; tables need their own layout pass
- 2026-08-20 [fio] table pagination → deferred nested cells to a `~` task — appetite holds
```

## Line grammar

| Element | Exact form |
|---|---|
| Header | `# Cycle <id>` on line 1; `Dates: <dev start> → <dev end> · Cooldown: → <cycle end> · Status: active\|closed` on line 2. The range is the **6-week dev window**; cooldown is recorded but never tracked (CYC-2) |
| Topic | `## [<repo>] <name>` — two tags for a cross-repo topic: `## [fio][ripley] <name>` |
| Fields | `Outcome:` `Appetite:` `No-gos:` `Done when:` — all four required; `Open questions:` when there are any; `Shipped:` / `Cut:` added at close |
| Scope | `### scope: <name> — <hill>` (em dash or hyphen both parse) |
| Task | `- [ ] <text>` / `- [x] <text>`; nice-to-have: `- [ ] ~ <text>`; personal (not Jira): `- [ ] self: <text>` |
| Log line | `- <YYYY-MM-DD> [<repo>] <scope> → <what changed>` |

Order is fixed: header, then topics, then exactly one `## Dev log` — **nothing after the log.**

## The four hill values

| Value | Means |
|---|---|
| `uphill` | Still figuring out the approach; unknowns unresolved |
| `top` | Approach known, all remaining work visible; nothing built yet |
| `downhill` | Executing known work |
| `done` | Every must-have complete (open `~` tasks are fine) |

The hill measures **knowledge, not output**. `top` is the pivot — the first moment an estimate would
even be meaningful. Set only from what the maintainer says; a scope moving back to `uphill` is normal
and must never be "corrected" or averaged (CYC-6).

**No percentages anywhere.** `validate` fails on any `\d%` — the hill exists precisely because
task-count and percentage status can't show uncertainty.

## Tasks

- Exactly one scope per task. A task at topic level is a validation error.
- Half a day to two days. Bigger is a scope; smaller isn't worth tracking.
- **Two kinds.** Unmarked = implementation, becomes a Jira ticket. `self:` = yours alone (research,
  conceptualising) and never a ticket — its outcome is usually *producing* the tickets (CYC-7).
- **Must-have by default.** `~` marks a nice-to-have: it never blocks `done`, and marking it **is**
  the scope-hammering action — so it earns a dev-log line as a *decision*.
- A scope may legitimately have **no tasks** — it marks work known to be needed whose steps aren't
  discovered yet. Write `(no tasks yet — …)` as plain text so the section isn't empty.

## Dev log

One line, dated, tagged `[repo]`, naming the scope, stating **the outcome not the activity**:

- ✅ `- 2026-08-19 [fio] extraction pipeline → nested tables need their own layout pass`
- ❌ `- 2026-08-19 [fio] extraction pipeline → worked on tables, ~60% done`

Append-only within a cycle: correct an earlier line by appending a new one, never by editing history.
`cycle.py log` rejects the banned openers (`worked on`, `continued`, `WIP`, `misc`, …) and any
percentage.

## Validation

```bash
python3 scripts/cycle.py validate          # active cycle
python3 scripts/cycle.py validate --id 2026-C4
```

Every failure names the rule it breaks (`CYC-4: appetite must be marked "(fixed)"`), so a fix is
mechanical. Run it after any hand-edit — the model edits the markdown directly, and this is the
backstop that catches a malformed hill value or a task that drifted out of its scope.
