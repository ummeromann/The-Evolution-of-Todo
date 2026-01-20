# Tasks: Authentication & Security Integration

**Input**: Design documents from `/specs/002-auth-security-integration/`
**Prerequisites**: plan.md (required), spec.md (required), contracts/jwt-token.md
**Base Implementation**: `001-todo-fullstack-webapp` (already complete)

**Tests**: Manual E2E validation tasks included per spec requirements. No automated test files requested.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/app/` for FastAPI Python code
- **Frontend**: `frontend/src/` for Next.js TypeScript code
- **Specs**: `specs/002-auth-security-integration/` for documentation

---

## Phase 1: Configuration & Secret Management Audit

**Purpose**: Verify secure configuration for JWT secret sharing between frontend and backend

- [x] T001 [P] Verify `BETTER_AUTH_SECRET` present in `backend/.env.example`
- [x] T002 [P] Verify `BETTER_AUTH_SECRET` present in `frontend/.env.local.example`
- [x] T003 [P] Verify `backend/app/config.py` loads `BETTER_AUTH_SECRET` from environment
- [x] T004 Scan codebase for hardcoded secrets using grep (verify zero matches)
- [x] T005 Verify `frontend/src/lib/auth.ts` uses HS256 algorithm for JWT signing
- [x] T006 Verify `backend/app/middleware/auth.py` decodes JWT using HS256 algorithm
- [x] T007 Verify JWT token claims structure matches `contracts/jwt-token.md` (sub, email, iat, exp)
- [x] T008 Update `contracts/jwt-token.md` with any discovered token structure details

**Checkpoint**: Configuration verified, shared secret properly managed (SC-007 validated)

---

## Phase 2: User Story 1 - User Signup (Priority: P1)

**Goal**: New users can create accounts with email/password and receive JWT tokens

**Independent Test**: Navigate to signup page, enter valid credentials, verify redirect to dashboard with authenticated session

**Acceptance Criteria**:
1. Valid email + password (8+ chars) creates account and redirects to dashboard
2. Duplicate email shows "Email already registered" error
3. Invalid email format shows validation error
4. Short password shows validation error

### Signup Validation Enhancement

- [x] T009 [US1] Verify email format validation in `frontend/src/components/forms/signup-form.tsx`
- [x] T010 [US1] Verify password minimum length (8 chars) validation in `frontend/src/components/forms/signup-form.tsx`
- [x] T011 [US1] Add email whitespace trimming before submission in `frontend/src/components/forms/signup-form.tsx`
- [x] T012 [US1] Verify Better Auth handles duplicate email registration with proper error in `frontend/src/lib/auth.ts`

### Error Handling

- [x] T013 [US1] Verify "Email already registered" error message displays correctly in signup form
- [x] T014 [US1] Ensure validation errors are user-friendly (no stack traces exposed) in `frontend/src/components/forms/signup-form.tsx`

### Post-Signup Flow

- [x] T015 [US1] Verify automatic signin after successful signup via Better Auth
- [x] T016 [US1] Verify JWT token issued and stored client-side after signup
- [x] T017 [US1] Verify redirect to `/dashboard` after successful signup in `frontend/src/app/(auth)/signup/page.tsx`

**Checkpoint**: US1 (Signup) complete - users can create accounts (SC-001 validated)

---

## Phase 3: User Story 2 - User Signin (Priority: P1)

**Goal**: Existing users can sign in with credentials and receive JWT tokens

**Independent Test**: Navigate to signin page with valid credentials, verify JWT issuance and dashboard access

**Acceptance Criteria**:
1. Correct email + password authenticates and redirects to dashboard
2. Wrong password shows generic "Invalid credentials" error
3. Non-existent email shows same generic "Invalid credentials" error
4. Already signed-in user redirects to dashboard

### Credential Validation

- [x] T018 [US2] Verify signin accepts valid credentials in `frontend/src/components/forms/signin-form.tsx`
- [x] T019 [US2] Verify generic "Invalid credentials" message for wrong password (security: no field indication)
- [x] T020 [US2] Verify generic "Invalid credentials" message for non-existent email (prevents enumeration)

### Already Authenticated Handling

- [x] T021 [US2] Add auth check to redirect authenticated users from signin page in `frontend/src/app/(auth)/signin/page.tsx`
- [x] T022 [US2] Add auth check to redirect authenticated users from signup page in `frontend/src/app/(auth)/signup/page.tsx`

### Token Issuance

- [x] T023 [US2] Verify JWT token issued on successful signin via Better Auth
- [x] T024 [US2] Verify token contains correct user ID in 'sub' claim
- [x] T025 [US2] Verify token stored in appropriate client storage (cookie or localStorage)

**Checkpoint**: US2 (Signin) complete - users can authenticate (SC-002 validated)

---

## Phase 4: User Story 3 - Protected API Access (Priority: P1)

**Goal**: All API endpoints require valid JWT tokens; proper error responses for invalid/missing tokens

**Independent Test**: Make API requests with valid/invalid/missing tokens, verify appropriate 401/200 responses

**Acceptance Criteria**:
1. Valid JWT token in Authorization header → request succeeds
2. Missing Authorization header → 401 Unauthorized
3. Invalid/malformed JWT → 401 Unauthorized
4. Expired JWT → 401 Unauthorized with expiration indication

### JWT Validation

- [x] T026 [US3] Verify 401 returned for missing Authorization header in `backend/app/middleware/auth.py`
- [x] T027 [US3] Verify 401 returned for malformed Bearer token format
- [x] T028 [US3] Verify 401 returned for invalid JWT signature (wrong secret)
- [x] T029 [US3] Verify 401 returned for expired JWT token with "Token has expired" message

### Token Expiration Handling (Frontend)

- [x] T030 [US3] Add token expiration check before API requests in `frontend/src/lib/api.ts`
- [x] T031 [US3] Implement redirect to signin on token expiration in `frontend/src/lib/api.ts`
- [x] T032 [US3] Add 401 response interception to trigger signin redirect in `frontend/src/lib/api.ts`

### Authorization Header Verification

- [x] T033 [US3] Verify all API requests include Authorization: Bearer header in `frontend/src/lib/api.ts`
- [x] T034 [US3] Verify Bearer token format matches `Authorization: Bearer <token>`
- [x] T035 [US3] Verify token is retrieved from Better Auth session correctly

**Checkpoint**: US3 (Protected API) complete - all routes require valid JWT (SC-003, SC-008 validated)

---

## Phase 5: User Story 4 - User Task Isolation (Priority: P1)

**Goal**: Each user can only access their own tasks; cross-user access blocked with 403

**Independent Test**: Create tasks with User A, attempt access with User B credentials, verify 403 response

**Acceptance Criteria**:
1. User A's task list returns only User A's tasks
2. User B accessing User A's task → 403 Forbidden
3. User B updating User A's task → 403 Forbidden
4. User B deleting User A's task → 403 Forbidden
5. New task automatically associated with authenticated user's ID

### List Tasks Isolation

- [x] T036 [US4] Verify GET /api/tasks filters by authenticated user_id in `backend/app/api/routes/tasks.py`
- [x] T037 [US4] Verify User A cannot see User B's tasks (cross-user list isolation)
- [x] T038 [US4] Verify empty list returned for new user with no tasks

### Create Task Ownership

- [x] T039 [US4] Verify POST /api/tasks sets user_id from JWT token (not request body) in `backend/app/api/routes/tasks.py`
- [x] T040 [US4] Verify task cannot be created for another user (user_id from token only)

### Modify Task Ownership Check

- [x] T041 [US4] Verify PUT /api/tasks/{id} returns 403 for non-owner in `backend/app/api/routes/tasks.py`
- [x] T042 [US4] Verify DELETE /api/tasks/{id} returns 403 for non-owner in `backend/app/api/routes/tasks.py`
- [x] T043 [US4] Verify PATCH /api/tasks/{id}/toggle returns 403 for non-owner in `backend/app/api/routes/tasks.py`
- [x] T044 [US4] Verify 404 returned for non-existent task (before 403 ownership check)

**Checkpoint**: US4 (User Isolation) complete - strict data isolation enforced (SC-004, SC-005 validated)

---

## Phase 6: User Story 5 - User Signout (Priority: P2)

**Goal**: Users can sign out, clearing JWT tokens and redirecting to signin page

**Independent Test**: Sign in, click signout, verify token removed and protected routes inaccessible

**Acceptance Criteria**:
1. Signout removes JWT from client storage
2. Redirect to signin page after signout
3. Protected routes redirect to signin after signout

### Client-Side Cleanup

- [x] T045 [US5] Verify signout removes JWT from client storage via Better Auth
- [x] T046 [US5] Verify Better Auth session is invalidated on signout
- [x] T047 [US5] Verify redirect to signin page after signout in `frontend/src/app/(protected)/layout.tsx`

### Post-Signout Protection

- [x] T048 [US5] Verify protected routes redirect to signin after signout
- [x] T049 [US5] Verify API requests fail with 401 after signout (token no longer sent)
- [x] T050 [US5] Add cache control headers to prevent browser back button exposing protected content

**Checkpoint**: US5 (Signout) complete - secure session termination (SC-006 validated)

---

## Phase 7: End-to-End Validation

**Purpose**: Comprehensive E2E verification of all user stories against acceptance scenarios

### US1: Signup E2E Validation

- [x] T051 [P] E2E: Complete signup with valid email and password (8+ chars), verify dashboard redirect
- [x] T052 [P] E2E: Attempt signup with duplicate email, verify "Email already registered" error
- [x] T053 [P] E2E: Attempt signup with invalid email format, verify validation error
- [x] T054 [P] E2E: Attempt signup with password < 8 chars, verify validation error

### US2: Signin E2E Validation

- [x] T055 [P] E2E: Complete signin with valid credentials, verify dashboard redirect
- [x] T056 [P] E2E: Attempt signin with wrong password, verify "Invalid credentials" error
- [x] T057 [P] E2E: Attempt signin with non-existent email, verify "Invalid credentials" error
- [x] T058 [P] E2E: Navigate to signin while authenticated, verify redirect to dashboard

### US3: Protected API E2E Validation

- [x] T059 E2E: Make authenticated API request, verify 200 success response
- [x] T060 E2E: Make request without Authorization header, verify 401 response
- [x] T061 E2E: Make request with invalid JWT token, verify 401 response
- [x] T062 E2E: Make request with expired JWT token, verify 401 response

### US4: User Isolation E2E Validation

- [x] T063 E2E: Create two users (User A, User B) each with tasks
- [x] T064 E2E: Verify User A only sees their own tasks in list
- [x] T065 E2E: Verify User B only sees their own tasks in list
- [x] T066 E2E: Verify User B accessing User A's task returns 403

### US5: Signout E2E Validation

- [x] T067 E2E: Complete signout flow, verify signin page redirect
- [x] T068 E2E: Attempt to access protected route after signout, verify redirect to signin
- [x] T069 E2E: Verify previous session token no longer works after signout

**Checkpoint**: All acceptance scenarios validated - feature complete

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Configuration Audit ────────────────────┐
                                                 ▼
                         ┌───────────────────────┴───────────────────────┐
                         ▼                                               ▼
Phase 2: US1 Signup (P1)                           Phase 3: US2 Signin (P1)
         │                                                   │
         └───────────────────────┬───────────────────────────┘
                                 ▼
                    Phase 4: US3 Protected API (P1)
                                 │
                                 ▼
                    Phase 5: US4 User Isolation (P1)
                                 │
                                 ▼
                    Phase 6: US5 Signout (P2)
                                 │
                                 ▼
                    Phase 7: E2E Validation
```

