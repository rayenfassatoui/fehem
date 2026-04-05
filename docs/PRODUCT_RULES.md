# Fehem Product Rules

## 1. Core User Types
- Student
- Professional worker
- Teacher/Professor

## 2. Authentication Rules
- Google OAuth is the only login method.
- No email/password registration.
- One active account per Google identity.

## 3. Onboarding Rules (Required)
Onboarding must be completed before user can use AI generation features.

### Common required fields
- First name
- Last name
- Country
- Phone number (validated format)
- Main usage intent:
  - personal learning
  - create and sell courses
  - support class/group learning

### Role-specific fields
- Student:
  - education level and institution (school/lycee/fac)
- Professional worker:
  - work domain/industry
- Teacher/Professor:
  - taught subject
  - institution (school/lycee/fac)

## 4. Content Upload Rules
- Users can upload PDFs.
- Uploaded documents are associated with an owner and optional group.
- Parsed text and embeddings are generated asynchronously.
- Failed parsing jobs must expose actionable error state.

## 5. AI Features Rules
- AI presentation generation from one or more PDFs.
- AI video explanation generation from course PDF context.
- Course chat assistant grounded in uploaded content.
- AI-generated quizzes (MCQ/QCM) from PDF content.
- Quiz correction and explanation must reference source content when available.

## 6. Points and Quota Rules
- Every generation action consumes points.
- Daily free quota exists (example target: 3-4 generation actions/day/user).
- If points are insufficient, generation must fail with explicit error reason.
- Point deduction happens before job execution and is idempotent.

## 7. Points Earning Rules
- Invite links can grant reward points after anti-fraud checks.
- Promo codes can add points if valid and not already redeemed by the user.
- Direct user-to-user point transfer is optional and must be rate-limited.

## 8. Group Collaboration Rules
- Users can create or join groups.
- Groups support:
  - shared PDF context
  - real-time group chat with AI
  - shared quizzes
- Group point model options:
  - payer-only mode (action initiator pays)
  - pooled mode (group wallet pays)
- Mode must be visible to all members and auditable.

## 9. Teacher Bonus Rules
- Teacher profile includes a request flow to contact admin.
- Approved teachers can receive bonus points for class quiz generation.
- Bonus grants must be traceable and revocable by admin.

## 10. Anti-Abuse Rules
- Rate-limit generation endpoints and invite/promo operations.
- Detect duplicate invite abuse and suspicious redemption patterns.
- Add moderation and policy checks for generated content.
- Keep immutable ledger for points transactions.

## 11. Minimal Admin Rules
- Manage promo codes
- Review teacher bonus requests
- Monitor usage, failures, and abuse flags
- View points ledger and adjust points with reason logs
