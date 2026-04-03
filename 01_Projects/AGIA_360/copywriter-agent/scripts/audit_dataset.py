import os
import re

def audit_markdown_file(filepath):
    """
    Checks for common Markdown linting issues (MD001, MD022, MD041, MD047).
    """
    issues = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if not lines:
        return ["File is empty"]

    # MD041: First line should be H1
    if not lines[0].startswith('# '):
        issues.append(f"MD041: First line is not H1: {repr(lines[0][:20])}")

    last_header_level = 0
    for i, line in enumerate(lines):
        # Header checks
        header_match = re.match(r'^(#+)\s', line)
        if header_match:
            level = len(header_match.group(1))
            
            # MD001: Header levels should increment by one
            if last_header_level != 0 and level > last_header_level + 1:
                issues.append(f"MD001: Header level jump at line {i+1} ({last_header_level} -> {level})")
            last_header_level = level

            # MD022: Headers should be surrounded by blank lines
            if i > 0 and lines[i-1].strip() != '':
                issues.append(f"MD022: Missing blank line before header at line {i+1}")
            if i < len(lines) - 1 and lines[i+1].strip() != '':
                issues.append(f"MD022: Missing blank line after header at line {i+1}")

        # MD009: Trailing spaces
        if line.rstrip('\n').endswith(' '):
            issues.append(f"MD009: Trailing spaces at line {i+1}")

    # MD047: File should end with a single newline character
    if lines[-1].endswith('\n'):
        # Optional: check for excessive empty lines at the end
        empty_count = 0
        for line in reversed(lines):
            if line.strip() == '':
                empty_count += 1
            else:
                break
        if empty_count > 1:
            issues.append(f"MD047/Style: Excessive trailing newlines ({empty_count})")
    else:
        issues.append("MD047: Missing newline at end of file")

    return issues

def audit_directory(directory):
    print(f"Auditing directory: {directory}")
    all_issues = {}
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            filepath = os.path.join(directory, filename)
            issues = audit_markdown_file(filepath)
            if issues:
                all_issues[filename] = issues
    
    if not all_issues:
        print("✅ No issues found! 100% Professional Certification.")
    else:
        for filename, issues in all_issues.items():
            print(f"\n❌ Issues in {filename}:")
            for issue in issues[:10]: # Stop at 10 per file to avoid too much noise
                print(f"  - {issue}")
            if len(issues) > 10:
                print(f"  ... and {len(issues) - 10} more.")

if __name__ == "__main__":
    audit_directory('/home/npe927/SaaS_Factory/agia-360/copywriter-agent/02_DATASET_TRONCAL/')
