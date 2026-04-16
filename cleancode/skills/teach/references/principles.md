# Clean Code Principles Reference

## Principle Map: Violation → Principle → Book Citation

---

### file-too-long / monolith

**Principle:** Single Responsibility Principle (SRP)
**Rule:** A file should represent one concept and one responsibility.

**Book citations:**
- *Code Complete 2nd Ed.*, Chapter 5 — "A class should have one reason to change." If you find yourself saying "and" when describing what a file does, it's doing too much.
- *The Art of Clean Code*, Chapter 5 — "A module should be responsible to one, and only one, actor."

**Why it matters:** A 600-line file is a module that has absorbed multiple responsibilities over time. Every change to it risks breaking something unrelated. New contributors take 10x longer to understand it.

**Fix:** Identify the distinct responsibilities in the file. Extract each into its own file with a name that clearly describes it.

**Counter-example:**
```typescript
// ❌ userUtils.ts — 450 lines containing:
// - User authentication
// - User formatting / display
// - User database queries
// - Email sending
// - Permission checking

// ✅ Split into:
// auth/userAuth.ts
// formatting/userFormatter.ts
// repositories/userRepository.ts
// email/userEmailService.ts
// permissions/userPermissions.ts
```

---

### function-too-long

**Principle:** Do One Thing
**Rule:** A function does one thing if you cannot meaningfully extract another function from it.

**Book citations:**
- *The Art of Clean Code*, Chapter 3 — "Functions should do one thing. They should do it well. They should do it only."
- *Code Complete 2nd Ed.*, Chapter 7 — "The ideal function length is somewhere between 1 and 25 executable lines of code."

**Why it matters:** Long functions accumulate multiple levels of abstraction. The reader must hold all of it in their head. Short functions have names that document intent.

**Fix:** Extract sub-operations into named functions. The parent function becomes a sequence of high-level steps — readable like a table of contents.

**Counter-example:**
```typescript
// ❌ 80-line processOrder() that:
// 1. Validates input
// 2. Calculates tax
// 3. Checks inventory
// 4. Charges payment
// 5. Sends confirmation email
// 6. Updates analytics

// ✅ processOrder() becomes 6 lines:
function processOrder(order: IOrder): OrderResult {
  validateOrder(order);
  const tax = calculateTax(order);
  checkInventory(order);
  chargePayment(order, tax);
  sendConfirmation(order);
  trackAnalytics(order);
}
```

---

### too-many-parameters

**Principle:** Parameter Objects / Interface Segregation
**Rule:** When a function takes more than 4 parameters, the parameters belong together in an object.

**Book citations:**
- *The Art of Clean Code*, Chapter 3 — "The ideal number of arguments for a function is zero... More than three (polyadic) requires very special justification."
- *Code Complete 2nd Ed.*, Chapter 7 — "Limit the number of a routine's parameters to about seven."

**Why it matters:** Long parameter lists signal that related data belongs together. They also make call sites hard to read — which parameter is which?

**Fix:** Group related parameters into a typed interface. The function signature becomes self-documenting.

**Counter-example:**
```typescript
// ❌ createUser(name, email, role, department, managerId, startDate, isRemote)

// ✅ 
interface ICreateUserParams {
  name: string;
  email: string;
  role: UserRole;
  department: string;
  managerId: string;
  startDate: Date;
  isRemote: boolean;
}
function createUser(params: ICreateUserParams): User
```

---

### deep-nesting

**Principle:** Guard Clauses / Early Return
**Rule:** Return early for invalid conditions. Don't wrap the happy path in conditionals.

**Book citations:**
- *Code Complete 2nd Ed.*, Chapter 19 — "Use guard clauses (early returns) to reduce nesting."
- *The Art of Clean Code*, Chapter 3 — "Blocks within if/else/while statements should be one line long. That line should probably be a function call."

**Why it matters:** Deep nesting forces the reader to track multiple conditions simultaneously. The happy path is buried inside layers.

**Fix:** Invert conditions and return early. Extract nested blocks into named functions.

