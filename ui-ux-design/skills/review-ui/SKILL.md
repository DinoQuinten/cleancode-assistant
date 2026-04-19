---
name: review-ui
description: Reviews an existing UI (file, URL, screenshot, code, or description) against the full UI_MASTER_GUIDE.md — hierarchy, spacing, typography, color, depth, forms, patterns, mobile, copy, and WCAG 2.2 accessibility. Auto-activates on "review my UI", "critique this design", "audit this page", "is this design good", "what's wrong with this screen", or /uix:review-ui. Produces a categorized findings list with severity, source citations, and fix recommendations.
argument-hint: "[file, URL, or description]"
version: 0.1.0
allowed-tools: Read, Grep, Glob
---

# review-ui

Conduct rigorous UI reviews against the master guide. Auto-activates on UI-review requests or via `/uix:review-ui`.

## Triggers

"review my UI / design / component / page / screen" · "critique this" · "audit this" · "is this design good" · "what's wrong with this screen" · "does this follow best practices" · "grade my UI".

## Process

1. **Ingest the target.** File path → Read. URL → ask the user for a screenshot or rendered HTML (don't fetch live unless explicitly asked). Screenshot provided → analyze visually. Description only → treat as a verbal spec, note assumptions.

2. **Load the checklist** from `${CLAUDE_PLUGIN_ROOT}/references/UI_MASTER_GUIDE.md` Part XIV (60-second pre-ship checklist). Work through each category.

3. **Evaluate along these axes** (skip sections that don't apply):
   - **Clarity & scannability** `[DMMT]`
   - **Visual hierarchy** (weight+color, not size alone) `[RUI]`
   - **Spacing & layout** (fixed scale, breathing room, grid discipline) `[RUI]`
   - **Typography** (scale, line length, line-height, baseline alignment) `[RUI]`
   - **Color** (systemic palette, value contrast, color-only meaning) `[RUI][IOC]`
   - **Depth & shadows** (tinted shadows, consistent light source) `[RUI][C&L]`
   - **Forms** (labels visible, errors actionable, progressive disclosure) `[DI][DMMT]`
   - **Navigation & IA** (persistent nav, breadcrumbs, escape hatches) `[DMMT][DI]`
   - **Pattern choice** — is the right Tidwell pattern being used? `[DI]`
   - **Mobile** (target sizes, thumb zones, reflow) `[DI][WCAG]`
   - **Content & copy** (jargon, happy talk, action-oriented) `[DMMT][UXB]`
   - **Accessibility (WCAG 2.2 AA)** — delegate deep check to `accessibility-audit` skill if issues are dense.

4. **Output format:**
   ```
   ## UI Review — <target>

   ### Summary
   One-paragraph verdict. Top 3 priorities.

   ### Critical (must fix before ship)
   - [Category] **Issue** — Why it fails · Source · Fix.

   ### Warnings (should fix)
   - [Category] ...

   ### Suggestions (nice-to-have)
   - [Category] ...

   ### Strengths
   - What the design already does well — keep these.

   ### Next steps
   - 2-3 concrete next actions.
   ```

5. **Assign severity honestly:**
   - **Critical** — broken experience, WCAG AA failure, lost conversions, broken keyboard path.
   - **Warning** — violates a named principle; slows users; brittle at scale.
   - **Suggestion** — polish, edge-case, or style preference.

6. **Every finding must cite a source tag** — no unsourced opinions.

## Ground rules

- Critique the design, not the designer. No sarcasm.
- Name strengths too — reviews that are only negative lose signal.
- If the design violates a WCAG 2.2 AA criterion, that's Critical, not Warning.
- If you're unsure (e.g., only have a screenshot), say so and list which axes you couldn't evaluate.
- When multiple issues share a root cause, group them — don't pad the list.
- Suggest a *specific* fix, not just "improve hierarchy".

## Handoffs

- Accessibility-deep → `accessibility-audit` skill.
- Needs a new component design → `design-component` skill.
- Needs pattern selection → `choose-pattern` skill.
- Color-system problems → `color-system` skill.
