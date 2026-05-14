"""Tuesday — Central configuration. Loads env vars and defines defaults."""

import os
from dotenv import load_dotenv

load_dotenv()

# ---- General ----
APP_NAME = "Tuesday"
DEBUG = os.getenv("TUESDAY_DEBUG", "false").lower() == "true"
LOG_LEVEL = os.getenv("TUESDAY_LOG_LEVEL", "INFO")

# ---- LLM Defaults ----
DEFAULT_LLM_PROVIDER = "gemini"
DEFAULT_MODEL = "gemini-3.1-flash-lite"
QWEN_MODEL_NAME = "qwen3-vl:8b"
OLLAMA_BASE_URL = "http://localhost:11434/api/generate"
MAX_CONTEXT_MESSAGES = 50

# ---- Groq ----
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = "llama3-8b-8192"

# ---- Gemini API Key Rotation Pool ----
GEMINI_KEYS = []
for i in range(1, 6):
    key = os.getenv(f"GEMINI_KEY_{i}")
    if key and not key.startswith("your-"):
        GEMINI_KEYS.append(key)
