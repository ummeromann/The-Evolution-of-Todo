# Tasks: Todo AI Chatbot

**Input**: Design documents from `/specs/004-todo-ai-chatbot/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in spec - tests omitted per template guidelines.

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US6)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/app/`
- **Frontend**: `frontend/src/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install dependencies and configure environment

- [x] T001 Add openai-agents>=0.7.0 and mcp>=1.26.0 to backend/requirements.txt
- [x] T002 [P] Add OPENAI_API_KEY to backend/.env.example with placeholder
- [x] T003 [P] Add @openai/chatkit-react to frontend/package.json via npm install
- [x] T004 [P] Add NEXT_PUBLIC_CHAT_ENABLED=true to frontend/.env.local.example

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Database models and MCP infrastructure that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Models

- [x] T005 [P] Create Conversation SQLModel in backend/app/models/conversation.py with user relationship
- [x] T006 [P] Create Message SQLModel in backend/app/models/message.py with MessageRole enum
- [x] T007 [P] Create ToolCall SQLModel in backend/app/models/tool_call.py with JSONB fields
- [x] T008 Export new models in backend/app/models/__init__.py
- [x] T009 Create Alembic migration for conversations, messages, tool_calls tables in backend/alembic/versions/

### Chat Schemas

- [x] T010 [P] Create ChatRequest Pydantic schema in backend/app/schemas/chat.py
- [x] T011 [P] Create ChatResponse Pydantic schema in backend/app/schemas/chat.py
- [x] T012 [P] Create ConversationListResponse schema in backend/app/schemas/chat.py
- [x] T013 [P] Create ConversationDetailResponse schema in backend/app/schemas/chat.py

### MCP Tools Infrastructure

- [x] T014 Create MCP server with FastMCP in backend/app/services/mcp_tools.py
- [x] T015 Implement fuzzy matching utility function in backend/app/services/mcp_tools.py
- [x] T016 Add user context injection mechanism for MCP tools in backend/app/services/mcp_tools.py

### AI Agent Infrastructure

- [x] T017 Create agent service with OpenAI Agents SDK in backend/app/services/agent.py
- [x] T018 Define agent instructions for todo management in backend/app/services/agent.py
- [x] T019 Connect agent to MCP tools in backend/app/services/agent.py

### Chat API Infrastructure

- [x] T020 Create chat router in backend/app/api/routes/chat.py
- [x] T021 Register chat router in backend/app/main.py

**Checkpoint**: Foundation ready - user story implementation can begin

---

## Phase 3: User Story 1 - Add Todo via Chat (Priority: P1) 🎯 MVP

**Goal**: Users can add tasks via natural language chat

**Independent Test**: Send "Add a task to buy groceries" and verify task appears in database

### MCP Tool Implementation

- [x] T022 [US1] Implement add_todo MCP tool with validation in backend/app/services/mcp_tools.py

### Chat API Implementation

- [x] T023 [US1] Implement POST /api/chat endpoint in backend/app/api/routes/chat.py
- [x] T024 [US1] Implement conversation creation logic for new chats in backend/app/api/routes/chat.py
- [x] T025 [US1] Implement message persistence (user + assistant) in backend/app/api/routes/chat.py
- [x] T026 [US1] Implement tool call logging to database in backend/app/api/routes/chat.py

### Frontend Implementation

- [x] T027 [P] [US1] Create chat API client with sendMessage function in frontend/src/lib/chat-api.ts
- [x] T028 [P] [US1] Create ChatInput component in frontend/src/components/chat/ChatInput.tsx
- [x] T029 [US1] Create ChatInterface component in frontend/src/components/chat/ChatInterface.tsx
- [x] T030 [US1] Create chat page at frontend/src/app/(protected)/chat/page.tsx
- [x] T031 [US1] Add navigation link to chat from dashboard in frontend/src/app/(protected)/layout.tsx

**Checkpoint**: User Story 1 complete - users can add tasks via chat

---

## Phase 4: User Story 2 - List Todos via Chat (Priority: P1)

**Goal**: Users can view their tasks by asking the chatbot

**Independent Test**: Ask "Show my todos" and verify response lists all tasks

### MCP Tool Implementation

- [x] T032 [US2] Implement list_todos MCP tool with filtering in backend/app/services/mcp_tools.py

### Agent Enhancement

- [x] T033 [US2] Add list formatting instructions to agent in backend/app/services/agent.py
- [x] T034 [US2] Add empty list handling with suggestions in backend/app/services/agent.py

### Frontend Enhancement

- [x] T035 [P] [US2] Create MessageList component in frontend/src/components/chat/MessageList.tsx
- [x] T036 [US2] Integrate MessageList into ChatInterface in frontend/src/components/chat/ChatInterface.tsx

**Checkpoint**: User Stories 1 & 2 complete - add and list tasks via chat

---

## Phase 5: User Story 3 - Complete Todo via Chat (Priority: P2)

**Goal**: Users can mark tasks complete through natural language

**Independent Test**: Say "Mark buy groceries as done" and verify task status changes

### MCP Tool Implementation

- [x] T037 [US3] Implement complete_todo MCP tool with fuzzy matching in backend/app/services/mcp_tools.py
- [x] T038 [US3] Handle already-completed task case in complete_todo in backend/app/services/mcp_tools.py
- [x] T039 [US3] Handle multiple matches with clarification request in backend/app/services/mcp_tools.py

### Agent Enhancement

- [x] T040 [US3] Add completion confirmation instructions to agent in backend/app/services/agent.py
- [x] T041 [US3] Add ambiguous match handling instructions in backend/app/services/agent.py

**Checkpoint**: User Story 3 complete - can complete tasks via chat

---

## Phase 6: User Story 4 - Update Todo via Chat (Priority: P2)

**Goal**: Users can update task descriptions through chat

**Independent Test**: Say "Change groceries to buy fruits" and verify description updates

### MCP Tool Implementation

- [x] T042 [US4] Implement update_todo MCP tool with description matching in backend/app/services/mcp_tools.py
- [x] T043 [US4] Return previous description in update response in backend/app/services/mcp_tools.py

### Agent Enhancement

- [x] T044 [US4] Add update confirmation instructions showing old/new descriptions in backend/app/services/agent.py

**Checkpoint**: User Story 4 complete - can update tasks via chat

---

## Phase 7: User Story 5 - Delete Todo via Chat (Priority: P2)

**Goal**: Users can delete tasks through chat

**Independent Test**: Say "Delete the groceries task" and verify it's removed

### MCP Tool Implementation

- [x] T045 [US5] Implement delete_todo MCP tool with single task deletion in backend/app/services/mcp_tools.py
- [x] T046 [US5] Implement bulk delete (delete_completed=true) in delete_todo in backend/app/services/mcp_tools.py
- [x] T047 [US5] Handle delete confirmation and clarification in backend/app/services/mcp_tools.py

### Agent Enhancement

- [x] T048 [US5] Add delete confirmation instructions to agent in backend/app/services/agent.py
- [x] T049 [US5] Add bulk delete reporting instructions in backend/app/services/agent.py

**Checkpoint**: User Story 5 complete - can delete tasks via chat

---

## Phase 8: User Story 6 - Resume Conversation (Priority: P3)

**Goal**: Conversation history persists across sessions

**Independent Test**: Have a conversation, close browser, return, verify previous messages visible

### Backend Implementation

- [x] T050 [US6] Implement GET /api/conversations endpoint in backend/app/api/routes/chat.py
- [x] T051 [US6] Implement GET /api/conversations/{id} endpoint in backend/app/api/routes/chat.py
- [x] T052 [US6] Implement DELETE /api/conversations/{id} endpoint in backend/app/api/routes/chat.py
- [x] T053 [US6] Load conversation history when continuing conversation in backend/app/api/routes/chat.py

### Frontend Implementation

- [x] T054 [P] [US6] Add getConversations function to frontend/src/lib/chat-api.ts
- [x] T055 [P] [US6] Add getConversation function to frontend/src/lib/chat-api.ts
- [x] T056 [P] [US6] Add deleteConversation function to frontend/src/lib/chat-api.ts
- [x] T057 [US6] Create ConversationList sidebar component in frontend/src/components/chat/ConversationList.tsx
- [x] T058 [US6] Load conversation history on page mount in frontend/src/components/chat/ChatInterface.tsx
- [x] T059 [US6] Integrate ConversationList into chat page in frontend/src/app/(protected)/chat/page.tsx

**Checkpoint**: User Story 6 complete - full conversation persistence

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Error handling, edge cases, and final polish

### Error Handling

- [x] T060 [P] Add OpenAI API error handling with user-friendly messages in backend/app/services/agent.py
- [x] T061 [P] Add database error handling in chat endpoints in backend/app/api/routes/chat.py
- [x] T062 [P] Add rate limiting error handling in backend/app/api/routes/chat.py
- [x] T063 [P] Add error display component in frontend/src/components/chat/ChatInterface.tsx
- [x] T064 Add loading states during AI processing in frontend/src/components/chat/ChatInterface.tsx

### Edge Cases

- [x] T065 Handle empty message validation in POST /api/chat in backend/app/api/routes/chat.py
- [x] T066 Handle task not found responses gracefully in agent in backend/app/services/agent.py
- [x] T067 Handle ambiguous commands with clarification requests in backend/app/services/agent.py
- [x] T068 Handle empty task list with suggestions in backend/app/services/agent.py

### Security Hardening

- [x] T069 Verify JWT authentication on all chat endpoints in backend/app/api/routes/chat.py
- [x] T070 Verify user isolation in conversation queries in backend/app/api/routes/chat.py
- [x] T071 Verify user isolation in all MCP tool operations in backend/app/services/mcp_tools.py

### Final Validation

- [x] T072 Run quickstart.md verification steps
- [x] T073 Verify conversation continuity after server restart

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
    │
    └── Phase 2 (Foundational) ─── BLOCKS ALL USER STORIES
            │
            ├── Phase 3 (US1: Add Todo) 🎯 MVP
            │       │
            │       └── Phase 4 (US2: List Todos)
            │               │
            │               ├── Phase 5 (US3: Complete Todo)
            │               │
            │               ├── Phase 6 (US4: Update Todo)
            │               │
            │               └── Phase 7 (US5: Delete Todo)
            │
            └── Phase 8 (US6: Resume Conversation) ─── Can start after Phase 2
                    │
                    └── Phase 9 (Polish) ─── After all stories complete
```

