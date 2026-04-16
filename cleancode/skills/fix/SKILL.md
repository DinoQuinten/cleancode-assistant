---
name: fix
description: This skill should be used when the user asks to "fix everything", "fix all violations", "clean this up", "auto-fix", "apply all fixes", "clean my code", "fix the whole project", or wants a one-shot fixer that runs every cleancode fixer in order across the codebase. Orchestrates analyze + each fixer skill (safety, untangle, test, refactor) in severity order across every source file, produces a full project-wide plan, asks for confirmation, and applies fixes.
argument-hint: "[. or file-path, default: .] [critical-only | all] [stage-first | file-first]"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
version: 0.2.0
---

# Clean Code Fix

One-shot orchestrator that runs every cleancode fixer in order **across every source file in the project**. This is the "Claude, handle it all and change the code too" command — it produces a full-on, codebase-wide plan, gets confirmation, then executes.

## When This Runs

- User asks to fix everything, auto-fix, or clean up the project
- User wants a single command that applies every available fixer across every file
- A single-file target is supported but is the narrow case, not the default

## Arguments

```
/cleancode:fix                       # project-wide, critical only (default)
/cleancode:fix all                   # project-wide, critical + warnings
/cleancode:fix <file>                # single-file, critical only
/cleancode:fix <file> all            # single-file, critical + warnings
/cleancode:fix .                     # explicit project scope (same as default)
/cleancode:fix . all                 # explicit project scope, all severities

# Execution strategy (optional, prompted if omitted):
/cleancode:fix . stage-first         # run each fixer across all files, then next fixer
/cleancode:fix . file-first          # fully clean each file, then move to the next
```

Default scope is **the whole project**. Default mode is `critical-only`. **Strategy is not defaulted** — if the user didn't pass `stage-first` or `file-first`, ask them at the confirmation gate (Step 1). Single-file invocations skip the strategy question (only one file, so both strategies are equivalent).

### Resolving the File Set

For project scope, build the file set by:

1. Reading ignore patterns from `.gitignore` and `.cleancode-ignore` (if present).
2. Including source files by extension: `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.go`, `.rs`, `.java`, `.kt`, `.rb`, `.cs`, `.cpp`, `.c`, `.h`, `.hpp`, `.swift`, `.php`.
3. Excluding common noise dirs: `node_modules/`, `dist/`, `build/`, `.next/`, `out/`, `target/`, `vendor/`, `__pycache__/`, `.venv/`, `coverage/`.
4. Excluding generated or lock files (`*.min.js`, `*.lock`, `package-lock.json`).

If the set is empty, stop and report "no source files found."

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

For project scope (the default), always confirm with the user before touching anything:

```
/cleancode:fix — project scope

Source files scanned: 47  (after .gitignore + .cleancode-ignore)
Mode: critical-only

Violations found:
  🔴 12 critical   across  8 files
  🟡 38 warning    across 14 files
  ⚪ 133 style     across 22 files  (not auto-fixed)

Stages that will run:
  • safety fix      →  4 files,  7 edits
  • untangle fix    →  3 files,  5 edits
  • refactor        →  6 files, 11 edits
  • structure       →  report only

How should I execute?
  [1] stage-first  — run each fixer across all files, then next fixer
                     (safety on all → untangle on all → refactor on all)
                     Best when you want coherent fixer-by-fixer progress and
                     don't mind files sitting in intermediate states briefly.
  [2] file-first   — fully clean each file through every stage, then next file
                     Best when you want each file to reach a reviewable state
                     before the run moves on, or plan to abort midway.

Proceed? (1 / 2 / narrow to <path> / all (include warnings) / no)
```

Wait for an explicit choice (`1`, `2`, `stage-first`, or `file-first`) plus `yes` intent. If the user passed the strategy on the command line, skip the `[1] / [2]` prompt and just confirm.

For single-file invocations (user passed a path), skip this gate — they already scoped it, and the strategy question is moot for a single file.

## Step 2: Analyze

Run the analyze detection logic on **every file in the resolved set**. Collect every violation into a flat list:

