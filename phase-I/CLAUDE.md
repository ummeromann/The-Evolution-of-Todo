# Claude Code Instructions

This file provides instructions for Claude on how to assist with "The Evolution of Todo" project.

## Project Overview

**The Evolution of Todo** is a multi-phase educational project that evolves a simple console application into a full-stack, AI-powered, cloud-deployed distributed system.

**Current Phase**: Phase I - In-Memory Python Console Todo App

## Project Structure

```
phase-I/
├── src/                    # Python source code
│   ├── main.py             # Entry point and menu controller
│   ├── todo.py             # CRUD operations
│   └── utils.py            # Validation and display utilities
├── tests/                  # pytest test suite
├── specs-history/          # Specifications and development history
├── Constitution.md         # Project principles and standards
└── README.md               # Project documentation
```

## Coding Standards

### Python Style

- **PEP8 Compliance**: Follow Python style guidelines
- **Type Hints**: Use type annotations for function signatures
- **Docstrings**: Document all functions with purpose, args, and returns
- **Naming**: Use snake_case for functions/variables, PascalCase for classes

### Architecture Principles

- **Separation of Concerns**: Keep main.py (UI), todo.py (logic), utils.py (helpers) separate
- **In-Memory Only**: Phase I uses Python lists/dicts only - no file I/O or databases
- **Input Validation**: All user inputs validated before processing
- **Graceful Errors**: User-friendly error messages, no crashes on invalid input

### Testing Requirements

- **pytest**: All tests use pytest framework
- **Unit Tests**: Test each function in isolation
- **Fixtures**: Reset state between tests using fixtures
- **Coverage**: Cover all CRUD operations and edge cases

## Phase I Constraints

When working on Phase I, Claude MUST:

- Use only Python standard library (no external packages except pytest for testing)
- Store data in memory only (lists, dicts) - no file I/O
- Keep the CLI menu-driven interface
- Maintain modular code structure
- Follow existing patterns in the codebase

## Key Files Reference

| File | Purpose |
|------|---------|
| `src/main.py` | CLI menu and operation handlers |
| `src/todo.py` | Task CRUD operations |
| `src/utils.py` | Input validation and display formatting |
| `tests/test_todo.py` | Unit tests for CRUD operations |
| `tests/test_utils.py` | Unit tests for utilities |

## Common Tasks

### Adding a Feature

1. Review the spec in `specs-history/features/001-console-todo/spec.md`
2. Follow patterns established in existing code
3. Add unit tests in `tests/`
4. Ensure all tests pass with `pytest tests/ -v`

### Fixing a Bug

1. Reproduce the issue
2. Write a failing test that demonstrates the bug
3. Fix the bug in the relevant module
4. Verify the test passes

### Running Tests

```bash
pytest tests/ -v           # Run all tests
pytest tests/test_todo.py  # Run specific test file
```

### Running the Application

```bash
python src/main.py
```

## Constitution Reference

The project follows principles defined in `Constitution.md`:

1. **Accuracy**: Code must precisely match requirements
2. **Clarity**: Self-documenting code with clear structure
3. **Reproducibility**: Consistent behavior across environments
4. **Scalability**: Design supports future phase evolution
5. **Security**: Validate inputs, no hardcoded secrets
6. **Phase Compliance**: Adhere to Phase I tech stack

## Future Phases Preview

- **Phase II**: Web UI + FastAPI + Neon DB
- **Phase III**: AI chatbot with OpenAI
- **Phase IV**: Kubernetes deployment
- **Phase V**: Cloud distributed system with Kafka

When suggesting improvements, consider forward compatibility with future phases.

---

*Last Updated: 2026-01-12*
