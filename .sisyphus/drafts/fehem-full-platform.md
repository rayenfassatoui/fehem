# Draft: Fehem Educational Platform - Full Implementation

## Current State (from exploration)

### What EXISTS:
- **Frontend**: Next.js 16 + React 19 + TypeScript + Tailwind + shadcn/ui (Bun toolchain)
- **Backend**: FastAPI + asyncpg + pgvector (uv toolchain)
- **Infrastructure**: Docker compose, PostgreSQL with pgvector
- **AI Bridge**: NVIDIA endpoints for chat, embeddings, image (NO auth/billing yet)
- **Docs**: Full product rules and architecture specs exist

### What's MISSING (needs to be built):
- Authentication (Google OAuth)
- Onboarding flow (multi-step form)
- User/profile management
- Points/credits system
- Document upload & PDF processing
- AI generation features (video, presentation, quiz)
- Group collaboration
- Real-time chat
- Admin panel

---

## Requirements (from user - Tunisian Arabic translated)

### 1. User Types (Roles)
- **Student (telmidh/etudient)**: Studies at lycée or university
- **Worker (yekhdem)**: Has a job/profession
- **Professor (ostedh)**: Teaches at lycée or university

### 2. Onboarding Flow (MANDATORY before account creation)
**Step 1**: Google OAuth login (NO email/password option)
**Step 2**: Personal info
  - Name, Surname
  - Role selection (Student/Worker/Professor)

**Step 3**: Role-specific info
  - **If Student**: Where do you study? (which fac or lycée?)
  - **If Worker**: What do you do for work?
  - **If Professor**: What subject do you teach? Where (fac/lycée)?

**Step 4**: Common info
  - Country (bled)
  - Phone number

**Step 5**: Usage intent
  - Personal learning
  - Create & sell courses
  - Support class/group learning

### 3. Core Features (after onboarding)
- **PDF Upload**: User uploads course PDFs
- **AI Presentation**: Generate slides from PDF content
- **AI Video**: Generate video explanations of courses
- **AI Chat**: Conversational Q&A about uploaded courses
- **AI Quiz**: Generate QCM questions from PDF, with corrections

### 4. Points System (credits)
- **Daily Limits**: 3-4 free generations (video/presentation) per day
- **Earn Points**:
  - Invite friends via special link
  - Use promo codes
  - Share with friends (transfers)
- **Spend Points**:
  - Extra video generations
  - Extra slide generations beyond limit
  - Premium features

### 5. Groups Feature
- Create groups, invite friends
- Group chat with AI integration
- Share PDFs within group
- Generate content from group PDFs
- **Point modes**:
  - Payer-only: Person who generates pays from their points
  - Pooled: Everyone shares points for generation

### 6. Quiz Sharing
- Generate quiz from PDFs
- Share quiz in groups
- AI corrects answers with explanations from source PDF

### 7. Professor-Specific Features
- "Contact Admin" button in profile
- Bonus points for creating class quizzes
- Can create quizzes for their class groups

---

## Technical Decisions (confirmed)

- **Auth**: Google OAuth only (per existing docs)
- **Backend**: FastAPI + uv (per existing docs)
- **Frontend**: Next.js + Bun (per existing docs)
- **Database**: PostgreSQL + pgvector (per existing docs)
- **AI Provider**: NVIDIA APIs (existing bridge)

---

## Decisions Made (User Confirmed)

### Scope: FULL - Everything in ONE plan
- All features go into a single comprehensive plan
- Will be 40-50+ tasks organized in parallel waves

### Video Generation: SKIP
- No video generation feature in this scope
- Focus on: PDF upload, AI chat, presentation slides, quiz

### Real-time Chat: WebSockets
- Full real-time experience for group chat
- AI integrated into group conversations

### Testing: TDD Style
- Write tests first, then implement
- Every task includes test cases

### Points Economics: Generous
- **Starting balance**: 50 points for new users
- **Daily free generations**: 3 per day
- **Invite reward**: 20 points per successful invite
- **Promo codes**: Admin-configurable amounts

### Admin Panel: Full
- Manage promo codes (create, disable, view redemptions)
- Review teacher bonus requests
- User management and analytics
- Points ledger and adjustments

---

## Research Findings

### From Codebase Exploration:
- Basic AI endpoints exist but need auth/billing guards
- Architecture docs define 3 delivery phases
- Existing: health checks, NVIDIA AI bridge (chat, embeddings, image)

### From Librarian Research (AI APIs & Patterns):

**Conversational AI:**
- GPT-4o-mini recommended for cost-effective Q&A
- Claude for RAG with long documents (200K context)
- NVIDIA endpoints already integrated - can use those

**Presentation Generation:**
- SlidesAI for Google Slides integration
- 2Slides API for programmatic generation
- Can build custom with AI + template system

**Points System Patterns:**
- Pessimistic locking for balance checks
- Atomic reserve → commit → refund pattern
- Idempotency keys for all mutations
- Immutable ledger for audit trail

**Google OAuth:**
- NextAuth.js v5 recommended
- Zero-config, production-ready
- Already supports Google provider

---

## Scope Boundaries (CONFIRMED)

### INCLUDE:
- Google OAuth authentication
- Multi-step onboarding flow (role-specific)
- User profiles and role management
- PDF upload and processing pipeline
- Document chunking + embeddings (pgvector)
- AI Chat with course context (RAG)
- AI Presentation/Slide generation
- AI Quiz generation (QCM) with corrections
- Points system (wallet, ledger, transactions)
- Daily limits and quota enforcement
- Invite links with rewards
- Promo codes
- Groups with shared PDFs
- Real-time group chat (WebSockets) with AI
- Quiz sharing in groups
- Group point modes (payer-only vs pooled)
- Professor features (contact admin, bonus points)
- Full admin panel

### EXCLUDE:
- Video generation (deferred to future)
- Payment integration (use points only for now)
- Mobile app
- Email notifications (can add later)
- Advanced analytics dashboards
- Multi-language support
