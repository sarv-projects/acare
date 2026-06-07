import ast
import os
import glob

DOCS_FILE = os.path.join(os.path.dirname(__file__), "..", "docs", "arch.md")
WORKSPACE_DIR = os.path.join(os.path.dirname(__file__), "..")

def parse_python_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return None
    
    classes = []
    functions = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, ast.FunctionDef) and not isinstance(getattr(node, "parent", None), ast.ClassDef):
            functions.append(node.name)
            
    return {"classes": classes, "functions": functions}

def generate_api_doc():
    api_doc = "## Auto-Generated API Reference\n\n"
    for root, dirs, files in os.walk(WORKSPACE_DIR):
        if ".git" in root or "venv" in root or "node_modules" in root or "__pycache__" in root:
            continue
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, WORKSPACE_DIR)
                data = parse_python_file(filepath)
                if data and (data["classes"] or data["functions"]):
                    api_doc += f"### {rel_path}\n"
                    if data["classes"]:
                        api_doc += "**Classes**:\n"
                        for c in data["classes"]:
                            api_doc += f"- `{c}`\n"
                    if data["functions"]:
                        api_doc += "**Functions**:\n"
                        for f in data["functions"]:
                            api_doc += f"- `{f}`\n"
                    api_doc += "\n"
    return api_doc

def update_docs():
    api_doc = generate_api_doc()
    
    if os.path.exists(DOCS_FILE):
        with open(DOCS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = "# ACARE Architecture\n\n<!-- AUTO-GENERATED-API-START -->\n<!-- AUTO-GENERATED-API-END -->\n"
        
    start_tag = "<!-- AUTO-GENERATED-API-START -->"
    end_tag = "<!-- AUTO-GENERATED-API-END -->"
    
    if start_tag in content and end_tag in content:
        before = content.split(start_tag)[0]
        after = content.split(end_tag)[1]
        new_content = before + start_tag + "\n" + api_doc + end_tag + after
    else:
        new_content = content + "\n\n" + start_tag + "\n" + api_doc + end_tag + "\n"
        
    os.makedirs(os.path.dirname(DOCS_FILE), exist_ok=True)
    with open(DOCS_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    update_docs()
