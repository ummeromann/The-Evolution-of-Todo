# Tasks: Frontend Web Application - Todo Web App

**Input**: Design documents from `/specs/003-frontend-todo-webapp/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/frontend-api-client.md
**Agent**: `nextjs-frontend-builder`

**Tests**: Manual E2E validation only (no automated tests requested)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US10)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/src/` (Next.js App Router structure)
- All paths relative to repository root

---

## Phase 1: Setup (Foundation Types & Utilities)

**Purpose**: TypeScript types and enhanced API client - foundational for all user stories

- [ ] T001 [P] Create Task type interfaces in frontend/src/types/task.ts
- [ ] T002 [P] Create User and Session type interfaces in frontend/src/types/auth.ts
- [ ] T003 [P] Create ApiResponse and ApiError type interfaces in frontend/src/types/api.ts
- [ ] T004 [P] Create form state interfaces in frontend/src/types/forms.ts
- [ ] T005 Update frontend/src/types/index.ts to export all type modules

---

## Phase 2: Foundational (API Client & Common Components)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 Enhance frontend/src/lib/api.ts with proper TypeScript types from Phase 1
- [ ] T007 Add request timeout handling (30s) to frontend/src/lib/api.ts
- [ ] T008 Add 401 response interception with redirect to signin in frontend/src/lib/api.ts
- [ ] T009 Add comprehensive error response parsing to frontend/src/lib/api.ts
- [ ] T010 Add taskApi object with list/get/create/update/delete/toggle methods in frontend/src/lib/api.ts
- [ ] T011 [P] Create LoadingSpinner component in frontend/src/components/common/loading-spinner.tsx
- [ ] T012 [P] Create ErrorMessage component with retry button in frontend/src/components/common/error-message.tsx
- [ ] T013 [P] Create ConfirmDialog component in frontend/src/components/common/confirm-dialog.tsx

**Checkpoint**: Foundation ready - API client enhanced, common components available

---

## Phase 3: User Story 1 - User Signup Page (Priority: P1)

**Goal**: New visitors can create an account and access the Todo application

**Independent Test**: Navigate to `/signup`, enter valid email/password, verify redirect to dashboard

### Implementation for User Story 1

- [ ] T014 [US1] Enhance signup-form.tsx with email format validation in frontend/src/components/forms/signup-form.tsx
- [ ] T015 [US1] Add password length validation (min 8 chars) to frontend/src/components/forms/signup-form.tsx
- [ ] T016 [US1] Add loading state during form submission to frontend/src/components/forms/signup-form.tsx
- [ ] T017 [US1] Add API error display (duplicate email, etc.) to frontend/src/components/forms/signup-form.tsx
- [ ] T018 [US1] Add redirect to dashboard on successful signup in frontend/src/components/forms/signup-form.tsx

**Checkpoint**: User Story 1 complete - signup flow fully functional

---

## Phase 4: User Story 2 - User Signin Page (Priority: P1)

**Goal**: Returning users can sign in to access their existing tasks

**Independent Test**: Navigate to `/signin`, enter valid credentials, verify redirect to dashboard

### Implementation for User Story 2

- [ ] T019 [US2] Enhance signin-form.tsx with email/password validation in frontend/src/components/forms/signin-form.tsx
- [ ] T020 [US2] Add loading state during form submission to frontend/src/components/forms/signin-form.tsx
- [ ] T021 [US2] Add generic error display for invalid credentials in frontend/src/components/forms/signin-form.tsx
- [ ] T022 [US2] Add redirect to dashboard on successful signin in frontend/src/components/forms/signin-form.tsx
- [ ] T023 [US2] Update auth layout to check if already authenticated in frontend/src/app/(auth)/layout.tsx
- [ ] T024 [US2] Redirect authenticated users from signin/signup to dashboard in frontend/src/app/(auth)/layout.tsx
- [ ] T025 [US2] Handle session_expired query param on signin page in frontend/src/app/(auth)/signin/page.tsx

**Checkpoint**: User Story 2 complete - signin flow fully functional

---

## Phase 5: User Story 3 - Dashboard Landing Page (Priority: P1)

**Goal**: Authenticated users see a dashboard with task summary and quick actions

**Independent Test**: Sign in and verify dashboard displays welcome message, task counts, and navigation

### Implementation for User Story 3

