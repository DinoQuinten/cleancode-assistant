# Clean Code Violation Thresholds

## Severity Levels

| Severity | Meaning | Display |
|---|---|---|
| Critical | Must fix before shipping | 🔴 |
| Warning | Should fix soon | 🟡 |
| Style | Nice to fix | 🔵 |

## File-Level Thresholds

| Metric | Critical | Warning | Style |
|---|---|---|---|
| Lines of code | > 300 | > 200 | > 150 |
| Number of classes/functions in file | > 10 | > 7 | > 5 |
| Import count | > 20 | > 15 | — |

## Function/Method-Level Thresholds

| Metric | Critical | Warning | Style |
|---|---|---|---|
| Lines of code | > 40 | > 20 | > 15 |
| Parameter count | > 4 | = 4 | — |
| Nesting depth | > 4 | = 4 | = 3 |
| Return points | > 5 | > 3 | — |
| Cyclomatic complexity* | > 15 | > 10 | > 7 |

*Cyclomatic complexity: count each `if`, `else if`, `for`, `while`, `case`, `&&`, `||`, `?` as +1 starting from 1.

## Naming Thresholds

| Issue | Severity |
|---|---|
| Variable name ≤ 1 char (non loop var) | Warning |
| Variable name ≤ 2 chars | Style |
| Name is abbreviation (not in approved list) | Style |
| Name contains type encoding (e.g., `strName`, `bFlag`) | Style |
| Name is generic (`data`, `info`, `manager`, `util`, `helper`) | Warning |
| Function name is not verb-noun | Style |
| Class name is not noun | Style |

**Approved abbreviations:** `id`, `url`, `api`, `db`, `btn`, `img`, `ctx`, `req`, `res`, `err`, `fn`, `cb`, `i`, `j`, `k`, `n`, `x`, `y`

## Comment Thresholds

| Issue | Severity |
|---|---|
| Commented-out code block (≥ 2 lines) | Warning |
| TODO / FIXME / HACK comment | Style |
| Comment explains "what" not "why" | Style |
| File has no comments at all (> 100 lines) | Style |

## TypeScript-Specific Thresholds

| Issue | Severity |
|---|---|
| Public class/service with no interface | Warning |
| Function parameter typed as `any` | Warning |
| Variable typed as `any` | Warning |
| Missing return type on public function | Style |
| Interface with > 15 properties | Warning |
| Type assertion `as X` without comment | Style |

## OOP Thresholds

| Issue | Severity |
|---|---|
| Class with > 10 public methods | Critical |
| Class with > 20 total methods | Critical |
| Class with > 15 properties/fields | Warning |
| Constructor with > 5 parameters | Critical |
| `extends` chain > 3 levels deep | Warning |
| File mixing multiple unrelated classes | Warning |

## Coupling Thresholds (Rule 11 — Law of Demeter)

| Issue | Threshold | Severity |
|---|---|---|
| Method chain depth (`a.b().c().d()`) | > 2 calls | Warning |
| Method chain depth | > 3 calls | Critical |
| File imports from N other modules | > 10 | Warning |
| File imports from N other modules | > 15 | Critical |
| Circular imports detected | any | Critical |

## Error Handling Thresholds (Rule 12 — Fail Fast)

| Issue | Severity |
|---|---|
| Empty `catch {}` block | Critical |
| Empty `catch (e) {}` with no rethrow or log | Critical |
| `except: pass` (Python) | Critical |
| Public function with no input validation (first statement uses a param) | Warning |
| Division without zero check on non-constant divisor | Warning |
| External I/O (fetch, file, DB) without error handling | Warning |

## Test Quality Thresholds (Rule 14 — AAA)

| Issue | Severity |
|---|---|
| Test body contains `if` / `for` / `while` | Warning |
| Test asserts more than 3 separate conditions | Warning |
| Test name doesn't describe behavior (no verb or `should_` prefix) | Style |
| Test shares mutable state with other tests (module-level mutable var) | Warning |
| Test name like `test1`, `testUser`, `testIt` | Style |

## Unused Code Thresholds (Rule 13 — YAGNI)

| Issue | Severity |
|---|---|
| Exported symbol with zero callers in the project | Style |
| Interface with exactly one implementation and one caller | Style |
| Feature flag / config option with no reads | Style |
| Parameter declared but never used in function body | Style |

## Duplication Detection

Duplication is flagged when:
- 3+ consecutive identical or near-identical lines appear in multiple locations
- A pattern (loop + same logic) repeats 3+ times in the same file
- Identical function body found in 2+ locations

## Language-Specific Notes

### TypeScript / JavaScript
- Arrow functions count toward file line total
- JSX/TSX: component file max is still 300 lines
- Test files (`*.test.*`, `*.spec.*`): relaxed — 500 lines max, no interface requirement

### Python
- Docstrings count as lines
- `__init__.py` exempt from file length (usually just re-exports)
- Type hints treated same as TS: missing hints on public functions = Style violation

### Java / C#
- Longer due to verbosity: file max is 300 non-blank lines
- Interfaces are already part of the language — enforce their usage

### Go
- Functions: still 40 lines max
- Error handling patterns don't count toward nesting depth
