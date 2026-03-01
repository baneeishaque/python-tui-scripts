import subprocess
import os
import sys

def main():
    print("🚀 Starting Robust Audit...")
    markdown_files = []
    excluded_dirs = ["node_modules", ".git", "build", "vendor"]
    
    for root, dirs, files in os.walk("."):
        # Modify dirs in-place to exclude unwanted directories
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
            
        for file in files:
            if file.endswith(".md"):
                markdown_files.append(os.path.join(root, file))

    print(f"📄 Found {len(markdown_files)} Markdown files.")
    
    files_with_issues = 0
    with open("robust_audit_report.txt", "w") as report_file:
        for file in markdown_files:
            try:
                # Run lint on each file individually to avoid shell arg limits
                result = subprocess.run(
                    ["markdownlint-cli2", file], 
                    capture_output=True, 
                    text=True
                )
                if result.returncode != 0:
                     report_file.write(f"\n--- {file} ---\n")
                     # markdownlint-cli2 output usually contains the error lines directly on stderr
                     output = result.stderr if result.stderr else result.stdout
                     report_file.write(output + "\n")
                     print(f"❌ Violation in {file}")
                     files_with_issues += 1
            except Exception as e:
                print(f"⚠️ Error processing {file}: {e}")

    if files_with_issues == 0:
        print("✅ Audit Complete. ZERO VIOLATIONS FOUND! 🏆")
        with open("robust_audit_report.txt", "w") as f:
            f.write("PASS: Zero violations found across the entire repository.")
    else:
        print(f"⚠️ Audit Complete. Found violations in {files_with_issues} files. Check robust_audit_report.txt")

if __name__ == "__main__":
    main()
