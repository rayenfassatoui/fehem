# Fehem Senior FastAPI + AI Architecture

## 1. Goal
Build Fehem as a reliable AI-learning platform with:
- strict onboarding and auth gates
- auditable and atomic points logic
- grounded AI outputs via RAG
- clear domain boundaries for long-term maintainability

The architecture should start as a modular monolith, then split selected workloads into services only when scale requires it.

## 2. Architecture Principles
1. Domain-first boundaries, not file-type boundaries.
2. API layer stays thin; business rules live in services.
3. Every AI request must be traceable and reproducible.
4. Heavy AI workflows run asynchronously.
5. Point mutations must be atomic, idempotent, and auditable.
6. Responses that are not grounded in indexed content must be labeled external.

## 3. System Topology
- Frontend (Next.js + Bun): app UI, auth session, user workflows.
- API (FastAPI + uv): authz, onboarding guard, orchestration, domain services.
- Worker (Python + uv): document parsing, embedding, generation jobs.
- PostgreSQL: transactional source of truth and immutable points ledger.
- Redis: queue broker, rate limit counters, short-lived locks.
- Object storage: raw files and generated artifacts.
- Vector index (pgvector on PostgreSQL): semantic retrieval.
- AI providers: chat/embedding/media APIs behind provider adapters.
- Observability stack: structured logs, metrics, traces, audit trails.

## 4. Backend Package Layout (Target)
```text
backend/
  pyproject.toml
  src/app/
    main.py
    config.py
    api/
      router.py
      deps/
        auth.py
        onboarding_gate.py
        idempotency.py
      v1/
        health.py
        ai_chat.py
        generation.py
        documents.py
        groups.py
        points.py
    core/
      errors.py
      logging.py
      tracing.py
      security.py
    db/
      session.py
      models/
      repositories/
      migrations/
    modules/
      auth/
        service.py
        schemas.py
      onboarding/
        service.py
        schemas.py
      documents/
        service.py
        chunker.py
        parser.py
        schemas.py
      rag/
        retriever.py
        prompt_builder.py
        citation.py
      ai_generation/
        service.py
        providers/
          base.py
          nvidia_provider.py
      quiz/
        service.py
        validator.py
      groups/
        service.py
      points_billing/
        service.py
        ledger.py
        idempotency.py
      notifications/
        service.py
      admin/
        service.py
    workers/
      queue.py
      jobs/
        index_document.py
        generate_quiz.py
        generate_slides.py
        generate_video.py
    contracts/
      events.py
      ai_payloads.py
      api_errors.py
  tests/
    unit/
    integration/
    e2e/
```

## 5. Domain Ownership
- auth: Google OAuth identity, token/session validation, role resolution.
- onboarding: profile completion checks and role-specific required fields.
- documents: upload metadata, parsing orchestration, chunk lifecycle.
- rag: retrieval, grounding prompt assembly, citation payload formatting.
- ai_generation: provider orchestration for chat/quiz/slides/video.
- quiz: generation, schema validation, correction logic.
- groups: membership, shared context, access policy.
- points_billing: reserve/commit/refund and immutable transaction ledger.
- notifications: user and group delivery for job completion/failure.
- admin: promo codes, bonus grants, abuse review actions.

Each domain exposes a service interface and keeps internal details private.

## 6. Core Runtime Flows

### 6.1 Onboarding Gate (Mandatory)
1. User authenticates with Google OAuth.
2. API resolves role and onboarding status.
3. For generation endpoints, onboarding gate denies access when incomplete.
4. Error response includes machine-readable code and next_action.

Example error contract:
```json
{
  "error": {
    "code": "ONBOARDING_REQUIRED",
    "message": "Complete onboarding before using AI generation.",
    "next_action": "open_onboarding"
  }
}
```

### 6.2 PDF to Embeddings Pipeline
1. API validates ownership/group scope and stores upload metadata.
2. Raw PDF stored in object storage with upload_id.
3. Worker parses PDF, splits text into chunks, tags metadata:
   - owner_id
   - group_id
   - language
   - page
   - upload_id
4. Worker creates embeddings and upserts to vector index.
5. API marks document indexing_status as ready or failed with actionable reason.

### 6.3 Grounded Course Chat
1. User question arrives with course/group context.
2. Retriever fetches top-k chunks with metadata filters.
3. Prompt builder injects only retrieved context.
4. Model response includes citation payload.
5. If response uses external knowledge, external=true must be explicit.

Response shape (minimum):
```json
{
  "answer": "...",
  "citations": [
    {
      "document_id": "...",
      "page": 12,
      "snippet": "..."
    }
  ],
  "external": false
}
```

