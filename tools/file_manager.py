"""
Tuesday — File Manager Tool
Read, write, and search files on the local system.
"""

import os
from pathlib import Path


def read_file(filepath: str) -> str:
    """Read and return the contents of a file."""
    path = Path(filepath)
    if not path.exists():
        return f"Error: File '{filepath}' not found."
    return path.read_text(encoding="utf-8")


def write_file(filepath: str, content: str) -> str:
    """Write content to a file (creates parent directories if needed)."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"Successfully wrote to '{filepath}'."


def list_directory(dirpath: str = ".") -> list[str]:
    """List all files and folders in a directory."""
    path = Path(dirpath)
    if not path.is_dir():
        return [f"Error: '{dirpath}' is not a directory."]
    return [str(item) for item in path.iterdir()]
