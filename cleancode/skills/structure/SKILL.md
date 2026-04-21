---
name: structure
description: This skill should be used when the user asks to "suggest a better structure", "apply a design pattern", "this switch is too big", "simplify this class", "apply strategy pattern", "apply command pattern", "apply factory pattern", "fix this structure", "replace switch with polymorphism", or mentions restructuring a class or giant switch statement. Detects and optionally applies well-known design patterns (Strategy, Command, Factory, State) from OOP vs. Functional Programming.
argument-hint: "[path, default: whole project] [fix]"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
version: 0.3.0
---

# Clean Code Structure

Spot places where a well-known structural pattern would help, name it in plain language, and optionally apply it. Patterns are drawn from the OOP vs. Functional Programming material plus Code Complete Ch. 18.

## When This Runs

- User asks to suggest a better structure or apply a design pattern
- User mentions a big switch, a class that does too many things, or repeated construction logic
- `/cleancode:fix` delegates structural rewrites to this skill

## Default Scope: whole codebase

No path given → scan the whole project for pattern candidates (see `../../SCOPE_POLICY.md`). Pass a file or folder to narrow.

## Modes

| Invocation | Behavior |
|---|---|
| `/cleancode:structure` | **Report across whole project (default)** — rank candidate files by pattern fit |
| `/cleancode:structure <path>` | Report only on the given file or folder |
| `/cleancode:structure <path> fix` | Show the rewrite plan for that path, then apply |
| `/cleancode:structure .` | Explicit whole-project (same as the no-arg default) |

Default is **report mode** for writes. Structural rewrites are large — project-wide `fix` is intentionally not offered; narrow to a file first. Default scope is **whole codebase** unless a path is given in the command or in the current user message.

## Patterns This Skill Knows

### 1. Big switch / if-else chain → Strategy pattern

**Signal:**
- A `switch` with > 4 cases, each executing non-trivial logic (not just returning a constant).
- An `if/else if/else if` chain with > 3 branches doing different behaviors.

**Plain-language explanation:** *"You're choosing one of several different behaviors based on a type or flag. Put each behavior in its own small class, pick the right one at runtime from a lookup table. Adding a new behavior becomes adding a new class instead of editing the switch."*

### 2. Repeated do-something-then-remember → Command pattern

**Signal:**
- Methods that both perform an action AND store it for later (for undo, audit log, retry, queue).
- A function that executes something, then pushes to a history list, then returns — pattern appears 3+ times.

**Plain-language explanation:** *"You're doing operations that also need to be remembered. Wrap each operation in a small object with an `execute()` method — now you can queue them, replay them, or undo them uniformly."*

### 3. Many similar object constructions → Factory pattern

**Signal:**
- Multiple call sites do `new X()` with slightly different setup logic.
- A switch or chain that picks which subclass to instantiate.

**Plain-language explanation:** *"Construction logic is scattered across the codebase. Put it in one factory function/class — every caller says `UserFactory.create(...)` instead of reinventing setup."*

### 4. Shared mutable state between methods → Value object / State pattern

**Signal:**
- A class whose methods mutate and read the same field in sequence, where the field's allowed transitions form a state machine.
- A primitive field (string / number) used as a state flag with branching everywhere.

**Plain-language explanation:** *"This class tracks state with branching `if` checks everywhere. Either make the value an immutable value object, or introduce a State class so each state knows its own legal transitions."*

See `references/pattern-catalog.md` for detection heuristics and full rewrite templates.

## Step 1: Read & Analyze

Read the target file. For each class and top-level function, check for the four signals above.

## Step 2: Report

```
cleancode structure — [file]

🔵 Pattern suggestion: Strategy
  • src/paymentProcessor.ts:34 — switch with 6 cases in `processPayment()`
      Why: adding a new payment method means editing a 60-line switch
      Fix: extract each case into a Payment strategy class
      Plain: "one small class per payment method, pick the right one at runtime"

🔵 Pattern suggestion: Factory
  • src/userBuilder.ts — 4 call sites construct User with slightly different setup
      Why: construction logic duplicated
      Fix: centralize in UserFactory.create(role) { ... }
      Plain: "one place that knows how to build a user — every caller asks it"

Report only. Pass `fix` to apply.
```

If no patterns are a clear fit, say so: `✓ No structural improvements suggested. Your code is already well-factored.`

## Step 3: Plan Rewrite (fix mode)

Show the full rewrite plan BEFORE writing:

```
Strategy pattern — src/paymentProcessor.ts

Will create:
  • src/payments/IPaymentMethod.ts    (interface)
  • src/payments/CreditCardPayment.ts (strategy)
  • src/payments/PayPalPayment.ts     (strategy)
  • src/payments/BankTransferPayment.ts (strategy)
  • src/payments/index.ts             (strategy registry)

Will modify:
  • src/paymentProcessor.ts           (replace switch with registry lookup)

Lines changed: ~180. Test file unchanged (same inputs → same outputs).

Apply? (yes / dry run / no)
```

Wait for confirmation. Apply via Write (new files) + Edit (existing files).

## Step 4: Apply Pattern

Each pattern has a full rewrite template in `references/pattern-catalog.md` — look up the one the report selected and follow it step by step. Strategy, Command, Factory, and State are all documented there with interface definitions, per-case file layout, registry/dispatch code, and the exact call-site replacement.

**When NOT to apply:** the catalog documents cases where each pattern would over-engineer the situation. Check the "When it does NOT fit" section of the selected pattern before writing — if any row matches, report the suggestion but do not apply the `fix`.

## Step 5: Verify

After applying:

1. Re-read the touched files.
2. Confirm:
   - No compilation errors (if the user's project has a type checker, suggest running it).
   - The original function signature is preserved (callers don't need to change).
   - The new files follow the project's existing naming conventions.
3. Print: `✓ Strategy pattern applied. 5 new files, 1 file modified. Suggest running tests to confirm behavior is preserved.`

## Rules

- **Preserve behavior.** Every rewrite must return identical results for identical inputs. If a rewrite would change behavior, flag it and ask.
- **Don't over-pattern.** If the code is already clear, don't apply a pattern just because it fits a signal. Over-engineering is itself a clean code violation (Rule 13).
- **Ask for deep restructurings.** Any change touching > 3 files needs explicit user approval beyond the initial `fix` flag.

## Additional Resources

- **`references/pattern-catalog.md`** — detection heuristics, full rewrite templates for all 4 patterns, and when NOT to apply each
