---
name: solution-patterns
description: Index of documented solution patterns from past engineering problems. Use this skill when encountering similar issues to leverage proven solutions for TypeScript strict mode compliance, authentication migrations, and error handling patterns.
metadata:
  short-description: Past engineering solutions and patterns
---

# Solution Patterns Skill

Reference documented solutions from past engineering problems to avoid re-solving known issues.

## When to Use This Skill

Use this skill when you encounter:
- TypeScript strict mode compilation errors (`noImplicitReturns`, implicit returns in catch blocks)
- Authentication system changes or migrations (NextAuth, Clerk, JWT verification)
- Database error handling patterns (silent failures, lost context, inconsistent error types)
- Drizzle ORM query patterns with proper error propagation

## Solution Index

| Problem Domain | Solution Document | Key Pattern |
|----------------|-------------------|-------------|
| TypeScript Strict Mode | `docs/solutions/type-safety/typescript-strict-mode-database-queries.md` | `return throwDbError()` with `never` return type |
| Auth Migration | `docs/solutions/architecture-decisions/nextauth-to-clerk-migration.md` | Clerk user mapping + JWKS JWT verification |
| DB Error Handling | `docs/solutions/error-handling/database-error-propagation.md` | Centralized `throwDbError()` helper |

## Quick Reference Patterns

### Pattern 1: TypeScript `noImplicitReturns` Fix

When catch blocks throw but TypeScript complains about missing return:

```typescript
// Problem: TypeScript error - function lacks ending return statement
async function getUser(id: string): Promise<User | null> {
  try {
    const [user] = await db.select().from(users).where(eq(users.id, id));
    return user ?? null;
  } catch (error) {
    throw new Error("Failed"); // TypeScript thinks code continues after this
  }
}

// Solution: Use helper that returns `never`
const throwDbError = (message: string, error: unknown): never => {
  console.error(message, error);
  throw new ChatSDKError("bad_request:database", message);
};

async function getUser(id: string): Promise<User | null> {
  try {
    const [user] = await db.select().from(users).where(eq(users.id, id));
    return user ?? null;
  } catch (error) {
    return throwDbError("Failed to get user", error); // `return` + `never` = terminates
  }
}
```

### Pattern 2: Clerk User Mapping

Map Clerk IDs to local database users with branded types:

```typescript
export type ClerkUserId = string & { readonly __brand: "ClerkUserId" };
export type DatabaseUserId = string & { readonly __brand: "DatabaseUserId" };

export const requireClerkUser = async (): Promise<ClerkUserContext> => {
  const { userId } = await auth();

  // Check local DB first (avoids Clerk API call)
  const existingUser = await getUserByClerkId(userId);
  if (existingUser) {
    return { clerkUserId: userId as ClerkUserId, userId: existingUser.id as DatabaseUserId };
  }

  // Fallback: fetch from Clerk API and create local user
  const dbUser = await getOrCreateUserByClerkId({ clerkUserId: userId, email });
  return { /* ... */ };
};
```

### Pattern 3: Backend JWT Verification

Dual auth for FastAPI (API key or Clerk JWT):

```python
def verify_api_key_or_clerk(request: Request, x_api_key: Optional[str] = Header(default=None)):
    # Option 1: API key for server-to-server
    if x_api_key and secrets.compare_digest(x_api_key, expected):
        return {"type": "api_key"}

    # Option 2: Clerk JWT for browser clients
    authorization = request.headers.get("Authorization")
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ", 1)[1].strip()
        claims = _decode_clerk_token(token)  # JWKS verification
        return {"type": "clerk", "claims": claims}

    raise HTTPException(status_code=401)
```

## Prevention Checklists

### TypeScript Strict Mode Checklist
- [ ] All async functions have explicit `Promise<T>` return types
- [ ] All catch blocks use `return throwDbError()` or equivalent
- [ ] Nullable queries return `null`, not `undefined`
- [ ] Insert/update operations verify result before returning

### Error Handling Checklist
- [ ] No empty catch blocks
- [ ] Error messages include operation context
- [ ] Consistent error types (ChatSDKError)
- [ ] Errors are logged before throwing

## Full Documentation

For complete details, read the full solution documents:
- `docs/solutions/type-safety/typescript-strict-mode-database-queries.md`
- `docs/solutions/architecture-decisions/nextauth-to-clerk-migration.md`
- `docs/solutions/error-handling/database-error-propagation.md`
