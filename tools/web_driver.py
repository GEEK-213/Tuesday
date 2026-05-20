"""Tuesday — Web Driver Tool. Inspects web pages via Playwright.

Supports visible (headed) mode with second-monitor targeting,
configurable view delay, and screenshot capture.
"""

import json
import os
import sys
import time
import datetime
from playwright.sync_api import sync_playwright

os.environ["PYTHONUTF8"] = "1"
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from config.settings import (
    BROWSER_HEADLESS,
    BROWSER_TARGET_MONITOR,
    BROWSER_VIEW_DELAY,
    BROWSER_SCREENSHOT_DIR,
)


MAX_CONTENT_LENGTH = 5000


def _get_monitor_position(target_monitor: int) -> tuple[int, int, int, int]:
    """Detect monitor positions and return (x, y, width, height) for the target.

    Falls back to (0, 0, 1280, 720) if screeninfo is unavailable or only one monitor exists.
    """
    try:
        from screeninfo import get_monitors

        monitors = get_monitors()

        if len(monitors) < target_monitor:
            mon = monitors[0]
            print(f"  ⚠ Only {len(monitors)} monitor(s) detected — using primary display.")
        else:
            mon = monitors[target_monitor - 1]
            print(f"  🖥 Targeting monitor {target_monitor}: {mon.width}x{mon.height} at ({mon.x}, {mon.y})")

        return mon.x, mon.y, mon.width, mon.height

    except ImportError:
        print("  ⚠ screeninfo not installed — browser will open on default display.")
        return 0, 0, 1280, 720
    except Exception as e:
        print(f"  ⚠ Monitor detection failed ({e}) — using default position.")
        return 0, 0, 1280, 720


def _save_screenshot(page, url: str) -> str | None:
    """Capture a screenshot and save it to the screenshots directory."""
    try:
        os.makedirs(BROWSER_SCREENSHOT_DIR, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = url.split("//")[-1].split("/")[0].replace(".", "_")
        filename = f"{safe_name}_{timestamp}.png"
        filepath = os.path.join(BROWSER_SCREENSHOT_DIR, filename)

        page.screenshot(path=filepath, full_page=False)
        return filepath

    except Exception as e:
        print(f"  ⚠ Screenshot failed: {e}")
        return None


def inspect_url(url: str, view_delay: float | None = None, keep_open: bool = False) -> str:
    """Open a browser, navigate to the URL, and extract page content.

    In visible mode (default), the browser opens on the target monitor
    and stays visible for `view_delay` seconds before auto-closing.
    """
    headless = BROWSER_HEADLESS
    delay = view_delay if view_delay is not None else BROWSER_VIEW_DELAY

    try:
        with sync_playwright() as p:
            launch_args = []

            if not headless:
                x, y, width, height = _get_monitor_position(BROWSER_TARGET_MONITOR)
                launch_args.extend([
                    f"--window-position={x},{y}",
                    f"--window-size={width},{height}",
                    "--start-maximized",
                ])

            browser = p.chromium.launch(
                headless=headless,
                args=launch_args,
            )

            context = browser.new_context(
                viewport=None if not headless else {"width": 1280, "height": 720},
                no_viewport=not headless,
            )
            page = context.new_page()
            page.goto(url, timeout=15000)
            page.wait_for_load_state("domcontentloaded")

            title = page.title()
            content = page.evaluate("() => document.body.innerText") or ""

            if len(content) > MAX_CONTENT_LENGTH:
                content = content[:MAX_CONTENT_LENGTH] + "\n\n[...truncated to save context window]"

            screenshot_path = _save_screenshot(page, url)

            if not headless and delay > 0 and not keep_open:
                time.sleep(delay)

            if keep_open and not headless:
                try:
                    print("  🔓 Browser is open. Press Enter in the terminal to close...")
                    input()
                except EOFError:
                    pass

            browser.close()

        result = {
            "status": "success",
            "title": title,
            "content": content.strip(),
        }
        if screenshot_path:
            result["screenshot"] = screenshot_path

        return json.dumps(result, indent=2)

    except Exception as e:
        error_msg = str(e)

        if "ERR_CONNECTION_REFUSED" in error_msg:
            message = f"Connection refused — the server at {url} is not running."
        elif "Timeout" in error_msg:
            message = f"Navigation timed out — {url} did not respond within 15 seconds."
        elif "ERR_NAME_NOT_RESOLVED" in error_msg:
            message = f"DNS resolution failed — {url} could not be found."
        else:
            message = error_msg

        return json.dumps({
            "status": "error",
            "message": message,
        }, indent=2)


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    print(f"Inspecting: {target}")
    print("=" * 40)
    print(inspect_url(target))
