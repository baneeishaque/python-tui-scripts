#!/usr/bin/env python3
import os
import re

RULES_DIR = "/Users/dk/lab-data/ai-agents/ai-agent-rules"


def migrate_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Match XML-style comments
    xml_pattern = r"^<!--\s*(.*?)\s*-->"
    match = re.search(xml_pattern, content, re.DOTALL)

    if match:
        meta_text = match.group(1).strip()
        # Convert to YAML frontmatter
        new_meta = f"---\n{meta_text}\n---\n"
        new_content = re.sub(xml_pattern, new_meta, content, count=1, flags=re.DOTALL)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"✅ Migrated {os.path.basename(filepath)}")
    else:
        print(f"⏩ Skipping {os.path.basename(filepath)} (no XML meta)")


if __name__ == "__main__":
    for f in os.listdir(RULES_DIR):
        if f.endswith("-rules.md") and f not in ["agent-rules.md"]:
            migrate_file(os.path.join(RULES_DIR, f))