### User Story Dependencies

| Story | Depends On | Can Start After |
|-------|------------|-----------------|
| US1 (Signup) | Phase 1 Config Audit | Phase 1 complete |
| US2 (Signin) | Phase 1 Config Audit | Phase 1 complete |
| US3 (Protected API) | US1, US2 | Phase 2 & 3 complete |
| US4 (User Isolation) | US3 | Phase 4 complete |
| US5 (Signout) | US4 | Phase 5 complete |

### Within Each User Story

- Verification tasks before enhancement tasks
- Backend tasks before frontend tasks that depend on them
- Error handling after core functionality
- E2E validation after all implementation

---

## Parallel Opportunities

### Phase 1 (All tasks can run in parallel)

```bash
# These can run in parallel:
T001 [P] Verify backend .env.example
T002 [P] Verify frontend .env.local.example
T003 [P] Verify config.py
```

### Phase 2 & 3 (US1 and US2 can run in parallel)

```bash
# After Phase 1, these stories can proceed in parallel:
US1 (T009-T017) - Signup flow
US2 (T018-T025) - Signin flow
```

### Phase 7 (E2E tests within each story can run in parallel)

```bash
# US1 E2E tests can run in parallel:
T051 [P] Valid signup
T052 [P] Duplicate email
T053 [P] Invalid email format
T054 [P] Short password

# US2 E2E tests can run in parallel:
T055 [P] Valid signin
T056 [P] Wrong password
T057 [P] Non-existent email
T058 [P] Already authenticated
```

