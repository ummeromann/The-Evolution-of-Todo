# JWT Token Contract

**Feature**: 002-auth-security-integration
**Date**: 2026-01-14

## Overview

This document defines the JWT token structure used for authentication between the Next.js frontend (Better Auth) and FastAPI backend.

## Token Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        Authentication Flow                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. User signs up/in via Better Auth (Next.js)                  │
│                    │                                             │
│                    ▼                                             │
│  2. Better Auth creates session & JWT token                     │
│                    │                                             │
│                    ▼                                             │
│  3. Token stored in client (httpOnly cookie or localStorage)    │
│                    │                                             │
│                    ▼                                             │
│  4. Frontend API client attaches token to requests              │
│     Authorization: Bearer <jwt_token>                           │
│                    │                                             │
│                    ▼                                             │
│  5. FastAPI middleware validates token using shared secret      │
│                    │                                             │
│                    ▼                                             │
│  6. User ID extracted from 'sub' claim for query filtering      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Token Structure

### Header

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### Payload (Claims)

| Claim | Type | Required | Description |
|-------|------|----------|-------------|
| `sub` | string (UUID) | Yes | User ID - primary identifier for authorization |
| `email` | string | Yes | User's email address |
| `iat` | integer | Yes | Issued at timestamp (Unix epoch seconds) |
| `exp` | integer | Yes | Expiration timestamp (Unix epoch seconds) |
| `iss` | string | No | Issuer identifier (Better Auth) |

### Example Payload

```json
{
  "sub": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "iat": 1736841600,
  "exp": 1737446400,
  "iss": "better-auth"
}
```

## Signature

- **Algorithm**: HS256 (HMAC with SHA-256)
- **Secret**: `BETTER_AUTH_SECRET` environment variable
- **Encoding**: Base64URL

### Signature Generation

```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  BETTER_AUTH_SECRET
)
```

## Token Lifetime

| Setting | Value | Rationale |
|---------|-------|-----------|
| Expiration | 7 days | Balance between security and user convenience |
| Session Update | 1 day | Token refreshed if older than 24 hours |

## Validation Rules

### Backend (FastAPI)

1. **Verify Signature**: Using `BETTER_AUTH_SECRET`
2. **Check Expiration**: `exp` must be in the future
3. **Extract User ID**: From `sub` claim (UUID format)
4. **Validate Format**: Must be valid UUID string

### Validation Code Reference

```python
# backend/app/middleware/auth.py

payload = jwt.decode(
    token,
    settings.BETTER_AUTH_SECRET,
    algorithms=["HS256"],
    options={"verify_exp": True}
)

user_id = payload.get("sub")
if not user_id:
    raise HTTPException(status_code=401, detail="Invalid token: missing user ID")

return UUID(user_id)
```

## Error Responses

| Error | HTTP Status | Response Body |
|-------|-------------|---------------|
| Missing token | 401 | `{"detail": "Not authenticated"}` |
| Invalid signature | 401 | `{"detail": "Invalid token"}` |
| Expired token | 401 | `{"detail": "Token has expired"}` |
| Missing `sub` claim | 401 | `{"detail": "Invalid token: missing user ID"}` |
| Invalid UUID format | 401 | `{"detail": "Invalid token"}` |

## Security Considerations

### Environment Variables

```bash
# backend/.env
BETTER_AUTH_SECRET=<cryptographically-random-string-min-32-chars>

# frontend/.env.local
BETTER_AUTH_SECRET=<same-value-as-backend>
```

### Best Practices

1. **Secret Rotation**: Plan for secret rotation (requires re-authentication)
2. **HTTPS Only**: Tokens must only be transmitted over HTTPS
3. **No Sensitive Data**: Don't store sensitive data in token payload
4. **Consistent Errors**: Generic error messages prevent information leakage

## Integration Points

### Frontend (Better Auth)

```typescript
// frontend/src/lib/auth.ts
export const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.DATABASE_URL,
  }),
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // 1 day
  },
  secret: process.env.BETTER_AUTH_SECRET, // Uses HS256 by default
});
```

**Note**: Better Auth uses HS256 (HMAC-SHA256) as the default JWT signing algorithm. No explicit configuration is needed.

### API Client

```typescript
// frontend/src/lib/api.ts
const token = await getSessionToken(); // From Better Auth
headers.set('Authorization', `Bearer ${token}`);
```

### Backend Dependency

```python
# backend/app/api/deps.py
from app.middleware.auth import get_current_user

# Usage in route
@router.get("/api/tasks")
async def list_tasks(user_id: UUID = Depends(get_current_user)):
    # user_id is validated and extracted from JWT
```

## Testing Token Validation

### Valid Token Test

```bash
curl -X GET "http://localhost:8000/api/tasks" \
  -H "Authorization: Bearer <valid_jwt_token>"
# Expected: 200 OK with task list
```

### Invalid Token Test

```bash
curl -X GET "http://localhost:8000/api/tasks" \
  -H "Authorization: Bearer invalid_token"
# Expected: 401 Unauthorized
```

### Missing Token Test

```bash
curl -X GET "http://localhost:8000/api/tasks"
# Expected: 401 Unauthorized
```
