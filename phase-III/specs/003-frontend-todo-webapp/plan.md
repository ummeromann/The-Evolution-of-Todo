# Implementation Plan: Frontend Web Application - Todo Web App

**Branch**: `003-frontend-todo-webapp` | **Date**: 2026-01-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-frontend-todo-webapp/spec.md`
**Prerequisite**: Phases 1 & 2 from `001-todo-fullstack-webapp` and `002-auth-security-integration` complete

## Summary

Build the complete frontend web application for the Todo system using Next.js 16+ App Router. This feature implements:
- All authentication UI pages (signup, signin)
- Dashboard with task summary
- Complete task management UI (list, create, edit, delete, toggle)
- Responsive design across all viewport sizes
- Proper loading, error, and empty states
- JWT-authenticated API communication

This plan builds on the existing frontend foundation from spec 001 and enhances/completes the UI layer.

## Technical Context

**Language/Version**: TypeScript/Node.js 18+ (Next.js 16+)
**Primary Dependencies**: Next.js, Better Auth, Tailwind CSS
**Storage**: N/A (Frontend communicates with FastAPI backend)
**Testing**: Manual E2E validation, viewport testing
**Target Platform**: Web (Mobile-first responsive design)
**Constraints**: No additional libraries, Fetch API only, no server actions for business logic

## Constitution Check

*GATE: Must pass before implementation. Re-checked after design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | PASS | This plan derived from approved spec.md |
| II. Zero Manual Coding | PASS | All implementation via Claude Code (nextjs-frontend-builder agent) |
| III. Security by Design | PASS | JWT attachment, protected routes, auth state management |
| IV. Single Source of Truth | PASS | spec.md authoritative |
| V. Clean Separation of Concerns | PASS | Frontend UI only, no business logic, API communication through client |
| VI. Reproducibility | PASS | Full plan documented, PHR records maintained |

## Current Implementation Status

Based on `001-todo-fullstack-webapp` and `002-auth-security-integration` completion:

### Already Implemented (from Previous Specs)

- [x] Next.js project structure
- [x] Better Auth configuration (`frontend/src/lib/auth.ts`)
- [x] Better Auth client (`frontend/src/lib/auth-client.ts`)
- [x] Auth API route handler (`frontend/src/app/api/auth/[...all]/route.ts`)
- [x] Basic signup form (`frontend/src/components/forms/signup-form.tsx`)
- [x] Basic signin form (`frontend/src/components/forms/signin-form.tsx`)
- [x] Protected layout (`frontend/src/app/(protected)/layout.tsx`)
- [x] Basic API client (`frontend/src/lib/api.ts`)
- [x] Basic UI components (button, input, card)
- [x] Basic task components (task-list, task-item, empty-state)
- [x] Tailwind CSS configuration

### Gaps to Address (This Feature)

- [ ] Enhanced API client with comprehensive error handling
- [ ] Loading and error state components
- [ ] Dashboard page with task summary statistics
- [ ] Tasks list page (separate from dashboard)
- [ ] Enhanced task list with full CRUD operations
- [ ] Create task form with validation
- [ ] Edit task modal/form with validation
- [ ] Delete confirmation dialog
- [ ] Toggle completion with optimistic updates
- [ ] Navigation header with signout button
- [ ] Mobile-responsive navigation
- [ ] Comprehensive form validation
- [ ] Loading states for all operations
- [ ] Error messages with retry options
- [ ] Empty state enhancements
- [ ] Responsive design refinements

---

## Implementation Phases

### Phase 1: Foundation & API Client Enhancement

**Agent**: `nextjs-frontend-builder`
**Dependencies**: None (builds on existing code)
**Output**: Enhanced API client and common components

#### 1.1 TypeScript Types

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 1.1.1 | Create `src/types/task.ts` with Task interfaces | nextjs-frontend-builder | None |
| 1.1.2 | Create `src/types/auth.ts` with User/Session interfaces | nextjs-frontend-builder | None |
| 1.1.3 | Create `src/types/api.ts` with ApiResponse/ApiError interfaces | nextjs-frontend-builder | None |
| 1.1.4 | Create `src/types/forms.ts` with form state interfaces | nextjs-frontend-builder | None |
| 1.1.5 | Update `src/types/index.ts` to export all types | nextjs-frontend-builder | 1.1.4 |

#### 1.2 API Client Enhancement

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 1.2.1 | Enhance `src/lib/api.ts` with proper TypeScript types | nextjs-frontend-builder | 1.1.5 |
| 1.2.2 | Add request timeout handling (30s) | nextjs-frontend-builder | 1.2.1 |
| 1.2.3 | Add 401 response interception with redirect to signin | nextjs-frontend-builder | 1.2.2 |
| 1.2.4 | Add comprehensive error response parsing | nextjs-frontend-builder | 1.2.3 |
| 1.2.5 | Add taskApi object with all CRUD methods | nextjs-frontend-builder | 1.2.4 |

#### 1.3 Common Components

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 1.3.1 | Create `src/components/common/loading-spinner.tsx` | nextjs-frontend-builder | 1.1.5 |
| 1.3.2 | Create `src/components/common/error-message.tsx` with retry button | nextjs-frontend-builder | 1.1.5 |
| 1.3.3 | Create `src/components/common/confirm-dialog.tsx` | nextjs-frontend-builder | 1.1.5 |

**Checkpoint**: API client enhanced, common components ready

---

### Phase 2: Navigation & Layout

**Agent**: `nextjs-frontend-builder`
**Dependencies**: Phase 1 complete
**Output**: Complete navigation structure with responsive design

#### 2.1 Layout Components

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 2.1.1 | Create `src/components/layout/header.tsx` with logo and nav | nextjs-frontend-builder | Phase 1 |
| 2.1.2 | Create `src/components/layout/nav-menu.tsx` for mobile menu | nextjs-frontend-builder | 2.1.1 |
| 2.1.3 | Add signout button to header | nextjs-frontend-builder | 2.1.2 |
| 2.1.4 | Implement mobile hamburger menu toggle | nextjs-frontend-builder | 2.1.3 |

#### 2.2 Root Layout Updates

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 2.2.1 | Update `src/app/layout.tsx` with proper meta tags | nextjs-frontend-builder | 2.1.4 |
| 2.2.2 | Update `src/app/page.tsx` landing page with CTA buttons | nextjs-frontend-builder | 2.2.1 |

#### 2.3 Protected Layout Updates

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 2.3.1 | Update `src/app/(protected)/layout.tsx` with Header component | nextjs-frontend-builder | 2.2.2 |
| 2.3.2 | Add navigation links (Dashboard, Tasks) | nextjs-frontend-builder | 2.3.1 |
| 2.3.3 | Ensure signout clears auth state and redirects | nextjs-frontend-builder | 2.3.2 |

**Checkpoint**: Navigation complete with responsive mobile menu

---

### Phase 3: Authentication Pages Enhancement

**Agent**: `nextjs-frontend-builder`
**Dependencies**: Phase 2 complete
**Output**: Polished auth pages with full validation and error handling

#### 3.1 Signup Page Enhancement

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 3.1.1 | Enhance `signup-form.tsx` with proper validation | nextjs-frontend-builder | Phase 2 |
| 3.1.2 | Add email format validation with error message | nextjs-frontend-builder | 3.1.1 |
| 3.1.3 | Add password length validation (min 8 chars) | nextjs-frontend-builder | 3.1.2 |
| 3.1.4 | Add loading state during form submission | nextjs-frontend-builder | 3.1.3 |
| 3.1.5 | Add API error display (duplicate email, etc.) | nextjs-frontend-builder | 3.1.4 |
| 3.1.6 | Add redirect to dashboard on success | nextjs-frontend-builder | 3.1.5 |

#### 3.2 Signin Page Enhancement

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 3.2.1 | Enhance `signin-form.tsx` with proper validation | nextjs-frontend-builder | 3.1.6 |
| 3.2.2 | Add email and password validation | nextjs-frontend-builder | 3.2.1 |
| 3.2.3 | Add loading state during form submission | nextjs-frontend-builder | 3.2.2 |
| 3.2.4 | Add generic error display for invalid credentials | nextjs-frontend-builder | 3.2.3 |
| 3.2.5 | Add redirect to dashboard on success | nextjs-frontend-builder | 3.2.4 |

#### 3.3 Auth Page Redirects

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 3.3.1 | Update `src/app/(auth)/layout.tsx` to check if already authenticated | nextjs-frontend-builder | 3.2.5 |
| 3.3.2 | Redirect authenticated users from signin/signup to dashboard | nextjs-frontend-builder | 3.3.1 |
| 3.3.3 | Handle session_expired query param on signin page | nextjs-frontend-builder | 3.3.2 |

**Checkpoint**: Auth pages complete with full validation and redirects

---

### Phase 4: Dashboard Page

**Agent**: `nextjs-frontend-builder`
**Dependencies**: Phase 3 complete
**Output**: Dashboard with task statistics and quick actions

#### 4.1 Dashboard Statistics Component

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 4.1.1 | Create `src/components/dashboard/task-stats.tsx` | nextjs-frontend-builder | Phase 3 |
| 4.1.2 | Display total, completed, pending task counts | nextjs-frontend-builder | 4.1.1 |
| 4.1.3 | Add visual cards for each statistic | nextjs-frontend-builder | 4.1.2 |

#### 4.2 Dashboard Page

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 4.2.1 | Create/update `src/app/(protected)/dashboard/page.tsx` | nextjs-frontend-builder | 4.1.3 |
| 4.2.2 | Add welcome message with user email | nextjs-frontend-builder | 4.2.1 |
| 4.2.3 | Add task statistics display | nextjs-frontend-builder | 4.2.2 |
| 4.2.4 | Add "View Tasks" and "Create Task" CTA buttons | nextjs-frontend-builder | 4.2.3 |
| 4.2.5 | Add loading state while fetching task data | nextjs-frontend-builder | 4.2.4 |
| 4.2.6 | Add empty state for new users (no tasks) | nextjs-frontend-builder | 4.2.5 |

**Checkpoint**: Dashboard page complete with statistics

---

### Phase 5: Task List Page

**Agent**: `nextjs-frontend-builder`
**Dependencies**: Phase 4 complete
**Output**: Full task list with all CRUD operations

#### 5.1 Tasks Page Structure

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 5.1.1 | Create `src/app/(protected)/tasks/page.tsx` | nextjs-frontend-builder | Phase 4 |
| 5.1.2 | Add page title and "Create Task" button | nextjs-frontend-builder | 5.1.1 |
| 5.1.3 | Integrate TaskList component | nextjs-frontend-builder | 5.1.2 |

#### 5.2 Task List Enhancement

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 5.2.1 | Update `task-list.tsx` to fetch tasks from API | nextjs-frontend-builder | 5.1.3 |
| 5.2.2 | Add loading spinner while fetching | nextjs-frontend-builder | 5.2.1 |
| 5.2.3 | Add error message with retry button | nextjs-frontend-builder | 5.2.2 |
| 5.2.4 | Add empty state when no tasks exist | nextjs-frontend-builder | 5.2.3 |
| 5.2.5 | Pass edit/delete/toggle handlers to TaskItems | nextjs-frontend-builder | 5.2.4 |

#### 5.3 Task Item Enhancement

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 5.3.1 | Update `task-item.tsx` with completion checkbox | nextjs-frontend-builder | 5.2.5 |
| 5.3.2 | Add visual distinction for completed tasks (strikethrough) | nextjs-frontend-builder | 5.3.1 |
| 5.3.3 | Add Edit and Delete action buttons | nextjs-frontend-builder | 5.3.2 |
| 5.3.4 | Add loading state for toggle operation | nextjs-frontend-builder | 5.3.3 |
| 5.3.5 | Add loading state for delete operation | nextjs-frontend-builder | 5.3.4 |

**Checkpoint**: Task list displays with basic interactions

---

### Phase 6: Create Task Functionality

**Agent**: `nextjs-frontend-builder`
**Dependencies**: Phase 5 complete
**Output**: Task creation with modal form and validation

#### 6.1 Create Task Form

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 6.1.1 | Update `task-form.tsx` to support create mode | nextjs-frontend-builder | Phase 5 |
| 6.1.2 | Add description textarea with character counter | nextjs-frontend-builder | 6.1.1 |
| 6.1.3 | Add validation (1-500 characters, non-empty) | nextjs-frontend-builder | 6.1.2 |
| 6.1.4 | Add loading state during submission | nextjs-frontend-builder | 6.1.3 |
| 6.1.5 | Add error message display | nextjs-frontend-builder | 6.1.4 |

#### 6.2 Create Task Integration

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 6.2.1 | Add create task modal/section to tasks page | nextjs-frontend-builder | 6.1.5 |
| 6.2.2 | Call taskApi.create on form submit | nextjs-frontend-builder | 6.2.1 |
| 6.2.3 | Add new task to list on success | nextjs-frontend-builder | 6.2.2 |
| 6.2.4 | Close modal/clear form on success | nextjs-frontend-builder | 6.2.3 |

**Checkpoint**: Task creation functional

---

### Phase 7: Edit Task Functionality

**Agent**: `nextjs-frontend-builder`
**Dependencies**: Phase 6 complete
**Output**: Task editing with modal form and validation

#### 7.1 Edit Task Form

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 7.1.1 | Update `task-form.tsx` to support edit mode | nextjs-frontend-builder | Phase 6 |
| 7.1.2 | Pre-populate form with existing task description | nextjs-frontend-builder | 7.1.1 |
| 7.1.3 | Add Cancel button to discard changes | nextjs-frontend-builder | 7.1.2 |
| 7.1.4 | Add validation same as create | nextjs-frontend-builder | 7.1.3 |

#### 7.2 Edit Task Integration

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 7.2.1 | Add edit modal state management to tasks page | nextjs-frontend-builder | 7.1.4 |
| 7.2.2 | Open modal with task data when Edit clicked | nextjs-frontend-builder | 7.2.1 |
| 7.2.3 | Call taskApi.update on form submit | nextjs-frontend-builder | 7.2.2 |
| 7.2.4 | Update task in list on success | nextjs-frontend-builder | 7.2.3 |
| 7.2.5 | Close modal on success or cancel | nextjs-frontend-builder | 7.2.4 |

**Checkpoint**: Task editing functional

---

### Phase 8: Delete Task Functionality

**Agent**: `nextjs-frontend-builder`
**Dependencies**: Phase 7 complete
**Output**: Task deletion with confirmation dialog

#### 8.1 Delete Confirmation

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 8.1.1 | Integrate ConfirmDialog component for delete | nextjs-frontend-builder | Phase 7 |
| 8.1.2 | Show dialog when Delete clicked on task | nextjs-frontend-builder | 8.1.1 |
| 8.1.3 | Add loading state to confirm button | nextjs-frontend-builder | 8.1.2 |

#### 8.2 Delete Integration

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 8.2.1 | Call taskApi.delete on confirm | nextjs-frontend-builder | 8.1.3 |
| 8.2.2 | Remove task from list on success | nextjs-frontend-builder | 8.2.1 |
| 8.2.3 | Close dialog on success or cancel | nextjs-frontend-builder | 8.2.2 |
| 8.2.4 | Handle error with message display | nextjs-frontend-builder | 8.2.3 |

**Checkpoint**: Task deletion functional with confirmation

---

### Phase 9: Toggle Task Completion

**Agent**: `nextjs-frontend-builder`
**Dependencies**: Phase 8 complete
**Output**: Task completion toggle with optimistic updates

#### 9.1 Toggle Implementation

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 9.1.1 | Add onClick handler to completion checkbox | nextjs-frontend-builder | Phase 8 |
| 9.1.2 | Implement optimistic UI update (toggle immediately) | nextjs-frontend-builder | 9.1.1 |
| 9.1.3 | Call taskApi.toggle on click | nextjs-frontend-builder | 9.1.2 |
| 9.1.4 | Revert UI if API call fails | nextjs-frontend-builder | 9.1.3 |
| 9.1.5 | Show subtle loading indicator during toggle | nextjs-frontend-builder | 9.1.4 |

**Checkpoint**: Task toggle functional with optimistic updates

---

### Phase 10: Responsive Design & Polish

**Agent**: `nextjs-frontend-builder`
**Dependencies**: Phase 9 complete
**Output**: Fully responsive UI across all viewports

#### 10.1 Mobile Responsiveness (320px)

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 10.1.1 | Verify single-column layout on mobile | nextjs-frontend-builder | Phase 9 |
| 10.1.2 | Ensure touch targets are at least 44px | nextjs-frontend-builder | 10.1.1 |
| 10.1.3 | Test hamburger menu functionality | nextjs-frontend-builder | 10.1.2 |
| 10.1.4 | Ensure forms are full-width on mobile | nextjs-frontend-builder | 10.1.3 |
| 10.1.5 | Test task list scrolling on mobile | nextjs-frontend-builder | 10.1.4 |

#### 10.2 Tablet Responsiveness (768px)

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 10.2.1 | Verify layout adapts at tablet breakpoint | nextjs-frontend-builder | 10.1.5 |
| 10.2.2 | Adjust spacing and padding for medium screens | nextjs-frontend-builder | 10.2.1 |

#### 10.3 Desktop Responsiveness (1024px+)

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 10.3.1 | Verify comfortable reading width (max-width) | nextjs-frontend-builder | 10.2.2 |
| 10.3.2 | Ensure navigation is horizontal on desktop | nextjs-frontend-builder | 10.3.1 |
| 10.3.3 | Test at 1920px viewport | nextjs-frontend-builder | 10.3.2 |

#### 10.4 Final UI Polish

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 10.4.1 | Ensure consistent spacing across components | nextjs-frontend-builder | 10.3.3 |
| 10.4.2 | Verify all loading states are visible | nextjs-frontend-builder | 10.4.1 |
| 10.4.3 | Verify all error states have retry option | nextjs-frontend-builder | 10.4.2 |
| 10.4.4 | Verify visual distinction of completed tasks | nextjs-frontend-builder | 10.4.3 |

**Checkpoint**: Responsive design complete across all viewports

---

### Phase 11: End-to-End Validation

**Agent**: `nextjs-frontend-builder`
**Dependencies**: Phase 10 complete
**Output**: Full E2E verification of all user stories

#### 11.1 Authentication Flow Validation

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 11.1.1 | E2E: Complete signup flow (page to dashboard) | nextjs-frontend-builder | Phase 10 |
| 11.1.2 | E2E: Complete signin flow (page to dashboard) | nextjs-frontend-builder | 11.1.1 |
| 11.1.3 | E2E: Signout flow (dashboard to signin) | nextjs-frontend-builder | 11.1.2 |
| 11.1.4 | E2E: Protected route redirect when not authenticated | nextjs-frontend-builder | 11.1.3 |
| 11.1.5 | E2E: Auth page redirect when already authenticated | nextjs-frontend-builder | 11.1.4 |

#### 11.2 Task CRUD Validation

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 11.2.1 | E2E: View empty task list (new user) | nextjs-frontend-builder | 11.1.5 |
| 11.2.2 | E2E: Create new task | nextjs-frontend-builder | 11.2.1 |
| 11.2.3 | E2E: View task in list | nextjs-frontend-builder | 11.2.2 |
| 11.2.4 | E2E: Edit task description | nextjs-frontend-builder | 11.2.3 |
| 11.2.5 | E2E: Toggle task completion | nextjs-frontend-builder | 11.2.4 |
| 11.2.6 | E2E: Delete task with confirmation | nextjs-frontend-builder | 11.2.5 |
| 11.2.7 | E2E: Verify task persists after page refresh | nextjs-frontend-builder | 11.2.6 |

#### 11.3 Error Handling Validation

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 11.3.1 | E2E: Form validation errors display correctly | nextjs-frontend-builder | 11.2.7 |
| 11.3.2 | E2E: API error messages display correctly | nextjs-frontend-builder | 11.3.1 |
| 11.3.3 | E2E: 401 response triggers signin redirect | nextjs-frontend-builder | 11.3.2 |

#### 11.4 Responsive Validation

| Step | Task | Agent | Dependencies |
|------|------|-------|--------------|
| 11.4.1 | E2E: All features work at 320px viewport | nextjs-frontend-builder | 11.3.3 |
| 11.4.2 | E2E: All features work at 768px viewport | nextjs-frontend-builder | 11.4.1 |
| 11.4.3 | E2E: All features work at 1920px viewport | nextjs-frontend-builder | 11.4.2 |

**Checkpoint**: All user stories validated end-to-end

---

## Task Summary

| Phase | Tasks | Agent |
|-------|-------|-------|
| Phase 1: Foundation & API Client | 13 | nextjs-frontend-builder |
| Phase 2: Navigation & Layout | 9 | nextjs-frontend-builder |
| Phase 3: Auth Pages Enhancement | 12 | nextjs-frontend-builder |
| Phase 4: Dashboard Page | 7 | nextjs-frontend-builder |
| Phase 5: Task List Page | 11 | nextjs-frontend-builder |
| Phase 6: Create Task | 8 | nextjs-frontend-builder |
| Phase 7: Edit Task | 8 | nextjs-frontend-builder |
| Phase 8: Delete Task | 7 | nextjs-frontend-builder |
| Phase 9: Toggle Completion | 5 | nextjs-frontend-builder |
| Phase 10: Responsive Design | 12 | nextjs-frontend-builder |
| Phase 11: E2E Validation | 15 | nextjs-frontend-builder |
| **Total** | **107** | |

---

## Risk Analysis

| Risk | Probability | Mitigation |
|------|-------------|------------|
| Better Auth session token retrieval issues | Low | Test early in Phase 1, fallback error handling |
| API client 401 handling complexity | Medium | Comprehensive testing in Phase 11 |
| Responsive breakpoint issues | Medium | Test at each viewport during Phase 10 |
| Form validation edge cases | Low | Mirror backend validation rules exactly |
| Modal state management complexity | Low | Use simple useState per modal |

---

## Success Criteria Mapping

| Success Criterion | Phase | Validation Step |
|-------------------|-------|-----------------|
| SC-001: Signup <60s | Phase 11 | 11.1.1 |
| SC-002: Signin <30s | Phase 11 | 11.1.2 |
| SC-003: Create task <10s | Phase 11 | 11.2.2 |
| SC-004: Task operations <5s | Phase 11 | 11.2.3-11.2.6 |
| SC-005: Viewports 320px-1920px | Phase 11 | 11.4.1-11.4.3 |
| SC-006: Protected route redirect | Phase 11 | 11.1.4 |
| SC-007: JWT in all requests | Phase 1 | 1.2.3, 1.2.5 |
| SC-008: Loading states <100ms | Phase 10 | 10.4.2 |
| SC-009: Clear error messages | Phase 10 | 10.4.3 |
| SC-010: Visual task distinction | Phase 10 | 10.4.4 |
| SC-011: Form validation | Phase 3, 6, 7 | 3.1.2-3.1.3, 6.1.3, 7.1.4 |
| SC-012: All 5 operations | Phase 11 | 11.2.1-11.2.6 |

---

## Generated Artifacts

| Artifact | Path | Purpose |
|----------|------|---------|
| spec.md | specs/003-frontend-todo-webapp/spec.md | Feature requirements |
| plan.md | specs/003-frontend-todo-webapp/plan.md | This implementation plan |
| research.md | specs/003-frontend-todo-webapp/research.md | Technology decisions |
| data-model.md | specs/003-frontend-todo-webapp/data-model.md | Frontend data types |
| frontend-api-client.md | specs/003-frontend-todo-webapp/contracts/frontend-api-client.md | API client contract |
| requirements.md | specs/003-frontend-todo-webapp/checklists/requirements.md | Spec quality checklist |

---

## Next Steps

1. Run `/sp.tasks` to generate detailed task list from this plan
2. Run `/sp.implement` to begin Phase 1 implementation
3. Each phase validated before proceeding to next
4. Create PHR after implementation completes

---

## Implementation Notes

### Component Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                     Page Components                          │
├─────────────────────────────────────────────────────────────┤
│  /signup          /signin         /dashboard      /tasks     │
│      │                │                │              │      │
│      ▼                ▼                ▼              ▼      │
│  SignupForm      SigninForm       TaskStats      TaskList    │
│                                        │              │      │
│                                        ▼              ▼      │
│                                   EmptyState     TaskItem    │
│                                                      │       │
│                                                      ▼       │
│                                              TaskForm (modal)│
│                                              ConfirmDialog   │
└─────────────────────────────────────────────────────────────┘
```

### State Management Strategy

- **Auth State**: Managed by Better Auth client hooks
- **Task List State**: Local useState in TaskList component
- **Form State**: Local useState in each form component
- **Modal State**: Local useState in parent page component
- **No global state management needed** (Redux, Zustand not required)

### API Communication Pattern

1. Component mounts → fetch data
2. User action → show loading → call API
3. Success → update local state → hide loading
4. Error → show error message → allow retry
5. 401 response → redirect to signin

### Responsive Breakpoints

| Breakpoint | Width | Behavior |
|------------|-------|----------|
| Mobile | 320px - 767px | Single column, hamburger menu |
| Tablet | 768px - 1023px | Adjusted spacing, inline nav |
| Desktop | 1024px+ | Full layout, max content width |
