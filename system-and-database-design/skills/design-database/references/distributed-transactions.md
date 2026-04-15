# Distributed Transactions

_Source: Designing Data-Intensive Applications (DDIA), Chapter 9 (Consistency and Consensus) — plus author-added saga/outbox content._

## Concepts (DDIA ch. 9 subset)

- **Atomic commit and two-phase commit (2PC)** — coordinator prepares, then commits. Blocking, slow, coordinator is SPOF.
- **Three-phase commit (3PC)** — attempts to reduce blocking; assumes bounded network delay (rarely holds).
- **Fault-tolerant consensus** — Paxos, Raft, Zab underlie the "happy path" for distributed commit.
- **XA transactions** — cross-database 2PC. Works in theory, painful in practice.

## Saga pattern

The pragmatic alternative to 2PC for microservices. A long-running business transaction is modeled as a sequence of local transactions, each with a compensating action.

- **Orchestration saga** — central coordinator drives steps. Easier to reason about, but the coordinator is a bottleneck.
- **Choreography saga** — each service publishes events; others react. Decentralized, but flow is scattered across services.
- **Compensating actions** — semantic undo (refund, cancel), not a `ROLLBACK`. Must be idempotent and commutative where possible.
- **Failure modes** — compensating action itself fails → manual intervention queue.

## Transactional outbox

The durable way to publish an event **atomically with a DB write**, without 2PC.

1. In the same transaction as the business write, `INSERT INTO outbox (event)`.
2. A relay process polls or tails WAL → publishes to the broker → marks the outbox row consumed.
3. At-least-once delivery; consumers must be idempotent.

Alternative: **change data capture (CDC)** via Debezium / logical replication — read the WAL directly and publish. No outbox table, but tighter coupling to the DB.

## Idempotency keys at boundaries

Every external write endpoint accepts `Idempotency-Key`. Server stores key → result for a TTL. Retries return the cached result. This is non-negotiable for any payment or order flow.

## See also

- `transactions.md` — single-DB isolation levels
- `../../design-system/references/microservices-patterns.md` — saga + outbox in context
- `../../design-principles/references/consensus.md` — what the coordinator is built on
- `../../design-principles/references/trade-off-catalog.md` — entry 12 (2PC vs Saga)
