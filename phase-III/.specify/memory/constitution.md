<!--
================================================================================
SYNC IMPACT REPORT
================================================================================
Version change: 1.0.0 → 2.0.0 (MAJOR - Phase III architectural transformation)

Modified principles:
- "Phase II Todo Full-Stack Web Application Constitution" → "Phase III Todo AI Chatbot Constitution"
- "Clean Separation of Concerns" → expanded to include MCP and Agent layers

Added sections:
- MCP Architecture Standards (new principle VII)
- AI Agent Behavior Rules (new principle VIII)
- Stateless Backend Architecture (new principle IX)
- Conversation Persistence (new principle X)
- MCP Tool Standards (under Technology & Architecture)
- AI Integration Requirements (under Technology & Architecture)
- Deliverable Enforcement (new section)

Removed sections: None (all Phase II principles retained and extended)

Templates requiring updates:
- ✅ .specify/templates/plan-template.md - Compatible (Constitution Check section exists)
- ✅ .specify/templates/spec-template.md - Compatible (requirements structure aligns)
- ✅ .specify/templates/tasks-template.md - Compatible (web app structure option exists)
- ✅ .specify/templates/phr-template.prompt.md - Compatible (no changes needed)

Follow-up TODOs: None
================================================================================
-->

# Phase III Todo AI Chatbot Constitution

## Core Principles

### I. Spec-Driven Development

All implementation MUST be preceded by approved specifications. No code is written until specs are reviewed and accepted. The development workflow is strictly:

1. Write specification (`/sp.specify`)
2. Generate implementation plan (`/sp.plan`)
3. Break into tasks (`/sp.tasks`)
4. Implement via Claude Code (`/sp.implement`)

**Rationale**: Ensures requirements are captured before implementation begins, reducing rework and maintaining traceability.

### II. Zero Manual Coding

All code MUST be generated through Claude Code using the Agentic Dev Stack workflow. Manual code edits are prohibited. This ensures:

- Full reproducibility from specs and prompts alone
- Consistent code quality via AI-enforced standards
- Complete audit trail of all changes

**Rationale**: Maintains the integrity of the spec-driven approach and enables project regeneration.

### III. Security by Design

Security is mandatory at every layer. Authentication, authorization, and user isolation are non-negotiable requirements:

- Every protected route MUST validate JWT tokens via Better Auth
- Every database query MUST filter by authenticated user ID
- Every MCP tool MUST validate user ownership of tasks before execution
- No cross-user data access is permitted under any circumstance
- Missing/invalid tokens MUST return 401 Unauthorized
- Forbidden access MUST return 403 Forbidden

**Rationale**: Security cannot be bolted on later; it must be architected from the start.

### IV. Single Source of Truth

Specifications override all implementation. When conflicts arise between spec and code, the spec is authoritative. This principle ensures:

- Clear decision authority
- Reduced ambiguity in requirements
- Predictable conflict resolution

**Rationale**: Prevents implementation drift and maintains alignment between documentation and code.

### V. Clean Separation of Concerns

Frontend, backend, AI agent, MCP layer, and database layers MUST be clearly separated:

- **Frontend**: Next.js 16+ (App Router) - Chat UI and user interaction only
- **Backend**: Python FastAPI - API endpoints and request orchestration (stateless)
- **AI Agent**: OpenAI Agents SDK - Natural language processing and tool invocation
- **MCP Layer**: Model Context Protocol tools - All task operations exposed as tools
- **Authentication**: Better Auth with JWT - Security layer
- **Database**: Neon PostgreSQL with SQLModel - Data persistence (single source of state)

No business logic in UI components. No direct database access from AI agents. Each layer has defined responsibilities.

**Rationale**: Enables independent development, testing, and scaling of each layer.

### VI. Reproducibility

The entire project MUST be regenerable using specifications and prompts alone. This requires:

- All features map directly to written specs
- All architectural decisions are documented
- All prompts are recorded in PHR files
- No undocumented manual interventions

