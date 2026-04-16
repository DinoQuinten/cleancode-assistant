---
name: Clean Code Health
description: This skill should be used when the user asks for "project health", "code health", "clean code score", "cleanliness score", "how bad is my code", "show metrics", "code quality dashboard", or wants a top-level view of the codebase's cleanliness. Produces a read-only dashboard of violation counts, worst offenders, and a 0-100 cleanliness score. Read-only by design — for fixing, use the specific skills.
argument-hint: "[save]"
allowed-tools: Read, Write, Glob, Grep
version: 0.2.0
---

# Clean Code Health

Print a short dashboard summarizing the project's clean code health. This skill is **read-only by design** — it reports, it does not change code. To fix what it reports, the user runs a specific skill (`/cleancode:untangle fix`, `/cleancode:safety fix`, `/cleancode:fix`).

**Source:** The Art of Clean Code, Principle 16 — Use Metrics.

## When This Runs

- User asks for project health, a cleanliness score, or a quality dashboard
- Periodic team check-in on code quality

## Arguments

```
/cleancode:health          # print dashboard, don't save
/cleancode:health save     # print + write .cleancode-health.md (for tracking over time)
```

## Step 1: Scan the Project

1. Glob all source files (exclude `node_modules`, `.git`, `dist`, `build`, generated code).
2. For each file, measure:
   - Lines of code (excluding blank lines and comment-only lines)
   - Number of functions
   - Longest function length
   - Max nesting depth
   - Import count
   - For TypeScript files: number of exported classes and whether each has an interface

3. Aggregate across the project:
   - Total LOC
   - Total files
   - Files over 300 lines (Critical — Rule 1)
   - Files over 200 lines (Warning)
   - Functions over 40 lines (Critical — Rule 2)
   - Functions over 20 lines (Warning)
   - Average nesting depth
   - Max nesting depth
   - Interface coverage % (TS only): classes with interfaces / total public classes
   - Rough duplication estimate: run the 3-line-window duplication check, count flagged blocks

## Step 2: Compute Cleanliness Score

Score is 100 minus weighted penalty for each violation. See `references/metric-definitions.md` for the exact formula. Summary:

| Violation type | Penalty per occurrence |
|---|---|
| Critical file size | 5 |
| Critical function size | 3 |
| Warning file size | 2 |
| Warning function size | 1 |
| Deep nesting (> 4) | 2 |
| High fan-out (> 15 imports) | 3 |
| Missing interface [TS] | 1 |
| Duplication block | 2 |
| Hidden error (Rule 12) | 3 |

Clamp to [0, 100]. Round to nearest integer.

## Step 3: Print Dashboard

```
═══════════════════════════════════════════════════════════
  cleancode health — [Project Name]
═══════════════════════════════════════════════════════════

  Cleanliness Score: 72/100  🟡 Needs attention

  ──  Totals ──────────────────────────────
    Total LOC:              14,320
    Total files:               182
    Average file length:        79 lines
    Average function length:    14 lines
    Max nesting depth:           6

  ──  Violations ──────────────────────────
    🔴 Critical:  12
       • 3 files > 300 lines
       • 9 functions > 40 lines
    🟡 Warning:   38
       • 11 files > 200 lines
       • 22 functions > 20 lines
       •  5 method chains > 2
    🔵 Style:    124 (naming, magic numbers, unused code)

  ──  Top 10 Worst Files ──────────────────
    1. src/App.tsx                        487 lines 🔴
    2. src/services/userService.ts        412 lines 🔴
    3. src/utils/helpers.ts               378 lines 🔴
    ...

  ──  Top 10 Longest Functions ───────────
    1. processOrder()     src/order.ts           98 lines 🔴
    2. validateInput()    src/validator.ts       72 lines 🔴
    ...

  ──  TypeScript Coverage ─────────────────
    Interface coverage:       64% (32/50 public classes)

  ──  Suggested Next Actions ──────────────
    • Start with /cleancode:fix src/App.tsx
    • Run /cleancode:analyze src/services/userService.ts
    • Run /cleancode:untangle . to find coupling issues

═══════════════════════════════════════════════════════════
```

## Step 4: Save (if requested)

If the user passed `save`:

1. Write the dashboard text + raw metrics (JSON block) to `<project root>/.cleancode-health.md`.
2. If the file already exists, append today's run to a history section:

   ```markdown
   # Clean Code Health

   Last run: 2026-04-15

   ## Current
   [dashboard as above]

   ## History

   | Date | Score | Critical | Warning | Style |
   |---|---|---|---|---|
   | 2026-04-15 | 72 | 12 | 38 | 124 |
   | 2026-04-01 | 68 | 15 | 42 | 131 |
   | 2026-03-15 | 61 | 19 | 48 | 144 |
   ```

The history table is how teams track progress over time.

## Rules

- **Read-only.** This skill never modifies source code. To fix, use the specific fixer skills.
- **Always whole-project.** Single-file health doesn't make sense — use `/cleancode:analyze <file>` for that.
- **Fast.** Don't deep-analyze every file; use quick line counts and spot-check violations. Target < 10 seconds for projects up to 200 files.
- **Stable scoring.** The formula in `metric-definitions.md` should not drift between runs — re-running on unchanged code must produce the same score.

## Additional Resources

- **`references/metric-definitions.md`** — exact scoring formula, metric calculations, and tuning notes
