# .cursorrules Template

This template is written to `.cursorrules` in the project root by `/cleancode:setup cursor`.

```
# Clean Code Rules — enforced by cleancode plugin
# Source of truth: .cleancode-rules.md
# Run /cleancode:init to regenerate this file

## Code Quality Standards

ALWAYS follow these rules when writing or editing any code in this project:

### File Size
- Keep all files under 300 lines of code
- If adding new code would push a file past 300 lines, propose splitting it first
- Each file must represent one single concept or responsibility

### Function Size
- Keep all functions and methods under 40 lines
- The ideal function length is 10-20 lines
- If a function needs more, extract sub-operations into named helper functions

### Parameters
- Maximum 4 parameters per function
- When more are needed, group them into a typed object
- TypeScript: create a named interface for the parameter object

### Nesting
- Maximum nesting depth of 4 levels
- Use early returns and guard clauses to reduce nesting
- Never wrap the happy path in conditionals

### Naming
- Every name must reveal its intent without needing a comment
- Variables: noun or noun phrase (userAccount, not obj or x)
- Functions: verb + noun (calculateTax, not calc)
- Classes: noun (OrderProcessor, not Manager)
- No single-letter names except loop counters (i, j, k)
- No abbreviations unless universally known

### Object-Oriented Design
- Apply SOLID principles
- Each class has one responsibility (Single Responsibility Principle)
- Prefer composition over inheritance
- Small, focused classes over large, general ones

### TypeScript Interfaces
- Every public-facing class, service, or repository must have an explicit interface
- Depend on interfaces, not concrete classes
- Constructor injection: always inject by interface
- Use interfaces for all parameter objects (4+ params)

### DRY
- No logic duplicated more than once
- Extract shared logic to named utilities
- If you copy-paste 3+ lines, extract a function

### Comments
- Comments explain WHY, never WHAT
- The code itself explains what it does
- No commented-out code
- No TODO comments in committed code

### Don't Reach Through Objects (Law of Demeter)
- A function talks only to objects it holds directly
- Avoid chains like `a.b().c().d()` — add a helper on `a` instead
- Fluent builders and array chains are fine
- Max method chain depth: 2

### Check Inputs Early, Never Hide Errors (Fail Fast)
- Public functions validate inputs at the top (guard clauses)
- Never use empty `catch {}` or `except: pass` — errors must log, rethrow, or translate
- If something goes wrong, let it show — don't swallow it silently

### Only Build What You Need (YAGNI + Boy Scout)
- Don't add code "just in case" — wait until there's a real need
- Delete unused flags, single-implementation interfaces, and dead code
- When you touch a file, fix small issues you notice

### Tests Should Be As Clean As The Code (AAA)
- Every test has three blocks: Arrange, Act, Assert
- Name tests after the behavior they verify (`should_reject_expired_token`)
- One idea per test — no `if`/`for`/`while` inside test bodies
- Don't share mutable state between tests

### Clean Module & Folder Structure (dynamic — adapts to the project)
- The top-level folder tree should read like a table of contents — a new reader should guess the domain from folder names alone
- Group files by what changes together, not by technical layer — prefer `auth/`, `billing/`, `orders/` over one big `controllers/` + `services/` split when the project has multiple domains
- Be skeptical of catch-all folders (`utils/`, `helpers/`, `common/`, `misc/`, `shared/`) — a few genuine helpers are fine; a growing pile is a missing domain folder
- Follow the language/framework grain: Rails, Next.js, Go packages, Java Maven, Rust `mod.rs` all have their own conventions — honor the ecosystem first
- Size shapes structure: small projects want flat, mid-size wants grouping, large wants nested domains — no universal template
- Test files colocate with code in TS/JS/Python; parallel test trees are idiomatic in Java and Rust
- This is a style-level rule — treat as a dynamic hint, never a blocker, never auto-fixed

## Violation Handling

When you identify a violation while writing code:
- Complete the task first
- Add a non-blocking suggestion at the end of your response
- Format: "Clean code suggestion: [what to fix] — [why]"
- Do NOT refuse to write code because of a potential violation

## Human Readability Test

Before finalizing any file, ask:
- Can I describe this file's purpose in one sentence without using "and"?
- Would a new contributor understand this file in 5 minutes?
- Are all names clear without reading the implementation?
- Does every function do exactly what its name says (no hidden side effects)?
```
