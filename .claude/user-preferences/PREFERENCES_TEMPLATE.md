# User Preferences Template

**Instructions:** Copy this template to create your own preferences file (e.g., `[your-name]-preferences.md`). All agents will automatically read and apply these preferences on every invocation.

---

## 💬 Communication Preferences

### Style
- **Verbosity:** [Concise and direct / Detailed explanations / Technical depth]
- **Emoji usage:** [No emojis unless requested / Use emojis / Occasional emojis]
- **Status reporting:** [Status-first (✅/⚠️/❌) / Narrative style / Bullet points]
- **Blocker communication:** [Blocker FIRST / End with blockers / Standard format]

### Format
- **Response length:** [Under 10 lines / Moderate / Detailed as needed]
- **Technical jargon:** [Avoid / Use freely / Explain when used]
- **Examples:** [Always provide / Only when asked / Case-by-case]

### Questions & Clarification
- **When to ask questions:** [Always clarify ambiguity / Proceed with best judgment / Ask only critical questions]
- **Decision-making:** [Ask for approval / Autonomous for safe operations / Always autonomous]

---

## 🤖 Agent Behavior Expectations

### Role Boundaries
- **Stay in lane:** [Strict boundaries / Flexible when urgent / Allow cross-role work]
- **Delegation protocol:** [Always ask before invoking / Auto-invoke related agents / Let me invoke]
- **Takeovers:** [Never take over / Only for urgent fixes / Ask first]

