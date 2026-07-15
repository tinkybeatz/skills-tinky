# Plan format

The deliverable `god` returns. Keep it short and actionable — the user should be able to act on it immediately. Omit any section that doesn't apply (no "N/A").

## Template

```markdown
## 🎯 Objective
<one line, restated in your own words so the user can confirm you understood>

## 🧩 Recommended skills
- `<skill>` (<category>) — <one line: why it fits>
- ...

## 🗺️ Plan
1. **<skill>** — <what it does for you here>.
   - Invoke: `/<name>` (or: "<natural phrase>")
   - Produces: <output>  →  feeds step 2
2. **<skill>** — ...
   - Invoke: ...
   - Produces: ...

## ✅ End state
<what you'll have when the plan is done>

## ⚠️ Gaps (only if any)
<part of the goal with no matching skill → suggest skill-creator + the category it'd live in;
 or "this needs no skill — just do X">
```

## Worked example — "I want to launch a small SaaS side project"

> ## 🎯 Objective
> Go from a rough SaaS idea to a validated plan + first buildable slice.
>
> ## 🧩 Recommended skills
> - `documentor` (research) — market/competitor research with cited sources.
> - `ceo-challenger` (product) — pressure-test the idea before you build.
> - `generate-business-model` (product) — a justified monetization model.
> - `architecture-conceptor` (dev) — choose the stack and structure.
> - `frontend-design` (design/build) — build the first UI slice.
>
> ## 🗺️ Plan
> 1. **documentor** — research the space and demand. Invoke: `/documentor`. Produces: a cited research brief → informs steps 2–3.
> 2. **ceo-challenger** — challenge the idea against that research. Invoke: "challenge this idea". Produces: go/no-go + sharper scope → informs step 3.
> 3. **generate-business-model** — pricing & unit economics. Produces: a business-model doc → informs scope of the MVP.
> 4. **architecture-conceptor** — pick stack & structure for the MVP. Produces: an architecture + decisions → informs step 5.
> 5. **frontend-design** — build the first screen. Produces: the initial UI.
>
> ## ✅ End state
> A validated, costed plan and the first buildable slice of the product.

## Rules
- Only real skills. Prefer the fewest that reach the goal.
- Make the **handoffs** explicit — the value is the chain, not the list.
- If the objective is one stage, a one-skill plan is correct; don't pad it.
