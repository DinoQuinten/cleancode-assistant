# Coupling Detection Patterns

Reference for `/cleancode:untangle`. Covers chain detection, fan-out measurement, cycle detection, and fix templates.

---

## Method Chain Detection

### Regex (initial scan)

```
\b\w+\s*\([^)]*\)\s*\.\s*\w+\s*\([^)]*\)\s*\.\s*\w+\s*\(
```

This matches 3 or more chained method calls. For deeper chains, count consecutive `)\s*\.\s*\w+\s*\(` occurrences after the first call.

### Counting chain depth

Split the expression on `.` while tracking parenthesis depth. A chain of depth N has N function-call nodes after the initial owner.

- `a.b()` → depth 1 (ok)
- `a.b().c()` → depth 2 (borderline, flag as Style if warranted)
- `a.b().c().d()` → depth 3 (Warning)
- `a.b().c().d().e()` → depth 4 (Critical)

### Exceptions — don't flag

**Fluent builder pattern:** every call returns the same type.

```typescript
const q = new QueryBuilder()
  .where("id", 1)     // returns QueryBuilder
  .orderBy("name")    // returns QueryBuilder
  .limit(10)          // returns QueryBuilder
  .build();           // returns Query
```

Detect: if every intermediate call returns `this` (check function body for `return this`), treat as builder.

**Array / iterator chains:**

```typescript
users.filter(u => u.active).map(u => u.name).join(", ")
```

These are idiomatic transformations on a collection, not reaching through objects. Flag only if the collection itself came from a chain.

**Optional chaining on data:**

```typescript
const city = user?.address?.city;
```

Property chains (no function calls) on plain-data objects are fine.

---

## High Fan-Out Detection

### Count imports

**TypeScript / JavaScript:**
```
^\s*import\s+.+\s+from\s+['"].+['"]
^\s*const\s+\w+\s*=\s*require\(
```

**Python:**
```
^\s*import\s+
^\s*from\s+\w+\s+import\s+
```

**Java / C#:**
```
^\s*import\s+
^\s*using\s+
```

### Thresholds

| Imports from N other modules | Severity |
|---|---|
| ≤ 10 | ✓ |
| 11 – 15 | Warning |
| > 15 | Critical |

Exclude:
- Standard library imports (`node:`, `std::`, `java.lang.`, built-in Python modules)
- Type-only imports (`import type ...`)

---

## Circular Import Detection

Build a directed graph: node = file, edge = `A imports B`.

Run a depth-first search from each file; flag any back edge as a cycle.

For a small project (<200 files) it's fast enough to:

1. Glob all source files
2. Grep imports from each
3. Build an in-memory adjacency list
4. DFS + cycle check

For large projects, limit the scan to the file being analyzed and its transitive imports (depth 3).

---

## Fix Templates

### Template 1: Replace chain with helper method

**Before:**
```typescript
// call site
const zip = order.getCustomer().getAddress().getZip();
```

**Transformation:**
1. Locate class `Order` — e.g., `src/models/Order.ts`.
2. Add method:
   ```typescript
   getZip(): string {
     return this.getCustomer().getAddress().getZip();
   }
   ```
3. Replace call site:
   ```typescript
   const zip = order.getZip();
   ```

**Across multiple call sites:** grep for the exact chain, replace all.

### Template 2: Break circular import

**Before:**
```
// a.ts
import { B } from "./b";
export class A { b: B; }

// b.ts
import { A } from "./a";
export class B { a: A; }
```

**Transformation:**
1. Extract shared interfaces to `types.ts`:
   ```typescript
   // types.ts
   export interface IA { /* ... */ }
   export interface IB { /* ... */ }
   ```
2. Rewrite `a.ts` and `b.ts` to import from `types.ts`:
   ```typescript
   // a.ts
   import { IB } from "./types";
   export class A implements IA { b: IB; }
   ```

### Template 3: Split a god class

When a class has > 10 public methods AND high fan-out, propose a split:

1. Group methods by domain noun they use most.
2. Each group becomes a new class/file.
3. The original class either delegates or is deleted.

Do not auto-apply — show the plan and ask the user to confirm each extraction.

---

## Language-Specific Notes

### Python

- `self.a.b.c` property access is not a chain (Python doesn't distinguish method from property syntax — check for `()`).
- Django ORM: `Model.objects.filter().order_by().first()` is a fluent chain — downgrade to Style.

### Go

- Method chains on embedded types are fine (Go composition).
- Interface assertions (`x.(*T).Method()`) aren't chains.

### TypeScript / JavaScript

- Promise chains (`.then().catch()`) are idiomatic — ignore.
- RxJS pipelines — ignore (they're the whole point of the library).

### Java / C#

- Stream / LINQ chains are idiomatic.
- Builder pattern is common — detect via return type identity.
