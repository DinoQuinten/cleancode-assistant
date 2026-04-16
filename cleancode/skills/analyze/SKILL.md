---
name: Clean Code Analyze
description: This skill should be used when the user asks to "analyze this file", "check this code", "scan for violations", "find clean code issues", "review code quality", "check file length", "audit this project", "what's wrong with this code", or when a file looks messy or overly long. Scans files for clean code violations and outputs a grouped report of critical issues, warnings, and style suggestions.
argument-hint: "[file-path or . for whole project]"
allowed-tools: Read, Glob, Grep
version: 0.1.0
---

# Clean Code Analyze

Scan one file or the whole project for clean code violations. Output a grouped report (Critical / Warning / Style) with specific line numbers and actionable suggestions.

## Thresholds (Quick Reference)

| Metric | Critical | Warning |
|---|---|---|
| File length | > 300 lines | > 200 lines |
| Function length | > 40 lines | > 20 lines |
| Parameter count | > 4 | = 4 |
| Nesting depth | > 4 | = 4 |

For full thresholds including naming, TypeScript interfaces, OOP, and duplication detection — see `references/thresholds.md`.

## Single File Analysis

When `$ARGUMENTS` is a file path:

1. **Read the file** — get full content and line count
2. **Extract all functions/methods** — record name, start line, line count, parameter count
3. **Measure nesting depth** — track depth through the file, record max per function
4. **Check naming** — scan for generic names, short names, type encodings
5. **TypeScript check** — for `.ts`/`.tsx` files, check for missing interfaces on public classes
6. **Detect duplication** — find repeated 3+ line blocks
7. **Find comments** — flag commented-out code and TODOs

For detailed detection rules and patterns by language, see `references/detection-rules.md`.

### Report Format

Present findings as:

```
## cleancode Analysis: [filename]

### Summary
- Lines: [N] (🔴 over limit | ✅ ok)
- Functions: [N] analyzed
- Violations: [N critical] 🔴, [N warnings] 🟡, [N style] 🔵

### 🔴 Critical
- Line [N]: Function `name` is [X] lines (limit: 40)
- Line [N]: Function `name` has [X] parameters (limit: 4)

### 🟡 Warnings  
- Line [N]: File is [X] lines — approaching 300-line limit
- Line [N]: Class `Name` has no TypeScript interface

### 🔵 Style
- Line [N]: Name `data` is generic — consider something more specific
- Line [N]: TODO comment — open a ticket instead

### Suggestions
1. Split `[bigFunction]` into: `[part1]`, `[part2]`
2. Extract interface `I[ClassName]` for class `[ClassName]`

Run /cleancode:rewrite [file] to see a cleaner version.
Run /cleancode:teach [violation] to understand any principle.
```

## Whole Project Analysis

When `$ARGUMENTS` is empty, `.`, or not provided:

1. **Glob all source files** — exclude `node_modules`, `.git`, `dist`, `build`, `*.min.*`, `*.lock`, `*.generated.*`
2. **Quick line scan** — count lines for every file
3. **Deep scan only files over 150 lines** — run full analysis on those
4. **Present project summary table** then list worst offenders

```
## Project Analysis

| File | Lines | 🔴 | 🟡 | 🔵 |
|------|-------|----|----|-----|
| src/services/user.ts | 487 🔴 | 3 | 5 | 2 |
| src/utils/helpers.ts | 312 🔴 | 1 | 3 | 0 |

Top 3 files to fix first:
1. [file] — [reason]
2. [file] — [reason]  
3. [file] — [reason]
```

## Language-Specific Rules

Apply these adjustments per detected language:

- **TypeScript/JavaScript**: Interface check enabled. Test files (`*.test.*`, `*.spec.*`) use relaxed limits (500 lines).
- **Python**: Docstrings count as lines. `__init__.py` exempt from file length.
- **Java/C#**: 300 non-blank lines max. Interfaces already language-native — enforce usage.
- **Go**: Error handling pattern (`if err != nil`) doesn't count toward nesting depth.

## After Analysis

Always end with next steps:
- Point to `/cleancode:rewrite [file]` for the worst violating file
- Point to `/cleancode:teach [violation]` for the most common violation type
- If no violations: `✅ [filename] passes all clean code checks.`

## Additional Resources

### Reference Files

- **`references/thresholds.md`** — Full threshold table for all metrics, all languages, and severity levels. Read when deciding borderline cases.
- **`references/detection-rules.md`** — Step-by-step detection algorithm, patterns for each language, and full report format. Read for detailed implementation of the analysis steps.
