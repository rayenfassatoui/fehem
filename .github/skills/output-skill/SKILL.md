---
name: fehem-output-skill
description: "Use when: the user needs full, production-ready output with no placeholders, no skipped sections, and no partial implementations."
---

# Fehem Output Skill

## Mission
Deliver complete, runnable output for the exact requested scope.

## Non-Negotiable Rules
1. No placeholder comments in generated code.
2. No omitted middle sections in long files.
3. No "continue later" behavior unless a hard token limit is reached.
4. No vague pseudo-code where concrete implementation is expected.

## Delivery Process
1. Count deliverables (files, functions, routes, tests).
2. Implement all deliverables completely.
3. Validate syntax and consistency.
4. Confirm all requested items are present.

## If Output Must Be Split
Use an explicit progress line:
`[PAUSED - X of Y complete. Continue from: <next-file-or-section>]`