# Fehem Educational Platform - Full Implementation Plan

## TL;DR

> **Quick Summary**: Build a complete AI-powered educational platform with Google OAuth, multi-step onboarding, PDF processing with RAG, AI chat/presentations/quizzes, points system, real-time group collaboration, and full admin panel.
> 
> **Deliverables**:
> - Google OAuth authentication (no email/password)
> - Role-based onboarding flow (Student/Worker/Professor)
> - PDF upload with chunking and vector embeddings
> - AI Chat grounded in course content (RAG)
> - AI Presentation generation from PDFs
> - AI Quiz generation (QCM) with corrections
> - Points/credits system with daily limits
> - Invite rewards and promo codes
> - Groups with shared PDFs and real-time WebSocket chat
> - Professor features and full admin panel
> 
> **Estimated Effort**: XL (40-50+ tasks)
> **Parallel Execution**: YES - 6 waves
> **Critical Path**: Auth → Onboarding → Documents → Points → AI Features → Groups → Admin

---

## Context

### Original Request
Build "Fehem" - an AI-powered learning platform where students, workers, and professors can:
- Sign up via Google OAuth only
- Complete role-specific onboarding
- Upload course PDFs
- Get AI-generated presentations, quizzes, and chat
- Earn and spend points for AI features
- Collaborate in groups with real-time chat
- Share quizzes and resources

### Interview Summary
**Key Discussions**:
- **Scope**: Full implementation in ONE plan (no phasing)
- **Video**: EXCLUDED - too expensive, deferred to future
- **Chat**: WebSockets for real-time group communication
- **Testing**: TDD approach (tests first)
- **Points**: Generous model (50 start, 3 daily free, 20 per invite)
- **Admin**: Full panel with promo codes, user management, analytics

**Research Findings**:
- NextAuth.js v5 recommended for Google OAuth
- Existing NVIDIA AI bridge can be extended for chat/embeddings
- Pessimistic locking + idempotency keys for points mutations
- Existing docs define clear domain boundaries

### Gap Analysis (Self-Review)
**Guardrails Applied**:
- No video generation (explicitly excluded)
- No payment integration (points-only for now)
- No email notifications (can add later)
- No mobile app
- Must follow existing architecture in docs/AI_ARCHITECTURE.md

**Assumptions Made** (validated by existing docs):
- PostgreSQL + pgvector already set up
- NVIDIA AI endpoints functional
- Bun for frontend, uv for backend (non-negotiable per docs)

---

## Work Objectives

### Core Objective
Transform the existing Fehem scaffolding into a fully functional AI-powered educational platform with authentication, onboarding, document processing, AI features, points system, group collaboration, and administration.

### Concrete Deliverables
- `/auth/*` - Google OAuth login/callback/logout
- `/onboarding/*` - Multi-step role-based onboarding flow
- `/dashboard` - Main user dashboard
- `/documents/*` - PDF upload and management
- `/chat/*` - AI course chat interface
- `/presentations/*` - AI presentation generator
- `/quizzes/*` - AI quiz generator and player
- `/groups/*` - Group management and real-time chat
- `/admin/*` - Admin panel for promo codes, users, teachers
- `/api/v1/*` - All backend endpoints with auth guards

### Definition of Done
- [ ] `bun run build` passes with 0 errors
- [ ] `bun run typecheck` passes
- [ ] `uv run pytest` all tests pass
- [ ] All QA scenarios verified with evidence
- [ ] Onboarding blocks unauthenticated/incomplete users from AI features
- [ ] Points deducted atomically before AI generation

### Must Have
- Google OAuth as ONLY auth method
- Onboarding completion required before AI features
- Points check before every generation
- Atomic point mutations with idempotency
- RAG-grounded AI responses with citations
- Real-time WebSocket group chat
- TDD for all critical paths

### Must NOT Have (Guardrails)
- ❌ Email/password authentication
- ❌ Video generation feature
- ❌ Payment/billing integration
- ❌ Email notifications
- ❌ Mobile app
- ❌ AI slop: No over-commenting, no placeholder code, no "TODO: implement later"
- ❌ Partial implementations - every feature must be 100% complete

---

## Verification Strategy

> **ZERO HUMAN INTERVENTION** - ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: NO (needs setup)
- **Automated tests**: TDD - write tests first
- **Framework**: 
  - Frontend: bun test (vitest-compatible)
  - Backend: pytest
- **TDD Flow**: RED (failing test) → GREEN (minimal impl) → REFACTOR

### QA Policy
Every task MUST include agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **Frontend/UI**: Use Playwright - Navigate, interact, assert DOM, screenshot
- **API/Backend**: Use Bash (curl) - Send requests, assert status + response
- **WebSocket**: Use interactive_bash - Connect, send messages, verify events
- **Database**: Use Bash (psql/queries) - Verify data state

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Foundation - Infrastructure + Types):
├── Task 1: Test infrastructure setup (frontend + backend) [quick]
├── Task 2: Database schema + migrations (users, profiles, points) [quick]
├── Task 3: Shared TypeScript types + API contracts [quick]
├── Task 4: Shared Python schemas + error contracts [quick]
├── Task 5: Design system tokens + base components [visual-engineering]
└── Task 6: WebSocket infrastructure setup [quick]

Wave 2 (Auth + Onboarding Core):
├── Task 7: Google OAuth backend (FastAPI + NextAuth bridge) [deep]
├── Task 8: Google OAuth frontend (NextAuth.js v5) [deep]
├── Task 9: Auth middleware + session management [deep]
├── Task 10: Onboarding API endpoints [unspecified-high]
├── Task 11: Onboarding UI - Step 1: Role selection [visual-engineering]
├── Task 12: Onboarding UI - Step 2: Role-specific info [visual-engineering]
├── Task 13: Onboarding UI - Step 3: Common info + intent [visual-engineering]
└── Task 14: Onboarding gate middleware [deep]

Wave 3 (Documents + Points System):
├── Task 15: PDF upload API + storage [unspecified-high]
├── Task 16: PDF parsing + chunking worker [deep]
├── Task 17: Embeddings generation + pgvector upsert [deep]
├── Task 18: Document management UI [visual-engineering]
├── Task 19: Points wallet + ledger tables [quick]
├── Task 20: Points service (reserve/commit/refund) [deep]
├── Task 21: Daily quota enforcement [deep]
├── Task 22: Points UI component [visual-engineering]
└── Task 23: Invite link system [unspecified-high]

Wave 4 (AI Features):
├── Task 24: RAG retriever service [deep]
├── Task 25: AI Chat API with citations [deep]
├── Task 26: AI Chat UI [visual-engineering]
├── Task 27: Presentation generation API [deep]
├── Task 28: Presentation generation UI [visual-engineering]
├── Task 29: Quiz generation API [deep]
├── Task 30: Quiz generation UI [visual-engineering]
├── Task 31: Quiz player + correction UI [visual-engineering]
└── Task 32: Promo code system [unspecified-high]

Wave 5 (Groups + Real-time):
├── Task 33: Groups CRUD API [unspecified-high]
├── Task 34: Group membership + invites [unspecified-high]
├── Task 35: Group PDF sharing [deep]
├── Task 36: WebSocket chat server [deep]
├── Task 37: Real-time chat UI [visual-engineering]
├── Task 38: AI in group chat [deep]
├── Task 39: Group points modes (payer/pooled) [deep]
├── Task 40: Quiz sharing in groups [unspecified-high]
└── Task 41: Professor contact admin feature [quick]

Wave 6 (Admin Panel):
├── Task 42: Admin auth + role guard [deep]
├── Task 43: Promo code management UI [visual-engineering]
├── Task 44: User management UI [visual-engineering]
├── Task 45: Teacher bonus request workflow [unspecified-high]
├── Task 46: Points adjustment UI [visual-engineering]
├── Task 47: Analytics dashboard [visual-engineering]
└── Task 48: Audit log viewer [visual-engineering]

Wave FINAL (Verification - 4 parallel reviews):
├── Task F1: Plan compliance audit [oracle]
├── Task F2: Code quality review [unspecified-high]
├── Task F3: Real manual QA [unspecified-high]
└── Task F4: Scope fidelity check [deep]
-> Present results -> Get explicit user okay