**Counter-example:**
```typescript
// ❌ 5 levels of nesting
function process(user) {
  if (user) {
    if (user.isActive) {
      if (user.hasPermission) {
        if (user.data) {
          // actual work — buried on level 5
        }
      }
    }
  }
}

// ✅ Guard clauses
function process(user: IUser): void {
  if (!user) return;
  if (!user.isActive) return;
  if (!user.hasPermission) throw new PermissionError();
  if (!user.data) throw new DataError();

  // actual work — at top level
}
```

---

### bad-naming

**Principle:** Intention-Revealing Names
**Rule:** A name is good when you never need a comment to explain what it is.

**Book citations:**
- *Code Complete 2nd Ed.*, Chapter 11 — "The most important naming consideration is that the name fully and accurately describe the entity the variable represents."
- *The Art of Clean Code*, Chapter 2 — "If a name requires a comment, then the name does not reveal its intent."

**Why it matters:** Good names are the cheapest form of documentation. They survive refactoring. They never go out of sync.

**Fix:** Ask: what does this hold? What does this do? Name it that. If the name has "and" in it, split the concept.

**Counter-example:**
```typescript
// ❌
const d = new Date();
const mgr = new UserMgr();
let flag = false;
function calc(x, y) {}

// ✅
const createdAt = new Date();
const userManager = new UserManager();
let isAuthenticated = false;
function calculateTax(income: number, rate: number): number {}
```

---

### missing-interface (TypeScript)

**Principle:** Dependency Inversion Principle
**Rule:** High-level modules should not depend on low-level modules. Both should depend on abstractions (interfaces).

**Book citations:**
- *OOP vs. Functional Programming* — "Program to an interface, not an implementation."
- *The Art of Clean Code*, Chapter 10 — "The DIP states that our classes should depend upon abstractions, not on concrete details."

**Why it matters:** Interfaces make code testable (inject a mock), swappable (replace the implementation), and legible (the interface documents the contract without implementation noise).

**Fix:** Extract an interface. Update all consumers to accept the interface, not the concrete class. Constructor injection becomes injectable.

**Counter-example:**
```typescript
// ❌ Tight coupling
class OrderService {
  constructor(private db: PostgresDatabase) {} // depends on concrete
}

// ✅ Depends on abstraction
interface IDatabase {
  query(sql: string): Promise<Row[]>;
  execute(sql: string): Promise<void>;
}
class OrderService {
  constructor(private db: IDatabase) {} // injectable, testable
}
```

---

### dry-violation / duplication

**Principle:** DRY — Don't Repeat Yourself
**Rule:** Every piece of knowledge must have a single, unambiguous, authoritative representation.

**Book citations:**
- *The Art of Clean Code*, Chapter 6 — "Duplication is the primary enemy of a well-designed system."
- *Code Complete 2nd Ed.*, Chapter 24 — "Anytime you see duplicated code, consider whether it can be combined."

**Why it matters:** When logic is duplicated, a bug fix in one place fails silently in another. Duplication is also a hidden cost — you maintain the same logic twice.

**Fix:** Extract the shared logic into a named function, class, or utility. If it's configuration, extract to a constant.

---

### comments-what-not-why

**Principle:** Self-Documenting Code
**Rule:** Code should explain what it does through naming. Comments explain why decisions were made.

**Book citations:**
- *The Art of Clean Code*, Chapter 4 — "The proper use of comments is to compensate for our failure to express ourselves in code."
- *Code Complete 2nd Ed.*, Chapter 32 — "Good code is its own best documentation."

**Why it matters:** "What" comments go stale as code evolves. The code is always right; the comment might not be. "Why" comments preserve decisions that aren't obvious from the code alone.

**Counter-example:**
```typescript
// ❌ What comment (redundant)
// Loop through users and check if active
for (const user of users) {
  if (user.isActive) { ... }
}

// ✅ Why comment (valuable)
// Must process in creation order — downstream audit log expects chronological entries
for (const user of sortedByCreatedAt(users)) { ... }
```

---

### human-readability

**Principle:** Optimize for the Reader
**Rule:** Code is read far more than it is written. Every decision should optimize for the next reader.

**Book citations:**
- *The Art of Clean Code*, Chapter 1 — "Clean code reads like well-written prose."
- *Code Complete 2nd Ed.*, Chapter 5 — "Write code to be read by humans, not just executed by machines."

