# Data Model: Todo AI Chatbot

**Feature**: 004-todo-ai-chatbot
**Date**: 2026-02-02

## Overview

This document defines the data model extensions for the AI chatbot feature. The existing `User` and `Task` models from Phase II are reused. Three new entities are introduced for conversation persistence.

## Existing Entities (Reused)

### User
*No changes required - reused from Phase II*

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| email | VARCHAR(255) | UNIQUE, INDEX | User email |
| hashed_password | VARCHAR(255) | NOT NULL | Bcrypt hash |
| created_at | TIMESTAMP | NOT NULL | Creation time |
| updated_at | TIMESTAMP | NOT NULL | Last update time |

### Task
*No changes required - reused from Phase II*

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| description | VARCHAR(500) | NOT NULL | Task description |
| is_completed | BOOLEAN | DEFAULT FALSE | Completion status |
| user_id | UUID | FK → users.id | Owner reference |
| created_at | TIMESTAMP | NOT NULL | Creation time |
| updated_at | TIMESTAMP | NOT NULL | Last update time |

## New Entities

### Conversation

Represents a chat session between a user and the AI assistant.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| user_id | UUID | FK → users.id, INDEX | Owner reference |
| title | VARCHAR(255) | NULLABLE | Auto-generated or user-set title |
| created_at | TIMESTAMP | NOT NULL | Session start time |
| updated_at | TIMESTAMP | NOT NULL | Last message time |

**Relationships**:
- Belongs to one User (many-to-one)
- Has many Messages (one-to-many, cascade delete)

**Indexes**:
- `idx_conversations_user_id` on user_id
- `idx_conversations_updated_at` on updated_at (for sorting)

### Message

Represents a single message within a conversation.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| conversation_id | UUID | FK → conversations.id, INDEX | Parent conversation |
| role | VARCHAR(20) | NOT NULL | Message role (see enum) |
| content | TEXT | NOT NULL | Message content |
| tool_call_id | VARCHAR(100) | NULLABLE | For tool result messages |
| created_at | TIMESTAMP | NOT NULL | Message timestamp |

**Role Enum Values**:
- `user` - Message from the user
- `assistant` - Response from the AI
- `tool` - Result from an MCP tool call

**Relationships**:
- Belongs to one Conversation (many-to-one)
- Has many ToolCalls (one-to-many, cascade delete)

**Indexes**:
- `idx_messages_conversation_id` on conversation_id
- `idx_messages_created_at` on created_at (for ordering)

### ToolCall

Records an MCP tool invocation for audit and debugging.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| message_id | UUID | FK → messages.id, INDEX | Parent message |
| tool_name | VARCHAR(100) | NOT NULL | Name of invoked tool |
| parameters | JSONB | NOT NULL | Input parameters |
| result | JSONB | NULLABLE | Tool execution result |
| status | VARCHAR(20) | NOT NULL | Execution status |
| duration_ms | INTEGER | NULLABLE | Execution time |
| created_at | TIMESTAMP | NOT NULL | Invocation time |

**Status Enum Values**:
- `pending` - Tool call initiated
- `success` - Completed successfully
- `error` - Failed with error

**Relationships**:
- Belongs to one Message (many-to-one)

**Indexes**:
- `idx_tool_calls_message_id` on message_id
- `idx_tool_calls_tool_name` on tool_name (for analytics)

## Entity Relationship Diagram

```
┌─────────────┐       ┌──────────────────┐       ┌─────────────┐
│    User     │───────│   Conversation   │───────│   Message   │
└─────────────┘  1:N  └──────────────────┘  1:N  └─────────────┘
      │                                                 │
      │ 1:N                                            │ 1:N
      ▼                                                ▼
┌─────────────┐                                 ┌─────────────┐
│    Task     │                                 │  ToolCall   │
└─────────────┘                                 └─────────────┘
```

## SQLModel Definitions

### Conversation Model

```python
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, List

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: "User" = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
```

### Message Model

```python
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True)
    role: MessageRole = Field(...)
    content: str = Field(...)
    tool_call_id: Optional[str] = Field(default=None, max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")
    tool_calls: List["ToolCall"] = Relationship(
        back_populates="message",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
```

### ToolCall Model

```python
class ToolCallStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    ERROR = "error"

class ToolCall(SQLModel, table=True):
    __tablename__ = "tool_calls"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    message_id: UUID = Field(foreign_key="messages.id", index=True)
    tool_name: str = Field(max_length=100, index=True)
    parameters: dict = Field(default_factory=dict, sa_type=JSONB)
    result: Optional[dict] = Field(default=None, sa_type=JSONB)
    status: ToolCallStatus = Field(default=ToolCallStatus.PENDING)
    duration_ms: Optional[int] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    message: "Message" = Relationship(back_populates="tool_calls")
```

## Migration Strategy

### Migration Order

1. Create `conversations` table
2. Create `messages` table (depends on conversations)
3. Create `tool_calls` table (depends on messages)
4. Add indexes

### Alembic Migration Example

```python
def upgrade():
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_conversations_user_id', 'conversations', ['user_id'])
    op.create_index('idx_conversations_updated_at', 'conversations', ['updated_at'])

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('conversation_id', sa.UUID(), sa.ForeignKey('conversations.id'), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_call_id', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_messages_conversation_id', 'messages', ['conversation_id'])
    op.create_index('idx_messages_created_at', 'messages', ['created_at'])

    # Create tool_calls table
    op.create_table(
        'tool_calls',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('message_id', sa.UUID(), sa.ForeignKey('messages.id'), nullable=False),
        sa.Column('tool_name', sa.String(100), nullable=False),
        sa.Column('parameters', sa.dialects.postgresql.JSONB(), nullable=False),
        sa.Column('result', sa.dialects.postgresql.JSONB(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('duration_ms', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_tool_calls_message_id', 'tool_calls', ['message_id'])
    op.create_index('idx_tool_calls_tool_name', 'tool_calls', ['tool_name'])

def downgrade():
    op.drop_table('tool_calls')
    op.drop_table('messages')
    op.drop_table('conversations')
```

## Data Retention

- Conversations and messages are retained indefinitely by default
- Future consideration: Add `archived_at` field for soft-delete
- Future consideration: Implement retention policy for compliance

## Performance Considerations

1. **Conversation Loading**: Index on `user_id` + `updated_at` for listing recent conversations
2. **Message Ordering**: Index on `conversation_id` + `created_at` for chronological retrieval
3. **Tool Analytics**: Index on `tool_name` for usage statistics
4. **JSONB Fields**: Use JSONB for efficient querying of parameters/results if needed
