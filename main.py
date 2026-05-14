"""Tuesday — Autonomous AI Agent entry point."""

import os
import sys

# Fix Windows cp1252 encoding so emoji/unicode prints correctly
os.environ["PYTHONUTF8"] = "1"
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from brain.llm_client import LLMClient
from config.settings import GEMINI_KEYS, DEFAULT_LLM_PROVIDER, DEFAULT_MODEL


def main():
    """Boot Tuesday and start the interactive chat loop."""
    print("=" * 50)
    print("🤖 Good morning. I'm Tuesday.")
    print("=" * 50)
    print()
    print("Status: Online")
    print(f"Provider: {DEFAULT_LLM_PROVIDER} | Model: {DEFAULT_MODEL}")
    print(f"Gemini Keys Loaded: {len(GEMINI_KEYS)}")
    print(f"Debug Mode: {os.getenv('TUESDAY_DEBUG', 'false')}")
    print()

    llm_client = LLMClient(provider=DEFAULT_LLM_PROVIDER)

    print("Tuesday is ready. Type 'quit' to exit.")
    print()

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ("quit", "exit", "bye"):
                print("\nTuesday: Goodbye! Have a great day. 👋")
                break
            if not user_input:
                continue

            response = llm_client.chat(user_input)
            print(f"Tuesday: {response}\n")

        except KeyboardInterrupt:
            print("\n\nTuesday: Caught interrupt. Shutting down gracefully. 👋")
            break


if __name__ == "__main__":
    main()