**Checklist:**
- [ ] Can you describe what this file does in one sentence without "and"?
- [ ] Are all names clear to someone new to the codebase?
- [ ] Is the public API obvious from the file top?
- [ ] Are there no magic numbers or unexplained constants?
- [ ] Would a 5-minute read give a new contributor full understanding?

---

### reaching-through-objects

**Principle:** Law of Demeter ("Don't Reach Through Objects")
**Rule (plain):** A function should only talk to the things it holds directly. Don't dig through several objects to reach something deep inside.

**Book citations:**
- *The Art of Clean Code*, Chapter 4, Principle 13 — "A method of an object should only call methods of itself, its parameters, objects it creates, and its direct fields."

**Why it matters:** Every extra `.getSomething().getSomethingElse()` couples your code to a class you shouldn't even know about. When the middle class changes, your code breaks for no good reason. Short chains keep code loosely joined; long chains tangle everything together.

**Fix:** Add a small helper on the object you already hold that hides the digging. `order.getCustomer().getAddress().getZip()` becomes `order.getZip()`.

**Counter-example:**
```typescript
// ❌ Reaches through three objects
const zip = order.getCustomer().getAddress().getZip();

// ✅ Hides the digging behind one call
const zip = order.getZip();
```

---

### hidden-errors / no-input-check

**Principle:** Fail Fast (Defensive Programming)
**Rule (plain):** Public functions check their inputs at the top. Errors are shown, not hidden.

**Book citations:**
- *Code Complete 2nd Ed.*, Chapter 8 — "Protect your code from invalid inputs. Handle errors at the point of detection, not five layers away."

**Why it matters:** Silent failures are the most expensive bugs — they corrupt data, mislead users, and burn hours of debugging. An error that shows up immediately, close to its source, is cheap to fix. An error that gets swallowed and reappears three days later in a different part of the system can cost days.

**Fix:**
- Add guard clauses at the top of public functions (`if (!user) throw new Error(...)`).
- Replace empty `catch {}` or `except: pass` with real handling, logging, or rethrow.
- Use assertions for invariants that should always hold.

**Counter-example:**
```typescript
// ❌ Silent failure and missing input check
function charge(amount, card) {
  try {
    paymentAPI.charge(card, amount);
  } catch (e) {
    // nothing — the charge might have failed, we'll never know
  }
}

// ✅ Fail fast, handle explicitly
function charge(amount: number, card: ICard): ChargeResult {
  if (amount <= 0) throw new Error("amount must be positive");
  if (!card?.token) throw new Error("card token required");

  try {
    return paymentAPI.charge(card, amount);
  } catch (e) {
    logger.error("charge failed", { card: card.id, amount, error: e });
    throw new PaymentFailedError(e);
  }
}
```

---

### unused-code / boy-scout

**Principle:** YAGNI + Boy Scout Rule ("Only Build What You Need; Leave It Cleaner")
**Rule (plain):** Don't add code "just in case we need it later". When you touch a file for some other reason, tidy up the small things you notice.

**Book citations:**
- *The Art of Clean Code*, Principle 14 — "YAGNI: You Aren't Gonna Need It."
- *The Art of Clean Code*, Principle 17 — "Boy Scout Rule: Always leave the campground cleaner than you found it."

**Why it matters:** Speculative features are almost always wrong guesses — but they still cost bugs and complexity right now. Meanwhile, tiny as-you-go fixes keep a codebase healthy without ever needing a big cleanup sprint.

**Fix:**
- Delete unused exports, flags, and options with only one implementation.
- Remove commented-out code (version control remembers it).
- When editing a file, fix obvious small issues you spot — a bad name, a missing type, an unused import.

---

### messy-tests

**Principle:** Developer Testing — AAA (Arrange / Act / Assert)
**Rule (plain):** Each test has three short blocks: set it up, do the thing, check the result. One idea per test, no loops or `if`s inside a test body, named after the behavior it verifies.

**Book citations:**
- *Code Complete 2nd Ed.*, Chapter 22 — "Developer Testing: The first goal of tests is to prove the code works, but just as important is that tests document what the code is supposed to do."

**Why it matters:** Messy tests are worse than no tests. They pass for the wrong reasons, break for unrelated changes, and nobody knows what they were meant to prove. Clean tests double as documentation: a new reader learns what the code does by reading its tests.

