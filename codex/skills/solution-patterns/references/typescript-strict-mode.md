# TypeScript Strict Mode Database Queries Pattern

**Source:** `docs/solutions/type-safety/typescript-strict-mode-database-queries.md`

## Problem

TypeScript strict mode (`noImplicitReturns: true`) fails when:
- Catch blocks throw but don't "return"
- Functions lack explicit `Promise<T>` return types
- Nullable queries return `undefined` instead of `null`
- Insert operations don't verify results

## Solution

### The `throwDbError()` Helper

```typescript
const throwDbError = (message: string, error: unknown): never => {
  console.error(message, error);
  throw new ChatSDKError("bad_request:database", message);
};
```

### Usage Pattern

```typescript
export async function getUser(id: string): Promise<User | null> {
  try {
    const [user] = await db.select().from(users).where(eq(users.id, id));
    return user ?? null;  // Explicit null, not undefined
  } catch (error) {
    return throwDbError("Failed to get user", error);  // return + never = terminates
  }
}
```

### Key Commits

| Commit | Description |
|--------|-------------|
| `4446d18` | Type document queries |
| `41b5d3f` | Type query helpers for arrays |
| `adc396b` | Enforce user creation return types |
| `c595099` | Make db errors return explicitly |

## Checklist

- [ ] All async functions have explicit `Promise<T>` return types
- [ ] All catch blocks use `return throwDbError()` or equivalent
- [ ] Nullable queries return `null`, not `undefined`
- [ ] Insert/update operations check if result is defined
