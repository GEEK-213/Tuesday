# Day 4 — Web Search: Giving Tuesday a Library Card

## The Analogy

Imagine an AI as a very smart person locked inside a room full of textbooks. Those textbooks were printed on the day the model was trained — they cover a *lot*, but they're frozen in time. The AI has no idea what happened yesterday, let alone an hour ago.

**A web search tool is like giving that person a library card.** They still think with their own brain (the LLM), but now they can walk to the library, look something up, bring the book back to the room, and *then* give you an informed answer.

That's exactly what we built today. Tuesday can now leave the room.

---

## How It Works: The ReAct Loop

Tuesday already uses a simple **ReAct (Reason → Act → Observe)** pattern for tools. Web search follows the exact same flow:

```
User asks a question
        ↓
   LLM responds with a trigger word   ← REASON
        ↓
   Python detects the trigger word
   and calls the search function       ← ACT
        ↓
   Results are injected into memory
   and the LLM is called again         ← OBSERVE
        ↓
   Tuesday gives a natural answer
```

### The Trigger Word

In `system_prompt.txt`, we told Tuesday:

> If the user asks about current events or real-time information, reply EXACTLY with: `[SEARCH_WEB: your_search_query_here]`

When the LLM detects it can't answer from memory, it outputs this structured tag instead of guessing.

---

## Parsing the Query: String Manipulation

The most important piece of code in `main.py` is extracting the actual search query from the trigger word. Here's how it works, step by step:

```python
response = "[SEARCH_WEB: latest Python 3.14 features]"
```

### Step 1 — Find where the query starts

```python
start = response.index("[SEARCH_WEB:") + len("[SEARCH_WEB:")
# "[SEARCH_WEB:" is 13 characters, so `start` points to the space right after the colon
```

`str.index()` returns the position of the first character of the match. Adding `len("[SEARCH_WEB:")` skips past the tag itself, landing us right at the beginning of the actual query.

### Step 2 — Find where the query ends

```python
end = response.index("]", start)
# Searches for the closing bracket, starting from `start` so we don't accidentally match an earlier `]`
```

### Step 3 — Slice and clean

```python
query = response[start:end].strip()
# Result: "latest Python 3.14 features"
```

`.strip()` removes any leading/trailing whitespace, giving us a clean search string ready to pass to DuckDuckGo.

---

## The Search Function

`tools/web_search.py` uses the `ddgs` package (formerly `duckduckgo-search`), which is completely free and requires **no API key**.

```python
from ddgs import DDGS

results = DDGS().text(query, max_results=3)
```

Each result is a dictionary with `title`, `href` (the URL), and `body` (a text snippet). We reformat these into a clean JSON structure:

```json
{
  "status": "success",
  "results": [
    {
      "title": "Python 3.14 Released",
      "link": "https://example.com/python-3.14",
      "snippet": "Python 3.14 introduces several new features..."
    }
  ]
}
```

If the network is down or DuckDuckGo is unreachable, the `try/except` block catches the error and returns a JSON error message instead of crashing.

---

## Handling Edge Cases: Query Reformulation

### The Problem

DuckDuckGo is a keyword search engine. It doesn't "understand" your intent — it matches strings. So when the user says *"pull the latest news on Dr. Ketan Bhatekar"* and the correct spelling is actually *Bhatikar*, DDG returns zero results. A human would instinctively try a different spelling, but our first version of Tuesday would just report failure and move on.

### The Fix: Giving the LLM Agency to Retry

Instead of hard-coding retry logic in Python, we lean on what the LLM is *already good at* — reasoning about language. We added a **Self-Correction** rule to the system prompt:

> If your initial search returns no results, try ONE more time with a different query. Fix likely typos, broaden keywords, or use context clues.

When Tuesday reads an empty `TOOL OUTPUT`, she now has permission to fire a second `[SEARCH_WEB: ...]` trigger with a smarter query. Python doesn't need to know *what* to search — the LLM figures that out.

### How It Works in Code

The old code used a single `if` statement — one shot, done. The new code uses a `while` loop with a counter:

```python
search_attempts = 0
while "[SEARCH_WEB:" in response and search_attempts < 2:
    search_attempts += 1
    # ... extract query, search, inject results, call LLM again
```

**Why `< 2` and not `< 5`?** Two attempts is the sweet spot:
- **Attempt 1**: The original query from the user's question.
- **Attempt 2**: The LLM's reformulated query after reading empty results.

If two different queries both fail, the information probably doesn't exist on the web. Going beyond 2 would waste API calls and make the user wait for nothing.

### Example Flow

```
User: "What happened to Dr. Ketan Bhatekar?"

Attempt 1:
  🌐 Searching for: Dr. Ketan Bhatekar demise news
  → TOOL OUTPUT: { "results": [] }

Attempt 2:
  🔄 Retry — reformulated query.
  🌐 Searching for: Ketan Bhatikar Ponda Goa news
  → TOOL OUTPUT: { "results": [ ... ] }

Tuesday: "According to recent reports, Dr. Ketan Bhatikar..."
```

---

## File Changes Summary

| File | Change |
|---|---|
| `tools/web_search.py` | Replaced placeholder with full DuckDuckGo implementation |
| `brain/prompts/system_prompt.txt` | Added `[SEARCH_WEB]` trigger instruction |
| `main.py` | Imported `search_web`, added ReAct detection loop |
| `requirements.txt` | Added `ddgs>=9.0.0` |

---

## Testing

Run Tuesday and try asking something she can't know from training data:

```
You: What happened in tech news today?
🌐 Tuesday is searching the web for: tech news today...
Tuesday: Here's what's happening in tech today...
```

If the search works, you'll see the 🌐 globe emoji followed by Tuesday's synthesized answer. If you want to see the raw JSON, set `TUESDAY_DEBUG=true` in your `.env` file and add a `print(tool_output)` line after the search call.
