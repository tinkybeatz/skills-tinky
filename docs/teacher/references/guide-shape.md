# The shape of a guide

This structure is not a suggestion. The user chose it after working through one
that landed, and the parts below are the parts that made it land. Deviate only
when the change genuinely has no sequence to teach.

## Anatomy, in order

### Header

The name of the thing being built, not a category. "Wiring lockBlock to GTM",
not "Analytics implementation guide". One sentence under it saying what the
reader will have when they finish, and why this one is worth doing carefully.

A small strip of facts earns its place when the reader will want them at a
glance: files touched, the ticket, the symbol at the centre of the change, how
it gets verified. Four at most. Skip it rather than pad it.

### Step zero: what you are building, in one breath

Before any instruction, one short section that explains the *idea*. Not the
steps — the shape of the solution and why it is that shape. For a listener:
"you could add a call to every button, or you could listen in one place; here
is why one place wins."

This is the section a reader returns to in six months. It is also the one most
often skipped, because it feels like preamble. It is not.

### Numbered steps

One per real move. Each step carries, in this order:

1. **The file it touches**, as a visible path.
2. **What to do**, in one or two sentences, plainly.
3. **Why**, in a short paragraph of its own. This is the teaching. If a step has
   no why worth writing, ask whether it is a step or just typing.
4. **The code, hidden** behind a `<details>`/`<summary>` reveal, closed by
   default, with the summary reading like an offer: "Show the code".

Number the steps only because their order is real. If three of them can be done
in any order, say so rather than implying a sequence that does not exist.

### The lines that matter

After the largest step, break out the two or three lines that carry the actual
idea and explain each one on its own, with a subheading or bolded lead. In a
twenty-line snippet, three lines are load-bearing and seventeen are ceremony —
a reader who understands the three can write the seventeen next time.

This is the single highest-value section in the document. It is what separates a
guide from a diff.

### Gotchas

Anything that will bite them, as a visually distinct callout — not a sentence
buried in a paragraph. A gotcha is: an event that fires more often than you
expect, a name that looks stable and is not, a flag that changes what the code
does, a test that passes for the wrong reason.

Give it a short label and one or two sentences. Long gotchas get skipped.

### Pre-PR checklist

What must be true before they open it. Four to six items, each independently
checkable: the typecheck, the two behaviours the tests must pin, the repo's own
conventions (comment policy, formatter, file placement), and any restraint worth
naming — "resist adding the other twelve until this one is proven".

### Footer

What comes after this guide, in two or three lines. What the next piece of work
is, and anything still waiting on someone else.

## Writing rules

**Address the reader directly.** "You are building", "run this", "look at". Not
"one should" and not "the developer will".

**Explain the language, not just the change.** Beginner is the default. If the
step uses a `useEffect` cleanup, a generic, a discriminated union or a
dependency array, say what it does here. One clause is usually enough:
"returning it from the effect is what stops the listener piling up".

**Never let a snippet stand alone.** Code with no prose around it is the failure
this whole shape exists to prevent.

**Keep it as short as the change is.** Four steps for a four-step change.
Padding reads as thoroughness for about thirty seconds, then as noise.

**Write the real thing.** Real paths, real symbols, real commands from this
repository. No `foo`, no `myFunction`, no placeholder that the reader has to
translate.

## Design

Load `artifact-design` before writing the page. A few things that specifically
serve a guide:

- A readable measure, around 65 characters, because this is read in order rather
  than scanned.
- Reveals that look like controls — a `+` that becomes `−`, a cursor, a visible
  focus state.
- Monospace for every path, symbol and command, inline as well as in blocks.
- Code blocks that scroll inside their own container, so the page never scrolls
  sideways.
- Gotcha callouts in a colour that is not the accent, so "pay attention here"
  reads differently from "this is a link".

## Worked example

`Wiring lockBlock to GTM`, built 2026-09-16, is the reference implementation of
this shape: a five-step guide to adding one analytics event, with a step zero
explaining the one-listener idea, three broken-out lines under the largest step,
two gotcha callouts, and a four-item pre-PR checklist. Every path in it was read
first, and one section says plainly which decision was still open.

What made it work, in the user's own reaction: the code was hidden, the why came
before the how, and it named the three lines that mattered instead of leaving
them inside a twenty-line block.