### Invocation Style
- **Permission mode:** [Always ask / Auto-accept for safe tools / Auto-deny risky tools]
- **Agent handoffs:** [Explicit mentions required / Implicit handoffs OK / I'll manage]
- **Parallel agents:** [Encourage concurrent work / Sequential preferred / Ask first]

### Autonomy Level
- **Safe operations:** [Fully autonomous / Ask first / Notify after]
- **Risky operations:** [Always ask / Proceed if confident / I'll approve separately]
- **Git commits:** [Only when requested / Auto-commit safe changes / After my review]

---

## 🛠️ Technical Preferences

### Code Quality
- **Security:** [Security-first (OWASP top 10) / Standard practices / Basic validation]
- **Over-engineering:** [Avoid / Allow for scalability / Balance complexity]
- **Code simplicity:** [Minimum viable / Moderate / Plan for future]
- **Error handling:** [At boundaries only / Comprehensive / Standard try-catch]

### Development Practices
- **Testing:** [TDD / Test after implementation / Manual testing focus]
- **Documentation:** [Only when needed / Comprehensive / Inline comments]
- **Type safety:** [Strict TypeScript / Lenient / JavaScript preferred]
- **Code style:** [Follow existing patterns / Establish new standards / Use linter only]

### Technology Choices
- **Trust level:** [Trust internal code / Validate everything / Case-by-case]
- **Dependencies:** [Minimize / Use established libraries / Prefer custom solutions]
- **Frameworks:** [Use project standards / Suggest alternatives / I'll decide]

---

## 📋 Workflow Preferences

### Task Management
- **TodoWrite usage:** [Always for multi-step / Only for complex tasks / Rarely needed]
- **Task granularity:** [Fine-grained steps / High-level milestones / Mixed approach]
- **Completion marking:** [Immediately after done / Batch updates / End of session]

### Progress Tracking
- **Agent Communication Board:** [Update after every task / Daily summary / Major milestones only]
- **Memory updates:** [After every task / Weekly / Major work only]
- **Status format:** [✅/⚠️/❌ emoji system / Text-based / Numeric scoring]

### Git Workflow
- **Commit frequency:** [Small atomic commits / Feature-based / End of work session]
- **Commit messages:** [Conventional commits / Descriptive / Brief]
- **Branch strategy:** [Feature branches / Direct to main / Release branches]

---

## 🎨 Design & UI Preferences

### Frontend Development
- **Plugin usage:** [Always use frontend-design for new UI / Manual coding OK / Ask first]
- **Component approach:** [Reusable components / Single-use OK / Balance reusability]
- **Styling:** [Tailwind utility-first / CSS modules / Styled components]

### Design Philosophy
- **Aesthetics priority:** [Function over form / Equal balance / Form over function]
- **Design patterns:** [Avoid generic AI patterns / Standard patterns OK / Custom always]
- **Animation:** [Minimal / Moderate / Rich interactions]

### Accessibility
- **WCAG level:** [AA required / AAA target / Basic compliance]
- **Testing:** [Automated tools / Manual testing / User testing]

---

## 🧪 Testing & Quality Standards

### Test Coverage
- **Coverage target:** [>80% / >60% / Focus on critical paths]
- **Test types:** [Unit + Integration + E2E / Unit focus / E2E focus]
- **Test framework:** [Playwright / Jest / Mixed]

### Quality Gates
- **Pre-deployment:** [All tests pass / Critical tests only / Manual verification]
- **Code review:** [Always required / Pair programming / Post-commit review]
- **Performance:** [Core Web Vitals required / Best effort / Not critical]

### What Matters vs What Doesn't
- **Critical:** [Security, correctness, performance / Functionality, tests / User experience]
- **Nice to have:** [Perfect coverage, documentation / Optimization / Aesthetics]
- **Don't care:** [Comment style, naming / Code organization / Tooling choices]

---

## 🚨 When Things Go Wrong

### Blocker Handling
- **Reporting:** [Immediate notification / Status update / File issue]
- **Unblocking:** [Proactive action / Wait for instructions / Escalate]
- **Impact assessment:** [Always include / For major blockers / When asked]

### Debugging Approach
- **Investigation depth:** [Root cause analysis / Quick fix / Balance based on severity]
- **Logs:** [Comprehensive logging / Standard logging / Minimal]
- **Rollback:** [Immediate on failure / Investigate first / Ask before rollback]

### Error Recovery
- **Retry strategy:** [Auto-retry safe operations / Always ask / Never retry]
- **Fallbacks:** [Implement fallbacks / Fail fast / Case-by-case]
- **User notification:** [Immediate / End of session / Only critical]

---

## 🚀 Deployment Preferences

### Deployment Strategy
- **Frequency:** [Continuous / Daily / Weekly batches]
- **Environments:** [dev → staging → production / Direct to production / Custom flow]
- **Approval:** [Auto-deploy to staging / Manual approval for all / I'll trigger]

### Monitoring
- **Post-deployment:** [10+ minute monitoring / Quick check / Automated alerts]
- **Health checks:** [Comprehensive / Basic endpoints / Manual verification]
- **Rollback trigger:** [Any error / Critical errors only / After investigation]

---

## 🔧 Project-Specific Customizations

### [Project Name 1]
- **Special rules:** [Add project-specific preferences here]
- **Exceptions:** [List any exceptions to global preferences]
- **Key contacts:** [Stakeholders, reviewers, etc.]

### [Project Name 2]
- **Special rules:** [Add project-specific preferences here]
- **Exceptions:** [List any exceptions to global preferences]
- **Key contacts:** [Stakeholders, reviewers, etc.]

---

## 📝 How to Use This Template

1. **Copy this file** to `[your-name]-preferences.md` in `.claude/user-preferences/`
2. **Fill in your preferences** for each section (delete bracketed options, keep your choice)
3. **Add/remove sections** as needed for your workflow
4. **Commit to git** so preferences transfer across projects
5. **Update regularly** as you learn what works best for you

**Example:**
```markdown
### Style
- **Verbosity:** Concise and direct
- **Emoji usage:** No emojis unless requested
- **Status reporting:** Status-first (✅/⚠️/❌)
```

---

## 🎯 Quick Preference Examples

### Example 1: Speed-Focused Developer
- Concise communication, no emojis
- Auto-accept safe tools, ask for risky ones
- Security-first, no over-engineering
- Continuous deployment to staging
- 10-minute post-deployment monitoring

### Example 2: Quality-Focused Developer
- Detailed explanations with examples
- Always ask before any tool use
- Comprehensive testing (>80% coverage)
- Manual approval for all deployments
- Root cause analysis for all issues

### Example 3: Balanced Approach
- Moderate verbosity, status-first
- Auto-accept for safe operations
- Security + simplicity focus
- Deploy to staging auto, production manual
- Quick checks + automated alerts

---

**Version:** 1.0.0
**Last Updated:** 2025-11-23
**Created By:** @memory-expert
**Maintained By:** Project team
