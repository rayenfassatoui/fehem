# Fehem Engineering Rules (Workspace)

## Mission
Build Fehem as a reliable AI-learning platform for students, professionals, and teachers, with strong product quality, privacy, and cost control.

## Mandatory Toolchain
- Frontend runtime and package manager: Bun only.
- Backend dependency and environment manager: uv only.
- Do not use npm, yarn, pnpm, or pip for project workflows.

## Standard Commands
### Frontend (Bun)
- Install: `bun install`
- Dev: `bun run dev`
- Build: `bun run build`
- Typecheck: `bun run typecheck`
- Lint: `bun run lint`

### Backend (uv)
- Create env: `uv venv`
- Sync deps: `uv sync`
- Run API: `uv run <command>`
- Tests: `uv run pytest`
- Lint/format: `uv run ruff check .` and `uv run ruff format .`

## Architecture Rules
- Use modular monolith first, with clean boundaries by domain:
  - auth
  - onboarding
  - documents
  - ai-generation
  - quiz
  - groups
  - points-billing
  - notifications
  - admin
- Use async jobs for heavy AI tasks (video generation, long slide generation, bulk quiz generation).
- Store generated artifacts and job logs with trace IDs.
- Every AI operation must be auditable.

## AI and Embeddings Rules
- RAG required for course chat and quiz grounding.
- No answer should claim facts that are not present in indexed course content unless clearly marked as external/general knowledge.
- Embeddings pipeline must include:
  - PDF parse
  - chunking
  - metadata tagging (owner, group, language, page, upload_id)
  - embedding generation
  - vector index upsert
- Include source citation payload in AI responses when possible.

## Security and Privacy Rules
- Login provider: Google OAuth only.
- No email/password auth.
- Enforce role-based authorization for teacher/admin capabilities.
- Encrypt sensitive data in transit and at rest.
- Never log raw secrets, tokens, or personal phone numbers.

## Quality Gates
- Every PR must pass lint, typecheck, tests, and build.
- Add tests for critical rules:
  - points deduction
  - role permissions
  - quota enforcement
  - group sharing behavior
  - onboarding completion checks

## Product Constraints
- A user cannot access generation features before onboarding completion.
- Points must be checked before generation starts.
- All point mutations must be atomic and idempotent.
- Support promo codes, invite rewards, and teacher bonus points with abuse protections.

## Coding Style
- Prefer explicit domain services over fat controllers/routes.
- Keep business logic out of UI components.
- Use typed contracts for API payloads.
- Add concise docstrings for non-obvious logic.

## Installed Skills
- Workspace skills are available under `.github/skills`.
- For new frontend UI work, combine `taste-skill` with one visual mode:
  - `soft-skill`
  - `minimalist-skill`
  - `brutalist-skill`
- For upgrading existing screens, use `redesign-skill` first.
- For guaranteed complete implementations, use `output-skill`.
- For Google Stitch design-system exports, use `stitch-skill`.

## Skill Priority
- Domain and platform rules in this file always come first.
- Security, onboarding gate, points atomicity, and RAG grounding are non-negotiable.
- Style skills may change visuals, but cannot break product constraints.