```
[
  { file, line, rule, severity, description, fixer_skill }
]
```

Group the list two ways for later use:

- **By stage** (for execution): safety → untangle → test → refactor.
- **By file** (for the plan output and per-file verification).

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

The plan must cover **every file with at least one fixable violation**, grouped by file and annotated with stages. Keep the top-level summary compact; the per-file detail is what makes it a "full-on plan."

```
cleancode fix — plan  (project scope, critical-only)

═══ Summary ═══
23 files will be edited. ~210 lines changed. 0 files renamed.

Stages (executed in this order across the whole project):
  1. safety fix    →  4 files,  7 edits
  2. untangle fix  →  3 files,  5 edits
  3. test fix      →  2 files,  3 edits
  4. refactor      →  6 files, 11 edits
  5. structure     →  report only (2 candidates)
  6. re-analyze    →  verify all files

═══ Per-file detail ═══

src/auth.ts  🔴 3 critical
  safety     • Replace empty catch at line 47
  safety     • Add guard for email at line 12
  untangle   • Replace chain at line 89: user.getAccount().getBalance().format()

src/checkout/totals.ts  🔴 2 critical
  refactor   • Extract function: lines 120-160 (tax calc) → calculateTax()
  refactor   • Flatten nesting: lines 200-230 → 3 guard clauses

src/api/users.ts  🔴 1 critical
  safety     • Add guard for userId at line 8

…(21 more files — run with --verbose to expand, or narrow scope)

═══ Not auto-fixed (manual review) ═══
  • src/App.tsx:1           file too long (642 lines) — suggest /cleancode:rewrite
  • src/utils.ts:45         bad naming (`d`, `tmp`)  — human judgment

Apply? (yes / preview <path> / narrow <path> / no)
```

Interaction rules:

- `yes` → run Step 4 across all listed files.
- `preview <path>` → show the diff-style preview for one file's planned edits, then re-prompt.
- `narrow <path>` → reduce the scope to a single file or subdirectory and re-plan.
- `no` → abort, no edits made.

If the plan lists more than 20 files, show the first 20 per-file entries and append the `…(N more files)` line. Never truncate the summary header or the "not auto-fixed" list.

## Step 4: Execute

Execution depends on the strategy the user picked at the Step 1 gate. Both strategies apply the same fixer logic (inlined from `safety`, `untangle`, `test`, `refactor`) — they differ only in loop order.

Apply the same detection + fix logic documented in the corresponding fixer skill. The fix skill does not invoke other skills as sub-processes — it re-uses their detection rules and fix templates inline.

### Strategy A — stage-first (outer: stage, inner: file)

```
for stage in [safety, untangle, test, refactor]:
  for file in stage.applicable_files:
    apply fixer logic for `stage` to `file`
    emit progress: "[safety 3/4] src/api/users.ts — 2 edits applied"
```

- **Between stages:** re-read every file that was touched in the previous stage. Downstream stages must see post-edit content.
- **Between files within a stage:** each file edit is independent. A single-file failure does not roll back others — log it and continue.
- **Invariant:** after stage N finishes, every applicable file has fixer N applied before fixer N+1 starts anywhere.

### Strategy B — file-first (outer: file, inner: stage)

```
for file in all_files_with_violations:
  for stage in [safety, untangle, test, refactor]:
    apply fixer logic for `stage` to `file` (if applicable)
  emit progress: "[file 6/23] src/api/users.ts — 4 edits across 2 stages"
```

- Each file passes through every relevant stage before moving to the next file.
- Progress is reported **per file**, not per stage — one line per completed file.
- A failure on one file logs and moves to the next file. Completed files are fully clean and reviewable.
- **Invariant:** when the run reports `[file 6/23] …`, files 1–6 are fully processed and files 7–23 are untouched.

### Common rules (both strategies)

- A **per-file failure** is logged and skipped; the run continues.
- A **stage-wide failure** (detection logic crash, cache corruption) stops the run entirely.
- Progress markers are one line each. Don't dump diffs to the console — the user reviews via their diff tool.
- At the end of Step 4, hand the collected results (edits applied, files touched, skipped violations) to Step 5.

