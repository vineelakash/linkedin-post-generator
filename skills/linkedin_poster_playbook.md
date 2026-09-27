---
name: linkedin_poster
description: Autonomous multi-profile workflow to generate, humanize (via Claude /humanizer), visualize (Cover Pages & Infographics via ChatGPT/Pillow), and publish/schedule LinkedIn posts.
version: 2.1.0
tags:
  - linkedin
  - content-generation
  - claude
  - humanizer
  - chatgpt
  - browser-automation
  - multi-profile
---

# Autonomous LinkedIn Content & Multi-Profile Browser Workflow

## 1. Browser Profile Routing Architecture (CRITICAL RULE)

To prevent session conflicts and account mismatch, the workflow strictly isolates tasks across two dedicated Google Chrome profiles or attaches to active sessions:

| Service / Platform | Purpose | Chrome Profile Directory | Account Email |
| :--- | :--- | :--- | :--- |
| **Claude AI** (`https://claude.ai/`) | Post Copy Generation & `/humanizer` Execution | `--profile-directory="Default"` | `generation_user@example.com` |
| **ChatGPT** (`https://chatgpt.com/`) | 1:1 SaaS Visuals / Cover Page / Infographics | `--profile-directory="Default"` | `generation_user@example.com` |
| **LinkedIn** (`https://www.linkedin.com/`) | Media Upload, Immediate Posting & Scheduling | `--profile-directory="Profile 1"` | `publishing_user@example.com` |

---

## 2. DevTools WebSocket Discovery Protocol

Newer Chrome versions (130+) reject `http://localhost:9222/json`. Always read the active browser endpoint directly from:
`C:\Users\Vinee\AppData\Local\Google\Chrome\User Data\DevToolsActivePort`

```python
from pathlib import Path

def get_cdp_ws_url():
    port_file = Path(r"C:\Users\Vinee\AppData\Local\Google\Chrome\User Data\DevToolsActivePort")
    with open(port_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return f"ws://127.0.0.1:{lines[0]}{lines[1]}"
```

---

## 3. Claude `/humanizer` Execution Standard

When generating copy in Claude (`https://claude.ai/new`):
1. **Always invoke `/humanizer` explicitly** in the prompt box with the draft story/brief.
2. **Enforce anti-AI constraints:** Ban clichés like *"game-changer"*, *"testament"*, *"tapestry"*, *"in today's fast-paced world"*, *"supercharge"*, *"dive in"*.
3. **Pacing:** Short 1–2 sentence paragraphs for mobile scannability, raw founder vulnerability, tangible stakes, and an engagement question.

---

## 4. Visual Asset Formats: Cover Pages vs. Carousel Infographics

1. **Cover Page / Hero Visual (Single Image Posts):**
   - 1:1 Square (1200x1200px) or 4:5 Portrait.
   - Dark mode slate (`#0B0F17`), large punchy typography, eyebrow badge (`OPERATOR PERSPECTIVE`), 2 asymmetric comparison cards (Cost Friction vs. Leverage), and a crisp footer heuristic.
2. **Carousel Infographics (Multi-Slide Systems):**
   - Hero frame + Process/Architecture diagram + Closing CTA pill.

---

## 5. LinkedIn Publishing Protocol

1. Connect to active LinkedIn session over DevTools WebSocket.
2. If composer modal is already open, proceed directly without re-clicking.
3. Attach visual asset(s) via `expect_file_chooser()` on the Media button.
4. Fill post copy into `div[role='textbox']`.
5. **Immediate Post:** Click `"Post"` directly.
6. **Scheduled Post:** Click schedule clock (`a[aria-label='Scheduled']`), configure date/time, confirm, and click `"Schedule"`.
7. Save verification screenshot to `Logs/`.
