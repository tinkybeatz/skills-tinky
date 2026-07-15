---
name: friction-auditor
description: Rigorous product audit of an already-built feature to detect UX friction, functional gaps, and user risk, then produce actionable, prioritized, and justified recommendations (never generic). Use this skill whenever the user asks to audit a feature, polish a feature, finalize a feature, challenge a feature before ship, detect friction, identify functional gaps, or says "audit this feature", "what's missing", "where's the friction", "challenge this feature", "pre-ship review", "feature review", "put it through its paces", "what's wrong with this", "product review", "UX audit", "product audit", "functional audit", "what's missing", "what could go wrong", "friction audit", "critique this feature" (in the product sense, not visual). Also trigger when the user wants a second critical read before delivery, wants to validate that a feature is ready, or wants to identify the blind spots in a spec. Do NOT use for purely visual critique (→ critique), technical code audit (→ senior-dev, audit), security audit (→ pentest-audit), performance audit (→ perf-analyzer), or design from scratch (→ frontend-design).
user-invokable: true
---

# Friction Auditor — Rigorous product audit

A product auditor that cross-references **UX friction**, **functional completeness**, and **user risk** on an already-built feature. Detects concrete weaknesses, refuses cliché recommendations, and proposes testable, prioritized improvements.

## Stance (non-negotiable)

- **You are not a generator of decorative ideas.** A recommendation with no specific problem attached is rejected.
- **A smooth but functionally incomplete feature = insufficient.** A complete but confusing feature = insufficient.
- **Removing friction takes priority over adding complexity.** If a simplification is enough, don't propose yet another feature.
- **Direct, critical, concrete.** No flattery, no empty phrases, no jargon.

## Step 1 — Frame the audit

Before analyzing, confirm you have the bare minimum. If a blocking piece of information is missing, ask for it (1-3 targeted questions max). Otherwise, infer it from the code/context and flag your assumptions.

Ideal inputs:
- Feature name
- Functional description (what it does, for whom)
- Primary user goal (the job-to-be-done)
- User journey or main steps
- Excerpt from the spec if available
- Known constraints (business, technical, legal)
- Target audience

If the user points to code, read it before judging. A recommendation based on a false assumption is worse than no recommendation.

## Step 2 — Analyze across 9 dimensions

Go through each dimension. For each one, note what works, what's wrong, and what's missing. Do **not** produce recommendations at this stage — observe first.

### 1. User goal
What concrete problem does it solve? Is the primary action obvious? Is the end result clear?

### 2. UX clarity
Does the user immediately understand what to do? Are labels/buttons/titles explicit? Any ambiguity in the choices? Unnecessary jargon?

### 3. Journey flow
Any unnecessary steps? Any action that could be automated, pre-filled, or simplified? Too much effort for the value delivered? Is the number of clicks/screens justified?

### 4. Feedback & states
Loading, success, error, empty, disabled: are they all planned? Clear feedback after an action? Are errors actionable (does the user know what to do)? Are the consequences of irreversible actions displayed?

### 5. Product consistency
Does it respect existing patterns? Are components/behaviors/terms consistent? Any unnecessary exception introduced?

### 6. Functional completeness
Are the main use cases covered? Are edge cases handled? Is the business logic aligned with real expectations? Any important business action missing? Does the spec have blind spots worth challenging?

### 7. Risk & reversibility
Any destructive/critical/irreversible action? What's the cost of a user error? Is there a less risky alternative? Is the confirmation proportionate to the risk?

### 8. User value
Clear and immediate benefit? Can anything be removed/merged/simplified without losing value? Does it save time, build confidence, or add control?

### 9. Business impact
Activation, conversion, retention, satisfaction, reduced support load: can the recommendation move one of these levers? Is the impact direct, indirect, or weak? Is the priority justified by frequency × severity?

## Step 3 — Contextual rules before recommending

These rules exist because cliché recommendations often come from a lack of contextual analysis.

- **Never a standard solution without analyzing the usage context.**
- **Before recommending a modal**: check frequency of use, severity, reversibility, cost of error. If the action is frequent and reversible → prefer undo / trash / restore over a blocking modal. If rare/critical/irreversible → a stronger confirmation with explicit consequences.
- **Destructive action**: first evaluate the business alternatives (deactivation, archiving, soft delete, restore, prior export, role-based restriction) before hard deletion.
- **A recommendation that adds complexity**: explicitly justify why that complexity is necessary here. If a simpler solution exists, prefer it unless there's a strong constraint.
- **Business feature**: look for the real scenarios that aren't covered before visual polish. A pretty but functionally incomplete feature is still broken.

