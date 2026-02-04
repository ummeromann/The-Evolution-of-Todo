# Authentication Flow Contract

**Feature Branch**: `001-todo-fullstack-webapp`
**Date**: 2026-01-13

## Overview

This document defines the authentication flow contract between the Next.js frontend (with Better Auth) and the FastAPI backend. Better Auth handles user registration, sign-in, and JWT issuance on the frontend, while FastAPI validates JWT tokens for protected API endpoints.

---

## Authentication Architecture

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND (Next.js)                             │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌──────────────┐     ┌─────────────────┐     ┌──────────────────────┐    │
│  │   User UI    │────►│  Better Auth    │────►│  Better Auth API     │    │
│  │ (Forms)      │     │  Client SDK     │     │  Routes (/api/auth)  │    │
│  └──────────────┘     └─────────────────┘     └──────────┬───────────┘    │
│                                                          │                 │
│                                              JWT Token issued              │
│                                                          │                 │
│                       ┌─────────────────┐               │                 │
│                       │   API Client    │◄──────────────┘                 │
│                       │ (JWT attached)  │                                  │
│                       └────────┬────────┘                                  │
│                                │                                           │
└────────────────────────────────┼───────────────────────────────────────────┘
                                 │
                    Authorization: Bearer <token>
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND (FastAPI)                              │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌──────────────────┐     ┌─────────────────┐     ┌──────────────────┐    │
│  │  Auth Middleware │────►│  JWT Validator  │────►│  Protected       │    │
│  │                  │     │  (JWKS/Secret)  │     │  Endpoints       │    │
│  └──────────────────┘     └─────────────────┘     └──────────────────┘    │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Better Auth Configuration (Frontend)

### Endpoints (Next.js API Routes)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/sign-up/email` | POST | Register new user |
| `/api/auth/sign-in/email` | POST | Authenticate user |
| `/api/auth/sign-out` | POST | End session |
| `/api/auth/session` | GET | Get current session |

### Sign-Up Request

```typescript
// POST /api/auth/sign-up/email
interface SignUpRequest {
  email: string;      // Valid email format
  password: string;   // Minimum 8 characters
  name?: string;      // Optional display name
}

interface SignUpResponse {
  user: {
    id: string;
    email: string;
    name?: string;
    createdAt: string;
  };
  session: {
    id: string;
    userId: string;
    expiresAt: string;
  };
}
```

### Sign-In Request

```typescript
// POST /api/auth/sign-in/email
interface SignInRequest {
  email: string;
  password: string;
}

interface SignInResponse {
  user: {
    id: string;
    email: string;
    name?: string;
  };
  session: {
    id: string;
    userId: string;
    expiresAt: string;
  };
}
```

### Session Response

```typescript
// GET /api/auth/session
interface SessionResponse {
  user: {
    id: string;
    email: string;
    name?: string;
  } | null;
  session: {
    id: string;
    userId: string;
    expiresAt: string;
  } | null;
}
```

---

## JWT Token Contract

### Token Structure

```typescript
interface JWTPayload {
  sub: string;        // User ID (UUID)
  email: string;      // User email
  iat: number;        // Issued at timestamp
  exp: number;        // Expiration timestamp
  iss: string;        // Issuer (Better Auth)
}
```

### Token Transport

- **Header**: `Authorization: Bearer <token>`
- **Format**: Standard JWT (header.payload.signature)
- **Encoding**: Base64URL

### Token Lifecycle

| Event | Action |
|-------|--------|
| Sign-in successful | Token issued, stored in session |
| API request | Token retrieved, attached to Authorization header |
| Token expired | 401 response, redirect to sign-in |
| Sign-out | Session invalidated, token cleared |

---

## FastAPI JWT Validation

### Validation Flow

```python
async def validate_jwt(token: str) -> JWTPayload:
    """
    1. Extract token from Authorization header
    2. Decode token (without verification first to get header)
    3. Verify signature using Better Auth secret/JWKS
    4. Validate expiration (exp claim)
    5. Validate issuer (iss claim)
    6. Return payload with user_id (sub claim)
    """
    pass
```

### Dependency Injection

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Returns user_id (UUID) from validated JWT.
    Raises HTTPException 401 if invalid/expired.
    """
    token = credentials.credentials
    payload = await validate_jwt(token)
    return payload["sub"]  # User ID
```

### Protected Route Usage

```python
@router.get("/api/tasks")
async def list_tasks(
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # user_id guaranteed to be authenticated
    tasks = await get_user_tasks(db, user_id)
    return tasks
```

---

## Error Responses

### 401 Unauthorized

Returned when:
- No Authorization header present
- Token format invalid
- Token signature invalid
- Token expired

```json
{
  "detail": "Not authenticated",
  "code": "UNAUTHORIZED"
}
```

### 403 Forbidden

Returned when:
- Valid token but accessing another user's resource

```json
{
  "detail": "Access denied to this resource",
  "code": "FORBIDDEN"
}
```

---

## Environment Variables

### Frontend (.env.local)

```bash
# Better Auth
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000

# Database (for Better Auth session storage)
DATABASE_URL=postgresql://user:pass@host/db

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env)

```bash
# JWT Validation
BETTER_AUTH_SECRET=your-secret-key-min-32-chars

# Or use JWKS endpoint
BETTER_AUTH_JWKS_URL=http://localhost:3000/.well-known/jwks.json

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host/db

# CORS
CORS_ORIGINS=http://localhost:3000
```

---

## Security Requirements

| Requirement | Implementation |
|-------------|----------------|
| Token expiration | Better Auth default or configured expiry |
| Signature verification | HMAC-SHA256 with shared secret |
| User isolation | All queries filtered by user_id from token |
| HTTPS in production | Required for token transport |
| Secret rotation | Support for multiple secrets during rotation |

---

## Testing Contracts

### Valid Token Test

```bash
# Should return 200 with user's tasks
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <valid-token>"
```

### Missing Token Test

```bash
# Should return 401
curl -X GET http://localhost:8000/api/tasks
```

### Invalid Token Test

```bash
# Should return 401
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer invalid-token"
```

### Expired Token Test

```bash
# Should return 401
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <expired-token>"
```

### Cross-User Access Test

```bash
# User A's token trying to access User B's task
# Should return 403
curl -X GET http://localhost:8000/api/tasks/<user-b-task-id> \
  -H "Authorization: Bearer <user-a-token>"
```