**Rationale**: Ensures the project can be rebuilt or audited at any point in its lifecycle.

### VII. MCP-First Task Operations

All task operations MUST be exposed as MCP (Model Context Protocol) tools. Direct database access from AI agents is prohibited:

- AI agents MUST use MCP tools for every task operation
- MCP tools MUST be deterministic and stateless
- MCP tools MUST validate user ownership before execution
- MCP tools MUST return structured responses suitable for AI interpretation
- Tool failures MUST return clear error messages with actionable guidance

Required MCP Tools:
- `create_task` - Create a new todo task
- `list_tasks` - List user's tasks (with optional filters)
- `update_task` - Update task details (title, description)
- `complete_task` - Mark a task as complete
- `delete_task` - Delete a task
- `get_task` - Get details of a specific task

**Rationale**: MCP provides a standardized interface for AI-tool interaction, ensuring predictable behavior and security boundaries.

### VIII. AI Agent Behavior Rules

The AI agent MUST follow strict behavioral guidelines when processing user requests:

- The agent MUST always use MCP tools for task operations (no direct database access)
- Natural language intent MUST be mapped to the correct MCP tool
- Every action MUST return a friendly, human-readable confirmation
- Errors (task not found, invalid input, permission denied) MUST be handled gracefully
- The agent MUST NOT expose internal system details in responses
- The agent MUST maintain conversational context within a session

**Rationale**: Consistent AI behavior ensures predictable user experience and security compliance.

### IX. Stateless Backend Architecture

The FastAPI server MUST maintain zero in-memory state. All state MUST be persisted to the database:

- No in-memory caches for user data or conversation state
- No session storage in server memory
- Every request MUST be processable independently using only database state
- Conversation context MUST be reconstructed from database per request
- Server restarts MUST NOT affect system functionality

**Rationale**: Stateless architecture enables horizontal scaling, fault tolerance, and predictable behavior.

### X. Conversation Persistence

All conversations and messages MUST be stored in PostgreSQL for continuity:

- Every user message MUST be persisted before processing
- Every AI response MUST be persisted after generation
- Conversation history MUST survive server restarts
- Each request MUST reconstruct context from stored history
- Old conversations MUST be resumable at any time

**Rationale**: Persistence ensures conversation continuity and enables audit trails.

## Security Standards

### Authentication & Authorization

| Aspect | Requirement |
|--------|-------------|
| Provider | Better Auth with JWT plugin |
| Token Transport | Authorization: Bearer `<token>` header only |
| Token Expiry | MUST have expiration time set |
| Validation | FastAPI middleware validates every protected request |
| User Isolation | Every query filtered by authenticated user_id |
| MCP Tool Security | Every tool validates user ownership before execution |

### Failure Handling

| Condition | Response |
|-----------|----------|
| Missing token | 401 Unauthorized |
| Invalid/expired token | 401 Unauthorized |
| Valid token, forbidden resource | 403 Forbidden |
| Task not found | 404 Not Found (friendly message via AI) |
| Invalid input | 400 Bad Request (friendly message via AI) |

### Prohibited Practices

- Storing JWT in localStorage (use httpOnly cookies or memory)
- Hardcoding secrets or tokens in code
- Cross-user data access
- Disabling security for convenience
- AI agent direct database queries
- In-memory state storage on backend

## Technology & Architecture Constraints

### Technology Stack (Non-Negotiable)

| Layer | Technology | Version |
|-------|------------|---------|
| Frontend | Next.js (App Router) | 16+ |
| Backend | Python FastAPI | Latest stable |
| ORM | SQLModel | Latest stable |
| Database | Neon Serverless PostgreSQL | - |
| Authentication | Better Auth | Latest stable |
| AI Agent | OpenAI Agents SDK | Latest stable |
| Tool Protocol | Model Context Protocol (MCP) | Latest stable |
| Workflow | Spec-Kit Plus + Claude Code | - |

Alternative frameworks or libraries are prohibited unless explicitly defined in specifications.

