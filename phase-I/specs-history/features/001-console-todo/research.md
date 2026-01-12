# Research: Console Todo App Technical Decisions

**Feature**: Console Todo App (Phase I)
**Date**: 2026-01-07
**Status**: Complete

## Overview

This document captures research findings and technical decisions made during the planning phase for the in-memory Python console todo application. All decisions prioritize simplicity, educational value, and alignment with constitutional requirements for Phase I.

---

## Research Area 1: Task Data Structure

### Question
How should we store tasks in memory to balance simplicity, maintainability, and future compatibility with Phase II (database persistence)?

### Options Evaluated

**Option A: List of Dictionaries**
```python
tasks = [
    {"id": 1, "description": "Task 1", "completed": False},
    {"id": 2, "description": "Task 2", "completed": True}
]
```

**Pros**:
- Simple and Pythonic
- Self-documenting with named fields
- Easy to iterate and display
- Direct mapping to JSON/database records
- Flexible for adding fields

**Cons**:
- No type enforcement (could add invalid fields)
- Slightly more memory overhead vs tuples
- No attribute access (must use dict keys)

**Option B: Namedtuples**
```python
from collections import namedtuple
Task = namedtuple('Task', ['id', 'description', 'completed'])
tasks = [Task(1, "Task 1", False), Task(2, "Task 2", True)]
```

**Pros**:
- Immutable (prevents accidental modification)
- Memory efficient
- Attribute access (`task.id`)
- Type-safe field names

**Cons**:
- Immutable makes updates difficult (must create new tuple)
- Less intuitive for beginners
- No direct JSON serialization
- Awkward CRUD operations

**Option C: Custom Task Class**
```python
class Task:
    def __init__(self, id, description, completed=False):
        self.id = id
        self.description = description
        self.completed = completed
```

**Pros**:
- Full OOP encapsulation
- Can add methods (validate, to_dict, etc.)
- Attribute access
- Clear intent

**Cons**:
- Over-engineering for Phase I scope
- More boilerplate code
- Increased complexity for beginners
- Constitutional concern: unnecessary abstraction

**Option D: List of Lists**
```python
tasks = [
    [1, "Task 1", False],
    [2, "Task 2", True]
]
```

**Pros**:
- Maximum memory efficiency
- Simple to implement

**Cons**:
- Not self-documenting (which index is what?)
- Error-prone (easy to swap fields)
- Poor readability and maintainability
- No field name validation

### Decision: **Option A - List of Dictionaries**

**Rationale**:
- **Simplicity**: Easy to understand for beginner/intermediate Python developers (target audience)
- **Educational Value**: Teaches dictionary usage, aligns with JSON/NoSQL concepts
- **Future Compatibility**: Direct mapping to SQLModel/database schemas in Phase II
- **Constitutional Compliance**: Avoids unnecessary abstraction (Principle II: Clarity)
- **Flexibility**: Easy to add `created` timestamp or other fields without refactoring

**Implementation Pattern**:
```python
tasks = []  # Global task list
next_task_id = 1  # Counter for unique IDs

def create_task(description):
    global next_task_id
    task = {
        "id": next_task_id,
        "description": description,
        "completed": False,
        "created": datetime.now().isoformat()
    }
    tasks.append(task)
    next_task_id += 1
    return task["id"]
```

---

## Research Area 2: ID Generation Strategy

### Question
What's the best approach for generating unique task IDs in an in-memory system?

### Options Evaluated

**Option A: Sequential Integer Counter**
- Start at 1, increment for each new task
- Track with global `next_task_id` variable

**Pros**:
- User-friendly (easy to type/remember)
- Predictable and intuitive
- Aligns with database auto-increment
- Simple implementation

**Cons**:
- Gaps after deletions (ID 1, 3, 5 if 2 and 4 deleted)
- Not globally unique (resets each session)

**Option B: UUID (Universal Unique Identifier)**
- Use `uuid.uuid4()` for random UUIDs

