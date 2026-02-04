"""
AI Agent Service for Todo Chatbot.

This module implements the OpenAI Agent that processes natural language
messages and invokes MCP tools to perform todo operations.

The agent:
- Interprets user intent from natural language
- Calls appropriate MCP tools (add, list, complete, update, delete)
- Generates human-friendly confirmation messages
- Handles ambiguous requests with clarification questions
"""

import os
from typing import List, Dict, Any, Optional
from uuid import UUID

from agents import Agent, Runner, function_tool, set_default_openai_client
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

# Configure OpenAI client for custom base URL (Ollama, Groq, etc.)
_base_url = os.environ.get("OPENAI_BASE_URL")
_api_key = os.environ.get("OPENAI_API_KEY", "ollama")

if _base_url:
    _client = AsyncOpenAI(
        base_url=_base_url,
        api_key=_api_key,
    )
    set_default_openai_client(_client)

from app.services.mcp_tools import (
    add_todo,
    list_todos,
    complete_todo,
    update_todo,
    delete_todo,
    set_mcp_context,
    clear_mcp_context,
)


# ============================================================================
# Agent Instructions
# ============================================================================

AGENT_INSTRUCTIONS = """You are a helpful AI assistant that helps users manage their todo tasks through natural conversation.

## Your Capabilities
You have access to the following tools to manage tasks:
- add_todo: Create a new task
- list_todos: View all tasks (can filter to show only incomplete tasks)
- complete_todo: Mark a task as done
- update_todo: Change a task's description
- delete_todo: Remove a task or all completed tasks

## Guidelines

### 1. Always Use Tools for Task Operations
- NEVER pretend to perform task operations without calling the appropriate tool
- If a user asks to add, list, complete, update, or delete tasks, you MUST use the tools
- Report the actual result from the tool, don't make up responses

### 2. Confirm Actions Clearly
- After adding a task: "I've added '{description}' to your todo list."
- After completing a task: "Done! I've marked '{description}' as complete."
- After updating a task: "I've updated '{old}' to '{new}'."
- After deleting a task: "I've removed '{description}' from your list."
- After listing tasks: Format as a numbered list with checkmarks for completed items

### 3. Handle Ambiguity
- If the user's request is unclear, ask a clarifying question
- If multiple tasks match a description, present the options and ask which one
- If no tasks match, let the user know and suggest alternatives

### 4. Be Conversational and Helpful
- Respond naturally and conversationally
- If the user has no tasks, suggest they add one
- If all tasks are complete, congratulate them
- Keep responses concise but informative

### 5. Handle Errors Gracefully
- If a tool returns an error, explain it in user-friendly terms
- Don't expose technical details like IDs or stack traces
- Suggest what the user can do next

## Examples

User: "Add a task to buy groceries"
You: [Call add_todo with description="buy groceries"]
Response: "I've added 'buy groceries' to your todo list."

User: "What are my tasks?"
You: [Call list_todos]
Response: "Here are your tasks:
1. ✓ Call dentist
2. Buy groceries
3. Finish report

You have 3 tasks total (1 completed, 2 pending)."

User: "Mark groceries as done"
You: [Call complete_todo with description_match="groceries"]
Response: "Done! I've marked 'buy groceries' as complete."

User: "I need to remember something"
Response: "Sure! What would you like me to add to your todo list?"

User: "Delete the completed tasks"
You: [Call delete_todo with delete_completed=True]
Response: "I've removed 2 completed tasks from your list."
"""


# ============================================================================
# Function Tools for Agent
# ============================================================================

@function_tool(name_override="add_todo")
async def fn_add_todo(description: str) -> dict:
    """
    Add a new todo task for the user.

    Args:
        description: The task description (1-500 characters)
    """
    return await add_todo(description)


@function_tool(name_override="list_todos")
async def fn_list_todos(include_completed: bool = True) -> dict:
    """
    List all todo tasks for the user.

    Args:
        include_completed: Whether to include completed tasks (default: true)
    """
    return await list_todos(include_completed)


@function_tool(name_override="complete_todo")
async def fn_complete_todo(
    task_id: str = None,
    description_match: str = None
) -> dict:
    """
    Mark a task as completed.

    Args:
        task_id: Specific task UUID (optional, provide this OR description_match)
        description_match: Text to match against task descriptions (optional)
    """
    return await complete_todo(task_id, description_match)


