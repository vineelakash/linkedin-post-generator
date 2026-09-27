---
name: instant_linkedin_posts
description: Complete workflow to create, humanize (via Claude /humanizer), design cover pages, publish immediately, and edit live personal experience and founder insight posts on LinkedIn.
version: 1.0.0
tags:
  - linkedin
  - instant-posts
  - founder-insights
  - humanizer
  - claude
  - cover-pages
  - live-editing
---

# Instant LinkedIn Posts — Personal Experience & Founder Insights

## 1. Overview & System Separation

Unlike the **Founder Content Calendar** (which focuses on scheduled business marketing and the 3-Image Carousel System for ICP AI operations), **Instant LinkedIn Posts** focus on:
* **Personal Founder Experiences:** Real stories, mistakes, near-misses, high-stakes decisions.
* **Mental Models & Asymmetric Risk:** Reflections on speed, leverage, frugality, operations, and leadership.
* **Immediate Live Publishing:** Published right away (not scheduled in the calendar queue).
* **Single Cover Page Asset:** Minimalist, high-contrast dark B2B SaaS cover slide (1:1 aspect ratio).

---

## 2. Profile Routing & WebSocket Discovery

1. **Generation Profile (`generation_user@example.com` / `Default`):**
   * Used for Claude AI (`https://claude.ai/new`) to run `/humanizer` on raw drafts.
2. **Publishing Profile (`publishing_user@example.com` / `Profile 1` or Active Session):**
   * Used for LinkedIn (`https://www.linkedin.com/`) for media upload, live posting, and editing.
3. **Chrome DevTools Connection:**
   * Read the active WebSocket URL from `C:\Users\Vinee\AppData\Local\Google\Chrome\User Data\DevToolsActivePort`.

---

## 3. The 4-Stage Execution Workflow

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐     ┌────────────────┐
│ 1. Raw Brief /  │ ──> │ 2. Claude AI     │ ──> │ 3. 1:1 Cover    │ ──> │ 4. Live Post / │
│    Experience   │     │    /humanizer    │     │    Page Slide   │     │    In-Place    │
│    Story        │     │    Refinement    │     │    Renderer     │     │    Editing     │
└─────────────────┘     └──────────────────┘     └─────────────────┘     └────────────────┘
```

### Stage 1: Content Creation via Claude (`/humanizer`)
* Open `https://claude.ai/new`.
* Pass `/humanizer` alongside the raw story brief.
* **Strict Anti-AI Rules:**
  - Zero corporate buzzwords (*"game-changer"*, *"testament"*, *"tapestry"*, *"dive in"*, *"crucial"*).
  - Short 1–2 sentence paragraphs for mobile scannability.
  - Authentic emotional stakes, vulnerability, and specific sensory details.
  - Clean currency formatting (avoid dollar signs if requested: e.g. `50k`, `eighteen bucks`, `24`).
  - Conclude with a punchy one-line rule and an engaging founder question.

### Stage 2: Cover Page Slide Generation
* Render a 1200 × 1200 px (1:1 square) image in `assets/` adhering to the dark B2B SaaS design framework:
  - Background: Obsidian slate (`#0B0F17`) with rounded inner container (`#0F1523`).
  - Top Badge: `OPERATOR PERSPECTIVE` (`#34D399` on `#0D2820`).
  - Massive Headline: 64pt high-contrast typography emphasizing the tension/mistake and stakes.
  - Asymmetric Comparison Cards: Left card (Cost Friction / Downside) vs. Right card (Leverage / Upside).
  - Footer Heuristic Pill: Grounded founder rule.

### Stage 3: Immediate Live Publishing
* Connect to active LinkedIn session over DevTools WebSocket.
* Open composer, attach the single Cover Page slide via `expect_file_chooser()`.
* Inject the Claude-humanized post text into `div[role='textbox']`.
* Click **`"Post"` immediately** (do NOT click schedule).
* Save confirmation screenshot in `Logs/`.

### Stage 4: Live In-Place Post Editing
* When edits or corrections are needed on live posts:
  1. Navigate to `https://www.linkedin.com/in/me/recent-activity/all/`.
  2. Click the 3-dots control menu on the top post (`button.feed-shared-control-menu__trigger`).
  3. Click `Edit post` from the dropdown list.
  4. In the edit modal, locate `div.ql-editor[contenteditable='true']`.
  5. Select all, type the updated copy, and click `Save` (`button:has-text('Save')`).
  6. Confirm and capture verification screenshot.
