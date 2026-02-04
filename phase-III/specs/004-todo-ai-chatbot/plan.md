# Implementation Plan: Todo AI Chatbot

**Branch**: `004-todo-ai-chatbot` | **Date**: 2026-02-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-todo-ai-chatbot/spec.md`

## Summary

Implement an AI-powered chatbot that enables natural language todo management using OpenAI Agents SDK and MCP tools. The system extends the existing Phase II web application with a stateless chat API, database-persisted conversations, and a ChatKit-based frontend interface.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript/Node 20+ (frontend)
**Primary Dependencies**: FastAPI, OpenAI Agents SDK (0.7.0), MCP SDK (1.26.0), ChatKit React
**Storage**: Neon PostgreSQL (existing) + 3 new tables (conversations, messages, tool_calls)
**Testing**: pytest (backend), Jest (frontend)
**Target Platform**: Web application (browser + API server)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <5s end-to-end response time for chat interactions
**Constraints**: Stateless API, all state persisted in database, JWT authentication required
**Scale/Scope**: Single-user conversations, ~50 concurrent users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | ✅ PASS | Spec complete at spec.md, plan follows workflow |
| II. Zero Manual Coding | ✅ PASS | All implementation via Claude Code agents |
| III. Security by Design | ✅ PASS | JWT required, user isolation on all operations |
| IV. Single Source of Truth | ✅ PASS | Spec is authoritative |
| V. Clean Separation of Concerns | ✅ PASS | MCP tools separate from API, agent separate from business logic |
| VI. Reproducibility | ✅ PASS | PHR records maintained, ADRs suggested |

**Post-Design Re-check**: All principles maintained. No violations.

## Project Structure

### Documentation (this feature)

```text
specs/004-todo-ai-chatbot/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 research output
├── data-model.md        # Phase 1 data model
├── quickstart.md        # Phase 1 setup guide
├── contracts/
│   ├── chat-api.yaml    # OpenAPI contract for chat endpoints
│   └── mcp-tools.md     # MCP tool definitions
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── models/
│   │   ├── conversation.py    # NEW: Conversation SQLModel
│   │   ├── message.py         # NEW: Message SQLModel
│   │   └── tool_call.py       # NEW: ToolCall SQLModel
│   ├── schemas/
│   │   └── chat.py            # NEW: Chat Pydantic schemas
│   ├── services/
│   │   ├── agent.py           # NEW: OpenAI Agent orchestration
│   │   └── mcp_tools.py       # NEW: MCP tool implementations
│   └── api/routes/
│       └── chat.py            # NEW: Chat API endpoints
├── alembic/versions/
│   └── xxx_add_conversation_tables.py  # NEW: Migration
└── requirements.txt           # MODIFIED: Add openai-agents, mcp