## Step 5: Verify

After all stages:

1. Re-run analyze on **every file that was touched** (no need to re-scan untouched files).
2. Compare to the original violation list.
3. Report:

```
cleancode fix — complete ✓   (project scope, critical-only)

Before: 12 critical, 38 warnings, 133 style   across 47 files
After:   0 critical,  3 warnings, 133 style   across 47 files

Fixed:
  • 12 critical (100%)
  • 35 warnings (92%)

Files changed: 23
Lines changed: ~210

Per-stage results:
  ✓ safety fix    — 7 edits across 4 files
  ✓ untangle fix  — 5 edits across 3 files
  ✓ test fix      — 3 edits across 2 files
  ✓ refactor      — 11 edits across 6 files

Still open (manual review):
  • src/App.tsx                file too long — run /cleancode:rewrite
  • src/utils.ts:45            bad naming    — human judgment
  • src/legacy/parser.ts:88    structure     — run /cleancode:structure fix

Suggest running your test suite to confirm behavior is preserved.
```

## Rules

- **Never auto-commit.** Changes stay in working directory. User reviews and commits.
- **Per-file failures continue; stage-wide failures stop.** A broken single file does not abort the whole project run. A detection-logic crash does.
- **User picks the execution strategy.** Don't default to stage-first or file-first silently — ask at the Step 1 gate unless the user passed the choice on the command line.
- **Preserve behavior.** Every fix must preserve observable behavior. If a fix would change semantics, skip it and log a manual-review note.
- **Ask once, run fully.** After the user says `yes` to the plan, run the whole pipeline across all files — don't re-confirm each stage or each file (unless a fixer flags an ambiguous case).
- **Always show the plan and wait for `yes`** before editing, regardless of file count or change size. The user is in control of every write.
- **Use bash helpers (Step 0) before expanding tools.** Enumerating files, counting lines, and first-pass violation scans belong in the shell — they save tokens and keep Claude's context focused on decisions, not directory walks.

## Step 0: Bash Helpers (token-saving scans)

Before running Claude-side analysis, use these bash helpers to pre-compute the cheap facts. They reduce the number of `Read`/`Grep` tool calls needed and keep the file list and line-count totals out of Claude's context when it's just summary data.

### 0.1 — Resolve the file set

```bash
# Emit one source file per line, honoring .gitignore and .cleancode-ignore.
# Works in any git repo; falls back to find(1) outside git.
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git ls-files -co --exclude-standard \
    | grep -E '\.(ts|tsx|js|jsx|py|go|rs|java|kt|rb|cs|cpp|c|h|hpp|swift|php)$' \
    | grep -Ev '(^|/)(node_modules|dist|build|\.next|out|target|vendor|__pycache__|\.venv|coverage)/' \
    | grep -Ev '\.min\.js$|\.lock$|package-lock\.json$'
else
  find . -type f \( -name '*.ts' -o -name '*.tsx' -o -name '*.js' -o -name '*.jsx' \
    -o -name '*.py' -o -name '*.go' -o -name '*.rs' -o -name '*.java' -o -name '*.kt' \
    -o -name '*.rb' -o -name '*.cs' -o -name '*.cpp' -o -name '*.c' -o -name '*.h' \
    -o -name '*.hpp' -o -name '*.swift' -o -name '*.php' \) \
    | grep -Ev '(^|/)(node_modules|dist|build|\.next|out|target|vendor|__pycache__|\.venv|coverage)/'
fi \
  | { [ -f .cleancode-ignore ] && grep -vFf .cleancode-ignore || cat; } \
  > .cleancode-cache/files.txt
```

Append `| wc -l` to get just the count — use this for the Step 1 summary without reading the file list into context.

### 0.2 — First-pass violation scan

