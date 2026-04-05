# Fehem Senior AI Architecture (Modular Monolith First)

## 1. Architecture Style
Start with a modular monolith backend and explicit domain modules:
- auth
- onboarding
- documents
- ai-generation
- quiz
- groups
- points-billing
- notifications
- admin

This enables fast product iteration now and future service extraction later.

## 2. High-Level Components
- Frontend (Next.js, Bun): UI, session handling, dashboards, group workspaces.
- API Backend (Python, uv): domain services, authz, orchestration, points ledger.
- Worker Layer (Python, uv): async processing for embeddings and generation jobs.
- PostgreSQL: source of truth for users, docs metadata, groups, quizzes, points ledger.
- Redis: queue broker, cache, rate limit counters, short-lived job states.
- Object Storage (S3-compatible): original PDFs, generated slides/videos, exports.
- Vector DB (pgvector or dedicated vector store): semantic retrieval over chunks.
- LLM/Media Providers: text model, embedding model, optional video generation provider.
- Observability: structured logs, traces, metrics, audit events.

## 3. Suggested Backend Layout
```
backend/
  pyproject.toml
  src/
    app/
      main.py
      api/
      core/
      db/
      modules/
        auth/
        onboarding/
        documents/
        ai_generation/
        quiz/
        groups/
        points_billing/
        notifications/
        admin/
      workers/
  tests/
```

## 4. Data Model Essentials
- users
- user_profiles (role-specific attributes)
- onboarding_responses
- groups, group_members
- documents, document_chunks
- embeddings_index_metadata
- generation_jobs, generation_artifacts
- quizzes, quiz_questions, quiz_attempts
- points_wallets, points_transactions (immutable ledger)
- promo_codes, promo_redemptions
- invite_links, invite_redemptions
- admin_actions, audit_logs

## 5. Critical Flows
### A. Onboarding gate
1. Google sign-in success.
2. If onboarding incomplete, force onboarding workflow.
3. Block generation endpoints until onboarding_completed = true.

### B. PDF to embeddings pipeline
1. Upload PDF to object storage.
2. Create parsing job with trace id.
3. Extract text, split into chunks.
4. Tag metadata (owner_id, group_id, language, page, upload_id).
5. Generate embeddings and upsert to vector index.
6. Mark document as indexed.

### C. AI course chat
1. User question arrives with course/group scope.
2. Retrieve top-k chunks from vector index.
3. Compose grounded prompt with citations.
4. Generate response.
5. Return answer + citation payload.

### D. Generation jobs (slides/video/quiz)
1. Validate onboarding and authorization.
2. Validate points/quota and reserve points atomically.
3. Enqueue async job.
4. Worker executes and stores artifacts.
5. Finalize points (commit/refund policy based on outcome).
6. Notify user/group with result.

## 6. Points Engine Rules
- Use immutable transaction ledger.
- All mutations are atomic and idempotent (idempotency key per operation).
- Separate operations:
  - reserve
  - commit
  - release/refund
- Support wallets:
  - personal wallet
  - optional group wallet
- Every deduction references actor, target feature, and generation job id.

## 7. Security Model
- Google OAuth only.
- RBAC roles: student, worker, teacher, admin.
- Document access policy based on ownership/group membership.
- Encrypt sensitive data at rest and in transit.
- Do not log tokens, secrets, or raw phone numbers.

## 8. AI Safety and Quality
- Default to grounded answers from indexed documents.
- Mark non-grounded output explicitly as external knowledge.
- Keep prompt templates versioned.
- Add output validation for quiz schema and citation format.

## 9. Reliability and SRE Baseline
- Job retries with exponential backoff.
- Dead-letter queue for failed jobs.
- Trace id propagation: API -> queue -> worker -> artifact.
- Metrics:
  - generation success rate
  - average job latency
  - retrieval hit quality
  - points transaction failures

## 10. Delivery Phases
### Phase 1 (MVP)
- Google auth
- mandatory onboarding
- PDF upload/indexing
- grounded AI chat
- basic quiz generation
- points ledger + daily quota

### Phase 2
- slide generation
- group collaboration and shared context
- invite rewards + promo codes
- admin panel for bonuses and moderation

### Phase 3
- video generation
- advanced analytics
- teacher classroom workflows
- potential extraction of ai-generation worker into separate service

## 11. Engineering Process Rules
- Frontend commands use Bun only.
- Backend workflows use uv only.
- Every PR must pass lint, typecheck, tests, and build.
- Add tests first for:
  - points correctness
  - onboarding gate
  - role-based access
  - group sharing rules
  - promo/invite anti-abuse behavior
