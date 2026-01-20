# Tasks: Todo Full-Stack Web Application

**Input**: Design documents from `/specs/001-todo-fullstack-webapp/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in specification. Tests are EXCLUDED from this task list.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/app/` for FastAPI Python code
- **Frontend**: `frontend/src/` for Next.js TypeScript code
- **Database**: Alembic migrations in `backend/alembic/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for both backend and frontend

### Backend Setup

- [x] T001 Create backend directory structure: `backend/app/`, `backend/app/models/`, `backend/app/schemas/`, `backend/app/api/`, `backend/app/api/routes/`, `backend/app/middleware/`
- [x] T002 Create `backend/requirements.txt` with FastAPI, SQLModel, asyncpg, pyjwt, python-dotenv, alembic, uvicorn dependencies
- [x] T003 [P] Create `backend/.env.example` with DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS placeholders
- [x] T004 [P] Create `backend/app/__init__.py` as empty package marker
- [x] T005 [P] Create `backend/app/models/__init__.py` as empty package marker
- [x] T006 [P] Create `backend/app/schemas/__init__.py` as empty package marker
- [x] T007 [P] Create `backend/app/api/__init__.py` as empty package marker
- [x] T008 [P] Create `backend/app/api/routes/__init__.py` as empty package marker
- [x] T009 [P] Create `backend/app/middleware/__init__.py` as empty package marker

### Frontend Setup

- [x] T010 Create frontend directory structure: `frontend/src/`, `frontend/src/app/`, `frontend/src/components/`, `frontend/src/lib/`, `frontend/src/types/`
- [x] T011 Initialize Next.js 16+ project with TypeScript in `frontend/` using create-next-app
- [x] T012 Install Tailwind CSS and configure in `frontend/tailwind.config.ts`
- [x] T013 [P] Create `frontend/.env.local.example` with BETTER_AUTH_SECRET, BETTER_AUTH_URL, DATABASE_URL, NEXT_PUBLIC_API_URL placeholders

**Checkpoint**: Project structure ready for implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

### Backend Core Infrastructure

- [x] T014 Create `backend/app/config.py` with Settings class loading environment variables using pydantic-settings
- [x] T015 Create `backend/app/database.py` with async SQLModel engine and session dependency for Neon PostgreSQL
- [x] T016 Initialize Alembic in `backend/` with `alembic init alembic` and configure `backend/alembic/env.py` for async SQLModel

### Data Models (Shared by Multiple Stories)

- [x] T017 Create `backend/app/models/user.py` with User SQLModel class per data-model.md (id, email, hashed_password, created_at, updated_at)
- [x] T018 Create `backend/app/models/task.py` with Task SQLModel class per data-model.md (id, description, is_completed, user_id, created_at, updated_at)
- [x] T019 Update `backend/app/models/__init__.py` to export User and Task models

### Database Migration

- [ ] T020 Generate initial Alembic migration for User and Task tables using `alembic revision --autogenerate -m "Initial schema"`

### Pydantic Schemas

- [x] T021 [P] Create `backend/app/schemas/user.py` with UserCreate, UserResponse, UserLogin schemas per data-model.md
- [x] T022 [P] Create `backend/app/schemas/task.py` with TaskCreate, TaskUpdate, TaskResponse schemas per data-model.md and openapi.yaml
- [x] T023 Update `backend/app/schemas/__init__.py` to export all schemas

### Backend API Foundation

- [x] T024 Create `backend/app/api/deps.py` with get_db async session dependency
- [x] T025 Create `backend/app/api/routes/health.py` with GET /health endpoint returning status and timestamp per openapi.yaml

### Frontend Core Infrastructure

- [x] T026 Create `frontend/src/types/index.ts` with Task and User TypeScript interfaces matching backend schemas
- [x] T027 Create `frontend/src/lib/utils.ts` with cn() classname utility function
- [x] T028 Create `frontend/src/lib/api.ts` with base API client fetch wrapper (without auth initially)

### UI Components (Shared by Multiple Stories)

- [x] T029 [P] Create `frontend/src/components/ui/button.tsx` with Button component using Tailwind CSS (variants: primary, secondary, danger)
- [x] T030 [P] Create `frontend/src/components/ui/input.tsx` with Input component using Tailwind CSS (with label, error state support)
- [x] T031 [P] Create `frontend/src/components/ui/card.tsx` with Card component using Tailwind CSS
- [x] T032 [P] Create `frontend/src/components/ui/spinner.tsx` with loading spinner component using Tailwind CSS

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - User Registration (Priority: P1)

**Goal**: New users can create an account with email and password to access their private task workspace

**Independent Test**: Complete signup flow, verify redirect to dashboard, verify user exists in database

**Acceptance Criteria**:
1. Valid email + password (8+ chars) creates account and redirects to dashboard
2. Duplicate email shows "Email already registered" error
3. Invalid email format or short password shows validation errors

### Better Auth Setup

- [x] T033 [US1] Install Better Auth dependencies in `frontend/`: better-auth, @better-auth/jwt
- [x] T034 [US1] Create `frontend/src/lib/auth.ts` with Better Auth server configuration (email provider, JWT plugin, database adapter)
- [x] T035 [US1] Create `frontend/src/lib/auth-client.ts` with Better Auth client instance for frontend usage
- [x] T036 [US1] Create `frontend/src/app/api/auth/[...all]/route.ts` with Better Auth API route handler

### Frontend Registration UI

- [x] T037 [US1] Create `frontend/src/app/(auth)/layout.tsx` with centered card layout for auth pages
- [x] T038 [US1] Create `frontend/src/components/forms/signup-form.tsx` with email, password fields, validation (email format, password min 8 chars), loading state, error display
- [x] T039 [US1] Create `frontend/src/app/(auth)/signup/page.tsx` with SignupForm component and link to signin

**Checkpoint**: User Story 1 (Registration) complete - users can create accounts

---

## Phase 4: User Story 2 - User Sign-In (Priority: P1)

**Goal**: Registered users can sign in with credentials to access their existing tasks

**Independent Test**: Sign in with valid credentials, verify redirect to dashboard, verify session exists

**Acceptance Criteria**:
1. Correct email + password authenticates and redirects to dashboard
2. Incorrect credentials show "Invalid email or password" error
3. Sign out ends session and redirects to signin page

### JWT Validation Backend

- [x] T040 [US2] Add PyJWT to `backend/requirements.txt` if not already present
- [x] T041 [US2] Create `backend/app/middleware/auth.py` with decode_jwt() function and get_current_user() dependency that extracts user_id from JWT
- [x] T042 [US2] Update `backend/app/api/deps.py` to import and expose get_current_user dependency

### Frontend Sign-In UI

- [x] T043 [US2] Create `frontend/src/components/forms/signin-form.tsx` with email, password fields, validation, loading state, error display
- [x] T044 [US2] Create `frontend/src/app/(auth)/signin/page.tsx` with SigninForm component and link to signup

### Protected Layout

- [x] T045 [US2] Create `frontend/src/app/(protected)/layout.tsx` with session check, redirect to signin if unauthenticated, header with sign-out button
- [x] T046 [US2] Update `frontend/src/lib/api.ts` to automatically attach JWT token from Better Auth session to all API requests

### Sign-Out Functionality

- [x] T047 [US2] Add sign-out handler in protected layout that calls Better Auth signOut and redirects to signin page

**Checkpoint**: User Story 2 (Sign-In) complete - users can authenticate and sign out

---

## Phase 5: User Story 3 - Create Task (Priority: P2)

**Goal**: Authenticated users can create new tasks with descriptions that persist across sessions

**Independent Test**: Create a task, verify it appears in list, sign out and back in, verify task persists

**Acceptance Criteria**:
1. Valid description (1-500 chars) creates task with "pending" status
2. Empty description shows validation error
3. Task persists across sessions

### Backend Create Task API

- [x] T048 [US3] Create `backend/app/api/routes/tasks.py` with POST /api/tasks endpoint per openapi.yaml (requires auth, creates task with user_id from JWT)
- [x] T049 [US3] Update `backend/app/api/routes/__init__.py` to include tasks router

### FastAPI Application Entry

- [x] T050 [US3] Create `backend/app/main.py` with FastAPI app, include health and tasks routers, add CORS middleware with origins from config

### Frontend Create Task UI

- [x] T051 [US3] Create `frontend/src/components/forms/task-form.tsx` with description input (max 500 chars), submit button, validation, loading state
- [x] T052 [US3] Create `frontend/src/app/(protected)/dashboard/page.tsx` with TaskForm component for creating tasks

**Checkpoint**: User Story 3 (Create Task) complete - users can create tasks

---

## Phase 6: User Story 4 - View Tasks (Priority: P2)

**Goal**: Authenticated users can view all their tasks with descriptions and completion status

**Independent Test**: Create multiple tasks, verify all appear in list with correct status, verify other users' tasks are NOT visible

**Acceptance Criteria**:
1. Dashboard shows all user's tasks with descriptions and status
2. Empty state message shown when no tasks exist
3. Only own tasks visible (not other users' tasks)

### Backend List Tasks API

- [x] T053 [US4] Add GET /api/tasks endpoint to `backend/app/api/routes/tasks.py` per openapi.yaml (requires auth, filters by user_id, sorted by created_at DESC)

### Frontend Task List UI

- [x] T054 [US4] Create `frontend/src/components/tasks/empty-state.tsx` with encouraging message to create first task
- [x] T055 [US4] Create `frontend/src/components/tasks/task-item.tsx` with task description display, completion status indicator (visual distinction pending/completed)
- [x] T056 [US4] Create `frontend/src/components/tasks/task-list.tsx` with list of TaskItem components, loading state, empty state
- [x] T057 [US4] Update `frontend/src/app/(protected)/dashboard/page.tsx` to fetch and display TaskList component

**Checkpoint**: User Story 4 (View Tasks) complete - users can see their task list

---

## Phase 7: User Story 5 - Update Task (Priority: P3)

**Goal**: Authenticated users can edit task descriptions to refine details

**Independent Test**: Edit a task description, verify change persists, verify cannot edit other users' tasks

**Acceptance Criteria**:
1. Edited description saves and displays updated text
2. Empty description shows validation error, keeps original
3. Attempting to update another user's task is denied (403)

### Backend Update Task API

- [x] T058 [US5] Add PUT /api/tasks/{task_id} endpoint to `backend/app/api/routes/tasks.py` per openapi.yaml (requires auth, verifies ownership, returns 403 if not owner)

### Frontend Update Task UI

- [x] T059 [US5] Update `frontend/src/components/tasks/task-item.tsx` to add edit mode with inline input, save/cancel buttons
- [x] T060 [US5] Add update task handler to `frontend/src/app/(protected)/dashboard/page.tsx` that calls PUT /api/tasks/{task_id}

**Checkpoint**: User Story 5 (Update Task) complete - users can edit task descriptions

---

## Phase 8: User Story 6 - Delete Task (Priority: P3)

**Goal**: Authenticated users can remove tasks from their list permanently

**Independent Test**: Delete a task, verify it no longer appears, refresh page, verify still gone

**Acceptance Criteria**:
1. Deleted task permanently removed from list
2. Attempting to delete another user's task is denied (403)
3. Deleted task does not reappear on refresh

### Backend Delete Task API

- [x] T061 [US6] Add DELETE /api/tasks/{task_id} endpoint to `backend/app/api/routes/tasks.py` per openapi.yaml (requires auth, verifies ownership, returns 204 on success)

### Frontend Delete Task UI

- [x] T062 [US6] Update `frontend/src/components/tasks/task-item.tsx` to add delete button with confirmation
- [x] T063 [US6] Add delete task handler to `frontend/src/app/(protected)/dashboard/page.tsx` that calls DELETE /api/tasks/{task_id}

**Checkpoint**: User Story 6 (Delete Task) complete - users can delete tasks

---

## Phase 9: User Story 7 - Toggle Task Completion (Priority: P3)

**Goal**: Authenticated users can mark tasks complete or revert to pending status

**Independent Test**: Toggle a task's status, verify visual change, refresh page, verify persists

**Acceptance Criteria**:
1. Pending task can be marked as completed
2. Completed task can be reverted to pending
3. Toggle change persists across page refreshes

### Backend Toggle Task API

- [x] T064 [US7] Add PATCH /api/tasks/{task_id}/toggle endpoint to `backend/app/api/routes/tasks.py` per openapi.yaml (requires auth, verifies ownership, flips is_completed)

### Frontend Toggle Task UI

- [x] T065 [US7] Update `frontend/src/components/tasks/task-item.tsx` to add clickable checkbox/button for toggling completion status
- [x] T066 [US7] Add toggle task handler to `frontend/src/app/(protected)/dashboard/page.tsx` that calls PATCH /api/tasks/{task_id}/toggle

**Checkpoint**: User Story 7 (Toggle Completion) complete - users can track progress

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories, error handling, and final UX polish

### Error Handling

- [x] T067 Add global exception handler in `backend/app/main.py` for consistent 401/403/404/500 error responses
- [x] T068 Update `frontend/src/lib/api.ts` with error handling that displays user-friendly messages for API errors

### Landing Page

- [x] T069 Create `frontend/src/app/layout.tsx` root layout with html, body, global styles, font configuration
- [x] T070 Create `frontend/src/app/page.tsx` landing page with app title, description, links to signin/signup

### Loading States

- [x] T071 Add loading states to all data operations in `frontend/src/app/(protected)/dashboard/page.tsx` using Spinner component

### Form Validation

- [x] T072 Add client-side validation for all forms: email format, password min 8 chars, description 1-500 chars

### Responsive Design

- [x] T073 Apply mobile-first responsive styles to all components using Tailwind CSS breakpoints (sm, md, lg)
- [x] T074 Verify layout works on 320px viewport (mobile)
- [x] T075 Verify layout works on 1920px viewport (desktop)

### Database Migration Execution

- [ ] T076 Run Alembic migration with `alembic upgrade head` to create database tables

### Final Validation

- [ ] T077 Verify complete signup flow end-to-end
- [ ] T078 Verify complete signin flow end-to-end
- [ ] T079 Verify complete signout flow end-to-end
- [ ] T080 Verify create task end-to-end
- [ ] T081 Verify view tasks with user isolation
- [ ] T082 Verify update task end-to-end
- [ ] T083 Verify delete task end-to-end
- [ ] T084 Verify toggle task completion end-to-end

**Checkpoint**: All features complete and validated

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup ─────────────────┐
                                ▼
Phase 2: Foundational ──────────┤ BLOCKS ALL USER STORIES
                                ▼
                    ┌───────────┴───────────┐
                    ▼                       ▼
Phase 3: US1 Registration      Phase 4: US2 Sign-In
(Better Auth Setup)            (JWT Validation)
        │                              │
        └──────────────┬───────────────┘
                       ▼
           ┌───────────┴───────────┐
           ▼                       ▼
Phase 5: US3 Create Task    Phase 6: US4 View Tasks
           │                       │
           └───────────┬───────────┘
                       ▼
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
Phase 7: US5       Phase 8: US6    Phase 9: US7
Update Task        Delete Task     Toggle Task
        │              │              │
        └──────────────┴──────────────┘
                       ▼
            Phase 10: Polish
```