### 6.4 Generation Jobs (Quiz, Slides, Video)
1. Validate auth, role, onboarding, and scope permissions.
2. Reserve points atomically with idempotency key.
3. Create generation_job row and enqueue async work.
4. Worker executes generation and stores artifacts.
5. Commit or refund points based on final status.
6. Emit notification and audit event with trace_id.

## 7. Points and Billing Architecture

### 7.1 Ledger Rules
- Use immutable ledger table for all point changes.
- Wallet balance is derived from committed ledger entries or maintained by transactional snapshot.
- No silent in-place balance edits without ledger event.

### 7.2 Required Operations
- reserve
- commit
- release (refund)

### 7.3 Idempotency
- Every mutation requires idempotency_key.
- Unique constraint on (wallet_id, operation_type, idempotency_key).
- Retries return previous result instead of duplicating charges.

### 7.4 Atomicity Pattern
Use one DB transaction for:
1. wallet row lock (FOR UPDATE)
2. funds check
3. ledger insert
4. wallet snapshot update (if used)

## 8. Database Design Essentials

Core entities:
- users
- user_profiles
- onboarding_responses
- groups
- group_members
- documents
- document_chunks
- generation_jobs
- generation_artifacts
- quizzes
- quiz_questions
- quiz_attempts
- points_wallets
- points_transactions
- promo_codes
- promo_redemptions
- invite_links
- invite_redemptions
- audit_logs

Important constraints/indexes:
- unique google_subject on users
- unique (group_id, user_id) on group_members
- unique idempotency keys for points operations
- index on document_chunks by (document_id, page)
- index on generation_jobs by (owner_id, status, created_at)
- index on audit_logs by (trace_id, created_at)

## 9. API and Contract Standards
- Version APIs under /api/v1.
- Return typed error codes, not only free-text messages.
- Propagate x-trace-id through all services and workers.
- Validate payloads with Pydantic schemas at boundaries.
- Keep provider-specific payloads behind adapters, never exposed to frontend.

## 10. AI Provider Abstraction
- Define a provider interface (chat, embeddings, image/video generation).
- Implement NVIDIA adapter now; keep optional adapters pluggable.
- Store provider model version with each generation result for auditability.

## 11. Security and Privacy
- Google OAuth only.
- RBAC roles: student, worker, teacher, admin.
- Enforce resource-level access: owner or authorized group member.
- Encrypt data in transit and at rest.
- Never log raw tokens, secrets, or personal phone numbers.

## 12. Observability and Operations
- Structured JSON logs with trace_id, user_id, route, domain, job_id.
- Metrics:
  - request latency by route
  - generation success/failure rate
  - worker queue time and processing time
  - points reserve/commit/refund failure rate
  - retrieval quality proxy metrics
- Dead-letter queue for poison jobs.
- Retry policy with exponential backoff and max attempts.

## 13. Testing Strategy (Quality Gates)

Must pass on every PR:
- backend lint/format/type/tests
- frontend lint/type/build

Critical test suites:
1. onboarding gate enforcement
2. role and scope permissions
3. points reserve/commit/refund idempotency
4. insufficient-points rejection
5. group sharing behavior
6. promo/invite anti-abuse rules
7. RAG response includes citations when context exists

## 14. Current State to Target Migration

Current backend has:
- health/db checks
- NVIDIA bridge endpoints (/api/ai/embeddings, /api/ai/chat, /api/ai/image)

Migration path:
1. Split current AI bridge into provider adapter + ai_generation service.
2. Introduce api/v1 routers and domain service layer.
3. Add onboarding and auth dependencies for generation endpoints.
4. Implement documents + rag modules and embedding jobs.
5. Add points_billing module with immutable ledger and idempotency table.
6. Move heavy generation to worker queue with durable job states.
7. Add audit_logs and trace_id propagation end to end.

## 15. Recommended Delivery Phases

### Phase 1
- Google auth + onboarding gate
- documents upload + indexing pipeline
- grounded course chat with citations
- points ledger reserve/commit/release

### Phase 2
- quiz generation with correction explanations
- groups and shared context rules
- promo codes, invite rewards, anti-abuse checks
- admin workflows for teacher bonus points

### Phase 3
- slide and video generation pipelines
- richer analytics and reliability dashboards
- extract worker-heavy AI generation into separate deployable service if needed

## 16. Toolchain Rules (Non-Negotiable)
- Frontend workflows use Bun only.
- Backend workflows use uv only.
- Do not use npm, yarn, pnpm, or pip in normal project workflows.
