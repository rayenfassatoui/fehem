# Fehem

Fehem is an AI-powered learning platform for students, professionals, and teachers.
It helps users upload course PDFs and use AI for:
- grounded course chat
- embeddings-based retrieval
- quiz generation
- presentation and video generation workflows (planned and partially scaffolded)

## Current Status

This repository currently contains:
- a Next.js frontend (Bun toolchain)
- a FastAPI backend (uv toolchain)
- Neon PostgreSQL connectivity checks
- NVIDIA AI bridge endpoints for embeddings, chat, and image generation

## Product Vision (Short)

Fehem focuses on:
- Google-only authentication
- mandatory onboarding before generation features
- points/quota system for AI actions
- group collaboration and shared learning context
- teacher workflows and admin controls

Detailed product and architecture specs are available in:
- `docs/PRODUCT_RULES.md`
- `docs/AI_ARCHITECTURE.md`

## Mandatory Toolchain

- Frontend: Bun only
- Backend: uv only
- Do not use npm/yarn/pnpm/pip in normal project workflows

## Prerequisites

- Bun `>= 1.3`
- Python `>= 3.12`
- uv installed on your machine

## Environment Setup

### 1. Backend environment

Create or update `backend/.env` from `backend/.env.example`.

Required variables:
- `DATABASE_URL` (Neon PostgreSQL URL)
- `FRONTEND_ORIGIN` (usually `http://localhost:3000`)
- `NVIDIA_API_KEY` (required for NVIDIA AI endpoints)

Optional model/endpoints are preconfigured:
- `NVIDIA_OPENAI_BASE_URL`
- `NVIDIA_EMBEDDING_MODEL`
- `NVIDIA_CHAT_MODEL`
- `NVIDIA_IMAGE_ENDPOINT`

### 2. Frontend environment

Create `frontend/.env.local` and set:

```bash
NEXT_PUBLIC_BACKEND_URL=http://127.0.0.1:8000
```

## Install and Run

### Terminal 1: Backend (uv)

```bash
cd backend
uv venv
uv sync --group dev
uv run uvicorn app.main:app --app-dir src --host 127.0.0.1 --port 8000 --reload
```

Backend runs on `http://127.0.0.1:8000`.

### Terminal 2: Frontend (Bun)

```bash
cd frontend
bun install
bun run dev
```

Frontend runs on `http://localhost:3000`.

## Docker Setup (Frontend + Backend + PostgreSQL pgvector)

The repository now includes:
- `docker-compose.yml`
- `.env.docker.example`
- `backend/Dockerfile`
- `frontend/Dockerfile`
- `frontend/Dockerfile.prod`
- `docker/postgres/init/01-enable-pgvector.sql`

Docker stack profiles:
- `dev`: local development containers
- `production`: hardened runtime profile for deployment-like runs

Dedicated Docker env file:
- `.env.docker` is loaded by backend/frontend services (optional but recommended).
- Use `.env.docker.example` as reference.
- Keep real secrets only in `.env.docker` (already ignored by git).
- `DATABASE_URL` can be set in `.env.docker`; if omitted, Docker falls back to `postgresql://fehem:fehem@postgres:5432/fehem`.

### Start Dev Profile

```bash
docker compose --profile dev up --build -d
```

### Start Production Profile

```bash
docker compose --profile production up --build -d
```

### Check service status

```bash
docker compose ps
docker compose logs -f backend
```

### Stop and clean

```bash
docker compose down
```

To remove database volume too:

```bash
docker compose down -v
```

### Service URLs

- frontend: `http://localhost:3000`
- backend: `http://localhost:8000`
- postgres (pgvector enabled): `localhost:5432`

### Verify frontend/backend communication

```bash
cd frontend
bun run test:backend-connection
bun run test:ai-bridge
bun run test:semantic-search
```

Expected behavior:
- `test:backend-connection` passes when backend and database are both reachable.
- `test:ai-bridge` returns either:
  - `200` when `NVIDIA_API_KEY` is configured
  - `503` when NVIDIA key is not configured yet (backend bridge still reachable)
- `test:semantic-search` validates pgvector upsert + nearest-neighbor search through backend API.

## Test and Quality Commands

### Backend

```bash
cd backend
uv run pytest -q
uv run ruff check .
```

### Frontend

```bash
cd frontend
bun run typecheck
bun run lint
bun run build
```

### Integration checks from frontend

```bash
cd frontend
bun run test:backend-connection
bun run test:ai-bridge
bun run test:semantic-search
```

What these scripts verify:
- `test:backend-connection`: frontend can call `/api/health` and `/api/db-check`
- `test:ai-bridge`: frontend can call backend `/api/ai/chat` and receive either:
  - `200` when NVIDIA key/provider is ready
  - `503` when `NVIDIA_API_KEY` is not configured yet
- `test:semantic-search`: frontend can upsert and search vectors via backend pgvector endpoints

## API Endpoints (Current)

### Core health
- `GET /api/health`
- `GET /api/db-check`

### NVIDIA AI bridge
- `POST /api/ai/embeddings`
- `POST /api/ai/chat`
- `POST /api/ai/image`

### Semantic Search (pgvector)
- `POST /api/ai/semantic-documents`
- `POST /api/ai/semantic-search`

Example:

```bash
curl -X POST http://127.0.0.1:8000/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Say hello from Fehem","max_tokens":64}'
```

Semantic example:

```bash
curl -X POST http://127.0.0.1:8000/api/ai/semantic-documents \
  -H "Content-Type: application/json" \
  -d '{"id":"chunk-1","content":"Fehem helps with AI learning","embedding":[0.11,0.22,0.33],"metadata":{"topic":"intro"}}'

curl -X POST http://127.0.0.1:8000/api/ai/semantic-search \
  -H "Content-Type: application/json" \
  -d '{"query_embedding":[0.11,0.22,0.33],"top_k":3}'
```

## Repository Structure

```text
fehem/
  backend/
    src/app/
      main.py
      db.py
      ai_routes.py
      ai_schemas.py
      nvidia_ai.py
    tests/
    pyproject.toml
  frontend/
    app/
    components/
    scripts/
    package.json
  docs/
    PRODUCT_RULES.md
    AI_ARCHITECTURE.md
  .github/
    copilot-instructions.md
    skills/
```

## Security Notes

- Do not commit real secrets (API keys, tokens, private URLs).
- Keep `backend/.env` local only.
- Use role-based access and audit rules as specified in project docs.

## Next Recommended Steps

1. Build onboarding/auth modules (Google OAuth only).
2. Implement document parsing + chunking + embeddings indexing pipeline.
3. Add points ledger tables and atomic mutation service.
4. Add async workers for heavy generation jobs.
5. Add end-to-end tests for onboarding gates and points enforcement.