### User Story Dependencies

| Story | Depends On | Can Start After |
|-------|------------|-----------------|
| US1 (Add) | Foundational | Phase 2 complete |
| US2 (List) | US1 | Phase 3 complete |
| US3 (Complete) | US2 | Phase 4 complete |
| US4 (Update) | US2 | Phase 4 complete |
| US5 (Delete) | US2 | Phase 4 complete |
| US6 (Resume) | Foundational | Phase 2 complete |

### Parallel Opportunities

**Phase 2 - Foundational (8 parallel groups)**:
```
Group 1: T005, T006, T007 (models - different files)
Group 2: T010, T011, T012, T013 (schemas - same file but independent)
```

**Phase 3 - US1 Frontend (parallel)**:
```
T027, T028 can run in parallel (different files)
```

**Phase 8 - US6 Frontend API (parallel)**:
```
T054, T055, T056 can run in parallel (same file but independent functions)
```

---

## Implementation Strategy

### MVP First (Phase 1-3 Only)

1. Complete Phase 1: Setup (~4 tasks)
2. Complete Phase 2: Foundational (~17 tasks)
3. Complete Phase 3: User Story 1 - Add Todo (~10 tasks)
4. **STOP and VALIDATE**: Test adding tasks via chat
5. **Deploy/Demo MVP**: Users can add tasks via natural language

