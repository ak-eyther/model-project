# Database Error Handling Pattern

**Source:** `docs/solutions/error-handling/database-error-propagation.md`

## Problem

Database errors in `lib/db/queries.ts` were handled inconsistently:
1. Silent failures - catch blocks logged but didn't throw
2. Lost context - error messages lacked operation context
3. Implicit returns - TypeScript couldn't verify all paths
4. Inconsistent error types - mix of raw errors and custom types

## Solution: Centralized `throwDbError()`

```typescript
const throwDbError = (message: string, error: unknown): never => {
  console.error(message, error);
  throw new ChatSDKError("bad_request:database", message);
};
```

### Why It Works

| Feature | Purpose |
|---------|---------|
| Returns `never` | TypeScript knows function never returns normally |
| Logs before throwing | Error context captured in server logs |
| Uses `ChatSDKError` | Consistent error type for API responses |
| Accepts `unknown` | Handles any error type from catch blocks |

## Usage Pattern

```typescript
export async function getUserByClerkId(clerkUserId: string): Promise<User | null> {
  try {
    const [existingUser] = await db
      .select()
      .from(user)
      .where(eq(user.clerkUserId, clerkUserId));
    return existingUser ?? null;
  } catch (error) {
    return throwDbError("Failed to get user by Clerk ID", error);
  }
}
```

The `return throwDbError(...)` syntax:
1. `throwDbError` returns `never` - never completes normally
2. `return` tells TypeScript this code path terminates
3. Without `return`, TypeScript thinks code continues after catch

## ChatSDKError Structure

```typescript
export class ChatSDKError extends Error {
  constructor(public readonly type: string, message?: string) {
    super(message ?? type);
    this.name = "ChatSDKError";
  }
}
```

Error type namespaces:
- `bad_request:database` - Database operation failures
- `bad_request:api` - API validation failures
- `unauthorized:auth` - Authentication failures

## Prevention Rules

```typescript
// BAD: Silent failure
try { /* ... */ } catch (e) { }

// BAD: Logs but continues
try { /* ... */ } catch (e) { console.error(e); }

// GOOD: Propagates error
try { /* ... */ } catch (e) { return throwDbError("Context", e); }
```

## Error Context Best Practices

```typescript
// Include operation context in messages
throwDbError(`Failed to get document by id: ${id}`, error);
throwDbError(`Failed to save chat for user: ${userId}`, error);
```
