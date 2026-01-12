# Quickstart Guide: Console Todo App

**Feature**: Console Todo App (Phase I)
**Date**: 2026-01-07
**Estimated Time**: 5 minutes to first task

## Prerequisites

Before you begin, ensure you have:

- **Python 3.13 or higher** installed
  - Check version: `python --version` or `python3 --version`
  - Download from: https://www.python.org/downloads/
- **Terminal/Command Prompt** access
- **Text editor** (optional, for viewing source code)

---

## Quick Start (30 seconds)

### 1. Navigate to Project Directory

```bash
cd phase-1
```

### 2. Run the Application

```bash
python src/main.py
```

**Expected Output**:
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

### 3. Add Your First Task

1. Type `1` and press Enter (Add task)
2. Type a task description: `Complete Phase I implementation`
3. Press Enter

**Expected Output**:
```
Task added successfully! (ID: 1)
```

### 4. View Your Task

1. Type `2` and press Enter (View tasks)

**Expected Output**:
```
ID   | Description                              | Status
------------------------------------------------------------
1    | Complete Phase I implementation          | Incomplete
```

**Congratulations!** You've successfully created and viewed your first task.

---

## Installation & Setup

### Step 1: Verify Python Version

```bash
python --version
```

**Required**: Python 3.13 or higher

