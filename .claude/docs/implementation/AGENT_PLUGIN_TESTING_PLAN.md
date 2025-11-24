# Agent Plugin Testing Plan

**Created:** 2025-11-24
**Purpose:** Validate that all 14 agents can access and use their newly added P0 global plugins

---

## Testing Strategy

### Phase 1: Plugin Availability Validation
**Goal:** Verify all P0 plugins are installed globally and accessible

**Method:**
1. Run validation script: `.claude/scripts/validate-plugins.sh`
2. Check global plugin directory for each P0 plugin
3. Verify no missing dependencies

**Expected Result:** All P0 plugins show ✓ (available)

---

### Phase 2: Agent-by-Agent Testing
**Goal:** Verify each agent can invoke their P0 plugins via skills

**Method:** Invoke each agent with a task that requires their P0 plugin

---

## Agent Test Cases

### 1. @anand-2.0 (Full-Stack Executor)
**P0 Plugins:** code-review, security-scanning, backend-development, api-development, database, database-migrations

**Test Case:**
```
Task: Create a simple FastAPI endpoint with database integration
Expected: Agent uses backend-development and api-development plugins
Success Criteria: Agent references plugin patterns in implementation
```

**Invocation:**
```bash
@anand-2.0 Create a simple /health endpoint in FastAPI that checks database connectivity
```

---

### 2. @atharva-2.0 (Feature Orchestrator)
**P0 Plugins:** agent-orchestration, full-stack-orchestration, documentation-generation, code-documentation

**Test Case:**
```
Task: Plan a simple feature requiring agent coordination
Expected: Agent uses agent-orchestration and full-stack-orchestration
Success Criteria: Agent delegates to correct agents and documents plan
```

**Invocation:**
```bash
@atharva-2.0 Plan a feature to add a /status endpoint that returns app health
```

---

### 3. @sama-2.0 (AI/ML Engineer)
**P0 Plugins:** llm-application-dev, mcp, machine-learning-ops, data-engineering

**Test Case:**
```
Task: Design a simple LLM integration pattern
Expected: Agent uses llm-application-dev plugin
Success Criteria: Agent references LLM best practices and patterns
```

**Invocation:**
```bash
@sama-2.0 Design a simple Claude API integration for text summarization
```

---

### 4. @shawar-2.0 (Deployment Expert)
**P0 Plugins:** cicd-automation, deployment-strategies, deployment-validation, cloud-infrastructure, kubernetes-operations

**Test Case:**
```
Task: Explain deployment strategy for staging environment
Expected: Agent uses deployment-strategies plugin
Success Criteria: Agent references deployment best practices
```

**Invocation:**
```bash
@shawar-2.0 Explain the current deployment strategy for staging environment
```

---

### 5. @harshit-2.0 (Test Executor)
**P0 Plugins:** testing, tdd-workflows, unit-testing, performance-testing-review, application-performance

**Test Case:**
```
Task: Create a test plan for /health endpoint
Expected: Agent uses testing and unit-testing plugins
Success Criteria: Agent references testing patterns and frameworks
```

**Invocation:**
```bash
@harshit-2.0 Create a test plan for a /health endpoint
```

---

### 6. @ankur-2.0 (Quality Gatekeeper)
**P0 Plugins:** security-scanning, security-compliance, backend-api-security, code-refactoring, codebase-cleanup

**Test Case:**
```
Task: Review security of a sample endpoint
Expected: Agent uses security-scanning and backend-api-security
Success Criteria: Agent references OWASP Top 10, security best practices
```

**Invocation:**
```bash
@ankur-2.0 Review security best practices for a /health endpoint
```

---

### 7. @vidya-2.0 (Solution Architect)
**P0 Plugins:** cloud-infrastructure, backend-development, api-development

**Test Case:**
```
Task: Design architecture for a simple API
Expected: Agent uses cloud-infrastructure and api-development
Success Criteria: Agent references architecture patterns and best practices
```

**Invocation:**
```bash
@vidya-2.0 Design architecture for a simple health check API
```

---

