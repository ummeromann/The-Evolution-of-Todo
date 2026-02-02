# MCP Tools Contract

**Feature**: 004-todo-ai-chatbot
**Date**: 2026-02-02

## Overview

This document defines the MCP (Model Context Protocol) tools exposed by the Todo AI Chatbot backend. These tools are invoked by the OpenAI Agent to perform todo operations on behalf of authenticated users.

## Tool Design Principles

1. **Stateless**: Tools receive all required context via parameters
2. **User-Scoped**: All operations filtered by authenticated user_id
3. **Idempotent**: Where possible, repeated calls produce same result
4. **Confirmable**: Return sufficient detail for meaningful user confirmation

---

## Tools

### 1. add_todo

Creates a new todo task for the user.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| description | string | Yes | Task description (1-500 chars) |

**Returns**:
```json
{
  "success": true,
  "task": {
    "id": "uuid",
    "description": "string",
    "is_completed": false,
    "created_at": "iso8601"
  }
}
```

**Error Cases**:
| Condition | Response |
|-----------|----------|
| Empty description | `{"success": false, "error": "Description is required"}` |
| Description > 500 chars | `{"success": false, "error": "Description too long (max 500 characters)"}` |
| Database error | `{"success": false, "error": "Failed to create task"}` |

**Example Agent Instruction**:
> When the user wants to add a task, call `add_todo` with the task description. Confirm creation by stating what was added.

---

### 2. list_todos

Retrieves all todos for the user.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| include_completed | boolean | No | Include completed tasks (default: true) |

**Returns**:
```json
{
  "success": true,
  "tasks": [
    {
      "id": "uuid",
      "description": "string",
      "is_completed": false,
      "created_at": "iso8601"
    }
  ],
  "total": 3,
  "completed_count": 1,
  "pending_count": 2
}
```

**Error Cases**:
| Condition | Response |
|-----------|----------|
| Database error | `{"success": false, "error": "Failed to retrieve tasks"}` |

**Example Agent Instruction**:
> When listing tasks, format them as a numbered list. Indicate which are completed with a checkmark. If no tasks exist, suggest adding one.

---

### 3. complete_todo

Marks a task as completed.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| task_id | string (uuid) | No* | Specific task ID to complete |
| description_match | string | No* | Fuzzy match on task description |

*At least one of `task_id` or `description_match` is required.

**Returns**:
```json
{
  "success": true,
  "task": {
    "id": "uuid",
    "description": "string",
    "is_completed": true,
    "updated_at": "iso8601"
  }
}
```

**Error Cases**:
| Condition | Response |
|-----------|----------|
| No matching task | `{"success": false, "error": "No task found matching your request", "found": false}` |
| Multiple matches | `{"success": false, "error": "Multiple tasks match. Please be more specific.", "matches": [...]}` |
| Already completed | `{"success": true, "task": {...}, "note": "Task was already completed"}` |

**Example Agent Instruction**:
> When completing a task, first try to match by description. If multiple tasks match, ask the user to clarify which one. Confirm completion with the task description.

---

### 4. update_todo

Updates a task's description.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| task_id | string (uuid) | No* | Specific task ID to update |
| description_match | string | No* | Fuzzy match on current description |
| new_description | string | Yes | New task description (1-500 chars) |

*At least one of `task_id` or `description_match` is required.

**Returns**:
```json
{
  "success": true,
  "task": {
    "id": "uuid",
    "description": "new description",
    "is_completed": false,
    "updated_at": "iso8601"
  },
  "previous_description": "old description"
}
```

**Error Cases**:
| Condition | Response |
|-----------|----------|
| No matching task | `{"success": false, "error": "No task found matching your request", "found": false}` |
| Multiple matches | `{"success": false, "error": "Multiple tasks match. Please be more specific.", "matches": [...]}` |
| Empty new description | `{"success": false, "error": "New description is required"}` |
| Description > 500 chars | `{"success": false, "error": "Description too long (max 500 characters)"}` |

