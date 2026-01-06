#!/usr/bin/env python3
"""
Bash Command Protection Hook for Mission Inbox
Blocks dangerous commands and warns about risky operations

This hook runs BEFORE Bash commands to prevent:
- Destructive commands (rm -rf /, etc.)
- Force pushes
- Hard resets
- Other dangerous operations
"""
import json
import sys
import re

# Patterns that BLOCK execution (dangerous)
BLOCKED_PATTERNS = [
    (r"rm\s+-rf\s+/(?!\S)", "Attempting to recursively delete from root"),
    (r"rm\s+-rf\s+\.$", "Attempting to delete current directory recursively"),
    (r"rm\s+-rf\s+\.\.$", "Attempting to delete parent directory recursively"),
    (r"git\s+push\s+.*--force\s+.*main", "Force pushing to main branch is forbidden"),
    (r"git\s+push\s+.*--force\s+.*master", "Force pushing to master branch is forbidden"),
    (r"git\s+push\s+-f\s+.*main", "Force pushing to main branch is forbidden"),
    (r"git\s+push\s+-f\s+.*master", "Force pushing to master branch is forbidden"),
    (r">\s*/dev/sda", "Attempting to write to disk device"),
    (r"mkfs\.", "Attempting to format filesystem"),
    (r"dd\s+if=.*of=/dev/", "Attempting to write directly to device"),
]

# Patterns that generate WARNINGS (risky but sometimes needed)
WARN_PATTERNS = [
    (r"git\s+reset\s+--hard", "Hard reset can cause data loss. Are you sure?"),
    (r"git\s+push\s+--force", "Force push can corrupt history for others"),
    (r"git\s+push\s+-f", "Force push can corrupt history for others"),
    (r"rm\s+-rf", "Recursive force delete - double check the path"),
    (r"git\s+rebase", "Rebasing can rewrite history - use with caution"),
    (r"DROP\s+TABLE", "SQL DROP TABLE detected - this is destructive"),
    (r"DROP\s+DATABASE", "SQL DROP DATABASE detected - this is destructive"),
    (r"TRUNCATE\s+TABLE", "SQL TRUNCATE detected - this deletes all data"),
]


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    tool_name = input_data.get("tool_name", "")
    command = input_data.get("tool_input", {}).get("command", "")

    if tool_name != "Bash" or not command:
        sys.exit(0)

    # Check against BLOCKED patterns
    for pattern, warning in BLOCKED_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            error_output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"""
DANGEROUS COMMAND BLOCKED

Command: {command}
Reason: {warning}

This command has been blocked for safety.

If this is intentional:
1. Explain why you need to run this command
2. Ask Arif explicitly for approval
3. Run the command manually if approved
"""
                }
            }
            print(json.dumps(error_output))
            sys.exit(0)

    # Check against WARNING patterns
    for pattern, warning in WARN_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            warn_output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "additionalContext": f"""
RISKY COMMAND WARNING

Command: {command}
Warning: {warning}

Proceed with caution. Make sure you understand what this command does.
"""
                }
            }
            print(json.dumps(warn_output))
            sys.exit(0)

    # Command is safe
    sys.exit(0)


if __name__ == "__main__":
    main()
