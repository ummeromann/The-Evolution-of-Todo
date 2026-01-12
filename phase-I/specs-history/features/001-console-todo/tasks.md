---

description: "Task list for Console Todo App implementation"
---

# Tasks: Console Todo App

**Input**: Design documents from `specs/001-console-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/cli-interface.md

**Tests**: Unit tests are REQUIRED per spec (FR-181: "Must include unit tests using pytest"). Tests are included for all CRUD operations and validation logic.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below follow single project structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project directory structure with src/ and tests/ folders
- [ ] T002 Create src/__init__.py package marker file
- [ ] T003 Create tests/__init__.py package marker file
- [ ] T004 Create requirements-dev.txt with pytest>=7.4.0

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 [P] Initialize global state (tasks list, next_task_id counter) in src/todo.py
- [ ] T006 [P] Implement validate_task_id(user_input) -> int | None in src/utils.py
- [ ] T007 [P] Implement validate_description(text) -> str | None in src/utils.py
- [ ] T008 [P] Implement display_menu() function in src/utils.py
- [ ] T009 [P] Implement format_tasks_table(tasks) -> str function in src/utils.py
- [ ] T010 [P] Create main menu loop structure with dispatch dictionary in src/main.py
- [ ] T011 [P] Implement invalid choice handler in src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add tasks and view their task list (minimal viable product)

**Independent Test**: Launch app, add tasks via menu option 1, view tasks via menu option 2, verify tasks display with ID, description, and status

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T012 [P] [US1] Write test_add_task() in tests/test_todo.py
- [ ] T013 [P] [US1] Write test_get_all_tasks() in tests/test_todo.py
- [ ] T014 [P] [US1] Write test_get_task_by_id() in tests/test_todo.py
- [ ] T015 [P] [US1] Write test_validate_description() in tests/test_utils.py
- [ ] T016 [P] [US1] Write test_format_tasks_table() with tasks in tests/test_utils.py
- [ ] T017 [P] [US1] Write test_format_tasks_table() empty state in tests/test_utils.py

### Implementation for User Story 1

- [ ] T018 [P] [US1] Implement add_task(description: str) -> int in src/todo.py
- [ ] T019 [P] [US1] Implement get_all_tasks() -> list[dict] in src/todo.py
- [ ] T020 [P] [US1] Implement get_task_by_id(task_id: int) -> dict | None in src/todo.py
- [ ] T021 [US1] Implement add_task_handler() in src/main.py (depends on T018)
- [ ] T022 [US1] Implement view_tasks_handler() in src/main.py (depends on T019)
- [ ] T023 [US1] Wire add_task_handler to menu option 1 in operations dict in src/main.py
- [ ] T024 [US1] Wire view_tasks_handler to menu option 2 in operations dict in src/main.py
- [ ] T025 [US1] Run pytest tests/test_todo.py::test_add_task and verify pass
- [ ] T026 [US1] Run pytest tests/test_todo.py::test_get_all_tasks and verify pass
- [ ] T027 [US1] Run pytest tests/test_utils.py and verify all US1 tests pass

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently (MVP complete!)

---

## Phase 4: User Story 2 - Mark Tasks as Complete (Priority: P2)

**Goal**: Enable users to mark tasks as complete to track progress

**Independent Test**: Add tasks (using US1), mark specific tasks complete via menu option 5, view tasks and verify status shows "Complete"

### Tests for User Story 2 ⚠️

- [ ] T028 [P] [US2] Write test_mark_task_complete() success case in tests/test_todo.py
- [ ] T029 [P] [US2] Write test_mark_task_complete() already complete (idempotent) in tests/test_todo.py
- [ ] T030 [P] [US2] Write test_mark_task_complete() task not found in tests/test_todo.py

### Implementation for User Story 2

- [ ] T031 [US2] Implement mark_task_complete(task_id: int) -> bool in src/todo.py
- [ ] T032 [US2] Implement mark_complete_handler() in src/main.py (depends on T031)
- [ ] T033 [US2] Wire mark_complete_handler to menu option 5 in operations dict in src/main.py
- [ ] T034 [US2] Run pytest tests/test_todo.py::test_mark_task_complete and verify pass

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task Descriptions (Priority: P3)

**Goal**: Enable users to modify task descriptions for corrections or clarifications

**Independent Test**: Add task (using US1), update description via menu option 3, view tasks and verify updated description persists

### Tests for User Story 3 ⚠️

- [ ] T035 [P] [US3] Write test_update_task() success case in tests/test_todo.py
- [ ] T036 [P] [US3] Write test_update_task() task not found in tests/test_todo.py
- [ ] T037 [P] [US3] Write test_update_task() preserves completed status in tests/test_todo.py

### Implementation for User Story 3

- [ ] T038 [US3] Implement update_task(task_id: int, description: str) -> bool in src/todo.py
- [ ] T039 [US3] Implement update_task_handler() in src/main.py (depends on T038)
- [ ] T040 [US3] Wire update_task_handler to menu option 3 in operations dict in src/main.py
- [ ] T041 [US3] Run pytest tests/test_todo.py::test_update_task and verify pass

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Delete Unwanted Tasks (Priority: P3)

**Goal**: Enable users to remove tasks that are no longer relevant

**Independent Test**: Add tasks (using US1), delete specific task via menu option 4, view tasks and verify task no longer appears

### Tests for User Story 4 ⚠️

- [ ] T042 [P] [US4] Write test_delete_task() success case in tests/test_todo.py
- [ ] T043 [P] [US4] Write test_delete_task() task not found in tests/test_todo.py
- [ ] T044 [P] [US4] Write test_delete_task() verify ID not reused in tests/test_todo.py

### Implementation for User Story 4

- [ ] T045 [US4] Implement delete_task(task_id: int) -> bool in src/todo.py
- [ ] T046 [US4] Implement delete_task_handler() in src/main.py (depends on T045)
- [ ] T047 [US4] Wire delete_task_handler to menu option 4 in operations dict in src/main.py
- [ ] T048 [US4] Run pytest tests/test_todo.py::test_delete_task and verify pass

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final quality gates

- [ ] T049 [P] Implement exit_handler() with goodbye message in src/main.py
- [ ] T050 [P] Wire exit_handler to menu option 6 in operations dict in src/main.py
- [ ] T051 [P] Add docstrings to all functions in src/todo.py
- [ ] T052 [P] Add docstrings to all functions in src/utils.py
- [ ] T053 [P] Add docstrings to all functions in src/main.py
- [ ] T054 Run PEP8 compliance check using flake8 or black on src/
- [ ] T055 Fix any PEP8 violations identified in T054
- [ ] T056 [P] Write test_validate_task_id() with valid inputs in tests/test_utils.py
- [ ] T057 [P] Write test_validate_task_id() with invalid inputs in tests/test_utils.py
- [ ] T058 Run full test suite: pytest tests/ -v
- [ ] T059 Verify all tests pass (target: 18+ tests passing)
- [ ] T060 Create README.md with project description, setup instructions, usage examples (minimum 100 words)
- [ ] T061 Manual integration test: Run through all 5 CRUD operations end-to-end
- [ ] T062 Verify quickstart.md instructions work on fresh environment

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P3)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Uses get_task_by_id from US1 but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Uses get_task_by_id from US1 but independently testable
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - Uses get_task_by_id from US1 but independently testable

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Implementation tasks within a story can often run in parallel (marked with [P])
- Tests verify implementation completeness before moving to next story

### Parallel Opportunities

- All Setup tasks (T001-T004) can run in parallel
- All Foundational tasks (T005-T011) marked [P] can run in parallel within Phase 2
- Once Foundational phase completes:
  - All user story test tasks marked [P] can run in parallel
  - All user story implementation tasks marked [P] can run in parallel (within their story)
  - Different user stories can be worked on in parallel by different team members
- All Polish tasks marked [P] can run in parallel (T049-T057)

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task T012: "Write test_add_task() in tests/test_todo.py"
Task T013: "Write test_get_all_tasks() in tests/test_todo.py"
Task T014: "Write test_get_task_by_id() in tests/test_todo.py"
Task T015: "Write test_validate_description() in tests/test_utils.py"
Task T016: "Write test_format_tasks_table() with tasks in tests/test_utils.py"
Task T017: "Write test_format_tasks_table() empty state in tests/test_utils.py"

# Launch all implementation for User Story 1 together (after tests):
Task T018: "Implement add_task() in src/todo.py"
Task T019: "Implement get_all_tasks() in src/todo.py"
Task T020: "Implement get_task_by_id() in src/todo.py"
```