**Fix:**
- Split tests that assert multiple unrelated things.
- Rename tests to describe behavior (`should_reject_negative_amount`, not `test1`).
- Move repeated setup into a helper or fixture (but don't share mutable state).
- Remove `if` / `for` / `while` from test bodies — if you need them, split the test.

**Counter-example:**
```typescript
// ❌ Named test1, multiple assertions, has a loop
it("test1", () => {
  const u = new User();
  for (const role of ["admin", "user", "guest"]) {
    u.setRole(role);
    expect(u.getRole()).toBe(role);
    expect(u.canLogin()).toBe(true);
  }
});

// ✅ One idea per test, AAA, descriptive names
it("admin_can_login", () => {
  // Arrange
  const user = new User();
  user.setRole("admin");
  // Act
  const canLogin = user.canLogin();
  // Assert
  expect(canLogin).toBe(true);
});

it("guest_can_login", () => { ... });
it("user_can_login",  () => { ... });
```

---

### folder-structure / module-cohesion *(dynamic rule)*

**Principle:** Clean Module & Folder Structure — Cohesion at Package Level
**Rule (plain):** The folder tree should read like a table of contents. A new contributor should be able to guess the project's domain from the top-level folders alone. But *how* to achieve that depends on the project — a 20-file CLI, a Rails app, a Go service, and a 5,000-file monorepo all have different "clean" shapes. This rule gives guidance, not a template.

**Book citations:**
- *Code Complete 2nd Ed.*, Chapter 5 — "Design in Construction" and Chapter 6 — "Working Classes" discuss packaging cohesion.
- *The Art of Clean Code*, Chapter 2 — "Focus" covers grouping by intent.

**Why it matters:** The folder tree is the first documentation a new person reads. `src/auth/`, `src/billing/`, `src/orders/` tells them the shape of the system before they open a file. A flat `src/` full of `utils.ts`, `helpers.py`, `common/` tells them nothing. But there's no universal best shape — ecosystem conventions (Rails, Next.js, Go packages, Java Maven layout) and project size change what "clean" looks like.

**Guiding principles (adapt to the project):**
- **Let the tree tell the story.** Top-level folder names should hint at the domain.
- **Group what changes together.** Files edited in the same PRs, by the same team, or for the same feature usually belong in the same folder.
- **Cohesion beats convention.** Layer folders (`controllers/`, `services/`, `models/`) are fine when the project is small and has only a few of each. They stop working when multiple unrelated domains pile up inside.
- **Be skeptical of catch-all folders** (`utils/`, `helpers/`, `common/`, `misc/`, `shared/`). A few genuine helpers are fine; a growing pile of unrelated files is a symptom of a missing domain folder.
- **Follow the language/framework grain.** Rails has `app/models`, Go prefers flat packages, Java/Maven wants parallel `src/main` and `src/test`, Next.js has `app/` routing. Honor the ecosystem before applying generic advice.
- **Size shapes structure.** Small projects want flat. Mid-size projects benefit from grouping. Large projects may need nested domains or workspace packages.
- **Test layout follows the language.** Colocated tests work in TS/JS/Python. Parallel trees are idiomatic in Java and Rust.

**How the plugin treats this rule:**
- Not a pass/fail check. The reviewer and `/cleancode:health` surface folder-structure observations as context-aware hints — never blocking, never auto-fixed.
- For small projects (< ~30 files), the plugin stays quiet. For larger projects, it starts suggesting groupings only when signals accumulate (e.g., oversized catch-all folder, many same-named files across folders, growing flat `src/`).
- No auto-fix: folder moves ripple through imports and the final call should be made by someone who knows the domain.

**Counter-example:**
```
# ❌ Technical-layer split in a medium project — domains are scattered
src/
  controllers/   (auth, billing, orders all mixed)
  services/     (auth, billing, orders all mixed)
  models/        (auth, billing, orders all mixed)
  utils/         (47 unrelated files)

# ✅ Domain-first — each folder tells part of the story
src/
  auth/          (types, service, controller, tests — colocated)
  billing/
  orders/
  shared/        (small, genuinely generic, not a dumping ground)
```
*But:* in a 20-file CLI, the first structure is perfectly fine — don't force domains that don't exist yet.
