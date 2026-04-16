# Refactoring Catalog

Reference for `/cleancode:refactor`. Each entry has the plain-language name, the textbook name, a when-to-apply note, and the transformation template.

---

## extract-function (Extract Method)

**Plain:** Pull a block of code out into its own named function.
**Textbook:** Fowler's *Refactoring*, "Extract Method"; Code Complete 2nd Ed., Ch. 24.

### When to apply

- A function is > 40 lines (Rule 2 violation)
- A block inside a function has a clear name ("validate order", "calculate tax") — extract it
- A block is used more than once — extract and share

### Transformation

1. Identify the block (contiguous lines inside a function).
2. Identify **reads** (become params) and **writes used afterward** (become return value).
3. Pick a name that describes WHAT the block does (verb + noun).
4. Create the new function.
5. Replace the block with a call.

Example:

```typescript
// Before
function processOrder(order: IOrder) {
  // ... 40 lines ...
  let tax = 0;                              // ← these 10 lines
  for (const item of order.items) {         //   are extract target
    if (item.taxable) {
      tax += item.price * 0.08;
    }
  }                                         //
  // ... more lines using `tax` ...
}

// After
function processOrder(order: IOrder) {
  // ... 40 lines ...
  const tax = calculateTax(order);
  // ... more lines using `tax` ...
}

function calculateTax(order: IOrder): number {
  let tax = 0;
  for (const item of order.items) {
    if (item.taxable) {
      tax += item.price * 0.08;
    }
  }
  return tax;
}
```

---

## extract-class (Extract Class)

**Plain:** Pull a group of fields and the methods that use them into a new class.
**Textbook:** Fowler's *Refactoring*, "Extract Class".

### When to apply

- A class has > 10 methods or > 15 fields (Rule 6 violation)
- A subset of fields is used together by a subset of methods — they form a mini-class inside

### Transformation

1. Identify the cohesive subset (methods + fields).
2. Create a new class with those fields.
3. Move the methods.
4. In the original class, add a field holding an instance of the new class.
5. Delegate the old method calls to the new class.

---

## inline (Inline Method)

**Plain:** Inline a function whose body says more than its name.
**Textbook:** Fowler's *Refactoring*, "Inline Method".

### When to apply

- A function is trivial (`getAge() { return this.age; }` called only once)
- A function's name is vague and the body is clearer than the name

### Transformation

1. Verify the function has no other callers.
2. Copy the body to the call site.
3. Delete the function.

---

## named-constant (Replace Magic Number with Named Constant)

**Plain:** Replace a bare number with a named constant that explains what it means.
**Textbook:** Code Complete 2nd Ed., Ch. 12.

### When to apply

- A literal number appears in code without explanation
- The same number appears in multiple places

### Transformation

1. Pick a name that captures the meaning (`TAX_RATE`, `MAX_RETRIES`, `DEFAULT_PAGE_SIZE`).
2. Define as a `const` at the top of the file (or in a constants file).
3. Replace every occurrence.

Example:

```typescript
// Before
if (retries > 3) throw new Error("too many retries");
for (let i = 0; i < 3; i++) { ... }

// After
const MAX_RETRIES = 3;

if (retries > MAX_RETRIES) throw new Error("too many retries");
for (let i = 0; i < MAX_RETRIES; i++) { ... }
```

---

## polymorphism (Replace Conditional with Polymorphism)

**Plain:** Replace a big if-chain or switch with subclasses that each implement the behavior.
**Textbook:** Fowler's *Refactoring*, "Replace Conditional with Polymorphism".

### When to apply

- A switch with 4+ cases, each doing non-trivial work
- The same switch appears in multiple methods (all branching on the same field)

### Transformation

Delegate to `/cleancode:structure` with Strategy pattern. See `skills/structure/references/pattern-catalog.md`.

---

## guard-clauses (Replace Nested Conditional with Guard Clauses)

**Plain:** Flatten nested ifs by returning early for invalid conditions.
**Textbook:** Code Complete 2nd Ed., Ch. 19.

### When to apply

- Nesting depth > 4 (Rule 4 violation)
- The happy path is wrapped in layers of `if`s

### Transformation

```typescript
// Before
function process(user) {
  if (user) {
    if (user.isActive) {
      if (user.hasPermission) {
        // actual work
      }
    }
  }
}

// After
function process(user: IUser): void {
  if (!user) return;
  if (!user.isActive) return;
  if (!user.hasPermission) throw new PermissionError();

  // actual work
}
```

---

## parameter-object (Introduce Parameter Object)

**Plain:** Group related parameters into a single object.
**Textbook:** Fowler's *Refactoring*, "Introduce Parameter Object".

### When to apply

- A function has > 4 parameters (Rule 3 violation)
- Several params always pass together (e.g., `startDate` + `endDate` → `DateRange`)

### Transformation

1. Create an interface or type for the grouped params.
2. Update the function signature.
3. Update every call site.

```typescript
// Before
function createUser(name, email, role, dept, managerId, startDate, isRemote) {}

// After
interface ICreateUserParams {
  name: string;
  email: string;
  role: UserRole;
  dept: string;
  managerId: string;
  startDate: Date;
  isRemote: boolean;
}
function createUser(params: ICreateUserParams): User {}
```

---

## table-driven (Table-Driven Method)

**Plain:** Replace a switch or long if-chain with a lookup table.
**Textbook:** Code Complete 2nd Ed., Ch. 18.

### When to apply

- Switch / if-chain where every case returns a value (or calls a simple handler)
- The mapping is stable (not expected to add cases at runtime)

### Transformation

```typescript
// Before
function getTaxRate(category: string): number {
  switch (category) {
    case "food":      return 0.00;
    case "clothing":  return 0.05;
    case "electronics": return 0.08;
    case "luxury":    return 0.15;
    default:          throw new Error(`Unknown: ${category}`);
  }
}

// After
const TAX_RATES: Record<string, number> = {
  food: 0.00,
  clothing: 0.05,
  electronics: 0.08,
  luxury: 0.15,
};

function getTaxRate(category: string): number {
  const rate = TAX_RATES[category];
  if (rate === undefined) throw new Error(`Unknown category: ${category}`);
  return rate;
}
```

For cases that execute logic (not return constants), use a map of handler functions:

```typescript
const HANDLERS: Record<string, (order: IOrder) => number> = {
  food: (o) => o.subtotal * 0.00,
  clothing: (o) => o.subtotal * 0.05,
  // ...
};
```

---

## split-variable (Split Temporary Variable)

**Plain:** If a variable gets assigned twice for two different purposes, give each purpose its own variable.
**Textbook:** Fowler's *Refactoring*, "Split Temporary Variable".

### When to apply

- A variable holds one thing early, then gets reassigned to hold something else
- The same name is used for both meanings

### Transformation

```typescript
// Before
let temp = 2 * (height + width);
console.log(temp);                 // perimeter
temp = height * width;
console.log(temp);                 // area

// After
const perimeter = 2 * (height + width);
console.log(perimeter);
const area = height * width;
console.log(area);
```

---

## When NOT to Refactor

- The code is already clear and short.
- The refactoring would spread the change across > 5 files without a clear gain.
- The user didn't ask for it. This skill only runs on explicit invocation.
