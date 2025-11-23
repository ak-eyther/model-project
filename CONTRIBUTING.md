# Contributing to Claude Code Project Template

Thank you for your interest in improving this template! 🎉

---

## 🚀 How to Contribute

### Reporting Issues
- **Bug Reports:** Describe the issue, steps to reproduce, expected vs actual behavior
- **Feature Requests:** Explain the use case and why it would be valuable
- **Documentation:** Point out unclear or missing documentation

### Contributing Code

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test your changes:** Run validation and ensure setup wizard works
5. **Commit:** Follow commit message format `[CATEGORY-ID] Description`
6. **Push:** `git push origin feature/your-feature-name`
7. **Open Pull Request**

---

## 📝 Adding New Agents

To contribute a new specialized agent:

1. **Create agent file:** `.claude/agents/your-agent-name.md`
2. **Include frontmatter:**
   ```yaml
   ---
   agent_name: "Your Agent Name"
   background_color: "#HexColor"
   text_color: "#FFFFFF"
   emoji: "🎯"
   role: "Brief role description"
   skills:
     - skill-name:skill-id
   permissionMode: ask|auto-accept|auto-deny
   disallowedTools: []  # Optional
   ---
   ```

3. **Add guardrails:**
   - ✅ What You MUST Do
   - ❌ What You MUST NOT Do

4. **Validate:**
   ```bash
   .claude/scripts/validate-agent-skills.sh
   ```

5. **Add to tier templates** if agent should be included in specific tiers

---

## 🛠️ Improving Scripts

When modifying automation scripts:

1. **Keep portable:** Use dynamic path detection, no hardcoded paths
2. **Add dry-run mode:** For destructive operations
3. **Add comprehensive error handling**
4. **Test on macOS and Linux** (Windows/WSL if possible)
5. **Document:** Add docstrings and comments

---

## 📚 Documentation Standards

- Use clear, concise language
- Include examples and code snippets
- Test all commands before documenting
- Use proper markdown formatting
- Add emoji for visual clarity (but don't overdo it)

---

## 🧪 Testing Checklist

Before submitting a PR, verify:

- [ ] Setup wizard runs successfully (all 3 tiers)
- [ ] Validation passes: `python tests/validate_setup.py`
- [ ] Git hooks work correctly
- [ ] No hardcoded paths or project-specific references
- [ ] Documentation updated (if applicable)
- [ ] No Jinja2 syntax errors in templates

---

## 🎯 Areas We Need Help

- **More agent templates** (mobile testing, security scanning, etc.)
- **Additional tier options** (ultra-minimal, enterprise, etc.)
- **Platform support** (Windows native, better cross-platform testing)
- **Integration examples** (GitHub Actions, GitLab CI, etc.)
- **Translation** (documentation in other languages)

---

## 💡 Code Style

- **Python:** PEP 8, type hints preferred
- **Shell:** Use `set -e`, quote variables, check for command existence
- **Markdown:** ATX headers (`#`), fenced code blocks with language tags

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for making this template better!** 🙏
