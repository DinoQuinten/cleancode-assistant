---
name: test
description: This skill should be used when the user asks to "check my tests", "clean up my tests", "fix my tests", "are my tests clean", "review this test file", "AAA pattern", "tests should be clean", or mentions messy tests, test naming, or tests that have loops or conditionals. Detects and optionally fixes Rule 14 violations — tests missing the Arrange / Act / Assert structure, bad test names, or control flow inside tests.
argument-hint: "[test-file-path] [fix]"
allowed-tools: Read, Write, Edit, Grep, Glob
version: 0.2.0
---

# Clean Code Test

Find and (optionally) clean up messy tests. Targets Rule 14 — Tests Should Be As Clean As The Code They Test (Developer Testing — AAA).

## When This Runs

- User asks to check, review, or clean up a test file
- Analyze reports Rule 14 violations
- `/cleancode:fix` delegates test cleanup to this skill when the target is a test file

## Modes

| Invocation | Behavior |
|---|---|
| `/cleancode:test <file>` | Report only — list messy tests |
| `/cleancode:test <file> fix` | Plan the rewrites, show diff, then apply |

Default is **report mode**.

## Step 1: Confirm This Is a Test File

Only run on files matching:
- `*.test.ts`, `*.test.tsx`, `*.test.js`, `*.test.jsx`
- `*.spec.ts`, `*.spec.tsx`, `*.spec.js`, `*.spec.jsx`
- `test_*.py`, `*_test.py`
- `*_test.go`
- `*Test.java`, `*Tests.cs`

If the file is not a test file, say so and stop.

## Step 2: Extract Each Test

For each test function in the file (`it(...)`, `test(...)`, `def test_*`, `func Test*`), record:

- Test name
- Start and end line
- Body (everything between the `{` and matching `}`, or the Python indented block)
- Assertion count (`expect(`, `assert`, `assertEqual`, etc.)
- Whether the body contains `if`, `for`, or `while`
- Whether the body has clear AAA sections (comments, blank lines, or obvious structural split)

## Step 3: Detect Violations

For each test, flag:

### Missing AAA structure (Warning)

A test is "missing AAA" if it has **more than 4 lines of code** AND there are no clear Arrange / Act / Assert boundaries (no blank lines separating setup, action, and assertion; no `// Arrange`, `// Act`, `// Assert` comments).

### Control flow inside test body (Warning)

Any `if`, `for`, `while`, or `switch` inside a test body. Tests should assert against specific inputs, not iterate.

### Multiple unrelated assertions (Warning)

More than 3 distinct assertions. "Distinct" means asserting different properties or different behaviors — `expect(x).toBe(1); expect(x).toBeDefined();` counts as related; `expect(user.name).toBe("x"); expect(user.age).toBe(30); expect(emailSent).toBe(true);` counts as 3 distinct.

### Bad test names (Style)

- `test1`, `test2`, `testUser`, `testIt`, `itWorks`
- Names with no verb or `should_` / `when_` / `given_` prefix
- Names longer than 80 chars

### Shared mutable state (Warning — report only)

Module-level `let` / mutable vars that are modified inside tests. Tests should be order-independent. This one is **reported but never auto-fixed**: rewriting shared state safely requires understanding the test's intent (is the shared object a real collaborator, a fixture, or a leak?). The report names the variable + file:line and suggests moving the setup into a per-test factory or `beforeEach`, but the rewrite is a human decision.

See `references/test-patterns.md` for detection patterns per framework.

## Step 4: Report

```
cleancode test — [file]

🟡 Warnings
  • user.test.ts:14 — test `test1` has a `for` loop
      Why: tests should be straight-line; iteration hides which input caused a failure
      Fix: split into one test per iteration

  • user.test.ts:14 — test name `test1` doesn't describe behavior
      Fix: rename to `admin_can_login` or `guest_without_role_cannot_login`

  • user.test.ts:42 — 5 assertions checking unrelated things (name, age, role, email, login state)
      Fix: split into separate tests

Report only. Pass `fix` to apply rewrites.
```

In report mode, stop.

## Step 5: Plan Rewrites (fix mode only)

### Split a multi-assertion test

Identify the groups of related assertions. Create one test per group. Each gets a descriptive name derived from what it checks.

### Split a test containing a loop

For each iteration value, emit one test with that value substituted. Use the loop variable in the test name to keep them distinct.

### Rename bad test names

Derive a new name from what the test does:
- `test1` → read the assertions, extract the subject + verb → `should_return_user_when_id_exists`
- `testUser` → `new_user_has_default_role` (based on what's actually asserted)

Use `should_X_when_Y` or `X_when_Y` as the pattern. Keep under 70 chars.

### Add AAA structure

Insert blank lines between setup, action, and assertion. Optionally add `// Arrange`, `// Act`, `// Assert` comments — but prefer structure over comments.

See `examples/test-before-after.md` for full worked examples of each transformation.

## Step 6: Show Diff, Confirm

```
Planned rewrites in user.test.ts:

1. Line 14 — split test `test1` (for loop, 3 iterations) into 3 tests:
   - `admin_can_login`
   - `user_can_login`
   - `guest_can_login`

2. Line 42 — split `test2` (5 unrelated assertions) into 3 tests:
   - `new_user_has_provided_name_and_age`
   - `new_user_has_default_role`
   - `new_user_triggers_welcome_email`

3. Line 78 — rename `testIt` → `should_reject_expired_session`

Total: 1 file, 5 new tests, 2 removed.
Apply? (yes / dry run / no)
```

Wait for confirmation. Apply via Write (cleaner to rewrite the block than to Edit many pieces).

## Step 7: Verify

After applying:

1. Re-read the test file.
2. Re-run Step 2 and Step 3.
3. If the user has a test runner configured (look for `package.json`, `pytest.ini`, etc.), suggest running the tests to make sure nothing broke: `suggest: run "npm test" to verify`.
4. Print: `✓ 5 tests rewritten. 0 messy tests remaining. Run your test suite to confirm they all pass.`

## Rules for Rewrites

- **Never change what the test actually asserts** — only restructure.
- **Never delete a test without user approval.** If an assertion is questionable, flag it but keep it.
- **Preserve setup dependencies** — if a test depends on a `beforeEach`, keep the dependency intact.
- **Use the framework's idioms** — use `describe` / `it` for Jest, `class Test...` for pytest, etc.

## Additional Resources

- **`references/test-patterns.md`** — per-framework detection regex, AAA structural markers, naming templates
- **`examples/test-before-after.md`** — full before/after examples for each rewrite type
