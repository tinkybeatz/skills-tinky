# Output Contract — Full Templates

The SKILL.md holds a compact version of these templates; this file has the full annotated version to read when you need to double-check what goes in each section and why. The contract scales with the tier — don't impose 7 sections on a 4-line answer.

---

## ⚡ Quick output (no marker, 2 sections, < 10 lines)

```
**Decision:** [direct answer in 1-2 sentences]
**Confidence:** low / medium / high — [1 phrase grounding it]
```

If a single non-obvious trade-off matters, add it inline. Otherwise stop. **No state marker, no Next line** — Quick answers are self-contained by definition.

**Why no Next line:** Quick is meant to unblock in one shot. Adding a forward-motion prompt would inflate the format and defeat its purpose.

---

## 📋 Standard output (state marker + 5 sections + Next)

```
[📋 Standard · Step X/4 · <activity> · <project>]

1. **Applicable Standards** — bullet list from Step 0 (skip if none load)
2. **Decision** — selected option in 2-3 sentences
3. **Trade-offs** — comparison table of the 2+ options on the dimensions that matter for this case
4. **Implementation Plan** — concrete steps with acceptance criteria and rollback note
5. **Risks** — top 2-3 with severity and mitigation

→ **Next:** [single concrete action] · or: [alternative if you want to pivot]
```

**Why 4 steps (not 6) in the marker:** Standard tier typically runs Steps 0 + 2 + 3 + 4. Steps 1 and 5 are skipped or collapsed.

---

## 🔬 Deep output (state marker + 7 sections + Decision Log proposal + Next)

```
[🔬 Deep · Step X/6 · <activity> · <project>]

1. **Applicable Standards** — bullet list from Step 0
2. **Executive Summary** — 2-3 sentence recommendation
3. **Technical Decisions** — selected option, key trade-offs, justification
4. **Implementation Plan** — steps, acceptance criteria, tests, release gates
5. **Validation Evidence** — checks run, results, failed checks
6. **Risks and Limitations** — unknowns, residual risks with severity/owner/mitigation
7. **Confidence** — low/medium/high with rationale

📝 **Decision Log:** [proposal to write/update the ADR — see closing-loop.md]

→ **Next:** [single concrete action] · or: [handoff to apply / back to architecture-conceptor]
```

---

## The Next line is mandatory for Standard and Deep

If you end with "that's it" or "let me know if you have questions", you've abandoned the partnership posture and reverted to oracle mode. The Next line forces you to propose what comes after — that's the entrepreneurial reflex made concrete.

Good Next lines:
- *"Next: run the migration on staging this afternoon and report p95."*
- *"Next: if you want, I can hand this off to apply for backlog + execution."*
- *"Next: open the 3 links and tell me which resonates — I pivot from there."*

Bad Next lines:
- *"Next: let me know if you need anything else"* (not forward motion)
- *"Next: think about it"* (not actionable)
- No Next at all.
