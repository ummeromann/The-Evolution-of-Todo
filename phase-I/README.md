# The Evolution of Todo - Phase I

> A multi-phase educational project demonstrating the evolution of a simple console application into a full-stack, AI-powered, cloud-deployed distributed system.

## Project Overview

**Phase I** implements an in-memory command-line todo application using Python. This foundational phase establishes core CRUD operations and clean architecture patterns that will evolve through subsequent phases:

| Phase | Focus | Technologies |
|-------|-------|--------------|
| **Phase I** (Current) | Console App | Python, In-Memory Storage |
| Phase II | Full-Stack Web | Next.js, FastAPI, Neon DB |
| Phase III | AI Chatbot | OpenAI ChatKit, Agents SDK |
| Phase IV | Kubernetes | Docker, Minikube, Helm |
| Phase V | Cloud Distributed | Kafka, Dapr, DigitalOcean DOKS |

## Features

- **Add Tasks**: Create new tasks with descriptions
- **View Tasks**: Display all tasks with ID, description, and status
- **Update Tasks**: Modify task descriptions
- **Delete Tasks**: Remove unwanted tasks
- **Mark Complete**: Track progress by marking tasks as complete
- **In-Memory Storage**: Tasks persist only during the current session

## Requirements

- Python 3.13 or higher
- pytest 7.4.0+ (for running tests)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ummeromann/The-Evolution-of-Todo.git
cd The-Evolution-of-Todo/phase-I
```

### 2. Install Development Dependencies (Optional)

```bash
pip install -r requirements-dev.txt
```

## Usage

### Running the Application

```bash
python src/main.py
```

### Main Menu

```
=== Todo App ===
1. Add task
2. View tasks
3. Update task
4. Delete task
5. Mark task as complete
6. Exit

Select option (1-6):
```

### Quick Example

```bash
# Launch the app
python src/main.py

# Select option 1 to add a task
> 1
Enter task description: Complete Python project

# Select option 2 to view tasks
> 2
ID   | Description                              | Status
------------------------------------------------------------
1    | Complete Python project                  | Incomplete

# Select option 5 to mark task as complete
> 5
Enter task ID: 1
Task marked as complete!

# Select option 6 to exit
> 6
Goodbye!
```

## Testing

Run the complete test suite:

```bash
pytest tests/ -v
```

Run specific test files:

```bash
pytest tests/test_todo.py -v      # CRUD operations
pytest tests/test_utils.py -v     # Validation and formatting
```

## Project Structure

```
phase-I/
├── src/                          # Source code
│   ├── __init__.py
│   ├── main.py                   # Entry point and menu controller
│   ├── todo.py                   # CRUD operations
│   └── utils.py                  # Validation and display utilities
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── test_todo.py              # CRUD operation tests
│   ├── test_utils.py             # Validation tests
│   └── test_main_integration.py  # Integration tests
├── specs-history/                # Specifications and history
│   ├── README.md                 # Specs index
│   ├── features/                 # Feature specifications
│   └── prompt-history/           # Development history
├── Constitution.md               # Project principles and standards
├── CLAUDE.md                     # AI assistant instructions
├── README.md                     # This file
└── requirements-dev.txt          # Development dependencies
```

## Documentation

| Document | Description |
|----------|-------------|
| [Constitution.md](Constitution.md) | Project vision, principles, and phase standards |
| [specs-history/](specs-history/) | Complete specifications and development history |
| [specs-history/features/001-console-todo/spec.md](specs-history/features/001-console-todo/spec.md) | Feature requirements |
| [specs-history/features/001-console-todo/plan.md](specs-history/features/001-console-todo/plan.md) | Implementation plan |

## Design Principles

This application follows Phase I technical standards defined in the [Constitution](Constitution.md):

- **In-Memory Storage**: Python lists and dictionaries only
- **Modular Design**: Separation of concerns (main, todo, utils)
- **Input Validation**: Graceful handling of invalid inputs
- **PEP8 Compliance**: Python style guidelines
- **Test Coverage**: Unit tests for all core functionality

## Error Handling

The application handles common errors gracefully:

| Error | Message |
|-------|---------|
| Invalid menu option | "Invalid option. Please select a number from the menu" |
| Invalid task ID | "Invalid input. Please enter a numeric task ID" |
| Task not found | "Task not found. Please enter a valid task ID" |
| Empty description | "Description cannot be empty" |
| Empty task list | "No tasks yet. Add your first task!" |

## Limitations (Phase I)

These limitations are intentional for Phase I:

- **No Persistence**: Tasks are lost when the application exits
- **Single Session**: No data saved between runs
- **No Advanced Features**: No priorities, tags, due dates, or search
- **Console Only**: Command-line interface only

Future phases will add web UI, database persistence, AI-powered chatbot, Kubernetes deployment, and cloud infrastructure.

## Development

### Code Standards

- **PEP8 Compliance**: All code follows Python style guidelines
- **Type Hints**: Function signatures include type annotations
- **Docstrings**: All functions documented with purpose, args, and returns
- **Modular Design**: Clear separation between menu, business logic, and utilities

### Testing Approach

- **Test-Driven Development**: Tests written before implementation
- **Unit Tests**: Isolated tests for each function
- **Fixtures**: Automatic state reset between tests
- **Coverage**: All CRUD operations and edge cases tested

## Contributing

This project follows spec-driven development principles. All implementation follows:

1. Feature specification (`spec.md`)
2. Implementation plan (`plan.md`)
3. Task breakdown (`tasks.md`)
4. Test-first approach

## License

Educational project - Phase I of multi-phase todo application learning series.

## Author

**Ummer Omann**
GitHub: [@ummeromann](https://github.com/ummeromann)

---

**Phase I** - In-Memory Console Application | v1.0.0
