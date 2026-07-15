# Closing the loop — Decision Log + Handoffs

The workflow produces a decision. Two things must happen at the end of a Deep tier (and optionally Standard) to make that decision *land* rather than evaporate. The SKILL.md has a 10-line summary; read this file when you actually need to bootstrap an ADR convention or when a handoff decision feels non-obvious.

---

## A. Decision Log — persist Deep decisions

Deep decisions deserve to be archived outside the chat. Without persistence, the rationale is lost the moment the conversation ends, and the next senior-dev session re-debates settled questions.

### Convention used by this skill (proposed when no existing pattern is detected)

- **Path:** `docs/decisions/NNNN-kebab-title.md` at the repo root
- **Filename:** zero-padded sequence number + kebab-case title (e.g., `0007-monolith-vs-microservice.md`)
- **Length:** 15-25 lines, no more — an ADR that takes an hour to write doesn't get written
- **Required fields:**
  - **Date**
  - **Status** (Accepted / Superseded)
  - **Context** (3-5 lines — what drove the decision)
  - **Decision** (2-3 lines — what we're doing)
  - **Alternatives considered** (1 line each, with reason rejected)
  - **Kill criterion** (when this decision would be revisited)

### Bootstrap behavior (when `docs/decisions/` doesn't exist yet)

At the end of a Deep tier deliverable, **propose — never auto-execute**:

> *"This decision is worth freezing. I don't see an existing ADR pattern in this repo — want me to bootstrap one with `docs/decisions/0001-<title>.md` using the convention above? It's a 15-line file, takes 30 seconds."*

If the user accepts:
1. Write the file
2. Add a one-line note to `std/<project>/` (e.g., `std/sapain-borne/CONVENTIONS.md`) recording the ADR pattern, so future senior-dev invocations know the convention exists and don't re-ask
3. Confirm in the response: *"Logged as `docs/decisions/0001-monolith.md`. Future sessions will reference it."*

### Steady-state behavior (when `docs/decisions/` exists)

- Step 0 already scans `docs/decisions/` and surfaces relevant past ADRs as constraints
- At the end of Deep tier, write a new ADR with the next sequence number — no need to re-ask for permission unless the user said "skip ADR" earlier in the session
- If a new decision *supersedes* a past one, mark the old one as `Status: Superseded by NNNN` and link it
- If a new decision *refines* without superseding, use `Refines: NNNN` in the frontmatter and keep the old one Accepted

### External doc-store sync (future enhancement, opt-in)

If the team keeps unstructured docs in an external tool (e.g. Notion, Confluence), a future iteration could optionally sync `docs/decisions/` into that tool's database on confirmation. Not in scope yet — local-first.

---

## B. Handoffs — bidirectional with the rest of the skill set

This skill lives in a pipeline, not in a silo:

```
architecture-conceptor  →  senior-dev  →  apply
       (design)            (decide impl)    (execute)
```

Three handoff patterns to use explicitly.

### 1. Upstream — receiving from architecture-conceptor

If the conversation arrives with an architectural decision already named (an ADR cited, a pattern decided, "we agreed on X last week"), treat it as a **given constraint** and do not re-debate it. Frame your work as:

> *"Given X is decided, here's how I'd implement it."*

The user came to senior-dev to decide **implementation**, not to re-litigate the architecture.

### 2. Downstream — handing off to apply

When the decision is settled and the user is ready to move from "decide" to "do", propose explicitly:

> *"Decision is locked. Want me to hand this off to apply for backlog + execution?"*

Don't silently start doing apply's job inside senior-dev. The handoff is part of the value — apply is bundled, optimised for execution, and turns the decision into trackable tasks.

### 3. Lateral — escalating back to architecture-conceptor

If during senior-dev a question reveals itself to be *architectural*, not implementation (e.g., the user asks "should I add this to module X" and you realise the right answer requires re-thinking module boundaries), surface it:

> *"This isn't really an implementation decision — it's an architecture one. I can keep going, or we can hand back to architecture-conceptor for a clean ADR first. Your call."*

Don't do architecture work in disguise. Naming the boundary lets the user pick the right tool.
