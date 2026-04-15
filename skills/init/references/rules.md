# Clean Code Rules — Canonical Ruleset

Source: Code Complete 2nd Ed. (McConnell), The Art of Clean Code (Mayer), Object-Oriented vs. Functional Programming

These rules apply to ALL programming languages. TypeScript/JavaScript projects have additional interface requirements marked [TS].

---

## 1. File Size

**Rule:** No file exceeds 300 lines of code (excluding blank lines and comments).
**Why:** A file that can't be read in one sitting is a file that violates single responsibility. If you need to scroll to understand it, it's too big.
**Book:** Code Complete 2nd Ed., Chapter 5 — "Design in Construction"
**Action when violated:** Split into smaller classes/modules. Each file should represent one concept.

---

## 2. Function / Method Size

**Rule:** No function or method exceeds 40 lines. The ideal is under 20.
**Why:** A function that does one thing fits on one screen. When it doesn't, it's doing more than one thing.
**Book:** The Art of Clean Code, Chapter 3 — "Functions"; Code Complete 2nd Ed., Chapter 7 — "High-Quality Routines"
**Action when violated:** Extract sub-functions. Name them by what they do, not how they do it.

---

## 3. Parameter Count

**Rule:** No function takes more than 4 parameters.
**Why:** Long parameter lists signal that a function is doing too much or that related data should be grouped into an object/interface.
**Book:** The Art of Clean Code, Chapter 3; Code Complete 2nd Ed., Chapter 7
**Action when violated:** Group related parameters into a typed object or interface. [TS] Create a named interface for the parameter object.

---

## 4. Nesting Depth

**Rule:** No code block nests deeper than 4 levels.
**Why:** Deep nesting is a cognitive tax on every reader. It usually means complex conditionals that can be simplified.
**Book:** Code Complete 2nd Ed., Chapter 19 — "General Control Issues"
**Action when violated:** Extract nested logic into named functions. Use early returns / guard clauses. Invert conditionals.

---

## 5. Meaningful Naming

**Rule:** Every name (variable, function, class, file) must reveal its intent without needing a comment to explain it.
**Standards:**
- Variables: noun or noun phrase describing what it holds (`userAccount`, not `obj` or `x`)
- Functions: verb + noun describing what it does (`calculateTax`, not `calc`)
- Classes: noun describing the concept it represents (`OrderProcessor`, not `Manager`)
- Files: match the primary class/module they contain
- No single-letter names except loop counters (i, j, k)
- No abbreviations that aren't universally known (`btn` is ok; `usrAcctMgr` is not)
**Book:** Code Complete 2nd Ed., Chapter 11 — "The Power of Variable Names"; The Art of Clean Code, Chapter 2
**Action when violated:** Rename immediately. Good names are the cheapest form of documentation.

---

## 6. Object-Oriented Principles (OOP)

**Rule:** Apply SOLID principles. Default to OOP unless the language or context makes functional a better fit.

- **S — Single Responsibility**: Each class does one thing. If you need "and" to describe it, split it.
- **O — Open/Closed**: Classes open for extension, closed for modification. Use inheritance/composition.
- **L — Liskov Substitution**: Subtypes must be substitutable for their base types.
- **I — Interface Segregation**: Don't force clients to depend on interfaces they don't use. Keep interfaces small.
- **D — Dependency Inversion**: Depend on abstractions, not concretions. [TS] Depend on interfaces, not classes.

**Book:** Object-Oriented vs. Functional Programming (included PDF)
**Action when violated:** Refactor toward the violated principle. Document the reason if deviation is intentional.

---

## 7. Interfaces (TypeScript — First-Class Rule)

**Rule [TS]:** Every public-facing API, service, repository, or class must define an explicit TypeScript interface.
**Why:** Interfaces separate contract from implementation. They enable testing with mocks, enable multiple implementations, and make the codebase's shape legible at a glance.
**Standards:**
- Interface names: prefix with `I` or use descriptive noun (`UserRepository`, `IUserRepository`)
- One interface per file, or group related interfaces in a `types.ts` / `interfaces.ts`
- Constructor parameters for services: inject via interface, not concrete class
- Avoid `any` — use proper interface types
**Action when violated:** Extract the interface. Update consumers to depend on the interface.

---

## 8. DRY — Don't Repeat Yourself

**Rule:** No logic is duplicated more than once. If you copy-paste more than 3 lines, extract a function.
**Why:** Duplication is the root cause of most bugs — fix one instance, forget the others.
**Book:** The Art of Clean Code, Chapter 6 — "Code Duplication"
**Action when violated:** Extract to a shared utility, base class, or helper. Name it clearly.

