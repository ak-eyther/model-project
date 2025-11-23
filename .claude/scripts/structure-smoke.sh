#!/bin/bash
#
# Quick smoke test: validate structure and run auto-fix in dry-run mode.
#

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"

echo "🔍 Running structure validator (full)..."
python3 .claude/scripts/structure_validator.py --mode full

echo ""
echo "🧪 Running auto-fix (dry run)..."
python3 .claude/scripts/auto_fix.py --dry-run

echo ""
echo "✅ Smoke test complete."
