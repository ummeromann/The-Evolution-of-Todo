# Research: Todo AI Chatbot (Phase III)

**Feature**: 004-todo-ai-chatbot
**Date**: 2026-02-02
**Status**: Complete

## Executive Summary

This research resolves all technical unknowns for implementing the AI-powered todo chatbot. The key finding is that OpenAI Agents SDK has **built-in MCP integration**, making it straightforward to connect the agent to MCP tools. The recommended architecture uses:

- **OpenAI Agents SDK** (v0.7.0) for agent orchestration
- **MCP Python SDK** (v1.26.0) with FastMCP for tool server
- **Streamable HTTP transport** for MCP server connection
- **OpenAI ChatKit** (@openai/chatkit-react) for frontend

## Research Topics

### 1. OpenAI Agents SDK Integration

**Decision**: Use OpenAI Agents SDK with `@function_tool` decorator for direct tool integration

**Rationale**:
- Native MCP support via `MCPServerStreamableHttp` class
- Simple decorator-based tool definition (`@function_tool`)
- Built-in async support with `Runner.run()`
- Automatic conversation history management
- Production-ready framework from OpenAI

**Alternatives Considered**:
| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| OpenAI Agents SDK | Native MCP, async, lightweight | Requires OPENAI_API_KEY | **Selected** |
| LangChain | Popular, many integrations | Heavy, complex for simple use case | Rejected |
| Custom implementation | Full control | Time-consuming, error-prone | Rejected |

**Key Code Pattern**:
```python
from agents import Agent, Runner, function_tool

@function_tool
def add_todo(description: str) -> str:
    """Add a new todo task for the user."""
    # Implementation here
    return f"Created task: {description}"

agent = Agent(
    name="Todo Assistant",
    instructions="Help users manage their todo tasks...",
    tools=[add_todo, list_todos, complete_todo, update_todo, delete_todo]
)

# Run agent
result = await Runner.run(agent, user_message)
```

**Source**: [OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/)

---

### 2. MCP Server Implementation

**Decision**: Use FastMCP with Streamable HTTP transport, embedded in FastAPI

**Rationale**:
- FastMCP simplifies MCP server creation with decorators
- Streamable HTTP works well with existing FastAPI backend
- Tools are stateless and database-backed (matching spec requirements)
- Clear separation between MCP tool definitions and database operations

**Alternatives Considered**:
| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| FastMCP + Streamable HTTP | Clean decorator syntax, HTTP-based | Requires async handling | **Selected** |
| Stdio transport | Simple for CLI | Not suitable for web API | Rejected |
| SSE transport | Legacy support | Deprecation concerns | Rejected |
| Hosted MCP (OpenAI) | No server management | Less control, external dependency | Rejected |

**Key Code Pattern**:
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Todo MCP Server", json_response=True)

@mcp.tool()
async def add_todo(user_id: str, description: str) -> dict:
    """Add a new todo task for the user."""
    # Database operation here
    return {"success": True, "task_id": "...", "description": description}

# Mount in FastAPI
app.mount("/mcp", mcp.get_asgi_app())
```

**Source**: [MCP Python SDK](https://modelcontextprotocol.github.io/python-sdk/)

---

### 3. Agent-MCP Connection Architecture

**Decision**: Use `MCPServerStreamableHttp` to connect agent to local MCP server

**Rationale**:
- Streamable HTTP allows agent to call MCP tools over HTTP
- Supports authentication headers for JWT token passing
- Caching improves performance for tool definitions
- Clean async context manager pattern

**Architecture Flow**:
```
User Message → FastAPI Endpoint → Agent Runner
                                      ↓
                              MCPServerStreamableHttp
                                      ↓
                              FastMCP Server (embedded)
                                      ↓
                              Database Operations
                                      ↓
                              Tool Result → Agent → Response
```

**Key Code Pattern**:
```python
from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

async def process_chat(user_id: str, message: str, jwt_token: str):
    async with MCPServerStreamableHttp(
        name="Todo MCP",
        params={
            "url": "http://localhost:8000/mcp",
            "headers": {"Authorization": f"Bearer {jwt_token}"},
        },
        cache_tools_list=True,
    ) as mcp_server:
        agent = Agent(
            name="Todo Assistant",
            instructions=AGENT_INSTRUCTIONS,
            mcp_servers=[mcp_server],
        )
        result = await Runner.run(agent, message)
        return result.final_output
