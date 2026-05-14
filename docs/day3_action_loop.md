# Day 3 — The Action Loop (ReAct Pattern)

## What is the ReAct Pattern? (The Chef Analogy)

Imagine you ask a chef, "What can we make for dinner?"
If the chef is locked in a room without a fridge, they can only guess: "Maybe pasta?" (This is what an LLM does without tools).

The **ReAct Pattern** (Reasoning + Acting) gives the chef a walkie-talkie to talk to a kitchen assistant (Python):

1. **Reasoning:** The chef thinks, "I need to know what ingredients we have."
2. **Action:** The chef says a secret trigger word: `[CHECK_FRIDGE]` into the walkie-talkie.
3. **Execution (Python):** You hear the trigger word, open the fridge, write down "Chicken, Rice, Broccoli," and slide the list back under the door.
4. **Second Reasoning:** The chef reads the list and says, "Great! We can make chicken and broccoli stir-fry."

This loop is what transforms an LLM from a simple chatbot into an autonomous **Agent**.

---

## How Tuesday Executes the Loop

In our `main.py` code, we use this exact loop for checking Git history:

1. **User asks a question:** "What was the last thing I worked on?"
2. **Tuesday (LLM) reasons:** She recognizes this matches her `TOOLS` instructions in the system prompt.
3. **Tuesday outputs an Action:** She replies with ONLY the trigger word: `[INSPECT_GIT]`
4. **Python intercepts (main.py):** The `while` loop checks `if "[INSPECT_GIT]" in response:`. It sees the trigger word and *does not print it to the user*.
5. **Python executes the tool:** It prints `⚙️ Tuesday is inspecting the repository...`, runs `get_latest_commit()`, and gets the JSON output back from the OS.
6. **Python feeds the data back:** It injects the JSON string directly into Tuesday's `Memory` history as a simulated user message (`"TOOL OUTPUT:\n{tool_output}"`).
7. **Second LLM Call:** Python calls `llm_client.chat()` a second time. Tuesday reads the newly injected JSON data and formulates a natural, conversational response (e.g., "Your last commit was 'Fixed login bug'.").

This loop gives Tuesday agency. She decides *when* to use the tool based purely on her system prompt, and Python handles the heavy lifting of executing the OS commands.
