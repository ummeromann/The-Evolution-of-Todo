from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, Any, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from app.models.message import Message


class ToolCallStatus(str, Enum):
    """Enum for tool call execution status."""
    PENDING = "pending"
    SUCCESS = "success"
    ERROR = "error"


class ToolCall(SQLModel, table=True):
    """
    Records an MCP tool invocation for audit and debugging.

    Stores the tool name, input parameters, result, and execution metadata.
    Used for tracking tool usage and debugging agent behavior.
    """
    __tablename__ = "tool_calls"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    message_id: UUID = Field(foreign_key="messages.id", index=True)
    tool_name: str = Field(max_length=100, index=True)
    parameters: dict = Field(default_factory=dict, sa_column=Column(JSONB, nullable=False))
    result: Optional[dict] = Field(default=None, sa_column=Column(JSONB, nullable=True))
    status: str = Field(default="pending", max_length=20)  # pending, success, error
    duration_ms: Optional[int] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    message: Optional["Message"] = Relationship(back_populates="tool_calls")
