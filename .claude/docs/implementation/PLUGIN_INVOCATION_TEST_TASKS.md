# Plugin Invocation Test Tasks

**Purpose:** Test tasks that REQUIRE agents to use their P0 plugins

---

## Test Strategy

Each task is designed to be **impossible to complete correctly** without accessing the P0 plugin knowledge:
- Ask for plugin-specific patterns
- Request framework-specific best practices
- Require security compliance standards
- Need deployment automation patterns

---

## Agent Test Tasks

### 1. @varsha-2.0 (UI/UX Designer)
**P0 Plugins:** accessibility-compliance, code-documentation

**Test Task:**
```
@varsha-2.0 Create a design spec for an accessible file upload button that meets WCAG 2.1 AA standards.

Required:
- Specific ARIA labels needed
- Minimum color contrast ratios
- Keyboard navigation requirements
- Screen reader announcements

This should require your accessibility-compliance plugin.
```

**Expected Evidence:** References to WCAG 2.1 AA, specific contrast ratios (4.5:1 for text), ARIA attributes

---

### 2. @hitesh-2.0 (Frontend Specialist)
**P0 Plugins:** javascript-typescript, framework-migration, accessibility-compliance, frontend-mobile-security

**Test Task:**
```
@hitesh-2.0 What are the modern React 18+ patterns for migrating from class components to functional components with hooks?

Required:
- Lifecycle method equivalents
- State management migration patterns
- Performance optimization with hooks

This should require your framework-migration plugin.
```

**Expected Evidence:** Specific React 18+ patterns, useEffect dependency arrays, custom hooks patterns

---

### 3. @sama-2.0 (AI/ML Engineer)
**P0 Plugins:** llm-application-dev, mcp, machine-learning-ops, data-engineering

**Test Task:**
```
@sama-2.0 What are the best practices for implementing RAG (Retrieval-Augmented Generation) with Claude API?

Required:
- Chunking strategies
- Embedding model selection
- Context window optimization
- Cost optimization patterns

This should require your llm-application-dev plugin.
```

**Expected Evidence:** Specific RAG patterns, semantic chunking strategies, Claude API optimization

---

### 4. @shawar-2.0 (Deployment Expert)
**P0 Plugins:** cicd-automation, deployment-strategies, deployment-validation, cloud-infrastructure, kubernetes-operations

**Test Task:**
```
@shawar-2.0 What is the blue-green deployment strategy and how would you implement it with Railway?

Required:
- Blue-green deployment steps
- Rollback strategy
- Health check validation
- Zero-downtime deployment pattern

This should require your deployment-strategies plugin.
```

**Expected Evidence:** Specific blue-green deployment pattern, health check endpoints, traffic switching

---

### 5. @ankur-2.0 (Quality Gatekeeper)
**P0 Plugins:** security-scanning, security-compliance, backend-api-security, code-refactoring, codebase-cleanup

**Test Task:**
```
@ankur-2.0 What are the OWASP Top 10 security checks I should perform on a FastAPI endpoint?

Required:
- Top 10 vulnerabilities
- FastAPI-specific security patterns
- Input validation requirements
- Authentication/authorization checks

This should require your security-scanning and backend-api-security plugins.
```

**Expected Evidence:** OWASP Top 10 list, SQL injection prevention, XSS prevention, authentication patterns

---

### 6. @harshit-2.0 (Test Executor)
**P0 Plugins:** testing, tdd-workflows, unit-testing, performance-testing-review, application-performance

**Test Task:**
```
@harshit-2.0 What is the TDD workflow for writing tests for a new FastAPI endpoint?

Required:
- Red-Green-Refactor cycle
- Test structure (Arrange-Act-Assert)
- Mocking patterns for external dependencies
- Test coverage requirements

This should require your tdd-workflows plugin.
```

**Expected Evidence:** TDD cycle steps, AAA pattern, pytest fixtures, mocking patterns

---

### 7. @vidya-2.0 (Solution Architect)
**P0 Plugins:** cloud-infrastructure, backend-development, api-development

