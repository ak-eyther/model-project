#!/usr/bin/env python3
"""
Add User Preferences Section to All Agent Files

This script adds a standard user preferences section to all agent definition files,
instructing them to read and apply user preferences from the preferences file.
"""

import os
import sys
from pathlib import Path

# Define the user preferences section to be added
USER_PREFERENCES_SECTION = """
---

## 👤 User Preferences Protocol

**MANDATORY: Read user preferences at the start of EVERY invocation**

### User Preferences File
**Location:** `.claude/user-preferences/arif-preferences.md`

**What's Inside:**
- Communication style (concise, no emojis, status-first)
- Agent behavior expectations (strict role boundaries, delegation protocol)
- Technical preferences (security-first, no over-engineering)
- Workflow preferences (TodoWrite for multi-step, commit protocols)
- Design & UI preferences (function over form, frontend-design plugin mandatory)
- Testing & quality standards (what matters vs what doesn't)
- When things go wrong (immediate blocker reporting, proactive action)

### How to Apply User Preferences

**Step 1: Read the preferences file (first invocation only)**
```bash
# Mentally load these preferences:
cat .claude/user-preferences/arif-preferences.md
```

**Step 2: Apply preferences to your work**
- **Communication:** Use concise, scannable format with ✅/⚠️/❌ status indicators
- **Role boundaries:** Stay in your lane (check your MUST/MUST NOT lists)
- **Delegation:** When crossing boundaries, delegate to correct agent
- **Code quality:** Security-first, no over-engineering, simple solutions
- **Workflow:** Use TodoWrite, update Agent Communication Board, mark tasks completed immediately

**Step 3: Check for conflicts**
- If user request contradicts preferences, **ask for clarification**
- Example: User asks you to write code outside your role → Ask if they want you to do it or delegate

**Step 4: Continuous application**
- Apply preferences to **every decision, every output, every action**
- When in doubt, re-read relevant section of preferences file

### Quick Preference Checks

**Before communicating status:**
- ✅ Leading with status emoji (✅/⚠️/❌)?
- ✅ Blocker stated FIRST (not buried in details)?
- ✅ Under 10 lines (unless detailed report requested)?
- ✅ No emojis (unless user explicitly requested)?

**Before writing code:**
- ✅ Is this in my "MUST" list?
- ✅ Am I crossing into another agent's territory?
- ✅ Should I use frontend-design plugin? (Anand/Hitesh for new UI)
- ✅ Am I over-engineering? (Keep it simple)

**Before completing a task:**
- ✅ Updated Agent Communication Board?
- ✅ Marked todo as completed?
- ✅ Updated my memory file?
- ✅ Communicated status using correct format?

### Examples of Applying Preferences

**Example 1: Communication (Good)**
```
✅ Feature implementation completed!

Key results:
- 8/8 tests passing
- Deployed to staging
- Performance within targets

Next step: @ankur-2.0 for quality validation
```

**Example 2: Communication (Bad - violates preferences)**
```
I've completed the feature implementation. 🎉

I'm happy to report that the implementation went smoothly...
[5 paragraphs of technical details]
...and I think this turned out really well.

Would you like me to proceed with the next steps?
```

**Example 3: Staying in lane (Good)**
```
I've completed the code implementation. However, I notice this
needs testing. @harshit-2.0 should run the test suite to verify.
```

**Example 4: Crossing boundaries (Bad - violates preferences)**
```
I've completed the code and also ran the tests myself.
Everything passed, so I'm deploying to production now.
```

### Why This Matters

User preferences represent **how Arif works best**. Following them means:
- ✅ Communication is efficient (no time wasted on verbose updates)
- ✅ Work quality is consistent (matches expectations)
- ✅ Agent system functions smoothly (no boundary violations)
- ✅ Trust is maintained (you behave predictably)

**Remember:** When you respect preferences, Arif can focus on the work instead of correcting your behavior.

"""

def add_preferences_section(agent_file: Path) -> bool:
    """
    Add user preferences section to an agent file if it doesn't already exist.

    Args:
        agent_file: Path to the agent markdown file

    Returns:
        bool: True if section was added, False if already exists
    """
    try:
        # Read the file
        content = agent_file.read_text(encoding='utf-8')

        # Check if preferences section already exists
        if "## 👤 User Preferences Protocol" in content:
            print(f"✓ {agent_file.name} - Preferences section already exists")
            return False

        # Find the position to insert (after the first main heading after frontmatter)
        lines = content.split('\n')
        frontmatter_end = -1
        first_heading = -1

        # Find where frontmatter ends (second occurrence of ---)
        frontmatter_count = 0
        for i, line in enumerate(lines):
            if line.strip() == '---':
                frontmatter_count += 1
                if frontmatter_count == 2:
                    frontmatter_end = i
                    break

        # Find the first H1 or H2 heading after frontmatter
        if frontmatter_end >= 0:
            for i in range(frontmatter_end + 1, len(lines)):
                if lines[i].startswith('# ') or lines[i].startswith('## '):
                    first_heading = i
                    break

        # If we found a good insertion point, add the section
        if first_heading > 0:
            # Insert after the first heading and any content that follows it
            # Find the next section (next ## heading) or end of file
            next_section = len(lines)
            for i in range(first_heading + 1, len(lines)):
                if lines[i].startswith('## '):
                    next_section = i
                    break

            # Insert the preferences section before the next section
            lines.insert(next_section, USER_PREFERENCES_SECTION)

            # Write back to file
            agent_file.write_text('\n'.join(lines), encoding='utf-8')
            print(f"✅ {agent_file.name} - Added user preferences section")
            return True
        else:
            print(f"⚠️  {agent_file.name} - Could not find insertion point")
            return False

    except Exception as e:
        print(f"❌ {agent_file.name} - Error: {e}")
        return False

def main():
    # Get project root (3 levels up from this script)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    agents_dir = project_root / '.claude' / 'agents'

    if not agents_dir.exists():
        print(f"❌ Agents directory not found: {agents_dir}")
        sys.exit(1)

    # Get all .md files in agents directory
    agent_files = list(agents_dir.glob('*.md'))

    if not agent_files:
        print("❌ No agent files found")
        sys.exit(1)

    print(f"\n🔧 Adding user preferences section to {len(agent_files)} agent files...\n")

    added_count = 0
    for agent_file in sorted(agent_files):
        if add_preferences_section(agent_file):
            added_count += 1

    print(f"\n✅ Summary: Added preferences section to {added_count} agent files")
    print(f"📁 Location: .claude/user-preferences/arif-preferences.md\n")

if __name__ == '__main__':
    main()