frontend/
├── src/
│   ├── app/(protected)/
│   │   └── chat/
│   │       └── page.tsx       # NEW: Chat page
│   ├── components/
│   │   └── chat/
│   │       ├── ChatInterface.tsx   # NEW: Main chat component
│   │       ├── MessageList.tsx     # NEW: Message display
│   │       └── ChatInput.tsx       # NEW: Input component
│   └── lib/
│       └── chat-api.ts        # NEW: Chat API client
└── package.json               # MODIFIED: Add @openai/chatkit-react
```

**Structure Decision**: Extends existing web application structure (Option 2). New files added to existing directories following established patterns.

## Complexity Tracking

No violations requiring justification. Architecture follows existing patterns.

---

## Implementation Phases

### Phase 1: Architecture & Data Design

**Objective**: Define database models and design stateless request lifecycle

**Tasks**:
1. Create `Conversation` SQLModel with user relationship
2. Create `Message` SQLModel with role enum (user/assistant/tool)
3. Create `ToolCall` SQLModel for audit logging
4. Create Alembic migration for new tables
5. Define MCP tool interface contracts

**Deliverables**:
- `backend/app/models/conversation.py`
- `backend/app/models/message.py`
- `backend/app/models/tool_call.py`
- `backend/alembic/versions/xxx_add_conversation_tables.py`

**Acceptance Criteria**:
- [ ] Tables created in database via migration
- [ ] Models have proper relationships and indexes
- [ ] Foreign keys enforce referential integrity

---

### Phase 2: MCP Server Implementation

**Objective**: Implement MCP tools for todo operations

**Tasks**:
1. Install MCP SDK (`mcp>=1.26.0`)
2. Create MCP server with FastMCP
3. Implement `add_todo` tool with validation
4. Implement `list_todos` tool with filtering
5. Implement `complete_todo` tool with fuzzy matching
6. Implement `update_todo` tool with description matching
7. Implement `delete_todo` tool with bulk delete support
8. Add user context injection for all tools
9. Add comprehensive error handling

**Deliverables**:
- `backend/app/services/mcp_tools.py`

**Acceptance Criteria**:
- [ ] All 5 tools implemented and stateless
- [ ] Tools receive user_id from request context
- [ ] Fuzzy matching works for description-based lookups
- [ ] Error responses follow contract format

---

### Phase 3: AI Agent Setup

**Objective**: Configure OpenAI Agents SDK with MCP tool integration

**Tasks**:
1. Install OpenAI Agents SDK (`openai-agents>=0.7.0`)
2. Create agent service with instructions
3. Define agent persona and behavior guidelines
4. Connect agent to MCP tools via function decorators
5. Implement multi-step tool calling support
6. Add confirmation message generation

**Agent Instructions** (key points):
- Help users manage todo tasks through natural conversation
- Use MCP tools for all task operations (never fake responses)
- Always confirm actions with specific details
- Ask clarifying questions when intent is ambiguous
- Handle errors gracefully with user-friendly messages

**Deliverables**:
- `backend/app/services/agent.py`

**Acceptance Criteria**:
- [ ] Agent interprets natural language to tool calls
- [ ] Multi-step operations work (e.g., list then complete)
- [ ] Agent generates human-friendly confirmations
- [ ] Ambiguous requests trigger clarification

---

### Phase 4: Chat API

**Objective**: Implement stateless chat endpoint with conversation persistence

**Tasks**:
1. Create Pydantic schemas for chat request/response
2. Implement `POST /api/chat` endpoint
3. Load conversation history from database
4. Store user message before agent processing
5. Execute agent with message and history
6. Store assistant response and tool calls
7. Implement `GET /api/conversations` list endpoint
8. Implement `GET /api/conversations/{id}` detail endpoint
9. Implement `DELETE /api/conversations/{id}` endpoint
10. Add comprehensive error handling

**Deliverables**:
- `backend/app/schemas/chat.py`
- `backend/app/api/routes/chat.py`

**Acceptance Criteria**:
- [ ] Chat endpoint requires JWT authentication
- [ ] Conversations persist across requests
- [ ] Tool calls are logged to database
- [ ] API follows OpenAPI contract

---

### Phase 5: Frontend Integration

**Objective**: Build chat UI with conversation management

**Tasks**:
1. Install ChatKit React (`@openai/chatkit-react`)
2. Create chat page at `/chat` route
3. Implement chat interface component
4. Connect to backend chat API
5. Handle new vs existing conversations
6. Display message history on load
7. Show assistant responses and confirmations
8. Handle and display errors gracefully
9. Add navigation to chat from dashboard

**Deliverables**:
- `frontend/src/app/(protected)/chat/page.tsx`
- `frontend/src/components/chat/ChatInterface.tsx`
- `frontend/src/components/chat/MessageList.tsx`
- `frontend/src/components/chat/ChatInput.tsx`
- `frontend/src/lib/chat-api.ts`

**Acceptance Criteria**:
- [ ] Chat UI renders and accepts input
- [ ] Messages display with correct roles
- [ ] Conversation history loads on page visit
- [ ] Errors display as user-friendly messages

---

### Phase 6: Error Handling & Edge Cases

**Objective**: Ensure robust handling of all error scenarios

**Tasks**:
1. Handle missing/non-existent tasks gracefully
2. Handle ambiguous user commands with clarification
3. Handle empty task lists with helpful suggestions
4. Handle OpenAI API failures with retry logic
5. Handle database connection issues
6. Handle rate limiting with user feedback
7. Ensure safe failures don't break chat flow

**Edge Cases**:
| Scenario | Expected Behavior |
|----------|-------------------|
| Empty message | Return validation error |
| Task not found | Agent says "couldn't find that task" |
| Multiple matching tasks | Agent asks for clarification |
| No tasks exist | Agent suggests adding one |
| OpenAI timeout | Return "service busy, try again" |
| Database error | Return "service unavailable" |

**Deliverables**:
- Error handling integrated into all components
- User-friendly error messages throughout

**Acceptance Criteria**:
- [ ] No unhandled exceptions in chat flow
- [ ] All errors return meaningful messages
- [ ] Chat continues working after recoverable errors

---

### Phase 7: Verification & Testing

**Objective**: Validate complete system functionality

**Tasks**:
1. Test all natural language command variations
2. Test conversation persistence across page reloads
3. Test conversation persistence across server restarts
4. Verify stateless behavior (no server-side session state)
5. Confirm all task mutations use MCP tools
6. Test user isolation (multi-user scenarios)
7. Performance test response times

**Test Scenarios**:
| Command | Expected Result |
|---------|-----------------|
| "Add a task to buy groceries" | Task created, confirmation shown |
| "What are my todos?" | List of tasks displayed |
| "Mark groceries as done" | Task completed, confirmation shown |
| "Change groceries to buy milk" | Task updated, confirmation shown |
| "Delete the milk task" | Task deleted, confirmation shown |
| "Remove all completed tasks" | Bulk delete, count reported |

**Deliverables**:
- All tests passing
- Documentation updated

**Acceptance Criteria**:
- [ ] All user stories from spec verified
- [ ] Conversation continuity works after restart
- [ ] No cross-user data leakage
- [ ] Response times within 5 second target

---

## Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| OpenAI API latency | Medium | Medium | Set 30s timeout, show loading state |
| MCP tool registration issues | Low | High | Test tools in isolation first |
| ChatKit domain allowlist | Medium | Low | Document setup in quickstart |
| Conversation context limits | Low | Medium | Truncate old messages if needed |

---

## Dependencies Graph

```
Phase 1 (Data Models)
    │
    ├── Phase 2 (MCP Tools) ──┐
    │                         │
    └── Phase 4 (Chat API) ───┼── Phase 5 (Frontend)
                              │
        Phase 3 (Agent) ──────┘
                              │
                              └── Phase 6 (Error Handling)
                                        │
                                        └── Phase 7 (Verification)
```

---

## Agent Routing Summary

| Phase | Agent | Rationale |
|-------|-------|-----------|
| 1 | `neon-postgres-architect` | Database schema design |
| 2 | `fastapi-backend` | MCP tool implementation |
| 3 | `fastapi-backend` | Agent service in Python |
| 4 | `fastapi-backend` | API endpoint implementation |
| 5 | `nextjs-frontend-builder` | React components |
| 6 | All agents | Cross-cutting error handling |
| 7 | All agents | Integration testing |

---

## Success Metrics

From spec success criteria:
- [ ] SC-001: Todo operations via chat in <30 seconds
- [ ] SC-002: 90%+ intent recognition accuracy
- [ ] SC-003: Conversation resume after restart
- [ ] SC-004: 50 concurrent users supported
- [ ] SC-005: <5s end-to-end response time
- [ ] SC-006: Zero cross-user data leakage
- [ ] SC-007: 95% successful response rate
- [ ] SC-008: 10+ message context maintained
