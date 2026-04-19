---
name: design-component
description: Proposes a component design (button, card, modal, form, nav, table, dashboard widget, etc.) grounded in Tidwell's pattern catalog plus Refactoring UI's hierarchy/spacing/color/type rules. Auto-activates when the user says "design a component", "propose a [component] design", "how should I build a [X]", "spec a [X]", or invokes /uix:design-component. Returns pattern choice, states, spacing/type decisions, accessibility notes, and a reference implementation sketch.
argument-hint: "[component-type]"
version: 0.1.0
allowed-tools: Read, Grep
---

# design-component

Propose production-grade component designs grounded in the master guide. Auto-activates on component-design requests or via `/uix:design-component`.

## Triggers

"design a [button / card / modal / dialog / dropdown / combobox / nav / tabs / accordion / table / list / empty-state / toast / dashboard widget / form / wizard / onboarding flow / data viz]" · "how should I build a [component]" · "spec a [component]" · "what should this [component] look like" · "component for [use case]".

## Process

1. **Clarify scope in one line.** What is the component, what's its primary job, where does it live (page context), and what's the user behavior it must support? If any of these are missing, ask one concise question before proceeding.

2. **Pick the Tidwell pattern(s)** from `${CLAUDE_PLUGIN_ROOT}/references/UI_MASTER_GUIDE.md` Part X. Name them explicitly. A component is usually one primary pattern + 1–2 supporting patterns (e.g., "Card" + "Prominent Done Button" + "Good Defaults").

3. **Spec the component in this format:**
   ```
   ## <Component Name>

   ### Purpose
   One sentence: what user goal this serves.

   ### Pattern(s)
   - <Tidwell pattern> — why it fits
   - <supporting pattern> — what it adds

   ### States
   default · hover · focus · active · disabled · loading · error · empty · success (only those that apply).

   ### Hierarchy
   Primary action · secondary · tertiary · destructive (with confirmation). How each is expressed (weight + color, not size) `[RUI]`.

   ### Spacing & size
   Padding, gap, target size. Must hit WCAG 2.5.8 (≥24×24 CSS px; prefer 44×44) `[WCAG]`.

   ### Type
   Role, weight, size, line-height. From a modular scale `[RUI]`.

   ### Color
   Base, hover, focus-ring, disabled, error — referencing the project's palette (not hex invented on the spot) `[RUI]`.

   ### Accessibility
   Keyboard interaction · focus ring ≥3:1 contrast and not obscured (WCAG 2.4.7, 2.4.11) · aria-role / aria-state · label · announce changes via role="status" if needed.

   ### Anti-patterns to avoid
   - ...
   - ...

   ### Reference implementation sketch
   Minimal HTML/JSX + Tailwind (or plain CSS) showing the structure. No invented design tokens — reference the project's system.
   ```

4. **Ground every decision in a source tag.** `[RUI]`, `[DI]`, `[DMMT]`, `[WCAG]`, etc.

5. **Default to conservative, accessible, reusable.** Do not invent novel interactions when a proven Tidwell pattern exists.

6. **If the user provides code or a screenshot**, first critique (what pattern is current, what breaks), then propose the new spec.

## Ground rules

- Never use size alone for hierarchy — always pair with weight or color `[RUI]`.
- Every interactive element must be keyboard-reachable with a visible focus indicator `[WCAG 2.1.1, 2.4.7]`.
- No color-only semantics (error, success) — always paired with icon or text `[WCAG 1.4.1]`.
- Tap targets ≥24×24 CSS px minimum, 44×44 recommended `[WCAG 2.5.8]`.
- Drag-only interactions must have a click alternative `[WCAG 2.5.7]`.
- Reflow at 320 px wide; no horizontal scroll `[WCAG 1.4.10]`.
- Don't hallucinate framework conventions — produce generic, adaptable markup unless the user's stack is known.

## Output

A crisp spec in the format above, followed by one sentence recommending the next action (test-with-users, iterate-on-states, or ship-to-review).
