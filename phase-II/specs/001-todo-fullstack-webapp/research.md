# Research: Todo Full-Stack Web Application

**Feature Branch**: `001-todo-fullstack-webapp`
**Date**: 2026-01-13
**Status**: Complete

## Overview

This document captures research findings for all technology choices, integration patterns, and best practices required to implement the Todo Full-Stack Web Application per the approved specification and constitution.

---

## 1. FastAPI Backend Best Practices

### Decision: Use FastAPI with async SQLModel

**Rationale**:
- FastAPI is the mandated backend framework per constitution
- SQLModel provides native async support with PostgreSQL
- Type hints enable automatic OpenAPI documentation
- Pydantic integration provides built-in request/response validation

**Alternatives Considered**:
- Flask: Rejected - Not in approved stack, less async support
- Django: Rejected - Not in approved stack, heavier framework

### Project Structure Pattern

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry
│   ├── config.py            # Environment configuration
│   ├── database.py          # Database connection setup
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User SQLModel
│   │   └── task.py          # Task SQLModel
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py          # User Pydantic schemas
│   │   └── task.py          # Task Pydantic schemas
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py          # Dependencies (auth, db session)
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── auth.py      # Auth endpoints
│   │       └── tasks.py     # Task CRUD endpoints
│   └── middleware/
│       ├── __init__.py
│       └── auth.py          # JWT validation middleware
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_*.py
├── requirements.txt
└── .env.example
```

### Key Patterns

1. **Dependency Injection**: Use `Depends()` for database sessions and auth
2. **Response Models**: Define explicit response schemas for all endpoints
3. **Error Handling**: Use HTTPException with consistent error structure
4. **CORS**: Configure for frontend origin

---

## 2. Neon PostgreSQL with SQLModel

### Decision: Use SQLModel with async driver (asyncpg)

**Rationale**:
- Neon PostgreSQL is the mandated database per constitution
- SQLModel provides ORM capabilities with SQLAlchemy core
- Async driver enables non-blocking database operations
- Connection pooling handled by Neon's serverless architecture

**Alternatives Considered**:
- Raw SQL: Rejected - Less type safety, more boilerplate
- SQLAlchemy only: Rejected - SQLModel integrates better with FastAPI

### Connection Configuration

```python
# Neon connection string format
DATABASE_URL = "postgresql+asyncpg://{user}:{password}@{host}/{database}?sslmode=require"
```

### Migration Strategy

- Use Alembic for database migrations
- Migrations stored in `backend/alembic/versions/`
- Each migration is reversible

---

## 3. Better Auth Integration

### Decision: Better Auth with JWT plugin for cross-origin authentication

**Rationale**:
- Better Auth is the mandated authentication provider per constitution
- JWT plugin enables stateless authentication for API requests
- Supports email/password authentication out of box
- TypeScript-first but has REST API for Python backend validation

**Alternatives Considered**:
- Custom JWT implementation: Rejected - More code, less tested
- Session-based auth: Rejected - Doesn't work well for separated frontend/backend

### Authentication Flow

```text
1. User submits credentials to Better Auth (Next.js)
2. Better Auth validates and creates session
3. Better Auth issues JWT token
4. Frontend includes JWT in Authorization header
5. FastAPI middleware validates JWT
6. Request proceeds with user context
```

### JWT Validation in FastAPI

- Better Auth exposes JWKS endpoint for public key retrieval
- FastAPI validates JWT signature using public key
- Token claims include user ID for database queries

### Integration Pattern

```text
Frontend (Next.js) ─── Better Auth SDK ─── Better Auth Backend (Next.js API routes)
                                                    │
                                                    ▼
                                              JWT Token issued
                                                    │
                                                    ▼
                             ─── Authorization: Bearer <token> ───
                                                    │
                                                    ▼
                             FastAPI Backend ─── JWT Validation Middleware
                                                    │
                                                    ▼
                                              Protected Resources
