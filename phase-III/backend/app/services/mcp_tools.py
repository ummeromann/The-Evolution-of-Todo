"""
MCP Tools for Todo Operations.

This module implements the MCP (Model Context Protocol) tools that the AI agent
uses to perform todo operations. All tools are stateless and database-backed.

Tools:
- add_todo: Create a new task
- list_todos: Retrieve user's tasks
- complete_todo: Mark a task as completed
- update_todo: Update task description
- delete_todo: Delete a task or all completed tasks
"""

from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Task


# ============================================================================
# Fuzzy Matching Utility
# ============================================================================

def fuzzy_match_task(
    query: str,
    tasks: List[Task],
    threshold: float = 0.5
) -> List[Task]:
    """
    Find tasks matching a query string using fuzzy matching.

    Matching strategy:
    1. Exact substring match (case-insensitive)
    2. Word overlap with threshold

    Args:
        query: The search query
        tasks: List of tasks to search
        threshold: Minimum word overlap ratio (default 0.5)

    Returns:
        List of matching tasks, sorted by relevance
    """
    if not query or not tasks:
        return []

    query_lower = query.lower().strip()
    query_words = set(query_lower.split())
    matches = []

    for task in tasks:
        description_lower = task.description.lower()
        description_words = set(description_lower.split())

        # Check exact substring match
        if query_lower in description_lower:
            matches.append((task, 1.0))  # High score for substring match
            continue

        # Check word overlap
        if query_words and description_words:
            overlap = len(query_words & description_words)
            ratio = overlap / len(query_words)
            if ratio >= threshold:
                matches.append((task, ratio))

    # Sort by score (highest first) and return tasks only
    matches.sort(key=lambda x: x[1], reverse=True)
    return [task for task, score in matches]


# ============================================================================
# User Context for MCP Tools
# ============================================================================

class MCPContext:
    """Context object passed to MCP tools containing user info and database session."""

    def __init__(self, user_id: UUID, db: AsyncSession):
        self.user_id = user_id
        self.db = db


# Global context holder (set per-request)
_current_context: Optional[MCPContext] = None


def set_mcp_context(user_id: UUID, db: AsyncSession) -> None:
    """Set the MCP context for the current request."""
    global _current_context
    _current_context = MCPContext(user_id, db)


def get_mcp_context() -> MCPContext:
    """Get the current MCP context."""
    if _current_context is None:
        raise RuntimeError("MCP context not set. Call set_mcp_context first.")
    return _current_context


def clear_mcp_context() -> None:
    """Clear the MCP context after request completes."""
    global _current_context
    _current_context = None


# ============================================================================
# MCP Tool Implementations
# ============================================================================

async def add_todo(description: str) -> Dict[str, Any]:
    """
    Add a new todo task for the user.

    Args:
        description: The task description (1-500 characters)

    Returns:
        Success status and created task details
    """
    ctx = get_mcp_context()

    # Validation
    if not description or not description.strip():
        return {"success": False, "error": "Description is required"}

    description = description.strip()
    if len(description) > 500:
        return {"success": False, "error": "Description too long (max 500 characters)"}

    try:
        # Create task
        task = Task(
            description=description,
            user_id=ctx.user_id,
            is_completed=False,
        )
        ctx.db.add(task)
        await ctx.db.commit()
        await ctx.db.refresh(task)

        return {
            "success": True,
            "task": {
                "id": str(task.id),
                "description": task.description,
                "is_completed": task.is_completed,
                "created_at": task.created_at.isoformat(),
            }
        }
    except Exception as e:
        await ctx.db.rollback()
        return {"success": False, "error": "Failed to create task"}


