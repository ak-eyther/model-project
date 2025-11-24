#!/bin/bash

# Plugin Validation Script
# Purpose: Validate that all agent skills/plugins are installed and accessible
# Usage: .claude/scripts/validate-plugins.sh [--fix]

set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Track statistics
TOTAL_AGENTS=0
TOTAL_SKILLS=0
MISSING_SKILLS=0
AVAILABLE_SKILLS=0

echo "========================================="
echo "Plugin Validation for Claude Code Agents"
echo "========================================="
echo ""

# Function to check if a plugin exists
check_plugin() {
    local skill_name="$1"
    local marketplace=""
    local plugin_name=""

    # Parse skill name (format: marketplace:plugin or just plugin)
    if [[ "$skill_name" == *":"* ]]; then
        marketplace="${skill_name%%:*}"
        plugin_name="${skill_name#*:}"
    else
        plugin_name="$skill_name"
    fi

    # Check in global plugins directory
    local plugin_found=false

    # Search all marketplace directories
    for marketplace_dir in ~/.claude/plugins/marketplaces/*/plugins/; do
        if [ -d "${marketplace_dir}${plugin_name}" ]; then
            plugin_found=true
            break
        fi
    done

    if [ "$plugin_found" = true ]; then
        return 0
    else
        return 1
    fi
}

# Function to validate agent skills
validate_agent() {
    local agent_file="$1"
    local agent_name=$(basename "$agent_file" .md)

    echo "Validating: $agent_name"
    echo "---"

    TOTAL_AGENTS=$((TOTAL_AGENTS + 1))

    # Extract skills from YAML frontmatter
    local in_skills=false
    local skills=()

    while IFS= read -r line; do
        # Check if we're in the skills section
        if [[ "$line" == "skills:" ]]; then
            in_skills=true
            continue
        fi

        # Exit skills section if we hit another top-level key
        if [[ "$line" =~ ^[a-zA-Z] ]] && [ "$in_skills" = true ]; then
            break
        fi

        # Extract skill name
        if [ "$in_skills" = true ] && [[ "$line" =~ ^[[:space:]]*-[[:space:]]*([a-zA-Z0-9_:-]+) ]]; then
            skill="${BASH_REMATCH[1]}"
            skills+=("$skill")
        fi
    done < "$agent_file"

    # Validate each skill
    local agent_missing=0
    local agent_available=0

    for skill in "${skills[@]}"; do
        TOTAL_SKILLS=$((TOTAL_SKILLS + 1))

        if check_plugin "$skill"; then
            echo -e "  ${GREEN}✓${NC} $skill"
            agent_available=$((agent_available + 1))
            AVAILABLE_SKILLS=$((AVAILABLE_SKILLS + 1))
        else
            echo -e "  ${RED}✗${NC} $skill (NOT FOUND)"
            agent_missing=$((agent_missing + 1))
            MISSING_SKILLS=$((MISSING_SKILLS + 1))
        fi
    done

    echo ""
    echo "  Agent Skills: $agent_available available, $agent_missing missing"
    echo ""
}

# Main validation loop
echo "Scanning agent definitions in .claude/agents/"
echo ""

for agent_file in .claude/agents/*.md; do
    # Skip AGENT_TEMPLATE.md
    if [[ "$(basename "$agent_file")" == "AGENT_TEMPLATE.md" ]]; then
        continue
    fi

    validate_agent "$agent_file"
done

# Summary
echo "========================================="
echo "Validation Summary"
echo "========================================="
echo ""
echo "Total Agents Scanned: $TOTAL_AGENTS"
echo "Total Skills Declared: $TOTAL_SKILLS"
echo -e "Available Skills: ${GREEN}$AVAILABLE_SKILLS${NC}"
echo -e "Missing Skills: ${RED}$MISSING_SKILLS${NC}"
echo ""

if [ $MISSING_SKILLS -eq 0 ]; then
    echo -e "${GREEN}✓ All skills are installed and accessible!${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠ Some skills are missing. Install them using:${NC}"
    echo ""
    echo "  claude plugin install <skill-name>"
    echo ""
    echo "Or add the marketplace first:"
    echo "  claude plugin marketplace add <marketplace-name>"
    echo ""
    exit 1
fi
