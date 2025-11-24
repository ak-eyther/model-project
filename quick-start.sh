#!/bin/bash
# Quick Start Script - Simplified project initialization
# For when you want to skip the interactive wizard

set -e

echo "🚀 Quick Start - Claude Code Project Template"
echo "=============================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Ask if user wants full wizard or quick setup
echo "Choose initialization mode:"
echo "  1. Full wizard (recommended for new projects)"
echo "  2. Quick setup (keeps template defaults)"
echo ""
read -p "Enter choice [1-2]: " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "🔧 Starting full initialization wizard..."
    python3 init-project.py
    echo ""
    echo "✅ Project initialized!"
else
    echo ""
    echo "📦 Quick setup - keeping template defaults"
    echo "   You can customize later by running: python3 init-project.py"
fi

echo ""
echo "=============================================="
echo "📚 Next Steps:"
echo ""
echo "1. Install dependencies:"
echo "   ./setup.sh"
echo ""
echo "2. Start development servers:"
echo "   Terminal 1: npm run dev              (Frontend: http://localhost:3000)"
echo "   Terminal 2: uvicorn main:app --reload (Backend: http://localhost:8000)"
echo ""
echo "3. Start coding! 🎉"
echo ""
