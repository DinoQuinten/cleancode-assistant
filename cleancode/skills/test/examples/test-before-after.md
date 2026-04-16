# Test Rewrite Examples — Before & After

Full worked examples for the `/cleancode:test fix` skill. Each example shows the detected violations, the rewrite plan, and the final code.

---

## Example 1 — Multiple Unrelated Assertions + Bad Name

### Before (user.test.ts)

```typescript
import { User } from "../user";

describe("user tests", () => {
  it("test1", () => {
    const u = new User("Bob", 30);
    u.setRole("admin");
    u.setEmail("bob@example.com");
    expect(u.name).toBe("Bob");
    expect(u.age).toBe(30);
    expect(u.getRole()).toBe("admin");
    expect(u.email).toBe("bob@example.com");
    expect(u.canAccess("settings")).toBe(true);
  });
});
```

### Violations

- `test1` — bad name (Style)
- 5 unrelated assertions (Warning — Rule 14)
- No AAA structure (Warning)

### After

```typescript
import { User } from "../user";

describe("User", () => {
  it("new_user_has_provided_name_and_age", () => {
    // Arrange + Act
    const user = new User("Bob", 30);

    // Assert
    expect(user.name).toBe("Bob");
    expect(user.age).toBe(30);
  });

  it("user_reports_assigned_role", () => {
    // Arrange
    const user = new User("Bob", 30);

    // Act
    user.setRole("admin");

    // Assert
    expect(user.getRole()).toBe("admin");
  });

  it("user_stores_email", () => {
    // Arrange
    const user = new User("Bob", 30);

    // Act
    user.setEmail("bob@example.com");

    // Assert
    expect(user.email).toBe("bob@example.com");
  });

  it("admin_can_access_settings", () => {
    // Arrange
    const user = new User("Bob", 30);
    user.setRole("admin");

    // Act
    const canAccess = user.canAccess("settings");

    // Assert
    expect(canAccess).toBe(true);
  });
});
```

---

## Example 2 — For Loop in Test Body

### Before

```typescript
it("all roles work", () => {
  for (const role of ["admin", "user", "guest"]) {
    const u = new User("Bob", role);
    expect(u.getRole()).toBe(role);
    expect(u.canLogin()).toBe(true);
  }
});
```

### Violations

- `for` loop in test body (Warning)
- Multiple assertions (Warning)

### After

```typescript
describe("User role", () => {
  it.each(["admin", "user", "guest"])(
    "user_reports_role_%s",
    (role) => {
      // Arrange
      const user = new User("Bob", role);

      // Act
      const actualRole = user.getRole();

      // Assert
      expect(actualRole).toBe(role);
    }
  );

  it.each(["admin", "user", "guest"])(
    "user_with_role_%s_can_login",
    (role) => {
      // Arrange
      const user = new User("Bob", role);

      // Act
      const canLogin = user.canLogin();

      // Assert
      expect(canLogin).toBe(true);
    }
  );
});
```

---

## Example 3 — Shared Mutable State Across Tests

### Before

```typescript
let user: User; // module-level mutable

it("can set role", () => {
  user = new User("Bob");
  user.setRole("admin");
  expect(user.getRole()).toBe("admin");
});

it("can set email", () => {
  user.setEmail("x@y.com"); // ⚠ depends on previous test running first
  expect(user.email).toBe("x@y.com");
});
```

### Violations

- Shared mutable state (Warning — Rule 14)
- Test order dependency (silent bug risk)

### After

```typescript
describe("User", () => {
  it("admin_role_is_stored", () => {
    // Arrange
    const user = new User("Bob");

    // Act
    user.setRole("admin");

    // Assert
    expect(user.getRole()).toBe("admin");
  });

  it("email_is_stored", () => {
    // Arrange
    const user = new User("Bob");

    // Act
    user.setEmail("x@y.com");

    // Assert
    expect(user.email).toBe("x@y.com");
  });
});
```

Each test now creates its own `User` — no shared state, runs in any order.

---

## Example 4 — Python / pytest

### Before

```python
def test_user():
    u = User("Bob", 30)
    u.set_role("admin")
    for role in ["admin", "user", "guest"]:
        u.set_role(role)
        assert u.get_role() == role
    assert u.name == "Bob"
    assert u.age == 30
```

### After

```python
import pytest
from user import User


class TestUser:
    def test_new_user_has_provided_name(self):
        # Arrange + Act
        user = User("Bob", 30)

        # Assert
        assert user.name == "Bob"

    def test_new_user_has_provided_age(self):
        # Arrange + Act
        user = User("Bob", 30)

        # Assert
        assert user.age == 30

    @pytest.mark.parametrize("role", ["admin", "user", "guest"])
    def test_user_reports_assigned_role(self, role):
        # Arrange
        user = User("Bob", 30)

        # Act
        user.set_role(role)

        # Assert
        assert user.get_role() == role
```
