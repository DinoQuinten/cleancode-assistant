---
name: Clean Code Safety
description: This skill should be used when the user asks to "check error handling", "find silent failures", "fix silent errors", "add input checks", "fail fast", "make this safer", "check for hidden errors", "defensive programming", or mentions empty catch blocks, swallowed exceptions, or missing validation. Detects and optionally fixes Rule 12 violations — silent error swallowing and missing guard clauses.
argument-hint: "[file-path] [fix]"
allowed-tools: Read, Write, Edit, Grep
version: 0.2.0
---

# Clean Code Safety

Find and (optionally) repair places where the code quietly fails or skips checks. Targets Rule 12 — Check Inputs Early, Never Hide Errors (Fail Fast / Defensive Programming).

## When This Runs

- User asks to check error handling, find silent failures, or add guards
- Analyze reports Rule 12 violations and user wants them fixed
- `/cleancode:fix` delegates safety fixes to this skill

## Modes

| Invocation | Behavior |
|---|---|
| `/cleancode:safety <file>` | Report only — list silent catches and missing guards |
| `/cleancode:safety <file> fix` | Plan the fix, show diff, then apply via Edit |
| `/cleancode:safety .` | Report across the whole project |

Default is **report mode**. Only write when `fix` is passed.

## Step 1: Detect Violations

Read the target file. Scan for:

### A. Hidden errors (Critical)

- Empty `catch {}` block
- `catch (e) { }` with no body
- `catch (e) { /* comment only */ }`
- Python `except: pass` or `except Exception: pass`
- `catch` that only suppresses without logging or rethrowing

### B. Weak error handling (Warning)

- `catch (e) { console.log(e) }` with no rethrow on a write operation
- `catch (e) { return null }` that hides a real failure from callers
- Bare `except:` in Python that catches all exceptions

### C. Missing guard clauses (Warning)

For every **public / exported** function with parameters:

1. Read the first 3 executable statements.
2. If none of them validate a parameter (via `throw`, `return`, `assert`, comparison, or type guard), flag as Warning.

### D. Missing zero / null divisor check (Warning)

- Any `/` operator where the divisor is a parameter or computed value with no preceding check.

### E. Unchecked I/O (Warning)

- `fetch(...)`, `await axios(...)`, DB `query(...)` without surrounding error handling or `.catch()`.
- File I/O (`readFileSync`, `fs.writeFile`) without error handling.

See `references/safety-patterns.md` for full detection patterns per language.

## Step 2: Report

```
cleancode safety — [file]

🔴 Critical — hidden errors
  • auth.ts:47 — empty `catch (e) {}` block
      Why: errors from `verifyToken()` are silently dropped, users may be authed as wrong user
      Fix: log + rethrow, or translate to a typed error

🟡 Warnings — missing guards
  • auth.ts:12 — `login(email, password)` — no input validation
      Why: a null email or empty password will reach the DB layer and fail with a confusing error
      Fix: add `if (!email) throw new Error("email required")` at function top

  • payments.ts:89 — division by `count` with no zero check
      Fix: `if (count === 0) return 0` before the division

Report only. Pass `fix` to apply these changes.
```

In report mode, stop here.

## Step 3: Plan Fixes (fix mode only)

For each violation, compute the concrete edit.

### Hidden errors — replace silent catch

Rules:
- **Never auto-delete a catch block** — the developer may have intended to suppress.
- Replace silent catches with a **safe default** that both logs AND lets the caller know:

```typescript
// Before
try { return riskyOp() } catch (e) {}

// After (applied)
try {
  return riskyOp();
} catch (e) {
  logger.error("riskyOp failed", { error: e });
  throw e; // rethrow so caller knows
}
```

If no logger is imported, add an import. If the function's return type allows `null` or an error type, prefer returning a typed error over rethrow — show both options and ask.

### Missing guard clauses — add at function top

Insert guards before the first existing statement. For each param:

- `string` param → `if (!param) throw new Error("param required")`
- `number` param → `if (typeof param !== "number" || isNaN(param)) throw new Error("param must be a number")`
- Object param → `if (!param) throw new Error("param required")` plus check required fields

Only add guards for parameters actually used inside the function (don't add noise for unused params).

### Division guards

Before the division: `if (divisor === 0) throw new Error("divisor is zero")` — or return a sensible default if the function already returns nullable.

### I/O error handling

Wrap in try/catch with logging + rethrow, or add `.catch(err => { ... throw err })` for promise chains.

## Step 4: Show Diff, Confirm

```
Planned fixes:

1. auth.ts:47  — replace empty catch with log + rethrow
2. auth.ts:12  — add guard: `if (!email) throw ...`
3. auth.ts:13  — add guard: `if (!password) throw ...`
4. payments.ts:89 — add zero check before division

Total: 2 files, 4 edits.
Apply? (yes / dry run / no)
```

Wait for confirmation. Apply via Edit.

## Step 5: Dangerous Suggestions — Never Auto-Apply

Some catches look silent but are intentional:

- `catch (e) {}` directly around a known-idempotent cleanup (a best-effort retry loop)
- Swallowing a `NotFound` error and returning a default

**Always show these as suggestions and ask the user.** Never silently replace a catch that might be intentional.

## Step 6: Verify

After applying:

1. Re-read the touched files.
2. Re-scan for the same violation types.
3. Print: `✓ 4 safety fixes applied. 0 violations remaining.`

## Additional Resources

- **`references/safety-patterns.md`** — full regex for each detection, language-specific handling, and example fixes
