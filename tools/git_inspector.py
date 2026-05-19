"""Tuesday — Git Inspector Tool. Reads git status and diff via subprocess."""

import subprocess
import json


def inspect_git() -> str:
    """Run `git status -s` and `git diff`, return results as a JSON string."""
    try:
        status_result = subprocess.run(
            "git status -s",
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=10,
        )

        diff_result = subprocess.run(
            "git diff",
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=10,
        )

        for result in (status_result, diff_result):
            if result.returncode != 0:
                return json.dumps({
                    "status": "error",
                    "message": result.stderr.strip() or "Git command failed",
                }, indent=2)

        return json.dumps({
            "status": "success",
            "git_status": status_result.stdout.strip(),
            "git_diff": diff_result.stdout.strip(),
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
    print(inspect_git())
