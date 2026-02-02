"""
Pydantic schemas for the AI Chat API.

These schemas define the request and response formats for:
- Chat message submission
- Conversation listing and retrieval
- Tool call records
"""

from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional, List, Any


# ============================================================================
# Chat Request/Response Schemas
# ============================================================================

class ChatRequest(BaseModel):
    """Schema for submitting a chat message."""
    message: str = Field(min_length=1, max_length=2000, description="Natural language message from the user")
    conversation_id: Optional[UUID] = Field(
        default=None,
        description="Existing conversation ID to continue, or null for new conversation"
    )


class ToolCallRecord(BaseModel):
    """Schema for recording a tool invocation."""
    tool_name: str = Field(description="Name of the MCP tool invoked")
    parameters: dict = Field(default_factory=dict, description="Parameters passed to the tool")
    result: Optional[dict] = Field(default=None, description="Result returned by the tool")


class ChatResponse(BaseModel):
    """Schema for chat response from AI assistant."""
    conversation_id: UUID = Field(description="The conversation ID (new or existing)")
    message: str = Field(description="AI assistant's response message")
    tool_calls: List[ToolCallRecord] = Field(
        default_factory=list,
        description="List of MCP tools invoked during this interaction"
    )


# ============================================================================
# Conversation Schemas
# ============================================================================

class ConversationSummary(BaseModel):
    """Schema for conversation summary in list view."""
    id: UUID
    title: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    message_count: int

    model_config = {"from_attributes": True}


class ConversationListResponse(BaseModel):
    """Schema for listing user's conversations."""
    conversations: List[ConversationSummary]
    total: int


class MessageResponse(BaseModel):
    """Schema for a single message in a conversation."""
    id: UUID
    role: str  # user, assistant, tool
    content: str
    tool_call_id: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationDetailResponse(BaseModel):
    """Schema for full conversation with messages."""
    id: UUID
    title: Optional[str] = None
    messages: List[MessageResponse]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ============================================================================
# Error Schemas
# ============================================================================

class ChatErrorResponse(BaseModel):
    """Schema for chat error responses."""
    detail: str = Field(description="Human-readable error message")
    code: str = Field(description="Machine-readable error code")
