# Adaptation matrix by audience

This file details how to adapt each dimension of the SRS to the type of
reader. The same required content is presented differently.

---

## Main matrix

| Dimension | Non-technical client | Technical client | Internal document (dev team) | Tender / Contract |
|-----------|---------------------|------------------|---------------------------|--------------------------|
| **Language** | Plain, zero jargon, domain analogies | Technical jargon OK, precision | Jargon + internal conventions | Formal, legally precise |
| **Main focus** | Business value, outcomes, user journey | Interfaces, constraints, metrics | Implementation, edge cases, APIs | Exhaustiveness, coverage, commitment |
| **Requirements format** | User stories + acceptance criteria in plain language | Shall statements + EARS | EARS + Gherkin/BDD | Formal shall statements |
| **Visuals** | Mockups, business workflows, user journeys | Architecture, sequence, and context diagrams | Technical diagrams, data models, ER | Formal UML diagrams |
| **NFRs** | Summarized in terms of business impact ("the site loads in under 2 seconds") | Precise metrics with thresholds and measurement methods | Metrics + test strategy + tooling | Metrics with binding SLA |
| **Glossary** | Extensive: both domain AND technical terms explained | Only non-standard technical terms | Minimal (conventions known to the team) | Exhaustive, legally precise definitions |
| **Executive summary** | Mandatory up front (1 page max) | Optional (table of contents is enough) | Not needed | Mandatory (summary + scope) |
| **Prioritization** | MoSCoW with business explanations | MoSCoW or numeric scoring | Numeric scoring + effort estimate | MoSCoW with contractual commitment |
| **Validation** | Visual walkthroughs, prototypes, demos | Formal technical reviews | Code reviews, test plans, spike results | Formal sign-off with acknowledgment |
| **Traceability** | Simplified (need → feature) | Complete (need → design → test) | Complete + links to tickets/code | Complete + contractual matrix |
| **Length** | Shorter, dense with value, no empty sections | Complete, structured | Complete + implementation notes | Exhaustive, nothing implicit |
| **Tone** | Collaborative, solution-oriented | Professional, factual | Direct, concise | Formal, contractual |

---

## Detailed adaptation strategies

### Non-technical client

**Guiding principle**: The client must understand EVERY sentence without
technical help. If they have to ask "what does this mean?", the SRS has
failed.

**Techniques:**
- An executive summary up front that answers: "what does this system do, and
  why?"
- User stories instead of shall statements
- Every technical term accompanied by an explanation in parentheses or a
  glossary entry
- Mockups/wireframes referenced inline rather than described in text
- Prioritization explained in business terms ("without this feature, users
  can't complete a purchase")
- NFRs translated into user impact ("the page loads in under 2 seconds"
  instead of "p95 latency < 200ms")

**Recommended structure:**
```
Executive summary (1 page)
1. Context and objectives
2. What the system does (user stories grouped by journey)
3. What matters (priorities explained)
4. Constraints and assumptions
5. Next steps
Appendix: Technical detail (for the development team)
```

### Technical client

**Guiding principle**: Precision and exhaustiveness. Every requirement must
be actionable without interpretation.

**Techniques:**
- Shall statements for functional requirements
- EARS for event-driven behaviors
- Quantified metrics for each NFR
- Architecture and sequence diagrams
- Documented API interfaces (endpoints, payloads, return codes)
- A complete traceability matrix

**Recommended structure:** The full IEEE 29148 template.

### Internal document (dev team)

**Guiding principle**: Efficiency. The team knows the context — get straight
to the point.

**Techniques:**
- EARS + Gherkin for each requirement
- Direct links to tickets (Jira, Linear, GitHub Issues)
- References to existing code when relevant
- Implementation notes in the margin (suggestion, not obligation)
- A naming convention aligned with the codebase
- Wiki/markdown format (a living document, not a frozen PDF)

**Recommended structure:**
```
1. Context (1 paragraph)
2. Scope (in/out)
3. Requirements per feature (EARS + Gherkin)
4. NFRs (compact table)
5. Open questions / TBDs
```

### Tender / Contract

**Guiding principle**: Nothing implicit. Whatever isn't written down doesn't
exist contractually.

**Techniques:**
- Strict shall wording with normative terminology (shall/should/may)
- Every requirement numbered and traceable
- Formal acceptance criteria for each requirement
- Disclaimer clauses for the assumptions
- A documented change management procedure
- An appendix of explicit exclusions

**Recommended structure:** The full IEEE 29148 template + contractual
sections (change management, acceptance criteria, penalties).

---

## Bilingual document (technical + non-technical)

When the audience is mixed (e.g. a non-technical client + a technical team
reading the same document), use a layered structure:

1. **Main body** — accessible language, user stories, visuals
2. **Technical callouts** — technical details in visually distinct blocks
   (blockquote or callout) that the non-technical reader can skip
3. **Technical appendix** — detailed specifications, API interfaces, data
   models, for the development team

This approach avoids producing two separate documents that inevitably
diverge.
