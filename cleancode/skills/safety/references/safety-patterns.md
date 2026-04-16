# Safety Detection Patterns

Reference for `/cleancode:safety`. Patterns for detecting silent errors and missing guards across languages.

---

## Hidden Error Patterns

### TypeScript / JavaScript

```
catch\s*\(\s*\w*\s*\)\s*\{\s*\}
catch\s*\{\s*\}
catch\s*\(\s*\w*\s*\)\s*\{\s*//[^\n]*\s*\}
```

All match an empty or comment-only catch block. Critical.

**Weak handling:**
```
catch\s*\(\s*(\w+)\s*\)\s*\{\s*console\.(log|error)\([^)]*\)\s*\}
```
Logs but does not rethrow. Warning.

```
catch\s*\(\s*\w*\s*\)\s*\{\s*return\s+(null|undefined|false|\[\]|\{\})\s*;?\s*\}
```
Returns a fake success value. Warning.

### Python

```
except\s*:\s*\n\s*pass
except\s+\w+\s*:\s*\n\s*pass
except\s+\w+\s+as\s+\w+\s*:\s*\n\s*pass
```
All Critical.

Bare `except:` (no exception type) — always Warning even with a body, because it catches `KeyboardInterrupt` and `SystemExit`.

### Java / C#

```
catch\s*\(\s*\w+\s+\w*\s*\)\s*\{\s*\}
catch\s*\(\s*Exception\s+\w*\s*\)\s*\{\s*\}
```
Critical.

### Go

Go uses explicit `err` values. Flag:
```
_\s*,\s*_\s*:?=\s*\w+\(
\w+\s*,\s*_\s*:?=\s*\w+\(
```
The underscore discards the error. Warning.

Also flag `if err != nil { }` — empty branch after an error. Critical.

---

## Missing Guard Clause Detection

For each function that is **public** (exported, non-underscore prefix, not `private`):

1. Parse the first 3 executable lines of the body (skip comments, blank lines).
2. Look for **guard patterns**:
   - `if (!x) throw ...`
   - `if (x == null) return ...`
   - `if (typeof x !== "...") throw ...`
   - `assert(x, "...")`
   - TypeScript type guard: `if (!isSomething(x)) throw ...`
   - Python: `if x is None: raise ...` / `assert x is not None`
   - Go: `if x == nil { return ..., errors.New(...) }`

If none of the first 3 lines contain any guard pattern AND the function has parameters that are used in the body, flag as Warning.

**Exceptions:**

- Constructor-like functions whose only job is to assign fields don't need guards beyond type checks (TS handles this).
- Functions wrapped by a validator (look for decorators like `@Validate`, `@Guard`, middleware patterns).
- Test files (`*.test.*`, `*.spec.*`, `test_*.py`).

---

## Division Check Detection

Regex: `/\s*\w+\b` (after a `/` with a variable divisor, excluding comments `//`).

For each match:

1. Look backward within the function for a check against zero: `if (x !== 0)`, `if (x > 0)`, `x || 1`, etc.
2. If none found and the divisor is a parameter or computed value, flag as Warning.

Skip:
- Division by constants (`/ 2`, `/ 100`).
- Division inside math expressions that are mathematically safe (`sqrt`, trig).

---

## Unchecked I/O Detection

Look for these calls without surrounding `try`, `.catch`, or error propagation:

**HTTP:**
- `fetch(` without `.catch` and not inside a `try`
- `axios(`, `axios.get(`, etc.
- `http.request(`, `https.request(`

**Filesystem:**
- `fs.readFileSync`, `fs.writeFileSync` (sync throws — must be in try)
- `fs.readFile`, `fs.writeFile` with callbacks that don't check `err` first

**Database:**
- Any `.query(`, `.execute(`, `.findOne(`, `.save(` without error handling

**Python:**
- `requests.get(`, `open(` without try or context manager that handles the error

Flag as Warning. Fix by wrapping in try/catch with logging + rethrow.

---

## Fix Templates

### Template 1: Replace silent catch with log + rethrow

```typescript
// Before
try {
  const user = await fetchUser(id);
  return user;
} catch (e) {}

// After (auto-applied)
try {
  const user = await fetchUser(id);
  return user;
} catch (e) {
  logger.error("fetchUser failed", { id, error: e });
  throw e;
}
```

If `logger` is not imported, add: `import { logger } from "./logger";` (or the detected logger import from other files in the same directory).

If no logger exists anywhere in the project, use `console.error` and warn the user in the report: "No logger found — used console.error; consider adding a real logger."

### Template 2: Guard clauses at function top

```typescript
// Before
export function login(email: string, password: string): User {
  const user = db.findUser(email);
  if (verifyPassword(user, password)) return user;
  throw new Error("Invalid credentials");
}

// After
export function login(email: string, password: string): User {
  if (!email) throw new Error("email required");
  if (!password) throw new Error("password required");

  const user = db.findUser(email);
  if (verifyPassword(user, password)) return user;
  throw new Error("Invalid credentials");
}
```

### Template 3: Division by zero check

```typescript
// Before
function averageScore(scores: number[]): number {
  return scores.reduce((a, b) => a + b, 0) / scores.length;
}

// After
function averageScore(scores: number[]): number {
  if (scores.length === 0) return 0;
  return scores.reduce((a, b) => a + b, 0) / scores.length;
}
```

### Template 4: Wrap I/O in try/catch

```typescript
// Before
export async function saveUser(user: User) {
  await db.insert("users", user);
}

// After
export async function saveUser(user: User): Promise<void> {
  if (!user) throw new Error("user required");

  try {
    await db.insert("users", user);
  } catch (e) {
    logger.error("saveUser failed", { userId: user.id, error: e });
    throw e;
  }
}
```

---

## Never Auto-Apply — Ask First

These patterns look silent but are often intentional:

- `catch (e) {}` around a cleanup call inside a `finally`-like retry
- `catch (NotFoundError) { return null }` — legitimate "return a default if missing"
- Node.js `process.on("uncaughtException", () => {})` — suppressing top-level crashes is a deliberate operational choice

For these:

1. Include them in the report.
2. Mark as "Manual review" instead of "Planned fix".
3. Suggest the change but require user confirmation of each instance individually.
