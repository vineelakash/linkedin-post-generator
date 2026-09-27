# System Architecture

The **LinkedIn Post Generator** is an autonomous, open-source publishing framework designed for founders, agency operators, and B2B tech leaders. It pairs programmatic copy generation, visual design synthesis, and Chrome DevTools Protocol (CDP) browser automation to deliver reliable scheduled campaigns and instant thought leadership posts.

---

## 1. High-Level Architecture Diagram

```mermaid
flowchart TD
    subgraph Input ["1. Ingestion & Briefing"]
        A1["20-Post Content Calendar<br/>(Markdown + Frontmatter)"]
        A2["Instant Story Brief<br/>(Raw Thoughts & Notes)"]
    end

    subgraph Processing ["2. Copywriting & Calibration Engine"]
        B1["Copy Humanizer"]
        B2["Anti-Cliché Filter<br/>(Bans 'game-changer', 'delve', etc.)"]
        B3["Zero-Dollar Rule Validator<br/>(Converts currency to operational metrics)"]
        B1 --> B2
        B1 --> B3
    end

    subgraph Visuals ["3. Visual Design System"]
        C1["Visual Prompt Engine<br/>(#0B0F17 Dark B2B Aesthetic)"]
        C2["3-Image Sequential Suite<br/>(Hero / Infographic / CTA)"]
        C3["Offline Pillow Generator<br/>(1200x1200px 1:1 Cover Cards)"]
        C1 --> C2
        C1 --> C3
    end

    subgraph Automation ["4. CDP Browser Automation Layer"]
        D1["BrowserController<br/>(Playwright via Chrome Remote Debugging)"]
        D2["Media Uploader<br/>(Sequential Asset Attachment)"]
        D3["Scheduler Modal Driver<br/>(Date & Time DOM Evaluation)"]
        D4["Live In-Place Post Editor<br/>(Update Active Posts Without Deleting)"]
        D1 --> D2
        D1 --> D3
        D1 --> D4
    end

    subgraph Output ["5. Publishing & Verification"]
        E1["LinkedIn Feed & Scheduled Queue"]
        E2["Confirmation Screenshots & Logs"]
        E3["JSON / Markdown Campaign Tracker"]
    end

    A1 --> B1
    A2 --> B1
    B1 --> C1
    B1 --> D1
    C2 --> D2
    C3 --> D2
    D3 --> E1
    D4 --> E1
    D1 --> E2
    D1 --> E3
```

---

## 2. Core Components

### 2.1 Content Calendar Framework (`content_calendar/`)
- **20 Pre-Built Posts:** Ready-to-publish mortgage and insurance operations posts covering pipeline leakage, CRM reactivation, after-hours AI intake, document chasing, renewal automation, and operational debt.
- **Tracker Engine (`tracker.json` & `TRACKER.md`):** State persistence tracking post lifecycle (`draft` → `staged` → `scheduled` → `published`).

### 2.2 Copy Humanizer & Style Enforcer (`generator/copy_humanizer.py`)
- **Anti-Cliché Filtering:** Programmatically blocks robotic corporate jargon (`game changer`, `dive deep`, `delve`, `revolutionize`, `supercharge`, `tapestry`, `leverage`).
- **The Zero-Dollar Rule:** Enforces the elimination of raw `$` symbols, reframing discussions around hours saved, pipeline capacity, conversion percentages, or operational efficiency.
- **Mobile Readability Rules:** Guarantees punchy 1-2 sentence beats, short hook lines (<90 characters), and clean footer hashtags (max 2-3).

### 2.3 Visual Design Engine (`generator/visual_prompt_engine.py`)
- **B2B SaaS Theme Tokens:** Consistent color schemes featuring Obsidian Dark (`#0B0F17`), Cyber Slate (`#161F30`), Electric Cyan (`#00F0FF`), and Emerald Green (`#10B981`).
- **3-Image Visual Sequences:**
  1. *Hero Slide:* High-contrast contrarian question or bold hook.
  2. *Infographic Diagram:* Operational flow, comparison matrix, or node-and-arrow system map.
  3. *Call to Action:* High-curiosity question paired with a specific DM keyword.
- **Built-in Pillow Generator:** Generates 1200x1200px 1:1 square cover graphics completely offline with no external API keys required.

### 2.4 Browser Automation Layer (`generator/browser_controller.py`)
- **Chrome Remote Debugging Protocol (CDP):** Connects to a persistent user Chrome session (port 9222) via Playwright. Avoids repeated 2FA challenges, prevents session invalidation, and preserves user login state.
- **Sequential Multi-Image Upload:** Attaches up to 3 visual assets in strict order (Hero → Infographic → CTA).
- **Date & Time Picker Automation:** Interacts with LinkedIn's scheduling dialog with zero flakiness.
- **In-Place Live Editing:** Modifies published post text directly via the feed interface without deleting the post or losing existing comments/reactions.

---

## 3. Data & Privacy Safeguards

- **Zero Hardcoded Secrets:** All configuration is managed via `.env` or `config/settings.json`.
- **Zero Personal Data:** The repository contains only generic, professional examples. No real user identifiers, emails, API keys, or private profiles are committed.
- **Non-Destructive Execution:** The browser automation connects to existing sessions without terminating browsers or modifying local browser profiles.
