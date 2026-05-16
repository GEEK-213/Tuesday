import os
import json

def write_file(filename: str, content: str) -> str:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    workspace_dir = os.path.join(project_root, 'workspace')
    
    if not os.path.exists(workspace_dir):
        os.makedirs(workspace_dir)
        
    filepath = os.path.join(workspace_dir, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return json.dumps({"status": "success", "file": f"workspace/{filename}"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})
