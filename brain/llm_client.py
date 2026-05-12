"""
Tuesday — LLM Client
Handles communication with Large Language Models (OpenAI, Gemini, local models, etc.)
"""

import os


class LLMClient:
    """Interface for talking to LLMs."""

    def __init__(self, provider: str = "openai"):
        self.provider = provider
        self.api_key = self._load_api_key()

    def _load_api_key(self) -> str | None:
        """Load the API key for the configured provider."""
        key_map = {
            "openai": "OPENAI_API_KEY",
            "google": "GOOGLE_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
        }
        env_var = key_map.get(self.provider)
        if env_var:
            return os.getenv(env_var)
        return None

    def chat(self, message: str) -> str:
        """Send a message to the LLM and get a response."""
        # TODO: Implement actual LLM API calls
        raise NotImplementedError(
            f"LLM provider '{self.provider}' not yet implemented."
        )
