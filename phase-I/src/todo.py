"""Task CRUD operations for Console Todo App."""

from datetime import datetime

# Global state
tasks = []
next_task_id = 1


def add_task(description: str) -> int:
    """
    Add a new task to the task list.

    Args:
        description: Task description text

    Returns:
        int: The ID of the newly created task
    """
    global next_task_id

    task = {
        "id": next_task_id,
        "description": description,
        "completed": False,
        "created": datetime.now().isoformat()
    }

    tasks.append(task)
    current_id = next_task_id
    next_task_id += 1

    return current_id


def get_all_tasks() -> list[dict]:
    """
    Retrieve all tasks.

    Returns:
        list[dict]: List of all tasks
    """
    return tasks.copy()


def get_task_by_id(task_id: int) -> dict | None:
    """
    Find a task by its ID.

    Args:
        task_id: The ID of the task to find

    Returns:
        dict | None: The task dictionary if found, None otherwise
    """
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def mark_task_complete(task_id: int) -> bool:
    """
    Mark a task as complete.

    Args:
        task_id: The ID of the task to mark complete

    Returns:
        bool: True if successful, False if task not found
    """
    task = get_task_by_id(task_id)
    if task is None:
        return False
    task["completed"] = True
    return True


def update_task(task_id: int, description: str) -> bool:
    """
    Update a task's description.

    Args:
        task_id: The ID of the task to update
        description: New description text

    Returns:
        bool: True if successful, False if task not found
    """
    task = get_task_by_id(task_id)
    if task is None:
        return False
    task["description"] = description
    return True


def delete_task(task_id: int) -> bool:
    """
    Delete a task from the list.

    Args:
        task_id: The ID of the task to delete

    Returns:
        bool: True if successful, False if task not found
    """
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return True
    return False
