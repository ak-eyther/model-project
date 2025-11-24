# Plugin Mapping Guide

**Last Updated:** 2025-11-24
**Purpose:** Map 80+ globally installed plugins to 15 specialized agents

---

## 🎯 Quick Reference Table

| Agent | Primary Plugins | Skills Auto-Loaded | Permission Mode |
|-------|----------------|-------------------|-----------------|
| @atharva-2.0 | feature-dev, full-stack-orchestration | explanatory-output-style | auto-accept |
| @anand-2.0 | ralph-wiggum, frontend-design, developer-essentials | learning-output-style | auto-accept |
| @sama-2.0 | ai-ml, llm-application-dev, machine-learning-ops | example-skills:mcp-builder | auto-accept |
| @shawar-2.0 | deployment-strategies, cicd-automation, kubernetes-operations | deployment-validation | auto-accept |
| @harshit-2.0 | testing, performance-testing-review, tdd-workflows | webapp-testing | auto-accept |
| @ankur-2.0 | code-review, security-scanning, comprehensive-review | code-review:code-reviewer | auto-accept |
| @vidya-2.0 | cloud-infrastructure, database-design, systems-programming | explanatory-output-style | auto-accept |
| @hitesh-2.0 | frontend-design, frontend-mobile-development | ralph-wiggum | auto-accept |
| @varsha-2.0 | accessibility-compliance, frontend-design (read-only) | canvas-design, theme-factory | auto-deny |
| @debugger | error-debugging, distributed-debugging, debugging-toolkit | error-detective | auto-accept |
| @bug-fix-orchestrator | error-diagnostics, incident-response | error-debugging:debugger | auto-accept |
| @memory-expert | context-management, documentation-generation | skill-enhancers | auto-accept |
| @reflection-expert | code-refactoring, performance | comprehensive-review | auto-accept |
| @documentation-manager | code-documentation, documentation-generation | example-skills:internal-comms | auto-accept |

---

## 📦 Detailed Plugin Assignments

### @atharva-2.0 (Feature Orchestrator)

**Core Plugins:**
- `feature-dev` - Feature development workflows (DPPM framework support)
- `full-stack-orchestration` - Multi-agent coordination
- `agent-orchestration` - Agent task delegation
- `explanatory-output-style` - Educational explanations during planning

**Supporting Plugins:**
- `context-management` - Large feature context tracking
- `team-collaboration` - Multi-agent handoffs

**Skills to Add:**
```yaml
skills:
  - feature-dev:feature-dev
  - explanatory-output-style
  - agent-orchestration
```

---

### @anand-2.0 (Code Executor)

**Core Plugins:**
- `ralph-wiggum` - Iterative code refinement (MANDATORY)
- `frontend-design` - Production-grade frontend code generation (MANDATORY for UI work)
- `developer-essentials` - Code execution utilities
- `learning-output-style` - Learn from each implementation

**Supporting Plugins:**
- `backend-development` - FastAPI/Python backend
- `python-development` - Python-specific tools
- `javascript-typescript` - JS/TS development
- `code-refactoring` - Clean code patterns

**Skills to Add:**
```yaml
skills:
  - frontend-design:frontend-design
  - learning-output-style
  - ralph-wiggum
```

**CRITICAL:** MUST use `frontend-design` plugin for ALL new UI/frontend work (not manual coding).

---

### @sama-2.0 (AI/ML Engineer)

**Core Plugins:**
- `ai-ml` - AI/ML engineering workflows
- `llm-application-dev` - LLM application development
- `machine-learning-ops` - MLOps pipelines
- `ai-agency` - AI agent architecture

**Supporting Plugins:**
- `data-engineering` - Data pipeline optimization
- `api-development` - AI service APIs
- `performance` - Model performance optimization

**Skills to Add:**
```yaml
skills:
  - ai-ml
  - llm-application-dev
  - example-skills:mcp-builder
```

---

### @shawar-2.0 (Deployment Expert)

**Core Plugins:**
- `deployment-strategies` - Multi-environment deployment (Vercel, Railway)
- `cicd-automation` - CI/CD pipelines (GitHub Actions, Railway CLI)
- `deployment-validation` - Health checks, rollback automation
- `kubernetes-operations` - K8s deployments (if needed)

**Supporting Plugins:**
- `cloud-infrastructure` - Cloud resource management
- `observability-monitoring` - Deployment monitoring
- `devops` - DevOps best practices

**Skills to Add:**
```yaml
skills:
  - deployment-strategies
  - cicd-automation
  - deployment-validation
```

---

### @harshit-2.0 (Test Executor)

