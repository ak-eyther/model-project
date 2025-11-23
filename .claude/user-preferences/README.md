# User Preferences System

**Version:** 1.0.0
**Last Updated:** 2025-11-23
**Status:** Production-ready

---

## 📖 Overview

The **User Preferences System** allows each developer to define their personal working style, communication preferences, and technical expectations in a git-committed file. All 15 agents automatically read and apply these preferences on every invocation, ensuring consistent behavior that matches how you work best.

### Why This Exists

- **Consistency:** Agents behave the same way across all projects
- **Transferability:** Pull the project, get your preferences automatically
- **Team-friendly:** Each developer has their own preferences file
- **Low-friction:** Set once, agents apply forever
- **Git-tracked:** Version-controlled and shareable

---

## 🏗️ Architecture

### Directory Structure

```
.claude/
├── user-preferences/
│   ├── README.md                    # This file (system documentation)
│   ├── PREFERENCES_TEMPLATE.md      # Template for creating new preferences
│   ├── arif-preferences.md          # Arif's personal preferences
│   └── [username]-preferences.md    # Other developers' preferences
```

### How It Works

1. **Developer creates preferences file** from template
2. **Commits to git** so preferences transfer across projects
3. **Agents auto-load preferences** on every invocation (via "User Preferences Protocol" section in agent definitions)
4. **Agents apply preferences** to all decisions, outputs, and actions

```
┌─────────────────────────────────────┐
│  Developer commits preferences      │
│  to .claude/user-preferences/       │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│  Agent invoked (e.g., @anand-2.0)   │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│  Agent reads user preferences file  │
│  (.claude/user-preferences/         │
│   arif-preferences.md)              │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│  Agent applies preferences to:      │
│  - Communication style              │
│  - Code decisions                   │
│  - Workflow actions                 │
│  - Delegation protocol              │
└─────────────────────────────────────┘
```

---

## 🚀 Quick Start

### For New Developers

1. **Copy the template:**
   ```bash
   cp .claude/user-preferences/PREFERENCES_TEMPLATE.md \
      .claude/user-preferences/[your-name]-preferences.md
   ```

2. **Fill in your preferences:**
   - Open `[your-name]-preferences.md`
   - Read each section and choose your preferences
   - Delete bracketed options, keep your choices
   - Example:
     ```markdown
     ### Style
     - **Verbosity:** Concise and direct  # (removed other options)
     - **Emoji usage:** No emojis unless requested
     ```

3. **Update agent files to reference your preferences:**
   - Edit `.claude/scripts/add-user-preferences-to-agents.py`
   - Change line 22: `**Location:** `.claude/user-preferences/[your-name]-preferences.md``
   - Run: `python .claude/scripts/add-user-preferences-to-agents.py`

4. **Commit your preferences:**
   ```bash
   git add .claude/user-preferences/[your-name]-preferences.md
   git commit -m "Add user preferences for [your-name]"
   git push
   ```

5. **Test it:**
   - Invoke any agent (e.g., `@anand-2.0 implement a feature`)
   - Verify agent follows your preferences (check communication style, workflow)

### For Existing Developers (Updating Preferences)

1. **Edit your preferences file:**
   ```bash
   # Example: Arif updating preferences
   code .claude/user-preferences/arif-preferences.md
   ```

2. **Make changes:**
   - Update sections as needed
   - Add new preferences
   - Remove obsolete ones

3. **Commit changes:**
   ```bash
   git add .claude/user-preferences/arif-preferences.md
   git commit -m "Update communication preferences"
   git push
   ```

4. **Agents auto-load new preferences** on next invocation (no script re-run needed)

---

## 📋 Preferences Categories

### 1. Communication Preferences

**What it controls:**
- Verbosity (concise vs detailed)
- Emoji usage
- Status reporting format (✅/⚠️/❌ vs narrative)
- Blocker communication (blocker-first vs end-with-blockers)
- Response length
- Technical jargon usage

**Example:**
```markdown
## 💬 Communication Preferences

### Style
- **Verbosity:** Concise and direct
- **Emoji usage:** No emojis unless requested
- **Status reporting:** Status-first (✅/⚠️/❌)
- **Blocker communication:** Blocker FIRST, not buried in details
```

**Impact:** Agents will match your preferred communication style in all responses.

---

### 2. Agent Behavior Expectations

**What it controls:**
- Role boundaries (strict vs flexible)
- Delegation protocol (always ask vs auto-invoke)
- Takeover handling (never vs ask-first)
- Permission modes (ask vs auto-accept vs auto-deny)
- Autonomy levels for different operations