- [ ] T026 [P] [US3] Create Header component with logo and nav in frontend/src/components/layout/header.tsx
- [ ] T027 [P] [US3] Create NavMenu component for mobile menu in frontend/src/components/layout/nav-menu.tsx
- [ ] T028 [US3] Add signout button to Header component in frontend/src/components/layout/header.tsx
- [ ] T029 [US3] Implement mobile hamburger menu toggle in frontend/src/components/layout/header.tsx
- [ ] T030 [US3] Update root layout with proper meta tags in frontend/src/app/layout.tsx
- [ ] T031 [US3] Update landing page with CTA buttons in frontend/src/app/page.tsx
- [ ] T032 [US3] Update protected layout with Header component in frontend/src/app/(protected)/layout.tsx
- [ ] T033 [US3] Add navigation links (Dashboard, Tasks) to protected layout in frontend/src/app/(protected)/layout.tsx
- [ ] T034 [P] [US3] Create TaskStats component in frontend/src/components/dashboard/task-stats.tsx
- [ ] T035 [US3] Display total, completed, pending task counts in TaskStats component
- [ ] T036 [US3] Create/update dashboard page in frontend/src/app/(protected)/dashboard/page.tsx
- [ ] T037 [US3] Add welcome message with user email to dashboard page
- [ ] T038 [US3] Add task statistics display to dashboard page
- [ ] T039 [US3] Add "View Tasks" and "Create Task" CTA buttons to dashboard page
- [ ] T040 [US3] Add loading state while fetching task data on dashboard
- [ ] T041 [US3] Add empty state for new users (no tasks) on dashboard

**Checkpoint**: User Story 3 complete - dashboard with navigation fully functional

---

## Phase 6: User Story 4 - Task List View (Priority: P1)

**Goal**: Authenticated users can view all their tasks with status indicators

**Independent Test**: Navigate to task list page, verify all tasks displayed with correct status

### Implementation for User Story 4

- [ ] T042 [US4] Create tasks page structure in frontend/src/app/(protected)/tasks/page.tsx
- [ ] T043 [US4] Add page title and "Create Task" button to tasks page
- [ ] T044 [US4] Update task-list.tsx to fetch tasks from API in frontend/src/components/tasks/task-list.tsx
- [ ] T045 [US4] Add loading spinner while fetching tasks in frontend/src/components/tasks/task-list.tsx
- [ ] T046 [US4] Add error message with retry button for task fetch failures
- [ ] T047 [US4] Add empty state when no tasks exist in frontend/src/components/tasks/task-list.tsx
- [ ] T048 [US4] Update task-item.tsx with completion checkbox in frontend/src/components/tasks/task-item.tsx
- [ ] T049 [US4] Add visual distinction for completed tasks (strikethrough) in frontend/src/components/tasks/task-item.tsx
- [ ] T050 [US4] Add Edit and Delete action buttons to task-item.tsx

**Checkpoint**: User Story 4 complete - task list view with status indicators functional

---

## Phase 7: User Story 5 - Create New Task (Priority: P2)

**Goal**: Authenticated users can create new tasks with validation

**Independent Test**: Click "Create Task", enter description, verify task appears in list

### Implementation for User Story 5

- [ ] T051 [US5] Update task-form.tsx to support create mode in frontend/src/components/forms/task-form.tsx
- [ ] T052 [US5] Add description textarea with character counter to task-form.tsx
- [ ] T053 [US5] Add validation (1-500 characters, non-empty) to task-form.tsx
- [ ] T054 [US5] Add loading state during task creation submission
- [ ] T055 [US5] Add error message display for task creation failures
- [ ] T056 [US5] Add create task modal/section to tasks page in frontend/src/app/(protected)/tasks/page.tsx
- [ ] T057 [US5] Implement taskApi.create call on form submit
- [ ] T058 [US5] Add new task to list on successful creation
- [ ] T059 [US5] Close modal/clear form on successful task creation

**Checkpoint**: User Story 5 complete - task creation fully functional

---

## Phase 8: User Story 6 - Edit Existing Task (Priority: P2)

**Goal**: Authenticated users can modify existing task descriptions

**Independent Test**: Click edit on a task, modify description, verify change persists

### Implementation for User Story 6

- [ ] T060 [US6] Update task-form.tsx to support edit mode in frontend/src/components/forms/task-form.tsx
- [ ] T061 [US6] Pre-populate form with existing task description in edit mode
- [ ] T062 [US6] Add Cancel button to discard changes in task-form.tsx
- [ ] T063 [US6] Apply same validation rules for edit as create mode
- [ ] T064 [US6] Add edit modal state management to tasks page
- [ ] T065 [US6] Open edit modal with task data when Edit button clicked
- [ ] T066 [US6] Implement taskApi.update call on edit form submit
- [ ] T067 [US6] Update task in list on successful edit
- [ ] T068 [US6] Close edit modal on success or cancel

