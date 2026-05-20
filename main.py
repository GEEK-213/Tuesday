"""Tuesday — Autonomous AI Agent entry point."""

import os
import sys
import datetime
import re

os.environ["PYTHONUTF8"] = "1"
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from brain.llm_client import LLMClient
from brain.memory import Memory
from config.settings import GEMINI_KEYS, DEFAULT_LLM_PROVIDER, DEFAULT_MODEL
from tools.git_inspector import inspect_git
from tools.web_search import search_web
from tools.file_writer import write_file
from tools.file_reader import read_file
from tools.terminal_executor import run_command
from tools.web_driver import inspect_url
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


def load_system_prompt() -> str:
    """Read Tuesday's system prompt from disk and inject current time."""
    prompt_path = os.path.join(os.path.dirname(__file__), "brain", "prompts", "system_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        raw_prompt = f.read().strip()
        
    current_time = datetime.datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
    return f"{raw_prompt}\n\n[SYSTEM INFO]\nThe current date and time is: {current_time}"


def main():
    """Boot Tuesday and start the interactive chat loop."""
    print("=" * 50)
    print("🤖 Good morning. I'm Tuesday.")
    print("=" * 50)
    print()

    system_prompt = load_system_prompt()
    print(f"✅ System prompt loaded ({len(system_prompt)} characters)")

    memory = Memory(max_history=50, filepath="data/memory.json")
    print(f"✅ Memory initialized ({len(memory.get_context())} messages recalled from disk)")

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

            if "[INSPECT_GIT]" in response:
                print("🔍 Tuesday is scanning the Git tree...")

                tool_output = inspect_git()

                memory.add("user", f"TOOL OUTPUT:\n{tool_output}")
                history = memory.get_context()
                followup = "I executed the tool. Read the TOOL OUTPUT above and answer the user naturally."
                response = llm_client.chat(
                    message=followup,
                    history=history,
                    system_prompt=system_prompt,
                )

            # Web Search ReAct loop (max 2 attempts for query reformulation)
            search_attempts = 0
            while "[SEARCH_WEB:" in response and search_attempts < 2:
                search_attempts += 1

                start = response.index("[SEARCH_WEB:") + len("[SEARCH_WEB:")
                end = response.index("]", start)
                query = response[start:end].strip()

                print(f"🌐 Tuesday is searching the web for: {query}...")
                if search_attempts == 2:
                    print("🔄 Retry — reformulated query.")

                tool_output = search_web(query)

                memory.add("user", f"TOOL OUTPUT:\n{tool_output}")

                history = memory.get_context()
                followup = "I executed the web search tool. Read the TOOL OUTPUT above and answer the user naturally."
                response = llm_client.chat(
                    message=followup,
                    history=history,
                    system_prompt=system_prompt,
                )

            # File Writer ReAct loop (regex-based robust parsing)
            write_match = re.search(
                r"\[WRITE_FILE:\s*(.+?)\s*\|\|\|\s*(.*)\]$",
                response,
                re.DOTALL,
            )
            if write_match:
                filename = write_match.group(1).strip()
                content = write_match.group(2).strip()

                # Safety: strip accidental 'workspace/' prefix from filename
                filename = re.sub(r"^workspace[\\/]", "", filename)

                print(f"✍️ Tuesday is writing to workspace/{filename}...")

                tool_output = write_file(filename, content)

                memory.add("user", f"TOOL OUTPUT:\n{tool_output}")
                history = memory.get_context()
                followup = "I executed the tool. Read the TOOL OUTPUT above and confirm to the user naturally."
                response = llm_client.chat(
                    message=followup,
                    history=history,
                    system_prompt=system_prompt,
                )

            # File Reader ReAct loop
            if "[READ_FILE:" in response:
                start = response.index("[READ_FILE:") + len("[READ_FILE:")
                end = response.index("]", start)
                filepath = response[start:end].strip()

                print(f"📖 Tuesday is reading {filepath}...")
                
                tool_output = read_file(filepath)
                
                memory.add("user", f"TOOL OUTPUT:\n{tool_output}")
                history = memory.get_context()
                followup = "I executed the tool. Read the TOOL OUTPUT above and answer the user naturally."
                response = llm_client.chat(
                    message=followup,
                    history=history,
                    system_prompt=system_prompt,
                )

            terminal_match = re.search(
                r"\[RUN_TERMINAL:\s*(.+?)\]$",
                response,
                re.DOTALL,
            )
            if terminal_match:
                command = terminal_match.group(1).strip()
                print(f"⚡ Tuesday is executing: {command}...")

                tool_output = run_command(command)

                memory.add("user", f"TOOL OUTPUT:\n{tool_output}")
                history = memory.get_context()
                followup = "I executed the command. Read the TOOL OUTPUT above and answer the user naturally."
                response = llm_client.chat(
                    message=followup,
                    history=history,
                    system_prompt=system_prompt,
                )

            web_match = re.search(
                r"\[INSPECT_WEB:\s*(.+?)\]$",
                response,
                re.DOTALL,
            )
            if web_match:
                url = web_match.group(1).strip()
                console.print(f"\n[bold cyan]🌐 Tuesday is opening browser → [underline]{url}[/underline][/bold cyan]")

                tool_output = inspect_url(url)

                # Rich display of browser results in terminal
                try:
                    import json as _json
                    result = _json.loads(tool_output)
                    if result.get("status") == "success":
                        title = result.get("title", "No title")
                        screenshot = result.get("screenshot")
                        content_preview = result.get("content", "")[:300]

                        panel_content = f"[bold white]{title}[/bold white]\n"
                        if screenshot:
                            panel_content += f"[dim]📸 Screenshot saved: {screenshot}[/dim]\n"
                        panel_content += f"\n[dim]{content_preview}...[/dim]"

                        console.print(Panel(
                            panel_content,
                            title="[bold green]✅ Page Captured[/bold green]",
                            border_style="green",
                            padding=(1, 2),
                        ))
                    else:
                        console.print(Panel(
                            f"[bold red]{result.get('message', 'Unknown error')}[/bold red]",
                            title="[bold red]❌ Browser Error[/bold red]",
                            border_style="red",
                        ))
                except Exception:
                    pass

                memory.add("user", f"TOOL OUTPUT:\n{tool_output}")
                history = memory.get_context()
                followup = "I executed the tool. Read the TOOL OUTPUT above and answer the user naturally."
                response = llm_client.chat(
                    message=followup,
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
