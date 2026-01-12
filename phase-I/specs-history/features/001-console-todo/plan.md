# Implementation Plan: Console Todo App

**Branch**: `001-console-todo` | **Date**: 2026-01-07 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/001-console-todo/spec.md`

## Summary

Build a Python-based in-memory console application that provides full CRUD operations for task management. The application enables developers to add, view, update, delete, and mark tasks as complete through an interactive command-line menu interface. Tasks are stored in memory using Python data structures and persist only during the application session. This phase establishes the foundational task management logic that will evolve into a full-stack web application (Phase II), AI-powered chatbot (Phase III), and cloud-deployed distributed system (Phase IV & V).

## Technical Context

**Language/Version**: Python 3.13 or higher
**Primary Dependencies**: Python standard library only (no external packages)
**Storage**: In-memory data structures (list of dictionaries for tasks)
**Testing**: pytest for unit tests
**Target Platform**: Cross-platform terminal/console (Windows, macOS, Linux)
**Project Type**: Single console application
**Performance Goals**: <3s startup time, <10s per operation, instant menu navigation
**Constraints**: No file I/O, no database, no external libraries beyond stdlib, PEP8 compliance required
**Scale/Scope**: Single-user session, 5 CRUD operations, ~100-200 LOC, educational focus

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase I Technical Standards Compliance

| Principle | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| **Language** | Python 3.10+ with PEP8 compliance | ✅ PASS | Using Python 3.13+, will enforce PEP8 via linter in tasks |
| **Storage** | In-memory data structures only (list, dict) | ✅ PASS | Tasks stored as list of dict, no file/DB I/O |
| **Interface** | Command-line menu system with clear prompts | ✅ PASS | Numbered menu with operation prompts |
| **Operations** | Full CRUD (Create, Read, Update, Delete) | ✅ PASS | Add, View, Update, Delete, Mark Complete |
| **Error Handling** | Graceful invalid input handling | ✅ PASS | Input validation in utils module |
| **Testing** | Unit tests for all CRUD operations using pytest | ✅ PASS | Test suite planned in tasks phase |
| **Documentation** | README with setup/usage (minimum 100 words) | ✅ PASS | README.md planned in tasks phase |

### Core Principles Alignment

| Principle | Requirement | Status | Implementation |
|-----------|-------------|--------|----------------|
| **I. Accuracy in Implementation** | Precisely match spec requirements | ✅ PASS | All 15 FRs mapped to implementation |
| **II. Clarity in Code and Structure** | Modular, self-documenting code | ✅ PASS | 3-module structure (main, todo, utils) |
| **III. Reproducibility** | Consistent behavior across environments | ✅ PASS | Python stdlib only, no env-specific deps |
| **IV. Scalability** | Design supports future phase evolution | ✅ PASS | Task model compatible with future DB schema |
| **V. Security and Data Integrity** | Input validation, no hardcoded secrets | ✅ PASS | Input validation in utils, no secrets needed |
| **VI. Phase-Specific Compliance** | Adhere to Phase I tech stack | ✅ PASS | In-memory only, no external DB/frameworks |

**Constitution Check Result**: ✅ **PASSED** - No violations detected

## Project Structure

### Documentation (this feature)

```text
specs/001-console-todo/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── cli-interface.md # CLI menu contract
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── __init__.py          # Package marker
├── main.py              # Entry point, CLI menu loop
├── todo.py              # Task CRUD operations
└── utils.py             # Input validation, display formatting

tests/
├── __init__.py          # Test package marker
├── test_todo.py         # Unit tests for CRUD operations
└── test_utils.py        # Unit tests for validation/formatting

README.md                # Project documentation
requirements-dev.txt     # Development dependencies (pytest only)
```

**Structure Decision**: Single project structure selected because this is a standalone console application with no frontend/backend separation. The modular design (main/todo/utils) supports code clarity and testability while remaining simple enough for educational purposes. This structure can evolve into a library/API pattern for Phase II integration.

## Complexity Tracking

> No constitution violations requiring justification

---

## Phase 0: Research & Technical Decisions

### Decision 1: Task Data Structure

**Decision**: Use list of dictionaries for task storage

**Rationale**:
- Simple and Pythonic for in-memory storage
- Direct mapping to future database models (Phase II)
- Supports easy iteration for view operations
- Dictionary structure allows flexible attribute expansion

**Alternatives Considered**:
- **Namedtuples**: Too rigid, difficult to update individual fields
- **Custom Task class**: Over-engineering for Phase I, adds unnecessary complexity
- **List of lists**: Poor readability, no self-documenting field names

**Example Structure**:
```python
tasks = [
    {"id": 1, "description": "Review Python docs", "completed": False, "created": "2026-01-07T10:00:00"},
    {"id": 2, "description": "Write unit tests", "completed": True, "created": "2026-01-07T11:30:00"}
]
```

### Decision 2: ID Generation Strategy

**Decision**: Sequential integer counter starting at 1

**Rationale**:
- User-friendly: easy to read and type (vs UUID)
- Guarantees uniqueness within session
- Simple implementation: `next_id = len(tasks) + 1` or track counter
- Aligns with database auto-increment in Phase II

**Alternatives Considered**:
- **UUID**: Overkill for in-memory, poor UX for typing
- **Index-based**: Fragile when deleting items, IDs change
- **Timestamp-based**: Collision risk, not user-friendly

**Implementation**: Maintain a global `next_task_id` counter, increment after each add

### Decision 3: Menu Loop Architecture

**Decision**: Infinite while loop with dispatch dictionary

**Rationale**:
- Clean separation: menu display vs operation logic
- Easy to extend with new operations
- Clear exit condition (explicit "exit" option)
- Avoids long if-elif chains

**Pattern**:
```python
def main():
    operations = {
        "1": add_task,
        "2": view_tasks,
        "3": update_task,
        "4": delete_task,
        "5": mark_complete,
        "6": exit_app
    }
    while True:
        display_menu()
        choice = input("Select option: ")
        operation = operations.get(choice, invalid_choice)
        operation()