---

## 9. Comments

**Rule:** Comments explain *why*, never *what*. Code explains what it does. Comments explain why it does it.
**Standards:**
- Good: `// Must run before DB migration — legacy schema requires this order`
- Bad: `// Loop through users` (the code already says that)
- No commented-out code. Use version control for history.
- No TODO comments in committed code. Open a ticket instead.
**Book:** The Art of Clean Code, Chapter 4 — "Comments"; Code Complete 2nd Ed., Chapter 32
**Action when violated:** Remove or rewrite. If the code needs a "what" comment, rename things until it doesn't.

---

## 10. Human Readability Test (Principle of Least Surprise)

**Rule:** Any new contributor with basic language knowledge must understand what a file does within 5 minutes without asking. Code should behave the way the name suggests — no hidden side effects, no "gotcha" logic.
**Why:** Code is read far more than it is written. Optimize for the reader. Surprises in code become bugs in production.
**Checklist:**
- [ ] File has a clear, single purpose
- [ ] Public API is obvious from names alone
- [ ] No magic numbers — use named constants
- [ ] No clever one-liners that sacrifice clarity for brevity
- [ ] Consistent formatting and style throughout
- [ ] Functions do exactly what their name says — no extra hidden work
**Book:** The Art of Clean Code, Chapter 1 — "Clean Code"; Principle 8 — "Principle of Least Surprise"

---

## 11. Don't Reach Through Objects (Law of Demeter)

**Rule (plain):** A function should only talk to things it owns directly. Don't go digging through several objects to reach something you want. For example, `order.getCustomer().getAddress().getZip()` reaches too far.
**Why:** When you chain calls like that, your code gets tangled up with classes it shouldn't even know about. If someone changes one of those middle classes, your code breaks too — even though it had no reason to.
**Book:** The Art of Clean Code, Chapter 4, Principle 13 — "Law of Demeter"
**Action when violated:** Add a small helper on the object you already have (`order.getZip()`) that hides the digging behind one call.
**Severity:** Warning.

---

## 12. Check Inputs Early, Never Hide Errors (Fail Fast / Defensive Programming)

**Rule (plain):** At the top of any function that takes outside input, check the values make sense before using them. If something goes wrong, let it show — don't wrap a `try/catch` around it and pretend everything is fine.
**Why:** Silent failures are the hardest bugs to find. They corrupt data, confuse users, and waste debugging time. Visible, early errors are easier to fix than buried ones.
**Book:** Code Complete 2nd Ed., Chapter 8 — "Defensive Programming"
**Action when violated:** Add guard clauses at the top of the function. Replace empty `catch {}` or `except: pass` with real error handling or let the error bubble up. Use assertions for things that should always be true.
**Severity:** **Critical** when a function silently swallows errors or skips input checks at a public boundary. Warning for internal helper functions.

---

## 13. Only Build What You Need; Leave Code Cleaner Than You Found It (YAGNI + Boy Scout Rule)

**Rule (plain):** Don't add code "just in case we need it later" — most of the time, you never do. And when you're already editing a file for some other reason, tidy up small things you notice (a bad name, a missing comment, an unused import).
**Why:** Features you add "for the future" are almost always wrong guesses — but they still cost you bugs and complexity right now. Meanwhile, tiny improvements as you go keep a codebase healthy without ever needing a big cleanup project.
**Book:** The Art of Clean Code, Principle 14 — "YAGNI" and Principle 17 — "Boy Scout Rule"
**Action when violated:** Delete unused options, flags, and abstractions with only one implementation. When you touch a file, fix the small issues you notice.
**Severity:** Style (informational — surfaced by review, never blocking).

---

## 14. Tests Should Be As Clean As The Code They Test (Developer Testing — AAA)

**Rule (plain):** Every test should follow three short blocks: **set it up**, **do the thing**, **check the result** (often called Arrange / Act / Assert). Name the test after what it checks (`should_show_error_when_password_is_blank`). Keep one idea per test — no loops or `if` statements inside a test. Don't share mutable data between tests.
**Why:** Tests are code too, and messy tests are worse than no tests — they pass when they shouldn't, break for the wrong reasons, and nobody understands what they were trying to prove.
**Book:** Code Complete 2nd Ed., Chapter 22 — "Developer Testing"
**Action when violated:** Split tests that check multiple things. Rename tests to describe behavior. Move repeated setup into a helper. Remove control flow from test bodies.
**Severity:** Warning.

---

## 15. Clean Module & Folder Structure (Cohesion at Package Level) — *Dynamic Rule*