Critical Path: T1-T4 → T7-T9 → T14 → T15-T17 → T19-T21 → T24-T26 → T33-T38 → T42 → F1-F4
Parallel Speedup: ~75% faster than sequential
Max Concurrent: 8 (Wave 3)
```

### Dependency Matrix

| Task | Depends On | Blocks | Wave |
|------|-----------|--------|------|
| 1-6 | - | 7-48 | 1 |
| 7 | 2,4 | 8,9,10 | 2 |
| 8 | 3,7 | 9,11-14 | 2 |
| 9 | 7,8 | 14,15-32 | 2 |
| 10 | 2,4,7 | 11-13 | 2 |
| 11-13 | 5,10 | 14 | 2 |
| 14 | 9,10 | 15-48 | 2 |
| 15-18 | 9,14 | 24-31 | 3 |
| 19-23 | 2,9 | 24-41 | 3 |
| 24-32 | 17,20,21 | 38,40 | 4 |
| 33-41 | 9,20,24 | 42-48 | 5 |
| 42-48 | 9,33 | F1-F4 | 6 |
| F1-F4 | 1-48 | Completion | FINAL |

### Agent Dispatch Summary

| Wave | Tasks | Categories |
|------|-------|------------|
| 1 | 6 | quick (4), visual-engineering (1), quick (1) |
| 2 | 8 | deep (4), unspecified-high (1), visual-engineering (3) |
| 3 | 9 | unspecified-high (2), deep (3), visual-engineering (2), quick (1), unspecified-high (1) |
| 4 | 9 | deep (4), visual-engineering (4), unspecified-high (1) |
| 5 | 9 | unspecified-high (3), deep (4), visual-engineering (1), quick (1) |
| 6 | 7 | deep (1), visual-engineering (5), unspecified-high (1) |
| FINAL | 4 | oracle (1), unspecified-high (2), deep (1) |

---

## TODOs

### Wave 1: Foundation (Infrastructure + Types)

- [ ] 1. Test Infrastructure Setup

  **What to do**:
  - Set up bun test (vitest) in frontend with proper config
  - Set up pytest in backend with fixtures for DB, auth mocking
  - Create test utilities: mock factories, test helpers
  - Verify test commands work: `bun test`, `uv run pytest`

  **Must NOT do**:
  - Skip test setup - TDD is mandatory
  - Use Jest (use bun test/vitest)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`
  - Reason: Standard test setup, well-documented patterns

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 2-6)
  - **Blocks**: Tasks 7-48 (all need test infra)
  - **Blocked By**: None

  **References**:
  - `frontend/package.json` - Add test scripts
  - `backend/pyproject.toml` - pytest already configured
  - `docs/AI_ARCHITECTURE.md:272-286` - Testing strategy

  **QA Scenarios**:
  ```
  Scenario: Frontend test runner works
    Tool: Bash
    Steps:
      1. cd frontend && bun test --run
      2. Assert exit code 0
    Expected: "No test files found" or tests pass
    Evidence: .sisyphus/evidence/task-1-frontend-test.txt

  Scenario: Backend test runner works
    Tool: Bash
    Steps:
      1. cd backend && uv run pytest --collect-only
      2. Assert exit code 0
    Expected: pytest collects tests successfully
    Evidence: .sisyphus/evidence/task-1-backend-test.txt
  ```

  **Commit**: YES (Wave 1 group)

---

- [ ] 2. Database Schema + Migrations

  **What to do**:
  - Create migration for users table (google_subject, email, name, role, created_at)
  - Create user_profiles table (user_id, institution, work_domain, subject, country, phone, usage_intent, onboarding_completed)
  - Create points_wallets table (user_id, balance, reserved, updated_at)
  - Create points_transactions table (id, wallet_id, type, amount, idempotency_key, created_at)
  - Create documents table (id, owner_id, group_id, filename, status, created_at)
  - Create document_chunks table (id, document_id, content, embedding vector(1024), page, metadata)
  - Create groups table (id, name, owner_id, point_mode, created_at)
  - Create group_members table (group_id, user_id, role, joined_at)
  - Create quizzes table (id, document_id, owner_id, questions jsonb, created_at)
  - Create promo_codes table (id, code, points, max_uses, uses, active, created_at)
  - Create invite_links table (id, user_id, code, redemptions, created_at)
  - Add indexes per docs/AI_ARCHITECTURE.md

  **Must NOT do**:
  - Skip any table - all are needed
  - Use raw SQL without migration tool

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`
  - Reason: Schema creation is well-defined

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 7, 10, 15, 19, 23, 29, 32, 33
  - **Blocked By**: None

  **References**:
  - `docs/AI_ARCHITECTURE.md:211-240` - Database design
  - `backend/src/app/db.py` - Existing DB connection
  - `docs/PRODUCT_RULES.md` - Domain requirements

  **QA Scenarios**:
  ```
  Scenario: All tables created
    Tool: Bash (curl to /api/db-check or direct psql)
    Steps:
      1. Run migrations
      2. Query information_schema.tables
      3. Assert all 11 tables exist
    Expected: users, user_profiles, points_wallets, points_transactions, documents, document_chunks, groups, group_members, quizzes, promo_codes, invite_links
    Evidence: .sisyphus/evidence/task-2-tables.txt

  Scenario: Indexes exist
    Tool: Bash
    Steps:
      1. Query pg_indexes for expected indexes
    Expected: Indexes on google_subject, idempotency_key, document_id
    Evidence: .sisyphus/evidence/task-2-indexes.txt
  ```

  **Commit**: YES (Wave 1 group)

---

- [ ] 3. Shared TypeScript Types + API Contracts

  **What to do**:
  - Create `frontend/types/user.ts` - User, UserProfile, UserRole
  - Create `frontend/types/points.ts` - Wallet, Transaction, PointCosts
  - Create `frontend/types/documents.ts` - Document, DocumentChunk, UploadStatus
  - Create `frontend/types/groups.ts` - Group, GroupMember, PointMode
  - Create `frontend/types/quiz.ts` - Quiz, Question, QuizAttempt
  - Create `frontend/types/api.ts` - ApiError, ApiResponse wrapper
  - Create `frontend/lib/api-client.ts` - Typed fetch wrapper with error handling

  **Must NOT do**:
  - Use `any` types
  - Skip error types

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`
  - Reason: Pure type definitions

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 8, 11-13, 18, 22, 26, 28, 30-31, 37, 43-48
  - **Blocked By**: None

  **References**:
  - `docs/PRODUCT_RULES.md` - Domain models
  - `docs/AI_ARCHITECTURE.md:164-177` - Response shapes

  **QA Scenarios**:
  ```
  Scenario: Types compile without errors
    Tool: Bash
    Steps:
      1. cd frontend && bun run typecheck
    Expected: Exit code 0, no errors
    Evidence: .sisyphus/evidence/task-3-typecheck.txt
  ```

  **Commit**: YES (Wave 1 group)

---

- [ ] 4. Shared Python Schemas + Error Contracts

  **What to do**:
  - Create `backend/src/app/modules/` directory structure per AI_ARCHITECTURE.md
  - Create `backend/src/app/contracts/api_errors.py` - ErrorResponse, error codes (ONBOARDING_REQUIRED, INSUFFICIENT_POINTS, etc.)
  - Create `backend/src/app/modules/auth/schemas.py` - UserCreate, UserResponse, TokenPayload
  - Create `backend/src/app/modules/onboarding/schemas.py` - OnboardingRequest, OnboardingResponse
  - Create `backend/src/app/modules/points_billing/schemas.py` - WalletResponse, TransactionCreate
  - Create `backend/src/app/modules/documents/schemas.py` - DocumentCreate, DocumentResponse, ChunkResponse
  - Create `backend/src/app/modules/groups/schemas.py` - GroupCreate, GroupResponse, MemberResponse
  - Create `backend/src/app/modules/quiz/schemas.py` - QuizCreate, QuizResponse, QuestionSchema

  **Must NOT do**:
  - Skip Pydantic validation
  - Use dict instead of typed models

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`
  - Reason: Schema definitions are straightforward

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 7, 10, 15, 19, 20, 24, 25, 27, 29, 33-35, 42
  - **Blocked By**: None

  **References**:
  - `docs/AI_ARCHITECTURE.md:32-110` - Package layout
  - `docs/AI_ARCHITECTURE.md:134-143` - Error contract example
  - `backend/src/app/ai_schemas.py` - Existing schema pattern

  **QA Scenarios**:
  ```
  Scenario: Schemas validate correctly
    Tool: Bash
    Steps:
      1. cd backend && uv run python -c "from app.contracts.api_errors import ErrorResponse; print('OK')"
    Expected: "OK" printed, no import errors
    Evidence: .sisyphus/evidence/task-4-schemas.txt
  ```

  **Commit**: YES (Wave 1 group)

---

- [ ] 5. Design System Tokens + Base Components

  **What to do**:
  - Extend existing shadcn/ui setup with Fehem color tokens
  - Create `frontend/components/ui/card.tsx` - Card component
  - Create `frontend/components/ui/input.tsx` - Input with validation states
  - Create `frontend/components/ui/select.tsx` - Select/dropdown
  - Create `frontend/components/ui/dialog.tsx` - Modal dialog
  - Create `frontend/components/ui/toast.tsx` - Toast notifications
  - Create `frontend/components/ui/avatar.tsx` - User avatar
  - Create `frontend/components/ui/badge.tsx` - Status badges
  - Create `frontend/components/layout/sidebar.tsx` - App sidebar
  - Create `frontend/components/layout/header.tsx` - App header

  **Must NOT do**:
  - Deviate from shadcn/ui patterns
  - Add custom CSS without Tailwind

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `["frontend-ui-ux"]`
  - Reason: UI component creation

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 11-13, 18, 22, 26, 28, 30-31, 37, 43-48
  - **Blocked By**: None

  **References**:
  - `frontend/components/ui/button.tsx` - Existing pattern
  - `frontend/components.json` - shadcn config

  **QA Scenarios**:
  ```
  Scenario: Components render without errors
    Tool: Bash
    Steps:
      1. cd frontend && bun run build
    Expected: Build succeeds
    Evidence: .sisyphus/evidence/task-5-build.txt
  ```

  **Commit**: YES (Wave 1 group)

---

- [ ] 6. WebSocket Infrastructure Setup

  **What to do**:
  - Add `python-socketio` to backend dependencies
  - Create `backend/src/app/websocket/manager.py` - Connection manager
  - Create `backend/src/app/websocket/events.py` - Event types (message, typing, join, leave)
  - Mount Socket.IO to FastAPI app
  - Add `socket.io-client` to frontend
  - Create `frontend/lib/socket.ts` - Socket connection manager
  - Create `frontend/hooks/useSocket.ts` - React hook for socket

  **Must NOT do**:
  - Use polling fallback as primary
  - Skip reconnection logic

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`
  - Reason: Standard WebSocket setup

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 36-38
  - **Blocked By**: None

  **References**:
  - `backend/src/app/main.py` - Mount point
  - Socket.IO docs for FastAPI integration

  **QA Scenarios**:
  ```
  Scenario: WebSocket server starts
    Tool: Bash
    Steps:
      1. Start backend server
      2. Check /socket.io/ endpoint responds
    Expected: Socket.IO handshake available
    Evidence: .sisyphus/evidence/task-6-websocket.txt
  ```

  **Commit**: YES (Wave 1 group)

