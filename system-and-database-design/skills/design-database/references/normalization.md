# Normalization (and When to Denormalize)

Authoritative sources: Codd's original papers, Date's "Introduction to Database Systems", DDIA ch. 2.

## The normal forms

Progressive constraints on schema to eliminate data anomalies.

### 1NF (First Normal Form)

- Each cell holds a single atomic value (no lists, no nested structs in relational DBs)
- Each row is uniquely identifiable (primary key)

**Violation**: `phone_numbers: "555-1234, 555-5678"` in one column.

### 2NF

- Satisfies 1NF AND
- No non-key column depends on PART of a composite key

**Violation**: `order_items(order_id, product_id, product_name, quantity)` where `product_name` depends only on `product_id`, not on `(order_id, product_id)`.

### 3NF

- Satisfies 2NF AND
- No non-key column depends on another non-key column (no transitive dependencies)

**Violation**: `employees(emp_id, dept_id, dept_name)` where `dept_name` depends on `dept_id`, which is non-key.

### BCNF (Boyce-Codd)

- Every determinant is a candidate key
- Rare cases 3NF-compliant schemas still have anomalies; BCNF fixes them

### Beyond BCNF

4NF (multi-valued dependencies), 5NF (join dependencies), 6NF (temporal). Academically interesting; rarely load-bearing in production apps.

## Practical stance

- **Design to 3NF first.** Clean, no redundancy, updates are single-row.
- **Apply indexes and query tuning before denormalizing.**
- **Denormalize with evidence**, not theory: measure slow query, profile, confirm index can't fix it, THEN duplicate data.

## When to denormalize

### 1. Read-path hot spot that indexes can't save

Example: a homepage query joins 6 tables. Everything is indexed. It's still slow because of planner choices or cardinality.

Options:
- Materialized view — refresh strategy must match staleness tolerance
- Denormalized "read model" table — maintained via triggers or async worker
- CQRS — dedicated read store separate from writes

### 2. Aggregations on every read

Example: every product page shows a review count. Joining and counting on every page load is wasteful.

Options:
- Cached count column on `products` — update via trigger or async
- Maintained counter in Redis
- Rebuild from source on a schedule if exact isn't required

### 3. Document model fits the domain

Hierarchical, always-loaded-together data (e.g., a blog post with its inline metadata). A document store naturally denormalizes; embrace it.

### 4. Analytics / reporting

Warehouses are denormalized by design. See Kimball dimensional modeling.

## Costs of denormalization

Every denormalized copy of a value is a **write-time burden** and a **consistency hazard**:

- Update anomalies — change in one place, not others
- Insert anomalies — can't record a fact without also having the denormalized parent
- Delete anomalies — delete a parent, lose denormalized facts about its children

Mitigations:
- **Single writer** — one code path updates both copies atomically
- **CDC-driven** — source of truth drives denormalized projection
- **Triggers** — for simple within-DB denormalization
- **Monotonic reconciliation jobs** — periodic consistency check + fix

## Rules of thumb

- **OLTP, transactional** → 3NF + indexes
- **OLAP, analytical** → star schema (denormalized)
- **Document store** → denormalize aggressively; schema is per-use-case
- **Event store / audit log** → immutable, append-only; no normalization problem

## Common mistakes

- "I denormalized for performance" without measuring the slow query — you just made writes slower
- Denormalized schema with no single writer — drift guaranteed within months
- Over-normalized schema requiring 8 joins for every page — measurable pain; denormalize at least the hot path
- Ignoring 3NF entirely because "we're NoSQL" — document stores still need discipline; schema mistakes are just slower to notice

## See also

- `sql-vs-nosql.md` — document-model denormalization is idiomatic
- `kimball-dimensional.md` — warehouses denormalize on purpose
- `indexing-tradeoffs.md` — try indexing before denormalizing