---

## Parallel Example: User Story 2

```bash
# Launch all tests for User Story 2 together:
Task T028: "Write test_mark_task_complete() success in tests/test_todo.py"
Task T029: "Write test_mark_task_complete() idempotent in tests/test_todo.py"
Task T030: "Write test_mark_task_complete() not found in tests/test_todo.py"

# Implementation (sequential - only one function):
Task T031: "Implement mark_task_complete() in src/todo.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T011) - CRITICAL, blocks all stories
3. Complete Phase 3: User Story 1 (T012-T027)
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Run: `python src/main.py`
   - Add tasks (option 1)
   - View tasks (option 2)
   - Verify empty state message
5. Demo MVP to stakeholders if ready

### Incremental Delivery

1. **Foundation** → Complete Setup + Foundational (T001-T011)
2. **MVP (US1)** → Add User Story 1 (T012-T027) → Test independently → Demo
3. **Enhanced (US2)** → Add User Story 2 (T028-T034) → Test independently → Demo
4. **Full CRUD (US3+US4)** → Add User Stories 3 & 4 (T035-T048) → Test independently → Demo
5. **Production Ready** → Polish (T049-T062) → Final validation → Release

Each increment adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T011)
2. Once Foundational is done:
   - Developer A: User Story 1 (T012-T027)
   - Developer B: User Story 2 (T028-T034)
   - Developer C: User Story 3 (T035-T041)
   - Developer D: User Story 4 (T042-T048)
3. Stories complete and integrate independently
4. Team completes Polish together (T049-T062)

---

## Task Breakdown by Module

### src/todo.py (CRUD Operations)

**Functions to implement**:
- `add_task(description: str) -> int` (T018, US1)
- `get_all_tasks() -> list[dict]` (T019, US1)
- `get_task_by_id(task_id: int) -> dict | None` (T020, US1)
- `mark_task_complete(task_id: int) -> bool` (T031, US2)
- `update_task(task_id: int, description: str) -> bool` (T038, US3)
- `delete_task(task_id: int) -> bool` (T045, US4)
- Global state: `tasks = []`, `next_task_id = 1` (T005)

**Total**: 6 functions + global state

### src/utils.py (Validation & Display)

**Functions to implement**:
- `validate_task_id(user_input: str) -> int | None` (T006, Foundational)
- `validate_description(text: str) -> str | None` (T007, Foundational)
- `display_menu() -> None` (T008, Foundational)
- `format_tasks_table(tasks: list[dict]) -> str` (T009, Foundational)

**Total**: 4 functions

### src/main.py (Menu & Handlers)

**Components to implement**:
- Main menu loop with dispatch dictionary (T010)
- Invalid choice handler (T011)
- `add_task_handler()` (T021, US1)
- `view_tasks_handler()` (T022, US1)
- `mark_complete_handler()` (T032, US2)
- `update_task_handler()` (T039, US3)
- `delete_task_handler()` (T046, US4)
- `exit_handler()` (T049, Polish)

**Total**: Menu loop + 6 handlers

### tests/test_todo.py (CRUD Tests)

**Test functions**:
- `test_add_task()` (T012, US1)
- `test_get_all_tasks()` (T013, US1)
- `test_get_task_by_id()` (T014, US1)
- `test_mark_task_complete()` - 3 cases (T028-T030, US2)
- `test_update_task()` - 3 cases (T035-T037, US3)
- `test_delete_task()` - 3 cases (T042-T044, US4)

**Total**: ~12 test functions

### tests/test_utils.py (Validation Tests)

**Test functions**:
- `test_validate_description()` (T015, US1)
- `test_format_tasks_table()` with tasks (T016, US1)
- `test_format_tasks_table()` empty state (T017, US1)
- `test_validate_task_id()` valid inputs (T056, Polish)
- `test_validate_task_id()` invalid inputs (T057, Polish)

**Total**: ~5 test functions

---

## Notes

- [P] tasks = different files or no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Tests MUST be written first and FAIL before implementing (TDD approach)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Count Summary

| Phase | Task Count | Parallel Tasks |
|-------|------------|----------------|
| Phase 1: Setup | 4 | 4 (all) |
| Phase 2: Foundational | 7 | 6 |
| Phase 3: User Story 1 (P1) | 16 | 8 |
| Phase 4: User Story 2 (P2) | 7 | 3 |
| Phase 5: User Story 3 (P3) | 7 | 3 |
| Phase 6: User Story 4 (P3) | 7 | 3 |
| Phase 7: Polish | 14 | 10 |
| **TOTAL** | **62 tasks** | **37 parallel** |

**MVP Scope** (minimum for demo): Phases 1-3 (T001-T027) = 27 tasks
**Full Implementation**: All phases (T001-T062) = 62 tasks

---

## Suggested Commit Strategy

**After Setup (T001-T004)**:
```
feat: initialize project structure for console todo app

