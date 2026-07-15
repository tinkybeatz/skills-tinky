---
name: "session-handover"
description: >
  Generates a handover.md file that captures the complete state of the current
  Claude Code session so a new session can pick up exactly where this one left off.
  A superior alternative to automatic compaction: the handover preserves decisions,
  the reasoning behind them, the dead ends, and the next steps — not just the most
  recent messages. Use this skill whenever the user says: "handover", "handoff",
  "do a handover", "prepare the handover", "prepare the handoff", "save session state",
  "save the session", "prepare next session", "prepare the next session",
  "before /clear", "before I clear", "before I compact", "before compaction",
  "create handover.md", "generate handover.md", "session bridge", "bridge the session",
  "I'm stopping the session", "I'm stopping here", "wrap up the session",
  "wrap up session", "summarize the session for Claude", "write a brief for the next
  Claude", "context dump", "session snapshot". Also trigger proactively when the user
  signals they are about to clear/compact/close and non-trivial work is in progress.
  Do NOT use it for a summary meant for a human (that's progress-report or
  sprint-review) nor to persist long-term memory (that's obsidian-memory or the native
  auto memory).
---

# Session Handover

You produce a `handover.md` optimized so that a **next Claude Code session** can resume the work without losing context. Not a summary for a human — a structured brief for an LLM.

A good handover is not a journal. It's a dense letter to a future you who has no memory of this session.

---

## Why this skill exists

Automatic compaction preserves the **recent messages**. It loses what actually matters for a clean resume:

- The **why** behind decisions made early in the session
- The **dead ends explored and abandoned** (otherwise the next session retries them)
- The **implicit constraints** the user mentioned in passing
- The **precise state** of work in progress (which line you're on, what verification is still pending)
- The **promises made** ("I'll rerun the tests after", "the CHANGELOG still needs updating")

A good handover preserves all of this. It is dense, structured, and **front-loaded**: the next session should be able to act after the first 30 lines.

---

## Operating modes

| Mode | Signal | What it produces |
|---|---|---|
| **Detailed** (default) | "do a handover", "handoff", "before I clear" | Complete `handover.md` (template `references/handover-template.md`) |
| **Minimal** | "quick handover", "TL;DR for next time" | TL;DR + Next steps only (5–15 lines) |
| **French** | conversation in French, "in French" | Same structure, French language |
| **Multi-goal** | several goals handled in the session | One Goal section with sub-sections, none omitted |

---

## When this skill adds value (and when it doesn't)

**Valuable for:**
- Before `/clear` or `/compact` when non-trivial work is in progress
- End of day, to resume cleanly tomorrow
- Handoff to another human (or to another Claude instance on a different machine)
- A session that has grown long and the user wants to restart fresh without losing state

**Useless (skip or ask for confirmation):**
- A 2–3 exchange trivial session — there's nothing to pass on
- A task already committed and documented in the commit message
- A one-off question (quick debug, lookup) with no state to carry forward

---

## Workflow

### Step 0 — Detect the session context

Before writing, scan what exists:

1. **`CLAUDE.md`** in the cwd and at the repo root — to understand the project and its conventions
2. **`memory/`** under `~/.claude/projects/.../memory/` — to pull relevant feedback / project memories (often referenced implicitly by the user)
3. **Git state** — branch, last commit, uncommitted files
4. **Background jobs still active** — listed via the harness notifications or recalled by the user
5. **Existing `handover.md`** in the cwd — if present, ask before overwriting (suffix as `handover-2.md` or timestamp as `handover-YYYY-MM-DD-HHMM.md`)

### Step 1 — Collect the objective state (parallelizable)

Run in a single batch of parallel tool calls:

```bash
pwd
git status
git log -5 --oneline
git diff --stat
git branch --show-current
```

If there's no git repo, omit the git sections of the handover (don't write "N/A").

### Step 2 — Reconstruct the subjective state

Reread the conversation and fill in:

