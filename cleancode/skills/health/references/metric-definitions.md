# Health Metric Definitions

Reference for `/cleancode:health`. Exact formulas and measurement rules.

---

## Scoring Formula

```
score = 100 − total_penalty
total_penalty = sum of (severity_weight × count) for every violation type
score = clamp(score, 0, 100)
```

### Weights

| Violation | Weight per occurrence |
|---|---|
| File > 300 lines | 5 |
| Function > 40 lines | 3 |
| Nesting > 4 | 2 |
| Method chain > 3 | 2 |
| Hidden error (empty catch, `except: pass`) | 3 |
| God class (> 10 public methods + > 200 lines) | 4 |
| File > 200 lines | 2 |
| Function > 20 lines | 1 |
| Method chain > 2 | 1 |
| Missing interface [TS] | 1 |
| Duplication block (3+ lines, 2+ occurrences) | 2 |
| Magic number | 0.5 |
| Bad name | 0.5 |

Style violations (weight < 1) round to 0 below 3 occurrences each (don't punish a project for 1 magic number).

### Score bands

| Score | Label |
|---|---|
| 90-100 | ✅ Excellent |
| 75-89  | 🟢 Good |
| 60-74  | 🟡 Needs attention |
| 40-59  | 🟠 Concerning |
| 0-39   | 🔴 Serious debt |

---

## Metric Definitions

### Lines of Code (LOC)

Count every line that is NOT:
- Blank (whitespace only)
- A comment-only line (`//`, `#`, `/* */`, `<!-- -->`)

### Function Length

Number of non-blank, non-comment-only lines between the function's `{` and matching `}` (or Python indent block).

### Nesting Depth

Track depth as `{`, `if`, `for`, `while`, `switch`, `try` increment; matching close decrements. Record max reached in each function.

Python: indent level / 4.

### Import Count

Count lines that start with `import` / `from ... import` / `require(` / `using`. Exclude:
- Standard library imports
- Type-only imports (`import type`)

### Interface Coverage (TypeScript only)

```
coverage = (# public classes with a matching interface) / (# public classes)
```

A "public class" is any `export class` or `export default class`. An "interface match" is an `interface I<ClassName>` or `interface <ClassName>` in the same file or imported.

Skip:
- `*.test.*`, `*.spec.*` files
- Classes inside React component files (UI components aren't services)

### Duplication

Simple approach (fast):

1. Split every file into 3-line sliding windows.
2. Hash each window (normalize whitespace).
3. Count hash collisions across files.
4. One "duplication block" = one hash seen in 2+ locations.

---

## Stability Requirements

The score must be deterministic:

- Same codebase → same score every run.
- Don't use random sampling for the quick scan.
- Round consistently (nearest integer, half to even).

---

## Performance Budget

For a 200-file project:

- Line counting: ≤ 2 seconds
- Function length + nesting: ≤ 5 seconds
- Duplication check: ≤ 3 seconds
- Total: ≤ 10 seconds

For projects > 1000 files, print a `Skipping deep analysis for large project` note and produce LOC-only metrics.

---

## History Tracking

When `.cleancode-health.md` exists, preserve its `## History` section and append today's row:

```markdown
| Date | Score | Critical | Warning | Style |
|---|---|---|---|---|
```

Keep at most 52 rows (roughly one year of weekly runs). If over, drop the oldest rows.
