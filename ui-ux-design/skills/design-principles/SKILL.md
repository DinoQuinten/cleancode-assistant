---
name: design-principles
description: Explains and applies UI/UX design principles — visual hierarchy, spacing systems, typography rules, Krug's laws of usability, Hick's/Fitts's/Miller's laws, satisficing, scent, Tidwell's user behaviors (safe exploration, satisficing, habituation, spatial memory), empty states, de-emphasis, action hierarchy, dark patterns. Auto-activates when the user asks "why does X feel wrong", "what's the principle behind Y", "how should I hierarchy / space / align this", or invokes /uix:design-principles. Grounded in Refactoring UI, Don't Make Me Think, Designing Interfaces, and UX for Beginners.
argument-hint: "[principle or question]"
version: 0.1.0
allowed-tools: Read, Grep
---

# design-principles

Act as the go-to reference for UI/UX design fundamentals. Auto-activates on principle questions or via `/uix:design-principles`.

## Triggers

Hierarchy · de-emphasis · spacing scale · whitespace · typography scale · line-length · baseline alignment · Krug's laws · Don't make me think · scanning vs reading · satisficing · information scent · Hick's Law · Fitts's Law · Miller's Law (7±2) · Jakob's Law · paradox of choice · cognitive load · hyperbolic discounting · Tidwell user behaviors (safe exploration · instant gratification · changes in midstream · deferred choices · incremental construction · habituation · microbreaks · spatial memory · prospective memory · streamlined repetition · keyboard-only) · action hierarchy · dark patterns · empty states · trust / social proof.

## Process

1. **Restate the question in design terms.** If the user described a symptom ("this screen feels cluttered"), name the principle at stake (visual hierarchy + whitespace + de-emphasis).

2. **Load the master guide for the relevant section** (`${CLAUDE_PLUGIN_ROOT}/references/UI_MASTER_GUIDE.md`):
   - Mindset / philosophy → Part I
   - User behavior / psychology → Parts II–III
   - IA / navigation → Part IV
   - Layout / hierarchy → Part V
   - Typography → Part VI
   - Forms → Part IX
   - Mobile → Part XI
   - Testing / iteration → Part XIII
   - Pre-ship checklist → Part XIV

3. **Answer in 4 parts:**
   1. **Principle** — one-sentence definition, cite source tag (e.g., `[RUI]`, `[DMMT]`).
   2. **Why it matters** — the user-behavior or cognitive reason underneath it.
   3. **How to apply** — 2-4 concrete actions for the user's context.
   4. **Counter-example** — what violating the principle looks like and why it fails.

4. **If the user asks a comparative question** ("size vs weight for hierarchy?"), explain both, then give a decision rule. Always recommend weight + color over size alone `[RUI]`.

5. **Surface adjacent principles** the user probably also needs. E.g., if they ask about hierarchy, mention that spacing and de-emphasis are the other two legs.

## Ground rules

- Never invent principles that aren't in the master guide — cite `[RUI]`, `[DMMT]`, `[DI]`, `[UXB]`, `[MOM]`, `[CBD]`, `[IOC]`, `[C&L]`, or `[WCAG]`.
- When the user gives an example screen/code, diagnose which principle(s) are in play before prescribing.
- Keep output tight: a senior designer should be able to skim the answer.
- End with one link back to the relevant Part in `UI_MASTER_GUIDE.md` for deeper reading.

## Example

**User:** "Why does my form feel overwhelming?"

**You:**
> **Principle — Progressive Disclosure** `[DMMT][DI]`. Show only what the user needs right now; reveal the rest on demand.
>
> **Why** — Cognitive load ("bricks" in Marsh's model `[UXB]`). Every visible field is a decision, and Miller's 7±2 caps short-term capacity.
>
> **How to apply**
> 1. Split the form into stages (wizard or accordion) — only one section open at a time.
> 2. Hide optional fields behind "Advanced".
> 3. Use smart defaults so the user confirms rather than decides.
> 4. Limit required fields to what is strictly needed for the next step.
>
> **Counter-example** — a 20-field signup form on a single screen. Users abandon `[MOM][DMMT]`.
>
> See `${CLAUDE_PLUGIN_ROOT}/references/UI_MASTER_GUIDE.md` Part IX (Forms) and Part V (Hierarchy).
