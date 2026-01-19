"""
Task management API endpoints.

This module provides REST API endpoints for creating, reading, updating, and
deleting tasks. All endpoints require JWT authentication.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from uuid import UUID
from datetime import datetime

from app.api.deps import get_db, get_current_user
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from typing import List

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    user_id: UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """
    Create a new task for the authenticated user.

    Requires JWT authentication. The task is automatically associated with
    the authenticated user from the JWT token's 'sub' claim.

    Args:
        task_data: Task creation data (description)
        user_id: Authenticated user ID from JWT token
        db: Database session

    Returns:
        TaskResponse: Created task with ID, timestamps, and completion status

    Raises:
        HTTPException 401: If JWT token is invalid or expired
        HTTPException 422: If validation fails (description too long/short)

    Example Request:
        POST /api/tasks
        Authorization: Bearer <jwt_token>
        {
            "description": "Buy groceries"
        }

    Example Response:
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "description": "Buy groceries",
            "is_completed": false,
            "created_at": "2026-01-13T10:30:45.123456Z",
            "updated_at": "2026-01-13T10:30:45.123456Z"
        }
    """
    task = Task(
        description=task_data.description,
        user_id=user_id,
        is_completed=False,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return TaskResponse.model_validate(task)


@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    user_id: UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[TaskResponse]:
    """
    List all tasks for the authenticated user.

    Returns tasks sorted by creation date (newest first).
    Only returns tasks owned by the authenticated user.

    Args:
        user_id: Authenticated user ID from JWT token
        db: Database session

    Returns:
        List[TaskResponse]: List of user's tasks sorted by created_at DESC
    """
    result = await db.execute(
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
    )
    tasks = result.scalars().all()
    return [TaskResponse.model_validate(task) for task in tasks]


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    user_id: UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """
    Update a task's description.

    Only the task owner can update their tasks.

    Args:
        task_id: UUID of the task to update
        task_data: New task data (description)
        user_id: Authenticated user ID from JWT token
        db: Database session

    Returns:
        TaskResponse: Updated task

    Raises:
        HTTPException 404: If task not found
        HTTPException 403: If user doesn't own the task
    """
    result = await db.execute(
        select(Task).where(Task.id == task_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this resource"
        )

    task.description = task_data.description
    task.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(task)
    return TaskResponse.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    user_id: UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """
    Delete a task permanently.

    Only the task owner can delete their tasks.

    Args:
        task_id: UUID of the task to delete
        user_id: Authenticated user ID from JWT token
        db: Database session

    Raises:
        HTTPException 404: If task not found
        HTTPException 403: If user doesn't own the task
    """
    result = await db.execute(
        select(Task).where(Task.id == task_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this resource"
        )

    await db.delete(task)
    await db.commit()


@router.patch("/{task_id}/toggle", response_model=TaskResponse)
async def toggle_task(
    task_id: UUID,
    user_id: UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """
    Toggle a task's completion status.

    Flips is_completed between True and False.
    Only the task owner can toggle their tasks.

    Args:
        task_id: UUID of the task to toggle
        user_id: Authenticated user ID from JWT token
        db: Database session

    Returns:
        TaskResponse: Updated task with toggled status

    Raises:
        HTTPException 404: If task not found
        HTTPException 403: If user doesn't own the task
    """
    result = await db.execute(
        select(Task).where(Task.id == task_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this resource"
        )

    task.is_completed = not task.is_completed
    task.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(task)
    return TaskResponse.model_validate(task)
