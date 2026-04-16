# Violation Detection Rules

## How to Analyze a File

### Step 1: Count Lines

```
Total lines = all lines including blank lines
Code lines = total lines minus blank lines and pure comment lines
```

Flag when code lines > 300 (Critical) or > 200 (Warning).

### Step 2: Extract Functions / Methods

For each function/method, record:
- Start line and end line
- Name
- Parameter count (count comma-separated params in signature)
- Line count (end - start)

Patterns to match by language:

**TypeScript/JavaScript:**
```
function name(...) {  → traditional
const name = (...) => {  → arrow function
name(...) {  → method (class)
async name(...) {  → async
```

**Python:**
```
def name(...):
async def name(...):
```

**Java/C#:**
```
[modifiers] ReturnType name(...) {
```

**Go:**
```
func name(...) ... {
func (r Receiver) name(...) ... {
```

### Step 3: Measure Nesting Depth

Track the current depth as you read line by line:
- Depth increases on: `{`, `if`, `for`, `while`, `switch`, `try`, `(` (where opening a block)
- Depth decreases on matching closing tokens
- Record the maximum depth reached in each function

For Python: indent level ÷ 4 ≈ nesting depth

### Step 4: Detect Naming Issues

Scan for:
- Variables/parameters with 1-2 character names (exclude loop vars i, j, k, n, x, y)
- Names matching generic patterns: `data`, `info`, `temp`, `tmp`, `obj`, `val`, `result` without qualification
- Type encodings: `str`, `bool`, `int`, `b`, `s`, `i` as prefixes
- Non-verb function names (functions should start with: `get`, `set`, `create`, `build`, `fetch`, `load`, `save`, `update`, `delete`, `check`, `validate`, `parse`, `format`, `convert`, `handle`, `process`, `calculate`, `generate`, etc.)

### Step 5: TypeScript Interface Check

For TypeScript files:
- Find all `class` declarations
- Find all `export class` and `export default class`
- Check if a corresponding `interface` exists in the same file or imported
- Classes ending in `Service`, `Repository`, `Controller`, `Handler`, `Manager`, `Provider` that have no interface = Warning

### Step 6: Detect Duplication

Simple duplication check:
- Read file in 3-line windows
- If the same 3-line block appears more than once = Warning
- Look for loops doing the same thing in multiple places

### Step 7: Detect Comments

- Commented-out code: lines starting with `//` or `#` that look like code (contain `=`, `(`, `;`, `{`, `}`)
- TODOs: `// TODO`, `// FIXME`, `// HACK`, `# TODO`

### Step 8: Detect Reaching Through Objects (Rule 11 — Law of Demeter)

Regex for method chains: `\w+\s*\(\s*\)?\s*\.\s*\w+\s*\(` repeated.

- Count `.method()` calls chained in sequence on one expression.
- Flag any chain of > 2 method calls (e.g., `a.b().c().d()`) — Warning.
- Flag any chain of > 3 method calls — Critical.
- Property-only access chains (`a.b.c.d`) with no function calls are fine — this rule targets method chains.
- **Exception:** fluent builders (`.set().set().build()`) and query builders (`.where().orderBy().limit()`) are intentional. If every call in the chain returns the same type, it's a builder — downgrade to Style.

### Step 9: Detect Hidden Errors (Rule 12 — Fail Fast)

Scan for:

- Empty `catch {}` block — Critical.
- `catch (e) { }` or `catch (e) {}` with no body — Critical.
- `catch (e) { /* ... */ }` where the body contains only a comment — Critical.
- Python: `except:\n    pass` or `except Exception:\n    pass` — Critical.
- Python: bare `except:` with any body that does not log, rethrow, or return a typed error — Warning.
- `catch` that only does `console.log` with no rethrow on a non-recoverable operation (fetch, DB write) — Warning.

Scan for missing input checks on public functions:

- For every exported / public function, read the first 3 executable statements.
- If the function has parameters and none of the first 3 statements contain `throw`, `return`, `assert`, a comparison against the param (`if (!param)`, `if (param == null)`), or a type check — flag as Warning.
- Skip private / internal helper functions (not exported, starts with `_`, or inside a class as `private`).

### Step 10: Detect Test Quality (Rule 14 — AAA)

Only runs on files matching: `*.test.*`, `*.spec.*`, `test_*.py`, `*_test.go`.

For each test function (`it(...)`, `test(...)`, `def test_*`, `func Test*`):

- Flag if the body contains `if`, `for`, or `while` — Warning (tests should be straight-line).
- Count assertions (`expect(`, `assert `, `assertEqual`, etc.) — flag if > 3 distinct unrelated assertions — Warning.
- Flag if the test name is `test1`, `testUser`, `testIt`, or similar non-behavioral name — Style.
- Flag if the test name does not contain a verb or `should_` / `when_` prefix — Style.

### Step 11: Detect Unused Code Hints (Rule 13 — YAGNI)

- Flag exported symbols that have zero callers anywhere in the project — Style.
- Flag interfaces with exactly one implementation AND one caller — Style ("single-impl interface").
- Flag commented-out code blocks of ≥ 2 consecutive commented code-looking lines — Warning.

## Report Format

```
## cleancode Analysis: [filename]

### Summary
- Lines: [N] ([severity emoji] over limit / ✅ ok)
- Functions: [N] analyzed
- Violations: [N critical] 🔴, [N warnings] 🟡, [N style] 🔵

### 🔴 Critical
- [Line N] Function `name` is [X] lines (limit: 40)
- [Line N] Function `name` has [X] parameters (limit: 4)

### 🟡 Warnings
- [Line N] Function `name` is [X] lines — consider splitting
- [Line N] Class `Name` has no TypeScript interface
- [Line N] Generic name `data` — consider renaming to reveal intent

### 🔵 Style
- [Line N] Comment explains "what" — rename instead
- [Line N] TODO: "fix this later" — open a ticket

### Suggestions
1. Split `[LargestFunction]` into: `[suggestedPart1]`, `[suggestedPart2]`
2. Extract interface `I[ClassName]` for class `[ClassName]`
3. Consider splitting this file into: `[SuggestedFile1].ts`, `[SuggestedFile2].ts`

Run `/cleancode:rewrite [filename]` to see a cleaner version.
Run `/cleancode:teach [violation]` to learn about any violation.
```

## Multi-File Analysis

When `$ARGUMENTS` is empty or `.` (whole project):

1. Glob all source files (exclude: `node_modules`, `.git`, `dist`, `build`, `*.min.*`, `*.lock`)
2. For each file, count lines only (quick scan)
3. For files over 200 lines, run full analysis
4. Present summary table:

```
## Project Analysis

| File | Lines | Critical | Warnings | Style |
|------|-------|----------|----------|-------|
| src/services/user.ts | 487 🔴 | 3 | 5 | 2 |
| src/utils/helpers.ts | 312 🔴 | 1 | 3 | 0 |
| src/components/Form.tsx | 245 🟡 | 0 | 2 | 4 |

Total: 12 files scanned • 3 critical violations • 10 warnings

Worst offenders:
1. src/services/user.ts — 487 lines, 3 critical violations
2. src/utils/helpers.ts — 312 lines, monolith risk
```
