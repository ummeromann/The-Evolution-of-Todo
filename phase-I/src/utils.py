"""Helper functions for validation and display formatting."""


def validate_task_id(user_input: str) -> int | None:
    """
    Validate and parse task ID from user input.

    Args:
        user_input: Raw user input string

    Returns:
        int | None: Parsed task ID if valid, None if invalid
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

    Args:
        text: Raw description text

    Returns:
        str | None: Trimmed description if valid (non-empty), None if invalid
    """
    trimmed = text.strip()
    if not trimmed:
        return None
    return trimmed


def display_menu() -> None:
    """Display the main menu."""
    print("\n=== Todo App ===")
    print("1. Add task")
    print("2. View tasks")
    print("3. Update task")
    print("4. Delete task")
    print("5. Mark task as complete")
    print("6. Exit")
    print()


def format_tasks_table(tasks: list[dict]) -> str:
    """
    Format tasks as a simple table.

    Args:
        tasks: List of task dictionaries

    Returns:
        str: Formatted task table or empty state message
    """
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
