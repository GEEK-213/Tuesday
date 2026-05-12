"""
Tuesday — Settings
Central configuration for the Tuesday AI agent.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ---- General ----
APP_NAME = "Tuesday"
DEBUG = os.getenv("TUESDAY_DEBUG", "false").lower() == "true"
LOG_LEVEL = os.getenv("TUESDAY_LOG_LEVEL", "INFO")

# ---- LLM Defaults ----
DEFAULT_LLM_PROVIDER = "openai"
DEFAULT_MODEL = "gpt-4o"
MAX_CONTEXT_MESSAGES = 50