**Example Agent Instruction**:
> When updating a task, confirm both the old and new descriptions so the user knows exactly what changed.

---

### 5. delete_todo

Deletes a task permanently.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| task_id | string (uuid) | No* | Specific task ID to delete |
| description_match | string | No* | Fuzzy match on task description |
| delete_completed | boolean | No | Delete all completed tasks |

*At least one parameter is required.

**Returns**:
```json
{
  "success": true,
  "deleted": {
    "id": "uuid",
    "description": "string"
  }
}
```

For bulk delete (delete_completed=true):
```json
{
  "success": true,
  "deleted_count": 3,
  "deleted_tasks": [
    {"id": "uuid", "description": "string"},
    ...
  ]
}
```

**Error Cases**:
| Condition | Response |
|-----------|----------|
| No matching task | `{"success": false, "error": "No task found matching your request", "found": false}` |
| Multiple matches | `{"success": false, "error": "Multiple tasks match. Please be more specific.", "matches": [...]}` |
| No completed tasks | `{"success": true, "deleted_count": 0, "note": "No completed tasks to delete"}` |

**Example Agent Instruction**:
> Before deleting, confirm the task description with the user. For bulk delete, report how many tasks were removed.

---

## Fuzzy Matching Algorithm

When `description_match` is provided, the system uses the following matching strategy:

1. **Exact substring match** (case-insensitive): If the query is a substring of any task description
2. **Word overlap**: Count matching words between query and descriptions
3. **Threshold**: Require at least 50% word overlap or exact substring

**Examples**:
| Query | Task Description | Match? |
|-------|-----------------|--------|
| "groceries" | "buy groceries" | Yes (substring) |
| "buy food" | "buy groceries" | Yes (word overlap) |
| "dentist" | "call the dentist tomorrow" | Yes (substring) |
| "xyz" | "buy groceries" | No |

---

## Security Considerations

1. **User Isolation**: All tools receive `user_id` from JWT context, not from parameters
2. **Input Validation**: All string inputs sanitized and length-limited
3. **No Direct IDs from User**: When user provides task reference, use description matching
4. **Audit Trail**: All tool calls logged with parameters and results

---

## MCP Server Registration

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Todo MCP Server", json_response=True)

@mcp.tool()
async def add_todo(description: str) -> dict:
    """Add a new todo task for the user.

    Args:
        description: The task description (1-500 characters)

    Returns:
        Success status and created task details
    """
    # Implementation
    pass

@mcp.tool()
async def list_todos(include_completed: bool = True) -> dict:
    """List all todo tasks for the user.

    Args:
        include_completed: Whether to include completed tasks (default: true)

    Returns:
        List of tasks with counts
    """
    # Implementation
    pass

@mcp.tool()
async def complete_todo(task_id: str = None, description_match: str = None) -> dict:
    """Mark a task as completed.

    Args:
        task_id: Specific task UUID (optional)
        description_match: Fuzzy match on description (optional)

    Returns:
        Success status and updated task
    """
    # Implementation
    pass

@mcp.tool()
async def update_todo(new_description: str, task_id: str = None, description_match: str = None) -> dict:
    """Update a task's description.

    Args:
        new_description: The new task description
        task_id: Specific task UUID (optional)
        description_match: Fuzzy match on current description (optional)

    Returns:
        Success status, updated task, and previous description
    """
    # Implementation
    pass

@mcp.tool()
async def delete_todo(task_id: str = None, description_match: str = None, delete_completed: bool = False) -> dict:
    """Delete a task or all completed tasks.

    Args:
        task_id: Specific task UUID (optional)
        description_match: Fuzzy match on description (optional)
        delete_completed: Delete all completed tasks (optional)

    Returns:
        Success status and deleted task(s) details
    """
    # Implementation
    pass
```
