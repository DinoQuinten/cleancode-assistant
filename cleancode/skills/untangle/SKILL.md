---
name: Clean Code Untangle
description: This skill should be used when the user asks to "reduce coupling", "untangle this code", "fix method chains", "too many imports", "this file depends on too much", "long method chains", "reaching through objects", "law of demeter", or mentions tangled dependencies between files. Detects and optionally fixes Rule 11 violations — long method chains, high fan-out imports, and circular dependencies.
argument-hint: "[file-path or . for project] [fix]"
allowed-tools: Read, Write, Edit, Grep, Glob
version: 0.2.0
---

# Clean Code Untangle

Find and (optionally) repair places where one file or function knows too much about other files. Targets Rule 11 — Don't Reach Through Objects (Law of Demeter) — plus high fan-out imports and circular dependencies.

## When This Runs

- User asks to untangle a file, reduce coupling, or fix method chains
- Analyze reports Rule 11 violations and user wants them fixed
- `/cleancode:fix` delegates chain-depth fixes to this skill

## Modes

| Invocation | Behavior |
|---|---|
| `/cleancode:untangle <file>` | Report only — list violations with line numbers, no file changes |
| `/cleancode:untangle <file> fix` | Show planned edits, then apply via Edit / Write |
| `/cleancode:untangle .` | Report across the whole project |
| `/cleancode:untangle . fix` | Apply fixes project-wide (asks for confirmation first) |

Default is **report mode**. Only write to files when the user passes `fix`.

## Step 1: Detect Violations

Read the target file(s). For each, scan for:

1. **Long method chains** — `obj.method().method().method()` with chain depth > 2. See `references/coupling-patterns.md` for the regex and exceptions (fluent builders are OK).
2. **High fan-out** — file imports from > 10 other modules (Warning) or > 15 (Critical).
3. **Circular imports** — build a small import graph across files touched; flag any cycle.
4. **God class signals** — a class with > 10 public methods OR that imports from > 8 other modules AND has > 200 lines.

Record each violation with: file, line, kind, chain text (for chains), and a plain-language explanation.

## Step 2: Report

Print a grouped report:

```
cleancode untangle — [file or .]

🔴 Critical
  • src/order.ts:47 — chain of 4: `order.getCustomer().getAddress().getCity().getZip()`
      Why: reaches through 3 classes — breaks if any middle class changes
      Fix: add `order.getZip()` that hides the chain

🟡 Warnings
  • src/order.ts:89 — chain of 3: `user.getAccount().getBalance().format()`
      Why: the formatter shouldn't know about accounts
      Fix: add `user.getFormattedBalance()`

  • src/services/userService.ts — imports from 13 modules
      Why: this file is a hub — changes everywhere can break it
      Fix: split into userReader.ts, userWriter.ts, userAuth.ts (see suggestion below)

Report only. Pass `fix` to apply these changes.
```

In report mode, stop here.

## Step 3: Plan Fixes (fix mode only)

For each violation, compute the concrete edit:

### Method chain — "add a helper on the owning object"

For a chain `a.b().c().d()`:

1. Identify the **owner** (`a`) and the **final result** (`d()`).
2. Find the class definition of `a`.
3. Propose a new method on `a` named after the final result — `aGetD()`, or a natural domain name (`order.getZip()`).
4. The new method's body is the inner chain: `return this.b().c().d();`.
5. Replace every call site of the original chain with the new helper.

### High fan-out — "split by responsibility"

Read the file's exports. Group imports by what uses them:

- Imports used only by auth methods → goes to an `auth` helper or module
- Imports used only by CRUD → `reader` / `writer`
- Shared across → stay in the core

Produce a split plan: proposed new files + which methods move where. **Do not auto-split** a file > 400 lines without user confirmation — show the plan and ask.

### Circular import — "break the cycle"

For `A ↔ B`:

1. Find which symbol(s) cause the cycle.
2. Extract the shared symbol into a third file `C` (types / interfaces / constants).
3. Rewrite `A` and `B` to both import from `C`.

## Step 4: Show Diff, Confirm

Before writing:

```
Planned fixes:

1. src/models/Order.ts:215  — add method `getZip(): string`
2. src/order.ts:47           — replace chain with `order.getZip()`
3. src/order.ts:89           — replace chain with `user.getFormattedBalance()`
4. src/models/User.ts:180    — add method `getFormattedBalance(): string`

Total: 4 files changed, 2 helper methods added, 3 chains replaced.
Apply? (say "yes" to proceed, or "dry run" to see the full diff first)
```

Wait for user confirmation. Apply with Edit (preferred — smaller diffs) or Write.

## Step 5: Verify

After applying:

1. Re-read the touched files.
2. Re-run Step 1 on each.
3. Confirm all flagged violations are gone.
4. Print a summary: `✓ 3 chains replaced, 2 helpers added. Re-run /cleancode:untangle <file> to verify.`

## Exceptions (don't flag these)

- **Fluent builders** — `builder.setX().setY().build()` where every intermediate call returns the same builder type. Downgrade to Style.
- **Query builders** — ORM chains like `.where().select().limit()`. Downgrade to Style.
- **Standard library chains** — `array.filter().map().reduce()` is idiomatic, not a Demeter violation.
- **Optional chaining** — `user?.profile?.name` is null-safe access on data you own, not method digging.

See `references/coupling-patterns.md` for full detection regex, edge cases, and language-specific notes.

## Additional Resources

- **`references/coupling-patterns.md`** — detection regex, fluent-builder detection, language-specific patterns, and example transformations