- Create src/ and tests/ directories
- Add __init__.py package markers
- Add requirements-dev.txt with pytest
```

**After Foundational (T005-T011)**:
```
feat: implement foundational utilities and menu structure

- Add global state management (tasks list, ID counter)
- Implement input validation functions
- Add menu display and dispatch logic
```

**After User Story 1 (T012-T027)**:
```
feat: implement add and view tasks (User Story 1 - MVP)

- Write unit tests for add/view operations
- Implement add_task, get_all_tasks, get_task_by_id
- Add menu handlers for add and view
- All tests passing (9/9)

Independent test verified: Can add tasks and view task list
```

**After User Story 2 (T028-T034)**:
```
feat: implement mark task as complete (User Story 2)

- Write unit tests for mark complete operation
- Implement mark_task_complete with idempotent behavior
- Add menu handler for mark complete
- All tests passing (12/12)

Independent test verified: Can mark tasks complete, status updates correctly
```

**After User Story 3 (T035-T041)**:
```
feat: implement update task description (User Story 3)

- Write unit tests for update operation
- Implement update_task preserving completion status
- Add menu handler for update
- All tests passing (15/15)

Independent test verified: Can update task descriptions
```

**After User Story 4 (T042-T048)**:
```
feat: implement delete task (User Story 4)

- Write unit tests for delete operation
- Implement delete_task with ID retirement
- Add menu handler for delete
- All tests passing (18/18)

Independent test verified: Can delete tasks, IDs not reused
```

**After Polish (T049-T062)**:
```
feat: finalize console todo app with documentation and quality checks

- Add exit handler and docstrings
- Verify PEP8 compliance
- Create README with setup and usage instructions
- All 18+ tests passing
- Manual integration testing complete
- Constitution compliance verified
```