**Example:**
```markdown
## 🤖 Agent Behavior Expectations

### Role Boundaries
- **Stay in lane:** Strict boundaries - never cross
- **Delegation protocol:** Always ask before invoking another agent
- **Takeovers:** Never take over another agent's work

### Autonomy Level
- **Safe operations:** Fully autonomous (Read, Grep, Glob)
- **Risky operations:** Always ask (Edit, Write, Bash, Deploy)
```

**Impact:** Agents will know when to ask permission vs proceed autonomously.

---

### 3. Technical Preferences

**What it controls:**
- Security practices (OWASP focus vs standard)
- Over-engineering tolerance (avoid vs allow)
- Code simplicity (minimum viable vs plan-for-future)
- Error handling strategy (boundaries-only vs comprehensive)
- Testing approach (TDD vs test-after vs manual)
- Type safety (strict TypeScript vs lenient)
- Dependency philosophy (minimize vs use-libraries)

**Example:**
```markdown
## 🛠️ Technical Preferences

### Code Quality
- **Security:** Security-first, OWASP top 10 awareness
- **Over-engineering:** Avoid - keep solutions simple
- **Code simplicity:** Minimum viable complexity
- **Error handling:** At system boundaries only (user input, external APIs)

### Development Practices
- **Testing:** Test after implementation, focus on critical paths
- **Type safety:** Strict TypeScript, no `any` types
```

**Impact:** Agents will write code that matches your technical philosophy.

---

### 4. Workflow Preferences

**What it controls:**
- TodoWrite usage (always vs complex-only)
- Task granularity (fine-grained vs high-level)
- Completion marking (immediate vs batch)
- Agent Communication Board updates (after-every-task vs daily)
- Memory updates (every-task vs weekly)
- Git commit frequency (atomic vs feature-based)
- Commit message style (conventional vs descriptive)

**Example:**
```markdown
## 📋 Workflow Preferences

### Task Management
- **TodoWrite usage:** Always for multi-step tasks (3+ steps)
- **Task granularity:** Fine-grained steps
- **Completion marking:** Immediately after done (never batch)

### Progress Tracking
- **Agent Communication Board:** Update after every task completion
- **Memory updates:** After every significant task
```

**Impact:** Agents will manage tasks and track progress according to your workflow.

---

### 5. Design & UI Preferences

**What it controls:**
- Plugin usage (frontend-design mandatory vs optional)
- Component approach (reusable vs single-use)
- Styling methodology (Tailwind vs CSS modules)
- Design philosophy (function-over-form vs equal-balance)
- Animation level (minimal vs rich)
- Accessibility standards (WCAG AA vs AAA)

**Example:**
```markdown
## 🎨 Design & UI Preferences

### Frontend Development
- **Plugin usage:** ALWAYS use frontend-design plugin for new UI work
- **Component approach:** Reusable components preferred
- **Styling:** Tailwind utility-first

### Design Philosophy
- **Aesthetics priority:** Function over form (but must look professional)
- **Design patterns:** Avoid generic AI patterns, create distinctive designs
```

**Impact:** Agents (@hitesh-2.0, @anand-2.0, @varsha-2.0) will follow your design preferences.

---

### 6. Testing & Quality Standards

**What it controls:**
- Coverage targets (>80% vs >60% vs critical-paths)
- Test types (unit+integration+E2E vs unit-focus)
- Test framework (Playwright vs Jest)
- Quality gates (all-tests-pass vs critical-only)
- Code review requirements (always vs post-commit)
- Performance standards (Core Web Vitals vs best-effort)
- What matters vs what doesn't (priorities)

**Example:**
```markdown
## 🧪 Testing & Quality Standards

### Test Coverage
- **Coverage target:** >60% (focus on critical paths)
- **Test types:** Unit + E2E (Playwright for E2E)
- **Test framework:** Playwright for browser testing, Jest for unit tests

### What Matters vs What Doesn't
- **Critical:** Security, correctness, user experience
- **Nice to have:** Perfect coverage, comprehensive docs
- **Don't care about:** Perfect naming, comment style
```

**Impact:** Agents (@harshit-2.0, @ankur-2.0) will validate quality according to your standards.

---

### 7. When Things Go Wrong

**What it controls:**
- Blocker reporting (immediate vs status-update)
- Unblocking approach (proactive-action vs wait)
- Impact assessment (always vs major-only)
- Investigation depth (root-cause vs quick-fix)
- Logging verbosity (comprehensive vs minimal)
- Rollback strategy (immediate vs investigate-first)
- Retry strategy (auto-retry vs ask)

