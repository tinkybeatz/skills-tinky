# Routing — matching a goal to the right skill(s)

Goal: given the user's objective, find the best-fit **existing** skill(s) to reach it — or say honestly that none fits. The output format (the plan) lives in `plan-format.md`; this file is about *finding* the skills.

## Method
1. **Build the catalog cheaply.** Read `CATEGORIES.md` for the map, then each `<category>/_category.md` for scopes. To compare specific skills, read their `description:` frontmatter (grep `description:` across the repo, or scan the relevant category folder). Don't read full SKILL.md bodies unless disambiguating a close call.
2. **Decompose the goal into stages.** Many objectives are a chain: research → decide → build → test → document → ship. Each stage maps to a category.
3. **Narrow by category first**, then compare skills within it via their descriptions' triggers and purpose. A skill fits if the user's task is the job its description describes.
4. **Pick the smallest sufficient set.** One skill if one suffices; a short chain if the goal has stages. Add a runner-up only if genuinely close — then state the boundary.

## Disambiguation (boundaries that come up)
- Product decision *itself* → `product/ceo-challenger`; the analysis feeding it → `research/documentor`; the write-up → `docs/…`.
- Security angle → `infra/pentest-audit`; general code review → `dev/senior-dev`; pure architecture → `dev/architecture-conceptor`.
- Build a UI → `design/build/frontend-design`; improve an existing UI's one dimension → the matching `design/refine/*`.
- Formal document as the deliverable → `docs/*`; the underlying capability → its function category.
- Research/understand → `research/*`; capture into Notion → `notes/*`.

## When nothing fits
Say so directly — don't force a poor match. Name the category the missing skill would belong to and suggest creating it with `skill-creator`. If the objective is a one-off unlikely to recur, note that a skill may be overkill and it's fine to just do the task.
