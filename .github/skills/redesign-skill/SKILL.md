---
name: fehem-redesign-skill
description: "Use when: improving existing frontend screens; run an audit first, then ship targeted upgrades with low regression risk."
---

# Fehem Redesign Skill

## Goal
Upgrade existing UI without breaking behavior, API contracts, or product constraints.

## Workflow
1. Audit current screen before editing.
2. List issues by severity: usability, hierarchy, spacing, responsiveness, accessibility.
3. Preserve functional behavior and data flow.
4. Apply focused visual and structural improvements.
5. Re-check loading, empty, and error states after redesign.

## Hard Constraints
1. Do not move business logic into UI rendering files.
2. Keep existing routes and public interfaces stable unless required.
3. Respect onboarding, role, and points constraints from workspace rules.
4. Do not introduce new libraries unless necessary.

## Audit Output Format
1. Findings by severity
2. Proposed changes
3. Regression risks
4. Verification checklist