# Visual Assets Directory

This directory stores visual media assets used by the **LinkedIn Post Generator** engine.

---

## 1. Specifications & Standards

| Parameter | Specification | Notes |
| :--- | :--- | :--- |
| **Aspect Ratio** | `1:1` Square | Optimal for mobile LinkedIn feed visibility |
| **Dimensions** | `1200 x 1200 px` | Crisp display on Retina & high-DPI displays |
| **Format** | `PNG` or `JPEG` | Minimum file size > 50 KB |
| **Theme** | Dark B2B SaaS (`#0B0F17`) | High contrast, obsidian background, cyan/emerald accents |
| **Typeface** | Sans-Serif Bold | Modern, legible, executive tone |

---

## 2. Naming Conventions

For the 20-post content calendar, image assets are resolved automatically using the following pattern in `assets/`:

- **Hero Slide:** `post_{id:02d}_hero.png` (e.g. `post_01_hero.png`)
- **Infographic Flow:** `post_{id:02d}_infographic.png` (e.g. `post_01_infographic.png`)
- **Call-to-Action:** `post_{id:02d}_cta.png` (e.g. `post_01_cta.png`)

For on-demand instant posts:
- Default output location: `assets/sample/sample_cover.png`

---

## 3. Generating Offline Cover Cards

You can generate sample 1200x1200px cards instantly without any external image API:

```python
from generator.visual_prompt_engine import VisualPromptEngine

engine = VisualPromptEngine()
image_path = engine.create_offline_cover_image(
    headline="Your Headline Goes Here",
    category="OPERATIONS",
    output_path="assets/sample/sample_cover.png"
)
print(f"Generated at: {image_path}")
```
