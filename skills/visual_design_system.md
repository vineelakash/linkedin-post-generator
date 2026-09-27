# Visual Design System — LinkedIn 3-Image Framework

## 1. Design Philosophy: The \$10M+ B2B SaaS Aesthetic

Every post on LinkedIn must look and feel like it was crafted by the design team of a tier-1 fintech / enterprise SaaS company (e.g., Stripe, Ramp, Linear, Retool).

### Core Brand Principles
* **Minimalist & High Signal:** Zero visual fluff. Every line, badge, and word has an architectural purpose.
* **Dark Theme Dominance:** Deep charcoal and obsidian slate backgrounds convey authority, security, and technical maturity.
* **Typographic Hierarchy:** Large, crisp, geometric sans-serif type that is immediately readable on mobile feeds without pinching.
* **Generous Negative Space:** 40%+ of the canvas should remain uncluttered breathing room.
* **Subtle Structural Grids:** Thin hairline borders (0.5px - 1px) with low opacity (10-20%), subtle pill badges, and restrained UI cards.

---

## 2. Color Palette & Typography

### Hex Color Tokens
| Element | Hex Code | Purpose |
| :--- | :--- | :--- |
| **Canvas Background** | `#0B0F17` / `#0D1117` | Deep obsidian slate base |
| **Surface Card** | `#161E2E` / `#1E293B` | Slightly elevated background for flow nodes |
| **Border / Grid Line** | `#334155` (15% - 30% alpha) | Hairline separators and flow connectors |
| **Primary Typography** | `#F8FAFC` (Pure/Off-White) | High-contrast headlines and focal points |
| **Secondary Typography** | `#94A3B8` (Cool Grey) | Supporting labels, subtitles, metadata |
| **Accent Primary (Emerald)** | `#10B981` | Positive outcomes, AI workflow path, recovered revenue |
| **Accent Secondary (Cyan)** | `#06B6D4` | System processes, data flow, active states |
| **Accent Alert (Rose/Amber)** | `#F43F5E` / `#F59E0B` | Problem leakage, manual friction, stalled file alerts |

### Typography Guidelines
* **Font Families:** `Plus Jakarta Sans`, `Inter`, `SF Pro Display`, `Geist Sans`.
* **Hero Headline:** 56px – 72px Bold / ExtraBold (Mobile readable in feed).
* **Card / Node Title:** 24px – 32px SemiBold.
* **Supporting Labels:** 16px – 20px Medium.
* **Case:** Sentence case for headlines; UPPERCASE for micro-badges and tags.

---

## 3. The 3-Image Carousel Structure

```
┌────────────────────────┐  ┌────────────────────────┐  ┌────────────────────────┐
│      IMAGE 1: HERO     │  │  IMAGE 2: INFOGRAPHIC  │  │      IMAGE 3: CTA      │
│                        │  │                        │  │                        │
│   [ Micro Tag Badge ]  │  │   [ Problem vs System] │  │   [ Closing Question ] │
│                        │  │                        │  │                        │
│     "YOUR LEADS        │  │   Step 1 ──> Step 2    │  │   "How many leads      │
│      AREN'T THE        │  │      │          │      │  │    are waiting?"       │
│       PROBLEM."        │  │      ▼          ▼      │  │                        │
│                        │  │   Step 3 ──> Outcome   │  │   [ DM "LEAD" ]        │
│   [ Subtle Accent Line]│  │                        │  │                        │
└────────────────────────┘  └────────────────────────┘  └────────────────────────┘
```

### Image 1: Hero Frame (The Curiosity Anchor)
* **Goal:** Stop the scroll in the first 0.5 seconds.
* **Content:** 1 bold, provocative statement or contrarian observation.
* **Layout:** Centered or left-aligned massive headline, small top category pill (e.g. `MORTGAGE OPERATIONS` or `P&C AGENCY REVENUE`), clean background with subtle linear grid.

### Image 2: Infographic Frame (The Operational Logic)
* **Goal:** Visually contrast the manual breakdown against the AI automation layer.
* **Content:** Flow diagram, 2-column comparison, or economic formula.
* **Layout:** Modular UI cards connected by glowing directional lines (`──>`). Clear designation of what AI executes vs where the licensed human steps in.

### Image 3: CTA Frame (The Conversion Trigger)
* **Goal:** Provoke self-diagnosis and invite direct conversation.
* **Content:** Diagnostic question + explicit DM keyword trigger.
* **Layout:** Minimalist frame, high contrast center text, clean pill badge at the bottom.

---

## 4. Strict "Do NOT" Rules

* ❌ **NO generic AI robots, android hands, or cyborg illustrations.**
* ❌ **NO glowing neon "AI brain" stock vectors.**
* ❌ **NO cheesy 3D cartoon characters or corporate Memphis clip art.**
* ❌ **NO stock photos of people in suits smiling at laptops.**
* ❌ **NO garish multi-color rainbow gradients.**
* ❌ **NO wall of unreadable small text.**
* ❌ **NO more than ONE core idea per visual frame.**

---

## 5. Master AI Prompt Templates (For ChatGPT DALL-E / Midjourney)

### Hero Image Prompt Formula
```text
A minimal, ultra-premium B2B SaaS graphic with a 1:1 aspect ratio. Deep dark charcoal and obsidian slate background (#0B0F17) with very subtle dark grey grid lines. Large, crisp, modern white sans-serif typography in the center reading: "[HERO TEXT]". Clean layout, generous negative space, high contrast, sophisticated fintech dashboard aesthetic, a single subtle emerald green (#10B981) accent line under the headline. No 3D objects, no cartoons, no robots, no stock photos. Clean, authoritative, executive presentation.
```

### Infographic Image Prompt Formula
```text
A sleek, modern B2B SaaS workflow diagram infographic with a 1:1 aspect ratio. Dark slate grey background (#0B0F17). Clean horizontal flow of dark UI cards connected by thin subtle cyan and emerald lines: [CARD 1: INPUT] -> [CARD 2: AI OPERATION] -> [CARD 3: LICENSED HUMAN DECISION] -> [CARD 4: MEASURABLE OUTCOME]. High-contrast typography in pure white and muted slate. Minimalist fintech UI aesthetic, precise alignment, plenty of negative space. No clutter, no cartoons, no generic robot imagery.
```

### CTA Image Prompt Formula
```text
A minimal, high-impact B2B closing slide with a 1:1 aspect ratio. Dark obsidian slate background (#0B0F17) with very subtle ambient dark cyan lighting. Centered crisp white typography reading: "[CTA QUESTION]". Below it, a sleek dark pill container with emerald green border and text reading: "[DM ACTION KEYWORD]". Generous negative space, sophisticated enterprise SaaS aesthetic, crisp vector finish.
```
