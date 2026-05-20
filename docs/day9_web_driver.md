# Day 9 — The Web Driver: Browser Automation for AI Agents

## The Problem

Tuesday can search the web, read files, and run terminal commands. But she can't actually *look* at a web page.

If you're building a React app on `localhost:3000` and you ask "is my homepage rendering correctly?", she has no way to answer. She can't see what the browser sees. She doesn't know if your CSS is broken, if your JavaScript failed to hydrate, or if the page is just a white screen.

Traditional scraping tools like `requests` + `BeautifulSoup` won't help here either — they download raw HTML and parse it statically. They never execute JavaScript. For any modern SPA (React, Vue, Next.js, Angular), the raw HTML is often just an empty `<div id="root"></div>`. The actual content is rendered client-side by JavaScript *after* the page loads.

Tuesday needs a real browser.

## Why Playwright?

Playwright is a browser automation library from Microsoft. It launches a real Chromium, Firefox, or WebKit browser — headless (no visible window) — and gives you full programmatic control.

### Playwright vs. BeautifulSoup

| Capability | BeautifulSoup | Playwright |
|---|---|---|
| Parse static HTML | ✅ | ✅ |
| Execute JavaScript | ❌ | ✅ |
| Render React/Vue/Angular SPAs | ❌ | ✅ |
| Wait for async data to load | ❌ | ✅ |
| Interact with forms, buttons, etc. | ❌ | ✅ |
| Test localhost dev servers | ❌ | ✅ |
| Headless mode | N/A | ✅ |

For an AI agent that needs to inspect real web pages — especially local development servers — Playwright is the only viable option.

## Installation

Two steps are required. The Python package alone is not enough — Playwright also needs browser binaries.

```bash
pip install playwright
playwright install chromium
```

The second command downloads a specific version of Chromium (~180 MB) that Playwright manages independently from your system browser. This ensures reproducible behavior regardless of what Chrome version is installed on the machine.

## How It Works

### The Tool: `tools/web_driver.py`

The `inspect_url(url)` function does the following:

1. **Launches a headless Chromium instance** via `sync_playwright()`.
2. **Navigates to the URL** with a 15-second timeout.
3. **Waits for `domcontentloaded`** — this ensures the page's initial HTML and JS have been parsed.
4. **Extracts the page title** via `page.title()`.
5. **Extracts the visible text** via `document.body.innerText` — this gives us only the human-readable text, stripping out HTML tags, scripts, and styles.
6. **Truncates at 5,000 characters** to protect Tuesday's context window from massive pages.

The result is returned as a clean JSON string:

```json
{
  "status": "success",
  "title": "My React App",
  "content": "Welcome to the homepage\nNavigation: Home | About | Contact\n..."
}
```

### Error Handling

The tool catches specific failure modes and returns human-readable error messages:

| Scenario | Raw Error | Tuesday Sees |
|---|---|---|
| Dev server not running | `ERR_CONNECTION_REFUSED` | "Connection refused — the server at localhost:3000 is not running." |
| Page takes too long | `Timeout` | "Navigation timed out — url did not respond within 15 seconds." |
| Bad domain | `ERR_NAME_NOT_RESOLVED` | "DNS resolution failed — url could not be found." |

In every case, Tuesday gets structured JSON — never a raw Python traceback.

### The Trigger: `[INSPECT_WEB: url]`

When the user asks something like "check if my app is running on localhost:3000" or "what does example.com look like?", the LLM responds with:

```
[INSPECT_WEB: http://localhost:3000]
```

The main loop detects this via regex, extracts the URL, calls `inspect_url()`, injects the result into memory, and fires a second LLM call so Tuesday can analyze the page content.

### The Flow

```
User: "Is my React app rendering on localhost:3000?"
  └─> LLM outputs: [INSPECT_WEB: http://localhost:3000]
        └─> main.py detects trigger, extracts URL
              └─> inspect_url() launches headless Chromium
                    └─> Page title + body text extracted
                          └─> JSON result injected into memory
                                └─> Second LLM call reads the content
                                      └─> Tuesday: "Your app is running. The 
                                           homepage shows a nav bar and a 
                                           welcome hero section. Looks clean."
```

## Why `innerText` Instead of `innerHTML`?

`innerHTML` returns the full HTML markup — tags, attributes, class names, the works. For a typical web page, that could be 50,000+ characters of DOM soup. Most of it is irrelevant to understanding what the page *says*.

`innerText` returns only the visible, rendered text content. It's what a human would see if they looked at the page. This is orders of magnitude more token-efficient and far more useful for an AI that needs to answer "what does this page say?" rather than "what is the exact DOM structure?"

If Tuesday ever needs DOM-level inspection (for debugging CSS or element attributes), that's a future enhancement — but for 95% of use cases, `innerText` is the right tool.

## The Capability Map

With the Web Driver, Tuesday now has six actuators:

| Day | Tool | Capability |
|---|---|---|
| Day 3 | `[SEARCH_WEB]` | Real-time web knowledge |
| Day 4 | `[WRITE_FILE]` | Create and save files |
| Day 5 | `[READ_FILE]` | Read local files |
| Day 7 | `[RUN_TERMINAL]` | Execute shell commands |
| Day 8 | `[INSPECT_GIT]` | See code changes in real-time |
| **Day 9** | **`[INSPECT_WEB]`** | **See rendered web pages** |

The pattern is consistent: each tool follows the same ReAct architecture. Trigger → execute → inject → re-prompt. The only difference is what the tool does under the hood. That modularity is what makes Tuesday easy to extend — every new sense is just another tool file and another `if` block.
