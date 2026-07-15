# Annotated example prompts

3 complete prompts, extracted and annotated to serve as models. Each annotation explains why a section is effective.

---

## Example 1 — Dark Cinematic Hero Section (Velorah style)

**Original brief:** Creative agency, dark, glassmorphism, video background, elegant typography.
**Length:** ~3900 chars | **Type:** Hero section only

```
Create a single-page hero section with a fullscreen looping background video,
glassmorphic navigation, and cinematic typography. Use React + Vite + Tailwind
CSS + TypeScript with shadcn/ui.
```
> ANNOTATION: The opening states the visual result (fullscreen video, glassmorphic nav, cinematic typography) + the stack. In two lines you know exactly what you'll get.

```
Video Background:
Fullscreen <video> element with autoPlay, loop, muted, playsInline
Source URL: https://d8j0ntlcm91z4.cloudfront.net/[...].mp4
Positioned absolute inset-0 w-full h-full object-cover z-0
```
> ANNOTATION: The video URL is provided — the LLM doesn't have to invent a placeholder. The exact Tailwind classes are specified.

```
Fonts:
Import from Google Fonts: Instrument Serif (display) and Inter weights 400/500 (body)
CSS variables: --font-display: 'Instrument Serif', serif and --font-body: 'Inter', sans-serif
```
> ANNOTATION: The font pairing is specified with the exact weights. Not "use a nice font".

```
Color Theme (dark, HSL values for CSS variables):
--background: 201 100% 13%
--foreground: 0 0% 100%
--muted-foreground: 240 4% 66%
--primary: 0 0% 100%, --primary-foreground: 0 0% 4%
[...]
```
> ANNOTATION: All the HSL variables are here. The LLM has no color decision to make.

```
Navigation Bar:
relative z-10, flex row, justify-between, px-8 py-6, max-w-7xl mx-auto
Logo: "Velorah®" (® as <sup className="text-xs">), text-3xl tracking-tight,
  Instrument Serif font, text-foreground
Nav links (hidden on mobile, md:flex): Home (active, text-foreground), Studio,
  About, Journal, Reach Us — text-sm text-muted-foreground hover:text-foreground
CTA button: "Begin Journey", liquid-glass rounded-full px-6 py-2.5 text-sm
```
> ANNOTATION: Every element of the navbar is detailed: exact content, classes, hover behavior, responsive (hidden on mobile). Nothing is left to interpretation.

```
Hero Section:
relative z-10, flex column, centered, text-center, px-6 pt-32 pb-40
H1: "Where dreams rise through the silence." — text-5xl sm:text-7xl md:text-8xl,
  leading-[0.95], tracking-[-2.46px], max-w-7xl, font-normal, Instrument Serif.
  The words "dreams" and "through the silence." wrapped in
  <em className="not-italic text-muted-foreground"> for color contrast
```
> ANNOTATION: The headline is written out in full. The words to emphasize are specified. The responsive sizing is complete (text-5xl -> text-8xl).

```
Liquid Glass Effect (CSS class .liquid-glass):
[... complete CSS ...]
```
> ANNOTATION: The CSS is given in full, not "use a glassmorphism effect".

```
Layout: No decorative blobs, radial gradients, or overlays. Minimalist,
cinematic, vertically centered hero. The video provides all visual depth.
```
> ANNOTATION: Critical section — it says what NOT to generate. Without it, the LLM would add unwanted decorative elements.

---

## Example 2 — Light SaaS Landing Page (Stellar style)

**Original brief:** AI/SaaS tool, light theme, clean, professional.
**Length:** ~3900 chars | **Type:** Hero + social proof

```
Create a "Stellar.ai" landing page hero section using React, Tailwind CSS,
and Lucide React icons. Use the Inter font (imported from Google Fonts).
The page has a white background (bg-white), max-width max-w-7xl, centered.
```
> ANNOTATION: Minimalist stack — no shadcn/ui or Framer Motion. The style is defined right from the opening: white background, centered.

```
Custom CSS animations (in index.css):
@keyframes fadeInUp -- from opacity: 0; transform: translateY(30px) to
  opacity: 1; transform: translateY(0).
Class .animate-fade-in-up uses this with 0.6s ease-out forwards.
[...]
Every major section uses .animate-fade-in-up with staggered animationDelay
inline styles (starting at 0.1s and incrementing by 0.1s).
Each element starts with opacity: 0 inline so the animation fills it to visible.
```
> ANNOTATION: The animations are specified in detail, including the staggering logic. The "Each element starts with opacity: 0" is crucial — without it, the elements flash before the animation.

```
HERO SECTION (px-6 pt-24 pb-32 max-w-7xl mx-auto text-center):
Reviews Badge (delay: 0.2s): inline-flex items-center gap-2 mb-8.
  Contains a bordered square (w-6 h-6 border border-gray-300 rounded)
  with a filled Star icon inside, plus "4.9 rating from 18.3K+ users"
```
> ANNOTATION: The social-proof badge is described with the exact dimensions of the star icon and the real text. Not "add a reviews badge".

```
Tab Bar (delay: 0.6s): Centered bg-gray-100 rounded-lg p-1 container.
Tabs auto-cycle every 4s using setInterval. State: useState('analyse').
Mobile (md:hidden): 2x2 grid with 4 buttons.
Desktop (hidden md:flex): Same 4 buttons in row with vertical dividers.
```
> ANNOTATION: The interactive behavior is specified (auto-cycle 4s, useState). The responsive layout differs between mobile (2x2 grid) and desktop (row).

---

## Example 3 — Full Editorial Landing Page (Mindloop style)

**Original brief:** Newsletter/content platform, dark monochrome, editorial, scroll animations.
**Length:** ~7200 chars | **Type:** Complete landing page (7 sections)

This prompt is the longest and most complete. Key points:

**Structure in 7 numbered sections:**
1. Navbar (fixed, transparent)
2. Hero Section (full viewport)
3. "Search has changed" Section
4. Mission Section (scroll word reveal)
5. Solution Section
6. CTA Section (HLS video background)
7. Footer

> ANNOTATION: The numbering helps the LLM structure the code. Each section is self-contained.

**Explicit dependencies:**
```
Key Dependencies:
framer-motion for all animations
hls.js for the CTA background video streaming
@fontsource/inter (400, 500, 600, 700)
@fontsource/instrument-serif (400, 400-italic)
lucide-react for icons
tailwindcss-animate plugin
```
> ANNOTATION: The "dependencies" section at the end prevents forgotten imports.

**Assets listed:**
```
Assets Needed:
3 avatar images (avatar-1.png, avatar-2.png, avatar-3.png)
3 platform icons (icon-chatgpt.png, icon-perplexity.png, icon-google.png)
```
> ANNOTATION: The LLM knows which assets it must create or use as placeholders.

**Scroll word reveal (the premium feature):**
```
Scroll-driven word-by-word reveal using useScroll and useTransform:
Each word transitions opacity from 0.15 to 1 based on scroll progress.
```
> ANNOTATION: The most complex effect is described in terms of behavior, not implementation. The LLM chooses how to implement useScroll/useTransform.

---

## Recurring patterns in effective prompts

1. **Always specify the real text content** — headlines, subtitles, button labels, link names
2. **Always give the exact Tailwind classes** for sizing and spacing
3. **Always define the responsive behavior** (hidden on mobile, md:flex, etc.)
4. **Always include a "what NOT to do" section** to avoid bloat
5. **Always list the dependencies** at the end of the prompt
6. **Describe animations in complete CSS** rather than natural language
7. **Provide asset URLs** whenever possible (videos, images)