**Pros**:
- Guaranteed uniqueness
- Collision-resistant
- Industry standard

**Cons**:
- Poor UX (typing `550e8400-e29b-41d4-a716-446655440000` is painful)
- Overkill for single-session app
- Not educational priority
- Violates simplicity principle

**Option C: Index-Based (Position in List)**
- Use list index as ID (0, 1, 2, ...)

**Pros**:
- No extra tracking needed
- Always sequential without gaps

**Cons**:
- **CRITICAL FLAW**: IDs change when items deleted
  - Delete task 0 → task 1 becomes task 0 (breaks user expectations)
- Violates data integrity principle
- Confusing UX

**Option D: Timestamp-Based**
- Use Unix timestamp (milliseconds since epoch)

**Pros**:
- Naturally unique (if no concurrent ops)
- Sortable by creation time

**Cons**:
- Not user-friendly for typing
- Collision risk in rare cases
- No clear advantage over counter

### Decision: **Option A - Sequential Integer Counter**

**Rationale**:
- **User Experience**: Typing "1", "2", "3" is far better than UUIDs
- **Educational Alignment**: Teaches auto-increment concept used in databases
- **Constitutional Compliance**: Simplicity principle (IV: Scalability - prepares for DB auto-increment)
- **Acceptable Trade-off**: ID gaps after deletion are acceptable (users understand deleted IDs don't reappear)
- **Implementation Simplicity**: Single integer variable to maintain

**Edge Case Handling**:
- IDs are permanent once assigned (even if task deleted)
- Gaps in sequence are acceptable and expected
- Counter never decreases (maintains uniqueness guarantee)

---

## Research Area 3: Menu Loop Architecture

### Question
How should we structure the main menu loop for clarity, extensibility, and error handling?

### Options Evaluated

**Option A: While Loop with Dispatch Dictionary**
```python
def main():
    operations = {
        "1": add_task,
        "2": view_tasks,
        "6": exit_app
    }
    while True:
        display_menu()
        choice = input("Select: ")
        operation = operations.get(choice, invalid_choice)
        operation()
```

**Pros**:
- Clean separation of concerns
- Easy to add new operations
- Dictionary-based dispatch is Pythonic
- Single point of menu definition

**Cons**:
- Requires function references
- Slightly more complex for absolute beginners

**Option B: If-Elif Chain**
```python
while True:
    display_menu()
    choice = input("Select: ")
    if choice == "1":
        add_task()
    elif choice == "2":
        view_tasks()
    elif choice == "6":
        break
    else:
        print("Invalid choice")
```

**Pros**:
- Simple and direct
- Easy for beginners to understand
- No indirection

**Cons**:
- Long if-elif chains hard to maintain
- Violates DRY if logic repeated
- Difficult to test menu dispatch separately

**Option C: Match-Case (Python 3.10+)**
```python
while True:
    choice = input("Select: ")
    match choice:
        case "1":
            add_task()
        case "2":
            view_tasks()
        case _:
            invalid_choice()
```

**Pros**:
- Modern Python feature
- Clean syntax
- Exhaustiveness checking

**Cons**:
- Requires Python 3.10+ (we have 3.13+, so OK)
- Less familiar to beginners
- Overkill for simple string matching

### Decision: **Option A - While Loop with Dispatch Dictionary**

**Rationale**:
- **Best Practice**: Dictionary dispatch is idiomatic Python
- **Extensibility**: Easy to add operations without modifying loop
- **Testability**: Menu dispatch logic testable separately
- **Educational Value**: Teaches dictionary usage and function references
- **Constitutional Compliance**: Clear structure (Principle II: Clarity)

**Implementation Pattern**:
```python
def main():
    """Main application loop"""
    operations = {
        "1": add_task_handler,
        "2": view_tasks_handler,
        "3": update_task_handler,
        "4": delete_task_handler,
        "5": mark_complete_handler,
        "6": exit_handler
    }

    while True:
        utils.display_menu()
        choice = input("Select option (1-6): ").strip()

        operation = operations.get(choice)
        if operation:
            operation()
        else:
            print("Invalid option. Please select a number from the menu")
```

---

## Research Area 4: Input Validation Strategy

### Question
How should we validate user inputs (task IDs, descriptions, menu choices) consistently across the application?

### Best Practices Researched

**Validation Patterns**:
1. **Centralized validation functions** (utils module)
2. **Return None pattern** for invalid inputs (vs exceptions)
3. **Caller handles error messages** (keeps validation logic pure)
4. **Explicit validation before operations** (fail fast)

**Industry Standards**:
- Validate at system boundaries (user input)
- Use type hints for clarity
- Provide helpful error messages
- Don't crash on invalid input

### Decision: **Centralized Validation with None Pattern**

**Rationale**:
- **DRY Principle**: Reusable validation functions in `utils.py`
- **Testability**: Validation logic tested independently
- **Clarity**: Explicit validation steps in operation functions
- **User-Friendly**: Controlled error messages, no crashes

**Key Validation Functions**:

```python
def validate_task_id(user_input: str) -> int | None:
    """
    Validate and parse task ID from user input.
    Returns integer ID if valid, None if invalid.
    """
    try:
        task_id = int(user_input.strip())
        if task_id < 1:
            return None
        return task_id
    except ValueError:
        return None

def validate_description(text: str) -> str | None:
    """
    Validate task description.
    Returns trimmed text if valid (non-empty), None if invalid.
    """
    trimmed = text.strip()
    if not trimmed:
        return None
    return trimmed
```

**Usage Pattern**:
```python
def update_task_handler():
    user_input = input("Enter task ID: ")
    task_id = validate_task_id(user_input)
    if task_id is None:
        print("Invalid input. Please enter a numeric task ID")
        return

    if not todo.get_task_by_id(task_id):
        print("Task not found. Please enter a valid task ID")
        return

    description = input("Enter new description: ")
    validated_desc = validate_description(description)
    if validated_desc is None:
        print("Description cannot be empty")
        return

    todo.update_task(task_id, validated_desc)
    print("Task updated successfully!")
```

---

## Research Area 5: Error Handling Approach

### Question
Should we use exceptions or return codes for error handling in CRUD operations?

### Options Evaluated

**Option A: Return Codes (bool/None pattern)**
```python
def delete_task(task_id: int) -> bool:
    """Returns True if deleted, False if not found"""
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return True
    return False
```

**Pros**:
- Simple and explicit
- Caller controls error handling
- No exception overhead
- Predictable flow

**Cons**:
- Caller must check return value
- Can't distinguish error types easily

**Option B: Exceptions**
```python
def delete_task(task_id: int):
    """Raises TaskNotFoundError if task doesn't exist"""
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return
    raise TaskNotFoundError(f"Task {task_id} not found")
```

**Pros**:
- Explicit error types
- Separates happy path from error handling
- Pythonic for exceptional conditions

**Cons**:
- Overkill for expected conditions (task not found is common)
- Requires custom exception classes
- More complex for beginners

### Decision: **Option A - Return Codes (bool pattern)**

**Rationale**:
- **Simplicity**: Boolean return values are straightforward
- **Expected Conditions**: Task not found is not exceptional, it's expected
- **Educational Value**: Teaches explicit error checking
- **Constitutional Compliance**: Avoids unnecessary complexity
- **Reserves Exceptions**: Use exceptions only for truly unexpected errors (system failures)

**Pattern**:
```python
# In todo.py
def mark_task_complete(task_id: int) -> bool:
    """Mark task as complete. Returns True if successful, False if not found."""
    task = get_task_by_id(task_id)
    if task is None:
        return False
    task["completed"] = True
    return True

# In main.py handler
def mark_complete_handler():
    task_id = get_validated_task_id()
    if task_id is None:
        return

    success = todo.mark_task_complete(task_id)
    if success:
        print("Task marked as complete!")
    else:
        print("Task not found. Please enter a valid task ID")
```

---

## Research Area 6: Display Formatting

### Question
How should we format the task list for console display without external dependencies?

### Options Evaluated

**Option A: Simple F-String Formatting**
```python
print(f"{task['id']:<4} | {task['description']:<30} | {status:<10}")
```

**Pros**:
- No dependencies (stdlib only)
- Simple and readable
- Sufficient for console output
- Easy to maintain

**Cons**:
- Manual width management
- No automatic column sizing
- Basic appearance

**Option B: External Libraries (tabulate, prettytable)**
```python
from tabulate import tabulate
print(tabulate(data, headers=["ID", "Description", "Status"]))
```

**Pros**:
- Professional appearance
- Automatic column sizing
- Multiple format styles

**Cons**:
- **CONSTITUTIONAL VIOLATION**: External dependency (Phase I requires stdlib only)
- Adds complexity
- Overkill for simple display

**Option C: ASCII Art Boxes**
```
┌────┬──────────────┬──────────┐
│ ID │ Description  │ Status   │
├────┼──────────────┼──────────┤
│ 1  │ Task one     │ Complete │
└────┴──────────────┴──────────┘
```

**Pros**:
- Visually appealing
- Clear boundaries

**Cons**:
- Encoding issues (UTF-8 box characters)
- More complex to implement
- Overkill for educational app

### Decision: **Option A - Simple F-String Formatting**

**Rationale**:
- **Constitutional Compliance**: No external dependencies (stdlib only requirement)
- **Simplicity**: Easy to understand and maintain
- **Sufficient**: Adequate for console display needs
- **Educational**: Teaches string formatting in Python

**Implementation**:
```python
def format_tasks_table(tasks: list[dict]) -> str:
    """Format tasks as a simple table"""
    if not tasks:
        return "No tasks yet. Add your first task!"

    lines = []
    lines.append(f"{'ID':<4} | {'Description':<40} | {'Status':<10}")
    lines.append("-" * 60)

    for task in tasks:
        status = "Complete" if task["completed"] else "Incomplete"
        desc = task["description"][:40]  # Truncate if too long
        lines.append(f"{task['id']:<4} | {desc:<40} | {status:<10}")

    return "\n".join(lines)
```

**Output Example**:
```
ID   | Description                              | Status
------------------------------------------------------------
1    | Review Python documentation              | Incomplete
2    | Write unit tests                         | Complete
3    | Create README                            | Incomplete
```

---

## Summary of Key Decisions

| Decision Area | Choice | Rationale |
|--------------|--------|-----------|
| **Data Structure** | List of dictionaries | Simple, future-compatible, self-documenting |
| **ID Generation** | Sequential integer counter | User-friendly, aligns with DB auto-increment |
| **Menu Loop** | While + dispatch dictionary | Clean, extensible, Pythonic |
| **Input Validation** | Centralized utils with None pattern | DRY, testable, consistent |
| **Error Handling** | Return codes (bool/None) | Simple, explicit, reserves exceptions |
| **Display Format** | F-string formatting | Stdlib only, sufficient, clear |

---

## Constitutional Compliance Verification

All research decisions verified against constitution:

✅ **Principle I (Accuracy)**: Explicit validation ensures correctness
✅ **Principle II (Clarity)**: Modular design with clear responsibilities
✅ **Principle III (Reproducibility)**: No external dependencies, stdlib only
✅ **Principle IV (Scalability)**: Data model compatible with Phase II DB schema
✅ **Principle V (Security)**: Input validation prevents injection/corruption
✅ **Principle VI (Phase Compliance)**: In-memory only, Python stdlib, console interface

---

## Next Steps

1. Proceed to Phase 1: Design & Contracts
2. Create `data-model.md` with detailed Task entity specification
3. Create `contracts/cli-interface.md` with complete menu flows
4. Create `quickstart.md` with setup and usage guide
5. Advance to `/sp.tasks` for task breakdown
