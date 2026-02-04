# Phase-III: Todo AI Chatbot

An AI-powered todo management application with natural language chat interface, built using Spec-Driven Development (SDD) methodology.

## Project Overview

Phase-III transforms the Phase-II multi-user web application into an intelligent AI chatbot experience. Users can manage their todos through natural language conversations powered by OpenAI Agents SDK and MCP (Model Context Protocol) tools.

### Key Features

- **Natural Language Todo Management**: Add, list, update, complete, and delete tasks through conversational chat
- **AI-Powered Agent**: Intelligent intent recognition and context-aware responses
- **MCP Tools Integration**: Standardized tool protocol for todo operations
- **Conversation Persistence**: Resume conversations after server restarts
- **Multi-User Authentication**: Secure JWT-based authentication with Better Auth
- **Responsive Chat Interface**: Modern web-based chat UI

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 16+, TypeScript, React 19, Tailwind CSS |
| Backend | Python 3.10+, FastAPI, SQLModel ORM |
| Database | Neon Serverless PostgreSQL |
| Authentication | Better Auth with JWT tokens |
| AI/LLM | OpenAI Agents SDK (supports Ollama for local LLMs) |
| Tools Protocol | MCP (Model Context Protocol) |

## Project Structure

```
phase-III/
├── backend/                 # FastAPI Python backend
│   ├── app/
│   │   ├── main.py         # Application entry point
│   │   ├── config.py       # Configuration management
│   │   ├── database.py     # Database connection
│   │   ├── api/routes/     # API endpoints
│   │   │   ├── chat.py     # Chat/conversation endpoints
│   │   │   ├── tasks.py    # Todo CRUD endpoints
│   │   │   └── health.py   # Health check
│   │   ├── models/         # SQLModel ORM models
│   │   │   ├── task.py     # Todo task model
│   │   │   ├── conversation.py  # Chat conversation model
│   │   │   └── message.py  # Chat message model
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   │   ├── agent.py    # AI agent orchestration
│   │   │   └── mcp_tools.py # MCP tool implementations
│   │   └── middleware/     # Auth middleware
│   └── requirements.txt
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # App Router pages
│   │   │   ├── (auth)/    # Auth pages (signin/signup)
│   │   │   └── (protected)/ # Protected pages
│   │   │       └── chat/  # Chat interface page
│   │   ├── components/    # React components
│   │   │   ├── chat/      # Chat UI components
│   │   │   │   ├── ChatInterface.tsx
│   │   │   │   ├── MessageList.tsx
│   │   │   │   └── ConversationList.tsx
│   │   │   ├── tasks/     # Task management components
│   │   │   └── ui/        # Shared UI components
│   │   └── lib/           # Utilities
│   │       ├── auth.ts    # Auth configuration
│   │       └── chat-api.ts # Chat API client
│   └── package.json
├── specs/                  # Feature specifications
│   └── 004-todo-ai-chatbot/ # AI Chatbot feature spec
├── history/               # Development history (PHRs)
├── .specify/              # Constitution and templates
└── CLAUDE.md              # AI assistant instructions
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 18+
- Neon PostgreSQL database account
- OpenAI API key (or Ollama for local LLM)

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd phase-III/backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate virtual environment:
   ```bash
   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create `.env` file from example:
   ```bash
   cp .env.example .env
   ```

6. Configure environment variables in `.env`:
   ```
   DATABASE_URL=postgresql+asyncpg://user:password@host/database
   BETTER_AUTH_SECRET=your-secret-key-min-32-chars
   CORS_ORIGINS=http://localhost:3000
   OPENAI_API_KEY=your-openai-api-key
   ```

   **For Ollama (local LLM):**
   ```
   OPENAI_API_KEY=ollama
   OPENAI_BASE_URL=http://localhost:11434/v1
   ```

7. Run database migrations:
   ```bash
   alembic upgrade head
   ```

8. Run the backend server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd phase-III/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create `.env.local` file from example:
   ```bash
   cp .env.local.example .env.local
   ```

