"""Tuesday — Git Inspector Tool. Reads the latest commit message via subprocess."""

import subprocess
import json


def get_latest_commit() -> str:
    """Run `git log -1` and return the result as a JSON string."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%s"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode != 0:
            return json.dumps({
                "status": "error",
                "message": result.stderr.strip() or "Git command failed",
            }, indent=2)

        commit_message = result.stdout.strip()

        if not commit_message:
            return json.dumps({
                "status": "success",
                "last_commit": "(no commits found in this repository)",
            }, indent=2)

        return json.dumps({
            "status": "success",
            "last_commit": commit_message,
        }, indent=2)

    except FileNotFoundError:
        return json.dumps({
            "status": "error",
            "message": "Git is not installed or not found in PATH",
        }, indent=2)

    except subprocess.TimeoutExpired:
        return json.dumps({
            "status": "error",
            "message": "Git command timed out after 10 seconds",
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Unexpected error: {str(e)}",
        }, indent=2)


if __name__ == "__main__":
    print("🔍 Tuesday Git Inspector")
    print("=" * 40)
    print(get_latest_commit())
