# Day 4 — Long-Term Memory: From RAM to Disk

## The Problem

Every time you closed Tuesday's terminal, she forgot everything. Your name, your project, the conversation you just had — gone. That's because her `Memory` class stored history in a Python list, which lives in **RAM**. RAM is wiped the moment a process exits.

To fix this, we need to write the conversation to a **file on disk** so it survives between sessions.

---

## Volatile vs. Persistent Memory

| | Volatile (RAM) | Persistent (Disk) |
|---|---|---|
| **Where it lives** | Computer's working memory | A file on your hard drive |
| **Speed** | Blazing fast (nanoseconds) | Slightly slower (milliseconds) |
| **Survives a restart?** | ❌ No | ✅ Yes |
| **Analogy** | A whiteboard you erase every night | A notebook you keep on a shelf |

### The Whiteboard vs. The Notebook

Imagine you're a doctor and every patient walks in. The **whiteboard** (RAM) is where you jot notes during the appointment — quick, convenient, but wiped clean for the next patient.

The **notebook** (disk) is where you write down the key takeaways and file it in a cabinet. Next time the patient returns, you pull out the notebook and remember everything.

Tuesday's memory now works like the notebook. Every message is written to `data/memory.json` in real time, and when she boots up, she reads it back.

---

## How It Works

### Saving

Every time `memory.add()` is called (which happens on every user message and every assistant response), the entire history list is serialized to JSON and written to disk:

```python
def _save_to_disk(self) -> None:
    os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
    with open(self.filepath, "w", encoding="utf-8") as f:
        json.dump(self.history, f, indent=2, ensure_ascii=False)
```

The `os.makedirs(..., exist_ok=True)` ensures the `data/` folder is created automatically on the first run — no manual setup needed.

### Loading

On startup, `__init__` calls `_load_from_disk()`, which reads the JSON file (if it exists) and populates `self.history`:

```python
def _load_from_disk(self) -> None:
    if not os.path.exists(self.filepath):
        return
    try:
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            self.history = data[-self.max_history:]
    except (json.JSONDecodeError, OSError):
        self.history = []
```

Two safety nets here:
1. **`isinstance(data, list)`** — if someone manually edits the file and breaks the structure, we don't crash.
2. **`except (json.JSONDecodeError, OSError)`** — if the file is corrupted or unreadable, we start fresh instead of crashing.

### The Trimming Window

We still respect `max_history=50`. When loading, we only take the last 50 messages (`data[-self.max_history:]`). This prevents the context window from growing unbounded — LLMs have token limits, and sending 10,000 messages would be expensive and slow.

---

## JSON vs. Vector Databases

You might wonder: *"Why not use a real database?"* Great question. Here's the comparison:

| Feature | Local JSON File | Vector Database (ChromaDB, Pinecone) |
|---|---|---|
| **Setup** | Zero — just `import json` | Requires installation, config, possibly a server |
| **Cost** | Free | Free tier or paid (Pinecone) |
| **Search** | Sequential scan (slow on large data) | Semantic similarity search (fast + smart) |
| **Best for** | Chronological chat history (< 1,000 messages) | Searching through thousands of documents by meaning |
| **Use case** | "What did the user say 5 minutes ago?" | "Find all paragraphs about authentication in my codebase" |

### When JSON Is the Right Choice

For an AI agent's **conversation memory**, a JSON file is perfect because:
- Messages are stored and read **in order** (chronological).
- We send the **entire recent history** to the LLM on every call — no search needed.
- The dataset is small (50 messages max).
- Zero dependencies, zero config.

### When You'd Upgrade to a Vector DB

A vector database becomes necessary when you need **Retrieval-Augmented Generation (RAG)** — for example:
- *"Search through all 200 of my project files and find the ones related to authentication."*
- *"Find the conversation from last week where we discussed database schemas."*

Vector DBs convert text into **embeddings** (numerical representations of meaning), so a search for "login" would also find paragraphs mentioning "authentication," "sign-in," or "credentials." JSON can't do that — it only stores raw text.

We'll explore RAG and vector databases in a future session. For now, the JSON notebook is exactly what Tuesday needs.

---

## File Changes Summary

| File | Change |
|---|---|
| `brain/memory.py` | Added `_save_to_disk()`, `_load_from_disk()`, and `filepath` parameter |
| `main.py` | Updated `Memory()` init to pass `filepath` and show recalled message count |

---

## Testing

1. Start Tuesday and have a short conversation:
   ```
   You: My name is Ketan and I'm building an AI agent.
   Tuesday: Nice to meet you, Ketan! ...
   ```

2. Quit with `quit` or Ctrl+C.

3. Check the file was created:
   ```
   type data\memory.json
   ```

4. Start Tuesday again:
   ```
   ✅ Memory initialized (2 messages recalled from disk)
   ```

5. Ask: *"What's my name?"* — she should remember.
