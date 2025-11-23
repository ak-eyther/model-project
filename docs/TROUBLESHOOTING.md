# Troubleshooting Guide

Common issues and how to fix them.

---

## 🚫 Setup Wizard Fails

**Symptom:** `python setup.py` crashes

**Causes & Fixes:**

1. **Missing dependencies**
   ```bash
   pip install PyYAML jinja2 questionary
   ```

2. **Python version < 3.8**
   ```bash
   python3 --version  # Should be 3.8+
   ```

3. **Not in git repository**
   ```bash
   git init
   python setup.py  # Retry
   ```

---

## 🔨 Git Hooks Not Triggering

**Symptom:** Commits succeed but pre-commit hook doesn't run

**Fixes:**

1. **Verify hooks installed**
   ```bash
   ls -la .git/hooks/pre-commit  # Should exist and be executable
   ```

2. **Reinstall hooks**
   ```bash
   .claude/scripts/install-hooks.sh
   ```

3. **Check permissions**
   ```bash
   chmod +x .git/hooks/pre-commit
   ```

---

## ❌ Structure Validation Errors

**Symptom:** Pre-commit hook blocks commit with structure violations

**Fix:**

1. **See what's wrong**
   ```bash
   python .claude/scripts/structure_validator.py
   ```

2. **Auto-fix (dry-run first)**
   ```bash
   python .claude/scripts/auto_fix.py --dry-run  # Preview changes
   python .claude/scripts/auto_fix.py --apply    # Apply fixes
   ```

3. **Bypass hook (emergency only)**
   ```bash
   git commit --no-verify -m "[EMERGENCY] message"
   ```

---

## 🤖 Agent Frontmatter Errors

**Symptom:** `validate_setup.py` fails on agent frontmatter

**Fixes:**

1. **Validate all agents**
   ```bash
   .claude/scripts/validate-agent-skills.sh
   ```

2. **Check specific agent**
   ```bash
   head -15 .claude/agents/anand-2.0.md
   # Should have:
   # ---
   # agent_name: "Anand 2.0"
   # permissionMode: ask
   # skills: ...
   # ---
   ```

3. **Fix manually** - Ensure frontmatter has:
   - `agent_name:`
   - `permissionMode:` (ask, auto-accept, or auto-deny)
   - `skills:` (list of skills)
   - Surrounded by `---` delimiters

---

## 💾 Memory System Not Working

**Symptom:** Agents don't remember past work

**Fixes:**

1. **Check memory files exist**
   ```bash
   ls .claude/memory/*-memory.json
   # Should see 14+ files
   ```

2. **Validate JSON structure**
   ```bash
   python3 -c "import json; json.load(open('.claude/memory/anand-2.0-memory.json'))"
   # No output = valid JSON
   ```

3. **Reinitialize memory**
   ```bash
   python setup.py --reinit-memory
   ```

---

## 📝 Jinja2 Placeholders Remain

**Symptom:** CLAUDE.md contains `{{ project_name }}` after setup

**Fix:**

1. **Re-run setup wizard**
   ```bash
   python setup.py
   ```

2. **Manual fix** - Edit files and replace:
   - `{{ project_name }}` → Your Project Name
   - `{{ admin_email }}` → your@email.com
   - `{{ frontend_platform }}` → Vercel (or your platform)
   - `{{ backend_platform }}` → Railway (or your platform)

---

## 🐍 Python Import Errors

**Symptom:** `ModuleNotFoundError: No module named 'yaml'`

**Fix:**

```bash
pip install PyYAML jinja2 questionary anthropic requests
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

---

## 🚀 Deployment Issues

**Symptom:** @shawar-2.0 can't deploy

**Fixes:**

1. **Update deployment URLs** in `.claude/config/project-config.yaml`:
   ```yaml
   deployment:
     frontend:
       production_url: "https://your-app.vercel.app"
     backend:
       production_url: "https://your-api.railway.app"
   ```

2. **Verify platform credentials** (Vercel CLI, Railway CLI installed)

3. **Check agent configuration** - Shawar's agent file should have correct platform references

---

## 🧪 Tests Not Found

**Symptom:** @harshit-2.0 says "test files not found"

**Fix:**

1. **Create test directory**
   ```bash
   mkdir -p tests
   touch tests/__init__.py
   ```

2. **Add tests based on your tech stack** (Playwright, Jest, PyTest, etc.)

---

## 🔄 Upgrade Fails

**Symptom:** `python setup.py --upgrade-to=complete` fails

**Fixes:**

1. **Backup first**
   ```bash
   git add .
   git commit -m "[BACKUP] Before upgrade"
   ```

2. **Clean run**
   ```bash
   rm -rf .claude/config/*.yaml .claude/config/*.json
   python setup.py --upgrade-to=complete
   ```

3. **Manual upgrade** - Copy files from `templates/complete/` to your project

---

## 📞 Get Help

**Still stuck?**

1. **Check agent definitions** - Each agent has troubleshooting sections
2. **Query memory expert**:
   ```
   @memory-expert query experiences similar to: [your issue]
   ```
3. **Read source code** - Scripts have detailed comments
4. **Open an issue** - GitHub repository (if template is on GitHub)

---

## 🛠️ Debug Mode

Enable verbose logging:

```bash
export DEBUG=1
python .claude/scripts/structure_validator.py
```

Or add `--verbose` flag:
```bash
python .claude/scripts/auto_fix.py --verbose --dry-run
```

---

**Most issues resolve with:**
1. Re-running setup wizard
2. Reinstalling git hooks
3. Updating Python dependencies
