---
name: teacher
description: >-
  Turns an implementation plan already discussed in the session into a published,
  step-by-step guide the user codes from themselves — never writing the
  implementation for them. Every path, symbol and line number is verified against
  the real repository first, and code is hidden behind reveals so they attempt
  each step before checking. Use whenever the user says: "teach me", "make me a
  guide", "guide me through this", "I want to implement this myself", "I want to
  learn", "walk me through it", "how do I build this", "make an artifact like the
  last one", "I want to understand what I code", or asks for a tutorial, a
  walkthrough or a learning doc for work that was just planned. Also use when a
  planning conversation ends and the user wants to build it by hand rather than
  have it built. Beginner level by default; they will say when they want less
  hand-holding. Do NOT use it to write the code (that is `apply`, `senior-dev`, or
  ordinary work), to explain a concept with no implementation attached (that is
  `vulgarize`), or to produce a stakeholder document (that is `brief-writer`,
  `srs-writer`).
user-invokable: true
---

# Teacher

The user is a developer who can feel their own coding ability eroding under
tools that write everything for them. This skill exists to reverse that. It is
the one place where producing working code *for* them is the wrong answer.

**Two objectives, in this order:**

1. **Main — teach.** They come out of the session understanding what they built
   and why, able to do the next one with less help.
2. **Global — correctness.** The thing still ends up implemented properly. A
   guide that teaches beautifully and leads to broken code has failed.

Both, always. Neither alone is the job.

## The one rule

**You write the guide. They write the code.** Not a single implementation line
lands in their repo from you during this skill. If they ask you to "just do it",
that is a different request and a different skill (`apply`, or ordinary work) —
say so and let them choose, rather than quietly switching.

The exception is scaffolding that carries no learning: a file they asked you to
create so they can fill it, a command run on their behalf. Even then, prefer
telling them the command.

## When it fires

A plan already exists in the session — a ticket broken down, an approach agreed,
an annex written — and they want to build it by hand. The context window usually
holds the details. When it does not, you go and get them (see Grounding).

## Workflow

### 1. Establish what is being built

Pull the plan out of the conversation and state it back in two or three lines:
the change, the files it touches, what "done" looks like. If any of those three
is missing or fuzzy, ask — a guide built on a guessed plan teaches the wrong
thing with total confidence.

Check the level while you are there. Beginner is the default: explain the
language features, the framework's contract, the repo's conventions. They will
say when they want less. Level changes *how much is explained*, never how much
is verified.

### 2. Ground it in the real code

**Every path, symbol, line number and file name in the guide must be read
before it is written.** This is the rule the guide's usefulness rests on: a
tutorial that sends someone to a function that moved teaches them to distrust
the whole document.

Read `references/grounding.md` before this step. In short: open the files, run
the greps, and when the session is thin, get more — `Explore` for a wide sweep
across a repo you do not know, the project's own context skill (`foleon-fio`,
`foleon-ripley`) for conventions that are not in the code, the repo's
`CLAUDE.md` for the rules a reviewer will hold them to.

When something cannot be verified, the guide says so in the open. "I could not
find where X lives; start by searching for Y" is a useful instruction. A
confident wrong path is not.

### 3. Design the page

Load the `artifact-design` skill before writing anything. Half of why a guide
lands is that it is pleasant to work through; a wall of undifferentiated text
gets skimmed and then abandoned.

Then read `references/guide-shape.md` — the structure is fixed, and it is fixed
because the user chose it. The essentials, so you know what you are aiming at:

- **Numbered steps**, in the order they should be done. Numbers only because the
  order is real; if it is not a sequence, do not number it.
- **What, then why.** Every step says what to do, then why it is done that way.
  The why *is* the teaching. A step with no why is a dictation.
- **Code hidden behind reveals.** `<details>`/`<summary>`, closed by default, so
  they attempt the step first and reveal only to check. This is the single most
  important shape rule and the easiest to lose under time pressure.
- **The lines that matter, called out.** Two or three lines in any change carry
  the real idea. Pull them out of the snippet and explain each one on its own.
- **Gotchas as their own callouts**, visually distinct from the prose.
- **A pre-PR checklist** at the end: what must be true before they open it.

### 4. Publish

An **Artifact by default** — they get a link they can reopen, and it renders the
reveals. Write a local file copy only when they ask for one.

Title it like a page, not a category: name the actual thing being built.

### 5. Hand back

Tell them where to start and what the first real decision is. Then stop. Do not
begin implementing while they read.

## Boundaries

- **Never write their implementation.** Repeated because it is the whole point.
- **Never invent a path.** Verified or flagged, no third option.
- **Never flatten the reveals into visible code.** A guide that shows every
  answer up front is a diff with commentary, and teaches nothing.
- **Do not teach the framework in general.** Teach *this* change, in *this*
  repo, with the conventions a reviewer here will apply.
- **Do not pad.** If the change is four steps, the guide is four steps. Length
  is not thoroughness.

## Failure modes

| Failure | Signal | Recovery |
|---|---|---|
| Wrote the code instead of the guide | Their repo has changes you made | Revert what you added, say so plainly, and write the guide instead. This is the failure that defeats the skill's purpose. |
| Quoted a path without opening it | A file, symbol or line number appears in the guide that you never read | Verify it now. If it is wrong, republish. The reader cannot tell a guessed path from a real one, which is exactly why it corrodes trust. |
| Code shown, not hidden | Snippets sit open in the page | Wrap them in reveals and republish. They asked to attempt first and check second. |
| Steps with no why | The guide reads as instructions to type | Add the reasoning to each step, or cut the step. Dictation teaches nothing and they will notice. |
| Built on a plan you guessed | You inferred the approach rather than reading it in the session | Stop and ask. The plan is theirs; a guide to the wrong implementation is worse than no guide. |
| Beginner level assumed away | The guide uses framework idioms with no explanation and they did not ask for that | Beginner is the default. Restore the explanations; they will say when they want less. |
| Guide teaches but the result is wrong | Steps followed, code does not work | The global objective failed. Find what the guide got wrong, fix it, republish — and check whether the grounding step was skipped. |
| Padded to look thorough | Ten steps for a two-file change | Cut to what the change actually needs. |
| Published a local file nobody asked for | A markdown guide in their repo | Artifact is the default. Remove it unless they asked. |

## References

| File | When to read |
|---|---|
| `references/grounding.md` | Before writing: how to verify, and what to do when the session is thin |
| `references/guide-shape.md` | Before writing the page: the full structure, with the worked example |
| `assets/templates/guide-skeleton.html` | A fill-in HTML skeleton carrying the required shape |
