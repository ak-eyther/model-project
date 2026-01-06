#!/usr/bin/env python3
"""
Branch Protection Hook for Mission Inbox
Reminds about branching strategy before commits to main

Per CLAUDE.md and user preferences:
- Always ask first: "Should I create a feature branch for this work?"
- Raise PR and wait for AI review agents to review it
"""
import json
import sys
import subprocess
import os
import re

# Keywords that suggest commit/push operations
COMMIT_KEYWORDS = [
    "commit",
    "push",
    "merge",
    "/commit",
    "/commit-push-pr",
    "deploy",
]


def get_current_branch(cwd):
    """Get the current git branch name."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=5
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    prompt = input_data.get("prompt", "").lower()
    cwd = input_data.get("cwd", os.getcwd())

    # Check if user is trying to commit or push
    is_commit_related = any(keyword in prompt for keyword in COMMIT_KEYWORDS)

    if not is_commit_related:
        sys.exit(0)

    # Get current branch
    current_branch = get_current_branch(cwd)

    if not current_branch:
        sys.exit(0)

    # If on main branch, add reminder
    if current_branch in ["main", "master"]:
        context = f"""
BRANCHING STRATEGY REMINDER

You're about to commit/push to the '{current_branch}' branch.

Per project guidelines (CLAUDE.md + user preferences):
1. Always ask first: "Should I create a feature branch for this work?"
2. Create a feature branch for changes
3. Raise the PR and wait for AI review agents
4. Don't commit directly to main unless it's a trivial fix

Current branch: {current_branch}

RECOMMENDED:
- Create a feature branch: git checkout -b feature/your-feature-name
- Make your changes there
- Push and create a PR for review

If this is a trivial documentation-only change, you may proceed with explicit approval.
"""
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": context
            }
        }
        print(json.dumps(output))

    sys.exit(0)


if __name__ == "__main__":
    main()
