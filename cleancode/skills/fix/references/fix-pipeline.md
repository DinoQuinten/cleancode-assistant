# Fix Pipeline Contract

Reference for `/cleancode:fix`. Defines the stage-by-stage contract: what each fixer expects as input, what it guarantees as output, and how failures propagate.

---

## Pipeline Order (Why This Order)

1. **safety** — run first, because fixing hidden errors doesn't depend on anything else
2. **untangle** — run after safety so guard clauses are in place; replacing chains may reveal places that need guards
3. **test** — only if target is a test file; run after source fixes in case the source changes affect test behavior
4. **refactor** — run last because extract-function and guard-clauses rewrites should happen on already-cleaned code (avoids extracting a block that still has a silent catch)
5. **structure** — reported only, not applied (big restructurings require explicit invocation)
6. **re-analyze** — confirm the fixes landed

---

## Stage Contract

Each stage receives:

```
{
  target: "<file path or .>"
  violations: [
    { file, line, rule, severity, description }
  ]
  mode: "critical-only" | "all"
}
```

Each stage returns:

```
{
  applied: [ { file, line, rule, before, after } ]
  skipped: [ { file, line, rule, reason } ]
  error?: { stage, message }
}
```

---

## Stage 1 — safety fix

**Input:** violations with rule `hidden-errors` or `missing-input-check`.

**Applied:**
- Empty catches replaced with log + rethrow.
- Guard clauses inserted at public function tops.

**Skipped:**
- Intentional-looking catches (retry loops, NotFound handlers).
- Private helper functions without guards (warning-only, auto-skipped in critical-only mode).

**Guarantees:**
- Adds no new side effects.
- Never deletes a catch — only replaces its body.
- If a logger import is added, it matches the project's existing logger if one is detected.

---

## Stage 2 — untangle fix

**Input:** violations with rule `reaching-through-objects`.

**Applied:**
- Method chains > 2 replaced with helper methods on the owning class.
- Helper methods added to the class definition.

**Skipped:**
- Fluent builders (downgraded to Style).
- Array / iterator chains.
- Chains in files the fixer can't locate the owning class for (external library).

**Guarantees:**
- New helper methods have a single line body that preserves the original chain.
- All call sites of the original chain are replaced.
- No new imports added unless required for the helper's return type.

---

## Stage 3 — test fix

**Input:** violations with rule `messy-tests`. Only runs if target file matches test patterns.

**Applied:**
- Multi-assertion tests split into separate tests.
- Loops inside tests converted to parameterized tests (`it.each`, `@pytest.parametrize`).
- Bad test names replaced with descriptive names derived from assertions.
- AAA structure inserted (blank-line separation).

**Skipped:**
- Tests whose intent is unclear from the assertions.
- Shared-state tests (warning, manual review).

**Guarantees:**
- The same assertions are made before and after (total assertion count preserved).
- No assertion is deleted.

---

## Stage 4 — refactor

**Input:** violations with rules `function-too-long`, `deep-nesting`, `too-many-parameters`.

**Applied:**
- `function-too-long` → `extract-function` on the largest internal block.
- `deep-nesting` → `guard-clauses` at the top of the function.
- `too-many-parameters` → `parameter-object` grouping the params.

**Skipped:**
- Functions whose only internal block is already atomic (one clear operation, already short).
- Parameter lists where grouping doesn't make semantic sense.

**Guarantees:**
- Function signatures only change for `parameter-object`; call sites are updated.
- Extract-function doesn't rename the host function.
- No behavior change.

---

## Failure Propagation

If a stage fails:

1. Stop the pipeline.
2. Keep all edits from previous stages (don't roll back).
3. Report the failure:

```
cleancode fix — stopped at stage 2 (untangle)

Completed:
  ✓ safety fix — 4 edits applied

Failed:
  ✗ untangle fix — could not locate class `Order` (imported from external module)

Partial result: 4 fixes applied from stage 1.
Re-run /cleancode:fix to continue from where it stopped.
```

---

## Idempotence

Running `/cleancode:fix <file>` twice on the same file should be safe:

- The second run re-analyzes the now-cleaner file.
- Violations already fixed are no longer detected.
- Only new violations (if any) are addressed.

This means a partial failure can be retried simply by re-running.

---

## Mode Differences

### critical-only (default)

Stage filter: only violations with severity == Critical.

Typical edits:
- Empty catches
- Missing input checks on public APIs (downgraded critical variant)
- Functions > 40 lines
- Method chains > 3

### all

Stage filter: Critical + Warning.

Additional edits:
- Functions 20-40 lines (extract if natural boundary found; skip otherwise)
- Method chains of exactly 2 (downgraded to Style)
- Division guards
- I/O error wrappers

Style violations (Rule 13 dead code, naming) are never auto-fixed in any mode — they need human judgment.
