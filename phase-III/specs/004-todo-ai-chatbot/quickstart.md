# Quickstart: Todo AI Chatbot

**Feature**: 004-todo-ai-chatbot
**Date**: 2026-02-02

## Prerequisites

- Python 3.11+
- Node.js 20+
- Existing Phase II setup (backend + frontend running)
- OpenAI API key with access to GPT-4

## Environment Setup

### 1. Backend Dependencies

Add to `backend/requirements.txt`:
```
openai-agents>=0.7.0
mcp>=1.26.0
```

Install:
```bash
cd backend
pip install -r requirements.txt
```

### 2. Frontend Dependencies

```bash
cd frontend
npm install @openai/chatkit-react
```

### 3. Environment Variables

Add to `backend/.env`:
```
OPENAI_API_KEY=sk-your-openai-api-key
```

Add to `frontend/.env.local`:
```
NEXT_PUBLIC_CHAT_ENABLED=true
```

## Database Migration

Run the Alembic migration to create conversation tables:

```bash
cd backend
alembic upgrade head
```

This creates:
- `conversations` table
- `messages` table
- `tool_calls` table

## Verification Steps

### 1. Start Backend

```bash
cd backend
uvicorn app.main:app --reload
```

Verify MCP endpoint:
```bash
curl http://localhost:8000/health
```

### 2. Start Frontend

```bash
cd frontend
npm run dev
```

### 3. Test Chat Endpoint

```bash
# Get JWT token first (sign in)
TOKEN=$(curl -X POST http://localhost:8000/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  | jq -r '.token')

# Send chat message
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to test the chatbot"}'
```

Expected response:
```json
{
  "conversation_id": "...",
  "message": "I've added 'test the chatbot' to your todo list.",
  "tool_calls": [...]
}
```

## Quick Test Scenarios

| Say This | Expected Behavior |
|----------|-------------------|
| "Add a task to buy milk" | Creates task, confirms |
| "Show my todos" | Lists all tasks |
| "Mark milk as done" | Completes matching task |
| "Delete all completed" | Removes completed tasks |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "OPENAI_API_KEY not set" | Check backend/.env file |
| 401 on chat endpoint | Verify JWT token is valid |
| "Tool not found" | Restart backend to reload MCP server |
| ChatKit not loading | Check domain allowlist in OpenAI dashboard |

## File Changes Summary

### New Files
- `backend/app/models/conversation.py`
- `backend/app/models/message.py`
- `backend/app/models/tool_call.py`
- `backend/app/schemas/chat.py`
- `backend/app/api/routes/chat.py`
- `backend/app/services/agent.py`
- `backend/app/services/mcp_server.py`
- `frontend/src/app/(protected)/chat/page.tsx`
- `frontend/src/components/chat/ChatInterface.tsx`

### Modified Files
- `backend/requirements.txt`
- `backend/app/main.py` (add chat router)
- `backend/app/models/__init__.py`
- `frontend/package.json`
- `frontend/src/app/(protected)/layout.tsx` (add chat nav)
