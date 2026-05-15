"""Tuesday — Memory Module. Persistent conversation history backed by a local JSON file."""

import json
import os


class Memory:
    """Stores conversation history in-memory and persists it to disk."""

    def __init__(self, max_history: int = 50, filepath: str = "data/memory.json"):
        self.max_history = max_history
        self.filepath = filepath
        self.history: list[dict] = []
        self._load_from_disk()

    def add(self, role: str, content: str) -> None:
        """Append a message and persist to disk."""
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        self._save_to_disk()

    def get_context(self) -> list[dict]:
        """Return the full conversation history for LLM context."""
        return self.history.copy()

    def clear(self) -> None:
        """Wipe all history from memory and disk."""
        self.history.clear()
        self._save_to_disk()

    def _save_to_disk(self) -> None:
        """Write current history to the JSON file."""
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)

    def _load_from_disk(self) -> None:
        """Load history from the JSON file if it exists."""
        if not os.path.exists(self.filepath):
            return
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                self.history = data[-self.max_history:]
        except (json.JSONDecodeError, OSError):
            self.history = []