**Alternative command** (if `python` doesn't work):
```bash
python3 --version
```

### Step 2: Install Development Dependencies (Optional)

Only needed if you want to run tests:

```bash
pip install -r requirements-dev.txt
```

**Contents of `requirements-dev.txt`**:
```
pytest>=7.4.0
```

### Step 3: Verify Installation (Optional)

Run tests to ensure everything works:

```bash
pytest tests/
```

**Expected Output**:
```
======================== test session starts ========================
collected 15 items

tests/test_todo.py .............                              [ 86%]
tests/test_utils.py ..                                        [100%]

======================== 15 passed in 0.23s =========================
```

---

## Project Structure

```
phase-1/
├── src/
│   ├── __init__.py        # Package marker
│   ├── main.py            # Entry point (run this!)
│   ├── todo.py            # CRUD operations
│   └── utils.py           # Validation & formatting
├── tests/
│   ├── __init__.py
│   ├── test_todo.py       # CRUD tests
│   └── test_utils.py      # Validation tests
├── specs/
│   └── 001-console-todo/
│       ├── spec.md        # Feature specification
│       ├── plan.md        # Implementation plan
│       └── ...
├── README.md              # Project documentation
└── requirements-dev.txt   # Development dependencies
```

---

## Basic Usage

### Operation 1: Add a Task

**Menu Option**: `1`

**Steps**:
1. Select option `1` from the main menu
2. Enter task description when prompted
3. Press Enter

**Example**:
```
Select option (1-6): 1
Enter task description: Write unit tests
Task added successfully! (ID: 2)
```

**Tips**:
- Descriptions can be any length
- Unicode characters supported (emoji, accents, etc.)
- Empty descriptions are rejected

---

### Operation 2: View All Tasks

**Menu Option**: `2`

**Steps**:
1. Select option `2` from the main menu
2. Review the task table

**Example (with tasks)**:
```
Select option (1-6): 2

ID   | Description                              | Status
------------------------------------------------------------
1    | Complete Phase I implementation          | Incomplete
2    | Write unit tests                         | Incomplete
3    | Create documentation                     | Complete
```

**Example (empty list)**:
```
Select option (1-6): 2

No tasks yet. Add your first task!
```

**Tips**:
- Tasks shown in creation order
- Status shows "Complete" or "Incomplete"
- Long descriptions are truncated with ellipsis

---

### Operation 3: Update a Task

**Menu Option**: `3`

**Steps**:
1. Select option `3` from the main menu
2. Enter the task ID when prompted
3. Enter the new description
4. Press Enter

**Example**:
```
Select option (1-6): 3
Enter task ID: 1
Enter new description: Complete Phase I implementation and testing
Task updated successfully!
```

**Tips**:
- Get task ID from "View tasks" (option 2)
- Completed status is preserved
- New description cannot be empty

---

### Operation 4: Delete a Task

**Menu Option**: `4`

**Steps**:
1. Select option `4` from the main menu
2. Enter the task ID when prompted
3. Press Enter

**Example**:
```
Select option (1-6): 4
Enter task ID: 2
Task deleted successfully
```

**Tips**:
- Deletion is permanent (no undo)
- Deleted task IDs are never reused
- Verify ID with "View tasks" before deleting

---

### Operation 5: Mark Task as Complete

**Menu Option**: `5`

**Steps**:
1. Select option `5` from the main menu
2. Enter the task ID when prompted
3. Press Enter

**Example**:
```
Select option (1-6): 5
Enter task ID: 1
Task marked as complete!
```

**If Already Complete**:
```
Select option (1-6): 5
Enter task ID: 1
Task already completed
```

**Tips**:
- You can mark a task complete multiple times (no error)
- Status updates immediately
- View tasks (option 2) to verify completion

---

### Operation 6: Exit Application

**Menu Option**: `6`

**Steps**:
1. Select option `6` from the main menu

**Example**:
```
Select option (1-6): 6
Goodbye!
```

**Important**: All tasks are stored in memory only. When you exit, all tasks are lost. This is expected behavior for Phase I.

---

## Common Workflows

### Workflow 1: Daily Task Management

**Scenario**: Manage your daily coding tasks

```
1. Launch app: python src/main.py
2. Add tasks:
   - Option 1 → "Review pull requests"
   - Option 1 → "Write documentation"
   - Option 1 → "Fix bug #42"
3. View tasks: Option 2
4. Complete tasks as you finish:
   - Option 5 → ID 1 (reviewed PRs)
   - Option 5 → ID 3 (fixed bug)
5. View progress: Option 2
6. Exit when done: Option 6
```

**Result**: Visual progress tracking for your daily tasks.

---

### Workflow 2: Learning Project Tracker

**Scenario**: Track learning objectives for a Python course

```
1. Add learning goals:
   - "Complete Python basics"
   - "Learn list comprehensions"
   - "Build a project"
2. Mark complete as you learn:
   - Complete "Python basics"
   - Complete "list comprehensions"
3. Update goals as understanding evolves:
   - Update "Build a project" to "Build a todo app with tests"
4. Review accomplishments: View tasks
```

**Result**: Track learning progress and update goals as you progress.

---

### Workflow 3: Sprint Planning (Short-Term)

**Scenario**: Plan tasks for a 1-2 hour coding session

```
1. Add sprint tasks:
   - "Set up project structure"
   - "Implement add_task function"
   - "Write unit tests"
   - "Run PEP8 linter"
2. Work through tasks in order
3. Mark complete as you go
4. View remaining tasks periodically
5. Exit when session ends (tasks lost - expected)
```

**Result**: Focus tool for short coding sessions (no long-term persistence needed).

---

## Error Handling Examples

### Invalid Menu Selection

**Input**: `9` or `abc` or `!@#`

**Output**:
```
Invalid option. Please select a number from the menu
```

**Action**: Returns to menu, try again with 1-6

---

### Empty Task Description

**Input**: Empty string or whitespace only

**Output**:
```
Description cannot be empty
```

**Action**: Returns to menu, try again with non-empty description

---

### Invalid Task ID

**Scenario 1**: Non-numeric input (e.g., `abc`)

**Output**:
```
Invalid input. Please enter a numeric task ID
```

**Scenario 2**: Task doesn't exist (e.g., ID `999`)

**Output**:
```
Task not found. Please enter a valid task ID
```

**Action**: Returns to menu, use "View tasks" to find valid IDs

---

### No Tasks Available

**Scenario**: Try to update/delete/complete when task list is empty

**Output**:
```
No tasks available. Add a task first
```

**Action**: Returns to menu, add tasks using option 1

---

## Testing Your Installation

### Run All Tests

```bash
pytest tests/ -v
```

**Expected Output**:
```
tests/test_todo.py::test_add_task PASSED                      [  6%]
tests/test_todo.py::test_get_all_tasks PASSED                 [ 13%]
tests/test_todo.py::test_get_task_by_id PASSED                [ 20%]
tests/test_todo.py::test_update_task PASSED                   [ 26%]
tests/test_todo.py::test_delete_task PASSED                   [ 33%]
tests/test_todo.py::test_mark_task_complete PASSED            [ 40%]
...
======================== 15 passed in 0.30s =========================
```

### Run Specific Test File

```bash
pytest tests/test_todo.py -v
```

### Run Single Test

```bash
pytest tests/test_todo.py::test_add_task -v
```

---

## Troubleshooting

### Issue: `python: command not found`

**Solution**: Try `python3` instead:
```bash
python3 src/main.py
```

Or install Python from https://www.python.org/downloads/

---

### Issue: `ModuleNotFoundError: No module named 'src'`

**Solution**: Ensure you're in the `phase-1` directory:
```bash
pwd  # Should show .../phase-1
cd phase-1  # If not in the right directory
python src/main.py
```

---

### Issue: `pytest: command not found`

**Solution**: Install pytest:
```bash
pip install pytest
# or
pip3 install pytest
```

---

### Issue: Tasks disappear after exiting

**Expected Behavior**: Phase I uses in-memory storage only. Tasks are lost when the application exits. This is by design.

**Workaround**: Keep the application running during your work session, or wait for Phase II (database persistence).

---

### Issue: Long descriptions are cut off in view

**Expected Behavior**: Descriptions longer than 40 characters are truncated with `...` for display formatting.

**Workaround**: Keep descriptions concise, or update the task to view full text (shows in update prompt).

---

## Keyboard Shortcuts

**Note**: No special keyboard shortcuts. All interaction via menu numbers and text input.

**Tips**:
- `Ctrl+C` (or `Cmd+C` on Mac): Emergency exit (not graceful)
- Use option `6` for clean exit instead

---

## Limitations (Phase I)

This is Phase I (MVP) with intentional limitations:

- ❌ **No data persistence**: Tasks lost on exit
- ❌ **No undo/redo**: Deletions permanent
- ❌ **No task search**: Must scroll through view
- ❌ **No task filtering**: Can't filter by status
- ❌ **No task sorting**: Always creation order
- ❌ **No priorities or due dates**: Simple descriptions only
- ❌ **No categories or tags**: Flat task list
- ❌ **No multi-user support**: Single session only

**Future Phases**:
- **Phase II**: Web UI + database persistence
- **Phase III**: AI-powered chatbot interface
- **Phase IV**: Kubernetes deployment
- **Phase V**: Cloud deployment with event streaming

---

## Next Steps

After completing this quickstart:

1. **Explore the code**: Read `src/main.py`, `src/todo.py`, `src/utils.py`
2. **Run the tests**: `pytest tests/ -v`
3. **Read the spec**: `specs/001-console-todo/spec.md`
4. **Review the plan**: `specs/001-console-todo/plan.md`
5. **Build enhancements**: Try adding features (save to file, search, etc.)

---

## Getting Help

**Documentation**:
- Feature Specification: `specs/001-console-todo/spec.md`
- Implementation Plan: `specs/001-console-todo/plan.md`
- Data Model: `specs/001-console-todo/data-model.md`
- CLI Interface: `specs/001-console-todo/contracts/cli-interface.md`

**Code Examples**:
All operations are implemented in `src/` directory with clear function names and docstrings.

---

## Summary

You now know how to:

- ✅ Launch the console todo app
- ✅ Add tasks with descriptions
- ✅ View all tasks and their status
- ✅ Update task descriptions
- ✅ Delete tasks
- ✅ Mark tasks as complete
- ✅ Exit the application gracefully
- ✅ Handle common errors
- ✅ Run tests to verify functionality

**Total Time**: ~5 minutes from installation to first completed task.

**Next**: Start managing your tasks or explore the codebase to understand the implementation!
