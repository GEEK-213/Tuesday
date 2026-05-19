import subprocess
import json

def run_command(command: str) -> str:
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return json.dumps({"status": "success", "output": result.stdout})
        else:
            return json.dumps({"status": "error", "error": result.stderr})
    except subprocess.TimeoutExpired:
        return json.dumps({"status": "error", "error": "Command timed out after 10 seconds."})
