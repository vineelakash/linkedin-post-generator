# Workflow Guide & Operational Manual

This guide walks through configuring your environment, running automated scheduling batches from the content calendar, creating instant thought leadership posts, and performing in-place live edits.

---

## 1. Prerequisites & Setup

### 1.1 Python Dependencies
Install the required dependencies in a virtual environment:

```bash
git clone https://github.com/your-username/linkedin-post-generator.git
cd linkedin-post-generator
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS / Linux:
source venv/bin/activate

pip install -r requirements.txt
playwright install chromium
```

### 1.2 Chrome Remote Debugging Setup
To allow the automation engine to schedule and post without triggering 2FA challenges or bot detection, run Google Chrome with remote debugging enabled:

**Windows (PowerShell / Command Prompt):**
```powershell
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\ChromeDebugProfile"
```

**macOS (Terminal):**
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-debug"
```

**Linux (Terminal):**
```bash
google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-debug"
```

> **Note:** Once Chrome launches, log into your LinkedIn account manually once. The automation script will connect to this persistent session.

### 1.3 Environment Variables
Copy `.env.example` to `.env` and adjust settings as needed:
```bash
cp .env.example .env
```

---

## 2. Workflow A: Content Calendar Batch Scheduling

The system includes a 20-post sequence covering operations, pipeline leakage, after-hours AI, and database monetization.

### Step 1: Inspect Calendar & Tracker
View all posts, scheduled times, and statuses:
```bash
python -m generator.content_calendar_scheduler --list
```

### Step 2: Validate & Dry-Run a Post
Preview copy validation, zero-dollar rule verification, and image resolution without touching LinkedIn:
```bash
python -m generator.content_calendar_scheduler --post-id 3
```

### Step 3: Live Scheduling on LinkedIn
Connect to your active Chrome browser and schedule the post at its designated date/time:
```bash
python -m generator.content_calendar_scheduler --post-id 3 --execute
```

To specify an explicit date and time:
```bash
python -m generator.content_calendar_scheduler --post-id 3 --schedule-time "Oct 15, 2026 10:00 AM" --execute
```

---

## 3. Workflow B: Instant On-Demand Post Generator

When you have a quick insight, case study, or contrarian takeaway:

### Step 1: Dry-Run Copy & Auto-Generate 1:1 Cover Graphic
```bash
python -m generator.instant_post_generator \
  --headline "Speed Over Savings" \
  --body "We spent 3 weeks trying to shave 20% off software costs. We lost 10x that in execution delay. Optimize for throughput, not penny-pinching." \
  --category "FOUNDER LESSON"
```

This will:
1. Run the copy through the Anti-Cliché and Zero-Dollar filters.
2. Synthesize a 1200x1200px 1:1 square cover card (`assets/sample/sample_cover.png`) using Pillow.
3. Print a draft preview for your review.

### Step 2: Publish Live Immediately
```bash
python -m generator.instant_post_generator \
  --headline "Speed Over Savings" \
  --body "We spent 3 weeks trying to shave 20% off software costs. We lost 10x that in execution delay. Optimize for throughput, not penny-pinching." \
  --category "FOUNDER LESSON" \
  --publish
```

### Step 3: Schedule for a Specific Time
```bash
python -m generator.instant_post_generator \
  --headline "Speed Over Savings" \
  --body "We spent 3 weeks trying to shave 20% off software costs. We lost 10x that in execution delay. Optimize for throughput, not penny-pinching." \
  --category "FOUNDER LESSON" \
  --schedule "Nov 02, 2026 09:30 AM"
```

---

## 4. Workflow C: In-Place Live Editing

If a live post contains a typo, updated link, or you want to refine the hook without deleting the post or losing existing engagement:

```bash
python -m generator.instant_post_generator \
  --edit-url "https://www.linkedin.com/feed/update/urn:li:activity:7123456789012345678/" \
  --new-copy "Updated post text goes here with corrected details."
```

The browser controller will:
1. Navigate directly to the post URL.
2. Locate the post control dropdown (`...`).
3. Click **Edit post**.
4. Replace the text in the editor.
5. Click **Save** and verify the updated content.

---

## 5. Visual Prompt Synthesis for External AI Generators

If you prefer using Midjourney, DALL-E 3, or Flux instead of the offline Pillow generator:

```python
from generator.visual_prompt_engine import VisualPromptEngine

engine = VisualPromptEngine()
prompts = engine.generate_prompt_sequence(
    topic_title="After-Hours Lead Intake",
    core_concept="Comparison of 9:47 PM missed call vs instant conversational AI qualification",
    cta_keyword="AFTERHOURS"
)

print(prompts["image_1_hero"])
print(prompts["image_2_infographic"])
print(prompts["image_3_cta"])
```
Paste the outputs into your image generator of choice and place the resulting files in `assets/`.
