# Tier Comparison: Which Tier Should I Choose?

Not all projects need the same infrastructure. Choose the tier that best fits your project size, team, and timeline.

---

## 🎯 Quick Decision Tree

**Answer these questions:**

1. **Is this a prototype or proof-of-concept?**
   - Yes → **MINIMAL**
   - No → Continue

2. **Is this going to production with a team?**
   - Yes → **STANDARD** (recommended)
   - No → Continue

3. **Is this mission-critical with strict quality requirements?**
   - Yes → **COMPLETE**
   - No → **STANDARD** (safe default)

---

## 📊 Feature Comparison

| Feature | Minimal | Standard | Complete |
|---------|---------|----------|----------|
| **Setup Time** | 30 minutes | 2 hours | 1 day |
| **Core Agents** | 5 | 15 | 15 |
| **Orchestrators** | 1 (Atharva) | 2 | 2 |
| **Executors** | 1 (Anand) | 3 | 3 |
| **Validators** | 2 (Ankur, Debugger) | 2 | 2 |
| **Domain Experts** | 0 | 7 | 7 |
| **Support Agents** | 1 (Memory Expert) | 3 | 3 |
| | | | |
| **Structure Enforcement** | Basic | Full | Full |
| **Auto-Fix** | ❌ | ✅ | ✅ |
| **Memory System** | ❌ | Tri-tier | Tri-tier |
| **Git Hooks** | Pre-commit only | All 3 | All 3 |
| **Reflection System** | ❌ | ❌ | ✅ |
| **Automated Cleanup** | ❌ | ❌ | ✅ (cron) |
| | | | |
| **Documentation Architecture** | Basic | Full | Full |
| **Lifecycle Rules** | ❌ | ✅ | ✅ |
| **Agent Memory** | ❌ | ✅ | ✅ |
| **Quality Gates** | Basic | Tier 2 | Tier 1 + Tier 2 |
| | | | |
| **Best For** | Prototypes, learning | Production projects | Mission-critical |
| **Team Size** | 1-2 | 2-10 | 5+ |
| **Project Duration** | < 1 month | 1-6 months | 6+ months |
| **Quality Requirements** | Medium | High | Very High |

---

## 🔍 Tier Details

### ⚡ MINIMAL Tier

**Who is this for?**
- Solo developers learning the system
- Prototypes and proofs-of-concept
- Projects with < 1 month timeline
- Exploratory work

**What you get:**
- **5 Core Agents:**
  - `@atharva-2.0` - Feature orchestrator
  - `@anand-2.0` - Full-stack executor
  - `@ankur-2.0` - Quality gatekeeper
  - `@debugger` - Bug investigation
  - `@memory-expert` - Memory management

- **Basic Structure Validation:**
  - Pre-commit hook validates file placement
  - Manual `python .claude/scripts/structure_validator.py` for deeper checks

- **No Memory System:**
  - Agents don't remember past work
  - Fresh start every time

**Limitations:**
- No specialized agents (frontend, deployment, AI/ML, etc.)
- No automatic file archival
- No agent learning/improvement over time
- Manual structure fixes required

**Upgrade Path:**
```bash
python setup.py --upgrade-to=standard
```

---

### ⭐ STANDARD Tier (RECOMMENDED)

**Who is this for?**
- Production projects
- Teams of 2-10 developers
- Projects lasting 1-6 months
- High-quality requirements

**What you get:**
- **All 15 Agents:**
  - Full orchestration (Atharva, Bug-Fix Orchestrator)
  - Specialized executors (Anand, Hitesh, SAMA)
  - Domain experts (Shawar, Vidya, Varsha)
  - Support (Memory, Reflection, Documentation)

- **Full Structure Enforcement:**
  - Pre-commit hook blocks invalid commits
  - Auto-fix repairs violations automatically
  - Commit-msg hook enforces task IDs
  - Post-merge hook reminds to validate

- **Tri-Tier Memory System:**
  - Agents remember past 20 events (hot memory)
  - Pattern recognition on events 21-100 (warm memory)
  - Long-term learnings from 101+ (cold memory)
  - Weekly consolidation, monthly archival

- **Documentation Architecture:**
  - Active docs in `.claude/docs/`
  - Lifecycle rules auto-archive old files
  - Completion reports preserved 7 days
  - Impact analyses retained 30 days

**Limitations:**
- No silent self-reflection (agents submit without self-assessment)
- No automated nightly cleanup (manual `cleanup-manager.py`)
- No advanced monitoring