### Incremental Delivery

| Milestone | Phases | User Value |
|-----------|--------|------------|
| MVP | 1-3 | Add tasks via chat |
| List | 1-4 | Add + view tasks |
| Full CRUD | 1-7 | All 5 todo operations |
| Persistence | 1-8 | Resume conversations |
| Production | 1-9 | Error handling, polish |

---

## Task Summary

| Phase | Tasks | Parallel | Focus |
|-------|-------|----------|-------|
| 1 Setup | 4 | 3 | Dependencies |
| 2 Foundational | 17 | 8 | Models, schemas, infrastructure |
| 3 US1 Add | 10 | 2 | Core chat + add task |
| 4 US2 List | 5 | 1 | List tasks |
| 5 US3 Complete | 5 | 0 | Complete tasks |
| 6 US4 Update | 3 | 0 | Update tasks |
| 7 US5 Delete | 5 | 0 | Delete tasks |
| 8 US6 Resume | 10 | 3 | Conversation persistence |
| 9 Polish | 14 | 5 | Error handling, security |
| **Total** | **73** | **22** | |

### Per User Story

| User Story | Tasks | MVP? |
|------------|-------|------|
| US1 Add Todo | 10 | Yes |
| US2 List Todos | 5 | No |
| US3 Complete Todo | 5 | No |
| US4 Update Todo | 3 | No |
| US5 Delete Todo | 5 | No |
| US6 Resume | 10 | No |

---

## Notes

- [P] tasks = different files, no dependencies within group
- [US#] label maps task to specific user story for traceability
- Each user story independently testable after its phase completes
- Commit after each task or logical group
- MVP scope: Phases 1-3 only (31 tasks)
- Full feature: All phases (73 tasks)