4. Configure environment variables in `.env.local`:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   BETTER_AUTH_SECRET=your-secret-key-min-32-chars
   ```

5. Run the frontend server:
   ```bash
   npm run dev
   ```

## Running the Application

1. Start the backend server (port 8000):
   ```bash
   cd phase-III/backend
   venv/Scripts/activate  # or source venv/bin/activate
   uvicorn app.main:app --reload --port 8000
   ```

2. Start the frontend server (port 3000):
   ```bash
   cd phase-III/frontend
   npm run dev
   ```

3. Open http://localhost:3000 in your browser

4. Sign up or sign in, then navigate to the Chat page

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/auth/signup` | Register new user | No |
| POST | `/auth/signin` | Login user | No |

### Tasks (REST API)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/tasks` | List user's tasks | Yes |
| POST | `/tasks` | Create new task | Yes |
| PUT | `/tasks/{id}` | Update task | Yes |
| DELETE | `/tasks/{id}` | Delete task | Yes |
| PATCH | `/tasks/{id}/toggle` | Toggle completion | Yes |

### Chat (AI Chatbot)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/chat/conversations` | List user's conversations | Yes |
| POST | `/chat/conversations` | Create new conversation | Yes |
| GET | `/chat/conversations/{id}` | Get conversation with messages | Yes |
| POST | `/chat/conversations/{id}/messages` | Send message to AI agent | Yes |
| DELETE | `/chat/conversations/{id}` | Delete conversation | Yes |

### Health

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/health` | Health check | No |

API documentation available at: http://localhost:8000/docs

## Features

### AI Chat Interface
- Natural language todo management
- Multi-turn conversation support
- Context-aware responses
- Conversation history persistence
- Real-time message streaming

### MCP Tools
The AI agent uses these MCP tools to manage todos:

| Tool | Description |
|------|-------------|
| `add_todo` | Create a new task |
| `list_todos` | Retrieve user's tasks |
| `update_todo` | Modify task description |
| `complete_todo` | Mark task as done |
| `delete_todo` | Remove a task |

### Example Conversations

**Adding a task:**
> User: "Add a task to buy groceries"
> Assistant: "I've added 'buy groceries' to your todo list!"

**Listing tasks:**
> User: "Show me my tasks"
> Assistant: "Here are your tasks: 1. Buy groceries (pending) 2. Call dentist (completed)"

**Completing a task:**
> User: "Mark buy groceries as done"
> Assistant: "Done! I've marked 'buy groceries' as complete."

**Deleting a task:**
> User: "Delete the groceries task"
> Assistant: "I've removed 'buy groceries' from your todo list."

### Authentication
- Email/password registration
- Secure login with JWT tokens
- Protected routes and API endpoints
- User session management
- Data isolation between users

### User Experience
- Responsive design (mobile + desktop)
- Loading states during operations
- Clear error messages
- Empty state guidance
- Dark/light theme support

## Development Workflow

This project follows Spec-Driven Development (SDD):

1. **Specification** (`specs/`) - Feature requirements
2. **Planning** (`specs/*/plan.md`) - Architecture decisions
3. **Tasks** (`specs/*/tasks.md`) - Implementation breakdown
4. **Implementation** - Code generated via Claude Code

## Architecture

```
┌──────────────────┐     ┌───────────────────┐     ┌──────────────────┐
│   Chat UI        │────>│   FastAPI API     │────>│   PostgreSQL     │
│   (Next.js)      │     │   (Stateless)     │     │   (Neon)         │
└──────────────────┘     └───────────────────┘     └──────────────────┘
                                │
                                v
                      ┌───────────────────┐
                      │   OpenAI Agent    │
                      │   (Agents SDK)    │
                      └───────────────────┘
                                │
                                v
                      ┌───────────────────┐
                      │   MCP Tools       │
                      │   (Todo Ops)      │
                      └───────────────────┘
```

**Data Flow:**
1. User sends message via Chat UI
2. Frontend calls stateless FastAPI endpoint with JWT token
3. API loads conversation history from database
4. API invokes OpenAI Agent with message and history
5. Agent determines intent and calls MCP tools as needed
6. MCP tools execute operations against database
7. Agent generates response
8. API persists new messages and returns response
9. Frontend displays response to user

## License

MIT License