---

### Wave 2: Auth + Onboarding Core

- [ ] 7. Google OAuth Backend (FastAPI)

  **What to do**:
  - Create `backend/src/app/modules/auth/service.py` - OAuth flow, token validation
  - Create `backend/src/app/modules/auth/google_provider.py` - Google OAuth client
  - Create `backend/src/app/api/v1/auth.py` - Routes: /login, /callback, /logout, /me
  - Create `backend/src/app/api/deps/auth.py` - get_current_user dependency
  - Store Google subject + email in users table
  - Create JWT session tokens with configurable expiry
  - Write tests for auth flow

  **Must NOT do**:
  - Implement email/password auth
  - Store Google tokens in DB (use sessions)

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: `[]`
  - Reason: Security-critical, needs careful implementation

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Wave 1)
  - **Parallel Group**: Wave 2 (with Tasks 8-14)
  - **Blocks**: Tasks 8, 9, 10, 14
  - **Blocked By**: Tasks 2, 4

  **References**:
  - `docs/PRODUCT_RULES.md:8-11` - Auth rules
  - `docs/AI_ARCHITECTURE.md:113-114` - Auth domain
  - `backend/src/app/config.py` - Settings pattern

  **QA Scenarios**:
  ```
  Scenario: Login redirects to Google
    Tool: Bash (curl)
    Steps:
      1. curl -I http://localhost:8000/api/v1/auth/login
    Expected: 302 redirect to accounts.google.com
    Evidence: .sisyphus/evidence/task-7-login-redirect.txt

  Scenario: Invalid token rejected
    Tool: Bash (curl)
    Steps:
      1. curl -H "Authorization: Bearer invalid" http://localhost:8000/api/v1/auth/me
    Expected: 401 Unauthorized
    Evidence: .sisyphus/evidence/task-7-invalid-token.txt
  ```

  **Commit**: YES (Wave 2 group)

---

- [ ] 8. Google OAuth Frontend (NextAuth.js v5)

  **What to do**:
  - Install and configure NextAuth.js v5
  - Create `frontend/auth.ts` - NextAuth config with Google provider
  - Create `frontend/app/api/auth/[...nextauth]/route.ts` - Auth API route
  - Create `frontend/middleware.ts` - Protect routes requiring auth
  - Create `frontend/components/auth/login-button.tsx` - Google sign-in button
  - Create `frontend/components/auth/user-menu.tsx` - User dropdown with logout
  - Create `frontend/lib/auth-client.ts` - useSession, signIn, signOut hooks
  - Write tests for auth components

  **Must NOT do**:
  - Add other providers (Google only)
  - Skip middleware protection

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: `[]`
  - Reason: Auth is security-critical

  **Parallelization**:
  - **Can Run In Parallel**: NO (needs Task 7)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 9, 11-14
  - **Blocked By**: Tasks 3, 7

  **References**:
  - NextAuth.js v5 documentation
  - `frontend/package.json` - Add next-auth dependency

  **QA Scenarios**:
  ```
  Scenario: Login button renders
    Tool: Playwright
    Steps:
      1. Navigate to /login
      2. Assert button with text "Sign in with Google" exists
    Expected: Button visible and clickable
    Evidence: .sisyphus/evidence/task-8-login-button.png

  Scenario: Protected route redirects
    Tool: Playwright
    Steps:
      1. Navigate to /dashboard (unauthenticated)
    Expected: Redirect to /login
    Evidence: .sisyphus/evidence/task-8-protected-redirect.png
  ```

  **Commit**: YES (Wave 2 group)

---

- [ ] 9. Auth Middleware + Session Management

  **What to do**:
  - Create `backend/src/app/api/deps/session.py` - Session validation
  - Create `backend/src/app/core/security.py` - JWT encode/decode, password hashing (for future)
  - Implement session refresh logic
  - Add session to request state for downstream handlers
  - Create `frontend/providers/auth-provider.tsx` - Auth context
  - Sync frontend/backend session state
  - Write integration tests

  **Must NOT do**:
  - Store sensitive data in localStorage
  - Skip CSRF protection

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: `[]`
  - Reason: Security-critical session handling

  **Parallelization**:
  - **Can Run In Parallel**: NO (needs Tasks 7, 8)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 14, 15-48
  - **Blocked By**: Tasks 7, 8

  **References**:
  - `docs/AI_ARCHITECTURE.md:255-259` - Security rules

  **QA Scenarios**:
  ```
  Scenario: Session persists across requests
    Tool: Bash (curl with cookies)
    Steps:
      1. Login and capture session cookie
      2. Call /api/v1/auth/me with cookie
    Expected: Returns current user data
    Evidence: .sisyphus/evidence/task-9-session.txt
  ```

  **Commit**: YES (Wave 2 group)

---

- [ ] 10. Onboarding API Endpoints

  **What to do**:
  - Create `backend/src/app/modules/onboarding/service.py` - Onboarding logic
  - Create `backend/src/app/api/v1/onboarding.py` - Routes: GET /status, POST /submit, PUT /update
  - Validate role-specific required fields per PRODUCT_RULES.md
  - Store responses in user_profiles table
  - Mark onboarding_completed when all fields valid
  - Create initial points wallet (50 points) on completion
  - Write tests for all validation scenarios

  **Must NOT do**:
  - Allow partial onboarding to access AI features
  - Skip phone number validation

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: `[]`
  - Reason: Business logic with validation

  **Parallelization**:
  - **Can Run In Parallel**: YES (parallel with 8, 9)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 11-14
  - **Blocked By**: Tasks 2, 4, 7

  **References**:
  - `docs/PRODUCT_RULES.md:13-34` - Onboarding rules
  - `docs/AI_ARCHITECTURE.md:126-143` - Onboarding gate

  **QA Scenarios**:
  ```
  Scenario: Student onboarding validates institution
    Tool: Bash (curl)
    Steps:
      1. POST /api/v1/onboarding/submit with role=student, missing institution
    Expected: 400 with validation error for institution
    Evidence: .sisyphus/evidence/task-10-student-validation.txt

  Scenario: Complete onboarding grants 50 points
    Tool: Bash (curl)
    Steps:
      1. Complete onboarding with all fields
      2. GET /api/v1/points/wallet
    Expected: balance = 50
    Evidence: .sisyphus/evidence/task-10-initial-points.txt
  ```

  **Commit**: YES (Wave 2 group)

---

- [ ] 11. Onboarding UI - Step 1: Role Selection

  **What to do**:
  - Create `frontend/app/onboarding/page.tsx` - Onboarding container
  - Create `frontend/app/onboarding/layout.tsx` - Onboarding layout (no sidebar)
  - Create `frontend/components/onboarding/role-selection.tsx` - Role cards (Student, Worker, Professor)
  - Add visual icons for each role
  - Store selection in onboarding state
  - Write component tests

  **Must NOT do**:
  - Allow skipping role selection
  - Use plain text without visual hierarchy

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `["frontend-ui-ux"]`
  - Reason: UI/UX focused component

  **Parallelization**:
  - **Can Run In Parallel**: YES (parallel with 12, 13)
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 14
  - **Blocked By**: Tasks 5, 10

  **References**:
  - `docs/PRODUCT_RULES.md:3-7` - User types
  - `frontend/components/ui/` - Base components

  **QA Scenarios**:
  ```
  Scenario: Role cards display correctly
    Tool: Playwright
    Steps:
      1. Navigate to /onboarding
      2. Assert 3 role cards visible (Student, Worker, Professor)
      3. Click Student card
      4. Assert selection state changes
    Expected: Card shows selected state
    Evidence: .sisyphus/evidence/task-11-role-selection.png
  ```

  **Commit**: YES (Wave 2 group)

---

- [ ] 12. Onboarding UI - Step 2: Role-Specific Info

  **What to do**:
  - Create `frontend/components/onboarding/student-form.tsx` - Institution type (lycée/fac), institution name
  - Create `frontend/components/onboarding/worker-form.tsx` - Work domain/industry
  - Create `frontend/components/onboarding/professor-form.tsx` - Subject, institution type, institution name
  - Conditional rendering based on selected role
  - Validate required fields before proceeding
  - Write component tests

  **Must NOT do**:
  - Show all forms at once
  - Skip validation

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `["frontend-ui-ux"]`
  - Reason: Form UI with conditional logic

  **Parallelization**:
  - **Can Run In Parallel**: YES (parallel with 11, 13)
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 14
  - **Blocked By**: Tasks 5, 10

  **References**:
  - `docs/PRODUCT_RULES.md:26-34` - Role-specific fields

  **QA Scenarios**:
  ```
  Scenario: Student sees institution fields
    Tool: Playwright
    Steps:
      1. Select Student role
      2. Proceed to step 2
      3. Assert institution type dropdown exists
    Expected: Lycée/Fac options visible
    Evidence: .sisyphus/evidence/task-12-student-form.png

  Scenario: Professor sees subject field
    Tool: Playwright
    Steps:
      1. Select Professor role
      2. Proceed to step 2
    Expected: Subject input field visible
    Evidence: .sisyphus/evidence/task-12-professor-form.png
  ```

  **Commit**: YES (Wave 2 group)