@function_tool(name_override="update_todo")
async def fn_update_todo(
    new_description: str,
    task_id: str = None,
    description_match: str = None
) -> dict:
    """
    Update a task's description.

    Args:
        new_description: The new task description
        task_id: Specific task UUID (optional, provide this OR description_match)
        description_match: Text to match against current task descriptions (optional)
    """
    return await update_todo(new_description, task_id, description_match)


@function_tool(name_override="delete_todo")
async def fn_delete_todo(
    task_id: str = None,
    description_match: str = None,
    delete_completed: bool = False
) -> dict:
    """
    Delete a task or all completed tasks.

    Args:
        task_id: Specific task UUID (optional)
        description_match: Text to match against task descriptions (optional)
        delete_completed: Set to True to delete all completed tasks (optional)
    """
    return await delete_todo(task_id, description_match, delete_completed)


# ============================================================================
# Agent Creation
# ============================================================================

def create_todo_agent() -> Agent:
    """Create and configure the Todo AI Agent."""
    # Use model from environment variable (supports OpenAI, Groq, Ollama, etc.)
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    return Agent(
        name="Todo Assistant",
        instructions=AGENT_INSTRUCTIONS,
        model=model,
        tools=[
            fn_add_todo,
            fn_list_todos,
            fn_complete_todo,
            fn_update_todo,
            fn_delete_todo,
        ],
    )


# ============================================================================
# Main Processing Function
# ============================================================================

async def process_chat_message(
    user_id: UUID,
    message: str,
    conversation_history: List[Dict[str, str]],
    db: AsyncSession
) -> Dict[str, Any]:
    """
    Process a chat message through the AI agent.

    Args:
        user_id: The authenticated user's ID
        message: The user's natural language message
        conversation_history: Previous messages in the conversation
        db: Database session for MCP tools

    Returns:
        Dict containing:
        - response: The agent's text response
        - tool_calls: List of tools that were invoked
    """
    # Set MCP context for tools
    set_mcp_context(user_id, db)

    try:
        # Create agent
        agent = create_todo_agent()

        # Build input with conversation history
        # Format: list of {"role": "user"|"assistant", "content": "..."}
        messages = []
        for msg in conversation_history:
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", ""),
            })

        # Add current message
        messages.append({
            "role": "user",
            "content": message,
        })

        # Run agent
        result = await Runner.run(
            agent,
            messages,
        )

        # Extract tool calls from result
        tool_calls = []
        if hasattr(result, 'raw_responses'):
            for response in result.raw_responses:
                if hasattr(response, 'output') and response.output:
                    for item in response.output:
                        if hasattr(item, 'type') and item.type == 'function_call':
                            tool_calls.append({
                                "tool_name": item.name if hasattr(item, 'name') else "unknown",
                                "parameters": item.arguments if hasattr(item, 'arguments') else {},
                                "result": None,  # Result captured separately
                            })

        return {
            "response": result.final_output if hasattr(result, 'final_output') else str(result),
            "tool_calls": tool_calls,
        }

    except Exception as e:
        # Log error for debugging
        import traceback
        traceback.print_exc()

        # Determine user-friendly error message based on error type
        error_str = str(e).lower()

        if "rate limit" in error_str or "rate_limit" in error_str:
            user_message = "I'm receiving too many requests right now. Please wait a moment and try again."
        elif "api key" in error_str or "authentication" in error_str or "unauthorized" in error_str:
            user_message = "There's a configuration issue with the AI service. Please contact support."
        elif "timeout" in error_str or "timed out" in error_str:
            user_message = "The request took too long to process. Please try a simpler request or try again."
        elif "context length" in error_str or "token" in error_str:
            user_message = "Your conversation has become too long. Please start a new chat to continue."
        elif "connection" in error_str or "network" in error_str:
            user_message = "I'm having trouble connecting to the AI service. Please try again in a moment."
        elif "invalid" in error_str and "model" in error_str:
            user_message = "There's a configuration issue with the AI model. Please contact support."
        else:
            user_message = "I'm having trouble processing your request right now. Please try again."

        return {
            "response": user_message,
            "tool_calls": [],
            "error": str(e),
        }

    finally:
        # Clear MCP context
        clear_mcp_context()
