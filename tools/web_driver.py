"""Tuesday — Web Driver Tool. Inspects web pages via headless Playwright."""

import json
from playwright.sync_api import sync_playwright


MAX_CONTENT_LENGTH = 5000


def inspect_url(url: str) -> str:
    """Open a headless browser, navigate to the URL, and extract page content."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=15000)
            page.wait_for_load_state("domcontentloaded")

            title = page.title()
            content = page.evaluate("() => document.body.innerText") or ""

            if len(content) > MAX_CONTENT_LENGTH:
                content = content[:MAX_CONTENT_LENGTH] + "\n\n[...truncated to save context window]"

            browser.close()

        return json.dumps({
            "status": "success",
            "title": title,
            "content": content.strip(),
        }, indent=2)

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
