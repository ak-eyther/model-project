#!/bin/bash
# Script to update remaining agent frontmatter with skills and permissionMode
# Created: 2025-11-18

set -e

AGENTS_DIR=".claude/agents"

echo "Updating remaining agents with skills and permissionMode..."
echo ""

# Function to check if frontmatter already has skills
has_skills() {
    grep -q "^skills:" "$1" && return 0 || return 1
}

# Agents already updated:
# - anand-2.0.md ✓
# - hitesh-2.0.md ✓
# - varsha-2.0.md ✓
# - harshit-2.0.md ✓
# - sama-2.0.md ✓
# - atharva-2.0.md ✓

echo "Remaining agents to update:"
echo "- ankur-2.0.md (Quality Validator - read-only)"
echo "- debugger.md (Bug Investigator - read-only)"
echo "- bug-fix-orchestrator.md (Bug Coordinator - read-only)"
echo "- memory-expert.md (Memory Manager - read-only)"
echo "- reflection-expert.md (Reflection Specialist - read-only)"
echo "- shawar-2.0.md (Deployment Expert - limited access)"
echo "- vidya-2.0.md (Solution Architect - read-only)"
echo ""

# List files that need updating
for agent in ankur-2.0 debugger bug-fix-orchestrator memory-expert reflection-expert shawar-2.0 vidya-2.0; do
    file="$AGENTS_DIR/${agent}.md"
    if [ -f "$file" ]; then
        if has_skills "$file"; then
            echo "✓ $agent - Already has skills frontmatter"
        else
            echo "⏳ $agent - Needs update"
        fi
    else
        echo "❌ $agent - File not found"
    fi
done

echo ""
echo "Run manual Edit commands to update each agent's frontmatter"