**Core Plugins:**
- `testing` - Test execution framework
- `performance-testing-review` - Performance profiling
- `tdd-workflows` - Test-driven development
- `unit-testing` - Unit test execution

**Supporting Plugins:**
- `error-debugging` - Test failure debugging
- `application-performance` - Performance analysis
- `accessibility-compliance` - WCAG testing

**Skills to Add:**
```yaml
skills:
  - example-skills:webapp-testing
  - testing
  - performance-testing-review
```

**CRITICAL:** Harshit executes tests, does NOT give quality verdicts (that's @ankur-2.0).

---

### @ankur-2.0 (Quality Gatekeeper)

**Core Plugins:**
- `code-review` - Static code review (ESLint, TypeScript)
- `security-scanning` - Vulnerability scanning (npm audit)
- `comprehensive-review` - Multi-dimensional code quality
- `security-compliance` - Security best practices

**Supporting Plugins:**
- `backend-api-security` - API security validation
- `frontend-mobile-security` - Frontend security
- `codebase-cleanup` - Code quality improvements

**Skills to Add:**
```yaml
skills:
  - code-review:code-reviewer
  - security-scanning
  - comprehensive-review
```

**CRITICAL:** Ankur reviews code statically, delegates test execution to @harshit-2.0.

---

### @vidya-2.0 (Solution Architect)

**Core Plugins:**
- `cloud-infrastructure` - Cloud architecture design
- `database-design` - Database architecture
- `systems-programming` - System design patterns
- `database-cloud-optimization` - Scalability planning

**Supporting Plugins:**
- `distributed-debugging` - Distributed systems design
- `api-development` - API architecture
- `framework-migration` - Migration strategies

**Skills to Add:**
```yaml
skills:
  - explanatory-output-style
  - cloud-infrastructure
  - database-design
```

---

### @hitesh-2.0 (Frontend Specialist)

**Core Plugins:**
- `frontend-design` - Production-grade React components (MANDATORY)
- `frontend-mobile-development` - React Native, mobile-first design
- `ralph-wiggum` - Iterative frontend refinement

**Supporting Plugins:**
- `accessibility-compliance` - WCAG compliance
- `javascript-typescript` - Modern JS/TS patterns
- `performance` - Frontend performance optimization

**Skills to Add:**
```yaml
skills:
  - frontend-design:frontend-design
  - ralph-wiggum
  - accessibility-compliance
```

**CRITICAL:** MUST use `frontend-design` plugin for ALL new component work (not manual coding).

---

### @varsha-2.0 (UI/UX Designer)

**Core Plugins:**
- `accessibility-compliance` - WCAG 2.1 AA compliance
- `frontend-design` - **READ-ONLY** design exploration (NOT implementation)

**Supporting Plugins:**
- `seo-technical-optimization` - SEO-friendly design
- `content-marketing` - Content design guidance

**Skills to Add:**
```yaml
skills:
  - frontend-design:frontend-design  # READ-ONLY exploration
  - example-skills:canvas-design
  - example-skills:theme-factory
  - accessibility-compliance:wcag-compliance
```

**CRITICAL:** Varsha explores designs with `frontend-design` but CANNOT implement (delegates to @hitesh-2.0/@anand-2.0).

---

### @debugger (Bug Investigator)

**Core Plugins:**
- `error-debugging` - Root cause analysis
- `distributed-debugging` - Distributed system debugging
- `debugging-toolkit` - Debugging utilities
- `incident-response` - Production incident handling

**Supporting Plugins:**
- `error-diagnostics` - Error pattern analysis
- `observability-monitoring` - Logging/tracing analysis

**Skills to Add:**
```yaml
skills:
  - error-debugging:error-detective
  - error-debugging:debugger
  - distributed-debugging
```

---

### @bug-fix-orchestrator (Bug Fix Coordinator)

**Core Plugins:**
- `error-diagnostics` - Bug diagnosis workflows
- `incident-response` - Incident management
- `git-pr-workflows` - Bug fix PR automation

**Supporting Plugins:**
- `testing` - Regression test coordination
- `deployment-strategies` - Hotfix deployment

**Skills to Add:**
```yaml
skills:
  - error-debugging:debugger
  - incident-response
  - git-pr-workflows
```

---

### @memory-expert (Memory Manager)

**Core Plugins:**
- `context-management` - ChromaDB memory management
- `documentation-generation` - Memory documentation
- `skill-enhancers` - Meta-learning from experiences

**Supporting Plugins:**
- `code-documentation` - Experience documentation

**Skills to Add:**
```yaml
skills:
  - context-management
  - skill-enhancers
```

---

### @reflection-expert (Meta-Reflection)

**Core Plugins:**
- `comprehensive-review` - Agent quality reflection
- `code-refactoring` - Workflow optimization
- `performance` - Efficiency analysis

**Supporting Plugins:**
- `productivity` - Workflow improvement

**Skills to Add:**
```yaml
skills:
  - comprehensive-review
  - performance
```

---

### @documentation-manager (Documentation Lifecycle)

**Core Plugins:**
- `code-documentation` - Auto-documentation generation
- `documentation-generation` - Doc creation/updates
- `content-marketing` - User-facing docs

**Supporting Plugins:**
- `seo-content-creation` - SEO-optimized docs

**Skills to Add:**
```yaml
skills:
  - example-skills:internal-comms
  - code-documentation
  - documentation-generation
```

---

## 🔧 How to Apply Plugin Mappings

### Option 1: Update Agent Definitions

Edit each agent's `.claude/agents/[agent-name].md` file to add `skills:` section:

```yaml
---
agent_name: "Anand 2.0"
skills:
  - frontend-design:frontend-design
  - learning-output-style
  - ralph-wiggum
---
```

### Option 2: Update Project Settings

Add to `.claude/settings.json`:

```json
{
  "agents": {
    "anand-2.0": {
      "skills": ["frontend-design:frontend-design", "learning-output-style", "ralph-wiggum"]
    },
    "harshit-2.0": {
      "skills": ["example-skills:webapp-testing", "testing", "performance-testing-review"]
    }
  }
}
```

---

## 🚨 Critical Enforcement Rules

### Rule 1: Frontend Design Plugin Usage

**Agents ALLOWED to implement with frontend-design:**
- ✅ @anand-2.0 (full-stack executor)
- ✅ @hitesh-2.0 (frontend specialist)

**Agent with READ-ONLY access:**
- ✅ @varsha-2.0 (design exploration only, NOT implementation)

**Violation Detection:**
If @varsha-2.0 says "Let me implement this component with frontend-design..." → STOP! Violation!

### Rule 2: Test Execution vs Quality Review

**Test EXECUTION (Harshit):**
- Plugins: `testing`, `performance-testing-review`, `webapp-testing`
- Output: "8/8 tests passed ✅" (factual results)

**Quality REVIEW (Ankur):**
- Plugins: `code-review`, `security-scanning`, `comprehensive-review`
- Output: "APPROVE (Risk: 15/100)" (verdict with reasoning)

**Violation Detection:**
If @harshit-2.0 says "I reviewed the code and found security issues..." → STOP! That's @ankur-2.0's job!

### Rule 3: Deployment Exclusivity

**Only @shawar-2.0 can deploy:**
- Plugins: `deployment-strategies`, `cicd-automation`, `deployment-validation`
- No other agent should use these plugins

**Violation Detection:**
If @anand-2.0 says "Let me deploy this to Vercel..." → STOP! Delegate to @shawar-2.0!

---

## 📊 Plugin Coverage Analysis

**Total Plugins Available:** 80+

**Plugins Mapped to Agents:** 45 (56% coverage)

**High-Value Plugins Not Yet Mapped:**
- `api-testing-observability` - Could be added to @harshit-2.0
- `dependency-management` - Could be added to @ankur-2.0
- `database-migrations` - Could be added to @vidya-2.0
- `security-guidance` - Could be added to @ankur-2.0
- `observability-monitoring` - Could be added to @shawar-2.0

**Specialized Domains Not Yet Covered:**
- `blockchain-web3` - Need new agent if blockchain work needed
- `game-development` - Need new agent if game dev needed
- `quantitative-trading` - Need new agent if fintech/trading needed

---

## 🎯 Next Steps

1. **Update Agent Definitions:**
   - Add `skills:` section to each agent's `.md` file
   - Use recommended plugins from this mapping

2. **Test Plugin Loading:**
   - Restart Claude Code after updating agent definitions
   - Verify plugins load correctly for each agent

3. **Monitor Plugin Usage:**
   - Track which plugins are actually used
   - Remove unused plugins to reduce token overhead

4. **Expand Coverage:**
   - Map remaining 35+ plugins as needed
   - Create new agents for specialized domains (blockchain, game dev, etc.)

---

## 📚 References

- **Global Plugins Directory:** `~/.claude/plugins/marketplaces/`
- **Agent Definitions:** `.claude/agents/*.md`
- **Project Settings:** `.claude/settings.json`
- **Plugin Documentation:** Each plugin's `README.md` in its directory

---

**Document Version:** 1.0
**Maintainer:** @documentation-manager
**Last Review:** 2025-11-24
