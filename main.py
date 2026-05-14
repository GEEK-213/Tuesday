"""Tuesday — Autonomous AI Agent entry point."""

import os
import sys

os.environ["PYTHONUTF8"] = "1"
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from brain.llm_client import LLMClient
from brain.memory import Memory
from config.settings import GEMINI_KEYS, DEFAULT_LLM_PROVIDER, DEFAULT_MODEL
from tools.git_inspector import get_latest_commit


def load_system_prompt() -> str:
    """Read Tuesday's system prompt from disk."""
    prompt_path = os.path.join(os.path.dirname(__file__), "brain", "prompts", "system_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip()


def main():
    """Boot Tuesday and start the interactive chat loop."""
    print("=" * 50)
    print("🤖 Good morning. I'm Tuesday.")
    print("=" * 50)
    print()

    system_prompt = load_system_prompt()
    print(f"✅ System prompt loaded ({len(system_prompt)} characters)")

    memory = Memory(max_history=50)
    print("✅ Memory initialized")

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

            # Record user input
            memory.add("user", user_input)
            history = memory.get_context()

            # Ask the AI for a response
            response = llm_client.chat(
                message=user_input,
                history=history,
                system_prompt=system_prompt,
            )

            # Check for Git tool trigger (ReAct loop)
            if "[INSPECT_GIT]" in response:
                print("⚙️ Tuesday is inspecting the repository...")
                
                # Execute tool and save result
                tool_output = get_latest_commit()
                
                # Add JSON to memory as user message
                memory.add("user", f"TOOL OUTPUT:\n{tool_output}")
                
                # Call LLM a second time so it reads the JSON
                history = memory.get_context()
                second_prompt = "I executed the tool. Read the TOOL OUTPUT above and answer the user naturally."
                response = llm_client.chat(
                    message=second_prompt,
                    history=history,
                    system_prompt=system_prompt,
                )

            # Final answer
            memory.add("assistant", response)
            print(f"Tuesday: {response}\n")

        except KeyboardInterrupt:
            print("\n\nTuesday: Caught interrupt. Shutting down gracefully. 👋")
            break


if __name__ == "__main__":
    main()
