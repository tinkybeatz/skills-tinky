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
| Topic | `## [<repo>] <name> — shaping\|shaped` — the state is required (CYC-3). Two tags for a cross-repo topic: `## [fio][ripley] <name> — shaped` |
| Fields | **shaped**: `Outcome:` `Appetite:` `No-gos:` `Done when:` all required. **shaping**: only `Appetite:` (may be `(provisional)`) and `Open questions:`; `Open questions:` when there are any; `Shipped:` / `Cut:` added at close |
| Scope | `### scope: <name> — <hill>` (em dash or hyphen both parse) |
| Task | `- [ ] <text>` / `- [x] <text>`; nice-to-have: `- [ ] ~ <text>`; personal (not Jira): `- [ ] self: <text>`. A completed `self:` task carries `→ answer: <…>` at the end of its text (CYC-7). Under one scope, `self:` tasks come first and the two kinds stay contiguous — the mirror renders the kind as a group label and preserves this order (CYC-15b) |
| Jira key | `- [ ] <text> [<KEY>]`, or `- [ ] <text> [<KEY> · <Status>]` once synced — at the **end** of the task line, never elsewhere on it (CYC-18). Only on a Jira-bound task: a `self:` task carrying one is a validation error, as is the same key on two tasks |
| Annex | `Annex: <label> → <url>`, several separated by ` · `. Optional, topic level. Links a supporting document — a ticket write-up, a question list — that is too long to live in the topic |
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
- **A `self:` task records its answer when it closes** — append `→ answer: <what was decided or found
  out>` to the task text (CYC-7). The task is the question; ticking it silently throws away the only
  thing it produced. The dev-log line still goes in where CYC-8 admits one: the log is chronological,
  the inline answer is findable from the question.
- **Must-have by default.** `~` marks a nice-to-have: it never blocks `done`, and marking it **is**
  the scope-hammering action — so it earns a dev-log line as a *decision*.
- **A task that exists in Jira carries its key**, and from that point Jira owns its title and its
  checkbox — the doc keeps the scope, hill, appetite, `~` mark and ordering (CYC-18). The key, not
  the title, is the identity: the maintainer rewords tickets on the way into Jira, and a title match
  would break exactly there. Completion is read from Jira's `statusCategory`, never a status name.
  Link with `cycle.py jira link`, refresh with `cycle.py jira sync`; see
  [`jira.md`](jira.md). **Nothing writes to Jira, ever.**
- A scope may legitimately have **no tasks** — it marks work known to be needed whose steps aren't
  discovered yet. Write `(no tasks yet — …)` as plain text so the section isn't empty.

## Annexes

A topic may need a supporting document that has no business inside the cycle doc: a ticket write-up
with a section per ticket, a list of questions for a call, a piece of research. Those are referenced
with an `Annex:` line on the topic — and, since CYC-16, they are **generated pages like every other**,
not hand-written in Notion.

**A shaped topic with at least one Jira-bound task must have one.** Its tickets otherwise reach Jira
with no write-up behind them, and CYC-17's slots never apply to them. A shaping topic needs no annex:
it holds only `self:` tasks, so there is nothing to write up.

**The content lives in a local sidecar** next to the cycle doc:

```
SHAPEUP-CYCLES/
  Cycle-11.md                                              <- the cycle doc
  Cycle-11.annex.tickets-to-write-shape-1-gtm-plumbing.md  <- the annex, authoritative
```

The filename's slug is derived from the label, so the label in the `Annex:` line is the identity.
Renaming it orphans the sidecar — reported loudly by `validate`, never silently duplicated.

```markdown
# Annex: Tickets to write — Shape 1 (GTM plumbing)
Cycle: Cycle-11 · Topic: GTM analytics — plumbing

## What this is
Shared background, once. Never repeated per ticket.

## Build the "send an event" call
Task: the track() call and its typed event contract, with a recording transport for tests
### Jira ticket name: Add the editor's analytics track() call and typed event contract
**Expected outcome** — …
**Environment** — …
**Build constraints** — what the implementation must respect, and what each one buys.
- … — what it buys
- … — what it buys
**Open questions** — …
**Done when** — …
**Criteria** — … · … · …
**Lives under** — …
**Expected testing** — …
**As built** — where the build diverged from the constraints above, and what each divergence changes.
- **dropped** · … — …
```

**The body is nine named slots in a fixed order (CYC-17)**, not free prose. Required:
`Expected outcome`, `Done when`, `Criteria` and `Expected testing` — the last one even when the
answer is the literal `none`. Conditional: `Environment`, `Build constraints`, `Open questions`,
`Lives under`, `As built`, each **omitted** when it does not apply rather than left as an empty
header. `Build constraints` and `As built` are bullet lists under their fixed glosses, quoted
verbatim; the rest are inline.

`As built` is the only slot written **after** the code, and it is never written by hand: it comes from
a ticket's comments, reduced by `cycle.py deviations add` to a verdict, the write-up line it
contradicts and what actually happened (CYC-19, [`deviations.md`](deviations.md)). The rest of the
section is never rewritten to match it.
Order is enforced. The full contract — the gloss, the ban on the old "what to build" bullet list, and
the ban on pointing at another ticket by position — is in [`tickets.md`](tickets.md).

- A section is **ticket-bound** when its first line is `Task: <the task text, verbatim from the cycle
  doc>`. That quote is the link between the two files, which is why it has to match exactly.
- **Every Jira-bound task in the topic needs exactly one section.** Missing, orphaned or duplicated —
  all three fail `cycle.py validate` on the *cycle doc*, so adding a ticket makes the doc
  non-conforming until the annex accounts for it. That is the enforcement, and it is the point.
- A ticket-bound section also carries a **proposed Jira ticket name**. The heading is for whoever
  reads this page; the Jira summary is read in a list of forty with none of it around, so it is
  written separately and never defaulted to the heading. It is a proposal — accept it or rewrite it,
  the way scope names work.
- Sections with no `Task:` line — background, an ordering note — are free-form.

```bash
python3 scripts/cycle.py annex list     # coverage per annex: what is missing, orphaned, still a stub
python3 scripts/cycle.py annex sync     # create the sidecar, stub every uncovered ticket
python3 scripts/cycle.py annex render   # the Notion body, backlink derived from mirror.json
```

**`sync` writes structure; you write the words.** The stub it inserts is deliberately unpublishable —
`annex render` refuses while any section still holds one. A generated write-up would be exactly the
filler CYC-14 bans acceptance criteria for: it reads finished and tests nothing. Read the code, then
write it.

The mirror renders each annex as a grey link directly under the topic's last scope, which is the
point on the page where the reader has just read the task lines and wants the detail behind them.

**The annex page is never read back.** It has no writable surface, so CYC-10's three-way merge does
not apply and a Notion-side edit to one is lost on the next render — the rendered page says so in its
own header. Edit the sidecar.

**Where the page lives** is the `Cycle <n> - Annexes` home under the cycle's own page in Notion; a
generated annex goes there as a row with a `Status`. Never create one as a parentless page — Notion
files those under the maintainer's private area, which is theirs, not a place for generated output.

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
