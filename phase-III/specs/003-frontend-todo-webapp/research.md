# Frontend Research: Todo Web Application

**Feature Branch**: `003-frontend-todo-webapp`
**Date**: 2026-01-15

## Technology Decisions

### Next.js 16+ App Router

**Decision**: Use Next.js 16+ with App Router pattern

**Rationale**:
- Mandated by constitution technology stack
- Server Components for initial page loads and SEO
- Client Components for interactive forms and state management
- Built-in routing with file-system based structure
- Native TypeScript support

**Alternatives Considered**:
- Pages Router (Legacy - not using per constitution)
- React SPA with Vite (Does not meet Next.js requirement)

### Tailwind CSS for Styling

**Decision**: Tailwind CSS utility-first approach

**Rationale**:
- Mandated by specification constraints
- Rapid UI development with utility classes
- Mobile-first responsive design built-in
- No CSS-in-JS runtime overhead
- Consistent design system through configuration

**Alternatives Considered**:
- CSS Modules (Acceptable alternative but Tailwind preferred for speed)
- Material UI / Chakra UI (Explicitly out of scope per specification)

### State Management

**Decision**: React useState/useReducer + Better Auth session state

**Rationale**:
- Simple app with limited global state needs
- Auth state managed by Better Auth client
- Task state local to TaskList component
- Form state local to each form component
- No need for Redux/Zustand complexity

**Alternatives Considered**:
- Redux (Over-engineered for this scope)
- Zustand (Not needed, React hooks sufficient)
- Context API for tasks (Not needed, API fetches fresh data)

### API Communication

**Decision**: Native Fetch API with wrapper utility

**Rationale**:
- Specification allows Fetch or Axios
- Fetch is native, no additional dependency
- Simple wrapper handles JWT attachment and error handling
- AbortController for request cancellation

**Alternatives Considered**:
- Axios (Additional dependency, not needed)
- SWR/React Query (Additional complexity not required for MVP)

### Token Storage

**Decision**: localStorage for development, httpOnly cookies preferred for production

**Rationale**:
- Better Auth handles session storage
- API client retrieves token from Better Auth session
- localStorage accessible for debugging during development
- Note: Constitution warns against localStorage; Better Auth session management handles secure storage

**Alternatives Considered**:
- Session storage (Clears on tab close, poor UX)
- Memory only (Lost on refresh, very poor UX)

---

## Resolved Questions

### Q1: How to handle token expiration?

**Resolution**:
- Frontend API client intercepts 401 responses
- On 401, clear local auth state and redirect to `/signin`
- Better Auth session expiration handled automatically
- No refresh token implementation (out of scope per spec)

### Q2: Component architecture - when to use Client vs Server Components?

**Resolution**:
- **Server Components** (default): Pages, layouts, static content
- **Client Components** (`"use client"`): Forms, buttons with onClick, state-dependent UI, task list with mutations
- Auth-related components must be Client Components for Better Auth hooks

### Q3: Form validation approach?

**Resolution**:
- Client-side validation mirrors backend rules:
  - Email: Valid format (regex pattern)
  - Password: Minimum 8 characters
  - Task description: 1-500 characters, non-empty
- Use native HTML5 validation + custom validation before API calls
- Display inline error messages below fields

### Q4: How to handle loading and error states consistently?

**Resolution**:
- Loading: Use useState `isLoading` boolean per operation
- Skeleton loaders for initial page loads
- Inline spinners for button actions
- Error: Use useState `error` string per component
- Toast-style or inline error messages
- "Retry" option for network failures

### Q5: Route protection implementation?

**Resolution**:
- Protected layout checks Better Auth session
- If no session, redirect to `/signin` using `redirect()` from `next/navigation`
- Auth pages check session and redirect to `/dashboard` if authenticated
- Middleware not used (Better Auth handles auth routes)

---

## Backend API Contract Summary

Based on existing contracts from spec 001 and 002:

### Task Endpoints (Protected)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/tasks` | GET | List all tasks for authenticated user |
| `/api/tasks` | POST | Create new task |
| `/api/tasks/{id}` | GET | Get single task |
| `/api/tasks/{id}` | PUT | Update task description |
| `/api/tasks/{id}` | DELETE | Delete task |
| `/api/tasks/{id}/toggle` | PATCH | Toggle completion status |

### Auth Endpoints (Better Auth)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/auth/sign-up/email` | POST | Register new user |
| `/api/auth/sign-in/email` | POST | Authenticate user |
| `/api/auth/sign-out` | POST | End session |
| `/api/auth/session` | GET | Get current session |

### Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 204 | Deleted (no content) |
| 400 | Validation error |
| 401 | Unauthorized (no/invalid token) |
| 403 | Forbidden (wrong user) |
| 404 | Not found |

---

## File Structure Plan

Based on existing project structure from spec 001:

```text
frontend/src/
├── app/
│   ├── layout.tsx                    # Root layout (exists)
│   ├── page.tsx                      # Landing page (exists)
│   ├── (auth)/
│   │   ├── layout.tsx               # Auth layout (exists)
│   │   ├── signin/page.tsx          # Signin page (exists)
│   │   └── signup/page.tsx          # Signup page (exists)
│   ├── (protected)/
│   │   ├── layout.tsx               # Protected layout (exists)
│   │   ├── dashboard/page.tsx       # Dashboard (enhance)
│   │   └── tasks/page.tsx           # Task list page (NEW)
│   └── api/auth/[...all]/route.ts   # Better Auth routes (exists)
├── components/
│   ├── ui/                          # Base UI components (exists)
│   ├── forms/
│   │   ├── signin-form.tsx          # (exists)
│   │   ├── signup-form.tsx          # (exists)
│   │   └── task-form.tsx            # (exists, enhance)
│   ├── tasks/
│   │   ├── task-list.tsx            # (exists, enhance)
│   │   ├── task-item.tsx            # (exists, enhance)
│   │   └── empty-state.tsx          # (exists)
│   ├── layout/                       # (NEW)
│   │   ├── header.tsx               # Navigation header
│   │   └── nav-menu.tsx             # Navigation links
│   └── common/                       # (NEW)
│       ├── loading-spinner.tsx      # Loading indicator
│       └── error-message.tsx        # Error display
└── lib/
    ├── api.ts                       # API client (exists, enhance)
    ├── auth.ts                      # Better Auth config (exists)
    ├── auth-client.ts               # Better Auth client (exists)
    └── utils.ts                     # Utilities (exists)
```

---

## Risk Mitigation

| Risk | Probability | Mitigation |
|------|-------------|------------|
| Better Auth session retrieval fails | Low | Fallback to localStorage, clear and re-auth |
| Token expires mid-operation | Medium | Intercept 401, redirect with message |
| Backend API unavailable | Low | Show error state with retry button |
| Slow API responses | Medium | Timeouts, loading states, cancel on unmount |
| Mobile viewport layout issues | Medium | Test at 320px breakpoint throughout |

---

## Dependencies

### Runtime Dependencies (existing)

- `better-auth` - Authentication
- `tailwindcss` - Styling
- `next` - Framework

### No Additional Dependencies Needed

Per specification constraints, using native Fetch API and React hooks only.

---

## Success Validation

This plan will be validated against spec success criteria:

- SC-001 to SC-004: Timing benchmarks during E2E testing
- SC-005: Visual testing at 320px, 768px, 1920px
- SC-006-007: Auth flow testing with token checks
- SC-008-011: UX testing for states and validation
- SC-012: All 5 CRUD operations functional