---

## Implementation Strategy

### MVP First (Phase 1-4)

1. Complete Phase 1: Configuration Audit
2. Complete Phase 2: US1 Signup (in parallel with Phase 3)
3. Complete Phase 3: US2 Signin (in parallel with Phase 2)
4. Complete Phase 4: US3 Protected API
5. **STOP and VALIDATE**: Basic auth flow complete - MVP READY

### Full Feature Set

6. Complete Phase 5: US4 User Isolation
7. Complete Phase 6: US5 Signout
8. Complete Phase 7: E2E Validation
9. **FINAL VALIDATION**: All 69 tasks complete

---

## Summary

| Phase | User Story | Priority | Tasks | Parallel |
|-------|------------|----------|-------|----------|
| 1 | Configuration Audit | - | T001-T008 (8) | 3 |
| 2 | US1 Signup | P1 | T009-T017 (9) | 0 |
| 3 | US2 Signin | P1 | T018-T025 (8) | 0 |
| 4 | US3 Protected API | P1 | T026-T035 (10) | 0 |
| 5 | US4 User Isolation | P1 | T036-T044 (9) | 0 |
| 6 | US5 Signout | P2 | T045-T050 (6) | 0 |
| 7 | E2E Validation | - | T051-T069 (19) | 8 |
| **Total** | | | **69 tasks** | **11 parallel** |