---

- [ ] 13. Onboarding UI - Step 3: Common Info + Intent

  **What to do**:
  - Create `frontend/components/onboarding/common-info-form.tsx` - Country, phone number
  - Create `frontend/components/onboarding/usage-intent.tsx` - Intent selection (personal, sell courses, support class)
  - Add country dropdown with common countries
  - Add phone number input with validation
  - Submit all data to API on completion
  - Show success state and redirect to dashboard
  - Write component tests

  **Must NOT do**:
  - Skip phone validation
  - Allow empty intent

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `["frontend-ui-ux"]`
  - Reason: Form completion and submission

  **Parallelization**:
  - **Can Run In Parallel**: YES (parallel with 11, 12)
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 14
  - **Blocked By**: Tasks 5, 10

  **References**:
  - `docs/PRODUCT_RULES.md:17-25` - Common fields

  **QA Scenarios**:
  ```
  Scenario: Complete onboarding flow
    Tool: Playwright
    Steps:
      1. Login with Google
      2. Select role
      3. Fill role-specific fields
      4. Fill country, phone, intent
      5. Submit
    Expected: Redirect to /dashboard
    Evidence: .sisyphus/evidence/task-13-complete-flow.png
  ```

  **Commit**: YES (Wave 2 group)

---

- [ ] 14. Onboarding Gate Middleware

  **What to do**:
  - Create `backend/src/app/api/deps/onboarding_gate.py` - Dependency that checks onboarding status
  - Apply gate to all AI generation endpoints
  - Return ONBOARDING_REQUIRED error with next_action
  - Create `frontend/middleware.ts` update - Redirect incomplete users to /onboarding
  - Create `frontend/hooks/useOnboardingStatus.ts` - Check status on mount
  - Write integration tests for gate enforcement

  **Must NOT do**:
  - Allow ANY AI feature without complete onboarding
  - Return generic errors (must be typed)

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: `[]`
  - Reason: Critical security gate

  **Parallelization**:
  - **Can Run In Parallel**: NO (needs 9, 10-13)
  - **Parallel Group**: Wave 2 (end)
  - **Blocks**: Tasks 15-48
  - **Blocked By**: Tasks 9, 10, 11, 12, 13

  **References**:
  - `docs/AI_ARCHITECTURE.md:126-143` - Gate specification
  - `docs/PRODUCT_RULES.md:14-15` - Gate requirement

  **QA Scenarios**:
  ```
  Scenario: Incomplete user blocked from AI
    Tool: Bash (curl)
    Steps:
      1. Login but skip onboarding
      2. POST /api/v1/ai/chat
    Expected: 403 with code ONBOARDING_REQUIRED
    Evidence: .sisyphus/evidence/task-14-gate-blocks.txt

  Scenario: Complete user accesses AI
    Tool: Bash (curl)
    Steps:
      1. Complete onboarding
      2. POST /api/v1/ai/chat
    Expected: 200 or points-related error (not onboarding)
    Evidence: .sisyphus/evidence/task-14-gate-passes.txt
  ```

  **Commit**: YES (Wave 2 group)

---

### Wave 3: Documents + Points System

- [ ] 15. PDF Upload API + Storage

  **What to do**:
  - Create `backend/src/app/modules/documents/service.py` - Document CRUD
  - Create `backend/src/app/api/v1/documents.py` - Routes: POST /upload, GET /list, GET /{id}, DELETE /{id}
  - Implement file upload with size limits (50MB max)
  - Store PDFs in local filesystem (configurable path) or S3-compatible storage
  - Create document record with status: pending, processing, ready, failed
  - Validate PDF mime type
  - Write tests

  **Must NOT do**:
  - Accept non-PDF files
  - Skip size validation
  - Store in database blob

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: `[]`
  - Reason: File handling with validation

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 16-23)
  - **Blocks**: Tasks 16, 17, 24-31
  - **Blocked By**: Tasks 9, 14

  **References**:
  - `docs/PRODUCT_RULES.md:36-40` - Upload rules
  - `docs/AI_ARCHITECTURE.md:146-156` - PDF pipeline

  **QA Scenarios**:
  ```
  Scenario: Upload PDF succeeds
    Tool: Bash (curl)
    Steps:
      1. curl -F "file=@test.pdf" http://localhost:8000/api/v1/documents/upload
    Expected: 201 with document_id
    Evidence: .sisyphus/evidence/task-15-upload.txt

  Scenario: Non-PDF rejected
    Tool: Bash (curl)
    Steps:
      1. curl -F "file=@test.txt" http://localhost:8000/api/v1/documents/upload
    Expected: 400 with validation error
    Evidence: .sisyphus/evidence/task-15-reject-txt.txt
  ```

  **Commit**: YES (Wave 3 group)

---

- [ ] 16. PDF Parsing + Chunking Worker

  **What to do**:
  - Create `backend/src/app/modules/documents/parser.py` - PDF text extraction (PyMuPDF/pdfplumber)
  - Create `backend/src/app/modules/documents/chunker.py` - Split text into chunks (500-1000 tokens)
  - Create `backend/src/app/workers/jobs/index_document.py` - Async job
  - Add metadata to chunks: page number, owner_id, group_id, upload_id
  - Update document status on completion/failure
  - Handle parsing errors gracefully with actionable messages
  - Write tests

  **Must NOT do**:
  - Skip error handling
  - Create chunks > 1000 tokens
  - Block the API during processing

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: `[]`
  - Reason: Complex text processing

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 15 schema)
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 17
  - **Blocked By**: Task 15

  **References**:
  - `docs/AI_ARCHITECTURE.md:146-156` - Pipeline spec

  **QA Scenarios**:
  ```
  Scenario: PDF parsed into chunks
    Tool: Bash
    Steps:
      1. Upload PDF
      2. Wait for processing
      3. Query document_chunks table
    Expected: Multiple chunks with page metadata
    Evidence: .sisyphus/evidence/task-16-chunks.txt
  ```

  **Commit**: YES (Wave 3 group)

---

- [ ] 17. Embeddings Generation + pgvector Upsert

  **What to do**:
  - Create `backend/src/app/modules/rag/embedder.py` - Generate embeddings via NVIDIA API
  - Extend index_document job to generate embeddings after chunking
  - Upsert chunks with embeddings to document_chunks table
  - Use existing `/api/ai/embeddings` endpoint as provider
  - Handle rate limits with retry logic
  - Write tests

  **Must NOT do**:
  - Skip retry on failure
  - Generate embeddings synchronously in API

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: `[]`
  - Reason: AI integration with error handling

  **Parallelization**:
  - **Can Run In Parallel**: YES (depends on 16)
  - **Parallel Group**: Wave 3
  - **Blocks**: Tasks 24, 25
  - **Blocked By**: Tasks 15, 16

  **References**:
  - `backend/src/app/ai_routes.py` - Existing embeddings endpoint
  - `backend/src/app/semantic_search.py` - Existing pgvector logic
  - `docs/AI_ARCHITECTURE.md:146-156` - Embeddings spec

  **QA Scenarios**:
  ```
  Scenario: Chunks have embeddings
    Tool: Bash
    Steps:
      1. Upload PDF, wait for indexing
      2. Query: SELECT id, embedding IS NOT NULL FROM document_chunks
    Expected: All chunks have embeddings
    Evidence: .sisyphus/evidence/task-17-embeddings.txt
  ```

  **Commit**: YES (Wave 3 group)

---

- [ ] 18. Document Management UI

  **What to do**:
  - Create `frontend/app/documents/page.tsx` - Documents list page
  - Create `frontend/components/documents/document-list.tsx` - List with status badges
  - Create `frontend/components/documents/upload-dialog.tsx` - Upload modal with drag-drop
  - Create `frontend/components/documents/document-card.tsx` - Card with actions
  - Show processing status with spinner
  - Add delete confirmation dialog
  - Write component tests

  **Must NOT do**:
  - Allow actions on processing documents
  - Skip loading states

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `["frontend-ui-ux"]`
  - Reason: Document management UI

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3
  - **Blocks**: None directly
  - **Blocked By**: Tasks 5, 15

  **References**:
  - `frontend/components/ui/` - Base components

  **QA Scenarios**:
  ```
  Scenario: Upload document via UI
    Tool: Playwright
    Steps:
      1. Navigate to /documents
      2. Click upload button
      3. Select PDF file
      4. Assert upload progress shows
    Expected: Document appears in list
    Evidence: .sisyphus/evidence/task-18-upload-ui.png
  ```

  **Commit**: YES (Wave 3 group)

---

