import os

def disable_md013(filepath):
    """Prepends markdownlint-disable MD013 if not present."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    if "markdownlint-disable MD013" in content:
        return # Already disabled
        
    print(f"🔧 Disabling MD013 in {filepath}")
    with open(filepath, 'w') as f:
        f.write("<!-- markdownlint-disable MD013 -->\n\n" + content)

def main():
    print("🚀 Starting Surgical Fix V5 (Conversations)...")
    
    # Target directories for disabling MD013
    target_dirs = [
        "ai-agent-rules/conversations",
        "ai-agent-rules/docs/conversations"
    ]
    
    for root, dirs, files in os.walk("."):
        # Check if current root matches one of our targets
        is_target = False
        for t in target_dirs:
            if t in root: # Loose matching (subdirectory ok)
                is_target = True
                break
        
        if is_target:
            for file in files:
                if file.endswith(".md"):
                    disable_md013(os.path.join(root, file))

if __name__ == "__main__":
    main()
