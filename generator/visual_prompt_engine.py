"""
Visual Prompt Engine & Asset Generator
Generates high-conversion 1:1 image prompts (Hero, Infographic, CTA) following the B2B SaaS Dark Theme (#0B0F17).
Includes an offline PIL/Pillow generator for 1200x1200px cover graphics.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class VisualPromptEngine:
    """
    Produces visual prompt specifications and creates offline 1:1 cover graphics.
    """

    COLOR_PALETTE = {
        "bg_primary": "#0B0F17",       # Obsidian Dark
        "bg_card": "#161F30",          # Cyber Slate
        "accent_cyan": "#00F0FF",      # Electric Cyan
        "accent_emerald": "#10B981",   # Emerald Green
        "accent_amber": "#F59E0B",     # Warning Amber
        "text_primary": "#F8FAFC",     # Bright White
        "text_secondary": "#94A3B8",   # Steel Muted
        "border_subtle": "#1E293B",    # Dark Border
    }

    def generate_prompt_sequence(self, topic_title: str, core_concept: str, cta_keyword: str) -> Dict[str, str]:
        """
        Creates a coordinated 3-image prompt sequence for carousel or multi-image posting.
        Image 1: Bold Hero Visual
        Image 2: Process / Infographic Flow
        Image 3: Conversion CTA Card
        """
        hero_prompt = (
            f"1:1 aspect ratio square visual, ultra-minimalist B2B tech aesthetic. "
            f"Dark mode obsidian background ({self.COLOR_PALETTE['bg_primary']}), crisp subtle slate borders. "
            f"Centered bold typography headline: \"{topic_title}\". "
            f"Accent lighting in electric cyan ({self.COLOR_PALETTE['accent_cyan']}) and cool slate. "
            f"Vector precision, clean typography, executive technology feel, 4k render, no clutter."
        )

        infographic_prompt = (
            f"1:1 aspect ratio square infographic diagram illustrating: \"{core_concept}\". "
            f"Dark slate background ({self.COLOR_PALETTE['bg_card']}), modern node-and-arrow data flow or comparison matrix. "
            f"Left side (Status Quo / Inefficient): Slate tones with amber friction nodes. "
            f"Right side (Optimized Workflow): Vibrant emerald green ({self.COLOR_PALETTE['accent_emerald']}) and cyan accents. "
            f"Clean labels, high legibility, modern SaaS dashboard diagram aesthetic, professional engineering diagram."
        )

        cta_prompt = (
            f"1:1 aspect ratio square call-to-action card. "
            f"Dark obsidian background ({self.COLOR_PALETTE['bg_primary']}) with subtle cyan edge glow. "
            f"Large, high-contrast text prompt: \"Want the workflow breakdown?\". "
            f"Highlighted badge container reading: 'Drop \"{cta_keyword}\" in the comments or DMs'. "
            f"Minimalist UI, crisp vector typography, frictionless layout, executive tone."
        )

        return {
            "image_1_hero": hero_prompt,
            "image_2_infographic": infographic_prompt,
            "image_3_cta": cta_prompt,
        }

    def create_offline_cover_image(
        self,
        headline: str,
        category: str = "WORKFLOW AUTOMATION",
        subtitle: Optional[str] = None,
        output_path: str = "assets/sample/sample_cover.png",
        accent_color: str = "#00F0FF",
    ) -> str:
        """
        Generates an offline 1200x1200px 1:1 square cover card using Pillow.
        Ideal for instant posts without requiring external generative image APIs.
        """
        if not PIL_AVAILABLE:
            raise RuntimeError("Pillow is required for offline image generation. Install with 'pip install Pillow'.")

        out_file = Path(output_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)

        width, height = 1200, 1200
        # Background: Obsidian Dark
        img = Image.new("RGB", (width, height), color=self.COLOR_PALETTE["bg_primary"])
        draw = ImageDraw.Draw(img)

        # Draw subtle grid dots or border
        border_color = self.COLOR_PALETTE["border_subtle"]
        draw.rectangle([(40, 40), (width - 40, height - 40)], outline=border_color, width=2)

        # Draw accent top bar
        draw.line([(40, 40), (280, 40)], fill=accent_color, width=6)

        # Category Pill Badge
        badge_x, badge_y = 80, 100
        badge_w, badge_h = 320, 50
        draw.rounded_rectangle(
            [(badge_x, badge_y), (badge_x + badge_w, badge_y + badge_h)],
            radius=8,
            fill=self.COLOR_PALETTE["bg_card"],
            outline=accent_color,
            width=2,
        )

        # Category text
        draw.text((badge_x + 20, badge_y + 14), category.upper(), fill=accent_color)

        # Headline text wrapping
        max_chars_per_line = 24
        words = headline.split()
        lines: List[str] = []
        current_line: List[str] = []

        for word in words:
            if sum(len(w) for w in current_line) + len(current_line) + len(word) <= max_chars_per_line:
                current_line.append(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            lines.append(" ".join(current_line))

        # Render headline
        start_y = 300
        for i, line in enumerate(lines):
            draw.text((80, start_y + (i * 90)), line, fill=self.COLOR_PALETTE["text_primary"])

        # Render optional subtitle
        if subtitle:
            sub_y = start_y + (len(lines) * 90) + 40
            draw.text((80, sub_y), subtitle, fill=self.COLOR_PALETTE["text_secondary"])

        # Footer element
        draw.line([(80, 1100), (width - 80, 1100)], fill=border_color, width=1)
        draw.text((80, 1120), "B2B OPERATIONS FRAMEWORK", fill=self.COLOR_PALETTE["text_secondary"])

        img.save(str(out_file), "PNG")
        return str(out_file)