async def list_todos(include_completed: bool = True) -> Dict[str, Any]:
    """
    List all todo tasks for the user.

    Args:
        include_completed: Whether to include completed tasks (default: true)

    Returns:
        List of tasks with counts
    """
    ctx = get_mcp_context()

    try:
        # Build query
        query = select(Task).where(Task.user_id == ctx.user_id)
        if not include_completed:
            query = query.where(Task.is_completed == False)
        query = query.order_by(Task.created_at.desc())

        result = await ctx.db.execute(query)
        tasks = result.scalars().all()

        # Count totals
        all_query = select(Task).where(Task.user_id == ctx.user_id)
        all_result = await ctx.db.execute(all_query)
        all_tasks = all_result.scalars().all()

        completed_count = sum(1 for t in all_tasks if t.is_completed)
        pending_count = len(all_tasks) - completed_count

        return {
            "success": True,
            "tasks": [
                {
                    "id": str(task.id),
                    "description": task.description,
                    "is_completed": task.is_completed,
                    "created_at": task.created_at.isoformat(),
                }
                for task in tasks
            ],
            "total": len(all_tasks),
            "completed_count": completed_count,
            "pending_count": pending_count,
        }
    except Exception as e:
        return {"success": False, "error": "Failed to retrieve tasks"}


async def complete_todo(
    task_id: Optional[str] = None,
    description_match: Optional[str] = None
) -> Dict[str, Any]:
    """
    Mark a task as completed.

    Args:
        task_id: Specific task UUID (optional)
        description_match: Fuzzy match on description (optional)

    Returns:
        Success status and updated task
    """
    ctx = get_mcp_context()

    if not task_id and not description_match:
        return {"success": False, "error": "Either task_id or description_match is required"}

    try:
        task = None

        if task_id:
            # Find by ID
            try:
                uuid_id = UUID(task_id)
                query = select(Task).where(Task.id == uuid_id, Task.user_id == ctx.user_id)
                result = await ctx.db.execute(query)
                task = result.scalar_one_or_none()
            except ValueError:
                return {"success": False, "error": "Invalid task ID format"}
        else:
            # Find by description match
            query = select(Task).where(Task.user_id == ctx.user_id)
            result = await ctx.db.execute(query)
            all_tasks = list(result.scalars().all())

            matches = fuzzy_match_task(description_match, all_tasks)

            if not matches:
                return {"success": False, "error": "No task found matching your request", "found": False}

            if len(matches) > 1:
                return {
                    "success": False,
                    "error": "Multiple tasks match. Please be more specific.",
                    "matches": [
                        {"id": str(t.id), "description": t.description}
                        for t in matches[:5]
                    ]
                }

            task = matches[0]

        if not task:
            return {"success": False, "error": "No task found matching your request", "found": False}

        # Check if already completed
        already_completed = task.is_completed

        # Mark as completed
        task.is_completed = True
        task.updated_at = datetime.utcnow()
        await ctx.db.commit()
        await ctx.db.refresh(task)

        response = {
            "success": True,
            "task": {
                "id": str(task.id),
                "description": task.description,
                "is_completed": task.is_completed,
                "updated_at": task.updated_at.isoformat(),
            }
        }

        if already_completed:
            response["note"] = "Task was already completed"

        return response

    except Exception as e:
        await ctx.db.rollback()
        return {"success": False, "error": "Failed to complete task"}


