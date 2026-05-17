import os
import json

def read_file(filepath: str) -> str:
    """Read a local file, restricted to the current working directory or the workspace/ folder."""
    try:
        base_dir = os.path.abspath(os.getcwd())
        workspace_dir = os.path.abspath(os.path.join(base_dir, "workspace"))
        
        target_path = os.path.abspath(filepath)
        
        # Security Check: Prevent directory traversal
        # Ensure the resolved path starts with the base_dir or workspace_dir
        # We append os.sep to ensure we match exact folder structures (e.g., prevent matching "workspace2")
        is_in_base = target_path.startswith(base_dir + os.sep) or target_path == base_dir
        is_in_workspace = target_path.startswith(workspace_dir + os.sep) or target_path == workspace_dir
        
        if not (is_in_base or is_in_workspace):
            return json.dumps({
                "status": "error", 
                "message": "Access Denied: Cannot read files outside the allowed directories."
            })
            
        with open(target_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        return json.dumps({"status": "success", "content": content})
        
    except FileNotFoundError:
        return json.dumps({"status": "error", "message": f"FileNotFoundError: The file '{filepath}' does not exist."})
    except PermissionError:
        return json.dumps({"status": "error", "message": f"PermissionError: Permission denied to read '{filepath}'."})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})
