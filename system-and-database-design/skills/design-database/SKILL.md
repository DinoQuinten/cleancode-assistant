---
name: design-database
description: Proposes a database schema (SQL or NoSQL) for a given domain. Use when the user asks to "design a database", "model data for X", "build an ER", pick SQL vs NoSQL, or invokes /design-database. Grounded in DDIA and Kimball.
argument-hint: "<domain, e.g. 'e-commerce catalog' or 'SaaS billing'>"
allowed-tools: Read, Write, Grep, Glob
---

# design-database

Design a DB that survives real load and schema change. Opinionated, not a survey.

## Process

1. **Workload first, entities second.** Answer: read/write ratio, top 3–5 queries, 1-year volume, transactional boundaries, consistency need, query shape (point/range/join/agg/search).
2. **Pick the store.** Default **Postgres**. Choose NoSQL only for a workload reason. Ref: `sql-vs-nosql.md`.
3. **OLTP vs OLAP.** Analytical → Kimball star schema (`kimball-dimensional.md`). Mixed → CDC into a separate warehouse.
4. **Schema sketch.** Entities, tables/collections with types + nullability + constraints, PK/FK, indexes (ref `indexing-tradeoffs.md`), uniqueness + check constraints.
5. **Normalization.** Default 3NF for OLTP (`normalization.md`). Denormalize only the hot read path, with a documented plan to prevent drift.
6. **Transactions.** State required isolation per multi-row operation (`transactions.md`). Cross-service → saga + outbox + idempotency keys (`distributed-transactions.md`).
7. **Scale strategy.** Replication topology (`replication.md`), sharding key + hot-partition mitigation (`sharding-partitioning.md`). Don't shard prematurely.
8. **Schema evolution.** Expand-contract, backfill, reversible migrations (`schema-evolution.md`). Never drop in a single deploy.
9. **Ops.** PITR window, RPO/RTO, backup frequency + retention, restore-drill cadence.

## Reference lookup

`sql-vs-nosql.md` · `kimball-dimensional.md` · `normalization.md` · `indexing-tradeoffs.md` · `transactions.md` · `distributed-transactions.md` · `replication.md` · `sharding-partitioning.md` · `schema-evolution.md`

Load only the ones relevant to the current step.

## Output skeleton

```markdown
# Database Design: <domain>

## 1. Workload  (ratio, top queries, volume, consistency)
## 2. Store choice  (engine, one-paragraph justification)
## 3. Schema  (tables/collections, indexes)
## 4. Transactions & consistency  (isolation per op)
## 5. Scale strategy  (replication, sharding, hotspots)
## 6. Schema evolution  (migration plan)
## 7. Operations  (backup, DR, monitoring)
## 8. Trade-offs & alternatives considered
```

Offer to generate a DBML diagram via the `diagram` skill and save to `./designs/db-<kebab-name>.md`.
