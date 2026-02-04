---
id: 001
title: Initial Constitution Ratification
stage: constitution
date: 2026-01-13
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["constitution", "governance", "security", "architecture"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - null
---

## Prompt

/sp.constitution

Project: Phase II – Todo Full-Stack Web Application (Next.js + FastAPI + SQLModel + Neon + Better Auth + JWT)

Core principles:
- Spec-driven development only (no implementation before approved specs)
- Agentic workflow compliance: Write spec → Generate plan → Break into tasks → Implement via Claude Code
- Zero manual coding – all code must be generated through Claude Code
- Security by design – authentication, authorization, and user isolation are mandatory
- Single source of truth – specs override all implementation
- Clean separation of concerns between frontend, backend, auth, and database layers
- Reproducibility – project must be regenerable using specs + prompts only

Key standards:
- All features must map directly to written specs
- All APIs must be RESTful and clearly documented
- JWT authentication must be enforced on every protected route
- User data isolation is mandatory in every database query
- Database schema must be normalized and migration-safe
- Frontend must be responsive and accessible
- Environment variables must be used for all secrets
- Code structure must follow framework best practices (Next.js App Router, FastAPI, SQLModel)

Security standards:
- Authentication: Better Auth with JWT plugin enabled
- Authorization: JWT verification in FastAPI middleware
- Token handling:
  - JWT passed only via Authorization: Bearer <token> header
  - Tokens must have expiry
- User isolation:
  - Every query filtered by authenticated user ID
  - No cross-user data access allowed
- Failure handling:
  - Missing or invalid token → 401 Unauthorized
  - Forbidden access → 403 Forbidden

Technology constraints:
- Frontend: Next.js 16+ (App Router only)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth
- Workflow: Spec-Kit Plus + Claude Code + Agentic Dev Stack
- No alternative frameworks or libraries unless explicitly defined in specs

Architecture constraints:
- Clear separation of frontend and backend folders
- API routes must follow /api/{user_id}/tasks pattern
- JWT verification via FastAPI middleware
- Frontend API client must automatically attach JWT
- No business logic in UI components
- No direct database access from frontend

Process constraints:
- No code before spec approval
- No implementation without generated plan
- No manual code edits
- Each phase must be independently reviewable
- All iterations must be documented
- Each spec must be completed before moving to the next

Success criteria:
- All 5 basic Todo features implemented as a web application
- Multi-user authentication works correctly
- JWT-based security fully enforced
- Each user only sees and modifies their own tasks
- Frontend is responsive and functional
- Backend APIs are stable and secure
- Database persists data correctly
- Entire project is regenerable using specs + prompts only
- Agentic workflow is clearly visible and reviewable

Quality bar:
- No broken flows
- No security holes
- No hardcoded secrets
- No missing specs
- No manual

## Response snapshot

Created constitution v1.0.0 for Phase II Todo Full-Stack Web Application with 6 core principles:
1. Spec-Driven Development - All implementation must follow approved specs
2. Zero Manual Coding - All code generated through Claude Code
3. Security by Design - Authentication, authorization, user isolation mandatory
4. Single Source of Truth - Specs override all implementation
5. Clean Separation of Concerns - Frontend/Backend/Auth/Database layers separated
6. Reproducibility - Project regenerable from specs + prompts

Additional sections include Security Standards (JWT handling, failure responses), Technology & Architecture Constraints (full stack definition), Process & Quality Standards (development workflow, quality checklist), and Governance (amendment process, versioning policy).

All dependent templates verified compatible. Constitution ratified at version 1.0.0.

## Outcome

- Impact: Initial project constitution established defining all development rules
- Tests: N/A (governance document)
- Files: 1 created (.specify/memory/constitution.md)
- Next prompts: /sp.specify to create first feature specification
- Reflection: Constitution captures all user-provided principles and standards comprehensively

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Template validation PASS, placeholder check PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
