import os
import re

def disable_md013(filepath):
    """Prepends markdownlint-disable MD013 if not present."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    if "markdownlint-disable MD013" in content:
        return # Already disabled
        
    print(f"🔧 Disabling MD013 in {filepath}")
    with open(filepath, 'w') as f:
        f.write("<!-- markdownlint-disable MD013 -->\n\n" + content)

def fix_md031(filepath):
    """Ensures blank lines around code fences."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Check if file has code blocks
    if "```" not in content:
        return
        
    original_content = content
    
    # 1. Ensure blank line BEFORE fence start (```lang or ```)
    # Avoid matching if it's start of file or already has blank line
    # Regex: Non-newline, newline, ```
    # Replace with: Non-newline, newline, newline, ```
    
    # We use a loop to handle overlapping matches or multiple instances reliably?
    # Or just re.sub
    
    # Fix missing blank before start fence
    # Look for: (anything not newline)(newline)(```)
    content = re.sub(r'([^\n])\n(```)', r'\1\n\n\2', content)
    
    # Fix missing blank after end fence
    # Look for: (```)(newline)(anything not newline)
    # BUT we must handle the case where the fence content itself ends with newline, then ```.
    # The fence marker is ``` on a line.
    
    # Regex for end fence: \n```\n
    # Followed by text.
    content = re.sub(r'(\n```)\n([^\n])', r'\1\n\n\2', content)
    
    # Also handle list items:
    # If ``` is inside a list, MD031 still applies but indentation matters. 
    # The regex above handles simple cases. 
    # Complex list cases might need `MD046` fix or similar, but let's try this global padding.
    
    if content != original_content:
        print(f"🔨 Fixed MD031 in {filepath}")
        with open(filepath, 'w') as f:
            f.write(content)

def main():
    print("🚀 Starting Surgical Fix V4...")
    
    excluded_dirs = ["node_modules", ".git", "build", "vendor"]
    
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        for file in files:
            if not file.endswith(".md"):
                continue
                
            filepath = os.path.join(root, file)
            
            # 1. Disable MD013 for legacy/generated files
            if (file.startswith("leetcode_") or 
                file.endswith(".ts.md") or 
                file.endswith(".json.md") or 
                file.endswith(".asm.ts.md") or
                "architectures/sync/packages" in filepath): # Broad check for that generated dir
                
                disable_md013(filepath)
            
            # 2. Fix MD031 globally (safe to ensure readability)
            fix_md031(filepath)

if __name__ == "__main__":
    main()
