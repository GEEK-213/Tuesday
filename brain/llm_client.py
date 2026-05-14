"""Tuesday — LLM Client.

Multi-provider interface with round-robin key rotation (Gemini),
Groq cloud inference, and local Qwen via Ollama.
"""

import requests
from google import genai
from groq import Groq
from config.settings import (
    GEMINI_KEYS,
    DEFAULT_MODEL,
    QWEN_MODEL_NAME,
    OLLAMA_BASE_URL,
    GROQ_API_KEY,
    GROQ_MODEL_NAME,
)


class LLMClient:
    """Routes messages to the correct LLM provider with automatic failover."""

    def __init__(self, provider: str = "gemini"):
        self.provider = provider
        self.gemini_keys = list(GEMINI_KEYS)
        self.current_key_index = 0
        self.total_keys = len(self.gemini_keys)
        self.client = self._create_gemini_client()
        self.groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

    # ---- Client Factory ----

    def _create_gemini_client(self):
        """Build a Gemini Client with the current API key."""
        if not self.gemini_keys:
            print("[Warning] No Gemini API keys found.")
            return None
        return genai.Client(api_key=self.gemini_keys[self.current_key_index])

    # ---- Key Rotation ----

    def _rotate_key(self) -> bool:
        """Advance to the next Gemini key. Returns False when exhausted."""
        self.current_key_index += 1
        if self.current_key_index < self.total_keys:
            self.client = self._create_gemini_client()
            print(f"[Key Rotation] Switched to key #{self.current_key_index + 1} of {self.total_keys}")
            return True
        return False

    # ---- Main Router ----

    def chat(self, message: str, is_visual: bool = False) -> str:
        """Route a message to the correct provider."""
        if is_visual:
            print("[Router] Visual task → Qwen")
            return self._chat_qwen(message)

        if self.provider == "gemini":
            return self._chat_gemini(message)
        elif self.provider == "groq":
            return self._chat_groq(message)
        elif self.provider == "qwen":
            return self._chat_qwen(message)
        else:
            return f"[Error] Unknown provider: '{self.provider}'"

    # ---- Gemini (with round-robin rotation) ----

    def _chat_gemini(self, message: str) -> str:
        """Send to Gemini, rotating keys on failure. Falls back to Qwen."""
        if not self.gemini_keys:
            print("[Fallback] No Gemini keys. Routing to Qwen.")
            return self._chat_qwen(message)

        self.current_key_index = 0
        self.client = self._create_gemini_client()

        while self.current_key_index < self.total_keys:
            try:
                response = self.client.models.generate_content(
                    model=DEFAULT_MODEL,
                    contents=message,
                )
                return response.text
            except Exception as e:
                print(f"[Gemini Error] Key #{self.current_key_index + 1} failed: {e}")
                if not self._rotate_key():
                    break

        print("[Fallback] All Gemini keys exhausted. Switching to Qwen.")
        return self._chat_qwen(message)

    # ---- Groq ----

    def _chat_groq(self, message: str) -> str:
        """Send to Groq for fast inference."""
        if not self.groq_client:
            return "[Error] Groq API key missing. Add GROQ_API_KEY to .env"

        try:
            completion = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": message}],
                model=GROQ_MODEL_NAME,
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"[Error] Groq request failed: {e}"

    # ---- Qwen (local Ollama) ----

    def _chat_qwen(self, message: str) -> str:
        """Send to a local Qwen model via Ollama."""
        payload = {
            "model": QWEN_MODEL_NAME,
            "prompt": message,
            "stream": False,
        }

        try:
            response = requests.post(OLLAMA_BASE_URL, json=payload, timeout=120)
            response.raise_for_status()
            return response.json().get("response", "[Qwen returned empty]")
        except requests.exceptions.ConnectionError:
            return "[Error] Cannot connect to Ollama. Start it with: ollama serve"
        except requests.exceptions.Timeout:
            return "[Error] Qwen timed out. Model may be loading — try again."
        except requests.exceptions.RequestException as e:
            return f"[Error] Qwen request failed: {e}"
