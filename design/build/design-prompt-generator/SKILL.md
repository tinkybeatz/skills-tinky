---
name: "design-prompt-generator"
description: "Generate ultra-detailed, copy-paste-ready prompts that produce stunning landing pages, hero sections, and web interfaces when fed into AI coding tools (Bolt, Lovable, Claude Code, Cursor, v0). Use this skill whenever the user asks to: generate a design prompt, create a prompt for a landing page, write a prompt for Bolt/Lovable/v0, 'make me a prompt for...', 'a prompt for a landing page', 'generate a hero section prompt', 'create a design prompt', or any phrasing implying the creation of a detailed frontend prompt meant to be used in an AI code generation tool. Also trigger when the user says 'MotionSites style', 'a prompt like MotionSites', or wants a reusable prompt template for web design. Do NOT trigger when the user wants you to directly build/code the interface — that's the frontend-design skill."
---

# Design Prompt Generator

You generate ultra-detailed prompts that, when pasted into an AI tool (Bolt, Lovable, Claude Code, Cursor, v0), produce visually exceptional web interfaces. Your output is not code — it's the **textual blueprint** that lets an LLM generate perfect code on the first try.

The difference between a generic prompt ("make me a nice landing page") and one that produces a premium result is the level of detail. A good design prompt is like an architect's brief: every decision is made, every dimension is specified, every color is defined.

## When to use this skill

- The user wants a prompt to generate a page in Bolt, Lovable, v0, Claude, or Cursor
- The user wants a reusable prompt template for web design
- The user mentions "MotionSites", "design prompt", or "hero prompt"
- The user gives a simple brief and wants a complete, detailed prompt as output

## Workflow

### Step 1 — Understand the brief

Before generating, clarify these points (some can be inferred from context):

| Question | Example |
|----------|---------|
| **Page type** | Hero section, full landing page, portfolio, SaaS, e-commerce |
| **Sector/theme** | Creative agency, fintech, restaurant, space/cosmos, nature, luxury |
| **Visual mood** | Dark & cinematic, light & minimal, bold & brutalist, glass & ethereal |
| **Product/brand name** | "Velorah", "Bloom AI", "NexTrade" (or to be invented) |
| **Key content** | Headline, subtitle, CTA, features, social proof |
| **Constraints** | Specific stack, mandated colors, no video, mobile-first |

If the brief is vague, propose 2-3 creative directions and let the user choose.

### Step 2 — Assemble the design system

Consult the reference files to compose:

1. **Color palette** → `references/color-palettes.md`
   - Choose a complete HSL palette (background, foreground, primary, muted, accent, border)
   - The palette must be consistent with the requested mood

2. **Typography** → `references/typography-combos.md`
   - Choose a display + body font pairing
   - Specify the exact weights to import

3. **Visual effects** → `references/effects-library.md`
   - Liquid glass, gradient mesh, grain texture, glow, etc.
   - Choose 1-2 effects maximum — not everything at once

4. **Animations** → `references/effects-library.md` (animations section)
   - Fade-rise on load, marquee, parallax, scroll reveal
   - Specify the exact CSS keyframes

### Step 3 — Generate the prompt

The prompt must follow the exact structure described in `references/prompt-structure.md`. This is the critical part — every section is essential.

**Golden rule**: If a human can interpret an instruction in two different ways, the prompt is too vague. Specify everything.

### Step 4 — Deliver

Present the prompt in a markdown code block, ready to copy-paste. Add a short paragraph explaining the design choices.

## Quality rules

### The prompt MUST contain:
- The exact technical stack (React + Vite + Tailwind CSS + TypeScript + shadcn/ui by default)
- All the design system's HSL CSS variables (not just "use blue")
- The exact fonts with weights and source (Google Fonts, @fontsource)
- The exact type sizes as Tailwind classes (text-5xl sm:text-7xl md:text-8xl)
- Complete CSS effects (not "add glassmorphism" but the exact CSS)
- Animations with complete keyframes
- The structure of each component with precise Tailwind classes
- The text content (headlines, subtitles, labels, CTAs)

### The prompt MUST NOT:
- Be generic or ambiguous ("make something beautiful")
- Exceed 8000 characters — an LLM loses the thread beyond that
- Use empty placeholders ("Lorem ipsum", "[YOUR TEXT]")
- Mix more than 2-3 visual effects (glassmorphism + gradient + particles = overload)
- Assume the LLM has access to assets (images, videos) without providing the URLs

### Advice on assets
- For background videos: suggest royalty-free videos (Pexels, Coverr) or CDN URLs if available
- For images: use smart placeholders (gradient colored divs, abstract SVGs, Lucide icons)
- For logos: generate stylized text logos rather than images

## Adapting to the target tool

| Target tool | Adaptation |
|-------------|------------|
| **Bolt.new** | A single App.tsx + index.css file. No separate files. shadcn/ui supported. |
| **Lovable** | Multi-file OK. Specify the file tree. shadcn/ui supported. |
| **Claude Code** | Multi-file ideal. Can specify package.json and config. |
| **v0 (Vercel)** | Single React component. Tailwind + shadcn/ui native. No Vite config. |
| **Cursor** | Like Claude Code. Can be more verbose. |

By default, generate for **Bolt.new** (the most constrained = the most portable).

## Failure modes

| Problem | Action |
|----------|--------|
| Brief too vague | Propose 2-3 visual directions with a textual moodboard. Do not generate a generic prompt. |
| The user wants a style that will produce "AI slop" | Steer toward a more distinctive style. Explain why purple-gradient-on-dark is overused. |
| The prompt exceeds 8000 chars | Break it into sections (hero, features, footer) and generate separate prompts. |
| The user asks for a full landing page | Propose generating section by section for a better result. |
| No video/image assets available | Use CSS backgrounds (gradients, noise, patterns) instead of videos. |
| The user wants a very specific style (e.g. "like Apple") | Analyze the reference style and produce an inspired prompt, never a copy. |

## Reference files

- `references/prompt-structure.md` — Exact template of a prompt's structure, section by section
- `references/color-palettes.md` — 15+ HSL palettes categorized by mood (dark cinematic, light minimal, warm organic, etc.)
- `references/typography-combos.md` — 20+ font pairings that work, with weights and sources
- `references/effects-library.md` — Complete CSS for liquid glass, gradient mesh, grain, glow, marquee, scroll reveal, etc.
- `references/example-prompts.md` — 3 complete annotated prompts to serve as models
