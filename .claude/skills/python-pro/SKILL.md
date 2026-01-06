---
name: python-pro
description: Write idiomatic Python code with advanced features like decorators, generators, and async/await. Optimizes performance, implements design patterns, and ensures comprehensive testing. Use for ML training, analytics tools, performance profiling, or any Python heavy lifting.
metadata:
  short-description: Advanced Python patterns
---

# Python Pro - Advanced Python Patterns

## When to Use This Skill

**Invoke python-pro for:**
- CatBoost model training (ml/train_models.py, feature_builder.py)
- Analytics tools optimization (async batching, caching)
- Performance profiling (bottleneck identification)
- Advanced Python patterns (decorators, generators, context managers)
- Heavy data processing on campaign datasets
- Executing ML designs from @sama-2.0

**Use fastapi-production-patterns instead for:**
- API endpoints, routing, middleware
- Pydantic validation, request/response models
- CORS configuration, authentication middleware
- FastAPI-specific patterns (dependency injection at API layer)

**Clear Boundary:**
| fastapi-production-patterns | python-pro |
|-----------------------------|------------|
| API layer (HTTP, routing) | Business logic (ML, analytics) |
| Pydantic, middleware, CORS | Decorators, generators, profiling |
| FastAPI endpoints | Core Python optimization |

---

## Executable Scripts

Run these scripts directly for profiling and debugging:

### Profile a Function
```bash
python scripts/profile_function.py app.ml.feature_builder build_features
python scripts/profile_function.py app.agents.analyst gather_evidence_async --args '{"candidate": {"list_id": "GM_30D"}}'
```

### Compare Two Implementations
```bash
python scripts/benchmark_compare.py app.tools.v1:analyze app.tools.v2:analyze_async --runs 10
```

### Check Memory Usage
```bash
python scripts/memory_check.py app.ml.feature_builder build_all_features --args '{"n_campaigns": 1000}'
```

---

## {{PROJECT_NAME}} ML System

Use `references/mission_inbox_ml.md` for ML-specific documentation:
- Model locations (`ml/models/*.cbm`)
- Training commands (`python ml/train_models.py`)
- Feature list (110 features from `FeatureBuilder`)
- How `MLPredictor` serves predictions to Analyst Agent
- EPC lookup (historical, NOT ML)
- Database tables used for training

---

## Core Patterns and Examples

Use `references/patterns.md` for detailed code patterns and examples across:
- Decorators (caching, timing, retries, validation)
- Generators (lazy feature building, chunking, async generators)
- Async/concurrency (batching, sync-to-async, semaphores)
- Profiling (cProfile, line_profiler, memory_profiler, benchmarking)
- Type hints and static analysis (TypedDict, Protocol, Generic, mypy/ruff/black)
- Testing (fixtures, parametrization, async tests, mocking)
- Design patterns (strategy/factory for ML and tool creation)
- Quick reference cheat sheet

---

## Usage Guidance

- Prefer clear, typed interfaces for analytics and ML modules.
- Favor async batching when tool calls are independent.
- Profile before optimizing; keep hotspots visible.
