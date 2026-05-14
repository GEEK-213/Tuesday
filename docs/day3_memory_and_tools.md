# Day 3 — Memory & Tools Reference

> All the "why" and "how" behind today's code changes.  
> The source files themselves are kept clean — this doc is the tutorial layer.

---

## Part 1: Short-Term Memory (LLM History)

### The Problem

LLMs are **stateless**. Every API call is independent — the model has zero memory of what you said 10 seconds ago. That's why Tuesday was responding like a generic Google AI and couldn't remember your name.

### The Fix: Carry a Transcript

Think of a **doctor with a clipboard**:

| Visit | Without Clipboard | With Clipboard |
|-------|------------------|----------------|
| 1 | "I have a headache" → Prescribes aspirin | Same |
| 2 | "It's still hurting" → "What's hurting? Who are you?" | Reads clipboard → "Let's try something stronger" |

The clipboard is our `Memory` class. On every API call, we send the **entire conversation so far** so the model can read it and "remember."

### System Prompt vs. History

| Concept | What It Is | Gemini API Slot |
|---------|-----------|-----------------|
| **System Prompt** | Permanent identity card — "You are Tuesday, you are concise…" | `GenerateContentConfig(system_instruction=...)` |
| **History** | The growing conversation transcript | `contents` parameter (list of `Content` objects) |

The system prompt sits *above* the conversation. It never changes. History grows with each turn.

### Message Flow

```
User types → memory.add("user", msg)
           → memory.get_context() returns full history
           → llm_client.chat(msg, history, system_prompt)
           → API receives: system_instruction + history + new message
           → API responds
           → memory.add("assistant", response)
           → print response
```

---

## Part 2: How Each Provider Receives Memory

### Gemini (google-genai SDK)

Gemini uses structured `Content` objects, not plain dicts:

```python
types.Content(
    role="user",          # or "model" (NOT "assistant")
    parts=[types.Part.from_text(text="Hello")]
)
```

**Key gotcha**: Gemini calls the AI role `"model"`, not `"assistant"`. Our `_build_gemini_contents()` method handles this translation.

The system prompt is injected via:
```python
config = types.GenerateContentConfig(system_instruction="You are Tuesday...")
```

### Groq (OpenAI-compatible)

Groq uses the standard OpenAI messages format — a flat list of dicts:

```python
messages = [
    {"role": "system", "content": "You are Tuesday..."},    # system prompt
    {"role": "user", "content": "Hi"},                       # history msg 1
    {"role": "assistant", "content": "Hello!"},              # history msg 2
    {"role": "user", "content": "What's my name?"},          # new message
]
```

No translation needed — our Memory already stores `"user"` and `"assistant"`.

### Qwen (Ollama)

The local Ollama `/api/generate` endpoint only takes a single `prompt` string. History/system prompt support would require switching to the `/api/chat` endpoint (future improvement).

---

## Part 3: `subprocess` — How Python Runs Terminal Commands

### The Concept

`subprocess` lets Python open an **invisible mini-terminal**, run a command, and capture the output as a string — instead of printing it to the screen.

Analogy — **texting a friend at a terminal**:

1. You (Python): "Run `git log -1` for me"
2. Friend (subprocess): *runs it* → "Output: `Fixed login bug`"
3. You (Python): stores `"Fixed login bug"` in a variable

### `subprocess.run()` Breakdown

```python
result = subprocess.run(
    ["git", "log", "-1", "--pretty=format:%s"],   # command as a list of words
    capture_output=True,                           # grab stdout + stderr
    text=True,                                     # return strings, not bytes
    timeout=10,                                    # abort if it takes >10s
)
```

| Attribute | What It Holds |
|-----------|-------------|
| `result.stdout` | Whatever the command printed (the commit message) |
| `result.stderr` | Error output, if any |
| `result.returncode` | `0` = success, anything else = failure |

### Error Cases Handled in `git_inspector.py`

| Exception | When It Fires |
|-----------|--------------|
| `FileNotFoundError` | Git is not installed on the system |
| `subprocess.TimeoutExpired` | Command hung for more than 10 seconds |
| Non-zero `returncode` | Git ran but failed (e.g., not a git repo) |
| Empty `stdout` | Repo exists but has zero commits |

### Output Format

Every return value is a JSON string:

```json
// Success
{"status": "success", "last_commit": "Added memory to Tuesday"}

// Error
{"status": "error", "message": "Git is not installed or not found in PATH"}
```

---

## File Reference

| File | Purpose | Lines |
|------|---------|-------|
| `brain/llm_client.py` | Multi-provider LLM interface with history + system prompt | ~170 |
| `brain/memory.py` | Conversation history storage (the "clipboard") | ~28 |
| `main.py` | Entry point — loads prompt, creates memory, runs chat loop | ~70 |
| `tools/git_inspector.py` | First OS tool — reads latest git commit via subprocess | ~60 |
| `brain/prompts/system_prompt.txt` | Tuesday's personality and rules | ~22 |
