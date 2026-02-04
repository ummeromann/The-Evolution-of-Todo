# Data Model: Console Todo App

**Feature**: Console Todo App (Phase I)
**Date**: 2026-01-07
**Version**: 1.0

## Overview

This document defines the data model for Phase I of the multi-phase Todo application. The model uses in-memory Python data structures (list of dictionaries) and is designed to map directly to database schemas in Phase II.

---

## Entity: Task

### Description

Represents a single todo item with a unique identifier, description text, completion status, and creation timestamp.

### In-Memory Representation

```python
{
    "id": int,
    "description": str,
    "completed": bool,
    "created": str  # ISO 8601 timestamp
}
```

### Field Specifications

| Field | Type | Required | Constraints | Default | Description |
|-------|------|----------|-------------|---------|-------------|
| `id` | `int` | Yes | Positive integer, unique within session | Auto-generated | Unique task identifier, sequential starting at 1 |
| `description` | `str` | Yes | Non-empty string, min 1 character | User-provided | Task description text, supports Unicode |
| `completed` | `bool` | Yes | `True` or `False` | `False` | Completion status indicator |
| `created` | `str` | No | ISO 8601 format (`YYYY-MM-DDTHH:MM:SS`) | Current timestamp | Creation timestamp for reference |

### Validation Rules

**ID Validation**:
- MUST be a positive integer (`id >= 1`)
- MUST be unique within the task list
- MUST NOT be reused after task deletion
- Generated sequentially using global counter

**Description Validation**:
- MUST NOT be empty string
- Whitespace-only strings NOT allowed (trimmed before validation)
- No maximum length constraint (Python string limits apply)
- All Unicode characters supported

**Completed Validation**:
- MUST be boolean (`True` or `False`)
- New tasks default to `False` (incomplete)
- Can transition from `False` to `True` (mark complete)
- Idempotent: marking completed task as complete is allowed (no-op)

**Created Validation**:
- MUST be valid ISO 8601 timestamp if provided
- Auto-generated using `datetime.now().isoformat()` if not provided
- Optional field (can be omitted in minimal implementations)

### Example Instances

**New Task** (just created):
```python
{
    "id": 1,
    "description": "Review Python documentation",
    "completed": False,
    "created": "2026-01-07T15:30:00"
}
```

**Completed Task**:
```python
{
    "id": 2,
    "description": "Write unit tests for CRUD operations",
    "completed": True,
    "created": "2026-01-07T14:00:00"
}
```

**Task with Long Description**:
```python
{
    "id": 3,
    "description": "Implement comprehensive error handling for all edge cases including invalid task IDs, empty descriptions, and menu input validation",
    "completed": False,
    "created": "2026-01-07T16:45:00"
}
```

**Task with Unicode**:
```python
{
    "id": 4,
    "description": "学习 Python 编程 (Learn Python programming)",
    "completed": False,
    "created": "2026-01-07T17:00:00"
}
```

---

## Global State

### Task List

**Variable**: `tasks`
**Type**: `list[dict]`
**Initial Value**: `[]` (empty list)

**Description**: Master list holding all tasks for the current session. Tasks are appended during creation and removed during deletion. Order is preserved (creation order maintained).

**Example**:
```python
tasks = [
    {"id": 1, "description": "Task one", "completed": False, "created": "2026-01-07T10:00:00"},
    {"id": 2, "description": "Task two", "completed": True, "created": "2026-01-07T10:30:00"},
    {"id": 3, "description": "Task three", "completed": False, "created": "2026-01-07T11:00:00"}
]
```

### ID Counter

**Variable**: `next_task_id`
**Type**: `int`
**Initial Value**: `1`

**Description**: Global counter tracking the next available task ID. Increments after each task creation. Never decreases, ensuring unique IDs even after deletions.

**Behavior**:
```python
# Initial state
next_task_id = 1
tasks = []

# After adding first task
next_task_id = 2
tasks = [{"id": 1, ...}]

# After deleting task 1 and adding task 2
next_task_id = 3
tasks = [{"id": 2, ...}]  # ID 1 never reused
```

---

## State Transitions

### Task Creation Flow

```
[User Input: Description]
    → Validate Description (non-empty)
    → Create Task (id=next_task_id, completed=False)
    → Append to tasks list
    → Increment next_task_id
    → Return new task ID
```

**Preconditions**: Description is non-empty string
**Postconditions**: Task exists in tasks list with unique ID, counter incremented

### Mark Complete Flow

```
[User Input: Task ID]
    → Validate ID (numeric, exists in tasks)
    → Find task by ID
    → Set completed=True
    → Return success
```

**Preconditions**: Task with given ID exists
**Postconditions**: Task's completed field is True
**Idempotency**: If task already complete, operation succeeds (no-op)

### Update Description Flow

```
[User Input: Task ID, New Description]
    → Validate ID (numeric, exists)
    → Validate Description (non-empty)
    → Find task by ID
    → Update description field
    → Preserve completed and created fields
    → Return success
```

**Preconditions**: Task exists, new description is non-empty
**Postconditions**: Task description updated, other fields unchanged

### Delete Task Flow

```
[User Input: Task ID]
    → Validate ID (numeric, exists)
    → Find task in list
    → Remove from tasks list
    → Do NOT decrement next_task_id (preserve ID uniqueness)
    → Return success
```

