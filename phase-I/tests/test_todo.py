"""Unit tests for todo.py CRUD operations."""

import pytest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import todo


@pytest.fixture(autouse=True)
def reset_todo_state():
    """Reset todo global state before each test."""
    todo.tasks.clear()
    todo.next_task_id = 1
    yield
    todo.tasks.clear()
    todo.next_task_id = 1


def test_add_task():
    """Test adding a new task."""
    task_id = todo.add_task("Test task 1")
    assert task_id == 1
    assert len(todo.tasks) == 1
    assert todo.tasks[0]["id"] == 1
    assert todo.tasks[0]["description"] == "Test task 1"
    assert todo.tasks[0]["completed"] is False


def test_get_all_tasks():
    """Test retrieving all tasks."""
    todo.add_task("Task 1")
    todo.add_task("Task 2")
    all_tasks = todo.get_all_tasks()
    assert len(all_tasks) == 2
    assert all_tasks[0]["description"] == "Task 1"
    assert all_tasks[1]["description"] == "Task 2"


def test_get_task_by_id():
    """Test finding a task by ID."""
    task_id = todo.add_task("Find me")
    task = todo.get_task_by_id(task_id)
    assert task is not None
    assert task["id"] == task_id
    assert task["description"] == "Find me"

    # Test non-existent ID
    assert todo.get_task_by_id(999) is None


def test_mark_task_complete_success():
    """Test marking a task as complete."""
    task_id = todo.add_task("Complete me")
    result = todo.mark_task_complete(task_id)
    assert result is True
    task = todo.get_task_by_id(task_id)
    assert task["completed"] is True


def test_mark_task_complete_idempotent():
    """Test marking an already complete task (idempotent)."""
    task_id = todo.add_task("Already complete")
    todo.mark_task_complete(task_id)
    result = todo.mark_task_complete(task_id)
    assert result is True  # Should succeed
    task = todo.get_task_by_id(task_id)
    assert task["completed"] is True


def test_mark_task_complete_not_found():
    """Test marking non-existent task as complete."""
    result = todo.mark_task_complete(999)
    assert result is False


def test_update_task_success():
    """Test updating a task description."""
    task_id = todo.add_task("Old description")
    result = todo.update_task(task_id, "New description")
    assert result is True
    task = todo.get_task_by_id(task_id)
    assert task["description"] == "New description"


def test_update_task_not_found():
    """Test updating non-existent task."""
    result = todo.update_task(999, "New description")
    assert result is False


def test_update_task_preserves_completed_status():
    """Test that updating a task preserves its completed status."""
    task_id = todo.add_task("Original")
    todo.mark_task_complete(task_id)
    todo.update_task(task_id, "Updated")
    task = todo.get_task_by_id(task_id)
    assert task["completed"] is True
    assert task["description"] == "Updated"


def test_delete_task_success():
    """Test deleting a task."""
    task_id = todo.add_task("Delete me")
    result = todo.delete_task(task_id)
    assert result is True
    assert len(todo.tasks) == 0
    assert todo.get_task_by_id(task_id) is None


def test_delete_task_not_found():
    """Test deleting non-existent task."""
    result = todo.delete_task(999)
    assert result is False


def test_delete_task_id_not_reused():
    """Test that deleted task IDs are not reused."""
    task_id_1 = todo.add_task("Task 1")
    todo.add_task("Task 2")
    todo.delete_task(task_id_1)
    task_id_3 = todo.add_task("Task 3")
    assert task_id_3 == 3  # ID counter doesn't reset