**Example:**
```markdown
## 🚨 When Things Go Wrong

### Blocker Handling
- **Reporting:** Immediate notification with blocker FIRST
- **Unblocking:** Proactive action (don't wait for instructions)
- **Impact assessment:** Always include impact in blocker reports

### Debugging Approach
- **Investigation depth:** Root cause analysis (don't just patch symptoms)
- **Rollback:** Immediate on critical failures, investigate first for non-critical
```

**Impact:** Agents will handle errors and blockers according to your preferred approach.

---

## 🔧 Advanced Usage

### Multi-Developer Projects

**Scenario:** Team of 3 developers, each with different preferences.

**Setup:**
```
.claude/user-preferences/
├── arif-preferences.md       # Arif: Speed-focused, concise
├── john-preferences.md       # John: Quality-focused, detailed
├── sarah-preferences.md      # Sarah: Balanced approach
```

**How it works:**
1. Each developer updates `.claude/scripts/add-user-preferences-to-agents.py` to reference their preferences file
2. Each developer runs the script to update their local agent files
3. Agents read the correct preferences file based on who's using the system
4. **Important:** Don't commit agent file changes if they reference personal preferences (add to `.gitignore`)

**Alternative (recommended):**
- Keep agent files generic (reference template)
- Each developer sets `CLAUDE_USER_PREFERENCES` environment variable
- Agents read from `$CLAUDE_USER_PREFERENCES` path
- (Requires minor modification to agent "User Preferences Protocol" section)

---

### Project-Specific Overrides

**Scenario:** You want different preferences for specific projects.

**Setup:**
```markdown
## 🔧 Project-Specific Customizations

### medical-claims-dashboard
- **Special rules:** WCAG AAA compliance required (vs AA for other projects)
- **Exceptions:** Allow more detailed comments for medical logic
- **Key contacts:** Dr. Smith (domain expert), Jane (compliance)

### internal-tools
- **Special rules:** Speed over polish, quick iterations
- **Exceptions:** Lower test coverage OK (>40% vs >60%)
- **Key contacts:** DevOps team (infrastructure questions)
```

**How it works:**
- Agents check "Project-Specific Customizations" section
- If current project matches, apply overrides
- Otherwise, use global preferences

---

### Preference Inheritance

**Scenario:** You want a base preferences file + role-specific overrides.

**Setup:**
```
.claude/user-preferences/
├── arif-base-preferences.md          # Base preferences
├── arif-frontend-preferences.md      # Frontend-specific overrides
├── arif-backend-preferences.md       # Backend-specific overrides
```

**Example override:**
```markdown
# Frontend-Specific Preferences (Extends arif-base-preferences.md)

## Overrides

### Design & UI Preferences
- **Plugin usage:** MANDATORY use of frontend-design plugin (stricter than base)
- **Accessibility:** WCAG AAA for all public-facing UIs (vs AA in base)
```

**How it works:**
- Frontend agents (@hitesh-2.0, @varsha-2.0) read `arif-frontend-preferences.md`
- Backend agents (@anand-2.0 for backend work) read `arif-backend-preferences.md`
- All agents fall back to `arif-base-preferences.md` for unspecified preferences
- (Requires updating "User Preferences Protocol" section in agent files)

---

## 🛠️ Maintenance

### Updating Agent Files (After Modifying Preferences Location)

If you change the preferences file path or add new developers:

1. **Edit the script:**
   ```bash
   code .claude/scripts/add-user-preferences-to-agents.py
   ```

2. **Update line 22 with new path:**
   ```python
   **Location:** `.claude/user-preferences/[new-file-name].md`
   ```

3. **Run the script:**
   ```bash
   python .claude/scripts/add-user-preferences-to-agents.py
   ```

4. **Verify all agent files updated:**
   ```bash
   grep -r "User Preferences Protocol" .claude/agents/
   # Should show all 15 agent files with updated path
   ```

---

### Validating Preferences

**Check preferences are being applied:**

1. **Invoke an agent with a test task:**
   ```
   @anand-2.0 write a simple hello world function
   ```

2. **Verify agent behavior matches preferences:**
   - Check communication style (concise vs detailed)
   - Check if agent asks for permission (vs auto-executes)
   - Check if TodoWrite is used (if preferences require it)
   - Check if Agent Communication Board is updated

3. **If behavior doesn't match:**
   - Verify agent file has "User Preferences Protocol" section
   - Verify path in protocol matches your preferences file
   - Check preferences file syntax (markdown formatting)
   - Re-run the update script

---

### Troubleshooting

**Problem:** Agents not following preferences

