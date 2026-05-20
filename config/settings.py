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

# ---- Browser (Web Driver) ----
BROWSER_HEADLESS = os.getenv("BROWSER_HEADLESS", "false").lower() == "true"
BROWSER_TARGET_MONITOR = int(os.getenv("BROWSER_TARGET_MONITOR", "2"))  # 1-indexed
BROWSER_VIEW_DELAY = float(os.getenv("BROWSER_VIEW_DELAY", "3.0"))     # seconds to keep visible
BROWSER_SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "screenshots")

