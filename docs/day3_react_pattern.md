# Day 3 — The ReAct Pattern (Action Loop)

## What is the ReAct Pattern? (The Chef Analogy)

Imagine you ask a chef, "What can we make for dinner?"
If the chef is locked in a room without a fridge, they can only guess: "Maybe pasta?" (This is what an LLM does without tools).

The **ReAct Pattern** (Reasoning + Acting) gives the chef a walkie-talkie to talk to a kitchen assistant (Python):

1. **Reasoning:** The chef thinks, "I need to know what ingredients we have."
2. **Action:** The chef says the secret trigger word: `[CHECK_FRIDGE]` into the walkie-talkie.
3. **Execution (Python):** You hear the trigger word, open the fridge, write down "Chicken, Rice, Broccoli," and pass the list back under the door.
4. **Second Reasoning:** The chef reads the list and says, "Great! We can make chicken and broccoli stir-fry."

This loop makes the AI an **Agent** rather than just a chatbot.

## How Tuesday Does It

In our code, we use this exact loop for Git:

1. **User:** "What was the last thing I worked on?"
2. **Tuesday (LLM):** Needs to check Git, so she outputs ONLY: `[INSPECT_GIT]`
3. **main.py (Python):** Sees the trigger word! It intercepts the message instead of printing it to the user.
4. **main.py (Python):** Runs `get_latest_commit()` and gets the JSON.
5. **main.py (Python):** Silently adds the JSON to Tuesday's memory and says, "Here is the Git output, now answer the user."
6. **Tuesday (LLM):** Reads the JSON and gives a natural response: "Your last commit was 'Fixed login bug'."

This is incredibly powerful because Tuesday decides *when* to use the tool based purely on her system prompt instructions!
