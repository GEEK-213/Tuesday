"""
Tuesday — System Info Tool
Retrieve OS information, running processes, and system stats.
"""

import platform
import os


def get_system_info() -> dict:
    """Return basic system information."""
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "username": os.getlogin(),
    }


def get_environment_variable(name: str) -> str | None:
    """Safely retrieve an environment variable."""
    return os.getenv(name)
