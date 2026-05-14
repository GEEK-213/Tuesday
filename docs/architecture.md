# Tuesday — Architecture & How It All Connects

## Overview

Tuesday is a multi-provider AI agent that routes user messages to the best available LLM. It supports **3 providers** (Gemini, Groq, Qwen) with automatic failover and API key rotation.

---

## Project Structure

```
Tuesday/
├── main.py                  # Entry point — boots the agent, runs the chat loop
├── requirements.txt         # Python dependencies
├── .env                     # API keys (never committed to Git)
├── .env.example             # Template showing required env vars
├── .gitignore               # Keeps .env and __pycache__ out of Git
│
├── brain/                   # Core AI logic
│   ├── __init__.py
│   ├── llm_client.py        # Multi-provider LLM router with key rotation
│   ├── memory.py            # Conversation history manager
│   └── prompts/             # (Future) System prompts and templates
│
├── config/                  # Centralized configuration
│   ├── __init__.py
│   └── settings.py          # Loads .env, defines all defaults and constants
│
├── docs/                    # Documentation
├── tools/                   # (Future) Agent tools (web search, file I/O, etc.)
├── skills/                  # (Future) Composable agent skills
├── models/                  # (Future) Data models and schemas
└── tests/                   # (Future) Unit and integration tests
```

---

## Data Flow

```
User Input
    │
    ▼
  main.py ──► LLMClient.chat(message)
                  │
                  ├── provider == "gemini" ──► _chat_gemini() ──► Gemini API (with key rotation)
                  │                                │ (on failure)
                  │                                ▼
                  │                           _chat_qwen() ← ultimate fallback
                  │
                  ├── provider == "groq"   ──► _chat_groq()  ──► Groq API
                  │
                  ├── provider == "qwen"   ──► _chat_qwen()  ──► Local Ollama
                  │
                  └── is_visual == True    ──► _chat_qwen()  ──► Local Ollama
                  
    ▼
Response printed to terminal
```

---

## Provider Details

### Gemini (Cloud — Primary)
- **SDK**: `google-genai` (client-based, NOT the deprecated `google-generativeai`)
- **Model**: `gemini-3.1-flash-lite` (500 RPD free tier)
- **Auth**: 5 API keys in `.env` (`GEMINI_KEY_1` through `GEMINI_KEY_5`)
- **Key Rotation**: Round-robin — if key #1 gets a 429/error, automatically tries #2, #3, etc.
- **Fallback**: If all 5 keys fail, automatically routes to local Qwen

### Groq (Cloud — Fast)
- **SDK**: `groq`
- **Model**: `llama3-8b-8192`
- **Auth**: Single key in `.env` (`GROQ_API_KEY`)
- **Use case**: When you need near-instant responses

### Qwen (Local — Offline)
- **Method**: HTTP POST to Ollama REST API via `requests`
- **Model**: `qwen3-vl:8b` (vision-language model)
- **Endpoint**: `http://localhost:11434/api/generate`
- **Requires**: Ollama running locally (`ollama serve`)
- **Use case**: Visual tasks, offline mode, ultimate fallback when cloud keys are exhausted

---

## Key Rotation — How It Works

```
Message arrives
    │
    ▼
Start at Key #1
    │
    ├── Success? → Return response
    │
    └── Error? → Log it, move to Key #2
                    │
                    ├── Success? → Return response
                    │
                    └── Error? → Move to Key #3 ... → Key #5
                                                        │
                                                        └── All failed? → Fallback to Qwen
```

The `current_key_index` resets to 0 on every new message, so all keys get fair usage.

---

## Configuration Map

All config lives in `config/settings.py`. It loads `.env` once at import time via `python-dotenv`.

| Variable | Source | Default | Purpose |
|---|---|---|---|
| `DEFAULT_LLM_PROVIDER` | Hardcoded | `"gemini"` | Which provider `main.py` uses |
| `DEFAULT_MODEL` | Hardcoded | `"gemini-3.1-flash-lite"` | Gemini model name |
| `QWEN_MODEL_NAME` | Hardcoded | `"qwen3-vl:8b"` | Ollama model tag |
| `OLLAMA_BASE_URL` | Hardcoded | `http://localhost:11434/api/generate` | Local Ollama endpoint |
| `GROQ_API_KEY` | `.env` | `None` | Groq authentication |
| `GROQ_MODEL_NAME` | Hardcoded | `"llama3-8b-8192"` | Groq model |
| `GEMINI_KEYS` | `.env` | `[]` | List of up to 5 Gemini API keys |
| `DEBUG` | `.env` | `false` | Toggle debug mode |
| `LOG_LEVEL` | `.env` | `"INFO"` | Logging verbosity |

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| `python-dotenv` | ≥1.0.0 | Load `.env` files into `os.environ` |
| `google-genai` | ≥2.2.0 | Gemini API (new client-based SDK) |
| `groq` | ≥1.2.0 | Groq API for fast LLaMA inference |
| `requests` | ≥2.31.0 | HTTP calls to local Ollama server |
| `rich` | ≥13.7.0 | Terminal formatting (future use) |

---

## Environment Setup Quick Reference

```bash
# 1. Clone and enter the project
cd Tuesday

# 2. Create your .env from the template
copy .env.example .env

# 3. Fill in your API keys in .env

# 4. Install dependencies
pip install -r requirements.txt

# 5. Start local model server (optional)
ollama serve

# 6. Run Tuesday
python main.py
```

---

## Security Notes

- `.env` is in `.gitignore` — API keys are never committed
- `.env.example` contains only placeholder values (`your-*-here`)
- Gemini keys with `your-` prefix are auto-filtered out in `settings.py`
- Groq client only initializes if `GROQ_API_KEY` is present
