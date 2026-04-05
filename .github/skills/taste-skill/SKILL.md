---
name: fehem-taste-skill
description: "Use when: building new frontend pages/components with intentional visual direction, modern motion, and production-ready polish."
---

# Fehem Taste Skill

## Goal
Build frontend UI that feels intentional, memorable, and clean while staying practical for production.

## Stack Assumptions
- Next.js App Router + TypeScript
- Tailwind CSS v4
- shadcn-style component primitives
- Existing design tokens from `app/globals.css`

## Creative Dials
- `DESIGN_VARIANCE`: 7
- `MOTION_INTENSITY`: 5
- `VISUAL_DENSITY`: 5

Adjust dials from 1 to 10 when the user asks for a different vibe.

## Core Rules
1. Avoid generic hero + three-card layouts unless explicitly requested.
2. Choose a clear visual direction before coding (grid rhythm, type scale, accent strategy).
3. Use one primary accent color and keep neutral surfaces consistent.
4. Respect mobile first behavior; all complex layouts collapse cleanly below `md`.
5. Never animate layout with `top/left/width/height`; animate with `transform` and `opacity`.
6. Include complete UI states for meaningful features: loading, empty, success, and error.
7. Keep accessibility baseline: visible focus states, keyboard support, and good contrast.

## Implementation Standards
1. Verify dependency existence in `package.json` before using third-party libraries.
2. If a package is missing, propose install commands with Bun only (`bun add` or `bun add -d`).
3. Keep business logic out of presentational components.
4. Prefer composable sections and reusable local components over one giant page file.

## Preflight Checklist
- Is the layout distinct enough to avoid template lookalikes?
- Does the page work on mobile without horizontal overflow?
- Are motion effects subtle, meaningful, and performant?
- Are all required states implemented?
- Are imports and dependencies valid for this repository?