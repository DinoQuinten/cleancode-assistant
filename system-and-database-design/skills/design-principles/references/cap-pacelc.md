# CAP and PACELC

_Source: Designing Data-Intensive Applications (DDIA), Chapter 9 (Consistency and Consensus)._

## Concepts (DDIA ch. 9 subset)

- **CAP theorem** — in a network partition, a distributed system must choose between consistency (reject or delay) and availability (serve, possibly inconsistent). You cannot have both during a partition.
- **Why "CA" is meaningless** — partitions are a fact of distributed systems. CAP is P-and-(C-or-A), not a free choice among three.
- **Linearizability** — the strongest single-object consistency model; behaves as if there's one copy and operations are atomic. Expensive.
- **Why linearizability is useful** — locks, uniqueness constraints, cross-channel time-of-check vs time-of-use.
- **The cost** — linearizability requires consensus; coordination kills availability during partition and latency always.
- **Alternatives** — sequential consistency, causal consistency, consistent-prefix, session guarantees.

## PACELC

**PACELC** (Abadi 2012) extends CAP:

> **If P**artitioned, choose C or A. **E**lse, choose **L**atency or **C**onsistency.

PACELC is more honest because partitions are rare and short. The everyday trade-off **is** latency vs consistency, not availability vs consistency.

| System | PACELC | Why |
|---|---|---|
| Postgres (sync replica) | PC/EC | Writes wait for sync replica |
| Postgres (async replica) | PC/EL | Reads from replicas can lag |
| Cassandra (tunable) | PA/EL | AP by default; tunable via consistency levels |
| DynamoDB (strong read) | PC/EC | Quorum read across replicas |
| DynamoDB (eventual read) | PA/EL | Cheaper, faster, may read stale |
| Spanner | PC/EC globally | TrueTime-based external consistency |
| CockroachDB | PC/EC | Spanner-style across multi-region |
| Kafka | PC/EL tunable | `acks=1` favors latency; `acks=all` favors durability |
| Redis primary | PA/EL | Async replication; small data-loss window on failover |

## See also

- `cap-vs-pacelc-decision.md` — how to actually pick C or A for your use case
- `consistency-models.md` — the spectrum between linearizable and eventual
- `consensus.md` — how CP systems actually do it
- `trade-off-catalog.md` — entries 1 (consistency/latency) and 2 (consistency/availability)
