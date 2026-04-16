---
name: Clean Code Refactor
description: This skill should be used when the user asks to "refactor this file", "clean up this code", "extract this function", "break this function apart", "pull this out into a method", "simplify this switch", "turn this into a table", "inline this", "replace magic number", or mentions a specific refactoring by name. Applies one named, surgical refactoring from the textbook catalog (Extract Method, Table-Driven, Replace Conditional with Polymorphism, etc.) and shows exactly what changed.
argument-hint: "[file-path] [refactoring-name]"
allowed-tools: Read, Write, Edit, Grep
version: 0.2.0
---

# Clean Code Refactor

Apply one specific, well-known refactoring to a file. Each refactoring has a textbook reference (Code Complete Ch. 24; Fowler's refactoring catalog). This skill differs from `/cleancode:rewrite`: `rewrite` produces a whole cleaner version; `refactor` applies **one** surgical, named change.

## When This Runs

- User asks to apply a specific named refactoring to a file
- `/cleancode:fix` delegates long-function and deep-nesting fixes here

## Arguments

```
/cleancode:refactor <file> <refactoring-name>
/cleancode:refactor <file>                      # skill suggests the best fit
```

Valid refactoring names (plain-language first, textbook name in parens):

| Name | Plain language | Textbook |
|---|---|---|
| `extract-function` / `pull-out-function` | Pull a block into its own named function | Extract Method |
| `extract-class` / `pull-out-class` | Pull a group of fields + methods into a new class | Extract Class |
| `inline` | Inline a function whose body says more than its name | Inline Method |
| `named-constant` / `replace-magic-number` | Replace a bare number with a named constant | Replace Magic Number |
| `polymorphism` / `swap-if-chain-for-polymorphism` | Replace a big if-chain with subclasses (see also `/cleancode:structure`) | Replace Conditional with Polymorphism |
| `guard-clauses` / `swap-nested-ifs-for-guards` | Flatten nested ifs with early returns | Replace Nested Conditional with Guard Clauses |
| `parameter-object` / `group-arguments` | Group related params into an object | Introduce Parameter Object |
| `table-driven` / `replace-switch-with-table` | Replace a switch with a lookup table | Table-Driven Method |
| `split-variable` | Split a reused variable into separate variables | Split Variable |

See `references/refactoring-catalog.md` for each refactoring's full template and when to apply it.

## Step 1: Identify the Refactoring

If the user supplied a name, use it. Otherwise:

1. Read the file and identify the most impactful violation:
   - Longest function → suggest `extract-function`
   - Deepest nesting → suggest `guard-clauses`
   - Largest switch → suggest `table-driven` or `polymorphism`
   - Magic numbers present → suggest `named-constant`
   - Too many params → suggest `parameter-object`
2. Propose the refactoring name and ask: "Apply `extract-function` to `processOrder()`? (yes / pick another)"

## Step 2: Plan the Change

Before editing, identify the exact target:

- For extract-function: which block of lines becomes the new function? What should it be named?
- For inline: which function is being removed? Where are its callers?
- For named-constant: which number? What's the meaningful name?
- For table-driven: which switch? What's the lookup shape?

Show the plan:

```
Refactoring: extract-function

Target: src/order.ts, lines 45-68 inside `processOrder()`
  (tax calculation block — 24 lines)

New function: `calculateTax(order: IOrder): number`
  • Extracted to: end of src/order.ts (below processOrder)
  • Reference: Fowler's "Extract Method"; Code Complete Ch. 24

After refactor:
  • `processOrder()` becomes 64 lines (was 88) ✓ under limit
  • `calculateTax()` is 24 lines ✓ under limit

Apply? (yes / preview diff / no)
```

## Step 3: Apply via Edit

Use Edit for surgical changes. For extract-function:

1. Copy the target block verbatim.
2. Identify the variables the block **reads** (become function parameters).
3. Identify the variables the block **writes** that are used after (become return value).
4. Create the new function at the bottom of the file (or in a helper file if instructed).
5. Replace the block at the original location with a call to the new function.

For table-driven:

1. Copy each case's body.
2. Build a map: key → handler function (or key → value if all cases are constants).
3. Replace the switch with a map lookup.

For guard-clauses:

1. Identify nested `if`s wrapping the happy path.
2. Invert each condition: `if (!x) return;`
3. Unindent the happy path.

For parameter-object:

1. Group params into a TypeScript interface (or dataclass / record).
2. Update the function signature.
3. Update all call sites to pass the new object.

Each template is fully documented in `references/refactoring-catalog.md`.

## Step 4: Verify

After applying:

1. Re-read the file.
2. Confirm:
   - The refactored function preserves the original behavior (same inputs → same outputs by inspection).
   - No broken references (did any callers need updating?).
   - Line counts improved (the refactoring achieved its stated goal).
3. Print:
   ```
   ✓ extract-function applied.
     processOrder: 88 → 64 lines
     calculateTax: new, 24 lines

   Suggest running your test suite to confirm behavior.
   ```

## Rules

- **One refactoring per invocation.** Don't chain multiple refactorings — user can re-run the skill.
- **Preserve behavior.** No logic changes. If the refactoring would change semantics, stop and explain.
- **Keep it small.** If the change touches > 5 files, stop and ask — this may be a case for `/cleancode:structure` instead.
- **Update callers when signatures change.** Extract, inline, and parameter-object change public signatures; update every call site.

## Difference from `/cleancode:rewrite`

| Skill | Behavior |
|---|---|
| `/cleancode:refactor` | One named surgical change — Extract Method, Inline, etc. |
| `/cleancode:rewrite` | Full rewrite of the file preserving behavior |

Use `refactor` for targeted improvements; use `rewrite` for a thorough cleanup.

## Additional Resources

- **`references/refactoring-catalog.md`** — full templates and when-to-apply for each refactoring