- [ ] 19. Points Wallet + Ledger Tables

  **What to do**:
  - Verify tables from Task 2 exist (points_wallets, points_transactions)
  - Create `backend/src/app/db/repositories/points_repository.py` - Wallet CRUD
  - Add unique constraint on (wallet_id, operation_type, idempotency_key)
  - Create indexes for fast lookups
  - Write repository tests

  **Must NOT do**:
  - Allow duplicate idempotency keys
  - Skip audit trail

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`
  - Reason: Database repository

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3
  - **Blocks**: Tasks 20, 21
  - **Blocked By**: Task 2

  **References**:
  - `docs/AI_ARCHITECTURE.md:187-210` - Points architecture

  **QA Scenarios**:
  ```
  Scenario: Idempotency key enforced
    Tool: Bash
    Steps:
      1. Insert transaction with key "abc"
      2. Try inserting same key again
    Expected: Unique constraint error
    Evidence: .sisyphus/evidence/task-19-idempotency.txt
  ```

  **Commit**: YES (Wave 3 group)

---

- [ ] 20. Points Service (Reserve/Commit/Refund)

  **What to do**:
  - Create `backend/src/app/modules/points_billing/service.py` - PointsService class
  - Implement reserve(wallet_id, amount, idempotency_key) - Lock funds
  - Implement commit(reservation_id) - Finalize deduction
  - Implement refund(reservation_id) - Release reserved funds
  - Use SELECT FOR UPDATE for wallet locking
  - All operations atomic in single transaction
  - Write comprehensive tests for edge cases

  **Must NOT do**:
  - Allow negative balance
  - Skip idempotency
  - Use multiple transactions

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: `[]`
  - Reason: Critical financial logic

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 19)
  - **Parallel Group**: Wave 3
  - **Blocks**: Tasks 21, 23, 24-32, 38-40
  - **Blocked By**: Tasks 2, 9, 19

  **References**:
  - `docs/AI_ARCHITECTURE.md:187-210` - Atomicity pattern
  - `docs/PRODUCT_RULES.md:48-53` - Points rules

  **QA Scenarios**:
  ```
  Scenario: Reserve then commit
    Tool: Bash
    Steps:
      1. Reserve 10 points (balance 50 -> available 40)
      2. Commit reservation
      3. Check balance = 40
    Expected: Balance decremented correctly
    Evidence: .sisyphus/evidence/task-20-commit.txt

  Scenario: Reserve then refund
    Tool: Bash
    Steps:
      1. Reserve 10 points
      2. Refund reservation
      3. Check balance = 50
    Expected: Balance unchanged
    Evidence: .sisyphus/evidence/task-20-refund.txt

  Scenario: Insufficient points rejected
    Tool: Bash
    Steps:
      1. Try reserve 100 points (balance 50)
    Expected: Error INSUFFICIENT_POINTS
    Evidence: .sisyphus/evidence/task-20-insufficient.txt
  ```

  **Commit**: YES (Wave 3 group)

---

- [ ] 21. Daily Quota Enforcement

  **What to do**:
  - Create `backend/src/app/modules/points_billing/quota.py` - Daily quota tracker
  - Track generations per user per day (3 free)
  - Reset counter at midnight UTC
  - Check quota before points deduction
  - If quota available, don't deduct points
  - If quota exhausted, require points
  - Create API endpoint: GET /api/v1/points/quota
  - Write tests

  **Must NOT do**:
  - Allow unlimited free generations
  - Skip timezone handling

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: `[]`
  - Reason: Quota logic with time handling

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 20)
  - **Parallel Group**: Wave 3
  - **Blocks**: Tasks 24-32
  - **Blocked By**: Tasks 9, 20

  **References**:
  - `docs/PRODUCT_RULES.md:49-50` - Daily quota

  **QA Scenarios**:
  ```
  Scenario: First 3 generations free
    Tool: Bash
    Steps:
      1. Generate 3 times
      2. Check points unchanged
    Expected: Balance still 50
    Evidence: .sisyphus/evidence/task-21-free.txt

  Scenario: 4th generation costs points
    Tool: Bash
    Steps:
      1. Generate 4th time
      2. Check points deducted
    Expected: Balance < 50
    Evidence: .sisyphus/evidence/task-21-paid.txt
  ```

  **Commit**: YES (Wave 3 group)

---

- [ ] 22. Points UI Component

  **What to do**:
  - Create `frontend/components/points/wallet-display.tsx` - Balance badge
  - Create `frontend/components/points/quota-display.tsx` - Daily quota remaining
  - Create `frontend/components/points/transaction-history.tsx` - Recent transactions
  - Add wallet display to header/sidebar
  - Show low-balance warning (< 10 points)
  - Write component tests

  **Must NOT do**:
  - Hide balance from user
  - Skip loading states

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `["frontend-ui-ux"]`
  - Reason: UI component

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3
  - **Blocks**: None
  - **Blocked By**: Tasks 5, 20

  **References**:
  - `frontend/components/ui/badge.tsx` - Badge pattern

  **QA Scenarios**:
  ```
  Scenario: Balance displays in header
    Tool: Playwright
    Steps:
      1. Login and complete onboarding
      2. Navigate to dashboard
    Expected: "50 points" visible in header
    Evidence: .sisyphus/evidence/task-22-balance.png
  ```

  **Commit**: YES (Wave 3 group)

---

- [ ] 23. Invite Link System

  **What to do**:
  - Create `backend/src/app/modules/invites/service.py` - Invite logic
  - Create `backend/src/app/api/v1/invites.py` - Routes: POST /create, GET /my-link, POST /redeem
  - Generate unique invite codes per user
  - Track redemptions (max 1 per invited user)
  - Award 20 points to inviter when invitee completes onboarding
  - Anti-fraud: same IP detection, rate limiting
  - Write tests

  **Must NOT do**:
  - Allow self-referral
  - Skip anti-fraud checks
  - Award before onboarding complete

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: `[]`
  - Reason: Business logic with fraud prevention

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3
  - **Blocks**: None
  - **Blocked By**: Tasks 9, 20

  **References**:
  - `docs/PRODUCT_RULES.md:55-57` - Invite rules
  - `docs/PRODUCT_RULES.md:75-79` - Anti-abuse

  **QA Scenarios**:
  ```
  Scenario: Invite rewards points
    Tool: Bash
    Steps:
      1. User A creates invite link
      2. User B signs up via link
      3. User B completes onboarding
      4. Check User A balance
    Expected: User A has 70 points (50 + 20)
    Evidence: .sisyphus/evidence/task-23-invite-reward.txt

  Scenario: Duplicate invite rejected
    Tool: Bash
    Steps:
      1. User B already redeemed
      2. User B tries to redeem again
    Expected: Error ALREADY_REDEEMED
    Evidence: .sisyphus/evidence/task-23-duplicate.txt
  ```

  **Commit**: YES (Wave 3 group)

---

### Wave 4: AI Features

- [ ] 24. RAG Retriever Service

  **What to do**:
  - Create `backend/src/app/modules/rag/retriever.py` - Semantic search over chunks
  - Create `backend/src/app/modules/rag/prompt_builder.py` - Build prompts with context
  - Create `backend/src/app/modules/rag/citation.py` - Extract citations from response
  - Implement top-k retrieval with metadata filters (document_id, user_id, group_id)
  - Use existing pgvector similarity search
  - Return chunks with page numbers for citation
  - Write tests

  **Must NOT do**:
  - Return chunks from other users' documents
  - Skip relevance filtering

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: `[]`
  - Reason: Core RAG implementation

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Tasks 25-32)
  - **Blocks**: Tasks 25, 27, 29, 38
  - **Blocked By**: Tasks 17

  **References**:
  - `docs/AI_ARCHITECTURE.md:158-177` - RAG spec
  - `backend/src/app/semantic_search.py` - Existing search

  **QA Scenarios**:
  ```
  Scenario: Retriever finds relevant chunks
    Tool: Bash
    Steps:
      1. Upload PDF about "machine learning"
      2. Query: "What is machine learning?"
      3. Check retrieved chunks contain relevant content
    Expected: Top chunks mention machine learning
    Evidence: .sisyphus/evidence/task-24-retrieval.txt
  ```

  **Commit**: YES (Wave 4 group)

---

- [ ] 25. AI Chat API with Citations

  **What to do**:
  - Create `backend/src/app/modules/ai_generation/chat_service.py` - Chat with RAG
  - Create `backend/src/app/api/v1/ai_chat.py` - Routes: POST /chat, GET /history
  - Integrate retriever to get context
  - Build prompt with grounded context
  - Call NVIDIA chat endpoint
  - Parse response and extract citations
  - Return answer with citations array
  - Check points/quota before generation
  - Store chat history
  - Write tests

  **Must NOT do**:
  - Return ungrounded answers without marking external=true
  - Skip points check

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: `[]`
  - Reason: Core AI feature with RAG

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 24)
  - **Parallel Group**: Wave 4
  - **Blocks**: Tasks 26, 38
  - **Blocked By**: Tasks 17, 20, 21, 24

  **References**:
  - `docs/AI_ARCHITECTURE.md:158-177` - Chat spec
  - `backend/src/app/ai_routes.py` - Existing chat endpoint

  **QA Scenarios**:
  ```
  Scenario: Chat returns grounded answer
    Tool: Bash (curl)
    Steps:
      1. Upload PDF
      2. POST /api/v1/ai/chat with question
    Expected: Response with answer + citations array
    Evidence: .sisyphus/evidence/task-25-chat.txt

  Scenario: Chat blocked without points
    Tool: Bash (curl)
    Steps:
      1. Exhaust daily quota and points
      2. POST /api/v1/ai/chat
    Expected: 402 INSUFFICIENT_POINTS
    Evidence: .sisyphus/evidence/task-25-no-points.txt
  ```

  **Commit**: YES (Wave 4 group)

---

- [ ] 26. AI Chat UI

  **What to do**:
  - Create `frontend/app/chat/page.tsx` - Chat interface
  - Create `frontend/app/chat/[documentId]/page.tsx` - Chat for specific document
  - Create `frontend/components/chat/message-list.tsx` - Chat messages
  - Create `frontend/components/chat/message-input.tsx` - Input with send button
  - Create `frontend/components/chat/citation-card.tsx` - Clickable citations
  - Show typing indicator
  - Highlight cited pages
  - Write component tests

  **Must NOT do**:
  - Block UI during response
  - Hide citations

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `["frontend-ui-ux"]`
  - Reason: Chat UI

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 25 API)
  - **Parallel Group**: Wave 4
  - **Blocks**: None
  - **Blocked By**: Tasks 5, 25

  **References**:
  - Modern chat UI patterns

  **QA Scenarios**:
  ```
  Scenario: Send message and receive response
    Tool: Playwright
    Steps:
      1. Navigate to /chat/[documentId]
      2. Type question in input
      3. Click send
      4. Wait for response
    Expected: AI response appears with citations
    Evidence: .sisyphus/evidence/task-26-chat-ui.png
  ```

  **Commit**: YES (Wave 4 group)

---

- [ ] 27. Presentation Generation API

  **What to do**:
  - Create `backend/src/app/modules/ai_generation/presentation_service.py` - Slide generation
  - Create `backend/src/app/api/v1/presentations.py` - Routes: POST /generate, GET /list, GET /{id}
  - Create `backend/src/app/workers/jobs/generate_slides.py` - Async job
  - Use RAG to get relevant content
  - Generate slide structure via AI (title, bullets, key points)
  - Output JSON slide format
  - Check points/quota
  - Store generated presentations
  - Write tests

  **Must NOT do**:
  - Generate synchronously (use worker)
  - Skip points check

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: `[]`
  - Reason: AI generation with worker

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4
  - **Blocks**: Task 28
  - **Blocked By**: Tasks 17, 20, 21, 24

  **References**:
  - `docs/PRODUCT_RULES.md:42` - Presentation feature

  **QA Scenarios**:
  ```
  Scenario: Generate presentation
    Tool: Bash (curl)
    Steps:
      1. POST /api/v1/presentations/generate with document_id
      2. Poll for completion
    Expected: Presentation with slides array
    Evidence: .sisyphus/evidence/task-27-presentation.txt
  ```

  **Commit**: YES (Wave 4 group)

---

- [ ] 28. Presentation Generation UI

  **What to do**:
  - Create `frontend/app/presentations/page.tsx` - Presentations list
  - Create `frontend/app/presentations/[id]/page.tsx` - Presentation viewer
  - Create `frontend/components/presentations/slide-viewer.tsx` - Slide carousel
  - Create `frontend/components/presentations/generate-dialog.tsx` - Generation options
  - Show generation progress
  - Allow slide navigation
  - Write component tests

  **Must NOT do**:
  - Block on generation
  - Skip progress feedback

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `["frontend-ui-ux"]`
  - Reason: Presentation UI

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 27)
  - **Parallel Group**: Wave 4
  - **Blocks**: None
  - **Blocked By**: Tasks 5, 27

  **QA Scenarios**:
  ```
  Scenario: View generated presentation
    Tool: Playwright
    Steps:
      1. Generate presentation
      2. Navigate to /presentations/[id]
    Expected: Slides display with navigation
    Evidence: .sisyphus/evidence/task-28-slides.png
  ```

  **Commit**: YES (Wave 4 group)

---

- [ ] 29. Quiz Generation API

  **What to do**:
  - Create `backend/src/app/modules/quiz/service.py` - Quiz generation
  - Create `backend/src/app/api/v1/quizzes.py` - Routes: POST /generate, GET /list, GET /{id}, POST /{id}/submit
  - Create `backend/src/app/workers/jobs/generate_quiz.py` - Async job
  - Use RAG to get content for questions
  - Generate QCM with 4 options each
  - Include correct answer and explanation
  - Store quiz with questions
  - Validate submissions and calculate score
  - Check points/quota
  - Write tests

  **Must NOT do**:
  - Generate questions without source content
  - Skip explanation generation

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: `[]`
  - Reason: Complex AI feature

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4
  - **Blocks**: Tasks 30, 31, 40
  - **Blocked By**: Tasks 17, 20, 21, 24

  **References**:
  - `docs/PRODUCT_RULES.md:45-46` - Quiz rules

  **QA Scenarios**:
  ```
  Scenario: Generate quiz from document
    Tool: Bash (curl)
    Steps:
      1. POST /api/v1/quizzes/generate with document_id
      2. Poll for completion
    Expected: Quiz with questions array, each having 4 options
    Evidence: .sisyphus/evidence/task-29-quiz.txt

  Scenario: Submit quiz answers
    Tool: Bash (curl)
    Steps:
      1. POST /api/v1/quizzes/{id}/submit with answers
    Expected: Score and corrections with explanations
    Evidence: .sisyphus/evidence/task-29-submit.txt
  ```

  **Commit**: YES (Wave 4 group)

---

- [ ] 30. Quiz Generation UI

  **What to do**:
  - Create `frontend/app/quizzes/page.tsx` - Quiz list
  - Create `frontend/app/quizzes/generate/page.tsx` - Generation options
  - Create `frontend/components/quiz/generate-form.tsx` - Select document, options
  - Show generation progress
  - Write component tests

  **Must NOT do**:
  - Block on generation
  - Skip document selection

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `["frontend-ui-ux"]`
  - Reason: Quiz UI

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 29)
  - **Parallel Group**: Wave 4
  - **Blocks**: None
  - **Blocked By**: Tasks 5, 29

  **QA Scenarios**:
  ```
  Scenario: Generate quiz via UI
    Tool: Playwright
    Steps:
      1. Navigate to /quizzes/generate
      2. Select document
      3. Click generate
    Expected: Progress shown, quiz created
    Evidence: .sisyphus/evidence/task-30-generate.png
  ```

  **Commit**: YES (Wave 4 group)

---

- [ ] 31. Quiz Player + Correction UI

  **What to do**:
  - Create `frontend/app/quizzes/[id]/page.tsx` - Quiz player
  - Create `frontend/components/quiz/question-card.tsx` - Question with options
  - Create `frontend/components/quiz/result-card.tsx` - Score and corrections
  - Create `frontend/components/quiz/explanation-card.tsx` - Show explanation on wrong answer
  - Track answered questions
  - Submit all at once or one by one
  - Show corrections with source references
  - Write component tests

  **Must NOT do**:
  - Allow changing answers after submission
  - Hide explanations

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `["frontend-ui-ux"]`
  - Reason: Interactive quiz UI

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 29)
  - **Parallel Group**: Wave 4
  - **Blocks**: None
  - **Blocked By**: Tasks 5, 29

  **QA Scenarios**:
  ```
  Scenario: Take quiz and see corrections
    Tool: Playwright
    Steps:
      1. Navigate to /quizzes/[id]
      2. Answer all questions
      3. Submit
    Expected: Score displayed, wrong answers show explanations
    Evidence: .sisyphus/evidence/task-31-quiz-player.png
  ```

  **Commit**: YES (Wave 4 group)

---

- [ ] 32. Promo Code System

  **What to do**:
  - Create `backend/src/app/modules/promo/service.py` - Promo logic
  - Create `backend/src/app/api/v1/promo.py` - Routes: POST /redeem
  - Validate code exists and is active
  - Check max uses not exceeded
  - Check user hasn't redeemed before
  - Award points to user wallet
  - Track redemption
  - Write tests

  **Must NOT do**:
  - Allow double redemption
  - Skip validation

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: `[]`
  - Reason: Business logic

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4
  - **Blocks**: Task 43
  - **Blocked By**: Tasks 9, 20

  **References**:
  - `docs/PRODUCT_RULES.md:55-57` - Promo rules

  **QA Scenarios**:
  ```
  Scenario: Redeem valid promo code
    Tool: Bash (curl)
    Steps:
      1. POST /api/v1/promo/redeem with code
    Expected: Points added to wallet
    Evidence: .sisyphus/evidence/task-32-redeem.txt

  Scenario: Invalid code rejected
    Tool: Bash (curl)
    Steps:
      1. POST /api/v1/promo/redeem with "INVALID"
    Expected: 404 CODE_NOT_FOUND
    Evidence: .sisyphus/evidence/task-32-invalid.txt
  ```

  **Commit**: YES (Wave 4 group)

---

### Wave 5: Groups + Real-time

- [ ] 33. Groups CRUD API

  **What to do**:
  - Create `backend/src/app/modules/groups/service.py` - Group management
  - Create `backend/src/app/api/v1/groups.py` - Routes: POST /create, GET /list, GET /{id}, PUT /{id}, DELETE /{id}
  - Create group with name, owner, point_mode (payer/pooled)
  - Validate group name uniqueness for owner
  - Owner can update/delete group
  - Write tests

  **Must NOT do**:
  - Allow non-owners to delete
  - Skip validation

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: `[]`
  - Reason: Standard CRUD

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 5 (with Tasks 34-41)
  - **Blocks**: Tasks 34-40
  - **Blocked By**: Task 9

  **References**:
  - `docs/PRODUCT_RULES.md:59-68` - Group rules

  **QA Scenarios**:
  ```
  Scenario: Create group
    Tool: Bash (curl)
    Steps:
      1. POST /api/v1/groups/create with name, point_mode
    Expected: 201 with group_id
    Evidence: .sisyphus/evidence/task-33-create.txt
  ```

  **Commit**: YES (Wave 5 group)

---

- [ ] 34. Group Membership + Invites

  **What to do**:
  - Create `backend/src/app/modules/groups/membership_service.py` - Membership logic
  - Add routes: POST /{id}/invite, POST /join/{code}, GET /{id}/members, DELETE /{id}/members/{userId}
  - Generate invite codes for groups
  - Add member with role (admin, member)
  - Owner can remove members
  - Members can leave
  - Write tests

  **Must NOT do**:
  - Allow joining without invite
  - Let members kick others

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: `[]`
  - Reason: Membership logic

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 33)
  - **Parallel Group**: Wave 5
  - **Blocks**: Tasks 35-40
  - **Blocked By**: Tasks 9, 33

  **QA Scenarios**:
  ```
  Scenario: Invite and join group
    Tool: Bash (curl)
    Steps:
      1. Create group
      2. Generate invite
      3. Different user joins with code
    Expected: User appears in members list
    Evidence: .sisyphus/evidence/task-34-join.txt
  ```

  **Commit**: YES (Wave 5 group)

---

- [ ] 35. Group PDF Sharing

  **What to do**:
  - Create `backend/src/app/modules/groups/documents_service.py` - Shared docs
  - Add routes: POST /{id}/documents, GET /{id}/documents, DELETE /{id}/documents/{docId}
  - Share document to group (set group_id on document)
  - All members can view shared documents
  - Chunks from shared docs available for group RAG
  - Write tests

  **Must NOT do**:
  - Allow non-members to access
  - Break individual document ownership

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: `[]`
  - Reason: RAG integration

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 34)
  - **Parallel Group**: Wave 5
  - **Blocks**: Tasks 38
  - **Blocked By**: Tasks 15, 33, 34

  **QA Scenarios**:
  ```
  Scenario: Shared doc visible to members
    Tool: Bash (curl)
    Steps:
      1. Share document to group
      2. Member queries group documents
    Expected: Document in list
    Evidence: .sisyphus/evidence/task-35-shared.txt
  ```

  **Commit**: YES (Wave 5 group)

---

- [ ] 36. WebSocket Chat Server

  **What to do**:
  - Create `backend/src/app/websocket/chat_handler.py` - Chat event handlers
  - Events: join_room, leave_room, message, typing
  - Authenticate connection via session token
  - Room = group_id
  - Broadcast messages to room members
  - Store messages in database
  - Handle disconnections
  - Write tests

  **Must NOT do**:
  - Allow unauthenticated connections
  - Skip message persistence

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: `[]`
  - Reason: Real-time infrastructure

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 6)
  - **Parallel Group**: Wave 5
  - **Blocks**: Tasks 37, 38
  - **Blocked By**: Tasks 6, 9, 33

  **References**:
  - Task 6 WebSocket setup

  **QA Scenarios**:
  ```
  Scenario: Message broadcast to room
    Tool: Bash (multiple connections)
    Steps:
      1. User A joins room
      2. User B joins room
      3. User A sends message
    Expected: User B receives message
    Evidence: .sisyphus/evidence/task-36-broadcast.txt
  ```

  **Commit**: YES (Wave 5 group)

---

- [ ] 37. Real-time Chat UI

  **What to do**:
  - Create `frontend/app/groups/[id]/chat/page.tsx` - Group chat
  - Create `frontend/components/groups/chat-room.tsx` - Chat container
  - Create `frontend/components/groups/chat-message.tsx` - Message bubble
  - Create `frontend/components/groups/typing-indicator.tsx` - Who's typing
  - Create `frontend/components/groups/member-list.tsx` - Online members
  - Connect to WebSocket on mount
  - Show real-time messages
  - Write component tests

  **Must NOT do**:
  - Use polling
  - Skip reconnection

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `["frontend-ui-ux"]`
  - Reason: Real-time UI

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 36)
  - **Parallel Group**: Wave 5
  - **Blocks**: None
  - **Blocked By**: Tasks 5, 6, 36

  **QA Scenarios**:
  ```
  Scenario: Real-time chat works
    Tool: Playwright (2 browser contexts)
    Steps:
      1. User A opens chat
      2. User B opens chat
      3. User A types and sends
    Expected: Message appears for User B instantly
    Evidence: .sisyphus/evidence/task-37-realtime.png
  ```

  **Commit**: YES (Wave 5 group)

---

- [ ] 38. AI in Group Chat

  **What to do**:
  - Add @ai mention detection in messages
  - When @ai mentioned, trigger RAG chat with group context
  - Include shared documents in retrieval
  - Broadcast AI response to room
  - Deduct points from sender (or pool based on mode)
  - Write tests

  **Must NOT do**:
  - Skip points check
  - Use private docs without consent

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: `[]`
  - Reason: AI + real-time integration

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Tasks 25, 35, 36)
  - **Parallel Group**: Wave 5
  - **Blocks**: None
  - **Blocked By**: Tasks 20, 24, 25, 35, 36

  **QA Scenarios**:
  ```
  Scenario: AI responds in group chat
    Tool: Bash
    Steps:
      1. User sends "@ai What is chapter 1 about?"
      2. Wait for AI response
    Expected: AI message broadcast to room with answer
    Evidence: .sisyphus/evidence/task-38-ai-chat.txt
  ```

  **Commit**: YES (Wave 5 group)

---

- [ ] 39. Group Points Modes (Payer/Pooled)

  **What to do**:
  - Create `backend/src/app/modules/groups/points_service.py` - Group points logic
  - Payer mode: Deduct from action initiator
  - Pooled mode: Create group wallet, members contribute
  - Add routes: POST /{id}/wallet/contribute, GET /{id}/wallet
  - Check mode before AI actions
  - Write tests

  **Must NOT do**:
  - Mix modes
  - Allow negative pool balance

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: `[]`
  - Reason: Financial logic

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Tasks 20, 33)
  - **Parallel Group**: Wave 5
  - **Blocks**: None
  - **Blocked By**: Tasks 20, 33, 34

  **References**:
  - `docs/PRODUCT_RULES.md:65-68` - Point modes

  **QA Scenarios**:
  ```
  Scenario: Payer mode deducts from initiator
    Tool: Bash
    Steps:
      1. Set group to payer mode
      2. User A generates in group
    Expected: User A points deducted
    Evidence: .sisyphus/evidence/task-39-payer.txt

  Scenario: Pooled mode uses group wallet
    Tool: Bash
    Steps:
      1. Set group to pooled mode
      2. Members contribute
      3. User generates in group
    Expected: Group wallet deducted
    Evidence: .sisyphus/evidence/task-39-pooled.txt
  ```

  **Commit**: YES (Wave 5 group)

---

- [ ] 40. Quiz Sharing in Groups

  **What to do**:
  - Add routes: POST /groups/{id}/quizzes/{quizId}/share, GET /groups/{id}/quizzes
  - Share quiz to group
  - Members can view and take shared quizzes
  - Track attempts per member
  - Show leaderboard
  - Write tests

  **Must NOT do**:
  - Allow editing shared quiz
  - Hide scores

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: `[]`
  - Reason: Business logic

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Tasks 29, 34)
  - **Parallel Group**: Wave 5
  - **Blocks**: None
  - **Blocked By**: Tasks 29, 33, 34

  **QA Scenarios**:
  ```
  Scenario: Member takes shared quiz
    Tool: Bash (curl)
    Steps:
      1. Owner shares quiz to group
      2. Member fetches group quizzes
      3. Member submits answers
    Expected: Score recorded
    Evidence: .sisyphus/evidence/task-40-shared-quiz.txt
  ```

  **Commit**: YES (Wave 5 group)

---

- [ ] 41. Professor Contact Admin Feature

  **What to do**:
  - Create `backend/src/app/modules/admin/contact_service.py` - Contact requests
  - Create route: POST /api/v1/profile/contact-admin (professor only)
  - Store contact request in database
  - Show "Contact Admin" button in professor profile UI
  - Create `frontend/components/profile/contact-admin-button.tsx`
  - Write tests

  **Must NOT do**:
  - Allow non-professors to contact
  - Skip rate limiting

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`
  - Reason: Simple feature

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 5
  - **Blocks**: Task 45
  - **Blocked By**: Task 9

  **References**:
  - `docs/PRODUCT_RULES.md:70-73` - Teacher bonus

  **QA Scenarios**:
  ```
  Scenario: Professor contacts admin
    Tool: Bash (curl)
    Steps:
      1. POST /api/v1/profile/contact-admin with message
    Expected: Request stored
    Evidence: .sisyphus/evidence/task-41-contact.txt
  ```

  **Commit**: YES (Wave 5 group)

