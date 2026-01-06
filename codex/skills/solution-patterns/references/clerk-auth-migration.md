# Clerk Auth Migration Pattern

**Source:** `docs/solutions/architecture-decisions/nextauth-to-clerk-migration.md`

## Problem

NextAuth lacked:
- Native organization support
- Built-in role management
- Vercel-first integration
- Simple backend JWT verification

## Solution: 7-Phase Clerk Migration

1. Domain and Clerk Organizations setup
2. Frontend auth migration
3. User mapping layer (Clerk ID to local DB)
4. Backend JWT verification
5. Admin route and marketing entry
6. Testing and rollout
7. Hardening and review fixes

## Key Patterns

### User Mapping with Branded Types

```typescript
export type ClerkUserId = string & { readonly __brand: "ClerkUserId" };
export type DatabaseUserId = string & { readonly __brand: "DatabaseUserId" };

export type ClerkUserContext = {
  clerkUserId: ClerkUserId;
  email: string;
  role: ClerkRole;
  userId: DatabaseUserId;
};
```

### Middleware Configuration

```typescript
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";

const isPublicRoute = createRouteMatcher([
  "/sign-in(.*)",
  "/sign-up(.*)",
  "/api/webhook(.*)",
  "/ping",
]);

export default clerkMiddleware(
  async (auth, request) => {
    if (isPublicRoute(request)) return;
    await auth.protect();
  },
  { signInUrl: "/sign-in", signUpUrl: "/sign-up" }
);
```

### Backend JWT Verification (FastAPI)

```python
def verify_api_key_or_clerk(request: Request, x_api_key: Optional[str] = Header(default=None)):
    # API key for server-to-server
    if x_api_key and secrets.compare_digest(x_api_key, expected):
        return {"type": "api_key"}

    # Clerk JWT for browser clients
    authorization = request.headers.get("Authorization")
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ", 1)[1].strip()
        claims = _decode_clerk_token(token)  # JWKS verification
        return {"type": "clerk", "claims": claims}

    raise HTTPException(status_code=401)
```

### Playwright Test Bypass

```typescript
const isPlaywright = ["true", "True"].includes(process.env.PLAYWRIGHT ?? "");
const allowTestBypass = isPlaywright && process.env.NODE_ENV !== "production";

export const requireClerkUser = async (): Promise<ClerkUserContext> => {
  if (allowTestBypass) {
    const dbUser = await getOrCreateUserByClerkId({
      clerkUserId: testClerkUserId,
      email: testClerkUserEmail,
    });
    return { /* synthetic context */ };
  }
  // ... normal auth flow
};
```

## Database Schema

```sql
ALTER TABLE "User" ADD COLUMN "clerk_user_id" varchar(255);
CREATE INDEX "user_clerk_user_id_idx" ON "User" ("clerk_user_id");
```
