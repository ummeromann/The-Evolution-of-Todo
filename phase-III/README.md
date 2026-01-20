# Phase-II: Multi-User Todo Web Application

A full-stack todo application with user authentication, built using Spec-Driven Development (SDD) methodology.

## Project Overview

Phase-II transforms the Phase-I console application into a modern, multi-user web application with:

- User registration and authentication
- Personal task management (Create, Read, Update, Delete)
- Task completion tracking
- Persistent storage with PostgreSQL
- Responsive web interface

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 16+, TypeScript, React 19, Tailwind CSS |
| Backend | Python 3.10+, FastAPI, SQLModel ORM |
| Database | Neon Serverless PostgreSQL |
| Authentication | Better Auth with JWT tokens |

## Project Structure

```
phase-II/
├── backend/                 # FastAPI Python backend
│   ├── app/
│   │   ├── main.py         # Application entry point
│   │   ├── config.py       # Configuration management
│   │   ├── database.py     # Database connection
│   │   ├── api/routes/     # API endpoints
│   │   ├── models/         # SQLModel ORM models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── middleware/     # Auth middleware
│   └── requirements.txt
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # App Router pages
│   │   ├── components/    # React components
│   │   ├── lib/           # Utilities and API client
│   │   └── contexts/      # React contexts
│   └── package.json
├── specs/                  # Feature specifications
├── history/               # Development history
├── .specify/              # Constitution and templates
└── CLAUDE.md              # AI assistant instructions
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 18+
- Neon PostgreSQL database account

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd phase-II/backend
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
   ```

7. Run the backend server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd phase-II/frontend
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
   cd phase-II/backend
   venv/Scripts/activate  # or source venv/bin/activate
   uvicorn app.main:app --reload --port 8000
   ```

2. Start the frontend server (port 3000):
   ```bash
   cd phase-II/frontend
   npm run dev
   ```

3. Open http://localhost:3000 in your browser

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/auth/signup` | Register new user | No |
| POST | `/auth/signin` | Login user | No |
| GET | `/tasks` | List user's tasks | Yes |
| POST | `/tasks` | Create new task | Yes |
| PUT | `/tasks/{id}` | Update task | Yes |
| DELETE | `/tasks/{id}` | Delete task | Yes |
| PATCH | `/tasks/{id}/toggle` | Toggle completion | Yes |
| GET | `/health` | Health check | No |

API documentation available at: http://localhost:8000/docs

## Features

### Authentication
- Email/password registration
- Secure login with JWT tokens
- Protected routes and API endpoints
- User session management

### Task Management
- Create tasks with descriptions (1-500 characters)
- View all personal tasks
- Edit task descriptions
- Delete tasks permanently
- Toggle task completion status
- Data persists across sessions

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

## License

MIT License
