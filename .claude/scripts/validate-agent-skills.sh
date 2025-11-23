#!/bin/bash
# Agent Skills & Permission Mode Validation Script
# Created: 2025-11-18
# Purpose: Validate all agent frontmatter configurations

set -e

AGENTS_DIR=".claude/agents"
ERRORS=0
WARNINGS=0

# Color codes for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "=================================================="
echo "  Agent Skills & Permission Mode Validation"
echo "=================================================="
echo ""

# Available skills list
AVAILABLE_SKILLS=(
    "frontend-design:frontend-design"
    "document-skills:xlsx"
    "document-skills:docx"
    "document-skills:pptx"
    "document-skills:pdf"
    "example-skills:webapp-testing"
    "example-skills:canvas-design"
    "example-skills:theme-factory"
    "example-skills:skill-creator"
    "example-skills:mcp-builder"
    "skills-powerkit:marketplace-manager"
    "skills-powerkit:plugin-auditor"
    "skills-powerkit:plugin-creator"
    "skills-powerkit:plugin-validator"
    "skills-powerkit:version-bumper"
)

# Function to check if skill exists
skill_exists() {
    local skill="$1"
    for available in "${AVAILABLE_SKILLS[@]}"; do
        if [ "$skill" == "$available" ]; then
            return 0
        fi
    done
    return 1
}

# Function to extract frontmatter field
get_frontmatter_field() {
    local file="$1"
    local field="$2"

    # Extract frontmatter between --- markers
    sed -n '/^---$/,/^---$/p' "$file" | grep "^${field}:" || echo ""
}

# Function to validate agent file
validate_agent() {
    local file="$1"
    local agent_name=$(basename "$file" .md)
    local has_errors=0

    echo "${BLUE}Validating:${NC} $agent_name"

    # Skip backup files
    if [[ "$agent_name" =~ "backup" || "$agent_name" =~ "task" ]]; then
        echo "  ${YELLOW}⚠ SKIP${NC} - Backup or task file"
        echo ""
        return
    fi

    # Check if file has frontmatter
    if ! grep -q "^---$" "$file"; then
        echo "  ${RED}✗ ERROR${NC} - No YAML frontmatter found"
        ((ERRORS++))
        ((has_errors++))
    fi

    # Check for skills field
    if ! grep -q "^skills:" "$file"; then
        echo "  ${RED}✗ ERROR${NC} - Missing 'skills:' frontmatter field"
        ((ERRORS++))
        ((has_errors++))
    else
        echo "  ${GREEN}✓${NC} Has 'skills:' field"

        # Validate skills exist
        while IFS= read -r line; do
            if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*(.*) ]]; then
                skill="${BASH_REMATCH[1]}"
                if [ -n "$skill" ]; then
                    if skill_exists "$skill"; then
                        echo "    ${GREEN}✓${NC} Skill exists: $skill"
                    else
                        echo "    ${YELLOW}⚠ WARNING${NC} - Unknown skill: $skill"
                        ((WARNINGS++))
                    fi
                fi
            fi
        done < <(sed -n '/^skills:/,/^[a-zA-Z]/p' "$file" | grep "^[[:space:]]*-")
    fi

    # Check for permissionMode field
    if ! grep -q "^permissionMode:" "$file"; then
        echo "  ${RED}✗ ERROR${NC} - Missing 'permissionMode:' frontmatter field"
        ((ERRORS++))
        ((has_errors++))
    else
        permission_mode=$(grep "^permissionMode:" "$file" | sed 's/permissionMode:[[:space:]]*//')
        if [[ "$permission_mode" =~ ^(ask|auto-accept|auto-deny)$ ]]; then
            echo "  ${GREEN}✓${NC} Valid permissionMode: $permission_mode"
        else
            echo "  ${RED}✗ ERROR${NC} - Invalid permissionMode: $permission_mode (must be: ask, auto-accept, or auto-deny)"
            ((ERRORS++))
            ((has_errors++))
        fi
    fi

    # Check disallowedTools syntax if present
    if grep -q "^disallowedTools:" "$file"; then
        echo "  ${GREEN}✓${NC} Has 'disallowedTools:' field"
    fi

    if [ $has_errors -eq 0 ]; then
        echo "  ${GREEN}✓ PASS${NC} - All checks passed"
    fi

    echo ""
}

# Main validation loop
for agent_file in "$AGENTS_DIR"/*.md; do
    if [ -f "$agent_file" ]; then
        validate_agent "$agent_file"
    fi
done

# Summary
echo "=================================================="
echo "  Validation Summary"
echo "=================================================="

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "${GREEN}✓ All agents configured correctly!${NC}"
    echo ""
    echo "All agents have:"
    echo "  • 'skills:' frontmatter field"
    echo "  • 'permissionMode:' frontmatter field"
    echo "  • Valid permission modes (ask, auto-accept, auto-deny)"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo "${YELLOW}⚠ Validation passed with warnings${NC}"
    echo "  Warnings: $WARNINGS"
    echo ""
    echo "Review warnings above for unknown skills"
    exit 0
else
    echo "${RED}✗ Validation failed${NC}"
    echo "  Errors: $ERRORS"
    echo "  Warnings: $WARNINGS"
    echo ""
    echo "Fix errors listed above before proceeding"
    exit 1
fi