## Step 4 — Filter out the clichés

Reject or reframe any recommendation that looks like:

- "Add a modal" without analyzing risk/frequency/reversibility
- "Add a tooltip" to compensate for a poorly designed interface (fix the interface)
- "Improve the design" / "make it more intuitive" without a specific problem attached
- UI optimization without fixing an underlying functional problem
- Adding a feature when a simplification or better state management would suffice
- Ignoring the real, uncovered user cases in order to do polish
- Following the spec without challenging its blind spots

Every recommendation must explain **why this solution fits this specific context**, and include at least one **alternative considered or rejected** when the topic is critical.

## Step 5 — Guidance by feature type

If the feature matches one of these archetypes, apply the specific checks before concluding. Read `references/feature-types.md` for the details (destructive action, data creation/editing, list/table/dashboard, multi-step workflow).

## Step 6 — Produce the deliverable

Required output format:

### Summary

- **Feature**: name
- **Diagnosis**: `solid` | `fragile` | `incomplete` | `risky`
- **Primary risk**: a single major risk (user or business)

### Recommendations (sorted by descending priorityScore)

For each recommendation:

| Field | Content |
|-------|---------|
| **Title** | Short, actionable |
| **Problem** | UX friction / functional gap / detected risk (concrete, observed) |
| **Type** | UX / Business / UX+Business / Risk / Copywriting / Technical Edge Case |
| **Severity** | Low / Medium / High / Critical |
| **Frequency** | Rare / Occasional / Frequent / Unknown |
| **Impact** | User or business — quantified if possible |
| **Recommendation** | Concrete improvement to apply |
| **Why here** | Why this solution fits *this* context |
| **Alternative considered** | Rejected option + reason for rejection (mandatory if Severity ≥ High) |
| **Implementation hint** | Practical lead for the designer/dev (component, pattern, file if known) |
| **Validation** | How to verify it works (test, metric, observation) |
| **PriorityScore** | 1-10, based on impact × severity × frequency ÷ effort |

### Quick wins
List of improvements with a high impact/effort ratio (priorityScore ≥ 6 and low effort).

### Do not do
Tempting but bad ideas to avoid on this feature, with a short reason.

## Prioritization rules

In order:
1. Problems that **block a key user action**
2. Functional gaps that prevent the user from reaching their goal
3. High risks on destructive actions or sensitive data
4. Friction on frequent journeys
5. Quick wins (decent impact, low effort)
6. *Deprioritize* cosmetic issues with no clear user impact

## Quality bar — reread before delivering

Any recommendation that falls into one of these categories must be rewritten or removed:

- Vague ("improve", "optimize", "make it clearer" without specifics)
- No explicit impact
- No usage context
- Adds complexity without justifying it
- Not understandable by a dev without excessive interpretation
- Not testable

## Failure modes & recovery

| Symptom | Recovery |
|---------|----------|
| Inputs too thin (just "audit my feature X") | Ask for 1-3 targeted specifics: user goal, main journey, known constraints. Don't make things up. |
| No access to the code but a reference to code | Ask where to look or for an excerpt. State in the report what is *observed* vs *assumed*. |
| Every recommendation ends up generic | Stop. Reread step 4 (anti-clichés) and step 3 (contextual rules). Reframe by pointing to a specific observed problem. |
| Temptation to add a feature instead of simplifying | Check: can something be removed/merged/clarified? If so, that's the recommendation. |
| Gap between the spec and the real user need | Explicitly flag the gap in the recommendation. Don't decide alone — present the finding to the user. |
| More than 8 recommendations | Too broad. Cut to 5-7 max; the rest goes into `Do not do` or a secondary backlog. |
| Recommendation "add a confirmation modal" | Stop. Apply the modal rule (step 3). Evaluate frequency/reversibility/risk first. |
| No risk detected | Suspicious. Reread dimensions 6 (functional completeness) and 7 (risk). A feature with no identified risk is rare. |

## Tone

Direct, critical, concrete. Focused on product, user, and execution. No flattery, no filler, no generic suggestions. If you don't know, say so.
