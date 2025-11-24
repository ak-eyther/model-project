# Agent Plugin Test Questions

**Purpose:** Test all 14 agents to verify they can access their P0 plugins

**Method:** Ask each agent a question that REQUIRES plugin-specific knowledge to answer correctly

---

## Test Questions (Copy-Paste Ready)

### 1. Harshit 2.0 (Test Executor)
**P0 Plugin:** tdd-workflows
**Question:**
```
@harshit-2.0 What is the TDD workflow for writing tests for a new FastAPI endpoint? Include Red-Green-Refactor cycle, Arrange-Act-Assert pattern, pytest fixtures, and mocking patterns for external dependencies.
```

### 2. Anand 2.0 (Full-Stack Executor)
**P0 Plugin:** database-migrations
**Question:**
```
@anand-2.0 What are the best practices for database migrations with Alembic in FastAPI? Include migration file naming convention, upgrade/downgrade functions, data migration patterns, and zero-downtime migration approach.
```

### 3. Atharva 2.0 (Feature Orchestrator)
**P0 Plugin:** agent-orchestration
**Question:**
```
@atharva-2.0 What is the agent orchestration pattern for a full-stack feature requiring frontend, backend, and deployment? Include agent delegation sequence, coordination patterns, handoff protocols, and documentation requirements.
```

### 4. SAMA 2.0 (AI/ML Engineer)
**P0 Plugin:** llm-application-dev
**Question:**
```
@sama-2.0 What are the best practices for implementing RAG (Retrieval-Augmented Generation) with Claude API? Include chunking strategies, embedding model selection, context window optimization, and cost optimization patterns.
```

### 5. Shawar 2.0 (Deployment Expert)
**P0 Plugin:** deployment-strategies
**Question:**
```
@shawar-2.0 What is the blue-green deployment strategy and how would you implement it with Railway? Include deployment steps, rollback strategy, health check validation, and zero-downtime deployment pattern.
```

### 6. Ankur 2.0 (Quality Gatekeeper)
**P0 Plugin:** security-scanning
**Question:**
```
@ankur-2.0 What are the OWASP Top 10 security checks I should perform on a FastAPI endpoint? Include vulnerability list, FastAPI-specific security patterns, input validation requirements, and authentication/authorization checks.
```

### 7. Vidya 2.0 (Solution Architect)
**P0 Plugin:** cloud-infrastructure
**Question:**
```
@vidya-2.0 What are the cloud infrastructure patterns for a scalable API with database? Include multi-tier architecture, load balancing strategy, database connection pooling, and caching layer design.
```

### 8. Hitesh 2.0 (Frontend Specialist)
**P0 Plugin:** framework-migration
**Question:**
```
@hitesh-2.0 What are the modern React 18+ patterns for migrating from class components to functional components with hooks? Include lifecycle method equivalents, state management migration patterns, and performance optimization with hooks.
```

### 9. Varsha 2.0 (UI/UX Designer)
**P0 Plugin:** accessibility-compliance
**Question:**
```
@varsha-2.0 Create a design spec for an accessible file upload button that meets WCAG 2.1 AA standards. Include specific ARIA labels, minimum color contrast ratios, keyboard navigation requirements, and screen reader announcements.
```

### 10. Debugger (Bug Investigation)
**P0 Plugin:** error-debugging
**Question:**
```
@debugger What is the systematic approach to debugging a production memory leak in Python/FastAPI? Include memory profiling tools, debugging workflow, common memory leak patterns, and observability metrics to check.
```

### 11. Bug Fix Orchestrator
**P0 Plugin:** git-pr-workflows
**Question:**
```
@bug-fix-orchestrator What is the git workflow for a critical production hotfix? Include hotfix branch strategy, cherry-pick patterns, emergency deployment process, and rollback plan.
```

### 12. Memory Expert
**P0 Plugin:** code-documentation
**Question:**
```
@memory-expert What are the documentation standards for API endpoints in FastAPI? Include docstring format, OpenAPI/Swagger annotations, parameter documentation, and response schema documentation.
```

### 13. Reflection Expert
**P0 Plugin:** code-review
**Question:**
```
@reflection-expert What are the code review checklist items for a security-sensitive FastAPI endpoint? Include security checks (OWASP), code quality standards, input validation requirements, and error handling patterns.
```

### 14. Documentation Manager
**P0 Plugin:** seo-content-creation
**Question:**
```
@documentation-manager What are the SEO best practices for technical documentation? Include meta tags structure, heading hierarchy (H1, H2, H3), keyword optimization, and internal linking strategy.
```

---

## Testing Instructions

1. Copy each question above (one at a time or in batches)
2. Paste into conversation
3. Wait for agent response
4. Analyze response for plugin-specific evidence
5. Record results in PLUGIN_EVIDENCE_TRACKING.md

---

**Expected Evidence Types:**
- ✅ **Strong:** Specific tool commands, exact configurations, framework-specific patterns
- ⚠️ **Weak:** General best practices without specifics
- ❌ **None:** Vague statements, no standards referenced