**Checkpoint**: User Story 6 complete - task editing fully functional

---

## Phase 9: User Story 7 - Delete Task (Priority: P2)

**Goal**: Authenticated users can delete tasks with confirmation

**Independent Test**: Click delete on a task, confirm, verify task removed from list

### Implementation for User Story 7

- [ ] T069 [US7] Integrate ConfirmDialog component for delete in tasks page
- [ ] T070 [US7] Show delete confirmation dialog when Delete button clicked
- [ ] T071 [US7] Add loading state to confirm button during deletion
- [ ] T072 [US7] Implement taskApi.delete call on confirm
- [ ] T073 [US7] Remove task from list on successful deletion
- [ ] T074 [US7] Close dialog on success or cancel
- [ ] T075 [US7] Display error message if deletion fails

**Checkpoint**: User Story 7 complete - task deletion with confirmation functional

---

## Phase 10: User Story 8 - Toggle Task Completion (Priority: P2)

**Goal**: Authenticated users can toggle task completion status with optimistic updates

**Independent Test**: Click toggle on a task, verify status changes and persists on refresh

### Implementation for User Story 8

- [ ] T076 [US8] Add onClick handler to completion checkbox in task-item.tsx
- [ ] T077 [US8] Implement optimistic UI update (toggle status immediately)
- [ ] T078 [US8] Call taskApi.toggle on checkbox click
- [ ] T079 [US8] Revert UI if API call fails with error message
- [ ] T080 [US8] Add subtle loading indicator during toggle operation
- [ ] T081 [US8] Pass toggle handler from task-list to task-item components

**Checkpoint**: User Story 8 complete - task toggle with optimistic updates functional

---

## Phase 11: User Story 9 - User Signout (Priority: P3)

**Goal**: Authenticated users can sign out and session is properly cleared

**Independent Test**: Click signout, verify token cleared and redirected to signin

### Implementation for User Story 9

- [ ] T082 [US9] Ensure signout button in header clears Better Auth session
- [ ] T083 [US9] Ensure signout redirects to signin page
- [ ] T084 [US9] Verify protected routes redirect to signin after signout
- [ ] T085 [US9] Verify browser back button doesn't expose protected content after signout

**Checkpoint**: User Story 9 complete - signout flow fully functional

---

## Phase 12: User Story 10 - Responsive Layout (Priority: P3)

**Goal**: Application works across mobile (320px), tablet (768px), and desktop (1920px) viewports

**Independent Test**: View application at different viewport widths, verify all features accessible

### Implementation for User Story 10

- [ ] T086 [US10] Verify single-column layout on mobile (320px) across all pages
- [ ] T087 [US10] Ensure touch targets are at least 44px on mobile
- [ ] T088 [US10] Test hamburger menu functionality on mobile
- [ ] T089 [US10] Ensure forms are full-width on mobile
- [ ] T090 [US10] Test task list scrolling on mobile
- [ ] T091 [US10] Verify layout adapts at tablet breakpoint (768px)
- [ ] T092 [US10] Adjust spacing and padding for medium screens
- [ ] T093 [US10] Verify comfortable reading width (max-width) on desktop
- [ ] T094 [US10] Ensure navigation is horizontal on desktop
- [ ] T095 [US10] Test at 1920px viewport

**Checkpoint**: User Story 10 complete - responsive design verified

---

## Phase 13: Polish & E2E Validation

**Purpose**: Final validation and cross-cutting concerns

### Final UI Polish

- [ ] T096 Ensure consistent spacing across all components
- [ ] T097 Verify all loading states are visible within 100ms
- [ ] T098 Verify all error states have retry option
- [ ] T099 Verify visual distinction of completed vs pending tasks

### E2E Authentication Validation

- [ ] T100 E2E: Complete signup flow (page to dashboard under 60s)
- [ ] T101 E2E: Complete signin flow (page to dashboard under 30s)
- [ ] T102 E2E: Signout flow (dashboard to signin)
- [ ] T103 E2E: Protected route redirect when not authenticated
- [ ] T104 E2E: Auth page redirect when already authenticated

### E2E Task CRUD Validation

- [ ] T105 E2E: View empty task list (new user)
- [ ] T106 E2E: Create new task (under 10s)
- [ ] T107 E2E: View task in list
- [ ] T108 E2E: Edit task description (under 5s)
- [ ] T109 E2E: Toggle task completion (under 5s)
- [ ] T110 E2E: Delete task with confirmation (under 5s)
- [ ] T111 E2E: Verify task persists after page refresh

