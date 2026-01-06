---
name: fastapi-production-patterns
description: Build production-ready FastAPI applications with async patterns, Pydantic validation, dependency injection, middleware, and database integration. Use for FastAPI endpoints, async workflows, or API design.
metadata:
  short-description: FastAPI production patterns
---

# FastAPI Production Patterns

## App Structure with Lifespan

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await database.connect()
    yield
    # Shutdown
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
```

## Async Endpoints

```python
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

## Pydantic Models with Validation

```python
from pydantic import BaseModel, validator, Field

class UserCreate(BaseModel):
    email: str = Field(..., example="user@example.com")
    age: int = Field(..., ge=0, le=150)

    @validator('email')
    def validate_email(cls, v):
        if '@' not in v or '.' not in v.split('@')[1]:
            raise ValueError('Invalid email format')
        return v.lower()

    class Config:
        orm_mode = True
```

---

## 🚨 CRITICAL: Pydantic v2 + PEP 563 Incompatibility (PR #75 Learning)

**Date:** 2026-01-03
**Issue:** `from __future__ import annotations` breaks FastAPI route type resolution

### The Problem

PEP 563 (`from __future__ import annotations`) makes ALL type hints strings for deferred evaluation. This breaks FastAPI's Pydantic v2 type adapter resolution at route definition time.

```python
# ❌ BROKEN - causes PydanticUndefinedAnnotation error
from __future__ import annotations  # <-- THIS BREAKS FASTAPI!

from pydantic import BaseModel

class FeedbackRequest(BaseModel):
    session_id: str
    rating: str

@router.post("", response_model=FeedbackResponse)
async def submit_feedback(
    feedback_request: FeedbackRequest,  # <-- Error: name 'FeedbackRequest' is not defined
):
    ...
```

**Error Message:**
```
pydantic.errors.PydanticUndefinedAnnotation: name 'FeedbackRequest' is not defined
```

### Why It Happens

1. FastAPI processes route decorators at **module import time**
2. PEP 563 makes `FeedbackRequest` a **string** annotation instead of a class reference
3. When FastAPI tries to resolve the string at import time, the class isn't available yet
4. `model_rebuild()` doesn't help because FastAPI reads annotations BEFORE it runs

### The Fix

**DO NOT use `from __future__ import annotations` in FastAPI route files:**

```python
# ✅ CORRECT - works with FastAPI + Pydantic v2
"""Feedback API routes."""
# Note: Do NOT use `from __future__ import annotations` here!
# It causes PEP 563 string annotations which break FastAPI's type adapter
# resolution for Pydantic models in route function signatures.

from pydantic import BaseModel

class FeedbackRequest(BaseModel):
    session_id: str
    rating: str

@router.post("", response_model=FeedbackResponse)
async def submit_feedback(feedback_request: FeedbackRequest):  # Works!
    ...
```

### When You CAN Use PEP 563

- Pure Pydantic model files (no FastAPI routes)
- Utility modules with no route decorators
- Type-only modules for static type checking

### Quick Check

If you see this error, grep for the import:
```bash
grep -n "from __future__ import annotations" backend/app/api/routes/*.py
```

If found in a route file, **remove it**.

---

## Dependency Injection

```python
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    user = await verify_token(token, db)
    return user

@app.get("/me")
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    return current_user
```

## CORS Middleware

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

## Error Handling

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

class CustomException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name}"}
    )
```

---

## 🔐 Error Logging Best Practices (PR #75 Learning)

**Date:** 2026-01-03
**Issue:** Logging `str(e)` can expose database schema, connection strings, or PII

### ❌ BAD - Information Disclosure Risk

```python
except Exception as e:
    logger.error("Failed: %s", str(e))  # May leak DB details!
    raise HTTPException(status_code=500, detail="Internal error")
```

If exception contains DB connection string or schema info, it goes to logs.

### ✅ GOOD - Log Exception Type Only

```python
except Exception as e:
    logger.error(
        "Failed to submit feedback: session_id=%s, error_type=%s",
        request.session_id,
        type(e).__name__,  # Safe: logs "ValueError" not the message
    )
    raise HTTPException(status_code=500, detail="Internal error")
```

### When Full Exception IS Safe

- Local development (not production logs)
- Internal debugging with `exc_info=True` (goes to Sentry, not stdout)
- Known-safe exception types (ValidationError, HTTPException)

```python
# OK for debugging - exc_info goes to Sentry, not stdout
logger.error("Database query failed", exc_info=True)
```

---

## 🔑 API Key Verification Pattern (PR #75 Learning)

**Date:** 2026-01-03
**Issue:** Development bypass must not silently disable security in production

### Pattern with Development Bypass Warning

```python
import secrets
from typing import Optional
from fastapi import Header, HTTPException, status
from app.config import settings
import logging

logger = logging.getLogger(__name__)

def _verify_api_key(
    x_api_key: Optional[str] = Header(default=None, alias="X-API-Key"),
) -> None:
    """
    Verify API key for protected endpoints.

    If API_KEY is not configured (empty), endpoints are open (dev mode).
    If configured, X-API-Key header must match.
    """
    expected = settings.API_KEY_V3
    if not expected:
        # Development mode - log warning on first request
        logger.warning(
            "API_KEY_V3 not configured - endpoint is OPEN (dev mode). "
            "Set API_KEY_V3 in production!"
        )
        return

    if not x_api_key or not secrets.compare_digest(str(x_api_key), str(expected)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
```

### Key Security Points

1. **Use `secrets.compare_digest()`** - Timing-safe comparison prevents timing attacks
2. **Log warning when disabled** - Makes misconfiguration visible in logs
3. **Convert to strings** - Handles edge cases where header/env var types differ
4. **Return 401 not 403** - 401 = authentication failed (no/bad key), 403 = forbidden (valid key, no permission)

---

## Background Tasks

```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Send email logic
    pass

@app.post("/send-notification/")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_email, email, "notification")
    return {"message": "Notification sent in background"}
```

## File Upload

```python
from fastapi import File, UploadFile

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    # Process file
    return {"filename": file.filename, "size": len(contents)}
```

---

**Last Updated:** 2026-01-03
**Changelog:**
- 2026-01-03: Added Pydantic v2 + PEP 563 incompatibility pattern (PR #75), error logging best practices, API key verification pattern