### User Story Dependencies

| Story | Depends On | Can Start After |
|-------|------------|-----------------|
| US1 (Registration) | Foundational | Phase 2 complete |
| US2 (Sign-In) | US1 (Better Auth must exist) | Phase 3 complete |
| US3 (Create Task) | US2 (needs auth) | Phase 4 complete |
| US4 (View Tasks) | US3 (needs tasks endpoint) | Phase 5 complete |
| US5 (Update Task) | US4 (needs task display) | Phase 6 complete |
| US6 (Delete Task) | US4 (needs task display) | Phase 6 complete |
| US7 (Toggle Task) | US4 (needs task display) | Phase 6 complete |

### Within Each Phase

- Tasks marked [P] can run in parallel (different files)
- Sequential tasks must complete in order
- Backend API endpoints before frontend UI that uses them

---

## Parallel Opportunities

### Phase 1 Setup (After T001-T002)

```bash
# These can run in parallel:
T003 [P] .env.example
T004 [P] app/__init__.py
T005 [P] models/__init__.py
T006 [P] schemas/__init__.py
T007 [P] api/__init__.py
T008 [P] routes/__init__.py
T009 [P] middleware/__init__.py
T013 [P] frontend .env.local.example
```

### Phase 2 Foundational (After T016)

```bash
# These can run in parallel:
T021 [P] schemas/user.py
T022 [P] schemas/task.py
T029 [P] button.tsx
T030 [P] input.tsx
T031 [P] card.tsx
T032 [P] spinner.tsx
```

