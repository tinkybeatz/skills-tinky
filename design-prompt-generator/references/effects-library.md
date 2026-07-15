# Visual effects and animations library

Each effect is provided as complete CSS, ready to drop into a prompt. Never describe an effect in natural language ("add a glass effect") — always include the exact CSS.

---

## Visual effects

### 1. Liquid Glass (the most versatile)

The signature MotionSites effect. Works on any dark background with content behind it.

**Light version (navbar, buttons, pills):**
```css
.liquid-glass {
  background: rgba(255, 255, 255, 0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: none;
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}
.liquid-glass::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,
    rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
```

**Strong version (cards, panels, CTAs):**
```css
.liquid-glass-strong {
  background: rgba(255, 255, 255, 0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(50px);
  -webkit-backdrop-filter: blur(50px);
  border: none;
  box-shadow: 4px 4px 4px rgba(0,0,0,0.05),
    inset 0 1px 1px rgba(255,255,255,0.15);
  position: relative;
  overflow: hidden;
}
.liquid-glass-strong::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.5) 0%, rgba(255,255,255,0.2) 20%,
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,
    rgba(255,255,255,0.2) 80%, rgba(255,255,255,0.5) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
```

### 2. Gradient Divider

A thin line that fades out at the ends. Perfect under the navbar.

```css
/* In Tailwind: */
w-full h-px bg-gradient-to-r from-transparent via-foreground/20 to-transparent
```

### 3. Video Background with fade

Fullscreen video with a gradient overlay for text legibility.

```
Background Video:
<video> element: autoPlay muted playsInline loop
  absolute inset-0 w-full h-full object-cover z-0

Gradient overlays (above the video, below the content):
  absolute inset-0 bg-gradient-to-b from-background via-transparent to-background
```

**Version with fade in/out on each loop:**
```
Fade logic (JavaScript): Use requestAnimationFrame to continuously read
currentTime and duration. Fade in over 0.5s at the start, fade out over
0.5s at the end. On ended, set opacity to 0, wait 100ms, reset
currentTime = 0, and play() again.
```

### 4. Gradient Text

Text with a gradient. Use sparingly (1 heading max).

```css
/* In Tailwind: */
bg-gradient-to-r from-[#E8E8E9] to-[#3A7BBF] bg-clip-text text-transparent

/* Or for a subtler gradient: */
bg-gradient-to-b from-foreground to-muted-foreground bg-clip-text text-transparent
```

### 5. Grain/Noise Texture

A subtle texture that adds depth. Use as a low-opacity overlay.

```css
.grain::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 1;
}
```

### 6. Subtle Glow

A soft glow behind an element. More elegant than a classic drop-shadow.

```css
.glow {
  box-shadow: 0 0 60px rgba(var(--primary), 0.15),
    0 0 120px rgba(var(--primary), 0.05);
}
```

### 7. Dot Grid Pattern

A background with a grid of dots. Minimal/tech style.

```css
.dot-grid {
  background-image: radial-gradient(circle, hsl(var(--border)) 1px, transparent 1px);
  background-size: 24px 24px;
}
```

---

## Animations

### Fade Rise (the standard)

The most versatile entrance animation. Stagger the elements for a cinematic effect.

```css
@keyframes fade-rise {
  from { opacity: 0; transform: translateY(24px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-rise { animation: fade-rise 0.8s ease-out both; }
.animate-fade-rise-delay { animation: fade-rise 0.8s ease-out 0.2s both; }
.animate-fade-rise-delay-2 { animation: fade-rise 0.8s ease-out 0.4s both; }
.animate-fade-rise-delay-3 { animation: fade-rise 0.8s ease-out 0.6s both; }
```

Usage in the prompt:
```
H1 gets animate-fade-rise
Subtext gets animate-fade-rise-delay
CTA button gets animate-fade-rise-delay-2
```

### Fade In Up (variant)

```css
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-up {
  animation: fadeInUp 0.6s ease-out forwards;
}
```

Usage with staggering via inline style:
```
style={{ animationDelay: '0.1s', opacity: 0 }}
style={{ animationDelay: '0.2s', opacity: 0 }}
```

### Logo Marquee

Infinite horizontal scroll for social-proof logos.

```
Tailwind config keyframe:
marquee: { '0%': { transform: 'translateX(0%)' }, '100%': { transform: 'translateX(-50%)' } }
Animation: marquee: "marquee 20s linear infinite"
```

Structure:
```
The logos are duplicated (2x the same list) inside a flex container.
The container animates from 0% to -50% (half = one complete list).
The scroll is seamless because the two lists are identical.
```

### Framer Motion — fadeUp helper

For projects that use Framer Motion. More flexible than pure CSS.

```typescript
const fadeUp = (delay: number) => ({
  initial: { opacity: 0, y: 20 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, margin: "-100px" },
  transition: { duration: 0.6, delay, ease: "easeOut" },
});
```

Usage: `<motion.div {...fadeUp(0.2)}>`

### Scroll-Driven Word Reveal

Each word of a paragraph appears progressively on scroll. A premium editorial effect.

```
Scroll-driven word-by-word reveal using useScroll and useTransform from framer-motion:
Split the paragraph into individual words.
Each word transitions opacity from 0.15 to 1 based on scroll progress.
Highlighted words (keywords) get text-foreground color, rest get text-muted-foreground.
```

### Hover Scale

A simple micro-interaction for buttons and cards.

```
hover:scale-[1.03] transition-transform duration-200
/* or with Framer Motion: */
whileHover={{ scale: 1.03 }}
whileTap={{ scale: 0.98 }}
```

### Tab Auto-Cycle

For sections with tabs (features, use cases).

```
Tabs auto-cycle every 4s using setInterval.
State: useState('tab1')
Each tab has its own overlay/content with fade-in animation.
```

---

## Recommended effect combinations

| Style | Effects to combine |
|-------|-------------------|
| Cinematic dark | Video background + liquid glass + fade-rise |
| Clean minimal | Fade-rise + gradient divider + hover scale |
| Editorial | Scroll word reveal + fade-rise + grain texture |
| Glass premium | Liquid glass strong + video background + gradient text |
| Bold impact | Gradient text + marquee + fade-rise |
| Tech/SaaS | Dot grid + fade-in-up + tab auto-cycle |

**Rule: never more than 3 effects per prompt.** Beyond that, the result is overloaded and the LLM loses its way.