```

### Decision 4: Input Validation Strategy

**Decision**: Centralized validation functions in `utils.py`

**Rationale**:
- DRY principle: reusable across all operations
- Easier to test validation logic independently
- Consistent error messages
- Supports future enhancement (regex patterns, type checking)

**Key Functions**:
- `validate_task_id(user_input) -> int | None`: Validates numeric ID
- `validate_description(text) -> str | None`: Ensures non-empty
- `validate_menu_choice(choice, valid_options) -> str | None`: Menu validation

### Decision 5: Error Handling Approach

**Decision**: Return None on validation failure, display errors in calling function

**Rationale**:
- Avoids exception handling for expected validation failures
- Caller controls error message display and retry logic
- Simpler flow for menu-driven interactions
- Reserves exceptions for unexpected errors

**Pattern**:
```python
task_id = validate_task_id(user_input)
if task_id is None:
    print("Invalid input. Please enter a numeric task ID")
    return
```

### Decision 6: Display Formatting

**Decision**: Simple tabular format using f-strings

**Rationale**:
- No external dependencies (no tabulate, prettytable)
- Sufficient for console display
- Easy to read and maintain
- Constitutional compliance (stdlib only)

**Example Output**:
```
ID  | Description                    | Status
----|--------------------------------|-----------
1   | Review Python documentation    | Incomplete
2   | Write unit tests              | Complete
```

---

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](data-model.md) for detailed entity specifications.

**Task Entity**:
- `id`: Integer (unique, auto-increment, primary identifier)
- `description`: String (non-empty, user-provided task text)
- `completed`: Boolean (default False, tracks completion status)
- `created`: String (ISO 8601 timestamp, optional for Phase I)

**In-Memory Representation**:
```python
# Global state
tasks: list[dict] = []
next_task_id: int = 1

# Example task
{
    "id": 1,
    "description": "Complete Phase I implementation",
    "completed": False,
    "created": "2026-01-07T15:30:00"
}
```

**Validation Rules**:
- ID: Must be positive integer, must exist in tasks list
- Description: Must be non-empty string (min 1 char)
- Completed: Must be boolean
- Created: ISO 8601 format (optional, auto-generated)

**State Transitions**:
- Task creation: `completed = False` (default)
- Mark complete: `completed = False → True`
- Update description: Preserves `completed` and `created` fields
- Delete: Remove from tasks list

### CLI Interface Contract

See [contracts/cli-interface.md](contracts/cli-interface.md) for complete menu specifications.

**Main Menu**:
```
=== Todo App ===
1. Add task
2. View tasks
3. Update task
4. Delete task
5. Mark task as complete
6. Exit