### E2E Error Handling Validation

- [ ] T112 E2E: Form validation errors display correctly
- [ ] T113 E2E: API error messages display correctly
- [ ] T114 E2E: 401 response triggers signin redirect

### E2E Responsive Validation

- [ ] T115 E2E: All features work at 320px viewport
- [ ] T116 E2E: All features work at 768px viewport
- [ ] T117 E2E: All features work at 1920px viewport

**Checkpoint**: All validation complete - frontend ready for deployment

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 (types) - BLOCKS all user stories
- **Phases 3-12 (User Stories)**: All depend on Phase 2 completion
  - Stories can proceed sequentially in priority order (P1 → P2 → P3)
- **Phase 13 (Polish)**: Depends on all user stories being complete

### User Story Dependencies

| Story | Priority | Dependencies | Can Parallelize After |
|-------|----------|--------------|----------------------|
| US1 (Signup) | P1 | Phase 2 | Phase 2 |
| US2 (Signin) | P1 | Phase 2 | Phase 2 |
| US3 (Dashboard) | P1 | Phase 2 | Phase 2 |
| US4 (Task List) | P1 | Phase 2 | Phase 2 |
| US5 (Create Task) | P2 | US4 (needs task list) | US4 |
| US6 (Edit Task) | P2 | US4, US5 (needs task form) | US5 |
| US7 (Delete Task) | P2 | US4 (needs task list) | US4 |
| US8 (Toggle) | P2 | US4 (needs task item) | US4 |
| US9 (Signout) | P3 | US3 (needs header) | US3 |
| US10 (Responsive) | P3 | All UI stories | US9 |

### Within Each User Story

- Models/Types before components
- Components before pages
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- T001-T004: All type files can be created in parallel
- T011-T013: Common components can be created in parallel
- T026-T027: Layout components can be created in parallel
- T034: TaskStats can parallel with other US3 layout tasks
- Different P2 stories (US5-US8) can be worked on in parallel after US4

---

## Implementation Strategy

### MVP First (P1 Stories Only)

1. Complete Phase 1: Setup (Types)
2. Complete Phase 2: Foundational (API Client, Common Components)
3. Complete Phase 3: US1 - Signup
4. Complete Phase 4: US2 - Signin
5. Complete Phase 5: US3 - Dashboard
6. Complete Phase 6: US4 - Task List View
7. **STOP and VALIDATE**: All P1 stories functional, users can sign up, sign in, and view tasks
8. Deploy/demo MVP

### Incremental Delivery

1. MVP (P1 stories) → Core functionality
2. Add P2 stories (US5-US8) → Full CRUD operations
3. Add P3 stories (US9-US10) → Polish and responsive

### Suggested Execution Flow

```text
Phase 1 → Phase 2 → [US1 → US2 → US3 → US4] (P1 MVP)
                          ↓
              [US5, US6, US7, US8] (P2 - can parallelize)
                          ↓
                   [US9 → US10] (P3)
                          ↓
                    Phase 13 (Polish)
```

---

## Task Summary

| Phase | Tasks | Story Coverage |
|-------|-------|----------------|
| Phase 1: Setup | 5 | Foundation |
| Phase 2: Foundational | 8 | Foundation |
| Phase 3: US1 Signup | 5 | P1 |
| Phase 4: US2 Signin | 7 | P1 |
| Phase 5: US3 Dashboard | 16 | P1 |
| Phase 6: US4 Task List | 9 | P1 |
| Phase 7: US5 Create Task | 9 | P2 |
| Phase 8: US6 Edit Task | 9 | P2 |
| Phase 9: US7 Delete Task | 7 | P2 |
| Phase 10: US8 Toggle | 6 | P2 |
| Phase 11: US9 Signout | 4 | P3 |
| Phase 12: US10 Responsive | 10 | P3 |
| Phase 13: Polish & E2E | 22 | Validation |
| **Total** | **117** | |

### Tasks Per Priority

- **P1 (MVP)**: 37 tasks (US1-US4)
- **P2 (CRUD)**: 31 tasks (US5-US8)
- **P3 (Polish)**: 14 tasks (US9-US10)
- **Foundation + Validation**: 35 tasks

---

## Notes

- All tasks target `nextjs-frontend-builder` agent
- [P] tasks = different files, no dependencies on incomplete tasks
- [USX] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