```

---

### 4. Conversation Persistence Strategy

**Decision**: Store messages in database, reconstruct history per request

**Rationale**:
- Stateless API requirement from spec
- Database persistence enables conversation resumption
- Message roles (user/assistant/tool) align with OpenAI format
- Tool calls stored separately for audit trail

**Data Model**:
```
Conversation
├── id (UUID)
├── user_id (FK → users)
├── created_at
└── updated_at

Message
├── id (UUID)
├── conversation_id (FK → conversations)
├── role (enum: user, assistant, tool)
├── content (text)
├── tool_call_id (optional, for tool results)
└── created_at

ToolCall
├── id (UUID)
├── message_id (FK → messages)
├── tool_name (string)
├── parameters (JSON)
├── result (JSON)
└── created_at
```

**Reconstruction Pattern**:
```python
async def get_conversation_history(conversation_id: str) -> list:
    messages = await db.query(Message).filter_by(conversation_id=conversation_id).all()
    return [{"role": m.role, "content": m.content} for m in messages]
```

---

### 5. Frontend Chat Integration

**Decision**: Use OpenAI ChatKit React component with custom backend

**Rationale**:
- Production-ready chat UI from OpenAI
- React component integrates with existing Next.js frontend
- Supports streaming responses
- Theming matches existing app design

**Alternatives Considered**:
| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| OpenAI ChatKit | Production-ready, official | Domain allowlist setup | **Selected** |
| Custom chat UI | Full control | Development time | Rejected |
| Third-party chat libs | Various features | Inconsistent quality | Rejected |

**Key Integration Pattern**:
```tsx
import { ChatKit } from '@openai/chatkit-react';

export function ChatInterface() {
  return (
    <ChatKit
      clientToken={clientToken}
      theme="dark"
      onMessage={handleMessage}
    />
  );
}
```

**Important**: Domain must be added to OpenAI organization allowlist.

**Source**: [OpenAI ChatKit Documentation](https://platform.openai.com/docs/guides/chatkit)

---

### 6. Authentication Flow for MCP Tools

**Decision**: Pass JWT token to MCP server via HTTP headers

**Rationale**:
- MCP tools need user context for database queries
- JWT contains user_id in 'sub' claim
- Existing middleware validates JWT
- Maintains security isolation per user

**Flow**:
```
1. Frontend includes JWT in chat request
2. FastAPI validates JWT, extracts user_id
3. Agent runner passes JWT to MCP server via headers
4. MCP tools extract user_id from request context
5. All database queries filter by user_id
```

---

### 7. Error Handling Strategy

**Decision**: Graceful degradation with user-friendly messages

**Rationale**:
- OpenAI API failures should not expose technical details
- Database errors return "service unavailable"
- Invalid tool calls handled by agent with clarification requests
- Rate limiting handled with retry guidance

**Error Categories**:
| Error Type | User Message | Technical Action |
|------------|--------------|------------------|
| OpenAI API failure | "I'm having trouble thinking right now. Please try again." | Log error, return 503 |
| Database error | "Service temporarily unavailable." | Log error, return 503 |
| Invalid user intent | Agent asks clarifying question | No error, conversation continues |
| Task not found | "I couldn't find that task." | Return tool result with found=false |
| Rate limit | "Please wait a moment before trying again." | Return 429 with retry-after |

---

## Technology Stack Summary

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Agent SDK | openai-agents | 0.7.0 | Agent orchestration |
| MCP SDK | mcp | 1.26.0 | Tool protocol |
| Frontend Chat | @openai/chatkit-react | latest | Chat UI |
| Backend | FastAPI | existing | API layer |
| Database | Neon PostgreSQL | existing | Persistence |
| ORM | SQLModel | existing | Data models |
| Auth | Better Auth + JWT | existing | Security |

---

## Dependencies to Add

**Backend (requirements.txt additions)**:
```
openai-agents>=0.7.0
mcp>=1.26.0
```

**Frontend (package.json additions)**:
```json
{
  "@openai/chatkit-react": "^latest"
}
```

**Environment Variables (new)**:
```
OPENAI_API_KEY=sk-...
```

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| OpenAI API latency | Medium | Medium | Set timeouts, show loading states |
| Token cost overruns | Low | Low | Monitor usage, set budget alerts |
| MCP transport issues | Low | High | Fallback to direct function tools |
| ChatKit domain setup | Medium | Low | Document setup clearly |

---

## References

- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [OpenAI Agents SDK - MCP Integration](https://openai.github.io/openai-agents-python/mcp/)
- [MCP Python SDK](https://modelcontextprotocol.github.io/python-sdk/)
- [OpenAI ChatKit](https://platform.openai.com/docs/guides/chatkit)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