Select option (1-6):
```

**Operation Flows**:

1. **Add Task**:
   - Prompt: "Enter task description: "
   - Validation: Non-empty description
   - Success: "Task added successfully! (ID: {id})"
   - Return to menu

2. **View Tasks**:
   - Display all tasks in tabular format
   - Empty state: "No tasks yet. Add your first task!"
   - Return to menu

3. **Update Task**:
   - Prompt: "Enter task ID: "
   - Validation: Numeric ID, task exists
   - Prompt: "Enter new description: "
   - Validation: Non-empty description
   - Success: "Task updated successfully!"
   - Return to menu

4. **Delete Task**:
   - Prompt: "Enter task ID: "
   - Validation: Numeric ID, task exists
   - Success: "Task deleted successfully"
   - Return to menu

5. **Mark Complete**:
   - Prompt: "Enter task ID: "
   - Validation: Numeric ID, task exists
   - Check: Already complete → "Task already completed"
   - Success: "Task marked as complete!"
   - Return to menu

6. **Exit**:
   - Display: "Goodbye!"
   - Exit application (sys.exit(0))

**Error Messages**:
- Invalid menu option: "Invalid option. Please select a number from the menu"
- Invalid task ID format: "Invalid input. Please enter a numeric task ID"
- Task not found: "Task not found. Please enter a valid task ID"
- Empty description: "Description cannot be empty"
- Empty task list: "No tasks available. Add a task first"

### Module Responsibilities

**main.py** (Entry point & menu controller):
- Display main menu
- Handle user menu selection
- Dispatch to appropriate operation
- Main application loop
- Graceful exit handling

**todo.py** (Core business logic):
- `add_task(description: str) -> int`: Create new task, return ID
- `get_all_tasks() -> list[dict]`: Retrieve all tasks
- `get_task_by_id(task_id: int) -> dict | None`: Find specific task
- `update_task(task_id: int, description: str) -> bool`: Update task description
- `delete_task(task_id: int) -> bool`: Remove task from list
- `mark_task_complete(task_id: int) -> bool`: Set completed = True
- Module-level state: `tasks` list, `next_task_id` counter

**utils.py** (Helper functions):
- `validate_task_id(user_input: str) -> int | None`: Parse and validate ID
- `validate_description(text: str) -> str | None`: Validate non-empty text
- `format_tasks_table(tasks: list[dict]) -> str`: Format tasks for display
- `get_current_timestamp() -> str`: Generate ISO 8601 timestamp
- `display_menu() -> None`: Print main menu
- `display_error(message: str) -> None`: Print error message
- `display_success(message: str) -> None`: Print success message

### Quickstart Guide

See [quickstart.md](quickstart.md) for complete setup and usage instructions.

**Quick Setup** (30 seconds):
```bash
# Clone repository (or navigate to phase-1 directory)
cd phase-1

# Verify Python version
python --version  # Must be 3.13+

# Run application
python src/main.py
```

**Quick Test**:
```bash
# Run unit tests
pytest tests/

# Run with verbose output
pytest tests/ -v
```

**First Task** (3 steps):
1. Launch app: `python src/main.py`
2. Select "1" (Add task)
3. Enter: "Complete Phase I"
4. Select "2" (View tasks) to see your task

---

## Phase 2: Task Breakdown

**Note**: Task breakdown is handled by the `/sp.tasks` command, not this planning phase.

The task list will be generated from this plan and should include:

**Setup Phase**:
- Create project directory structure
- Initialize Python package (`__init__.py` files)
- Create `requirements-dev.txt` with pytest

**Foundational Phase**:
- Implement task data model and global state in `todo.py`
- Implement validation functions in `utils.py`
- Implement display/formatting functions in `utils.py`

**User Story Phases** (P1 → P2 → P3):
- **P1**: Add task + View tasks operations
- **P2**: Mark task as complete operation
- **P3**: Update task + Delete task operations

**Testing & Documentation Phase**:
- Unit tests for all CRUD operations
- Unit tests for validation functions
- README.md with setup/usage examples
- Quickstart.md with step-by-step guide

**Validation Phase**:
- PEP8 compliance check (flake8 or black)
- Manual integration testing
- Constitution compliance verification

---

## Dependencies & Risks

### Dependencies

**Runtime**:
- Python 3.13+ interpreter
- Operating system with terminal/console support

**Development**:
- pytest (for unit testing)
- flake8 or black (for PEP8 compliance checking)

**External Systems**: None

### Risks & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Task IDs become non-sequential after deletions | High | Low | Use counter-based ID generation, accept gaps in sequence |
| Long descriptions break table formatting | Medium | Low | Use text wrapping or truncation with ellipsis in display |
| Users expect data persistence | Medium | Low | Clear messaging in app and docs about session-only storage |
| Python version incompatibility | Low | High | Document minimum version (3.13+), test on multiple versions |
| Input buffer issues with very long input | Low | Low | Accept any length (Python handles naturally), test edge case |

### Assumptions

- Users have Python 3.13+ installed or can install it
- Terminal supports UTF-8 characters for formatting
- Users understand command-line interface basics
- No need for concurrent access (single user per session)
- Task data volume is reasonable (<1000 tasks per session)
- No need for undo/redo in Phase I

### Open Questions

None - all technical decisions resolved in Phase 0 research.

---

## Post-Phase 1 Constitution Re-Check

**Status**: ✅ **PASSED** (re-evaluated after design phase)

All design decisions align with constitutional requirements:
- ✅ In-memory storage only (no file I/O, no database)
- ✅ Python stdlib only (no external dependencies beyond dev tools)
- ✅ Modular structure supports clarity and maintainability
- ✅ Design is compatible with Phase II evolution (task model maps to DB schema)
- ✅ Input validation ensures data integrity
- ✅ PEP8 compliance enforced via tooling

**Next Steps**: Proceed to `/sp.tasks` for task breakdown and implementation.
