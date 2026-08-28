# Jira — the tracker owns the ticket, the doc owns the plan

Governed by **CYC-18**. Read this when a ticket has been created in Jira, when a task's status looks
stale, or before writing anything that touches a Jira key.

## The one rule that is not negotiable

**You never write to Jira.** No ticket creation, no field edit, no transition, no comment, no matter
who asks or how the request is phrased. The maintainer writes every ticket themselves, in the words
they want it to have.

This is not a promise you are keeping — it is how the system is built, in two independent layers:

1. `cycle.py` has no network access at all. It reads fetched issues from a **local file** that someone
   else produced.
2. The Atlassian connector is authorised with read scopes only (`read:jira-work` plus Confluence
   reads). No create, edit, transition or comment tool is exposed, so there is nothing to call.

If either layer ever changes — a write tool appears in the connector's tool list, or someone proposes
giving `cycle.py` a network client — say so out loud before doing anything else. The guarantee is the
feature.

## The workflow this fits into

The maintainer's own description, and the shape everything below assumes:

> Cycle planning creates tickets → I read them in the Notion annex → I add them on Jira (the way I
> want them to be on Jira) → once on Jira, I give the ticket URL to Claude Code → Claude re-updates
> the whole cycle doc + annex → Jira becomes the source of truth for what is related to tickets.

So the annex is a **proposal**. What lands in Jira is the maintainer's edit of that proposal, and from
the moment it lands, the tracker wins.

## What Jira owns, and what it does not

| Jira owns | The cycle doc owns |
|---|---|
| The ticket's **title** | The **scope** the task sits under |
| Its **completion state** | The **hill position** (CYC-6 — a human sets it, always) |
| Its **status** (`To Do`, `Doing`, `Review`, `QA`, …) | The **appetite** and first cut (CYC-4) |
| | The `~` **nice-to-have** mark (CYC-7) |
| | The **ordering** of the work |

Nothing else is mirrored. Assignee, sprint, links, parent and subtask structure are all deliberately
left in Jira: the cycle doc has no field that would show them, and syncing data nothing reads is how a
sync acquires maintenance cost for no benefit.

## Completion comes from `statusCategory`, never a status name

Jira fixes exactly three status categories across every site: `new`, `indeterminate`, `done`. Status
**names** are per-project — the maintainer's own board carries `To Do`, `Doing`, `Review`, `QA` and
`Done`, plus `Funnel` on the epic workflow — so a name test breaks on any project that renames a
column, and breaks in the worst direction: reporting unfinished work as finished.

The checkbox ticks when, and only when, `statusCategory.key == "done"`. The status **name** is cached
on the line and shown in `status` and the mirror, because *2 in Review* and *2 not started* are the
same checkbox count and a completely different Wednesday.

## The line format

```
- [ ] Send editor analytics events to the GTM dataLayer [PROD-4357 · To Do]
```

The key sits at the **end of the line**, and it is the task's identity from then on. That is the point:
the maintainer rewords tickets on the way into Jira, and matching on the title would break exactly
when it matters. The status beside it is a cache of what the last sync read, stored so the doc renders
correctly offline.

A `self:` task can never carry a key — research and decisions do not become tickets (CYC-7), and
`validate` rejects it.

The site prefix for the ticket links is **learned, not configured**: the first `jira link` records the
`https://<site>/browse` part of the URL you passed into `<cycle home>/.state/jira.json`, and never
overwrites it. Before any URL has been seen the table renders the key as plain text — a missing link
is a smaller failure than a guessed one pointing at the wrong site.

## The three commands

```bash
python3 scripts/cycle.py jira list                 # what is linked, what is not, and its status
python3 scripts/cycle.py jira link --url <ticket-url> --task "<enough of the task text>"
python3 scripts/cycle.py jira sync --from <file>   # apply a payload you fetched
```

**`link`** records the key. It is a separate step from syncing on purpose: it is the only moment the
maintainer asserts *this local task and that Jira ticket are the same work*. Never infer that from a
title match — pass `--task` a fragment, and if it matches more than one task the command lists the
candidates and stops rather than guessing.

**`sync`** takes a file. Fetch the issues yourself (`searchJiraIssuesUsingJql` with
`key in (…)`, fields `summary` and `status`), save the payload, then point `sync` at it. It accepts
Jira's raw REST shape verbatim as well as a flat `{"issues": [{"key", "summary", "status",
"statusCategory"}]}` — paste what the fetch gave you rather than transcribing it, because a
transcription step is a transcription bug.

`sync` reports what it could not resolve and does not guess: a key on a task but absent from the
payload, and a key in the payload on no task. Neither is an error — syncing a subset is normal.

## When Jira renames a ticket

`sync` rewrites **both** the task line and the `Task:` line of the annex section covering it. CYC-16
identifies an annex section by the task text it quotes, so updating only one would orphan the write-up
and fail validation on the maintainer's next command — for a rename they made in a different tool.

The section's **body** is never touched. The write-up is the maintainer's, or was written by an agent
that read the code (CYC-14); nothing here regenerates it.

## Notion, after a key exists

A keyed task leaves the checkbox list and renders as a **table row** — key first (linked to the
ticket), then a coloured status, then the summary. Three reasons, and they compound: the checkbox
would do nothing, because Jira owns completion; the key is what a reader copies into Jira or a branch
name, so it belongs at the front rather than trailing a title that may have wrapped; and a status is
worth a colour, which CYC-15 forbids on any line parsed back out of Notion but permits in a table
cell, since nothing reads one.

The colour comes from `statusCategory` under NST-3's workspace mapping — `new` grey, `indeterminate`
blue, `done` green — never from the status name, for the same reason completion is not.

A keyed task's state in Notion is **rendered from Jira and no longer read back**. `reconcile`
reports a Notion-side tick on a keyed task and ignores it, which is the whole payoff: the maintainer
stops maintaining the same status in two places.

Unkeyed tasks — every `self:` task, and any ticket work not yet in Jira — reconcile from Notion
exactly as before.

## The annex page, after a key exists

A ticket-bound section renders the live ticket — key, status, real summary — **in place of** its
proposed `### Jira ticket name:` line. That line is the summary to paste into the tracker; once the
ticket exists the proposal is spent, and the reader wants the key to open, the state it is in, and
the title it actually got, which is rarely the one proposed. The sidecar keeps the proposal
untouched — it is the source of truth, and this is only its rendering.

## Failure modes

| Failure | Signal | Recovery |
|---|---|---|
| Wrote to Jira | Any ticket, field, transition or comment changed by you | The worst failure in this file. Say so plainly and immediately; the maintainer needs to check what changed, because nothing in the system was supposed to make it possible. |
| Guessed which task a key belongs to | A key linked without the maintainer naming the task | Unlink it. The rewording is the whole reason the key exists; a title match is confident and wrong. |
| Read completion from a status name | A `QA` or `Review` ticket showing as done | Read `statusCategory`. A name test is wrong on any board that renamed a column. |
| Synced without fetching | Status refreshed from memory of an earlier fetch | Fetch again. A cached status presented as current is a wrong number that looks like a right one. |
| Task text edited locally on a keyed task | Doc title differs from the ticket | Jira owns it (CYC-18). Change it in Jira, then `sync`. |
| Annex left behind after a rename | `validate` reports an orphaned section | `sync` handles this; if it was renamed by hand, fix the `Task:` line to match the task. |
| Mirrored a keyed task as writable | Notion tick applied to a keyed task | `reconcile` refuses this by construction. If it happened, the key was missing from the line. |
