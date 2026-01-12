"""Integration test script for main.py functionality."""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import todo
import utils


def test_full_workflow():
    """Test complete workflow: add, view, update, mark complete, delete."""
    print("=" * 60)
    print("INTEGRATION TEST: Console Todo App")
    print("=" * 60)

    # Reset state
    todo.tasks.clear()
    todo.next_task_id = 1

    # Test 1: Add tasks
    print("\n[TEST 1] Adding tasks...")
    task_id_1 = todo.add_task("Complete Python project")
    task_id_2 = todo.add_task("Write documentation")
    task_id_3 = todo.add_task("Deploy to production")
    print(f"[PASS] Added 3 tasks (IDs: {task_id_1}, {task_id_2}, {task_id_3})")

    # Test 2: View tasks
    print("\n[TEST 2] Viewing all tasks...")
    all_tasks = todo.get_all_tasks()
    print(utils.format_tasks_table(all_tasks))
    assert len(all_tasks) == 3
    print("[PASS] All tasks displayed correctly")

    # Test 3: Mark task as complete
    print("\n[TEST 3] Marking task 1 as complete...")
    success = todo.mark_task_complete(task_id_1)
    assert success is True
    task = todo.get_task_by_id(task_id_1)
    assert task["completed"] is True
    print(f"[PASS] Task {task_id_1} marked as complete")

    # Test 4: View tasks with updated status
    print("\n[TEST 4] Viewing tasks after marking complete...")
    all_tasks = todo.get_all_tasks()
    print(utils.format_tasks_table(all_tasks))
    print("[PASS] Task status updated correctly")

    # Test 5: Update task description
    print("\n[TEST 5] Updating task 2 description...")
    success = todo.update_task(task_id_2, "Write comprehensive documentation with examples")
    assert success is True
    task = todo.get_task_by_id(task_id_2)
    assert "comprehensive" in task["description"]
    print(f"[PASS] Task {task_id_2} description updated")

    # Test 6: Delete task
    print("\n[TEST 6] Deleting task 3...")
    success = todo.delete_task(task_id_3)
    assert success is True
    assert todo.get_task_by_id(task_id_3) is None
    print(f"[PASS] Task {task_id_3} deleted successfully")

    # Test 7: View final state
    print("\n[TEST 7] Viewing final task list...")
    all_tasks = todo.get_all_tasks()
    print(utils.format_tasks_table(all_tasks))
    assert len(all_tasks) == 2
    print("[PASS] Final state correct (2 tasks remaining)")

    # Test 8: Empty state
    print("\n[TEST 8] Testing empty state message...")
    todo.tasks.clear()
    empty_message = utils.format_tasks_table(todo.get_all_tasks())
    print(empty_message)
    assert "No tasks yet" in empty_message
    print("[PASS] Empty state message displayed correctly")

    # Test 9: Input validation
    print("\n[TEST 9] Testing input validation...")

    # Invalid task ID (non-numeric)
    result = utils.validate_task_id("abc")
    assert result is None
    print("[PASS] Non-numeric task ID rejected")

    # Invalid task ID (negative)
    result = utils.validate_task_id("-1")
    assert result is None
    print("[PASS] Negative task ID rejected")

    # Valid task ID
    result = utils.validate_task_id("42")
    assert result == 42
    print("[PASS] Valid task ID accepted")

    # Empty description
    result = utils.validate_description("")
    assert result is None
    print("[PASS] Empty description rejected")

    # Valid description
    result = utils.validate_description("  Valid task  ")
    assert result == "Valid task"
    print("[PASS] Valid description accepted and trimmed")

    # Test 10: ID uniqueness after deletion
    print("\n[TEST 10] Testing ID uniqueness after deletion...")
    todo.tasks.clear()
    todo.next_task_id = 1
    id1 = todo.add_task("Task 1")
    id2 = todo.add_task("Task 2")
    todo.delete_task(id1)
    id3 = todo.add_task("Task 3")
    assert id3 == 3  # IDs are never reused
    print(f"[PASS] IDs remain unique after deletion (got ID {id3}, not {id1})")

    print("\n" + "=" * 60)
    print("ALL INTEGRATION TESTS PASSED!")
    print("=" * 60)
    print("\nThe application is ready to use.")
    print("Run: python src/main.py")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_full_workflow()
    except AssertionError as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FAIL] UNEXPECTED ERROR: {e}")
        sys.exit(1)
