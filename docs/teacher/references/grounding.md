# Grounding

The guide's whole value is that its instructions are true of the repository the
reader is sitting in. Everything here serves one rule.

## The rule

**Read it before you write it.** Every file path, function name, type name,
constant, line number, command and test file that appears in the guide has been
opened, grepped or run first. No exceptions, and no "this is almost certainly
where it lives".

The reason is not pedantry. A reader following a guide cannot tell a verified
path from a plausible one — they hit the wrong file, assume they misunderstood,
and lose the thread. One wrong path costs more trust than five missing details.

## What to verify, concretely

| In the guide | Verify by |
|---|---|
| A file path | Opening it. Not `ls` on the directory — the file |
| A function, hook, type or constant | Grepping for its definition and reading the signature |
| A line number | Reading that line, now. They drift constantly; prefer a symbol name where one exists |
| "X already does Y" | Reading X and confirming it does Y |
| A command to run | Reading it out of `package.json`, the Makefile, the README — not memory |
| A test location or naming pattern | Finding a sibling test that already follows it |
| A convention ("we always…") | Finding it in `CLAUDE.md`, a linter config, or two existing examples |

Line numbers deserve their own warning. They are the detail most likely to be
stale by the time the guide is read, so anchor on a symbol name and give the
line number as a convenience, never as the only way to find something.

## When the session is thin

The plan is usually in context, and the code usually is not. Go and get it.

- **`Explore`** for a wide sweep across a repo whose layout you do not know:
  "where does X attach", "what already subscribes to Y", "does anything do Z
  today". One agent, a specific question, and you keep the conclusion instead of
  the file dumps.
- **The project's own context skill** — `foleon-fio`, `foleon-ripley`, or
  whatever serves the repo — for conventions, gotchas and history that are true
  but not visible in the code.
- **The repo's own committed instructions**: `CLAUDE.md`, `ARCHITECTURE.md`,
  `CONTRIBUTING.md`, `docs/adr/`. These carry the rules a reviewer will actually
  apply, and a guide that ignores them teaches the reader to fail review.
- **An existing example of the same shape.** The strongest thing a guide can say
  is "this file already does exactly this, read it first". Find one.

## Conventions are part of correctness

A guide that produces working code in the wrong house style has half failed. Before
writing, know at least:

- the comment policy (some repos want the why documented, some forbid it),
- the test framework, its command, and where tests sit relative to source,
- the formatter and linter, and whether a hook runs them,
- whether the repo has an opinion about file placement for the kind of thing
  being added.

Put these in the pre-PR checklist rather than scattering them through the steps.

## When you cannot verify something

Say so, in the guide, in the open:

> I could not find where the viewport value is resolved. Start by searching for
> `useActiveSettingsViewport` and work outward from its callers.

That is an honest instruction and a useful one. It also teaches the reader how to
look, which is worth more than the answer. What is not acceptable is a confident
path you did not check.

## Cost

This step is the slow part, and it is the part that makes the guide worth
publishing. A guide written from memory in two minutes and wrong in three places
costs the reader an afternoon. Spend the time here.
