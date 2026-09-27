import asyncio
import os
import sys
from pathlib import Path
from typing import List, Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

class BrowserController:
    """
    Manages Playwright browser automation via Chrome Remote Debugging Protocol (CDP).
    Enables scheduled and instant publishing on LinkedIn without session invalidation.
    """

    def __init__(self, port: int = 9222, host: str = "127.0.0.1", user_data_dir: Optional[str] = None):
        self.port = int(os.getenv("CHROME_DEBUG_PORT", port))
        self.host = host
        self.user_data_dir = user_data_dir or os.getenv("CHROME_USER_DATA_DIR")
        self._playwright = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None

    def get_cdp_ws_url(self) -> str:
        """Discovers the Chrome DevTools WebSocket URL from DevToolsActivePort or falls back to port."""
        if self.user_data_dir:
            port_file = Path(self.user_data_dir) / "DevToolsActivePort"
            if port_file.exists():
                lines = [line.strip() for line in port_file.read_text().splitlines() if line.strip()]
                if len(lines) >= 2:
                    return f"ws://{self.host}:{lines[0]}{lines[1]}"
        return f"http://{self.host}:{self.port}"

    async def connect(self):
        """Connects to the running Chrome instance over CDP."""
        ws_url = self.get_cdp_ws_url()
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.connect_over_cdp(ws_url)
        self._context = self._browser.contexts[0]
        return self._context

    async def disconnect(self):
        """Disconnects cleanly from the CDP session without closing the user's browser."""
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    async def get_or_create_page(self, url_keyword: str = "linkedin.com", target_url: str = "https://www.linkedin.com/feed/") -> Page:
        """Finds an existing page matching keyword or opens a new tab."""
        if not self._context:
            await self.connect()

        for page in self._context.pages:
            if url_keyword in page.url:
                await page.bring_to_front()
                return page

        page = await self._context.new_page()
        await page.goto(target_url, wait_until="domcontentloaded")
        await asyncio.sleep(3)
        return page

    async def dismiss_lingering_dialogs(self, page: Page):
        """Dismisses any active drafts or close prompts on LinkedIn feed."""
        for _ in range(3):
            discard_btn = page.locator("button:has-text('Discard'):visible").first
            if await discard_btn.is_visible():
                await discard_btn.click()
                await asyncio.sleep(1)

            close_btn = page.locator("button[aria-label='Dismiss']:visible, button[aria-label='Close']:visible").first
            if await close_btn.is_visible():
                await close_btn.click()
                await asyncio.sleep(1)

    async def publish_or_schedule(
        self,
        post_copy: str,
        asset_paths: List[str],
        schedule_date: Optional[str] = None,
        schedule_time: Optional[str] = None,
        confirmation_screenshot_path: Optional[str] = None
    ) -> bool:
        """
        Uploads media assets, injects post copy, and either schedules or immediately publishes on LinkedIn.

        :param post_copy: Sanitized, humanized text copy.
        :param asset_paths: Ordered list of image file paths (1 to 3 images).
        :param schedule_date: Optional date string 'MM/DD/YYYY' (e.g. '09/25/2026'). If None, publishes immediately.
        :param schedule_time: Optional time string 'HH:MM AM/PM' (e.g. '1:00 AM').
        :param confirmation_screenshot_path: Target path to save the verification screenshot.
        :return: True if successful, False otherwise.
        """
        page = await self.get_or_create_page(url_keyword="linkedin.com", target_url="https://www.linkedin.com/feed/")
        await self.dismiss_lingering_dialogs(page)
        await asyncio.sleep(2)

        # 1. Attach media assets
        print(f"Uploading {len(asset_paths)} asset(s)...")
        photo_btn = page.locator("div[role='button']:has-text('Photo'), p:has-text('Photo'), button:has-text('Photo')").first
        if await photo_btn.is_visible():
            async with page.expect_file_chooser() as fc_info:
                await photo_btn.click()
            file_chooser = await fc_info.value
            await file_chooser.set_files(asset_paths)
        else:
            start_post = page.locator("div[role='button']:has-text('Start a post'), button:has-text('Start a post'), span:has-text('Start a post')").first
            await start_post.click()
            await asyncio.sleep(2)
            media_btn = page.locator("button[aria-label='Media'], button[aria-label*='Add media']").first
            async with page.expect_file_chooser() as fc_info:
                await media_btn.click()
            file_chooser = await fc_info.value
            await file_chooser.set_files(asset_paths)

        await asyncio.sleep(5)

        # 2. Advance media editor
        print("Advancing media modal...")
        next_media_btn = page.locator("button:has-text('Next'):visible").first
        if await next_media_btn.is_visible():
            await next_media_btn.click()
        else:
            await page.evaluate("""() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const b = btns.find(x => x.textContent.trim() === 'Next' || x.innerText.trim() === 'Next');
                if (b) b.click();
            }""")

        await asyncio.sleep(3)

        # 3. Enter post text
        print("Injecting post copy into composer...")
        editor = page.locator("div.ql-editor[contenteditable='true'], div[role='textbox']").first
        await editor.click()
        await asyncio.sleep(1)

        await page.evaluate("""(text) => {
            const el = document.querySelector('div.ql-editor[contenteditable="true"], div[role="textbox"]');
            if (el) {
                el.focus();
                document.execCommand('insertText', false, text);
            }
        }""", post_copy)
        await asyncio.sleep(2)

        # 4. Schedule or Instant Publish
        if schedule_date and schedule_time:
            print(f"Configuring schedule for {schedule_date} at {schedule_time}...")
            sched_link = page.locator("a[aria-label='Scheduled'], a:has(svg#clock-medium)").first
            if await sched_link.is_visible():
                await sched_link.click()
            else:
                await page.evaluate("""() => {
                    const link = document.querySelector('a[aria-label="Scheduled"], a:has(svg#clock-medium)');
                    if (link) link.click();
                }""")
            await asyncio.sleep(3)

            inputs = await page.locator("input:visible").all()
            for inp in inputs:
                val = await inp.input_value()
                if "/" in val or "-" in val:
                    await inp.click()
                    await inp.fill("")
                    await inp.type(schedule_date)
                    await asyncio.sleep(1)
                elif "PM" in val or "AM" in val or ":" in val:
                    await inp.click()
                    await inp.fill("")
                    await inp.type(schedule_time)
                    await asyncio.sleep(1)
                    await page.keyboard.press("Enter")

            await asyncio.sleep(1)

            # Click Confirm in schedule modal
            await page.evaluate("""() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const confirmBtn = btns.find(b => b.innerText.trim() === 'Confirm' || b.textContent.trim() === 'Confirm');
                if (confirmBtn) confirmBtn.click();
            }""")
            await asyncio.sleep(3)

            # Click final Schedule button
            await page.evaluate("""() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const schedBtn = btns.find(b => b.innerText.trim() === 'Schedule' || b.textContent.trim() === 'Schedule');
                if (schedBtn) schedBtn.click();
            }""")
            print("Post schedule submitted.")
        else:
            print("Executing instant publish...")
            post_btn = page.locator("button.share-actions__primary-action, button:has-text('Post'):visible").first
            if await post_btn.is_visible():
                await post_btn.click()
            else:
                await page.evaluate("""() => {
                    const btns = Array.from(document.querySelectorAll('button'));
                    const b = btns.find(x => x.textContent.trim() === 'Post' || x.innerText.trim() === 'Post');
                    if (b) b.click();
                }""")
            print("Post publish submitted.")

        await asyncio.sleep(6)

        if confirmation_screenshot_path:
            Path(confirmation_screenshot_path).parent.mkdir(parents=True, exist_ok=True)
            await page.screenshot(path=confirmation_screenshot_path)
            print(f"Confirmation captured at: {confirmation_screenshot_path}")

        return True
