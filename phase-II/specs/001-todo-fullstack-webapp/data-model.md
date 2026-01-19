# Data Model: Todo Full-Stack Web Application

**Feature Branch**: `001-todo-fullstack-webapp`
**Date**: 2026-01-13
**Source**: Feature Specification `spec.md`

## Overview

This document defines the data model for the Todo Full-Stack Web Application. All entities, relationships, and validation rules are derived from the feature specification requirements.

---

## Entity: User

Represents a registered account holder in the system.

### Schema

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key, Auto-generated | Unique identifier for the user |
| `email` | String(255) | Unique, Not Null, Email Format | User's email address for authentication |
| `hashed_password` | String(255) | Not Null | Bcrypt-hashed password (never stored in plain text) |
| `created_at` | Timestamp | Not Null, Default: now() | Account creation timestamp |
| `updated_at` | Timestamp | Not Null, Default: now() | Last modification timestamp |

### Validation Rules

| Rule ID | Field | Rule | Error Message |
|---------|-------|------|---------------|
| U-001 | email | Must be valid email format | "Invalid email format" |
| U-002 | email | Must be unique across all users | "Email already registered" |
| U-003 | password | Minimum 8 characters (before hashing) | "Password must be at least 8 characters" |

### SQLModel Definition

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

---

## Entity: Task

Represents a to-do item belonging to a specific user.

### Schema

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key, Auto-generated | Unique identifier for the task |
| `description` | String(500) | Not Null, Length 1-500 | Task description text |
| `is_completed` | Boolean | Not Null, Default: false | Completion status |
| `user_id` | UUID | Foreign Key → users.id, Not Null | Owner reference |
| `created_at` | Timestamp | Not Null, Default: now() | Task creation timestamp |
| `updated_at` | Timestamp | Not Null, Default: now() | Last modification timestamp |

### Validation Rules

| Rule ID | Field | Rule | Error Message |
|---------|-------|------|---------------|
| T-001 | description | Must not be empty | "Task description is required" |
| T-002 | description | Maximum 500 characters | "Task description must be 500 characters or less" |
| T-003 | user_id | Must reference existing user | "Invalid user reference" |
| T-004 | user_id | Operation only allowed by owner | "Access denied" |

### SQLModel Definition

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    description: str = Field(max_length=500)
    is_completed: bool = Field(default=False)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship (optional, for ORM convenience)
    user: Optional["User"] = Relationship(back_populates="tasks")
```

---

## Relationships

### User → Tasks (One-to-Many)

- A User can have zero or more Tasks
- A Task belongs to exactly one User
- Deleting a User cascades to delete all their Tasks

```text
┌──────────────┐         ┌──────────────┐
│    users     │         │    tasks     │
├──────────────┤         ├──────────────┤
│ id (PK)      │◄────────│ user_id (FK) │
│ email        │    1:N  │ id (PK)      │
│ hashed_pass  │         │ description  │
│ created_at   │         │ is_completed │
│ updated_at   │         │ created_at   │
└──────────────┘         │ updated_at   │
                         └──────────────┘
```

---

## State Transitions

### Task Completion Status

```text
┌─────────┐     toggle()    ┌───────────┐
│ PENDING │ ───────────────►│ COMPLETED │
│ (false) │◄─────────────── │ (true)    │
└─────────┘     toggle()    └───────────┘
```

- Initial state: PENDING (is_completed = false)
- Toggle action: Flips between PENDING and COMPLETED
- No intermediate states

---

## Database Indexes

| Table | Column(s) | Type | Purpose |
|-------|-----------|------|---------|
| users | email | Unique | Fast lookup by email for authentication |
| tasks | user_id | B-tree | Fast query for user's tasks |
| tasks | user_id, created_at | Composite | Efficient ordering of user's tasks |

### Index Definitions

```sql
-- User email lookup
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- Task queries by user
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Sorted task retrieval for user
CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC);
```

---

## Pydantic Schemas (API Layer)

### User Schemas

```python
from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str  # Min 8 chars, validated

class UserResponse(BaseModel):
    id: UUID
    email: str
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str
```

### Task Schemas

```python
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class TaskCreate(BaseModel):
    description: str = Field(min_length=1, max_length=500)

class TaskUpdate(BaseModel):
    description: str = Field(min_length=1, max_length=500)

class TaskResponse(BaseModel):
    id: UUID
    description: str
    is_completed: bool
    created_at: datetime
    updated_at: datetime

class TaskToggle(BaseModel):
    is_completed: bool
```

---

## Migration Plan

### Migration 001: Initial Schema

```sql
-- Create users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    description VARCHAR(500) NOT NULL,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC);
```

### Rollback 001

```sql
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS users;
```

---

## Data Integrity Constraints

| Constraint | Type | Tables | Description |
|------------|------|--------|-------------|
| users_pkey | Primary Key | users | Unique user identifier |
| users_email_key | Unique | users | Prevent duplicate emails |
| tasks_pkey | Primary Key | tasks | Unique task identifier |
| tasks_user_id_fkey | Foreign Key | tasks → users | Ensure valid user reference |
| tasks_user_cascade | Cascade Delete | tasks | Delete tasks when user deleted |

---

## Security Considerations

1. **Password Storage**: Never store plain text passwords; use bcrypt with cost factor 12
2. **User Isolation**: All task queries MUST include `WHERE user_id = :current_user_id`
3. **UUID Usage**: Use UUIDs to prevent enumeration attacks on sequential IDs
4. **Timestamps**: Use UTC for all timestamp storage

---

## Query Patterns

### Get User's Tasks (sorted by creation, newest first)

```sql
SELECT id, description, is_completed, created_at, updated_at
FROM tasks
WHERE user_id = :user_id
ORDER BY created_at DESC;
```

### Create Task

```sql
INSERT INTO tasks (description, user_id)
VALUES (:description, :user_id)
RETURNING id, description, is_completed, created_at, updated_at;
```

### Update Task (with ownership check)

```sql
UPDATE tasks
SET description = :description, updated_at = NOW()
WHERE id = :task_id AND user_id = :user_id
RETURNING id, description, is_completed, created_at, updated_at;
```

### Toggle Task (with ownership check)

```sql
UPDATE tasks
SET is_completed = NOT is_completed, updated_at = NOW()
WHERE id = :task_id AND user_id = :user_id
RETURNING id, description, is_completed, created_at, updated_at;
```

### Delete Task (with ownership check)

```sql
DELETE FROM tasks
WHERE id = :task_id AND user_id = :user_id;
```
