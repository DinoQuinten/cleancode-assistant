# Replication

_Source: Designing Data-Intensive Applications (DDIA), Chapter 5 — Replication._

## Concepts

- **Leaders and followers (single-leader)** — the most common setup. Writes to leader; followers asynchronously apply WAL / logical changes.
- **Sync vs async replication** — the durability / latency trade-off. Semi-sync as a practical middle ground.
- **Setting up new followers** — snapshot + catch-up without locking; how Postgres / MySQL / MongoDB do this.
- **Handling node outages** — follower catch-up, leader failover, split-brain, fencing tokens.
- **Replication lag problems**:
  - Read-your-own-writes (session consistency)
  - Monotonic reads (no time travel)
  - Consistent prefix reads (causal ordering)
- **Multi-leader replication** — multi-region, offline clients, concurrent writes.
- **Leaderless replication (Dynamo-style)** — quorum reads/writes (W + R > N), read repair, anti-entropy.
- **Handling conflicts** — last-write-wins, CRDTs, application-level merges.

## Quick reference

| Topology | Pros | Cons | Examples |
|---|---|---|---|
| Single-leader | Simple, linearizable writes | SPOF + failover drama | Postgres, MySQL |
| Multi-leader | Multi-region writes | Conflict resolution hard | Cassandra cross-DC, CouchDB |
| Leaderless | High availability, no failover | Client handles quorum math | Dynamo, Cassandra, Riak |

## See also

- `../../design-principles/references/cap-pacelc.md` — how replication choices project onto CAP/PACELC
- `../../design-principles/references/consistency-models.md` — the consistency guarantees each topology can offer
- `../../design-principles/references/trade-off-catalog.md` — entries 10 (sync/async replication) and 11 (leader topologies)