**Test Task:**
```
@vidya-2.0 What are the cloud infrastructure patterns for a scalable API with database?

Required:
- Multi-tier architecture
- Load balancing strategy
- Database connection pooling
- Caching layer design

This should require your cloud-infrastructure and api-development plugins.
```

**Expected Evidence:** Specific architecture patterns, connection pooling configs, caching strategies

---

### 8. @anand-2.0 (Full-Stack Executor)
**P0 Plugins:** code-review, security-scanning, backend-development, api-development, database, database-migrations

**Test Task:**
```
@anand-2.0 What are the best practices for database migrations with Alembic in FastAPI?

Required:
- Migration file naming convention
- Rollback strategy
- Data migration patterns
- Zero-downtime migration approach

This should require your database-migrations plugin.
```

**Expected Evidence:** Alembic migration patterns, upgrade/downgrade functions, data migration strategies

---

### 9. @atharva-2.0 (Feature Orchestrator)
**P0 Plugins:** agent-orchestration, full-stack-orchestration, documentation-generation, code-documentation

**Test Task:**
```
@atharva-2.0 What is the agent orchestration pattern for a full-stack feature requiring frontend, backend, and deployment?

Required:
- Agent delegation sequence
- Coordination patterns
- Handoff protocols
- Documentation requirements

This should require your agent-orchestration and full-stack-orchestration plugins.
```

**Expected Evidence:** Specific delegation chains, agent coordination patterns, handoff protocols

---

### 10. @debugger (Bug Investigation)
**P0 Plugins:** error-debugging, debugging-toolkit, observability-monitoring

**Test Task:**
```
@debugger What is the systematic approach to debugging a production memory leak in Python/FastAPI?

Required:
- Memory profiling tools
- Debugging workflow
- Common memory leak patterns
- Observability metrics to check

This should require your error-debugging and observability-monitoring plugins.
```

**Expected Evidence:** Memory profiling tools (memory_profiler, tracemalloc), specific debugging steps

---

### 11. @bug-fix-orchestrator (Bug Fix Manager)
**P0 Plugins:** error-debugging, git-pr-workflows

**Test Task:**
```
@bug-fix-orchestrator What is the git workflow for a critical production hotfix?

Required:
- Hotfix branch strategy
- Cherry-pick patterns
- Emergency deployment process
- Rollback plan

This should require your git-pr-workflows plugin.
```

**Expected Evidence:** Hotfix branch naming (hotfix/*), git cherry-pick commands, merge strategies

---

### 12. @memory-expert (Memory Management)
**P0 Plugins:** code-documentation

**Test Task:**
```
@memory-expert What are the documentation standards for API endpoints in FastAPI?

Required:
- Docstring format
- OpenAPI/Swagger annotations
- Parameter documentation
- Response schema documentation

This should require your code-documentation plugin.
```

**Expected Evidence:** FastAPI docstring patterns, Pydantic schema docs, OpenAPI tags

---

### 13. @reflection-expert (Quality Validation)
**P0 Plugins:** code-review, security-scanning

**Test Task:**
```
@reflection-expert What are the code review checklist items for a security-sensitive FastAPI endpoint?

Required:
- Security checks (OWASP)
- Code quality standards
- Input validation requirements
- Error handling patterns

This should require your code-review and security-scanning plugins.
```

**Expected Evidence:** Code review checklist, OWASP references, security patterns

---

### 14. @documentation-manager (Documentation Lifecycle)
**P0 Plugins:** seo-content-creation

**Test Task:**
```
@documentation-manager What are the SEO best practices for technical documentation?

Required:
- Meta tags structure
- Heading hierarchy (H1, H2, H3)
- Keyword optimization
- Internal linking strategy

This should require your seo-content-creation plugin.
```

**Expected Evidence:** SEO meta tags, heading structure, keyword density, alt text patterns

---

## Testing Execution

I'll now invoke each agent with their specific task via @ mentions.

**Expected Outcome:** Each agent should reference plugin-specific knowledge that wouldn't be available from general LLM training.

**Success Criteria:**
- Agent references plugin-specific patterns
- Agent provides framework/tool-specific details
- Agent shows knowledge beyond general best practices
- Agent cites specific standards (WCAG, OWASP, etc.)
