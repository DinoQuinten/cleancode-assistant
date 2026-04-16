---
name: fix
description: This skill should be used when the user asks to "fix everything", "fix all violations", "clean this up", "auto-fix", "apply all fixes", "clean my code", "fix this file completely", or wants a one-shot fixer that runs every cleancode fixer in order. Orchestrates analyze + each fixer skill (safety, untangle, test, refactor) in severity order, asks for confirmation, and applies fixes.
argument-hint: "[file-path or . for project] [critical-only | all]"
allowed-tools: Read, Write, Edit, Grep, Glob
version: 0.2.0
---

# Clean Code Fix

One-shot orchestrator that runs every cleancode fixer in order. This is the "Claude, handle it all and change the code too" command — matches the user's intent to have one command that cleans a file or project top-to-bottom.

## When This Runs

- User asks to fix everything, auto-fix, or clean up a file completely
- User wants a single command that applies every available fixer

## Arguments

```
/cleancode:fix <file>                # fix critical violations only (default)
/cleancode:fix <file> all            # fix critical + warnings
/cleancode:fix .                     # fix critical across the whole project
/cleancode:fix . all                 # fix everything project-wide
```

Default is `critical-only` — safer, less churn.

## Pipeline

The fix skill runs other skills as a pipeline in this exact order. Each stage reads the result of the previous stage.

```
1. analyze      → list every violation, tagged by rule + severity
2. safety fix   → silent catches, missing guards (Rule 12)
3. untangle fix → method chains, high fan-out (Rule 11)
4. test fix     → if target is a test file (Rule 14)
5. refactor     → extract long functions, flatten deep nesting (Rules 2, 4)
6. structure    → suggest design patterns for big switches (report only in pipeline)
7. re-analyze   → verify violations are resolved
```

See `references/fix-pipeline.md` for the stage-by-stage contract and decision rules.

## Step 1: Scope Check

If the target is `.` (whole project), confirm with the user:

```
You asked to fix the whole project. This will edit multiple files.
Scope: 47 source files, 183 violations (12 critical, 38 warning, 133 style).
Mode: critical-only

This will run:
  • /cleancode:safety fix     (on 8 files)
  • /cleancode:untangle fix   (on 5 files)
  • /cleancode:refactor       (on 11 functions)

Proceed? (yes / narrow to one file / no)
```

Wait for explicit `yes`. For single-file invocations, skip this check — the user already targeted one file.

## Step 2: Analyze

Run the analyze detection logic on the target. Collect every violation into a list:

```
[
  { file, line, rule, severity, description, fixer_skill }
]
```

Map each rule to its fixer:

| Rule | Fixer skill |
|---|---|
| Rule 1 (file too long) | Manual suggest (`/cleancode:rewrite` or split) |
| Rule 2 (function too long) | `refactor` (extract-function) |
| Rule 3 (too many params) | `refactor` (parameter-object) |
| Rule 4 (deep nesting) | `refactor` (guard-clauses) |
| Rule 5 (bad naming) | Report only (needs human judgment) |
| Rule 7 (missing interface) | Manual suggest |
| Rule 11 (Demeter) | `untangle fix` |
| Rule 12 (hidden errors) | `safety fix` |
| Rule 14 (messy tests) | `test fix` |

Style violations (Rule 13, magic numbers) are reported but not auto-fixed unless the user passes `all`.

## Step 3: Show Plan

```
cleancode fix — plan

File: src/auth.ts
  🔴 3 critical, 🟡 5 warnings

  Stage 1 — safety fix
    • Replace empty catch at line 47
    • Add guard for email at line 12
    • Add guard for password at line 13

  Stage 2 — untangle fix
    • Replace chain at line 89: user.getAccount().getBalance().format()

  Stage 3 — refactor
    • Extract function: lines 120-160 (tax calc) → calculateTax()
    • Flatten nesting: lines 200-230 → 3 guard clauses

  Stage 4 — re-analyze
    • Verify all 8 violations are resolved

Estimated edits: 1 file, ~45 lines changed.
Apply? (yes / preview / no)
```

Wait for `yes`.

## Step 4: Execute Stages

Run each stage in order. For each:

1. Apply the same detection + fix logic documented in the corresponding fixer skill (`safety`, `untangle`, `test`, `refactor`). The fix skill does not invoke other skills as sub-processes — it re-uses their detection rules and fix templates inline.
2. Pass the subset of violations relevant to that stage.
3. Collect the results (edits applied, files touched).
4. If a stage fails (error, user cancels mid-way), stop the pipeline and report what was done.

**Between stages:** re-read any file that was touched. Downstream stages use the post-edit content.

## Step 5: Verify

After all stages:

1. Re-run analyze on the target.
2. Compare to the original violation list.
3. Report:

```
cleancode fix — complete ✓

Before: 12 critical, 38 warnings, 133 style
After:   0 critical,  3 warnings, 133 style

Fixed:
  • 12 critical (100%)
  • 35 warnings (92%)

Still open (manual review):
  • src/App.tsx: file too long (needs split — run /cleancode:rewrite)
  • src/utils.ts:45: bad naming (needs human judgment)

Files changed: 8
Lines changed: ~210

Suggest running your test suite to confirm behavior is preserved.
```

## Rules

- **Never auto-commit.** Changes stay in working directory. User reviews and commits.
- **Stop on error.** If any stage fails, stop the pipeline. Leave already-applied edits in place.
- **Preserve behavior.** Every fix must preserve observable behavior. If a fix would change semantics, skip it and log a manual-review note.
- **Ask once, run fully.** After the user says `yes` to the plan, run the whole pipeline — don't re-confirm each stage (unless a stage encounters an ambiguous case the fixer itself flags).
- **Always show the plan and wait for `yes`** before editing, regardless of file count or change size. The user is in control of every write.

## What /cleancode:fix Does Not Do

- Does not run `/cleancode:structure fix` (design patterns) — those are big restructurings, require explicit user invocation.
- Does not split files (Rule 1 too-long) — delegates to `/cleancode:rewrite` suggestion.
- Does not rename — naming changes are human judgment calls.
- Does not run `/cleancode:todo` — fixing ≠ tracking.

## Additional Resources

- **`references/fix-pipeline.md`** — stage-by-stage contract, rollback behavior, what each fixer guarantees
