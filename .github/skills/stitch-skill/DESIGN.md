# Design System: Fehem

## 1. Visual Theme and Atmosphere
Fehem should feel trustworthy, modern, and learning-focused.
The interface is clean and professional, with enough warmth to support students and teachers.

## 2. Color Palette and Roles
- Canvas: #F8FAFC
- Surface: #FFFFFF
- Text Primary: #0F172A
- Text Secondary: #475569
- Border: #E2E8F0
- Accent (single): #0EA5A4

Rules:
- Use one accent color only.
- Keep strong text contrast.
- Avoid neon glow aesthetics.

## 3. Typography System
- Headings: strong sans-serif hierarchy, tight tracking for titles.
- Body: readable and calm line-height.
- Mono: only for numbers, IDs, or technical metadata.

## 4. Component Behavior Rules
- Buttons: clear primary/secondary distinction, tactile active feedback.
- Inputs: label above field, errors below field.
- Cards: use only when elevation has meaning.
- States: provide loading, empty, success, and error patterns.

## 5. Layout and Responsive Rules
- Use grid-based responsive layout.
- Collapse to single-column on small devices.
- Avoid horizontal overflow.
- Keep content in readable max-width containers.

## 6. Motion Philosophy
- Subtle motion with transform/opacity only.
- Short easing curves, no distracting effects.
- Staggered reveal allowed for lists and dashboards.

## 7. Banned Patterns
- No generic template-looking hero sections.
- No visual overload with multiple competing accents.
- No inaccessible contrast or hidden focus states.
- No placeholder content in production screens.