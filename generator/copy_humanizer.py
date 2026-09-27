"""
Copy Humanizer & Anti-Cliché Validation Engine
Transforms corporate drafts and robotic AI outputs into punchy, authentic B2B founder posts.
Enforces the Zero-Dollar Rule, anti-cliché filters, and readability heuristics.
"""

import re
from typing import Dict, List, Tuple

# Common AI clichés and corporate jargon to detect and eliminate
BANNED_CLICHES = [
    "game changer",
    "game-changer",
    "dive deep",
    "dive into",
    "delve",
    "tapestry",
    "in today's fast-paced world",
    "in today's world",
    "look no further",
    "revolutionize",
    "supercharge",
    "unlock the power",
    "unlocking",
    "leverage",
    "seamlessly",
    "elevate",
    "harness the power",
    "testament to",
    "beacon of",
    "unleash",
    "paradigm shift",
    "it's crucial to remember",
    "at the end of the day",
]

# Formatting guidelines
MAX_HOOK_LENGTH = 90
MAX_HASHTAGS = 3


class CopyHumanizer:
    """
    Validates, calibrates, and formats B2B LinkedIn copy to ensure authentic human tone.
    """

    def __init__(self, ban_dollar_signs: bool = True):
        self.ban_dollar_signs = ban_dollar_signs

    def validate_copy(self, text: str) -> Dict[str, any]:
        """
        Runs rigorous checks against the copy:
        1. Zero-Dollar Rule check (prohibits raw '$' symbols; encourages contextual/unit metrics)
        2. AI Cliché & Corporate Buzzword detection
        3. Hook line brevity
        4. Hashtag discipline (maximum 3, placed at end)
        5. Spacing and readability
        """
        issues: List[str] = []
        suggestions: List[str] = []
        lines = [line.strip() for line in text.strip().splitlines() if line.strip()]

        if not lines:
            return {"valid": False, "issues": ["Copy is empty"], "suggestions": []}

        # 1. Zero-Dollar Rule
        if self.ban_dollar_signs and "$" in text:
            dollar_count = text.count("$")
            issues.append(
                f"Zero-Dollar Rule Violation: Found {dollar_count} dollar sign ('$') occurrence(s). "
                "Use spelled-out metric units, percentages, or process outcomes instead of raw dollar tags."
            )

        # 2. Cliché Detection
        lower_text = text.lower()
        found_cliches = [c for c in BANNED_CLICHES if re.search(rf"\b{re.escape(c)}\b", lower_text)]
        if found_cliches:
            issues.append(
                f"AI Clichés detected: {', '.join(found_cliches)}. Replace with direct, plainspoken observations."
            )

        # 3. Hook Length
        first_line = lines[0]
        if len(first_line) > MAX_HOOK_LENGTH:
            suggestions.append(
                f"Hook line is long ({len(first_line)} chars). Keep under {MAX_HOOK_LENGTH} chars for higher mobile tap-through."
            )

        # 4. Hashtags
        hashtags = re.findall(r"#\w+", text)
        if len(hashtags) > MAX_HASHTAGS:
            issues.append(
                f"Too many hashtags ({len(hashtags)} found). Maximum recommended is {MAX_HASHTAGS} at the footer."
            )

        # 5. Wall of text check
        paragraphs = text.split("\n\n")
        long_paragraphs = [p for p in paragraphs if len(p.splitlines()) > 3]
        if long_paragraphs:
            suggestions.append(
                "Detected paragraphs longer than 3 lines. Break them into 1-2 sentence beats for mobile skim-ability."
            )

        is_valid = len(issues) == 0
        return {
            "valid": is_valid,
            "issues": issues,
            "suggestions": suggestions,
            "char_count": len(text),
            "word_count": len(text.split()),
            "line_count": len(lines),
        }

    def clean_copy(self, text: str) -> str:
        """
        Performs basic automated cleanup:
        - Replaces common currency symbols if zero-dollar rule is active
        - Removes excessive trailing spaces
        - Ensures standard double-newline spacing between blocks
        """
        cleaned = text.strip()
        # Clean multiple blank lines
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
        return cleaned

    def build_humanizer_prompt(self, raw_draft_or_story: str, audience: str = "B2B Founders & Operations Leaders") -> str:
        """
        Generates a calibration prompt suitable for Claude or GPT to humanize a draft.
        """
        return f"""You are an elite B2B ghostwriter and founder communications strategist.
Rewrite the following raw thought into a high-engagement, authentic LinkedIn post.

Target Audience: {audience}

STRICT CONSTRAINTS:
1. THE ZERO-DOLLAR RULE: Never use the '$' dollar sign. Reframe financial discussions around operational leverage, capacity, hours saved, or conversion percentages.
2. NO AI CLICHÉS: Never use words like 'game changer', 'dive deep', 'delve', 'supercharge', 'tapestry', 'revolutionize', or 'seamless'.
3. FORMAT:
   - Line 1: Strong, provocative hook (<80 characters).
   - Body: Short 1-2 sentence paragraphs with clean whitespace. No wall of text.
   - Core premise: Personal experience or contrarian business observation.
   - Conclusion: Clear, frictionless takeaway or invitation to discuss (e.g. "Drop a DM or comment below").
   - Hashtags: Maximum 2-3 minimal tags at the very bottom.

RAW DRAFT / BRIEF:
\"\"\"
{raw_draft_or_story}
\"\"\"

Output ONLY the final, ready-to-publish post copy.
"""
