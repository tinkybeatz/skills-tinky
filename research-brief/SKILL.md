---
name: "research-brief"
description: >
  Research a topic and produce a client-ready brief in one command.
  Trigger when the user asks to: "research and write a brief", "research and brief",
  "make a brief on", "prepare a brief about", "client deliverable on",
  or any phrasing combining research + client deliverable in a single request.
---

# RESEARCH-BRIEF

Chain `/documentor` and then `/brief-writer` in a single command.

---

## Workflow

1. **Ask for the audience** if not specified (decision-maker client / technical client / designer brief / sales proposal)
2. **Run `/documentor`** — full research using the appropriate mode (Quick/Standard/Deep)
3. **Deliver the DOCUMENTOR report** in the conversation (traceable, with sources and labels)
4. **Run `/brief-writer`** — turn the report into a client deliverable tailored to the identified audience
5. **Deliver the brief** in the conversation

---

## Rules

- Never skip the DOCUMENTOR step — the brief needs a sourced report as its input
- Never merge the two outputs — the report and the brief are delivered separately
- If the research comes up empty (no source scoring ≥ 60/100), do not produce a brief — deliver only the DOCUMENTOR failure report