```bash
# Fast heuristic pre-scan. Outputs TSV: file<TAB>line<TAB>rule<TAB>snippet
# Claude uses this to prioritize which files to Read in full.
mkdir -p .cleancode-cache
: > .cleancode-cache/hits.tsv

# Rule 12: empty catch blocks (safety — critical)
while IFS= read -r f; do
  grep -n -E 'catch[[:space:]]*\([^)]*\)[[:space:]]*\{[[:space:]]*\}' "$f" 2>/dev/null \
    | awk -F: -v file="$f" '{print file"\t"$1"\thidden-errors\t"$2}'
done < .cleancode-cache/files.txt >> .cleancode-cache/hits.tsv

# Rule 11: method chains > 2 (untangle — critical)
while IFS= read -r f; do
  grep -n -E '\.[A-Za-z_]\w*\([^)]*\)\.[A-Za-z_]\w*\([^)]*\)\.[A-Za-z_]\w*\(' "$f" 2>/dev/null \
    | awk -F: -v file="$f" '{print file"\t"$1"\treaching-through-objects\t"$2}'
done < .cleancode-cache/files.txt >> .cleancode-cache/hits.tsv

# Rule 2: function length > 40 lines (refactor — critical) — language-agnostic bracket counter
# (approximate; precise detection is done by Claude per file only for flagged files)
awk '/^[[:space:]]*(function|def |async def |fn |func |public |private |protected ).*[\{:]/ {start=NR; name=$0}
     /^[[:space:]]*\}[[:space:]]*$/ && start {if (NR-start>40) print FILENAME"\t"start"\tfunction-too-long\t"name; start=0}' \
  $(cat .cleancode-cache/files.txt) 2>/dev/null >> .cleancode-cache/hits.tsv
```

### 0.3 — Summary for the plan header

```bash
# Totals Claude needs for the Step 1 confirmation prompt.
echo "files_scanned=$(wc -l < .cleancode-cache/files.txt)"
echo "critical_hits=$(grep -cE 'hidden-errors|reaching-through-objects|function-too-long' .cleancode-cache/hits.tsv)"
echo "files_with_hits=$(cut -f1 .cleancode-cache/hits.tsv | sort -u | wc -l)"
echo "safety_files=$(grep -c 'hidden-errors' .cleancode-cache/hits.tsv | sort -u | wc -l)"
echo "untangle_files=$(grep 'reaching-through-objects' .cleancode-cache/hits.tsv | cut -f1 | sort -u | wc -l)"
echo "refactor_files=$(grep 'function-too-long' .cleancode-cache/hits.tsv | cut -f1 | sort -u | wc -l)"
```

### 0.4 — Per-stage file list

```bash
# One file list per stage. Claude iterates these during Step 4
# without having to re-derive them from the full violation list.
grep 'hidden-errors'              .cleancode-cache/hits.tsv | cut -f1 | sort -u > .cleancode-cache/stage-safety.txt
grep 'reaching-through-objects'   .cleancode-cache/hits.tsv | cut -f1 | sort -u > .cleancode-cache/stage-untangle.txt
grep 'function-too-long'          .cleancode-cache/hits.tsv | cut -f1 | sort -u > .cleancode-cache/stage-refactor.txt
```

### Token-saving rules

- **Run the helpers, read only the summary.** Don't `cat` the full `files.txt` or `hits.tsv` into context — they can be thousands of lines. Read only the small summary outputs (`0.3`) and per-stage lists (`0.4`), then `Read` individual files on demand.
- **Cache directory.** All helpers write to `.cleancode-cache/`. It's safe to add that to `.gitignore`. The cache is disposable; delete it when the run finishes if the user prefers a clean tree.
- **Skip helpers for single-file invocations.** When the user passed one path, Step 0 is overkill — go straight to a single `Read` + inline analysis.

## What /cleancode:fix Does Not Do

- Does not run `/cleancode:structure fix` (design patterns) — those are big restructurings, require explicit user invocation.
- Does not split files (Rule 1 too-long) — delegates to `/cleancode:rewrite` suggestion.
- Does not rename — naming changes are human judgment calls.
- Does not run `/cleancode:todo` — fixing ≠ tracking.

## Additional Resources

- **`references/fix-pipeline.md`** — stage-by-stage contract, rollback behavior, what each fixer guarantees
