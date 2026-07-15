# Drafting anti-patterns

Detect and rephrase these patterns immediately, in Generation mode as well as
in Audit mode. Sources: Berry/Tjong (NLP for ambiguity), QuARS (SEI/CNR),
Wiegers, IEEE 1233.

---

## 1. Weak words (unverifiable adjectives and adverbs)

| Word | Problem | Rewrite |
|-----|----------|---------------|
| user-friendly | No threshold | "Task X completed in < 30 s by 8/10 testers" |
| robust | No scenario | "99.9% available during business hours, excluding scheduled maintenance" |
| fast / rapide | No measurement | "p95 response time < 200 ms" |
| easy / simple | Subjective | Measurable usability criterion |
| efficient | No indicator | Precise KPI (CPU < X%, RAM < Y MB) |
| scalable | No load threshold | "Sustains 10,000 req/s" |
| flexible | No evolution case | List the planned axes of evolution |
| reliable | No SLA | "MTBF > 1000 h, RPO < 1 h, RTO < 4 h" |
| modern | Meaningless | List the target technologies |
| seamless | Subjective | Describe the flow step by step |
| intuitive | Subjective | User test with objective criteria |
| optimal / best | Superlative | State what is being optimized |
| state-of-the-art | Vague | Cite a benchmark or a standard |
| acceptable | No threshold | Define the threshold |
| sufficient | No measurement | Quantify |
| appropriate / relevant | Subjective | Explicit criterion |

---

## 2. Weak verbs

| Verb | Problem | Replacement |
|-------|----------|--------------|
| should | States a recommendation, not an obligation | **shall** / **doit** |
| may | Optional by default, ambiguous | **may** only if genuinely optional |
| could | A wish, not a requirement | **shall** or remove |
| might | Hypothetical | **shall** or remove |
| will | Future tense, not a present obligation | **shall** / **doit** |
| supports | Vague | **shall allow** [precise action] |
| handles | Vague | Enumerate the cases |
| manages | Vague | Break down into actions |

**Convention**: in English, **shall** = contractual requirement;
**will** = future statement; **should** = recommendation; **may** = permission.
In French, **doit** = requirement; **devrait** = recommendation; **peut** = permission.

---

## 3. Modifying phrases (softeners)

To be removed or replaced with an explicit condition:

- *as appropriate* → state the condition
- *as required* → state who requires it and when
- *if necessary* → state the necessity criterion
- *if possible* → is this a requirement or not?
- *to the extent possible* → define the limits
- *as much as possible* → quantify
- *where applicable* → define the scope

---

## 4. Indefinite pronouns

To be replaced with a number or an exhaustive list:

- *few* → "fewer than 10" or "< 5%"
- *many* → quantify
- *most* → quantify ("> 80%")
- *some* → define which ones
- *several* → state how many

---

## 5. Passive voice

Hides the subject (who performs the action). Always prefer the active voice.

❌ *"It is expected that the data be saved."*
✅ *"The system shall save the data ..."*

❌ *"A verification must be performed."*
✅ *"The authentication module shall verify ..."*

---

## 6. Comparatives with no reference

❌ *"Faster than before"* → define "before"
❌ *"Better than the current version"* → measurable metric + dated baseline
❌ *"Comparable to the competitor"* → cite the competitor + the benchmark

---

## 7. Unverifiable totality

❌ *"Handle all cases"* → list cases A, B, C
❌ *"Cover all needs"* → list them explicitly
❌ *"Always / never"* → define the time scope
❌ *"100%"* → is it measurable? If not, reconsider

---

## 8. Pure, untestable negations

❌ *"The system shall not crash"* → positive criterion
✅ *"The system shall maintain 99.9% availability during business
   hours"*

---

## 9. Ambiguous pronouns

❌ *"It must send it to her."* (who? what? to whom?)
✅ Name the subjects and objects explicitly.

---

## 10. Compound requirements (anti-singular)

Detect the conjunctions "and", "or", "as well as" that bundle several
needs together:

❌ *"The system shall send an email **and** an SMS, **and** archive it
   to the database."*

→ split into 3 atomic requirements.

---

## 11. Recommended EARS pattern

For event-driven requirements, use **EARS** (Easy Approach to
Requirements Syntax):

```
[Optionally: When [condition]] [the subject] shall [action] [object]
[measurable constraint].
```

The 5 EARS patterns:
- **Ubiquitous**: *The system shall X.*
- **Event-driven**: *When E occurs, the system shall X.*
- **State-driven**: *While S is active, the system shall X.*
- **Optional**: *If F is enabled, the system shall X.*
- **Unwanted behavior**: *If undesired event E occurs, the system shall Y.*

---

## 12. Automated tools (reference)

If an automated analysis is requested, these peer-reviewed tools can be
recommended:

| Tool | Source | Capabilities |
|-------|--------|-----------|
| QuARS | SEI / CNR Pisa | NLP, linguistic defects, Coleman-Liau readability |
| ScopeMaster | Commercial | NLP S-V-O, COSMIC FP, ambiguity |
| RQA Quality Studio | The Reuse Company | CCC grid (Correctness/Consistency/Completeness) |

In manual Audit mode, aim for:
- Defect rate < 5%
- Ambiguity rate < 10%
- Coverage 100%
- Test coverage 100%

---

## Sources

- Daniel Berry, *Ambiguity in Natural Language Requirements Specifications*
- Tjong (PhD), *Avoiding Ambiguity in Requirements Specifications*
- Karl Wiegers, *Software Requirements 3rd ed.* (Microsoft Press)
- IEEE 1233 (System Requirements Specifications)
- ISO/IEC/IEEE 29148:2018 § "Requirements smell" annex