---

### Wave 6: Admin Panel

- [ ] 42. Admin Auth + Role Guard

  **What to do**:
  - Create `backend/src/app/api/deps/admin_guard.py` - Admin role check
  - Add admin role to user model
  - Create admin-only middleware
  - Return 403 for non-admins
  - Create `frontend/middleware.ts` update for /admin routes
  - Write tests

  **Must NOT do**:
  - Allow any user to access admin
  - Skip audit logging

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: `[]`
  - Reason: Security-critical

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 6 (with Tasks 43-48)
  - **Blocks**: Tasks 43-48
  - **Blocked By**: Task 9

  **References**:
  - `docs/AI_ARCHITECTURE.md:256-257` - RBAC roles

  **QA Scenarios**:
  ```
  Scenario: Non-admin blocked
    Tool: Bash (curl)
    Steps:
      1. Login as regular user
      2. GET /api/v1/admin/users
    Expected: 403 Forbidden
    Evidence: .sisyphus/evidence/task-42-blocked.txt

  Scenario: Admin allowed
    Tool: Bash (curl)
    Steps:
      1. Login as admin
      2. GET /api/v1/admin/users
    Expected: 200 with users list
    Evidence: .sisyphus/evidence/task-42-allowed.txt
  ```

  **Commit**: YES (Wave 6 group)

