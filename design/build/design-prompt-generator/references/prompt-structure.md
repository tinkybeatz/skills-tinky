# Structure of a design prompt

An effective prompt always follows this 8-section structure. Every section is essential — the LLM that receives the prompt needs all of this information to produce a premium result on the first try.

## Template

```
[Section 1 — Opening]
[Section 2 — Technical stack]
[Section 3 — Design tokens]
[Section 4 — Typography]
[Section 5 — Visual effects]
[Section 6 — Components]
[Section 7 — Animations]
[Section 8 — Final composition]
```

---

## Section 1 — Opening (2-3 lines)

Summarize in 2-3 sentences what the prompt will produce. State the visual tone, the page type, and the expected result.

**Good example:**
> Create a full-screen hero landing page for "Bloom" — an AI-powered plant/floral design platform. The design uses a liquid glass morphism aesthetic over a looping video background.

**Bad example:**
> Make a nice landing page for a plant company.

The difference: the good example contains the name, the concept, and the aesthetic in a single sentence.

---

## Section 2 — Technical stack (1-3 lines)

Specify exactly which technologies to use. Always first, to frame the LLM.

**Standard format:**
> Use React + Vite + Tailwind CSS + TypeScript with shadcn/ui.

**With additional dependencies:**
> Use React + Vite + Tailwind CSS + TypeScript with shadcn/ui + Framer Motion. Install hls.js and framer-motion.

**Fonts to install:**
> Install @fontsource/geist-sans.

---

## Section 3 — Design Tokens (HSL CSS variables)

This is the heart of the design system. Every prompt must contain a complete set of CSS variables.

**Mandatory minimum set:**
```css
:root {
  --background: [H] [S]% [L]%;
  --foreground: [H] [S]% [L]%;
  --card: [H] [S]% [L]%;
  --card-foreground: [H] [S]% [L]%;
  --primary: [H] [S]% [L]%;
  --primary-foreground: [H] [S]% [L]%;
  --secondary: [H] [S]% [L]%;
  --secondary-foreground: [H] [S]% [L]%;
  --muted: [H] [S]% [L]%;
  --muted-foreground: [H] [S]% [L]%;
  --accent: [H] [S]% [L]%;
  --accent-foreground: [H] [S]% [L]%;
  --border: [H] [S]% [L]%;
  --input: [H] [S]% [L]%;
  --ring: [H] [S]% [L]%;
  --radius: 0.75rem;
}
```

**Useful optional tokens:**
```css
  --hero-heading: [H] [S]% [L]%;
  --hero-sub: [H] [S]% [L]%;
  --destructive: [H] [S]% [L]%;
```

Always in HSL without the hsl() wrapper — the bare values let you use `hsl(var(--token))` and `hsl(var(--token) / 0.5)` in Tailwind.

---

## Section 4 — Typography

Specify:
1. The display font (for headings) with its exact import
2. The body font (for text) with its exact import
3. The weights to import
4. The CSS variables for the fonts

**Good format:**
```
Fonts:
Import from Google Fonts: Instrument Serif (display) and Inter weights 400/500 (body)
CSS variables: --font-display: 'Instrument Serif', serif and --font-body: 'Inter', sans-serif
Body uses var(--font-body), headings use inline fontFamily: "'Instrument Serif', serif"
```

---

## Section 5 — Visual effects (complete CSS)

Don't say "add glassmorphism" — give the exact CSS. The LLM must be able to copy the block as-is.

**Expected format:**
```
Liquid Glass Effect (CSS class .liquid-glass):

.liquid-glass {
  background: rgba(255, 255, 255, 0.01);
  backdrop-filter: blur(4px);
  [... complete CSS ...]
}
.liquid-glass::before {
  [... complete pseudo-element ...]
}
```

A prompt can contain 1 to 3 visual effects. Beyond that, the result will be overloaded.

---

## Section 6 — Components (the longest)

Describe each component of the page with:
- Its position and layout (exact Tailwind classes)
- Its real text content (no placeholders)
- Its interactions (hover, click)
- Its responsive variants (sm:, md:, lg:)

**Format per component:**
```
Navigation Bar:
relative z-10, flex row, justify-between, px-8 py-6, max-w-7xl mx-auto
Logo: "BrandName®" text-3xl tracking-tight, [font], text-foreground
Nav links (hidden on mobile, md:flex): Home, About, Work, Contact
  — text-sm text-muted-foreground hover:text-foreground transition-colors
CTA button: "Get Started", rounded-full px-6 py-2.5 text-sm text-foreground
```

**Standard component order:**
1. Background (video, gradient, pattern)
2. Navigation bar
3. Hero section (headline, subtitle, CTA)
4. Social proof (logos, testimonials, stats)
5. Features / content sections
6. CTA section
7. Footer

For a hero-only prompt, only sections 1-4 are needed.

---

## Section 7 — Animations

Specify the CSS keyframes and utility classes.

**Format:**
```
Animations (CSS keyframes + classes):

@keyframes fade-rise {
  from { opacity: 0; transform: translateY(24px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-rise { animation: fade-rise 0.8s ease-out both; }
.animate-fade-rise-delay { animation: fade-rise 0.8s ease-out 0.2s both; }
.animate-fade-rise-delay-2 { animation: fade-rise 0.8s ease-out 0.4s both; }

H1 gets animate-fade-rise
Subtext gets animate-fade-rise-delay
CTA button gets animate-fade-rise-delay-2
```

**For Framer Motion:**
```
Animation Pattern:
const fadeUp = (delay: number) => ({
  initial: { opacity: 0, y: 20 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, margin: "-100px" },
  transition: { duration: 0.6, delay, ease: "easeOut" },
});
```

---

## Section 8 — Final composition

Explain how the components fit together on the page.

**Format:**
```
Layout: No decorative blobs, radial gradients, or overlays. Minimalist,
cinematic, vertically centered hero. The video provides all visual depth.

Page Composition:
The Index page renders <Navbar /> then <HeroSection /> then <SocialProof />
sequentially with no wrapper styling.
```

This section is short but important — it guides the LLM on what NOT to add.

---

## Length rules

| Prompt type | Target length | Sections |
|----------------|---------------|----------|
| Hero section only | 2000-4000 chars | 1-5, 7, 8 (components = navbar + hero) |
| Complete landing page | 5000-8000 chars | All |
| Isolated component (pricing, CTA) | 1000-2000 chars | 1-3, 5-7 (adapted) |

Never exceed 8000 characters. If the page is complex, break it into sequential prompts.