```

---

## 4. Next.js 16+ App Router Best Practices

### Decision: Use App Router with Server and Client Components

**Rationale**:
- Next.js 16+ is the mandated frontend framework per constitution
- App Router is the modern standard for Next.js applications
- Server Components reduce client bundle size
- Client Components handle interactivity

**Alternatives Considered**:
- Pages Router: Rejected - Legacy approach
- React SPA: Rejected - Not in approved stack

### Project Structure Pattern

```text
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx       # Root layout with providers
│   │   ├── page.tsx         # Landing/home page
│   │   ├── (auth)/
│   │   │   ├── signin/
│   │   │   │   └── page.tsx
│   │   │   └── signup/
│   │   │       └── page.tsx
│   │   └── (protected)/
│   │       ├── layout.tsx   # Auth-protected layout
│   │       └── dashboard/
│   │           └── page.tsx
│   ├── components/
│   │   ├── ui/              # Reusable UI components
│   │   ├── forms/           # Form components
│   │   └── tasks/           # Task-specific components
│   ├── lib/
│   │   ├── api.ts           # API client with JWT
│   │   ├── auth.ts          # Better Auth client config
│   │   └── utils.ts
│   └── types/
│       └── index.ts
├── public/
├── package.json
├── tailwind.config.js
└── .env.local.example
```

### Key Patterns

1. **Route Groups**: Use `(auth)` and `(protected)` for layout organization
2. **Server Components**: Default for data fetching and static content
3. **Client Components**: Use `"use client"` for interactivity
4. **API Client**: Centralized client that attaches JWT to all requests

---

## 5. API Client and JWT Handling

### Decision: Custom fetch wrapper with automatic JWT attachment

**Rationale**:
- Centralized token management
- Automatic refresh handling (if implemented)
- Consistent error handling
- Type-safe API calls

### Implementation Pattern

```typescript
// lib/api.ts
const apiClient = {
  async fetch(endpoint: string, options?: RequestInit) {
    const token = await getAuthToken(); // From Better Auth
    return fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        ...options?.headers,
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
  }
};
```

---

## 6. Error Handling Strategy

### Decision: Consistent error structure across frontend and backend

**Backend Error Format**:
```json
{
  "detail": "Error message for users",
  "code": "ERROR_CODE",
  "field": "optional_field_name"
}
```

**Frontend Error Handling**:
- Display user-friendly messages from backend
- Handle network errors gracefully
- Show retry options for transient failures

### HTTP Status Code Usage

| Status | Use Case |
|--------|----------|
| 200 | Successful operation |
| 201 | Resource created |
| 400 | Validation error |
| 401 | Not authenticated |
| 403 | Not authorized |
| 404 | Resource not found |
| 422 | Unprocessable entity |
| 500 | Server error |

---

## 7. Testing Strategy

### Backend Testing

- **Framework**: pytest with pytest-asyncio
- **Database**: Use test database or SQLite for unit tests
- **Coverage**: Focus on API endpoints and auth middleware

### Frontend Testing

- **Framework**: Jest with React Testing Library
- **E2E**: Optional Playwright for critical paths
- **Coverage**: Focus on form validation and auth flows

---

## 8. Security Considerations

### Token Storage

- **Decision**: Store JWT in memory (React state) + httpOnly cookie for refresh
- **Rationale**: Prevents XSS access to tokens while enabling persistence

### CORS Configuration

- Restrict origins to frontend domain only
- Explicit allowed methods and headers

### Input Validation

- Backend validates all input with Pydantic
- Frontend validates for UX, backend is authoritative
- Task description: 1-500 characters
- Email: Standard format validation
- Password: Minimum 8 characters

---

## 9. Performance Considerations

### Backend

- Use async database operations
- Connection pooling via Neon
- Pagination for task lists (future consideration)

### Frontend

- Server Components for initial render
- Client-side caching for task list
- Optimistic UI updates

---

## 10. Environment Configuration

### Backend (.env)

```text
DATABASE_URL=postgresql+asyncpg://...
BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=...
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)

```text
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=...
DATABASE_URL=postgresql://...
```

---

## Summary of Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| Backend Framework | FastAPI with async | Mandated, best async support |
| Database ORM | SQLModel | Type-safe, FastAPI integration |
| Database | Neon PostgreSQL | Mandated, serverless |
| Authentication | Better Auth + JWT | Mandated, cross-origin support |
| Frontend Framework | Next.js 16 App Router | Mandated, modern patterns |
| Styling | Tailwind CSS | Constitution stack |
| Token Storage | Memory + httpOnly cookie | Security best practice |
| API Communication | REST with JSON | Simple, well-supported |

---

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Better Auth Documentation](https://better-auth.com/)
- [Next.js App Router](https://nextjs.org/docs/app)
- [Neon PostgreSQL](https://neon.tech/docs)
