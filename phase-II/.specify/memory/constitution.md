<!--
================================================================================
SYNC IMPACT REPORT
================================================================================
Version change: 0.0.0 → 1.0.0 (MAJOR - Initial constitution ratification)

Modified principles: N/A (initial creation)

Added sections:
- Core Principles (6 principles)
- Security Standards
- Technology & Architecture Constraints
- Process & Quality Standards
- Governance

Removed sections: N/A (initial creation)

Templates requiring updates:
- ✅ .specify/templates/plan-template.md - Compatible (Constitution Check section exists)
- ✅ .specify/templates/spec-template.md - Compatible (requirements structure aligns)
- ✅ .specify/templates/tasks-template.md - Compatible (web app structure option exists)
- ✅ .specify/templates/phr-template.prompt.md - Compatible (no changes needed)

Follow-up TODOs: None
================================================================================
-->

# Phase II Todo Full-Stack Web Application Constitution

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

- Every protected route MUST validate JWT tokens
- Every database query MUST filter by authenticated user ID
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

Frontend, backend, authentication, and database layers MUST be clearly separated:

- **Frontend**: Next.js 16+ (App Router) - UI and user interaction only
- **Backend**: Python FastAPI - Business logic and API endpoints
- **Authentication**: Better Auth with JWT - Security layer
- **Database**: Neon PostgreSQL with SQLModel - Data persistence

No business logic in UI components. No direct database access from frontend. Each layer has defined responsibilities.

**Rationale**: Enables independent development, testing, and scaling of each layer.

### VI. Reproducibility

The entire project MUST be regenerable using specifications and prompts alone. This requires:

- All features map directly to written specs
- All architectural decisions are documented
- All prompts are recorded in PHR files
- No undocumented manual interventions

**Rationale**: Ensures the project can be rebuilt or audited at any point in its lifecycle.

## Security Standards

### Authentication & Authorization

| Aspect | Requirement |
|--------|-------------|
| Provider | Better Auth with JWT plugin |
| Token Transport | Authorization: Bearer `<token>` header only |
| Token Expiry | MUST have expiration time set |
| Validation | FastAPI middleware validates every protected request |
| User Isolation | Every query filtered by authenticated user_id |

### Failure Handling

| Condition | Response |
|-----------|----------|
| Missing token | 401 Unauthorized |
| Invalid/expired token | 401 Unauthorized |
| Valid token, forbidden resource | 403 Forbidden |

### Prohibited Practices

- Storing JWT in localStorage (use httpOnly cookies or memory)
- Hardcoding secrets or tokens in code
- Cross-user data access
- Disabling security for convenience

## Technology & Architecture Constraints

### Technology Stack (Non-Negotiable)

| Layer | Technology | Version |
|-------|------------|---------|
| Frontend | Next.js (App Router) | 16+ |
| Backend | Python FastAPI | Latest stable |
| ORM | SQLModel | Latest stable |
| Database | Neon Serverless PostgreSQL | - |
| Authentication | Better Auth | Latest stable |
| Workflow | Spec-Kit Plus + Claude Code | - |

Alternative frameworks or libraries are prohibited unless explicitly defined in specifications.

### Architecture Requirements

- Clear separation of `frontend/` and `backend/` directories
- API routes follow `/api/{resource}` RESTful pattern
- JWT verification implemented as FastAPI middleware
- Frontend API client automatically attaches JWT to requests
- All APIs are RESTful and documented via OpenAPI
- Database schema is normalized and migration-safe

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
- [ ] Frontend is responsive and accessible
- [ ] Database persists data correctly
- [ ] User data isolation verified

### Success Criteria

- All 5 basic Todo features implemented as web application
- Multi-user authentication functioning correctly
- JWT-based security fully enforced
- Each user sees and modifies only their own tasks
- Project regenerable using specs + prompts only
- Agentic workflow visible and reviewable

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

**Version**: 1.0.0 | **Ratified**: 2026-01-13 | **Last Amended**: 2026-01-13
