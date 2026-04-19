---
name: rewrite
description: This skill should be used when the user asks to "clean my code", "make it human readable", "make this readable", "rewrite this cleanly", "refactor this", "clean up this function", "simplify this code", "make this code better", "fix code quality", "clean this file", "this code is messy", "improve this code", or when code has visible violations like long functions, deep nesting, poor names, or missing interfaces. Produces a clean version preserving all behavior, with reasoning for each change.
argument-hint: "[file-path or paste code directly]"
allowed-tools: Read, Write, Edit
version: 0.1.0
---

# Clean Code Rewrite

Produce a clean version of the provided code that preserves all existing behavior while fixing violations. Show what changed and why — this is both a fix and a learning moment.

## Core Principle

**Behavior preservation first.** A clean rewrite that changes what the code does is a bug introduction. Every rewrite must be functionally equivalent to the original.

## Before Rewriting

1. **Read the full file or code** — understand what it does completely before changing anything
2. **Identify all violations** — mentally run the analyze checklist (file length, function length, naming, nesting, interfaces, DRY)
3. **Identify what NOT to change** — public API signatures, exported names, database schemas, external interfaces
4. **Plan the split** — if the file needs splitting, decide the new file names and what goes where

## The Rewrite Process

### Step 1: Fix the Biggest Violation First

Priority order:
1. **File over 300 lines** → split the file. This is always done first.
2. **Functions over 40 lines** → extract sub-functions
3. **Deep nesting (>4)** → apply guard clauses
4. **Too many parameters (>4)** → introduce a parameter interface
5. **Bad names** → rename to reveal intent
6. **Missing interface [TS]** → extract interface
7. **DRY violations** → extract shared logic
8. **Comment cleanup** → remove "what" comments, keep "why" comments

### Step 2: Extract Functions with Good Names

When extracting a function:
- Name it by what it **does**, not how: `validateUserInput`, not `checkStuff`
- The parent function should read like a table of contents after extraction
- Keep the new function in the same file or a clearly named new file

### Step 3: Apply Guard Clauses

Transform nested conditionals into early returns:
```
if (x) {
  if (y) {
    // work
  }
}
→
if (!x) return;
if (!y) return;
// work
```

### Step 4: TypeScript — Extract Interfaces

For TypeScript files:
- If a class has no interface, extract one named `I[ClassName]` or `[ClassName]` (team convention)
- If a function takes 4+ related parameters, create an interface for them
- Place interfaces at the top of the file or in a `types.ts` alongside the implementation

### Step 5: Fix Names

Rename in this priority:
1. Generic names (`data`, `info`, `temp`, `obj`, `val`, `result`) → specific nouns
2. Abbreviated names → full words
3. Non-verb function names → verb + noun
4. Magic numbers → named constants

## Output Format

Always show the rewrite as:

```
## Clean Rewrite: [filename or "provided code"]

### What Changed

| Before | After | Why |
|---|---|---|
| 83-line `handleOrder()` | 4 extracted functions | Do One Thing — each function has one purpose |
| Nested 5 levels deep | Guard clauses + early returns | Max nesting depth 4 |
| `data`, `obj`, `d` | `orderDetails`, `userAccount`, `date` | Intention-revealing names |
| No interface for `OrderService` | `IOrderService` interface extracted | Dependency Inversion |

### Clean Version

[full rewritten code here]

### Files Created (if split)

If the file was split:
- `[new-file-1.ts]` — [what it contains]
- `[new-file-2.ts]` — [what it contains]

### What Was Not Changed

[Note any public APIs, exports, or signatures preserved intentionally]
```

## Handling File Splits

When a file over 300 lines needs splitting:

1. **Identify responsibilities** — list each distinct concern in the file
2. **Name the new files** by responsibility (not by technical layer when possible)
3. **Write all new files** — don't leave partial rewrites
4. **Update imports** — show the updated import statements in the parent
5. **State clearly** which files to delete or replace

Example:
```
userService.ts (450 lines) → split into:
- auth/userAuthService.ts (validates, hashes, tokens)
- repositories/userRepository.ts (database access)
- email/userEmailService.ts (sends emails)
- formatting/userFormatter.ts (display utilities)

Each file: under 100 lines, single responsibility.
```

## Rewrite Scope

- **Small function** (< 40 lines): rewrite inline, show before/after
- **Single file** (< 300 lines): rewrite the whole file
- **Large file** (> 300 lines): split into multiple files, show all of them
- **Whole directory**: ask user to confirm before proceeding — propose the split plan first

## After the Rewrite

End every rewrite with:
```
Violations fixed: [N critical], [N warnings]
Files changed: [list]

Run /cleancode:analyze [file] to confirm 0 violations.
Run /cleancode:teach [principle] to understand any change made.
```

## Constraints

- **Never break the public API** — if a function is exported or called externally, keep its signature
- **Never change business logic** — extract, rename, reorganize, but don't change behavior
- **Ask before splitting across modules** — if a split requires creating new directories or moving across package boundaries, confirm with the user first
- **Preserve tests** — if test files exist, note what test updates are needed but don't rewrite tests unless asked

## Chain to /cleancode:restructure when a split crosses folder boundaries

`/rewrite` splits files into siblings in the same folder. When a split reveals that the extracted pieces actually belong **in different folders** per the project's conventions (e.g., extracting a service from a route handler — service belongs in `services/` or `lib/server/services/<feature>/`, not next to the route file), do NOT silently apply the move yourself. Instead, after presenting the split plan:

1. Identify which extracted pieces are misplaced relative to the project's existing style (read top-level folders to infer style — feature-folders vs layered).
2. Append to your output:

   ```
   ## Cross-folder restructure suggested

   This split would benefit from cross-folder relocation:
   - <ExtractedPiece1> — better fits `<destination-folder>/`
   - <ExtractedPiece2> — better fits `<other-destination>/`

   Chain to /cleancode:restructure for an atomic, plan-first move with import rewrites? [y/N]
   ```

3. If the user confirms, hand off to `/cleancode:restructure` with the specific files and proposed destinations as input scope.

**When NOT to chain:** if all extracted files fit in the same folder as the original (typical case), no chain is needed. Only offer the chain when ≥ 2 extracted files clearly belong elsewhere — otherwise it's noise.

## Additional Resources

### Example Files

- **`examples/before-after.md`** — 5 complete before/after rewrites covering the most common transformations: monolith function split, deep nesting fix, bad naming fix, missing interface extraction, and large file split. Reference these for realistic examples of each transformation type.
