"""
Tuesday — Autonomous AI Agent
Entry point for the Tuesday AI assistant.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def main():
    """Start Tuesday."""
    print("=" * 50)
    print("🤖 Good morning. I'm Tuesday.")
    print("=" * 50)
    print()
    print("Status: Online")
    print(f"Debug Mode: {os.getenv('TUESDAY_DEBUG', 'false')}")
    print()

    # TODO: Initialize the brain (LLM client)
    # TODO: Load available tools
    # TODO: Start the main interaction loop

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

            # Placeholder — will be replaced with LLM calls
            print(f"Tuesday: I heard you say '{user_input}'. "
                  "My brain isn't wired up yet, but I will be soon!\n")

        except KeyboardInterrupt:
            print("\n\nTuesday: Caught interrupt. Shutting down gracefully. 👋")
            break


if __name__ == "__main__":
    main()