---

- [ ] 43. Promo Code Management UI

  **What to do**:
  - Create `frontend/app/admin/promo/page.tsx` - Promo codes list
  - Create `frontend/components/admin/promo-table.tsx` - Table with actions
  - Create `frontend/components/admin/create-promo-dialog.tsx` - Create new code
  - Show: code, points, max_uses, uses, active status
  - Actions: create, toggle active, delete
  - Create admin API routes: GET /admin/promo, POST /admin/promo, PUT /admin/promo/{id}, DELETE /admin/promo/{id}
  - Write tests

  **Must NOT do**:
  - Allow editing redeemed codes
  - Skip validation

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `["frontend-ui-ux"]`
  - Reason: Admin UI

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 42)
  - **Parallel Group**: Wave 6
  - **Blocks**: None
  - **Blocked By**: Tasks 32, 42

  **QA Scenarios**:
  ```
  Scenario: Create promo code
    Tool: Playwright
    Steps:
      1. Navigate to /admin/promo
      2. Click create
      3. Fill form, submit
    Expected: New code appears in table
    Evidence: .sisyphus/evidence/task-43-create-promo.png
  ```

  **Commit**: YES (Wave 6 group)

---

- [ ] 44. User Management UI

  **What to do**:
  - Create `frontend/app/admin/users/page.tsx` - Users list
  - Create `frontend/components/admin/users-table.tsx` - Table with filters
  - Create `frontend/components/admin/user-detail-dialog.tsx` - User details
  - Show: name, email, role, onboarding status, points balance, created
  - Filter by role, search by name/email
  - View user details and activity
  - Create admin API routes: GET /admin/users, GET /admin/users/{id}
  - Write tests

  **Must NOT do**:
  - Allow editing user data directly
  - Show sensitive data (phone)

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `["frontend-ui-ux"]`
  - Reason: Admin UI

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 42)
  - **Parallel Group**: Wave 6
  - **Blocks**: None
  - **Blocked By**: Task 42

  **QA Scenarios**:
  ```
  Scenario: Search users
    Tool: Playwright
    Steps:
      1. Navigate to /admin/users
      2. Type in search box
    Expected: Users filtered by name/email
    Evidence: .sisyphus/evidence/task-44-search.png
  ```

  **Commit**: YES (Wave 6 group)

