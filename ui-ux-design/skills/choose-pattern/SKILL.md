---
name: choose-pattern
description: Recommends the right UI pattern from Tidwell's "Designing Interfaces" catalog for a given interaction problem — navigation, layout, lists/data, forms, controls, mobile. Auto-activates on "what pattern should I use for X", "how do I let users [do Y]", "what's the best way to show [Z]", or /uix:choose-pattern. Returns primary pattern, 1-2 alternatives, and why each fits or doesn't.
argument-hint: "[interaction or problem]"
version: 0.1.0
allowed-tools: Read, Grep
---

# choose-pattern

Advise on Tidwell-pattern selection. Auto-activates on pattern-selection questions or via `/uix:choose-pattern`.

## Triggers

"what pattern should I use for [X]" · "how do I let users [do Y]" · "what's the best way to show [Z]" · "should I use a modal / tabs / accordion / wizard / dropdown / carousel for this" · "pattern for [navigation / filtering / comparing / multi-step task / large list]".

## Process

1. **Clarify the interaction problem in one sentence.** Focus on the user's goal, not the UI element. "User needs to compare 5 items side by side" is better than "I need a table."

2. **Identify the category** from `${CLAUDE_PLUGIN_ROOT}/references/UI_MASTER_GUIDE.md` Part X:
   - Page / IA · Navigation · Layout · Lists & Data · Forms & Input · Controls & Actions · Mobile

3. **Recommend one primary pattern + up to two alternatives.** Format:
   ```
   ## Pattern recommendation — <problem>

   ### Primary: <PatternName>
   **What it is:** one-line definition.
   **Why it fits:** maps to the user behavior at stake (safe exploration / satisficing / incremental construction / etc.).
   **When it wins:** specific conditions under which this beats alternatives.

   ### Alternatives
   - **<AlternativePattern>** — fits when [X]; weaker here because [Y].
   - **<AlternativePattern>** — fits when [X]; weaker here because [Y].

   ### Anti-patterns (avoid)
   - <AntiPattern> — why it fails.

   ### Implementation notes
   - 2-4 bullets: states, accessibility, mobile adaptation, known pitfalls.

   ### Next step
   If you want a full component spec, use `design-component` with this pattern.
   ```

4. **Always name the user behavior** the pattern serves (Tidwell's palette — see master guide Part III).

5. **If the user's problem doesn't map cleanly to a single Tidwell pattern**, propose a composite: e.g., "Two-Panel Selector + Cards + Dynamic Queries" and justify each.

6. **If the user is asking about a pattern they already chose** (e.g., "should I use a modal?"), evaluate their choice honestly. Often the right answer is "no, use X instead because Y."

## Ground rules

- Never invent patterns. If no Tidwell pattern fits, say so and name the closest analogs.
- Default to conservative, well-known patterns. Innovation here rarely pays `[DMMT]`.
- Flag patterns that break on mobile or keyboard-only and suggest adaptations.
- Carousels are usually wrong — say so when the user proposes one, unless there's a real linear-sequence reason `[RUI][DI]`.
- Modals are often overused — say so when the user proposes one for non-blocking content `[DI]`.

## Reference

Full pattern catalog in `${CLAUDE_PLUGIN_ROOT}/references/UI_MASTER_GUIDE.md` Part X. User-behavior palette in Part III.