async def update_todo(
    new_description: str,
    task_id: Optional[str] = None,
    description_match: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update a task's description.

    Args:
        new_description: The new task description
        task_id: Specific task UUID (optional)
        description_match: Fuzzy match on current description (optional)

    Returns:
        Success status, updated task, and previous description
    """
    ctx = get_mcp_context()

    if not task_id and not description_match:
        return {"success": False, "error": "Either task_id or description_match is required"}

    # Validate new description
    if not new_description or not new_description.strip():
        return {"success": False, "error": "New description is required"}

    new_description = new_description.strip()
    if len(new_description) > 500:
        return {"success": False, "error": "Description too long (max 500 characters)"}

    try:
        task = None

        if task_id:
            # Find by ID
            try:
                uuid_id = UUID(task_id)
                query = select(Task).where(Task.id == uuid_id, Task.user_id == ctx.user_id)
                result = await ctx.db.execute(query)
                task = result.scalar_one_or_none()
            except ValueError:
                return {"success": False, "error": "Invalid task ID format"}
        else:
            # Find by description match
            query = select(Task).where(Task.user_id == ctx.user_id)
            result = await ctx.db.execute(query)
            all_tasks = list(result.scalars().all())

            matches = fuzzy_match_task(description_match, all_tasks)

            if not matches:
                return {"success": False, "error": "No task found matching your request", "found": False}

            if len(matches) > 1:
                return {
                    "success": False,
                    "error": "Multiple tasks match. Please be more specific.",
                    "matches": [
                        {"id": str(t.id), "description": t.description}
                        for t in matches[:5]
                    ]
                }

            task = matches[0]

        if not task:
            return {"success": False, "error": "No task found matching your request", "found": False}

        # Store previous description
        previous_description = task.description

        # Update task
        task.description = new_description
        task.updated_at = datetime.utcnow()
        await ctx.db.commit()
        await ctx.db.refresh(task)

        return {
            "success": True,
            "task": {
                "id": str(task.id),
                "description": task.description,
                "is_completed": task.is_completed,
                "updated_at": task.updated_at.isoformat(),
            },
            "previous_description": previous_description,
        }

    except Exception as e:
        await ctx.db.rollback()
        return {"success": False, "error": "Failed to update task"}


async def delete_todo(
    task_id: Optional[str] = None,
    description_match: Optional[str] = None,
    delete_completed: bool = False
) -> Dict[str, Any]:
    """
    Delete a task or all completed tasks.

    Args:
        task_id: Specific task UUID (optional)
        description_match: Fuzzy match on description (optional)
        delete_completed: Delete all completed tasks (optional)

    Returns:
        Success status and deleted task(s) details
    """
    ctx = get_mcp_context()

    if not task_id and not description_match and not delete_completed:
        return {"success": False, "error": "Either task_id, description_match, or delete_completed is required"}

    try:
        # Handle bulk delete of completed tasks
        if delete_completed:
            query = select(Task).where(
                Task.user_id == ctx.user_id,
                Task.is_completed == True
            )
            result = await ctx.db.execute(query)
            completed_tasks = list(result.scalars().all())

            if not completed_tasks:
                return {
                    "success": True,
                    "deleted_count": 0,
                    "note": "No completed tasks to delete"
                }

            deleted_tasks = []
            for task in completed_tasks:
                deleted_tasks.append({
                    "id": str(task.id),
                    "description": task.description
                })
                await ctx.db.delete(task)

            await ctx.db.commit()

            return {
                "success": True,
                "deleted_count": len(deleted_tasks),
                "deleted_tasks": deleted_tasks,
            }

        # Handle single task delete
        task = None

        if task_id:
            # Find by ID
            try:
                uuid_id = UUID(task_id)
                query = select(Task).where(Task.id == uuid_id, Task.user_id == ctx.user_id)
                result = await ctx.db.execute(query)
                task = result.scalar_one_or_none()
            except ValueError:
                return {"success": False, "error": "Invalid task ID format"}
        else:
            # Find by description match
            query = select(Task).where(Task.user_id == ctx.user_id)
            result = await ctx.db.execute(query)
            all_tasks = list(result.scalars().all())

            matches = fuzzy_match_task(description_match, all_tasks)

            if not matches:
                return {"success": False, "error": "No task found matching your request", "found": False}

            if len(matches) > 1:
                return {
                    "success": False,
                    "error": "Multiple tasks match. Please be more specific.",
                    "matches": [
                        {"id": str(t.id), "description": t.description}
                        for t in matches[:5]
                    ]
                }

            task = matches[0]

        if not task:
            return {"success": False, "error": "No task found matching your request", "found": False}

        # Delete task
        deleted_info = {
            "id": str(task.id),
            "description": task.description
        }
        await ctx.db.delete(task)
        await ctx.db.commit()

        return {
            "success": True,
            "deleted": deleted_info,
        }

    except Exception as e:
        await ctx.db.rollback()
        return {"success": False, "error": "Failed to delete task"}