**Upgrade Path:**
```bash
python setup.py --upgrade-to=complete
```

---

### 🚀 COMPLETE Tier

**Who is this for?**
- Mission-critical production systems
- Large teams (5+ developers)
- Long-term projects (6+ months)
- Strict quality/compliance requirements

**What you get (everything in Standard +):**

- **Silent Reflection System:**
  - Agents self-assess before submission (Tier 1 quality gate)
  - Self-score on completeness, quality, role adherence (minimum 8/10)
  - Automatic retry if score < 8 (max 2 retries)
  - Escalate to Tier 2 (Ankur) only when confident
  - **Result:** 50% reduction in validator rejections

- **Automated Cleanup (Cron Jobs):**
  - Nightly archival of old files
  - Weekly memory consolidation
  - Monthly cold archival
  - Automatic removal of stale branches
  - **Result:** Zero-maintenance file organization

- **Advanced Monitoring:**
  - Track agent performance over time
  - Identify bottlenecks in delegation chain
  - Alert on quality degradation
  - Audit trail for compliance

**Complexity:**
- Requires cron job setup (automated by wizard)
- More moving parts to understand
- Higher initial learning curve

---

## 💰 Cost Comparison

| Tier | Setup Cost | Maintenance Cost | Value |
|------|------------|------------------|-------|
| **Minimal** | 30 min | Medium (manual fixes) | Good for learning |
| **Standard** | 2 hours | Low (mostly automated) | ⭐ Best value |
| **Complete** | 1 day | Very Low (fully automated) | High for large projects |

**Recommendation:** Start with **STANDARD**. It gives you 95% of the value with minimal overhead.

---

## 🔄 Upgrade Strategy

**You can upgrade anytime:**

```bash
# Minimal → Standard
python setup.py --upgrade-to=standard

# Standard → Complete
python setup.py --upgrade-to=complete
```

**What happens during upgrade:**
- New agents added
- New features enabled
- Existing configuration preserved
- No data loss

**Downgrade:**
Not officially supported, but you can:
1. Disable features in `.claude/config/project-config.yaml`
2. Remove unused agent files
3. Disable git hooks: `rm .git/hooks/pre-commit`

---

## 🎓 Real-World Examples

### Minimal: Weekend Hackathon Project
**Scenario:** Building a quick prototype to demo on Monday

**Why Minimal:**
- Only 2 days to build
- Solo developer
- Don't need memory (fresh start is fine)
- Basic structure validation prevents chaos

**Outcome:** Clean code, organized files, ready to present

---

### Standard: SaaS Startup MVP
**Scenario:** 3-person team building first production release

**Why Standard:**
- 3-month timeline to launch
- Need all specialists (frontend, backend, deployment)
- Memory system helps team avoid repeating mistakes
- Structure enforcement keeps codebase clean as it grows

**Outcome:** Production-ready, scalable, documented

---

### Complete: Enterprise Healthcare App
**Scenario:** 10-person team building HIPAA-compliant system

**Why Complete:**
- 12-month timeline
- Strict quality/compliance requirements
- Silent reflection reduces rework (saves weeks)
- Automated cleanup ensures audit trail
- Large team needs strong coordination

**Outcome:** Passes compliance audits, minimal technical debt

---

## ❓ FAQ

**Q: Can I customize a tier?**
A: Yes! Edit `.claude/config/project-config.yaml` to enable/disable features.

**Q: What if I'm between Standard and Complete?**
A: Choose Standard, manually run reflection when needed.

**Q: Can I add custom agents later?**
A: Yes! Copy an existing agent file as template, customize, validate with `.claude/scripts/validate-agent-skills.sh`.

**Q: Does tier affect agent quality?**
A: No. Agent quality is the same across all tiers. Complete tier adds self-reflection to catch issues earlier.

**Q: How much disk space do they use?**
- Minimal: ~5 MB (agents + docs)
- Standard: ~10 MB (+ memory files)
- Complete: ~15 MB (+ reflection logs)

---

## 🎯 Final Recommendation

**90% of projects should use STANDARD tier.**

It gives you:
- Full agent orchestration
- Automated quality gates
- Memory system (agents learn)
- Structure enforcement (zero-maintenance)
- Upgrade path to Complete when needed

**Only choose Minimal if:**
- You're learning the system
- Building a throwaway prototype
- Need setup in < 30 minutes

**Only choose Complete if:**
- Team of 5+ developers
- Mission-critical system
- Compliance requirements
- Long-term project (6+ months)

---

**Ready to set up?**
```bash
python setup.py
```