### Tasks per User Story

| User Story | Tasks | E2E Tasks |
|------------|-------|-----------|
| US1 Signup | 9 | 4 |
| US2 Signin | 8 | 4 |
| US3 Protected API | 10 | 4 |
| US4 User Isolation | 9 | 4 |
| US5 Signout | 6 | 3 |

### Success Criteria Mapping

| SC ID | Description | Validated In |
|-------|-------------|--------------|
| SC-001 | Signup <30s | Phase 2, T017 |
| SC-002 | Signin <15s | Phase 3, T025 |
| SC-003 | 100% invalid token rejection | Phase 4, T026-T029 |
| SC-004 | 100% cross-user block | Phase 5, T041-T043 |
| SC-005 | Zero data leakage | Phase 5, T036-T037 |
| SC-006 | Graceful expiration | Phase 4, T030-T032 |
| SC-007 | Zero hardcoded secrets | Phase 1, T004 |
| SC-008 | 100% JWT attachment | Phase 4, T033-T035 |

---

## Notes

- This feature builds on `001-todo-fullstack-webapp` - most implementation exists
- Focus is on verification, hardening, and edge case handling
- All paths are relative to repository root (`phase-II/`)
- [P] indicates parallelizable tasks within same phase
- [USn] indicates which user story the task belongs to
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
