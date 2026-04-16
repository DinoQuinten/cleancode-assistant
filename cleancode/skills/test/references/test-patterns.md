# Test Detection Patterns

Reference for `/cleancode:test`. Per-framework patterns for extracting tests, measuring AAA, and detecting violations.

---

## Framework Detection

| Pattern in file | Framework |
|---|---|
| `describe(`, `it(`, `test(` + `expect(` | Jest / Vitest |
| `import pytest` or `def test_*` | pytest |
| `class *Test extends TestCase` or `@Test` | JUnit |
| `func Test*(t *testing.T)` | Go |
| `[Test]` or `[Fact]` attributes | xUnit / NUnit / MSTest |

---

## Test Extraction

### Jest / Vitest

```
it\s*\(\s*['"`]([^'"`]+)['"`]\s*,\s*(?:async\s*)?\(\s*\)\s*=>\s*\{
test\s*\(\s*['"`]([^'"`]+)['"`]\s*,\s*(?:async\s*)?\(\s*\)\s*=>\s*\{
```

Capture the test name from group 1; the body starts after the `{` and ends at the matching `}`.

### pytest

Each `def test_*(` at module level or inside a `Test*` class is a test. The body is the indented block.

### Go

`func Test*(t *testing.T) {` — body is the `{}` block.

---

## AAA Detection

A test has "clear AAA" if any of these is true:

1. **Comment markers:** body contains `// Arrange`, `// Act`, `// Assert` (or `# Arrange`, `# Act`, `# Assert`).
2. **Blank-line separation:** body has at least 2 blank lines dividing setup / action / assertion.
3. **Three-line body:** total ≤ 4 code lines — considered trivially AAA by inspection.

A test is "missing AAA" if it has > 4 lines and no clear separation.

---

## Control Flow Detection

Scan the test body (excluding nested arrow functions / inner test helpers) for:

- `\bif\s*\(` — flag
- `\bfor\s*\(` — flag
- `\bwhile\s*\(` — flag
- `\bswitch\s*\(` — flag
- Python: `^\s*(if|for|while)\s+` inside the test function indent

Skip:
- `if` inside a mock implementation (e.g., `mockFn.mockImplementation((x) => { if (x > 0) ... })` — that's fake code, not test code).

---

## Assertion Counting

### Jest / Vitest

```
expect\(
```

Each `expect()` chain counts as one assertion — even if it has multiple matchers like `.toBe().toBeDefined()`.

### pytest

```
\bassert\s+
```

Each line starting with `assert` counts.

### JUnit / xUnit

```
assertEquals\(|assertTrue\(|assertFalse\(|assertNotNull\(|assertThat\(
Assert\.\w+\(
```

---

## Bad Name Detection

Flag if the test name matches any of:

- `^test\d+$` — `test1`, `test2`
- `^it\d+$` — `it1`
- Exact matches: `testIt`, `itWorks`, `testUser`, `testMethod`
- No verb AND no `should_` / `when_` / `given_` prefix (check against common verb list)
- Length > 80 chars
- Single word (e.g., `login`, `user`)

**Good name patterns:**
- `should_<verb>_<noun>_when_<condition>` (e.g., `should_return_error_when_password_is_blank`)
- `<subject>_<action>_when_<condition>` (e.g., `admin_can_access_settings_when_logged_in`)
- `given_<precondition>_<action>_<expected>` (e.g., `given_empty_cart_checkout_throws`)

---

## Shared State Detection

Scan the module (outside test functions) for:

- `let <name> = ` — mutable binding at module level
- Python: module-level assignments not inside `def` or `class`
- Properties on a shared fixture that's modified inside tests

Flag if a test body **writes** to such a binding (not just reads).

---

## Fix Templates

### Rename

Derive a new name from:
1. The primary subject (first noun in the test body after arrange).
2. The primary action (verb on the subject).
3. The assertion (what's being checked).

Format: `<subject>_<action>_<condition>` in snake_case (or `should<Verb><Result>When<Condition>` in camelCase — match the file's existing style).

### Split multi-assertion test

For a test with N unrelated assertion groups, emit N tests:

```typescript
// Before
it("test1", () => {
  const user = new User("Bob");
  user.setRole("admin");
  expect(user.name).toBe("Bob");
  expect(user.getRole()).toBe("admin");
  expect(user.canAccess("settings")).toBe(true);
});

// After
it("new_user_has_name", () => {
  const user = new User("Bob");
  expect(user.name).toBe("Bob");
});

it("user_reports_assigned_role", () => {
  const user = new User("Bob");
  user.setRole("admin");
  expect(user.getRole()).toBe("admin");
});

it("admin_can_access_settings", () => {
  const user = new User("Bob");
  user.setRole("admin");
  expect(user.canAccess("settings")).toBe(true);
});
```

### Split for loop

```typescript
// Before
it("roles", () => {
  for (const role of ["admin", "user", "guest"]) {
    const user = new User("Bob", role);
    expect(user.getRole()).toBe(role);
  }
});

// After
it.each(["admin", "user", "guest"])("user_reports_role_%s", (role) => {
  const user = new User("Bob", role);
  expect(user.getRole()).toBe(role);
});
```

Use the framework's parameterized-test feature (`it.each` in Jest, `@pytest.parametrize` in pytest, table tests in Go) when the only reason the loop existed was parameterization. Otherwise emit N separate tests.

### Add AAA structure

Insert blank lines to separate the three phases:

```typescript
// Before
it("login", () => {
  const user = new User("Bob");
  user.setPassword("secret");
  const result = user.login("secret");
  expect(result).toBe(true);
});

// After
it("user_can_login_with_correct_password", () => {
  // Arrange
  const user = new User("Bob");
  user.setPassword("secret");

  // Act
  const result = user.login("secret");

  // Assert
  expect(result).toBe(true);
});
```
