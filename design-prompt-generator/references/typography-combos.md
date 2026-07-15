# Typography pairings

Tested font pairings that produce premium results in design prompts. Each combo includes the exact import and the required weights.

## How to choose

| Mood | Display font type | Examples |
|------|---------------------|----------|
| Elegant, editorial | Classic serif | Instrument Serif, Playfair Display, Source Serif 4 |
| Modern, tech | Geometric sans | General Sans, Satoshi, Geist Sans |
| Bold, impact | Display/condensed | Bebas Neue, Oswald, Anton |
| Luxury, refined | Thin serif | Cormorant Garamond, Noto Serif Display |
| Playful, friendly | Rounded sans | Nunito, Outfit, DM Sans |
| Brutalist, raw | Monospace/slab | JetBrains Mono, Roboto Slab, IBM Plex Mono |

---

## Combo 1 — Instrument Serif + Inter (the most popular)

The signature MotionSites combo. Elegant, readable, versatile.

```
Import from Google Fonts: Instrument Serif (display) and Inter weights 400/500 (body)
CSS variables: --font-display: 'Instrument Serif', serif and --font-body: 'Inter', sans-serif
Body uses var(--font-body), headings use inline fontFamily: "'Instrument Serif', serif"
```

Usage: serif italic words inside a sans-serif heading create a premium contrast.
E.g. "Get *Inspired* with Us" — "Inspired" in Instrument Serif italic.

## Combo 2 — Geist Sans (mono-font)

For a modern tech/product look. A single font family; the hierarchy comes from the weights.

```
Install @fontsource/geist-sans
Import weights: 400, 500, 600, 700
@import "@fontsource/geist-sans/400.css";
@import "@fontsource/geist-sans/500.css";
@import "@fontsource/geist-sans/600.css";
@import "@fontsource/geist-sans/700.css";
Body font: 'Geist Sans', 'Inter', system-ui, sans-serif
```

## Combo 3 — Poppins + Source Serif 4

Rounded display + serif for accents. Approachable and refined.

```
Import from Google Fonts: Poppins weights 400/500/600 (display/body) and Source Serif 4 weight 400/400-italic (accent)
Headings use font-weight: 500
Serif accent: Source Serif 4 used only for italic/emphasis inside headings (<em>, <i>)
```

## Combo 4 — General Sans + Inter

Clean, modern, professional. General Sans brings character without being too bold.

```
Import General Sans via @fontsource or CDN (weights 400, 500, 600)
Body font: 'Inter', sans-serif
Display font: 'General Sans', sans-serif
```

Note: General Sans is not on Google Fonts. Use @fontsource or a self-hosted CDN.

## Combo 5 — Playfair Display + DM Sans

Luxury and strong contrast. Ornamental serif + geometric sans-serif.

```
Import from Google Fonts: Playfair Display weights 400/700 (display) and DM Sans weights 400/500 (body)
CSS: --font-display: 'Playfair Display', serif; --font-body: 'DM Sans', sans-serif
```

## Combo 6 — Space Grotesk + Inter

Geometric with character. Perfect for tech/AI products.

```
Import from Google Fonts: Space Grotesk weights 400/500/600/700 (display) and Inter weights 400/500 (body)
CSS: --font-display: 'Space Grotesk', sans-serif; --font-body: 'Inter', sans-serif
```

## Combo 7 — Bebas Neue + Inter

Maximum impact. For bold heroes, sports, events.

```
Import from Google Fonts: Bebas Neue weight 400 (display) and Inter weights 400/500 (body)
Heading style: uppercase, letter-spacing wide, text-8xl+
CSS: --font-display: 'Bebas Neue', sans-serif; --font-body: 'Inter', sans-serif
```

## Combo 8 — Cormorant Garamond + Lato

Ultra-elegant. Perfect for luxury, fashion, high-end real estate.

```
Import from Google Fonts: Cormorant Garamond weights 300/400/600 (display) and Lato weights 300/400 (body)
CSS: --font-display: 'Cormorant Garamond', serif; --font-body: 'Lato', sans-serif
```

## Combo 9 — Outfit + Inter

Modern, friendly, startup-friendly. Rounded sans without being childish.

```
Import from Google Fonts: Outfit weights 400/500/600/700 (display) and Inter weights 400/500 (body)
CSS: --font-display: 'Outfit', sans-serif; --font-body: 'Inter', sans-serif
```

## Combo 10 — Syne + Inter

Bold, creative, a little edgy. Perfect for agencies and portfolios.

```
Import from Google Fonts: Syne weights 400/500/600/700/800 (display) and Inter weights 400/500 (body)
CSS: --font-display: 'Syne', sans-serif; --font-body: 'Inter', sans-serif
```

---

## Pattern: the "italic serif accent"

A recurring pattern in premium prompts: insert an italic serif word in the middle of a sans-serif heading. It creates an elegant focal point.

```
H1: "Where dreams rise through the silence."
— "dreams" and "through the silence." wrapped in <em className="not-italic text-muted-foreground">
— The <em> font-family is Instrument Serif italic
— The rest of the heading is in Inter/Geist
```

This pattern works with any serif + sans-serif pairing.

---

## Standard type sizes

For a hero section, use this responsive scaling:
```
H1: text-5xl sm:text-6xl md:text-7xl lg:text-8xl
H2: text-3xl sm:text-4xl md:text-5xl lg:text-6xl
Subtitle: text-base sm:text-lg md:text-xl
Body: text-sm sm:text-base
Nav links: text-sm
CTA button: text-sm or text-base
```

Tracking (letter-spacing) for large headings:
```
tracking-tight (H1 < 60px)
tracking-[-2px] ou tracking-[-2.46px] (H1 > 60px)
tracking-[3px] uppercase (labels, overlines)
```
