"""
Instant Post Generator & Live Editor CLI
Generates high-impact B2B founder posts on demand, generates 1:1 cover cards,
publishes immediately to LinkedIn, and supports in-place live editing without deleting.
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path
from typing import Optional

from generator.browser_controller import BrowserController
from generator.copy_humanizer import CopyHumanizer
from generator.visual_prompt_engine import VisualPromptEngine


class InstantPostGenerator:
    """
    Handles instantaneous founder post generation, image asset synthesis,
    live posting, and in-place live edits.
    """

    def __init__(self):
        self.humanizer = CopyHumanizer()
        self.visual_engine = VisualPromptEngine()

    def process_brief(self, brief_or_draft: str, audience: str = "B2B Founders") -> str:
        """
        Validates and formats the draft. If it's a raw brief, provides the humanizer prompt.
        """
        validation = self.humanizer.validate_copy(brief_or_draft)
        cleaned = self.humanizer.clean_copy(brief_or_draft)
        return cleaned, validation

    async def create_and_publish(
        self,
        headline: str,
        body_text: str,
        category: str = "FOUNDER LESSON",
        generate_image: bool = True,
        output_image_path: str = "assets/sample/sample_cover.png",
        publish_live: bool = False,
        schedule_time: Optional[str] = None,
    ) -> bool:
        """
        Full workflow: validates copy, generates cover graphic, and publishes/schedules.
        """
        print("\n" + "=" * 60)
        print("INSTANT POST GENERATOR WORKFLOW")
        print("=" * 60)

        # 1. Humanize / Validate
        full_post = f"{headline}\n\n{body_text}"
        validation = self.humanizer.validate_copy(full_post)
        
        print("\n[*] Copy Validation Report:")
        if not validation["valid"]:
            print("[!] Validation issues found:")
            for issue in validation["issues"]:
                print(f"    - {issue}")
            if publish_live:
                print("[!] Refusing to publish invalid copy. Please resolve the above issues.")
                return False
        else:
            print("[+] Copy passed all anti-cliche and zero-dollar checks.")

        for sug in validation["suggestions"]:
            print(f"    ~ Suggestion: {sug}")

        # 2. Visual Synthesis
        image_path = None
        if generate_image:
            print(f"\n[*] Generating 1200x1200px cover card ({category})...")
            try:
                image_path = self.visual_engine.create_offline_cover_image(
                    headline=headline,
                    category=category,
                    subtitle=body_text.splitlines()[0] if body_text else None,
                    output_path=output_image_path,
                )
                print(f"[+] Visual generated at: {image_path}")
            except Exception as e:
                print(f"[!] Warning: Image generation skipped ({e})")

        # 3. Dry-Run or Live Execution
        if not publish_live and not schedule_time:
            print("\n--- [DRAFT PREVIEW] ---")
            print(full_post)
            print("-----------------------")
            print(f"Image Attachment: {image_path or 'None'}")
            print("\n[+] Dry run complete. Use --publish to post live or --schedule 'time' to schedule.")
            return True

        # 4. Connect via CDP Browser Controller
        print("\n[*] Initializing CDP browser session...")
        controller = BrowserController()
        try:
            image_list = [image_path] if image_path and Path(image_path).exists() else None
            success = await controller.publish_post(
                copy_text=full_post,
                image_paths=image_list,
                schedule_datetime=schedule_time,
            )
            if success:
                action = f"scheduled for {schedule_time}" if schedule_time else "published immediately"
                print(f"[+] Instant post successfully {action} on LinkedIn!")
                return True
            else:
                print("[!] Failed to publish post via browser.")
                return False
        finally:
            await controller.disconnect()

    async def live_edit(self, post_url: str, new_copy: str) -> bool:
        """
        Performs in-place live edit on an existing post.
        """
        print(f"\n[*] Executing in-place live edit for post: {post_url}")
        val = self.humanizer.validate_copy(new_copy)
        if not val["valid"]:
            print("[!] New copy failed validation:")
            for issue in val["issues"]:
                print(f"    - {issue}")
            return False

        controller = BrowserController()
        try:
            success = await controller.edit_live_post(post_url=post_url, new_copy=new_copy)
            if success:
                print("[+] Post successfully edited live!")
                return True
            else:
                print("[!] Live edit failed.")
                return False
        finally:
            await controller.disconnect()


def main():
    parser = argparse.ArgumentParser(description="LinkedIn Instant Post Generator & Live Editor")
    parser.add_argument("--headline", type=str, help="Post headline / hook line")
    parser.add_argument("--body", type=str, help="Post body text")
    parser.add_argument("--category", type=str, default="FOUNDER INSIGHT", help="Category tag for visual card")
    parser.add_argument("--no-image", action="store_true", help="Skip generating the 1:1 visual card")
    parser.add_argument("--publish", action="store_true", help="Publish immediately to LinkedIn")
    parser.add_argument("--schedule", type=str, help="Schedule date and time string")
    parser.add_argument("--edit-url", type=str, help="Post URL for in-place live edit")
    parser.add_argument("--new-copy", type=str, help="Updated copy for in-place live edit")

    args = parser.parse_args()
    engine = InstantPostGenerator()

    if args.edit_url:
        if not args.new_copy:
            print("[!] Error: --new-copy is required when performing --edit-url")
            sys.exit(1)
        asyncio.run(engine.live_edit(post_url=args.edit_url, new_copy=args.new_copy))
        return

    if args.headline and args.body:
        asyncio.run(
            engine.create_and_publish(
                headline=args.headline,
                body_text=args.body,
                category=args.category,
                generate_image=not args.no_image,
                publish_live=args.publish,
                schedule_time=args.schedule,
            )
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