### Phases 7-9 (After Phase 6)

```bash
# These user stories can run in parallel:
Phase 7: US5 Update Task (T058-T060)
Phase 8: US6 Delete Task (T061-T063)
Phase 9: US7 Toggle Task (T064-T066)
```

---

## Implementation Strategy

### MVP First (User Stories 1-4)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: US1 Registration
4. Complete Phase 4: US2 Sign-In
5. **STOP and VALIDATE**: Test registration and signin independently
6. Complete Phase 5: US3 Create Task
7. Complete Phase 6: US4 View Tasks
8. **STOP and VALIDATE**: Users can create and view tasks - MVP COMPLETE

### Full Feature Set

9. Complete Phase 7: US5 Update Task
10. Complete Phase 8: US6 Delete Task
11. Complete Phase 9: US7 Toggle Task
12. Complete Phase 10: Polish
13. **FINAL VALIDATION**: All 84 tasks complete

---

## Summary

| Phase | User Story | Priority | Tasks | Parallel |
|-------|------------|----------|-------|----------|
| 1 | Setup | - | T001-T013 (13) | 9 |
| 2 | Foundational | - | T014-T032 (19) | 6 |
| 3 | US1 Registration | P1 | T033-T039 (7) | 0 |
| 4 | US2 Sign-In | P1 | T040-T047 (8) | 0 |
| 5 | US3 Create Task | P2 | T048-T052 (5) | 0 |
| 6 | US4 View Tasks | P2 | T053-T057 (5) | 0 |
| 7 | US5 Update Task | P3 | T058-T060 (3) | 0 |
| 8 | US6 Delete Task | P3 | T061-T063 (3) | 0 |
| 9 | US7 Toggle Task | P3 | T064-T066 (3) | 0 |
| 10 | Polish | - | T067-T084 (18) | 2 |
| **Total** | | | **84 tasks** | **17 parallel** |

### Tasks per User Story

| User Story | Tasks |
|------------|-------|
| US1 Registration | 7 |
| US2 Sign-In | 8 |
| US3 Create Task | 5 |
| US4 View Tasks | 5 |
| US5 Update Task | 3 |
| US6 Delete Task | 3 |
| US7 Toggle Task | 3 |

### MVP Scope

**Suggested MVP**: Complete through Phase 6 (US4 View Tasks)
- Tasks: T001-T057 (57 tasks)
- Delivers: Registration, Sign-In, Create Task, View Tasks
- Enables: Basic task management workflow

---

## Notes

- All paths are relative to repository root (`phase-II/`)
- Backend uses `backend/app/` structure
- Frontend uses `frontend/src/` structure
- [P] indicates parallelizable tasks within same phase
- [USn] indicates which user story the task belongs to
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
