# CLI Interface Contract: Console Todo App

**Feature**: Console Todo App (Phase I)
**Date**: 2026-01-07
**Version**: 1.0

## Overview

This document defines the command-line interface contract for the console todo application. It specifies the exact menu structure, prompts, user inputs, outputs, and error messages to ensure consistent user experience.

---

## Main Menu

### Display Format

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

### Menu Behavior

- **Display Timing**: After every operation completion and on startup
- **Input Prompt**: `Select option (1-6): ` (with space after colon)
- **Valid Options**: `"1"`, `"2"`, `"3"`, `"4"`, `"5"`, `"6"` (as strings)
- **Invalid Input Handling**: Display error message and re-display menu
- **Exit Condition**: Option `"6"` terminates application

### Error Messages for Invalid Menu Selection

**Input**: Any value not in `["1", "2", "3", "4", "5", "6"]`

**Output**:
```
Invalid option. Please select a number from the menu
```

**Behavior**: Return to menu display

---

## Operation 1: Add Task

### Flow Diagram

```
Main Menu
    → User selects "1"
    → Display prompt: "Enter task description: "
    → User enters description
    → Validate description (non-empty)
    → If valid: Create task, display success
    → If invalid: Display error
    → Return to Main Menu
```

### Prompts

**Description Prompt**:
```
Enter task description:
```

### User Input

- **Expected**: Non-empty string (any text)
- **Validation**: Must have at least one non-whitespace character after trimming
- **Accepted**: All Unicode characters, special symbols, numbers, any length

### Success Output

```
Task added successfully! (ID: {task_id})
```

**Example**:
```
Task added successfully! (ID: 1)
```

### Error Outputs

**Empty Description** (blank input or whitespace only):
```
Description cannot be empty
```

### Complete Example Session

```
=== Todo App ===
1. Add task
2. View tasks
3. Update task
4. Delete task
5. Mark task as complete
6. Exit

Select option (1-6): 1
Enter task description: Review Python documentation
Task added successfully! (ID: 1)

=== Todo App ===
[menu repeats...]
```

---

## Operation 2: View Tasks

### Flow Diagram

```
Main Menu
    → User selects "2"
    → Check if tasks list is empty
    → If empty: Display empty state message
    → If not empty: Display task table
    → Return to Main Menu
```

### Empty State Output

**Condition**: No tasks in the task list

**Output**:
```
No tasks yet. Add your first task!
```

### Task Table Output

**Format**:
```
ID   | Description                              | Status
------------------------------------------------------------
{id}  | {description}                            | {status}
```

**Field Specifications**:
- **ID**: Left-aligned, 4 characters wide
- **Description**: Left-aligned, 40 characters wide (truncate with ellipsis if longer)
- **Status**: Left-aligned, 10 characters wide (`"Complete"` or `"Incomplete"`)
- **Separator**: 60 dashes between header and data rows

**Status Values**:
- `"Complete"`: If `completed == True`
- `"Incomplete"`: If `completed == False`

### Complete Example Session (with tasks)

```
Select option (1-6): 2

ID   | Description                              | Status
------------------------------------------------------------
1    | Review Python documentation              | Incomplete
2    | Write unit tests                         | Complete
3    | Create README                            | Incomplete

=== Todo App ===
[menu repeats...]
```

### Complete Example Session (empty)

```
Select option (1-6): 2

No tasks yet. Add your first task!

=== Todo App ===
[menu repeats...]
```

---

## Operation 3: Update Task

### Flow Diagram

```
Main Menu
    → User selects "3"
    → Check if tasks list is empty
    → If empty: Display "No tasks available" message
    → Display prompt: "Enter task ID: "
    → User enters task ID
    → Validate ID (numeric, positive)
    → If invalid: Display error, return to menu
    → Check if task exists
    → If not found: Display error, return to menu
    → Display prompt: "Enter new description: "
    → User enters description
    → Validate description (non-empty)
    → If valid: Update task, display success
    → If invalid: Display error
    → Return to Main Menu
```

### Prompts

**Task ID Prompt**:
```
Enter task ID:
```

**New Description Prompt**:
```
Enter new description:
```

### User Inputs

**Task ID**:
- **Expected**: Positive integer as string
- **Validation**: Must be numeric and exist in task list

**New Description**:
- **Expected**: Non-empty string
- **Validation**: Must have at least one non-whitespace character after trimming

### Success Output

```
Task updated successfully!
```

### Error Outputs

**No Tasks Available** (empty task list):
```
No tasks available. Add a task first
```

**Invalid Task ID Format** (non-numeric input):
```
Invalid input. Please enter a numeric task ID
```