### Architecture Requirements

- Clear separation of `frontend/` and `backend/` directories
- API routes follow `/api/{resource}` RESTful pattern
- Chat endpoint: `/api/chat` for AI conversation
- JWT verification implemented as FastAPI middleware
- Frontend API client automatically attaches JWT to requests
- All APIs are RESTful and documented via OpenAPI
- Database schema is normalized and migration-safe
- MCP tools registered and documented
- Conversation and message tables for persistence

### MCP Tool Standards

- Every tool MUST have a clear, single responsibility
- Tools MUST accept user_id as a parameter for ownership validation
- Tools MUST return structured JSON responses
- Tools MUST be idempotent where possible
- Tools MUST log operations for audit trails
- Tool errors MUST be catchable and translatable to user-friendly messages

### AI Integration Requirements

- Agent MUST use OpenAI Agents SDK for tool orchestration
- Agent MUST reconstruct conversation context from database
- Agent MUST map natural language to appropriate MCP tools
- Agent responses MUST be friendly and conversational
- Agent MUST handle ambiguous requests by asking clarifying questions

## Process & Quality Standards

### Development Process

1. **No code before spec approval** - Implementation blocked until spec is reviewed
2. **No implementation without plan** - Plan must be generated from spec
3. **No manual code edits** - All changes through Claude Code
4. **Independent reviewability** - Each phase can be reviewed separately
5. **Full documentation** - All iterations and decisions documented
6. **Sequential completion** - Each spec completed before moving to next

### Quality Bar

All deliverables MUST meet these criteria:

- [ ] No broken user flows
- [ ] No security vulnerabilities
- [ ] No hardcoded secrets (use `.env`)
- [ ] No missing specifications
- [ ] No manual code present
- [ ] All APIs documented
- [ ] Frontend chat UI is responsive and accessible
- [ ] Database persists conversations and tasks correctly
- [ ] User data isolation verified
- [ ] MCP tools documented and tested
- [ ] AI agent behavior verified against rules
- [ ] Server remains stateless (verified by restart test)

### Success Criteria

Phase III is complete only when:

- Tasks can be fully managed via chat interface
- MCP tools are used for every task operation
- Server remains stateless (survives restarts)
- Specs, MCP tools, and agent behavior are documented
- System resumes conversations after restart
- Multi-user authentication functioning correctly
- JWT-based security fully enforced
- Each user sees and modifies only their own tasks
- Project regenerable using specs + prompts only
- Agentic workflow visible and reviewable

## Deliverable Enforcement

### Phase III Completion Checklist

- [ ] Natural language todo management via chat
- [ ] All task operations via MCP tools (no direct DB from agent)
- [ ] Stateless FastAPI backend verified
- [ ] Conversation persistence in PostgreSQL
- [ ] Conversation resumption after server restart
- [ ] User authentication and authorization
- [ ] MCP tool documentation complete
- [ ] AI agent behavior rules enforced
- [ ] Full specification coverage

### Verification Tests

1. **Stateless Test**: Restart server mid-conversation, verify conversation continues
2. **MCP Test**: Verify all task operations use MCP tools
3. **Security Test**: Verify user cannot access another user's tasks
4. **Persistence Test**: Verify conversations survive database reconnection

## Governance

### Amendment Process

1. Proposed changes MUST be documented with rationale
2. Changes require explicit approval before adoption
3. All amendments MUST include migration plan for existing work
4. Version number MUST be updated per semantic versioning

### Versioning Policy

- **MAJOR**: Backward-incompatible principle changes or removals
- **MINOR**: New principles added or existing materially expanded
- **PATCH**: Clarifications, wording improvements, non-semantic changes

### Compliance

- All specifications MUST reference relevant constitution principles
- All PRs/reviews MUST verify constitution compliance
- Violations require documented justification and approval
- Constitution supersedes all other project documentation

**Version**: 2.0.0 | **Ratified**: 2026-01-13 | **Last Amended**: 2026-01-20
