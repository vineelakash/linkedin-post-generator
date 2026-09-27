"""
Content Calendar Scheduler CLI
Automates the batch validation, staging, and scheduling of posts from the 20-post content calendar.
Supports dry-run validation, image asset verification, and browser scheduling via CDP.
"""

import argparse
import asyncio
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from generator.browser_controller import BrowserController
from generator.copy_humanizer import CopyHumanizer


class ContentCalendarScheduler:
    """
    Coordinates post status tracking, copy validation, image asset verification,
    and automated browser scheduling for the content calendar sequence.
    """

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).resolve().parent.parent
        self.calendar_dir = self.base_dir / "content_calendar"
        self.posts_dir = self.calendar_dir / "posts"
        self.tracker_file = self.calendar_dir / "tracker.json"
        self.tracker_md = self.calendar_dir / "TRACKER.md"
        self.humanizer = CopyHumanizer()

    def load_tracker(self) -> Dict[str, any]:
        """Loads tracker.json data or initializes if missing."""
        if self.tracker_file.exists():
            with open(self.tracker_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"campaign": "B2B Content Calendar", "posts": []}

    def save_tracker(self, data: Dict[str, any]):
        """Persists tracker.json with indentation."""
        with open(self.tracker_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def parse_post_file(self, post_path: Path) -> Dict[str, any]:
        """Extracts title, metadata, copy, and visual prompts from a markdown post file."""
        content = post_path.read_text(encoding="utf-8")
        
        # Extract title
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else post_path.stem

        # Extract copy (section under ## LinkedIn Post Copy or similar)
        copy_match = re.search(
            r"##\s+(?:LinkedIn\s+)?(?:Post\s+Copy|Humanized\s+Copy|Post\s+Draft|Copy)\s*\n+(.*?)(?=\n---|\n##|\Z)",
            content,
            re.DOTALL | re.IGNORECASE,
        )
        post_copy = copy_match.group(1).strip() if copy_match else content

        # Extract DM keyword if present
        keyword_match = re.search(r"(?:DM|keyword|comment)\s*[`\"']*([A-Z0-9_\-]+)", content, re.IGNORECASE)
        cta_keyword = keyword_match.group(1) if keyword_match else "WORKFLOW"

        return {
            "file": post_path.name,
            "title": title,
            "copy": post_copy,
            "cta_keyword": cta_keyword,
        }

    def list_posts(self):
        """Prints a summary table of all scheduled and pending posts in the calendar."""
        tracker = self.load_tracker()
        posts = tracker.get("posts", [])
        print("\n" + "=" * 85)
        print(f"{'#':<4} {'Topic':<48} {'Date / Schedule':<20} {'Status':<10}")
        print("=" * 85)
        for p in posts:
            post_id = p.get("day") or p.get("post_id") or p.get("id", "-")
            topic = (p.get("topic") or p.get("title") or "Untitled")[:46]
            sched = p.get("scheduled_time") or p.get("scheduled_datetime") or p.get("date", "-")
            status = p.get("status", "pending")
            print(f"{str(post_id):<4} {topic:<48} {str(sched):<20} {status:<10}")
        print("=" * 85 + "\n")

    async def schedule_single_post(
        self,
        post_id: int,
        dry_run: bool = True,
        schedule_datetime: Optional[str] = None,
        custom_images: Optional[List[str]] = None,
    ) -> bool:
        """
        Validates, prepares, and optionally schedules a post via CDP.
        """
        tracker = self.load_tracker()
        target_entry = None
        for p in tracker.get("posts", []):
            p_day = p.get("day") or p.get("post_id")
            if p_day == post_id or p.get("id") == f"post_{post_id:02d}":
                target_entry = p
                break

        if not target_entry:
            print(f"[!] Post #{post_id} not found in tracker.")
            return False

        # Find post markdown file
        rel_file = target_entry.get("file", f"posts/post_{post_id:02d}.md")
        # Could be "posts/..." or directly post file
        if rel_file.startswith("posts/"):
            post_file = self.calendar_dir / rel_file
        else:
            post_file = self.posts_dir / rel_file

        if not post_file.exists():
            matched = list(self.posts_dir.glob(f"post_{post_id:02d}*.md"))
            if matched:
                post_file = matched[0]
            else:
                print(f"[!] File for Post #{post_id} does not exist at {post_file}")
                return False

        parsed = self.parse_post_file(post_file)
        copy_text = parsed["copy"]

        print(f"\n[*] Processing Post #{post_id}: '{parsed['title']}'")

        # Validate copy
        val = self.humanizer.validate_copy(copy_text)
        if not val["valid"]:
            print(f"[!] Copy validation issues found:")
            for issue in val["issues"]:
                print(f"    - {issue}")
            if not dry_run:
                print("[!] Aborting schedule due to validation errors. Fix issues first.")
                return False
        else:
            print("[+] Copy validation passed (Zero-dollar rule & anti-cliche checks clean).")

        if val["suggestions"]:
            for sug in val["suggestions"]:
                print(f"    ~ Suggestion: {sug}")

        # Resolve image assets
        images_to_upload: List[str] = []
        if custom_images:
            images_to_upload = custom_images
        else:
            asset_dir = self.base_dir / "assets"
            candidate_images = [
                asset_dir / f"post_{post_id:02d}_hero.png",
                asset_dir / f"post_{post_id:02d}_infographic.png",
                asset_dir / f"post_{post_id:02d}_cta.png",
            ]
            for img_path in candidate_images:
                if img_path.exists():
                    images_to_upload.append(str(img_path))

        sched_dt = schedule_datetime or target_entry.get("scheduled_datetime") or target_entry.get("target_date")

        if dry_run:
            print(f"\n--- [DRY RUN PREVIEW] ---")
            print(f"Target Schedule: {sched_dt}")
            print(f"Images ({len(images_to_upload)} found): {images_to_upload}")
            print(f"Copy Preview (First 150 chars):\n{copy_text[:150]}...\n")
            print("[+] Dry-run simulation completed successfully. Use --execute to publish live.")
            return True

        # Live execution via BrowserController
        print(f"\n[*] Connecting to Chrome CDP to schedule Post #{post_id}...")
        controller = BrowserController()
        try:
            success = await controller.publish_post(
                copy_text=copy_text,
                image_paths=images_to_upload if images_to_upload else None,
                schedule_datetime=sched_dt,
            )
            if success:
                target_entry["status"] = "scheduled"
                target_entry["scheduled_datetime"] = sched_dt
                self.save_tracker(tracker)
                print(f"[+] Post #{post_id} successfully scheduled on LinkedIn!")
                return True
            else:
                print(f"[!] Failed to schedule Post #{post_id}.")
                return False
        finally:
            await controller.disconnect()


def main():
    parser = argparse.ArgumentParser(description="LinkedIn Content Calendar Scheduler")
    parser.add_argument("--list", action="store_true", help="List all posts in the content calendar")
    parser.add_argument("--post-id", type=int, help="Post ID to process (1 to 20)")
    parser.add_argument("--schedule-time", type=str, help="Schedule date and time string (e.g. 'Oct 15, 2026 10:00 AM')")
    parser.add_argument("--execute", action="store_true", help="Perform live scheduling via browser (default is dry-run)")
    parser.add_argument("--images", nargs="+", help="Explicit list of image paths to attach")

    args = parser.parse_args()
    scheduler = ContentCalendarScheduler()

    if args.list:
        scheduler.list_posts()
        return

    if args.post_id:
        dry_run = not args.execute
        asyncio.run(
            scheduler.schedule_single_post(
                post_id=args.post_id,
                dry_run=dry_run,
                schedule_datetime=args.schedule_time,
                custom_images=args.images,
            )
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
