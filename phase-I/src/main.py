"""Main entry point and CLI menu controller for Console Todo App."""

import sys
import todo
import utils


def add_task_handler():
    """Handle adding a new task."""
    description = input("Enter task description: ")
    validated_desc = utils.validate_description(description)

    if validated_desc is None:
        print("Description cannot be empty")
        return

    task_id = todo.add_task(validated_desc)
    print(f"Task added successfully! (ID: {task_id})")


def view_tasks_handler():
    """Handle viewing all tasks."""
    all_tasks = todo.get_all_tasks()
    print("\n" + utils.format_tasks_table(all_tasks))


def update_task_handler():
    """Handle updating a task description."""
    if not todo.get_all_tasks():
        print("No tasks available. Add a task first")
        return

    user_input = input("Enter task ID: ")
    task_id = utils.validate_task_id(user_input)

    if task_id is None:
        print("Invalid input. Please enter a numeric task ID")
        return

    if not todo.get_task_by_id(task_id):
        print("Task not found. Please enter a valid task ID")
        return

    description = input("Enter new description: ")
    validated_desc = utils.validate_description(description)

    if validated_desc is None:
        print("Description cannot be empty")
        return

    todo.update_task(task_id, validated_desc)
    print("Task updated successfully!")


def delete_task_handler():
    """Handle deleting a task."""
    if not todo.get_all_tasks():
        print("No tasks available. Add a task first")
        return

    user_input = input("Enter task ID: ")
    task_id = utils.validate_task_id(user_input)

    if task_id is None:
        print("Invalid input. Please enter a numeric task ID")
        return

    success = todo.delete_task(task_id)
    if success:
        print("Task deleted successfully")
    else:
        print("Task not found. Please enter a valid task ID")


def mark_complete_handler():
    """Handle marking a task as complete."""
    if not todo.get_all_tasks():
        print("No tasks available. Add a task first")
        return

    user_input = input("Enter task ID: ")
    task_id = utils.validate_task_id(user_input)

    if task_id is None:
        print("Invalid input. Please enter a numeric task ID")
        return

    task = todo.get_task_by_id(task_id)
    if not task:
        print("Task not found. Please enter a valid task ID")
        return

    if task["completed"]:
        print("Task already completed")
        return

    todo.mark_task_complete(task_id)
    print("Task marked as complete!")


def exit_handler():
    """Handle exiting the application."""
    print("Goodbye!")
    sys.exit(0)


def main():
    """Main application loop."""
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


if __name__ == "__main__":
    main()
