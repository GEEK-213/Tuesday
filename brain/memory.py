"""
Tuesday — Memory Module
Manages conversation history and context for the AI agent.
"""


class Memory:
    """Stores and retrieves conversation history."""

    def __init__(self, max_history: int = 50):
        self.max_history = max_history
        self.history: list[dict] = []

    def add(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        self.history.append({"role": role, "content": content})
        # Trim if we exceed the max
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def get_context(self) -> list[dict]:
        """Return the full conversation history for LLM context."""
        return self.history.copy()

    def clear(self) -> None:
        """Clear all conversation history."""
        self.history.clear()