| Category | What to capture |
|----------|-----------------|
| **Goal** | The user's macro objective — not the last micro-task |
| **Done** | What is finished AND verified (not just written) |
| **In progress** | The exact step you stopped at (file:line if possible) |
| **Pending** | What remains, in order |
| **Decisions + why** | Technical choices + the reason given by the user or discovered |
| **Hidden context** | Constraints, preferences, gotchas discovered in session — not in the code |
| **Dead ends** | Approaches tried that didn't work, and why |
| **Open questions** | What's awaiting a decision from the user |
| **Unkept promises** | "I'll do X after Y" that hasn't happened yet |

### Step 3 — Write `handover.md`

Default path: `./handover.md` (cwd). Use the template `references/handover-template.md` as the structure. An empty section → omit it (no "N/A").

### Step 4 — Deliver

Present to the user:

1. The absolute path of the file written
2. The **exact sentence** to paste into the new session:

   ```
   Read @handover.md and pick up from there.
   ```

3. If background jobs are still active: remind them explicitly, with their intent.

---

## Writing principles

- **Front-load.** The first 30 lines must be enough to act. The TL;DR is not optional.
- **Absolute paths.** Always. The next session doesn't know the implicit cwd.
- **Verbatim when it matters.** If the user said "don't touch X", quote it word for word.
- **No marketing.** No "great progress made". Facts only.
- **The why before the what.** "We chose PostgreSQL because X" > "We installed PostgreSQL".
- **Don't duplicate what git knows.** The git history is accessible. The handover captures what is *not* in git: intentions, decisions, conversational context.

---

## What NOT to include

- The full contents of edited files (the next session will reread them)
- Copies of `git log` or `git diff` (the next session will run them)
- Complete code (just: "edited `auth.ts:42`, to do X")
- Narrative summaries ("we started with..., then...")
- Trivial information the system already surfaces at startup (date, OS, etc.)
- **Secrets** (tokens, API keys, passwords) — replace with `<REDACTED>` and note "secret mentioned, re-ask the user if needed"

---

## Anti-patterns to avoid

| Anti-pattern | Why it's bad | Replace with |
|---|---|---|
| "Continue the work already started" | No information | "Step 3/5 of the auth.ts refactor — the tests `auth.test.ts:120-180` still need updating" |
| File list with no context | Not actionable | File + line + intent |
| Copying the conversation | Reintroduces the noise you wanted to avoid | A structured synthesis |
| Generic "TODO" items | The next session will rediscover them badly | Ordered, concrete steps |
| Forgetting half-kept promises | The #1 source of drift between sessions | A dedicated "Unkept promises" section |

---

## Failure modes and recovery

| Failure | Recovery |
|---------|----------|
| Very short session, almost nothing done | Ask: "The session is short (X exchanges). Do you still want a handover?" |
| cwd is not a git repo | Omit the git sections, keep the rest |
| Background jobs still active | Dedicated "Background jobs still active" section with ID, purpose, and an instruction to check their state at the start of the next session |
| Multiple goals in parallel | Goal section with sub-sections, don't forget any |
| Existing `handover.md` | Always ask before overwriting (otherwise suffix or timestamp) |
| Secrets quoted by the user during the session | NEVER write them — `<REDACTED>` + a note to re-ask |
| No clear macro objective | Ask the user for a one-sentence objective before generating |
| Very long conversation exceeding the context | Prioritize: (1) current state, (2) decisions made early in the session, (3) dead ends. The intermediate narrative is disposable |
| The user says "quick handover" | Minimal mode: TL;DR + Next steps only |

---

## References

- Full template: `references/handover-template.md`
- Closely related skills (do NOT confuse):
  - `progress-report` — report for a human (client/team), not for Claude
  - `sprint-review` — technical recap with recommendations, agile format
  - `obsidian-memory` — long-term persistence in a vault, not a session bridge
  - native `auto memory` — persistent knowledge about the user, not a session snapshot