### 8. @hitesh-2.0 (Frontend Specialist)
**P0 Plugins:** javascript-typescript, framework-migration, accessibility-compliance, frontend-mobile-security

**Test Case:**
```
Task: Create a React component with accessibility
Expected: Agent uses accessibility-compliance plugin
Success Criteria: Agent references WCAG guidelines, ARIA labels
```

**Invocation:**
```bash
@hitesh-2.0 Design a simple React button component with full accessibility support
```

---

### 9. @varsha-2.0 (UI/UX Designer)
**P0 Plugins:** accessibility-compliance, code-documentation

**Test Case:**
```
Task: Create design spec with accessibility requirements
Expected: Agent uses accessibility-compliance plugin
Success Criteria: Agent references WCAG 2.1 AA standards
```

**Invocation:**
```bash
@varsha-2.0 Create design spec for an accessible button component
```

---

### 10. @debugger (Bug Investigation)
**P0 Plugins:** error-debugging, debugging-toolkit, observability-monitoring

**Test Case:**
```
Task: Investigate a hypothetical timeout error
Expected: Agent uses error-debugging plugin
Success Criteria: Agent references debugging strategies and tools
```

**Invocation:**
```bash
@debugger Investigate a hypothetical API timeout error (30s timeout)
```

---

### 11. @bug-fix-orchestrator (Bug Fix Manager)
**P0 Plugins:** error-debugging, git-pr-workflows

**Test Case:**
```
Task: Plan a hotfix workflow
Expected: Agent uses git-pr-workflows plugin
Success Criteria: Agent references git branching strategies
```

**Invocation:**
```bash
@bug-fix-orchestrator Plan a hotfix workflow for a critical production bug
```

---

### 12. @memory-expert (Memory Management)
**P0 Plugins:** code-documentation

**Test Case:**
```
Task: Query for documentation patterns
Expected: Agent uses code-documentation plugin
Success Criteria: Agent references documentation best practices
```

**Invocation:**
```bash
@memory-expert Query experiences similar to: documenting API endpoints
```

---

### 13. @reflection-expert (Quality Validation)
**P0 Plugins:** code-review, security-scanning

**Test Case:**
```
Task: Review a simple code snippet
Expected: Agent uses code-review plugin
Success Criteria: Agent references code quality standards
```

**Invocation:**
```bash
@reflection-expert Review best practices for a /health endpoint implementation
```

---

### 14. @documentation-manager (Documentation Lifecycle)
**P0 Plugins:** seo-content-creation

**Test Case:**
```
Task: Plan documentation structure
Expected: Agent uses documentation patterns
Success Criteria: Agent references documentation organization
```

**Invocation:**
```bash
@documentation-manager Explain the current project documentation structure
```

---

## Testing Execution Plan

### Option 1: Quick Smoke Test (15-20 minutes)
- Test 3-4 critical agents (@anand-2.0, @atharva-2.0, @sama-2.0, @shawar-2.0)
- Verify they can access and reference P0 plugins
- If successful, assume others work similarly

### Option 2: Comprehensive Test (45-60 minutes)
- Test all 14 agents systematically
- Document each agent's response
- Create test results report
- Fix any issues found

### Option 3: Validation Script Only (5 minutes)
- Run `.claude/scripts/validate-plugins.sh`
- Verify all P0 plugins are installed globally
- Skip agent invocation testing

---

## Success Criteria

### Minimum (Option 1 or 3)
- ✅ All P0 plugins show as available in validation script
- ✅ 3-4 sample agents successfully invoke their plugins

### Complete (Option 2)
- ✅ All 14 agents successfully invoke their P0 plugins
- ✅ Agents reference plugin patterns in responses
- ✅ No missing plugin errors
- ✅ Test results documented

---

## Which option would you prefer?

**Recommendation:** Start with **Option 3** (validation script) to confirm plugins are installed, then **Option 1** (quick smoke test) with 3-4 agents to verify functionality.

---

**Next Steps:**
1. Run validation script: `.claude/scripts/validate-plugins.sh`
2. If validation passes → Run quick smoke test with 3-4 agents
3. If issues found → Fix and re-test
4. Document results
