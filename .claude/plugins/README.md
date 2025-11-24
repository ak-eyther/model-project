# Agent Superpowers Plugin System

**3-layer delegation architecture for portable agent capabilities**

## Architecture

```
You (Arif Khan)
  ↓
@atharva-2.0 (Auto-invoked orchestrator)
  ↓
@anand, @hitesh, @harshit (Execution agents)
  ↓
Plugin Superpowers (Skills 90% + Sub-sub-agents 10%)
```

## Installed Plugins

### 1. anand-superpowers
Backend & full-stack execution help for @anand-2.0

**Skills (auto-loaded):**
- `nextjs-app-router-patterns` - Next.js 13+ App Router
- `fastapi-production-patterns` - FastAPI async patterns
- `smart-grep` - Token-efficient search

**Sub-sub-agents (explicit invoke):**
- `@fastapi-expert-builder` - Complex FastAPI features
- `@nextjs-expert-builder` - Complex Next.js features

### 2. hitesh-superpowers
Frontend execution help for @hitesh-2.0
*In progress*

### 3. harshit-superpowers
Testing execution help for @harshit-2.0
*In progress*

### 4. atharva-superpowers
Orchestration help for @atharva-2.0
*In progress*

### 5. shared-superpowers
Universal skills for all agents

**Skills:**
- `smart-grep` - Token-efficient codebase search

## Usage

### For You (Arif)
Just give high-level instructions:
```
"Build medical claims processing feature"
```

@atharva-2.0 auto-invokes and orchestrates everything.

### For Execution Agents

**90% of time - Skills auto-load:**
```
@anand-2.0 receives: "Build Next.js dashboard"
→ Claude auto-loads: nextjs-app-router-patterns skill
→ Anand uses guidance to implement
```

**10% of time - Explicit delegation:**
```
@anand-2.0: "This is complex, delegating to expert"
→ @fastapi-expert-builder builds complete feature
→ Returns to Anand for integration
```

## Project Context

All sub-sub-agents auto-load `.claude/context/project-context.yaml`

Contains:
- Project name, creator (Arif Khan)
- Tech stack (React, FastAPI)
- Deployment (Vercel, Railway)
- Domain context

## Created By
Arif Khan (arif.khan@vitraya.com)
