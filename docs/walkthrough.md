# Walkthrough: Visible Browser on Second Monitor

## What Changed

### [requirements.txt](file:///c:/My_Projects/My_Projects/Tuesday/requirements.txt)
- Added `playwright>=1.40.0` (was used but missing from deps)
- Added `screeninfo>=0.8.1` for multi-monitor detection

### [config/settings.py](file:///c:/My_Projects/My_Projects/Tuesday/config/settings.py)
New browser settings (all configurable via `.env`):

| Setting | Default | Description |
|---|---|---|
| `BROWSER_HEADLESS` | `false` | Set `true` to go back to invisible mode |
| `BROWSER_TARGET_MONITOR` | `2` | Which monitor to open on (1-indexed) |
| `BROWSER_VIEW_DELAY` | `3.0` | Seconds browser stays visible before closing |
| `BROWSER_SCREENSHOT_DIR` | `data/screenshots/` | Where screenshots are saved |

### [tools/web_driver.py](file:///c:/My_Projects/My_Projects/Tuesday/tools/web_driver.py)
Complete rewrite:
- Uses `screeninfo.get_monitors()` to detect second monitor position
- Launches Chromium **visible** with `--window-position` and `--start-maximized` targeting monitor 2
- Takes a screenshot before closing (saved to `data/screenshots/`)
- Configurable `view_delay` (default 3s) — browser stays visible so you can watch
- Optional `keep_open=True` mode — browser stays open until you press Enter
- Graceful fallback: if only 1 monitor detected, uses primary display
- UTF-8 stdout handling for emoji output

### [main.py](file:///c:/My_Projects/My_Projects/Tuesday/main.py)
- Added `rich` imports (`Console`, `Panel`, `Text`)
- The `[INSPECT_WEB:]` handler now shows a **rich panel** in terminal with:
  - Page title (bold white)
  - Screenshot path (dimmed)
  - Content preview (first 300 chars)
  - Green border for success, red for errors

## Verification

Tested with `python -c "from tools.web_driver import inspect_url; print(inspect_url('https://example.com', view_delay=1.0))"`:

- ✅ Browser opened **visibly** on monitor 2 (1920x1080 at position 1920,0)
- ✅ Page content extracted correctly
- ✅ Screenshot saved to `data/screenshots/example_com_20260520_185300.png`
- ✅ Browser auto-closed after 1 second delay

## How to Use

Just run Tuesday normally — `python main.py` — and ask it to inspect a URL. The browser will pop up on your second screen while the summary appears in terminal.

To customize, add to `.env`:
```env
BROWSER_HEADLESS=false
BROWSER_TARGET_MONITOR=2
BROWSER_VIEW_DELAY=3.0
```
