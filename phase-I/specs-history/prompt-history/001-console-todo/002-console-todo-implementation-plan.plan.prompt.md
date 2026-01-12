---
id: 002
title: Console Todo Implementation Plan
stage: plan
date: 2026-01-07
surface: agent
model: claude-sonnet-4-5
feature: 001-console-todo
branch: 001-console-todo
user: ummeromann
command: /sp.plan
labels: ["plan", "phase-1", "console-app", "architecture", "design", "contracts"]
links:
  spec: specs/001-console-todo/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-console-todo/plan.md
  - specs/001-console-todo/research.md
  - specs/001-console-todo/data-model.md
  - specs/001-console-todo/contracts/cli-interface.md
  - specs/001-console-todo/quickstart.md
tests:
  - N/A (planning document - tests defined in plan for implementation phase)
---

## Prompt

Phase I: In-Memory Python Console Todo-App

Architecture Overview:
- CLI-based application
- In-memory task storage (list/dictionary)
- Modular Python structure:
    - main.py → entry point, CLI menu
    - todo.py → task CRUD operations
    - utils.py → helper functions (input validation, display formatting)
- No external database or web interface
- State lost on app exit

Development Plan:
1. Setup Python 3.13+ project structure
2. Implement task model (dictionary or class)
3. Implement CRUD functions:
    - Add task
    - Delete task
    - Update task
    - View tasks
    - Mark task as complete
4. Create CLI interface in main.py
5. Integrate utility functions (input validation, formatting)
6. Test all features interactively
7. Ensure code readability and modularity

## Response snapshot

Created comprehensive implementation plan for Phase I Console Todo App with complete architecture, research findings, design specifications, and contracts.

**Branch**: `001-console-todo`
**Planning Artifacts Created**: 5 documents (plan, research, data-model, cli-interface, quickstart)

### Phase 0: Research (6 Technical Decisions)

**Decision 1 - Task Data Structure**: List of dictionaries
- Rationale: Simple, future-compatible with Phase II database, self-documenting
- Alternatives rejected: Namedtuples (immutable), custom class (over-engineering), list of lists (poor readability)

**Decision 2 - ID Generation**: Sequential integer counter starting at 1
- Rationale: User-friendly, aligns with database auto-increment, simple implementation
- Counter never decreases, ensuring ID uniqueness even after deletions

**Decision 3 - Menu Loop Architecture**: While loop with dispatch dictionary
- Rationale: Clean separation, extensible, Pythonic, testable
- Pattern: `operations = {"1": add_task, "2": view_tasks, ...}`

**Decision 4 - Input Validation**: Centralized validation in utils.py with None pattern
- Functions: `validate_task_id()`, `validate_description()`
- Returns None on failure, caller handles error messages

**Decision 5 - Error Handling**: Return codes (bool/None) instead of exceptions
- Rationale: Task-not-found is expected, not exceptional
- Reserves exceptions for truly unexpected errors

**Decision 6 - Display Formatting**: Simple f-string formatting (stdlib only)
- Constitutional compliance: No external dependencies (tabulate, prettytable)
- Sufficient for console display, easy to maintain

### Phase 1: Design & Contracts

**Data Model** (`data-model.md`):
- Task entity with 4 fields: id (int), description (str), completed (bool), created (str)
- Global state: tasks list, next_task_id counter
- Validation rules: non-empty description, positive numeric ID, task existence checks
- State transitions: create → mark complete → update → delete flows
- Database migration path defined for Phase II (SQLModel schema)

**CLI Interface Contract** (`contracts/cli-interface.md`):
- Complete menu structure with exact prompts and outputs
- 6 operations: Add, View, Update, Delete, Mark Complete, Exit
- Error message standards (consistent, helpful, actionable)
- User journey examples for all workflows
- Testing checklist (40+ test cases)

**Quickstart Guide** (`quickstart.md`):
- 5-minute setup and first task workflow
- Installation steps with troubleshooting
- Basic usage for all 6 operations
- Common workflows (daily tasks, learning tracker, sprint planning)
- Error handling examples
- Testing instructions

**Project Structure**:
```
src/
├── main.py    # Entry point, menu loop
├── todo.py    # CRUD operations (6 functions)
└── utils.py   # Validation & formatting (4 functions)

tests/
├── test_todo.py   # CRUD tests
└── test_utils.py  # Validation tests
```

**Module Responsibilities**:
- `main.py`: Menu display, user input, operation dispatch
- `todo.py`: add_task, get_all_tasks, get_task_by_id, update_task, delete_task, mark_task_complete
- `utils.py`: validate_task_id, validate_description, format_tasks_table, display_menu

### Constitution Check Results

**Phase I Technical Standards**: ✅ ALL PASSED (7/7)
- Language: Python 3.13+ with PEP8 ✅
- Storage: In-memory (list/dict) ✅
- Interface: CLI menu ✅
- Operations: Full CRUD ✅
- Error Handling: Graceful validation ✅
- Testing: pytest unit tests ✅
- Documentation: README + quickstart ✅

**Core Principles**: ✅ ALL PASSED (6/6)
- I. Accuracy: All 15 FRs mapped ✅
- II. Clarity: 3-module structure ✅
- III. Reproducibility: Stdlib only ✅
- IV. Scalability: DB-compatible design ✅
- V. Security: Input validation ✅
- VI. Phase Compliance: In-memory only ✅

**No constitutional violations** - Ready for task breakdown

### Technical Context

- **Language**: Python 3.13+
- **Dependencies**: Python stdlib only (pytest for dev)
- **Storage**: In-memory (list of dicts)
- **Performance**: <3s startup, <10s per operation
- **Scale**: Single user, 5 CRUD ops, ~100-200 LOC

### Key Decisions Documented

| Area | Decision | Documented In |
|------|----------|---------------|
| Data structure | List of dicts | research.md, data-model.md |
| ID generation | Sequential counter | research.md, data-model.md |
| Menu architecture | Dispatch dict | research.md, plan.md |
| Validation strategy | Centralized utils | research.md, plan.md |
| Error handling | Return codes | research.md, plan.md |
| Display formatting | F-strings | research.md, cli-interface.md |
| CLI prompts/outputs | Exact strings | cli-interface.md |
| State transitions | Flow diagrams | data-model.md |

## Outcome

- ✅ Impact: Complete implementation plan with architecture, research, design, and contracts ready for `/sp.tasks`
- 🧪 Tests: Constitution check PASSED (13/13 requirements), 40+ test cases defined in contracts
- 📁 Files: Created plan.md, research.md, data-model.md, contracts/cli-interface.md, quickstart.md
- 🔁 Next prompts: "/sp.tasks" to generate actionable task breakdown for implementation
- 🧠 Reflection: Plan successfully balances educational objectives (teaching modular design, validation patterns) with Phase I simplicity requirements. All research decisions documented with rationale and alternatives. Design artifacts provide unambiguous implementation guidance with exact prompts, error messages, and validation rules. Architecture positions Phase I for seamless evolution into Phase II (database) without requiring rewrites.

## Evaluation notes (flywheel)

- Failure modes observed: None - all constitutional gates passed, no technical unknowns remain
- Graders run and results (PASS/FAIL): Constitution Check - PASS (13/13), CLI Contract Completeness - PASS (all operations specified), Data Model Validation - PASS (all transitions defined)
- Prompt variant (if applicable): User provided architecture overview, plan expanded with detailed research and contracts
- Next experiment (smallest change to try): Monitor task generation to verify if design artifacts provide sufficient detail for unambiguous task breakdown, or if implementation questions emerge requiring plan amendments
