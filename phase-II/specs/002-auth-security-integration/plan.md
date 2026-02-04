# Implementation Plan: Authentication & Security Integration

**Branch**: `002-auth-security-integration` | **Date**: 2026-01-14 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-auth-security-integration/spec.md`
**Prerequisite**: Phase 1 implementation from `001-todo-fullstack-webapp` complete

## Summary

Enhance and harden the existing authentication system to fully implement:
- Secure user signup/signin with Better Auth
- JWT-based authentication for frontend-backend communication
- Strict user isolation in all backend operations
- Comprehensive error handling for auth failures

This feature builds on the foundation established in `001-todo-fullstack-webapp` and focuses on security hardening, edge case handling, and validation of the complete auth flow.

## Technical Context

**Language/Version**: Python 3.11+ (Backend), TypeScript/Node.js 18+ (Frontend)
**Primary Dependencies**: Better Auth, PyJWT, FastAPI, Next.js 16+
**Authentication**: Better Auth with JWT tokens (HS256)
**Storage**: Neon Serverless PostgreSQL (users stored by Better Auth)
**Testing**: Manual E2E validation, pytest (Backend), Jest (Frontend)
**Security Goals**: Zero hardcoded secrets, strict user isolation, proper error responses

## Constitution Check

*GATE: Must pass before implementation. Re-checked after design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | PASS | This plan derived from approved spec.md |
| II. Zero Manual Coding | PASS | All implementation via Claude Code agents |
| III. Security by Design | PASS | JWT validation, user isolation, env-based secrets |
| IV. Single Source of Truth | PASS | spec.md authoritative |
| V. Clean Separation of Concerns | PASS | Frontend auth, Backend validation, DB persistence |
| VI. Reproducibility | PASS | Full plan documented, PHR records maintained |

## Current Implementation Status

Based on `001-todo-fullstack-webapp` tasks completion:

### Already Implemented (from Phase 1)
- [x] Better Auth configuration (`frontend/src/lib/auth.ts`)
- [x] Better Auth client (`frontend/src/lib/auth-client.ts`)
- [x] Auth API route handler (`frontend/src/app/api/auth/[...all]/route.ts`)
- [x] JWT validation middleware (`backend/app/middleware/auth.py`)
- [x] get_current_user dependency (`backend/app/api/deps.py`)
- [x] User isolation in task queries (`backend/app/api/routes/tasks.py`)
- [x] Signup form and page (`frontend/src/components/forms/signup-form.tsx`)
- [x] Signin form and page (`frontend/src/components/forms/signin-form.tsx`)
- [x] Protected layout with auth check (`frontend/src/app/(protected)/layout.tsx`)
- [x] API client with JWT attachment (`frontend/src/lib/api.ts`)
- [x] Sign-out functionality

### Gaps to Address (this feature)
- [ ] JWT shared secret configuration verification
- [ ] Token expiration handling (frontend redirect)
- [ ] Comprehensive error message consistency
- [ ] Edge case handling (whitespace trimming, concurrent registration)
- [ ] Security audit of existing implementation
- [ ] End-to-end validation testing

---

## Implementation Phases

### Phase 1: Configuration & Secret Management Audit

**Agent**: `auth-security`
**Dependencies**: None
**Output**: Verified secure configuration for JWT secret sharing

#### 1.1 Environment Configuration Review

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 1.1.1 | Verify `BETTER_AUTH_SECRET` present in `backend/.env.example` | auth-security | None |
| 1.1.2 | Verify `BETTER_AUTH_SECRET` present in `frontend/.env.local.example` | auth-security | None |
| 1.1.3 | Verify `backend/app/config.py` loads `BETTER_AUTH_SECRET` | auth-security | None |
| 1.1.4 | Verify no hardcoded secrets in codebase using grep | auth-security | None |

#### 1.2 JWT Configuration Alignment

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 1.2.1 | Verify Better Auth uses HS256 algorithm for JWT signing | auth-security | 1.1 |
| 1.2.2 | Verify FastAPI JWT decoder uses HS256 algorithm | auth-security | 1.1 |
| 1.2.3 | Verify JWT token claims include required fields (sub, email, iat, exp) | auth-security | 1.2.2 |
| 1.2.4 | Document expected token structure in `contracts/jwt-token.md` | auth-security | 1.2.3 |

**Checkpoint**: Configuration verified, shared secret properly managed

---

### Phase 2: Signup Flow Hardening

**Agent**: `auth-security`, `nextjs-frontend-builder`
**Dependencies**: Phase 1 complete
**Output**: Robust signup flow with proper validation and error handling

#### 2.1 Input Validation Enhancement

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 2.1.1 | Verify email validation (format check) in signup form | nextjs-frontend-builder | Phase 1 |
| 2.1.2 | Verify password validation (min 8 chars) in signup form | nextjs-frontend-builder | Phase 1 |
| 2.1.3 | Add email whitespace trimming before submission | nextjs-frontend-builder | 2.1.1 |
| 2.1.4 | Verify Better Auth handles duplicate email registration | auth-security | 2.1.3 |

#### 2.2 Error Message Consistency

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 2.2.1 | Verify "Email already registered" error for duplicate emails | auth-security | 2.1.4 |
| 2.2.2 | Verify validation errors display correctly in form | nextjs-frontend-builder | 2.2.1 |
| 2.2.3 | Ensure error messages are user-friendly (no stack traces) | nextjs-frontend-builder | 2.2.2 |

#### 2.3 Post-Signup Flow

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 2.3.1 | Verify automatic signin after successful signup | auth-security | 2.2 |
| 2.3.2 | Verify JWT token issued and stored client-side | auth-security | 2.3.1 |
| 2.3.3 | Verify redirect to dashboard after signup | nextjs-frontend-builder | 2.3.2 |

**Checkpoint**: Signup flow complete with all edge cases handled

---

### Phase 3: Signin Flow Hardening

**Agent**: `auth-security`, `nextjs-frontend-builder`
**Dependencies**: Phase 2 complete
**Output**: Secure signin flow with consistent error handling

#### 3.1 Credential Validation

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 3.1.1 | Verify signin accepts valid credentials | auth-security | Phase 2 |
| 3.1.2 | Verify generic "Invalid credentials" for wrong password | auth-security | 3.1.1 |
| 3.1.3 | Verify generic "Invalid credentials" for non-existent email | auth-security | 3.1.1 |
| 3.1.4 | Verify no timing attacks (consistent response time) | auth-security | 3.1.3 |

#### 3.2 Already Authenticated Handling

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 3.2.1 | Verify redirect to dashboard if already signed in | nextjs-frontend-builder | 3.1 |
| 3.2.2 | Add auth check to signin page server component | nextjs-frontend-builder | 3.2.1 |
| 3.2.3 | Add auth check to signup page server component | nextjs-frontend-builder | 3.2.1 |

#### 3.3 Token Issuance

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 3.3.1 | Verify JWT token issued on successful signin | auth-security | 3.2 |
| 3.3.2 | Verify token contains correct user ID in 'sub' claim | auth-security | 3.3.1 |
| 3.3.3 | Verify token stored in appropriate client storage | auth-security | 3.3.2 |

**Checkpoint**: Signin flow complete with security best practices

---

### Phase 4: Protected API Access

**Agent**: `auth-security`, `fastapi-backend`
**Dependencies**: Phase 3 complete
**Output**: All API routes properly protected with JWT validation

#### 4.1 JWT Validation Verification

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 4.1.1 | Verify 401 returned for missing Authorization header | auth-security | Phase 3 |
| 4.1.2 | Verify 401 returned for malformed Bearer token | auth-security | 4.1.1 |
| 4.1.3 | Verify 401 returned for invalid JWT signature | auth-security | 4.1.1 |
| 4.1.4 | Verify 401 returned for expired JWT token | auth-security | 4.1.1 |

#### 4.2 Token Expiration Handling

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 4.2.1 | Add token expiration check in frontend API client | nextjs-frontend-builder | 4.1 |
| 4.2.2 | Implement redirect to signin on token expiration | nextjs-frontend-builder | 4.2.1 |
| 4.2.3 | Add 401 response interception in API client | nextjs-frontend-builder | 4.2.2 |

#### 4.3 Authorization Header Attachment

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 4.3.1 | Verify all API requests include Authorization header | nextjs-frontend-builder | 4.2 |
| 4.3.2 | Verify Bearer token format is correct | auth-security | 4.3.1 |
| 4.3.3 | Verify token is retrieved from Better Auth session | auth-security | 4.3.2 |

**Checkpoint**: All protected routes require valid JWT

---

### Phase 5: User Task Isolation

**Agent**: `auth-security`, `fastapi-backend`
**Dependencies**: Phase 4 complete
**Output**: Complete data isolation between users

#### 5.1 List Tasks Isolation

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 5.1.1 | Verify GET /api/tasks filters by authenticated user_id | auth-security | Phase 4 |
| 5.1.2 | Verify User A cannot see User B's tasks | auth-security | 5.1.1 |
| 5.1.3 | Verify empty list returned for new user | auth-security | 5.1.1 |

#### 5.2 Create Task Ownership

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 5.2.1 | Verify POST /api/tasks sets user_id from JWT | auth-security | 5.1 |
| 5.2.2 | Verify task cannot be created for another user | auth-security | 5.2.1 |
| 5.2.3 | Verify user_id is extracted from token, not request body | auth-security | 5.2.2 |

#### 5.3 Modify Task Ownership Check

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 5.3.1 | Verify PUT /api/tasks/{id} returns 403 for non-owner | auth-security | 5.2 |
| 5.3.2 | Verify DELETE /api/tasks/{id} returns 403 for non-owner | auth-security | 5.2 |
| 5.3.3 | Verify PATCH /api/tasks/{id}/toggle returns 403 for non-owner | auth-security | 5.2 |
| 5.3.4 | Verify 404 returned before 403 (task existence check) | auth-security | 5.3.3 |

**Checkpoint**: User isolation verified for all operations

---

### Phase 6: Signout Flow

**Agent**: `auth-security`, `nextjs-frontend-builder`
**Dependencies**: Phase 5 complete
**Output**: Secure signout with proper cleanup

#### 6.1 Client-Side Cleanup

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 6.1.1 | Verify signout removes JWT from client storage | auth-security | Phase 5 |
| 6.1.2 | Verify Better Auth session is invalidated | auth-security | 6.1.1 |
| 6.1.3 | Verify redirect to signin page after signout | nextjs-frontend-builder | 6.1.2 |

#### 6.2 Post-Signout Protection

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 6.2.1 | Verify protected routes redirect to signin after signout | nextjs-frontend-builder | 6.1 |
| 6.2.2 | Verify API requests fail with 401 after signout | auth-security | 6.1 |
| 6.2.3 | Verify browser back button doesn't expose protected content | nextjs-frontend-builder | 6.2.2 |

**Checkpoint**: Signout securely ends session

---

### Phase 7: End-to-End Validation

**Agent**: `auth-security`
**Dependencies**: Phase 6 complete
**Output**: Full E2E verification of all acceptance scenarios

#### 7.1 User Story 1: Signup Validation

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 7.1.1 | E2E: Complete signup with valid credentials | auth-security | Phase 6 |
| 7.1.2 | E2E: Verify duplicate email rejection | auth-security | 7.1.1 |
| 7.1.3 | E2E: Verify invalid email format rejection | auth-security | 7.1.1 |
| 7.1.4 | E2E: Verify short password rejection | auth-security | 7.1.1 |

#### 7.2 User Story 2: Signin Validation

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 7.2.1 | E2E: Complete signin with valid credentials | auth-security | 7.1 |
| 7.2.2 | E2E: Verify wrong password rejection | auth-security | 7.2.1 |
| 7.2.3 | E2E: Verify non-existent email rejection | auth-security | 7.2.1 |
| 7.2.4 | E2E: Verify already-authenticated redirect | auth-security | 7.2.1 |

#### 7.3 User Story 3: Protected API Validation

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 7.3.1 | E2E: Verify authenticated request succeeds | auth-security | 7.2 |
| 7.3.2 | E2E: Verify unauthenticated request returns 401 | auth-security | 7.3.1 |
| 7.3.3 | E2E: Verify invalid token request returns 401 | auth-security | 7.3.1 |
| 7.3.4 | E2E: Verify expired token request returns 401 | auth-security | 7.3.1 |

#### 7.4 User Story 4: User Isolation Validation

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 7.4.1 | E2E: Create two users with separate tasks | auth-security | 7.3 |
| 7.4.2 | E2E: Verify User A only sees their tasks | auth-security | 7.4.1 |
| 7.4.3 | E2E: Verify User B only sees their tasks | auth-security | 7.4.1 |
| 7.4.4 | E2E: Verify cross-user access returns 403 | auth-security | 7.4.1 |

#### 7.5 User Story 5: Signout Validation

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 7.5.1 | E2E: Complete signout flow | auth-security | 7.4 |
| 7.5.2 | E2E: Verify redirect to signin after signout | auth-security | 7.5.1 |
| 7.5.3 | E2E: Verify protected route access denied | auth-security | 7.5.1 |

**Checkpoint**: All acceptance scenarios validated

---

## Task Summary

| Phase | Tasks | Agent Assignments |
|-------|-------|-------------------|
| Phase 1: Configuration Audit | 8 | auth-security |
| Phase 2: Signup Hardening | 9 | auth-security, nextjs-frontend-builder |
| Phase 3: Signin Hardening | 9 | auth-security, nextjs-frontend-builder |
| Phase 4: Protected API Access | 9 | auth-security, fastapi-backend, nextjs-frontend-builder |
| Phase 5: User Isolation | 10 | auth-security, fastapi-backend |
| Phase 6: Signout Flow | 6 | auth-security, nextjs-frontend-builder |
| Phase 7: E2E Validation | 17 | auth-security |
| **Total** | **68** | |

---

## Risk Analysis

| Risk | Mitigation |
|------|------------|
| Better Auth session/JWT format mismatch | Verify token structure in Phase 1 |
| Shared secret not matching between frontend/backend | Configuration audit in Phase 1 |
| Token expiration edge cases | Implement redirect flow in Phase 4 |
| Race condition in concurrent registration | Better Auth handles at DB level |
| Browser caching exposing protected content | Add cache headers in Phase 6 |

---

## Success Criteria Mapping

| Success Criterion | Phase | Validation Step |
|-------------------|-------|-----------------|
| SC-001: Signup <30s | Phase 7 | 7.1.1 |
| SC-002: Signin <15s | Phase 7 | 7.2.1 |
| SC-003: 100% reject invalid tokens | Phase 7 | 7.3.2-7.3.4 |
| SC-004: 100% block cross-user access | Phase 7 | 7.4.4 |
| SC-005: Zero cross-user data leakage | Phase 7 | 7.4.1-7.4.3 |
| SC-006: Graceful expiration redirect | Phase 4 | 4.2.2 |
| SC-007: Zero hardcoded secrets | Phase 1 | 1.1.4 |
| SC-008: 100% JWT attachment | Phase 4 | 4.3.1 |

---

## Generated Artifacts

| Artifact | Path | Purpose |
|----------|------|---------|
| spec.md | specs/002-auth-security-integration/spec.md | Feature requirements |
| plan.md | specs/002-auth-security-integration/plan.md | This implementation plan |
| jwt-token.md | specs/002-auth-security-integration/contracts/jwt-token.md | JWT token structure |
| requirements.md | specs/002-auth-security-integration/checklists/requirements.md | Requirements checklist |

---

## Next Steps

1. Run `/sp.tasks` to generate detailed task list from this plan
2. Run `/sp.implement` to begin Phase 1 implementation
3. Each phase validated before proceeding to next
4. Create PHR after implementation completes

---

## Implementation Notes

### Better Auth JWT Integration

Better Auth creates sessions and tokens. The FastAPI backend validates these tokens using the shared secret. Key integration points:

1. **Frontend**: Better Auth handles signup/signin, issues JWT tokens
2. **API Client**: Extracts token from Better Auth session, attaches to requests
3. **Backend**: PyJWT validates token signature, extracts user ID
4. **Task Routes**: Use user ID from token to filter/validate ownership

### Security Considerations

1. **No refresh tokens**: Simple JWT with reasonable expiration (7 days)
2. **Consistent errors**: Generic "Invalid credentials" prevents enumeration
3. **User isolation**: Every query includes user_id filter
4. **403 vs 404**: Return 404 if task doesn't exist, 403 if wrong owner