**Solutions:**
1. Check preferences file exists at specified path
2. Verify agent file has "User Preferences Protocol" section (grep for it)
3. Check preferences file has proper markdown formatting
4. Re-run update script: `python .claude/scripts/add-user-preferences-to-agents.py`
5. Test with explicit instruction: "Follow my user preferences from arif-preferences.md"

---

**Problem:** Preferences template is missing sections I need

**Solutions:**
1. Add custom sections to your preferences file (template is just a starting point)
2. Use "Project-Specific Customizations" for one-off needs
3. Submit PR to improve template for all users

---

**Problem:** Multiple developers have conflicting preferences

**Solutions:**
1. Use environment variable approach (`CLAUDE_USER_PREFERENCES`) so each developer's agents read their own file
2. Establish team conventions for shared work (e.g., code review standards)
3. Document exceptions in "Project-Specific Customizations"

---

## 📊 Example Preferences Files

### Speed-Focused Developer (Arif's Actual Preferences)

See: `.claude/user-preferences/arif-preferences.md`

**Characteristics:**
- Concise communication, no emojis
- Status-first reporting (✅/⚠️/❌)
- Blocker FIRST in all reports
- Security-first, no over-engineering
- Auto-accept safe tools, ask for risky ones
- Mandatory TodoWrite for multi-step tasks
- Update Agent Communication Board after every task
- One task in_progress at a time
- 10+ minute post-deployment monitoring

**Best for:** Experienced developers who want fast iteration and minimal friction

---

### Quality-Focused Developer (Example)

**Characteristics:**
- Detailed explanations with examples
- Always ask before any tool use
- Comprehensive testing (>80% coverage)
- TDD approach preferred
- Manual approval for all deployments
- Root cause analysis for all issues
- Extensive documentation required
- Code review before commit

**Best for:** Teams with strict quality requirements or critical systems

---

### Balanced Approach (Example)

**Characteristics:**
- Moderate verbosity, status-first
- Auto-accept for safe operations, ask for risky
- Security + simplicity focus
- Test after implementation (>60% coverage)
- Deploy to staging auto, production manual
- Quick checks + automated alerts
- Standard documentation

**Best for:** General-purpose development, mixed-criticality projects

---

## 🎯 Best Practices

### 1. Start with Template, Iterate
- Don't try to fill out entire template at once
- Start with core sections (Communication, Agent Behavior, Technical)
- Add sections as you discover what matters to you
- Update after trying agents with initial preferences

### 2. Be Specific, Not Generic
❌ **Bad:** "Write good code"
✅ **Good:** "Security-first: OWASP top 10 awareness, input validation at boundaries, no SQL injection, XSS prevention"

❌ **Bad:** "Communicate well"
✅ **Good:** "Status-first: Lead with ✅/⚠️/❌, blocker FIRST (not buried), under 10 lines, no fluff"

### 3. Provide Examples
Agents learn better from examples. Include good vs bad examples:

```markdown
### Communication (Good)
✅ Feature implementation completed!

Key results:
- 8/8 tests passing
- Deployed to staging
- Performance within targets

### Communication (Bad - violates preferences)
I've completed the feature implementation. 🎉

I'm happy to report that the implementation went smoothly...
[5 paragraphs of technical details...]
```

### 4. Update Regularly
- Review preferences quarterly
- After any "agent didn't do what I wanted" moment, update preferences
- Document lessons learned in preferences file
- Version your preferences (add changelog section)

### 5. Share Knowledge
- If you discover a great preference pattern, submit PR to template
- Share your preferences file with team (anonymized if needed)
- Contribute to preference examples in this README

---

## 🔗 Related Documentation

- **Agent Catalog:** `.claude/agents/` - All 15 agent definitions
- **Delegation Protocol:** `.claude/docs/protocols/DELEGATION_PROTOCOL.md` - How agents hand off work
- **Memory Protocol:** `.claude/docs/protocols/MEMORY_PROTOCOL.md` - How agents remember past work
- **DPPM Framework:** `.claude/docs/methodologies/DPPM_FRAMEWORK.md` - Feature development workflow
- **Agent Communication Board:** `AGENT_COMMUNICATION_BOARD.md` - Active task tracking

---

## 📝 Changelog

### Version 1.0.0 (2025-11-23)
- Initial release
- Created preferences template with 9 major categories
- Implemented auto-load mechanism in all 15 agent files
- Added comprehensive documentation
- Included Arif's preferences as reference example

---

**Maintained By:** @memory-expert
**Questions/Issues:** Create issue in project repository
**Contributions:** PRs welcome to improve template and documentation
