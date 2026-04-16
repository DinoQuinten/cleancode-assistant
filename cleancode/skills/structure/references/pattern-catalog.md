# Pattern Catalog

Reference for `/cleancode:structure`. Four patterns the skill can detect and apply, with plain-language explanations, detection heuristics, rewrite templates, and guidance on when NOT to apply.

---

## 1. Strategy — "one class per behavior, picked at runtime"

### When it fits

- Big `switch` or `if/else` chain (> 4 cases) where each branch does different non-trivial work
- Adding a new case means editing the switch + several related spots
- Each case's logic is > 5 lines

### When it does NOT fit

- All cases just return a constant — use a lookup map, not Strategy
- Only 2-3 cases — an if/else is fine, extra classes add noise
- Cases share > 70% of their code — extract a helper function instead

### Detection

- Regex: `switch\s*\(` followed by 5+ `case` labels with non-return bodies
- If/else chain: 3+ consecutive `} else if (` with different condition predicates

### Rewrite template

See `SKILL.md` for the full TypeScript example. Summary:

1. Interface file — one method, the common behavior.
2. N strategy files — one per case.
3. Registry file — map from key to strategy instance.
4. Caller becomes: `registry[key].doIt(args)`.

---

## 2. Command — "wrap an operation so you can queue, log, or undo it"

### When it fits

- Methods that perform an action AND store it for later (undo stack, audit log, retry queue)
- Multiple actions that should be interchangeable (e.g., button handlers in a UI)

### When it does NOT fit

- A single action with no need for history, queuing, or undo — just call it
- Actions too different to share an interface

### Detection

- Look for: an array/list named `history`, `queue`, `log`, `actions`, `undoStack` that receives `push`/`append` calls from multiple methods
- Or: several methods ending with `this.log.push({...})`

### Rewrite template

```typescript
// Before
class Editor {
  text = "";
  history: string[] = [];

  addText(s: string) {
    this.text += s;
    this.history.push(`add:${s}`);
  }
  removeText(n: number) {
    this.text = this.text.slice(0, -n);
    this.history.push(`remove:${n}`);
  }
}

// After
interface ICommand {
  execute(editor: Editor): void;
  undo(editor: Editor): void;
}

class AddTextCommand implements ICommand {
  constructor(private readonly s: string) {}
  execute(e: Editor) { e.text += this.s; }
  undo(e: Editor)    { e.text = e.text.slice(0, -this.s.length); }
}

class RemoveTextCommand implements ICommand {
  constructor(private readonly n: number, private removed = "") {}
  execute(e: Editor) {
    this.removed = e.text.slice(-this.n);
    e.text = e.text.slice(0, -this.n);
  }
  undo(e: Editor) { e.text += this.removed; }
}

class Editor {
  text = "";
  private history: ICommand[] = [];

  run(cmd: ICommand) {
    cmd.execute(this);
    this.history.push(cmd);
  }
  undo() {
    const cmd = this.history.pop();
    cmd?.undo(this);
  }
}
```

---

## 3. Factory — "one place that knows how to build a thing"

### When it fits

- Multiple call sites construct an object with similar-but-different setup
- Deciding which subclass to instantiate based on a runtime value
- Construction requires multiple steps (allocate, configure, wire dependencies)

### When it does NOT fit

- Only one call site — `new X()` directly is fine
- Construction is trivial (no setup) — no factory needed

### Detection

- Grep for `new ClassName(` across the codebase; if 3+ call sites do different setup after construction, propose factory
- A switch that returns `new ChildA()` / `new ChildB()` etc.

### Rewrite template

```typescript
// Before — scattered
const admin = new User();
admin.role = "admin";
admin.permissions = ["read", "write", "delete"];

const guest = new User();
guest.role = "guest";
guest.permissions = ["read"];

// After — factory
class UserFactory {
  static create(role: "admin" | "user" | "guest"): User {
    const user = new User();
    user.role = role;
    user.permissions = UserFactory.permissionsFor(role);
    return user;
  }

  private static permissionsFor(role: string): string[] {
    switch (role) {
      case "admin": return ["read", "write", "delete"];
      case "user":  return ["read", "write"];
      case "guest": return ["read"];
      default: throw new Error(`Unknown role: ${role}`);
    }
  }
}

// Call sites
const admin = UserFactory.create("admin");
const guest = UserFactory.create("guest");
```

---

## 4. State — "each state knows its own legal transitions"

### When it fits

- A class has a field (`status`, `state`, `mode`) that's used as a branching flag in many methods
- The allowed transitions form a state machine (e.g., draft → submitted → approved → published)
- Methods frequently check the current state before doing work

### When it does NOT fit

- Only 2 states (boolean `isActive`) — a flag is fine
- State is pure data (user role) not a machine

### Detection

- A field whose value is compared in 4+ places inside the same class
- Multiple methods start with `if (this.status === "...")` branching

### Rewrite template

```typescript
// Before — branches everywhere
class Document {
  status: "draft" | "submitted" | "approved" | "published" = "draft";

  submit() {
    if (this.status !== "draft") throw new Error("invalid state");
    this.status = "submitted";
  }
  approve() {
    if (this.status !== "submitted") throw new Error("invalid state");
    this.status = "approved";
  }
  publish() {
    if (this.status !== "approved") throw new Error("invalid state");
    this.status = "published";
  }
}

// After — each state is a class
interface IDocumentState {
  submit(doc: Document): void;
  approve(doc: Document): void;
  publish(doc: Document): void;
}

class DraftState implements IDocumentState {
  submit(doc: Document) { doc.setState(new SubmittedState()); }
  approve(_: Document) { throw new Error("cannot approve a draft"); }
  publish(_: Document) { throw new Error("cannot publish a draft"); }
}

class SubmittedState implements IDocumentState {
  submit(_: Document) { throw new Error("already submitted"); }
  approve(doc: Document) { doc.setState(new ApprovedState()); }
  publish(_: Document) { throw new Error("must be approved first"); }
}

// ... ApprovedState, PublishedState similar

class Document {
  private state: IDocumentState = new DraftState();
  setState(s: IDocumentState) { this.state = s; }

  submit()  { this.state.submit(this); }
  approve() { this.state.approve(this); }
  publish() { this.state.publish(this); }
}
```

---

## When NOT to Apply Any Pattern

Over-engineering is itself a clean code violation (Rule 13 — YAGNI).

Don't apply a pattern when:

- **The current code is already clear.** A short switch of clear cases is fine.
- **The project has only one implementation** and won't grow — an interface with one impl is noise.
- **The user didn't ask for it.** This skill only runs on explicit `/cleancode:structure` invocation.

When in doubt, report the pattern as a suggestion in report mode and let the user decide.
