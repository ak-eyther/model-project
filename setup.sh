#!/bin/bash
# Auto-setup script for claude-code-project-template
# Installs all dependencies for Next.js + FastAPI stack

set -e  # Exit on error

echo "🚀 Claude Code Project Template - Auto Setup"
echo "=============================================="
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    echo "   Visit: https://nodejs.org/"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    echo "   Visit: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Node.js $(node --version) detected"
echo "✅ Python $(python3 --version) detected"
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies (FastAPI backend)..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    echo "✅ Python dependencies installed"
else
    echo "⚠️  requirements.txt not found, skipping Python setup"
fi
echo ""

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies (Next.js frontend)..."
if [ -f "package.json" ]; then
    npm install
    echo "✅ Node.js dependencies installed"
else
    echo "⚠️  package.json not found, skipping Node.js setup"
fi
echo ""

echo "=============================================="
echo "✅ Setup complete! Dependencies installed."
echo ""

# Check if project has been initialized
if [ ! -f ".claude/context/project-context.yaml" ]; then
    echo "⚠️  Project not yet customized for your use case."
    echo ""
    echo "Would you like to initialize this project now?"
    echo "   1. Yes - Quick wizard (Python - updates app files)"
    echo "   2. Yes - Full wizard (Bash - comprehensive setup)"
    echo "   3. No - I'll do it later"
    echo ""
    read -p "Enter choice [1-3]: " init_choice

    if [ "$init_choice" = "1" ]; then
        echo ""
        echo "🔧 Running quick initialization wizard..."
        python3 init-project.py
    elif [ "$init_choice" = "2" ]; then
        echo ""
        echo "🔧 Running full initialization wizard..."
        ./.claude/scripts/init-project.sh
    else
        echo ""
        echo "ℹ️  You can initialize later by running:"
        echo "     python3 init-project.py          (quick wizard)"
        echo "     ./.claude/scripts/init-project.sh (full wizard)"
    fi
fi

echo ""
echo "=============================================="
echo "🚀 Quick Start Commands:"
echo "   Frontend (Next.js):  npm run dev"
echo "   Backend (FastAPI):   uvicorn main:app --reload"
echo ""
echo "📚 See README.md for more details."
