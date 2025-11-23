# Arif Khan's User Preferences

**User:** arif.khan@vitraya.com
**Role:** Project Owner & Technical Lead
**Last Updated:** 2025-11-23

---

## 🎯 Core Philosophy

**"Plain simple if I can see the info correctly"**

- Prioritize functionality over aesthetics
- Value clarity and correctness above all
- Prefer working solutions over perfect solutions
- Focus on delivering value, not over-engineering

---

## 💬 Communication Preferences

### Style
- **Concise and direct** - No fluff, get to the point
- **No emojis** unless explicitly requested
- **Scannable format** - Use bullet points, clear headings
- **Status-first** - Lead with ✅/⚠️/❌ so I know the outcome immediately
- **No verbose reports** - Keep updates under 10 lines when possible

### What I Want to See
- **The blocker FIRST** - Don't bury critical issues in details
- **What you did to unblock** - Show proactive action taken
- **Next steps** - Always tell me what happens next
- **Impact** - Why does this matter to the project?

### What I Don't Want
- Long technical explanations unless I ask for them
- Assumptions that I'll read full details
- Over-the-top validation or praise ("You're absolutely right!")
- Suggestions to "improve" working code without a specific reason

### Example (Good)
```
⚠️ BLOCKER: Production deployment stuck

Issue: Railway won't auto-deploy
Needs: Manual trigger via CLI
Impact: Blocks final release

I've created urgent request file and notified deployment team.
```

### Example (Bad)
```
The deployment process has encountered some challenges...
[5 paragraphs of technical details]
...and we might need to consider alternative approaches.
Would you like me to proceed?
```

---

## 🤖 Agent Behavior Expectations

### Strict Role Boundaries
- **Agents must stay in their lane** - No crossing boundaries
- **Pure orchestrators don't execute** - Atharva plans, never codes
- **Executors don't plan** - Anand codes, never designs architecture
- **Validators don't implement** - Ankur reviews, never fixes code

### Delegation Protocol
- **Always ask before invoking an agent** - Don't assume
- **Use the right specialist** - Don't try to do it yourself
- **Explicit handoffs** - Clear communication between agents
- **No takeovers** - If an agent is stuck, diagnose why, don't replace them

### Autonomy vs Control
- **Autonomous for safe operations** - Reading files, gathering info, planning
- **Ask for permission** - Writing code, deploying, deleting files
- **No surprises** - Tell me before making significant changes
- **Explain deviations** - If you must break a pattern, tell me why

---

## 🛠️ Technical Preferences

### Code Quality Standards
- **Security first** - No XSS, SQL injection, command injection, OWASP top 10
- **No over-engineering** - Don't add features I didn't ask for
- **Simple solutions** - Three similar lines > premature abstraction
- **No backwards-compatibility hacks** - If unused, delete it completely
- **Trust internal code** - Only validate at system boundaries

### What NOT to Do
- ❌ Add features beyond what was requested
- ❌ Refactor surrounding code during bug fixes
- ❌ Add docstrings/comments to code you didn't change
- ❌ Create helpers/utilities for one-time operations
- ❌ Add error handling for scenarios that can't happen
- ❌ Design for hypothetical future requirements
- ❌ Add feature flags or compatibility shims unnecessarily

### Technology Choices
- **Frontend:** React + TypeScript + Vite (or plain HTML when requested)
- **Backend:** FastAPI + Python
- **Deployment:** Vercel (frontend), Railway (backend)
- **Testing:** Playwright + Chrome DevTools
- **Version Control:** Git (always use it)
- **AI/ML:** Claude AI (Anthropic)

### Design Philosophy
- **Use frontend-design plugin** for all new UI work (mandatory for Anand/Hitesh)
- **Plain HTML acceptable** for admin dashboards and internal tools
- **Data density over aesthetics** for admin interfaces
- **Responsive but desktop-first** for professional tools

---

## 📋 Workflow Preferences

### Task Management
- **Use TodoWrite** for multi-step tasks (mandatory)
- **Update Agent Communication Board** after every task (mandatory)
- **Mark tasks completed immediately** - Don't batch completions
- **One task in_progress at a time** - Focus matters

### When Direction Changes
If I say "stop that, do this instead":
1. Update Agent Communication Board (move to ⏸️ Paused)
2. Update your memory (why stopped, new priority)
3. Start new task immediately
4. Learn from the priority shift

### Git & Commits
- **Commit message format:** Clear, concise, explains WHY not WHAT
- **Include co-authored-by:** Claude footer in all commits
- **Never skip hooks** unless I explicitly request it
- **Never force push to main/master** (warn me if I request it)
- **Test before commit** when possible

### Deployment
- **Always delegate to @shawar-2.0** - Never deploy yourself
- **Test in all environments** - dev → staging → production
- **Health checks mandatory** - Verify deployment succeeded
- **Monitor post-deploy** - Watch for issues 10+ minutes after

---

## 🎨 Design & UI Preferences

### General Approach
- **Function over form** - Does it work? Can I read it?
- **Plain and simple** when explicitly stated
- **Data-dense admin interfaces** - Show me all the info
- **Polish is Phase 2** - MVP first, aesthetics later