**Rule (plain):** The folder tree should read like a table of contents — someone new should be able to guess what the project does and roughly where to find things by looking at the top-level directories. Files that change together live together. How to achieve that depends on the project: a small library, a microservice, and a large application all have different "clean" structures. This rule gives guidance, not a template.
**Why:** The folder tree is the first piece of documentation a new contributor reads. A tree that tells the story of the system saves hours of exploration. But every project is different — what works for a 50-file CLI tool doesn't work for a 5,000-file monorepo, and what the language community expects (Go's flat packages, Java's parallel test tree, Rust's `mod.rs`) overrides any universal preference. There is no one right shape.

**Book:** Code Complete 2nd Ed., Chapter 5 — "Design in Construction"; Chapter 6 — "Working Classes"; The Art of Clean Code, Chapter 2 — "Focus".

**Guiding principles (adapt to your project):**
- **Let the folder tree tell a story.** A first-time reader should be able to guess the domain from top-level folder names alone. If the top level is `src/`, `lib/`, `utils/`, they learn nothing. If it's `auth/`, `billing/`, `orders/`, they already understand the system.
- **Group by what changes together.** Files that are edited in the same PRs, touched by the same team, or belong to the same feature usually want to sit in the same folder — regardless of whether they're "types", "services", or "components" underneath.
- **Cohesion beats convention.** Technical-layer folders (`controllers/`, `services/`, `models/`) are fine for small projects where the domain is obvious and there are only a few of each. They become painful as the project grows and unrelated domains pile up in the same folder. When that happens, switch to domain-first.
- **Be skeptical of catch-all folders** (`utils/`, `helpers/`, `common/`, `misc/`, `shared/`). They're often a symptom — code landed there because no one knew where else to put it. A small amount is normal; a growing pile means a missing domain folder. But sometimes a `utils/` with 3 genuinely generic files really is fine. Use judgment.
- **Follow the language/framework grain.** Rails has `app/models`, `app/controllers` — don't fight it. Go prefers flat packages with descriptive names. Java/Maven want `src/main/java/com/example/...` with a parallel `src/test`. Next.js has `app/` routing. Honor the conventions of your ecosystem before applying generic advice.
- **Size shapes structure.** A 20-file script doesn't need domain folders at all — flat is clearer. A 500-file app usually benefits from grouping. A 5,000-file monorepo may need nested domains, bounded contexts, or workspace packages. The right structure scales with the codebase.
- **Test layout follows the language.** Colocated tests (`foo.ts` + `foo.test.ts`) work well in TS/JS/Python. Parallel test trees are the norm in Java and idiomatic in Rust (`tests/` directory). Match the ecosystem — don't force one pattern.

**How the plugin treats this rule:**
- This is **not** a pass/fail check. The reviewer and `/cleancode:health` surface folder-structure observations as *style hints* — "you have a top-level `utils/` with 47 files; consider whether these belong to specific domains" — rather than as violations.
- No auto-fix. Folder moves touch imports across the whole codebase and are almost always better done by a human who understands the domain.
- Context-aware: for small projects (< ~30 files) the plugin stays quiet. For larger projects it starts suggesting groupings when signs of a problem appear (oversized catch-all folders, many same-named files across folders, etc.).

**Severity:** Style — always surfaced as a suggestion, never blocking, always with "if this fits your project" framing.

---

## Thresholds Summary

| Metric | Threshold | Severity |
|---|---|---|
| File length | > 300 lines | Critical |
| Function length | > 40 lines | Critical |
| Function length | > 20 lines | Warning |
| Parameter count | > 4 | Critical |
| Parameter count | = 4 | Warning |
| Nesting depth | > 4 | Critical |
| Nesting depth | = 4 | Warning |
| Duplicated logic | > 3 lines copied | Warning |
| Missing interface [TS] | Public class/service with no interface | Warning |
| Magic number | Unexplained numeric literal | Style |
| Single-letter variable (non-loop) | — | Style |
| TODO in committed code | — | Style |
| Reaching through objects (`a.b().c().d()`) | chain depth > 2 | Warning |
| Hidden errors (`catch {}`, `except: pass`, empty `catch (e)`) | any occurrence | Critical |
| Missing input check on public function | first line isn't a guard | Warning |
| `if` / `for` / `while` inside test body | any occurrence | Warning |
| Test name doesn't describe behavior (no verb) | — | Style |
| Folder structure (domain vs. layer, catch-all folders, size-appropriate grouping) | context-dependent — only flagged when signals accumulate | Style (hint, never auto-fixed) |
| Unused export / single-implementation interface | — | Style |
