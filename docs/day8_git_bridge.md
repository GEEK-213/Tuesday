# Day 8 — The Git Bridge: OmniContext for AI Agents

## What is OmniContext?

Most AI chatbots are blind. They only know what you paste into the chat window. If you're debugging a Python project and you want help, you have to manually copy your code, paste it, explain what changed, and hope you didn't miss anything. The AI has zero awareness of your actual working environment.

**OmniContext** is the architectural philosophy that fixes this. Instead of relying on the user to be the middleman, we give the AI agent direct, read-only access to the tools and data sources that surround the codebase — the terminal, the file system, and now, the Git tree.

An agent with OmniContext doesn't ask "can you show me your code?" — it already knows.

## Why Git? Why Not Just Read the Files?

We already gave Tuesday `[READ_FILE]` on Day 5. She can open any file and read it cover-to-cover. So why do we need Git?

Because reading an entire file is **wasteful**.

### The Token Cost Problem

Let's say you have a 500-line Python file. You changed 3 lines. If Tuesday reads the whole file, she consumes tokens for all 500 lines — 497 of which are completely irrelevant to your question.

Multiply that across a real project with dozens of files, and you're burning through your context window (and your API budget) at an alarming rate.

### The `git diff` Solution

`git diff` solves this elegantly. Instead of dumping the entire file, it returns **only the lines that changed**, with a few lines of surrounding context. That 500-line file becomes a 10-line diff.

Here's a comparison:

| Approach | Tokens Used | Signal-to-Noise |
|---|---|---|
| Full file read (`READ_FILE`) | ~2,000 tokens | Low — 99% unchanged code |
| Git diff (`INSPECT_GIT`) | ~50 tokens | High — only the delta |

This is not a minor optimization. This is the difference between an agent that can analyze 1 file per question and an agent that can analyze an entire repository's worth of changes in a single turn.

### Beyond Token Savings

`git diff` also gives Tuesday something file reading never could — **temporal awareness**. She doesn't just see what the code looks like right now. She sees what *just changed*. That's the difference between:

- "Here is a file with a bug somewhere in 500 lines."
- "Here are the 3 lines you just modified. Line 47 introduced a typo in the variable name."

The second one is what a real senior engineer sitting next to you would say.

## How It Works

### The Tool: `tools/git_inspector.py`

The `inspect_git()` function runs two shell commands:

1. **`git status -s`** — Returns a short list of modified, added, or deleted files. The `-s` flag gives us machine-friendly output (e.g., `M main.py` instead of verbose paragraphs).

2. **`git diff`** — Returns the exact line-by-line changes for all unstaged files. This is the raw delta between the last commit and the current working tree.

Both commands are executed via Python's `subprocess` module with `shell=True` and `capture_output=True`. The results are packaged into a clean JSON string:

```json
{
  "status": "success",
  "git_status": " M main.py\n M tools/git_inspector.py",
  "git_diff": "diff --git a/main.py b/main.py\n..."
}
```

If the folder isn't a Git repo, or Git isn't installed, the function catches the error and returns a structured error message instead of crashing.

### The Trigger: `[INSPECT_GIT]`

This is a zero-argument trigger. When the user asks Tuesday something like "what did I just change?" or "review my recent edits," the LLM responds with the exact tag:

```
[INSPECT_GIT]
```

The main loop detects this tag, calls `inspect_git()`, injects the JSON output into memory, and fires a second LLM call so Tuesday can read the diff and respond intelligently.

### The Flow

```
User: "What did I just change?"
  └─> LLM outputs: [INSPECT_GIT]
        └─> main.py detects trigger
              └─> inspect_git() runs git status + git diff
                    └─> JSON result injected into memory
                          └─> Second LLM call reads the diff
                                └─> Tuesday: "You modified main.py — 
                                     looks like you updated the import 
                                     on line 15 and refactored the loop."
```

## Error Handling

The tool handles three failure modes:

| Error | Cause | Response |
|---|---|---|
| `FileNotFoundError` | Git is not installed on the system | Clean JSON error message |
| Non-zero return code | Not a Git repository, or a Git error | Returns `stderr` content |
| `TimeoutExpired` | Command hung for more than 10 seconds | Timeout error message |

In every case, Tuesday receives a structured JSON response — never a raw Python traceback.

## The Bigger Picture

With the Git Bridge, Tuesday now has five senses:

| Day | Tool | Capability |
|---|---|---|
| Day 3 | `[SEARCH_WEB]` | Real-time web knowledge |
| Day 4 | `[WRITE_FILE]` | Create and save files |
| Day 5 | `[READ_FILE]` | Read local files |
| Day 7 | `[RUN_TERMINAL]` | Execute shell commands |
| **Day 8** | **`[INSPECT_GIT]`** | **See code changes in real-time** |

Each tool adds a new dimension to her awareness. The Git Bridge is special because it gives her the most valuable signal an engineering copilot can have — the delta. Not "what does the code look like?" but "what just happened?"

That's OmniContext. Not omniscience — just the right information, at the right time, in the right format.