### Frontend-Design Plugin Usage
- **Mandatory for Anand/Hitesh** when implementing new designs
- **Read-only for Varsha** (exploration, not implementation)
- **Exception:** Bug fixes and refactoring can be manual
- **Never manually code** new UI components with design requirements

### Component Standards
- **Accessible by default** - WCAG compliance
- **Responsive but pragmatic** - Desktop-first for admin tools
- **Consistent with existing patterns** - Check codebase first
- **Tailwind CSS preferred** - Use existing design system

---

## 🧪 Testing & Quality

### Test Execution
- **@harshit-2.0 runs tests** - He executes, reports results
- **@ankur-2.0 validates quality** - He reviews, gives verdicts
- **Never conflate the roles** - Testing ≠ Quality validation

### What I Care About
- **Does it work?** - Functional correctness first
- **Is it secure?** - No vulnerabilities
- **Is it maintainable?** - Can future me understand it?
- **Does it match the spec?** - Did you deliver what I asked for?

### What I Don't Care About (Usually)
- Perfect test coverage (pragmatic coverage is fine)
- Premature optimization (unless it's a bottleneck)
- Theoretical edge cases (focus on real scenarios)
- Code style nitpicks (unless it impacts readability)

---

## 🚨 When Things Go Wrong

### Bug Investigation
- **@debugger investigates** - Root cause analysis
- **@harshit-2.0 reproduces** - Failing test proves it
- **@anand-2.0 fixes** - Implementation
- **Don't skip reproduction** - Prove the bug exists

### Blockers
- **Tell me immediately** - Don't wait
- **Be specific** - What exactly is blocking you?
- **Propose solutions** - What can unblock you?
- **Show proactive action** - What did you already try?

### When Stuck
- **Diagnose root cause** - Why are you stuck?
- **Don't take over** - Help the agent, don't replace them
- **Fix the blocker** - Missing env var? Wrong command?
- **Let same agent retry** - They learn from failures

---

## 📚 Learning & Memory

### What to Remember
- **My feedback patterns** - What I approve/reject
- **My decision rationale** - Why I chose X over Y
- **My risk tolerance** - What I'm comfortable with
- **My communication triggers** - What annoys me vs what I value

### What to Forget
- One-off requests that don't represent patterns
- Temporary workarounds (remember the proper solution)
- Experimental approaches I rejected

### Memory Queries
- **Query @memory-expert BEFORE planning** - Learn from past work
- **Submit experiences AFTER completion** - Share learnings
- **Reference past patterns** - Don't reinvent the wheel

---

## 🎓 Specific Patterns from Past Work

### From Conversations
- "Plain simple HTML if I can see the info correctly" → Prefer simplicity
- Asking agents to be invoked → Respect delegation protocol
- Interrupting with "stop that, do this" → Priorities shift, adapt quickly
- Validation fixes → Care about correctness and proper setup

### Technical Decisions
- ChromaDB for memory (semantic search valuable)
- 15-agent orchestration system (specialization matters)
- Tri-tier memory (hot/warm/cold) (optimize for relevance)
- Git-based project templates (reproducibility important)

### Quality Signals
- ✅ Fixed all validation errors before moving on
- ✅ Asked for confirmation before pushing to git
- ✅ Wanted deployment delegated to specialist
- ✅ Cares about transferable project knowledge

---

## 🔄 Continuous Improvement

### When to Update This File
- I give explicit feedback on agent behavior
- I express frustration with a pattern
- I praise a specific approach
- I make a technical decision with rationale
- I establish a new workflow preference

### How Agents Should Use This
1. **Read this file when invoked** - Know my preferences
2. **Apply preferences to decisions** - Use my mental model
3. **Flag conflicts** - If my request contradicts my preferences, ask
4. **Suggest updates** - If you notice a new pattern, propose adding it

---

## 🎯 Success Criteria

**I know agents are following my preferences when:**
- ✅ Communication is concise and scannable
- ✅ Blockers are reported immediately with impact
- ✅ Agents stay in their lanes (no boundary violations)
- ✅ Code is simple, secure, and matches the spec
- ✅ Delegation happens automatically (right agent for right task)
- ✅ No over-engineering or unnecessary features
- ✅ Agents learn from past work (query memory first)
- ✅ Quality is high but pragmatic (not perfectionist)

**I know preferences need updating when:**
- ❌ I repeatedly correct the same behavior
- ❌ Agents make assumptions I don't like
- ❌ Communication style frustrates me
- ❌ Technical decisions don't match my expectations

---

## 📖 Related Documentation

- **Global CLAUDE.md:** `~/.claude/CLAUDE.md` (cross-project rules)
- **Project CLAUDE.md:** `/CLAUDE.md` (this project's specifics)
- **Agent Catalog:** `.claude/agents/*.md` (agent definitions)
- **Delegation Protocol:** `.claude/docs/protocols/DELEGATION_PROTOCOL.md`
- **Memory Protocol:** `.claude/docs/protocols/MEMORY_PROTOCOL.md`

---

**Remember:** These preferences represent how I work best. When in doubt, optimize for clarity, simplicity, and correctness. Ask questions rather than make assumptions. I'd rather be asked 10 times than have you guess wrong once.

---

**Version:** 1.0.0
**Bootstrapped:** 2025-11-23
**Source:** Extracted from CLAUDE.md + conversation history with Claude Code