---

- [ ] 45. Teacher Bonus Request Workflow

  **What to do**:
  - Create `frontend/app/admin/teacher-requests/page.tsx` - Request list
  - Create `frontend/components/admin/request-card.tsx` - Request with actions
  - Show pending requests from Task 41
  - Actions: approve (grant bonus points), reject
  - Create admin API routes: GET /admin/teacher-requests, POST /admin/teacher-requests/{id}/approve, POST /admin/teacher-requests/{id}/reject
  - Add bonus points to teacher wallet on approve
  - Write tests

  **Must NOT do**:
  - Auto-approve
  - Skip audit log

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: `[]`
  - Reason: Workflow logic

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Tasks 41, 42)
  - **Parallel Group**: Wave 6
  - **Blocks**: None
  - **Blocked By**: Tasks 41, 42

  **References**:
  - `docs/PRODUCT_RULES.md:70-73` - Teacher bonus

  **QA Scenarios**:
  ```
  Scenario: Approve teacher request
    Tool: Playwright
    Steps:
      1. Navigate to /admin/teacher-requests
      2. Click approve on pending request
    Expected: Teacher wallet updated, request marked approved
    Evidence: .sisyphus/evidence/task-45-approve.png
  ```

  **Commit**: YES (Wave 6 group)

---

- [ ] 46. Points Adjustment UI

  **What to do**:
  - Create `frontend/app/admin/points/page.tsx` - Points management
  - Create `frontend/components/admin/adjust-points-dialog.tsx` - Adjust form
  - Search user, add/subtract points with reason
  - Create admin API route: POST /admin/points/adjust
  - Log all adjustments in ledger
  - Write tests

  **Must NOT do**:
  - Allow adjustment without reason
  - Skip ledger entry

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `["frontend-ui-ux"]`
  - Reason: Admin UI

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 42)
  - **Parallel Group**: Wave 6
  - **Blocks**: None
  - **Blocked By**: Tasks 20, 42

  **References**:
  - `docs/PRODUCT_RULES.md:85` - Adjust points

  **QA Scenarios**:
  ```
  Scenario: Add bonus points
    Tool: Playwright
    Steps:
      1. Search user
      2. Add 100 points with reason "Test bonus"
    Expected: User balance increases, ledger shows entry
    Evidence: .sisyphus/evidence/task-46-adjust.png
  ```

  **Commit**: YES (Wave 6 group)

---

- [ ] 47. Analytics Dashboard

  **What to do**:
  - Create `frontend/app/admin/page.tsx` - Admin dashboard
  - Create `frontend/components/admin/stats-cards.tsx` - Key metrics
  - Show: total users, users this week, total generations, points issued
  - Show: top users by generation, failing jobs
  - Create admin API route: GET /admin/stats
  - Write tests

  **Must NOT do**:
  - Show real-time without cache
  - Skip loading states

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `["frontend-ui-ux"]`
  - Reason: Dashboard UI

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 42)
  - **Parallel Group**: Wave 6
  - **Blocks**: None
  - **Blocked By**: Task 42

  **References**:
  - `docs/PRODUCT_RULES.md:81-85` - Admin rules

  **QA Scenarios**:
  ```
  Scenario: Dashboard shows stats
    Tool: Playwright
    Steps:
      1. Login as admin
      2. Navigate to /admin
    Expected: Stats cards visible with numbers
    Evidence: .sisyphus/evidence/task-47-dashboard.png
  ```

  **Commit**: YES (Wave 6 group)

---

- [ ] 48. Audit Log Viewer

  **What to do**:
  - Create `frontend/app/admin/audit/page.tsx` - Audit log
  - Create `frontend/components/admin/audit-table.tsx` - Log entries
  - Show: timestamp, user, action, resource, details
  - Filter by action type, user, date range
  - Create admin API route: GET /admin/audit
  - Create `backend/src/app/db/models/audit_log.py` - Audit model
  - Add audit logging to critical operations (points, admin actions)
  - Write tests

  **Must NOT do**:
  - Allow deleting logs
  - Skip sensitive action logging

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `["frontend-ui-ux"]`
  - Reason: Admin UI

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 42)
  - **Parallel Group**: Wave 6
  - **Blocks**: None
  - **Blocked By**: Task 42

  **References**:
  - `docs/AI_ARCHITECTURE.md:238-240` - Audit logs index

  **QA Scenarios**:
  ```
  Scenario: View audit logs
    Tool: Playwright
    Steps:
      1. Navigate to /admin/audit
      2. Filter by action type
    Expected: Filtered log entries shown
    Evidence: .sisyphus/evidence/task-48-audit.png
  ```

  **Commit**: YES (Wave 6 group)

---

## Final Verification Wave

> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.

- [ ] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists. For each "Must NOT Have": search codebase for forbidden patterns. Check evidence files exist. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. **Code Quality Review** — `unspecified-high`
  Run `bun run typecheck` + `bun run lint` + `bun run build` + `uv run pytest` + `uv run ruff check`. Review for: `as any`, empty catches, console.log in prod, AI slop patterns.
  Output: `Build [PASS/FAIL] | Lint [PASS/FAIL] | Tests [N/N] | VERDICT`

- [ ] F3. **Real Manual QA** — `unspecified-high` (+ `playwright` skill)
  Execute EVERY QA scenario from EVERY task. Test: login flow, onboarding, PDF upload, AI chat, presentations, quizzes, groups, admin. Save evidence to `.sisyphus/evidence/final-qa/`.
  Output: `Scenarios [N/N] | Integration [N/N] | VERDICT`

- [ ] F4. **Scope Fidelity Check** — `deep`
  For each task: verify 1:1 implementation vs spec. Check "Must NOT do" compliance. Detect scope creep. Flag unaccounted changes.
  Output: `Tasks [N/N compliant] | Scope Creep [CLEAN/issues] | VERDICT`

---

## Commit Strategy

| Wave | Commit Message | Files |
|------|---------------|-------|
| 1 | `feat(infra): add test infrastructure and base types` | configs, types, migrations |
| 2 | `feat(auth): add Google OAuth and onboarding flow` | auth/, onboarding/ |
| 3 | `feat(docs): add PDF processing and points system` | documents/, points/ |
| 4 | `feat(ai): add chat, presentations, and quiz generation` | ai/, chat/, quiz/ |
| 5 | `feat(groups): add group collaboration and real-time chat` | groups/, websocket/ |
| 6 | `feat(admin): add admin panel and management features` | admin/ |
| FINAL | `chore: final verification complete` | evidence/ |

---

## Success Criteria

### Verification Commands
```bash
# Frontend
cd frontend && bun run typecheck  # Expected: 0 errors
cd frontend && bun run lint       # Expected: 0 errors  
cd frontend && bun run build      # Expected: Success
cd frontend && bun test           # Expected: All pass

# Backend
cd backend && uv run ruff check . # Expected: 0 errors
cd backend && uv run pytest       # Expected: All pass

# Integration
curl -X POST http://localhost:8000/api/v1/auth/google  # Expected: 302 redirect
curl http://localhost:8000/api/health                   # Expected: {"status": "ok"}
```

### Final Checklist
- [ ] All "Must Have" requirements present and working
- [ ] All "Must NOT Have" items absent from codebase
- [ ] All tests pass (frontend + backend)
- [ ] All QA scenarios verified with evidence
- [ ] Onboarding gate blocks incomplete users
- [ ] Points mutations are atomic and idempotent
- [ ] WebSocket chat works in real-time
- [ ] Admin panel fully functional
