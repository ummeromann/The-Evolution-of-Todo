# Quickstart Guide: Todo Full-Stack Web Application

**Feature Branch**: `001-todo-fullstack-webapp`
**Date**: 2026-01-13

## Prerequisites

Before starting, ensure you have:

- [ ] Node.js 18+ installed
- [ ] Python 3.11+ installed
- [ ] Git installed
- [ ] Neon PostgreSQL account (free tier sufficient)
- [ ] Code editor (VS Code recommended)

---

## Project Structure Overview

```text
phase-II/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py            # Application entry point
│   │   ├── config.py          # Environment configuration
│   │   ├── database.py        # Database connection
│   │   ├── models/            # SQLModel definitions
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── api/               # API routes
│   │   └── middleware/        # Auth middleware
│   ├── alembic/               # Database migrations
│   ├── tests/                 # Backend tests
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                   # Next.js frontend
│   ├── src/
│   │   ├── app/               # App Router pages
│   │   ├── components/        # React components
│   │   ├── lib/               # Utilities and clients
│   │   └── types/             # TypeScript types
│   ├── public/
│   ├── package.json
│   └── .env.local.example
│
└── specs/                      # Specification documents
    └── 001-todo-fullstack-webapp/
        ├── spec.md
        ├── plan.md
        ├── research.md
        ├── data-model.md
        ├── quickstart.md (this file)
        └── contracts/
```

---

## Step 1: Database Setup (Neon PostgreSQL)

### 1.1 Create Neon Project

1. Go to [neon.tech](https://neon.tech) and sign in
2. Click "New Project"
3. Name: `todo-app`
4. Region: Choose closest to you
5. Click "Create Project"

### 1.2 Get Connection String

1. From project dashboard, copy the connection string
2. Format: `postgresql://user:password@host/database?sslmode=require`
3. Save this for later configuration

### 1.3 Connection String Variants

You'll need two variants:

```bash
# For Backend (async driver)
DATABASE_URL=postgresql+asyncpg://user:password@host/database?sslmode=require

# For Frontend (Better Auth)
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
```

---

## Step 2: Backend Setup (FastAPI)

### 2.1 Create Virtual Environment

```bash
cd phase-II/backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2.2 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2.3 Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your values
```

**.env contents:**

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@host/database?sslmode=require

# Better Auth (must match frontend)
BETTER_AUTH_SECRET=your-secret-key-at-least-32-characters-long

# CORS
CORS_ORIGINS=http://localhost:3000

# Optional
DEBUG=true
```

### 2.4 Run Database Migrations

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

### 2.5 Start Backend Server

```bash
uvicorn app.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`

API docs at `http://localhost:8000/docs`

---

## Step 3: Frontend Setup (Next.js)

### 3.1 Install Dependencies

```bash
cd phase-II/frontend
npm install
```

### 3.2 Configure Environment

```bash
# Copy example env file
cp .env.local.example .env.local

# Edit .env.local with your values
```

**.env.local contents:**

```bash
# Better Auth
BETTER_AUTH_SECRET=your-secret-key-at-least-32-characters-long
BETTER_AUTH_URL=http://localhost:3000

# Database (for Better Auth)
DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3.3 Start Frontend Server

```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

---

## Step 4: Verify Setup

### 4.1 Health Check

```bash
# Backend health
curl http://localhost:8000/health

# Expected: {"status":"healthy","timestamp":"..."}
```

### 4.2 Frontend Access

1. Open browser to `http://localhost:3000`
2. Should see landing page or sign-in form

### 4.3 API Documentation

1. Open `http://localhost:8000/docs`
2. Should see Swagger UI with all endpoints

---

## Development Workflow

### Running Both Servers

Open two terminal windows:

**Terminal 1 - Backend:**
```bash
cd phase-II/backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd phase-II/frontend
npm run dev
```

### Making Database Changes

1. Modify SQLModel definitions in `backend/app/models/`
2. Generate migration: `alembic revision --autogenerate -m "Description"`
3. Review migration in `backend/alembic/versions/`
4. Apply: `alembic upgrade head`

### Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests (if configured)
cd frontend
npm test
```

---

## Common Issues

### Issue: Database Connection Failed

**Symptom:** `ConnectionRefusedError` or `Connection timed out`

**Solution:**
1. Verify DATABASE_URL is correct
2. Check Neon project is active (not suspended)
3. Ensure `?sslmode=require` is present

### Issue: CORS Errors

**Symptom:** Browser console shows CORS policy error

**Solution:**
1. Verify `CORS_ORIGINS` in backend `.env` includes `http://localhost:3000`
2. Restart backend server after changing

### Issue: JWT Validation Failed

**Symptom:** 401 errors on protected routes

**Solution:**
1. Verify `BETTER_AUTH_SECRET` matches in both frontend and backend
2. Check token hasn't expired
3. Ensure `Authorization: Bearer <token>` header format

### Issue: Better Auth Session Not Persisting

**Symptom:** User logged out on page refresh

**Solution:**
1. Verify DATABASE_URL is configured for Better Auth
2. Check browser cookies are enabled
3. Ensure `httpOnly` cookie settings are correct

---

## Environment Variable Reference

### Backend (.env)

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | Neon PostgreSQL connection (with `+asyncpg`) |
| `BETTER_AUTH_SECRET` | Yes | JWT signing secret (min 32 chars) |
| `CORS_ORIGINS` | Yes | Allowed frontend origins |
| `DEBUG` | No | Enable debug mode |

### Frontend (.env.local)

| Variable | Required | Description |
|----------|----------|-------------|
| `BETTER_AUTH_SECRET` | Yes | JWT signing secret (must match backend) |
| `BETTER_AUTH_URL` | Yes | Better Auth base URL |
| `DATABASE_URL` | Yes | Neon PostgreSQL connection |
| `NEXT_PUBLIC_API_URL` | Yes | Backend API URL |

---

## Next Steps

After setup is complete:

1. Create a user account via sign-up
2. Create your first task
3. Test all CRUD operations
4. Verify user isolation (tasks only visible to owner)

For implementation details, refer to:
- `spec.md` - Feature requirements
- `plan.md` - Implementation plan
- `data-model.md` - Database schema
- `contracts/openapi.yaml` - API specification