**Task Not Found** (ID doesn't exist):
```
Task not found. Please enter a valid task ID
```

**Empty Description**:
```
Description cannot be empty
```

### Complete Example Session

```
Select option (1-6): 3
Enter task ID: 1
Enter new description: Review Python documentation and write examples
Task updated successfully!

=== Todo App ===
[menu repeats...]
```

---

## Operation 4: Delete Task

### Flow Diagram

```
Main Menu
    → User selects "4"
    → Check if tasks list is empty
    → If empty: Display "No tasks available" message
    → Display prompt: "Enter task ID: "
    → User enters task ID
    → Validate ID (numeric, positive)
    → If invalid: Display error, return to menu
    → Check if task exists
    → If not found: Display error, return to menu
    → Delete task, display success
    → Return to Main Menu
```

### Prompts

**Task ID Prompt**:
```
Enter task ID:
```

### User Input

**Task ID**:
- **Expected**: Positive integer as string
- **Validation**: Must be numeric and exist in task list

### Success Output

```
Task deleted successfully
```

### Error Outputs

**No Tasks Available** (empty task list):
```
No tasks available. Add a task first
```

**Invalid Task ID Format**:
```
Invalid input. Please enter a numeric task ID
```

**Task Not Found**:
```
Task not found. Please enter a valid task ID
```

### Complete Example Session

```
Select option (1-6): 4
Enter task ID: 2
Task deleted successfully

=== Todo App ===
[menu repeats...]
```

---

## Operation 5: Mark Task as Complete

### Flow Diagram

```
Main Menu
    → User selects "5"
    → Check if tasks list is empty
    → If empty: Display "No tasks available" message
    → Display prompt: "Enter task ID: "
    → User enters task ID
    → Validate ID (numeric, positive)
    → If invalid: Display error, return to menu
    → Check if task exists
    → If not found: Display error, return to menu
    → Check if already complete
    → If already complete: Display "already completed" message
    → If not complete: Mark complete, display success
    → Return to Main Menu
```

### Prompts

**Task ID Prompt**:
```
Enter task ID:
```

### User Input

**Task ID**:
- **Expected**: Positive integer as string
- **Validation**: Must be numeric and exist in task list

### Success Output

```
Task marked as complete!
```

### Informational Output (Already Complete)

```
Task already completed
```

**Note**: This is informational, not an error. Operation succeeds (idempotent behavior).

### Error Outputs

**No Tasks Available** (empty task list):
```
No tasks available. Add a task first
```

**Invalid Task ID Format**:
```
Invalid input. Please enter a numeric task ID
```

**Task Not Found**:
```
Task not found. Please enter a valid task ID
```

### Complete Example Session (Success)

```
Select option (1-6): 5
Enter task ID: 1
Task marked as complete!

=== Todo App ===
[menu repeats...]
```

### Complete Example Session (Already Complete)

```
Select option (1-6): 5
Enter task ID: 1
Task already completed

=== Todo App ===
[menu repeats...]
```

---

## Operation 6: Exit

### Flow Diagram

```
Main Menu
    → User selects "6"
    → Display goodbye message
    → Terminate application (exit code 0)
```

### Output

```
Goodbye!
```

### Behavior

- Display "Goodbye!" message
- Exit application cleanly with `sys.exit(0)` or equivalent
- No return to menu (application terminates)

### Complete Example Session

```
Select option (1-6): 6
Goodbye!
```

---

## Input Handling Standards

### Whitespace Handling

- **Menu Choices**: Strip leading/trailing whitespace before validation
- **Task Descriptions**: Strip leading/trailing whitespace, validate non-empty after stripping
- **Task IDs**: Strip leading/trailing whitespace before parsing to integer

### Case Sensitivity

- **Menu Choices**: Exact match (`"1"`, not `"one"` or `"ONE"`)
- **Task Descriptions**: Preserve user input (case-sensitive)

### Special Characters

- **Task Descriptions**: Accept all Unicode characters (emoji, accents, CJK, etc.)
- **Task IDs**: Accept only numeric digits (0-9)

### Input Length

- **Menu Choices**: Single character expected (but validate full input)
- **Task Descriptions**: No maximum length (Python string limits apply, ~2GB)
- **Task IDs**: Up to reasonable integer size (Python int is unbounded)

---

## Error Message Standards

### Consistency

All error messages follow the pattern:
- Clear problem statement
- Actionable guidance (what to do instead)
- No jargon or technical details
- Friendly, helpful tone

### Examples

**Good** (Specific, Actionable):
```
Invalid input. Please enter a numeric task ID
```

**Bad** (Vague, Unhelpful):
```
Error: Invalid input
```

**Good** (Explains empty state):
```
No tasks yet. Add your first task!
```

**Bad** (Terse):
```
No tasks
```

### Error Display

- Display error message immediately after invalid input
- Return to main menu (don't exit or loop on same operation)
- Don't display stack traces or debug information to users

---

## Success Message Standards

### Format

- Clear confirmation of action taken
- Include relevant details (task ID for adds)
- Concise (one line)
- Positive tone

### Examples

```
Task added successfully! (ID: 1)
Task updated successfully!
Task deleted successfully
Task marked as complete!
```

---

## Complete User Journey Examples

### Journey 1: Add and View Task

```
=== Todo App ===
1. Add task
2. View tasks
3. Update task
4. Delete task
5. Mark task as complete
6. Exit

Select option (1-6): 1
Enter task description: Learn Python
Task added successfully! (ID: 1)

=== Todo App ===
1. Add task
2. View tasks
3. Update task
4. Delete task
5. Mark task as complete
6. Exit

Select option (1-6): 2

ID   | Description                              | Status
------------------------------------------------------------
1    | Learn Python                             | Incomplete

=== Todo App ===
[menu repeats...]
```

### Journey 2: Complete Task Workflow

```
Select option (1-6): 1
Enter task description: Write tests
Task added successfully! (ID: 1)

[menu]

Select option (1-6): 5
Enter task ID: 1
Task marked as complete!

[menu]

Select option (1-6): 2

ID   | Description                              | Status
------------------------------------------------------------
1    | Write tests                              | Complete

[menu]
```

### Journey 3: Error Handling

```
Select option (1-6): 9
Invalid option. Please select a number from the menu

[menu]

Select option (1-6): 3
Enter task ID: abc
Invalid input. Please enter a numeric task ID

[menu]

Select option (1-6): 3
Enter task ID: 999
Task not found. Please enter a valid task ID

[menu]
```

---

## Testing Checklist

### Menu Tests

- [ ] Display menu on startup
- [ ] Display menu after each operation
- [ ] Accept valid options (1-6)
- [ ] Reject invalid options (0, 7, letters, symbols)
- [ ] Handle whitespace in menu input
- [ ] Exit cleanly on option 6

### Add Task Tests

- [ ] Add task with valid description
- [ ] Reject empty description
- [ ] Accept Unicode characters
- [ ] Display correct task ID
- [ ] Return to menu after add

### View Tasks Tests

- [ ] Display empty state when no tasks
- [ ] Display task table with tasks
- [ ] Show correct status (Complete/Incomplete)
- [ ] Handle long descriptions (truncation)
- [ ] Return to menu after view

### Update Task Tests

- [ ] Reject update when no tasks exist
- [ ] Reject non-numeric task ID
- [ ] Reject non-existent task ID
- [ ] Update description successfully
- [ ] Reject empty new description
- [ ] Preserve completed status
- [ ] Return to menu after update

### Delete Task Tests

- [ ] Reject delete when no tasks exist
- [ ] Reject non-numeric task ID
- [ ] Reject non-existent task ID
- [ ] Delete task successfully
- [ ] Task no longer appears in view
- [ ] Return to menu after delete

### Mark Complete Tests

- [ ] Reject mark when no tasks exist
- [ ] Reject non-numeric task ID
- [ ] Reject non-existent task ID
- [ ] Mark incomplete task as complete
- [ ] Handle already-complete task (idempotent)
- [ ] Status shows "Complete" in view
- [ ] Return to menu after mark

### Exit Tests

- [ ] Display goodbye message
- [ ] Terminate application cleanly
- [ ] Exit code 0

---

## Implementation Notes

### Menu Display Function

```python
def display_menu():
    print("\n=== Todo App ===")
    print("1. Add task")
    print("2. View tasks")
    print("3. Update task")
    print("4. Delete task")
    print("5. Mark task as complete")
    print("6. Exit")
    print()  # Blank line before prompt
```

### Menu Input Handling

```python
choice = input("Select option (1-6): ").strip()
```

### Operation Dispatch

```python
operations = {
    "1": add_task_handler,
    "2": view_tasks_handler,
    "3": update_task_handler,
    "4": delete_task_handler,
    "5": mark_complete_handler,
    "6": exit_handler
}

operation = operations.get(choice)
if operation:
    operation()
else:
    print("Invalid option. Please select a number from the menu")
```

---

## Summary

This CLI interface contract ensures:

- ✅ Consistent user experience across all operations
- ✅ Clear, helpful error messages
- ✅ Graceful handling of all invalid inputs
- ✅ Predictable flow (always returns to menu except on exit)
- ✅ Alignment with specification requirements
- ✅ Testable behavior with explicit inputs/outputs