**Preconditions**: Task with given ID exists
**Postconditions**: Task removed from list, ID permanently retired

---

## Relationships

**Phase I**: No relationships (single entity, flat structure)

**Future Phases**:
- **Phase II**: Task → User (many-to-one, foreign key relationship)
- **Phase II**: Task → Category (many-to-one, optional)
- **Phase III**: Task → AI Intent (one-to-many, operation history)

---

## Database Migration Path (Phase II Preview)

### SQLModel Schema (Phase II)

```python
from sqlmodel import Field, SQLModel
from datetime import datetime

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    description: str = Field(min_length=1)
    completed: bool = Field(default=False)
    created: datetime = Field(default_factory=datetime.now)
    user_id: int | None = Field(default=None, foreign_key="user.id")  # Phase II
```

### Migration Notes

- `id`: Auto-increment primary key (database handles generation)
- `description`: VARCHAR with NOT NULL constraint
- `completed`: BOOLEAN with default FALSE
- `created`: TIMESTAMP with default NOW()
- Additional fields (user_id, category, etc.) added in Phase II

**Phase I Compatibility**: The dictionary structure directly maps to SQLModel fields, enabling seamless migration without data transformation logic.

---

## Data Integrity Rules

### Uniqueness Constraints

- **Task ID**: MUST be unique within session (enforced by counter)
- No duplicate task IDs allowed
- Deleted IDs MUST NOT be reused

### Referential Integrity

- No foreign keys in Phase I (single entity)
- Phase II will add User relationship with CASCADE delete

### Business Rules

1. **Task Creation**:
   - Description MUST be non-empty after trimming whitespace
   - New tasks MUST default to incomplete status
   - ID MUST be auto-assigned (users cannot specify ID)

2. **Task Completion**:
   - Can only mark existing tasks as complete
   - Marking already-complete task is allowed (idempotent)
   - Cannot "uncomplete" a task in Phase I (future feature)

3. **Task Update**:
   - Can only update description, not ID or created timestamp
   - Completed status preserved during description updates
   - Updated description MUST be non-empty

4. **Task Deletion**:
   - Can only delete existing tasks
   - Deletion is permanent (no undo in Phase I)
   - Deleted task IDs are permanently retired

---

## Query Patterns

### Get All Tasks

```python
def get_all_tasks() -> list[dict]:
    """Return all tasks in creation order"""
    return tasks.copy()  # Return copy to prevent external modification
```

**Complexity**: O(n) where n = number of tasks
**Returns**: Shallow copy of tasks list

### Get Task by ID

```python
def get_task_by_id(task_id: int) -> dict | None:
    """Find task by ID, return None if not found"""
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None
```

**Complexity**: O(n) linear search (acceptable for Phase I scale)
**Returns**: Task dictionary or None
**Phase II Optimization**: Database index on ID field for O(1) lookup

### Get Incomplete Tasks (Future)

```python
def get_incomplete_tasks() -> list[dict]:
    """Return all incomplete tasks"""
    return [task for task in tasks if not task["completed"]]
```

**Phase I**: Not required by spec, included for completeness
**Phase II**: Database query with WHERE clause

---

## Performance Considerations

### Phase I (In-Memory)

- **Scale**: Up to ~1000 tasks (reasonable for single session)
- **Lookup**: O(n) linear search (acceptable for small datasets)
- **Memory**: ~100-200 bytes per task (negligible for Phase I)

### Phase II (Database)

- **Scale**: Thousands to millions of tasks
- **Lookup**: O(1) with database indexing on ID
- **Persistence**: Transactional guarantees via PostgreSQL

---

## Edge Cases & Error Handling

| Edge Case | Handling |
|-----------|----------|
| Empty task list | Return friendly message "No tasks yet" |
| Task ID doesn't exist | Return None, caller displays error |
| Empty description | Validation fails, reject before creation |
| Very long description (10,000+ chars) | Accept (Python handles, Phase II may add limits) |
| Special characters in description | Accept all Unicode characters |
| Deleted task ID reused | NEVER - counter never decrements |
| Concurrent modifications | Not applicable (single-user, single-session) |

---

## Testing Checklist

- [ ] Create task with valid description → success
- [ ] Create task with empty description → validation error
- [ ] Get task by valid ID → returns task
- [ ] Get task by invalid ID → returns None
- [ ] Update task with valid description → success
- [ ] Update task with empty description → validation error
- [ ] Mark task as complete → completed=True
- [ ] Mark already-complete task → no error (idempotent)
- [ ] Delete task → removed from list
- [ ] Delete non-existent task → validation error
- [ ] Verify ID uniqueness after deletions → no ID reuse
- [ ] Very long descriptions → accepted
- [ ] Unicode in descriptions → accepted

---

## Summary

The Phase I data model uses a simple, educational in-memory structure (list of dictionaries) that:

- ✅ Meets all Phase I requirements (in-memory CRUD)
- ✅ Aligns with constitutional principles (simplicity, clarity)
- ✅ Prepares for Phase II migration (direct SQLModel mapping)
- ✅ Supports all functional requirements from specification
- ✅ Handles edge cases gracefully with clear validation rules
