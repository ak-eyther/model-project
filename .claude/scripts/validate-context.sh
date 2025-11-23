#!/bin/bash
# validate-context.sh - Validate project context completeness
#
# Usage: ./.claude/scripts/validate-context.sh
#
# This script validates that project-context.yaml has all required fields
# and proper structure. Run this after initialization or before deployment.

set -e

CONTEXT_FILE=".claude/context/project-context.yaml"

echo "🔍 Validating Project Context..."
echo ""

# Check if context file exists
if [ ! -f "$CONTEXT_FILE" ]; then
    echo "❌ Context file missing: $CONTEXT_FILE"
    echo ""
    echo "Run initialization script first:"
    echo "   ./.claude/scripts/init-project.sh"
    echo ""
    exit 1
fi

# Check if file is valid YAML (basic check)
if ! grep -q "^project:" "$CONTEXT_FILE"; then
    echo "❌ Invalid YAML structure (missing 'project:' root key)"
    exit 1
fi

# Define required fields
required_fields=(
    "project.name"
    "project.slug"
    "project.description"
    "project.admin"
    "tech_stack.frontend.framework"
    "tech_stack.backend.framework"
    "deployment.frontend.platform"
    "deployment.backend.platform"
    "deployment.frontend.production_url"
    "deployment.backend.production_url"
)

errors=0
warnings=0

echo "📋 Checking Required Fields:"
echo ""

# Check each required field
for field in "${required_fields[@]}"; do
    # Convert dot notation to grep pattern
    # e.g., "project.name" -> check for "name:" under "project:"
    if echo "$field" | grep -q "\."; then
        # Nested field
        parent=$(echo "$field" | cut -d. -f1)
        child=$(echo "$field" | cut -d. -f2-)

        # Check if parent exists
        if ! grep -q "^$parent:" "$CONTEXT_FILE"; then
            echo "   ❌ Missing section: $parent"
            errors=$((errors + 1))
            continue
        fi

        # Check if child exists (simple check)
        field_key=$(echo "$child" | sed 's/\./:/g')
        if ! grep -q "$field_key:" "$CONTEXT_FILE"; then
            echo "   ❌ Missing field: $field"
            errors=$((errors + 1))
        else
            echo "   ✅ $field"
        fi
    else
        # Top-level field
        if ! grep -q "^$field:" "$CONTEXT_FILE"; then
            echo "   ❌ Missing field: $field"
            errors=$((errors + 1))
        else
            echo "   ✅ $field"
        fi
    fi
done

echo ""
echo "📋 Checking Optional Fields (Warnings):"
echo ""

# Check optional but recommended fields
optional_fields=(
    "domain_context.industry"
    "domain_context.domain"
    "repository.github_url"
)

for field in "${optional_fields[@]}"; do
    parent=$(echo "$field" | cut -d. -f1)
    child=$(echo "$field" | cut -d. -f2-)
    field_key=$(echo "$child" | sed 's/\./:/g')

    if ! grep -q "$field_key:" "$CONTEXT_FILE"; then
        echo "   ⚠️  Missing recommended field: $field"
        warnings=$((warnings + 1))
    else
        echo "   ✅ $field"
    fi
done

echo ""
echo "📋 Checking Initialization Status:"
echo ""

# Check if initialized flag is set
if grep -q "initialized: true" "$CONTEXT_FILE"; then
    echo "   ✅ Project initialized"
else
    echo "   ⚠️  Project not initialized (initialized: false)"
    echo "      This is expected for the template repo"
    warnings=$((warnings + 1))
fi

# Check for template placeholders
if grep -q "claude-code-project-template" "$CONTEXT_FILE"; then
    echo "   ⚠️  Template placeholders detected"
    echo "      Project may not be fully customized"
    warnings=$((warnings + 1))
else
    echo "   ✅ No template placeholders"
fi

# Summary
echo ""
echo "═══════════════════════════════════════════"
echo "📊 Validation Summary"
echo "═══════════════════════════════════════════"
echo ""

if [ $errors -eq 0 ] && [ $warnings -eq 0 ]; then
    echo "✅ Context validation PASSED!"
    echo ""
    echo "   All required fields present"
    echo "   No warnings"
    echo "   Ready for use"
    echo ""
    exit 0
elif [ $errors -eq 0 ]; then
    echo "⚠️  Context validation PASSED with warnings"
    echo ""
    echo "   Errors:   $errors"
    echo "   Warnings: $warnings"
    echo ""
    echo "   Context is valid but has minor issues."
    echo "   Review warnings above."
    echo ""
    exit 0
else
    echo "❌ Context validation FAILED"
    echo ""
    echo "   Errors:   $errors"
    echo "   Warnings: $warnings"
    echo ""
    echo "   Fix errors above before proceeding."
    echo ""
    echo "   To re-initialize context:"
    echo "      ./.claude/scripts/init-project.sh"
    echo ""
    exit 1
fi
