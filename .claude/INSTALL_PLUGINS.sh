#!/bin/bash
# Install recommended official Anthropic plugins

echo "📦 Adding official Anthropic marketplace..."
claude plugin marketplace add anthropics/claude-code

echo ""
echo "🔽 Installing recommended plugins..."
claude plugin install code-review@anthropics/claude-code
claude plugin install ralph-wiggum@anthropics/claude-code
claude plugin install hookify@anthropics/claude-code
claude plugin install explanatory-output-style@anthropics/claude-code

echo ""
echo "✅ Plugin installation complete!"
echo ""
echo "📋 Installed plugins:"
claude plugin list
