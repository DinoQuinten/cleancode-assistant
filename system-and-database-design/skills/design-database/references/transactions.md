# Transactions

_Source: Designing Data-Intensive Applications (DDIA), Chapter 7 — Transactions._

## Concepts

- **ACID** — atomicity, consistency, isolation, durability; what each actually guarantees (and what it doesn't).
- **Single-object vs multi-object** — most databases guarantee atomicity/isolation only for single-object ops unless you start a transaction.
- **Weak isolation levels** and the anomalies each allows:
  - **Read committed** — no dirty reads, no dirty writes. Still allows non-repeatable reads.
  - **Snapshot isolation / repeatable read** — MVCC; each transaction sees a consistent snapshot. Allows write skew.
  - **Serializable** — as if transactions ran one at a time. Costly.
- **Anomalies** — dirty read, dirty write, read skew, lost update, write skew, phantom.
- **Preventing lost updates** — atomic operations (`UPDATE ... SET x = x + 1`), explicit locking (`SELECT ... FOR UPDATE`), automatic detection + retry, compare-and-set.
- **Serializability implementations**:
  - Actual serial execution (VoltDB, Redis)
  - Two-phase locking (2PL)
  - Serializable snapshot isolation (SSI) — Postgres
- **How to choose** — most apps need at least snapshot isolation; serializable only where write skew matters (bank transfers, inventory, scheduling).

## Quick reference

| Isolation level | Prevents | Allows |
|---|---|---|
| Read uncommitted | — | Dirty reads |
| Read committed | Dirty reads, dirty writes | Non-repeatable reads, phantoms, write skew |
| Snapshot / repeatable read | Non-repeatable reads | Write skew, phantoms (MySQL InnoDB prevents phantoms) |
| Serializable | All classic anomalies | — |

Postgres defaults: Read Committed. MySQL InnoDB: Repeatable Read. Use `SET TRANSACTION ISOLATION LEVEL SERIALIZABLE` where correctness demands.

## See also

- `distributed-transactions.md` — when transactions span services
- `../../design-principles/references/trade-off-catalog.md` — entry 19 (ACID vs BASE)
