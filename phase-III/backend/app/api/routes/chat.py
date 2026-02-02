"""
Chat API routes for AI-powered todo management.

This module implements the chat endpoints:
- POST /api/chat: Send a message to the AI assistant
- GET /api/conversations: List user's conversations
- GET /api/conversations/{id}: Get conversation with messages
- DELETE /api/conversations/{id}: Delete a conversation

All endpoints require JWT authentication.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlmodel import select, func
from uuid import UUID
from datetime import datetime
from typing import Optional
import logging

from app.api.deps import get_db, get_current_user
from app.api.rate_limit import check_chat_rate_limit

logger = logging.getLogger(__name__)
from app.models import Conversation, Message, ToolCall
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ToolCallRecord,
    ConversationListResponse,
    ConversationSummary,
    ConversationDetailResponse,
    MessageResponse,
)
from app.services.agent import process_chat_message

router = APIRouter(prefix="/api", tags=["chat"])


# ============================================================================
# Chat Endpoint
# ============================================================================

@router.post("/chat", response_model=ChatResponse, dependencies=[Depends(check_chat_rate_limit)])
async def send_chat_message(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user),
):
    """
    Send a natural language message to the AI assistant.

    The assistant will interpret the intent and execute todo operations as needed.
    Creates a new conversation if conversation_id is not provided.

    Args:
        request: ChatRequest with message and optional conversation_id

    Returns:
        ChatResponse with assistant's reply and tool calls

    Raises:
        400: Bad request if message is empty
        401: Unauthorized if JWT is invalid
        404: Conversation not found (if conversation_id provided)
        503: Service unavailable if AI service fails
    """
    # T065: Validate empty message
    if not request.message or not request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )

    conversation = None

    # Get or create conversation
    if request.conversation_id:
        # Verify conversation belongs to user
        query = select(Conversation).where(
            Conversation.id == request.conversation_id,
            Conversation.user_id == user_id
        )
        result = await db.execute(query)
        conversation = result.scalar_one_or_none()

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
    else:
        # Create new conversation
        conversation = Conversation(
            user_id=user_id,
            title=None,  # Will be auto-generated later if needed
        )
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)

    # Load conversation history
    history_query = select(Message).where(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at)
    history_result = await db.execute(history_query)
    history_messages = history_result.scalars().all()

    conversation_history = [
        {"role": msg.role, "content": msg.content}
        for msg in history_messages
        if msg.role in ("user", "assistant")
    ]

    # Store user message
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=request.message,
    )
    db.add(user_message)
    await db.commit()

    try:
        # Process through AI agent
        agent_result = await process_chat_message(
            user_id=user_id,
            message=request.message,
            conversation_history=conversation_history,
            db=db,
        )

        # Store assistant response
        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=agent_result["response"],
        )
        db.add(assistant_message)
        await db.commit()
        await db.refresh(assistant_message)

        # Store tool calls
        tool_call_records = []
        for tc in agent_result.get("tool_calls", []):
            tool_call = ToolCall(
                message_id=assistant_message.id,
                tool_name=tc.get("tool_name", "unknown"),
                parameters=tc.get("parameters", {}),
                result=tc.get("result"),
                status="success",
            )
            db.add(tool_call)
            tool_call_records.append(ToolCallRecord(
                tool_name=tc.get("tool_name", "unknown"),
                parameters=tc.get("parameters", {}),
                result=tc.get("result"),
            ))

        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        await db.commit()

        return ChatResponse(
            conversation_id=conversation.id,
            message=agent_result["response"],
            tool_calls=tool_call_records,
        )

    except SQLAlchemyError as e:
        # T061: Handle database errors
        logger.error(f"Database error in chat endpoint: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred. Please try again."
        )

    except Exception as e:
        # Log error but return user-friendly message
        logger.error(f"Chat processing error: {e}", exc_info=True)

        # Try to save an error response if we have a conversation
        try:
            if conversation:
                error_message = Message(
                    conversation_id=conversation.id,
                    role="assistant",
                    content="I'm having trouble processing your request. Please try again.",
                )
                db.add(error_message)
                await db.commit()
        except Exception:
            # If saving also fails, just rollback and continue
            await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service temporarily unavailable. Please try again."
        )


# ============================================================================
# Conversation Endpoints
# ============================================================================

@router.get("/conversations", response_model=ConversationListResponse)
async def list_conversations(
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user),
):
    """
    List all conversations for the authenticated user.

    Conversations are ordered by most recent first.

    Args:
        limit: Maximum number of conversations to return (1-100)
        offset: Number of conversations to skip

    Returns:
        ConversationListResponse with conversation summaries
    """
    # Clamp limit
    limit = max(1, min(100, limit))
    offset = max(0, offset)

    # Get conversations with message counts
    query = select(Conversation).where(
        Conversation.user_id == user_id
    ).order_by(Conversation.updated_at.desc()).offset(offset).limit(limit)

    result = await db.execute(query)
    conversations = result.scalars().all()

    # Get total count
    count_query = select(func.count(Conversation.id)).where(
        Conversation.user_id == user_id
    )
    count_result = await db.execute(count_query)
    total = count_result.scalar()

    # Build response with message counts
    summaries = []
    for conv in conversations:
        # Get message count for this conversation
        msg_count_query = select(func.count(Message.id)).where(
            Message.conversation_id == conv.id
        )
        msg_count_result = await db.execute(msg_count_query)
        msg_count = msg_count_result.scalar()

        summaries.append(ConversationSummary(
            id=conv.id,
            title=conv.title,
            created_at=conv.created_at,
            updated_at=conv.updated_at,
            message_count=msg_count,
        ))

    return ConversationListResponse(
        conversations=summaries,
        total=total,
    )


@router.get("/conversations/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(
    conversation_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user),
):
    """
    Get a conversation with all its messages.

    Args:
        conversation_id: The conversation UUID

    Returns:
        ConversationDetailResponse with full message history

    Raises:
        404: Conversation not found
    """
    # Get conversation
    query = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    result = await db.execute(query)
    conversation = result.scalar_one_or_none()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    # Get messages
    msg_query = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at)
    msg_result = await db.execute(msg_query)
    messages = msg_result.scalars().all()

    return ConversationDetailResponse(
        id=conversation.id,
        title=conversation.title,
        messages=[
            MessageResponse(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                tool_call_id=msg.tool_call_id,
                created_at=msg.created_at,
            )
            for msg in messages
        ],
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
    )


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user),
):
    """
    Delete a conversation and all its messages.

    Args:
        conversation_id: The conversation UUID

    Raises:
        404: Conversation not found
    """
    # Get conversation
    query = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    result = await db.execute(query)
    conversation = result.scalar_one_or_none()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    # Delete (cascade will handle messages and tool_calls)
    await db.delete(conversation)
    await db.commit()

    return None
