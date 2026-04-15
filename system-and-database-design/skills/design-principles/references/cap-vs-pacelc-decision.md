# CAP vs PACELC — A Decision Guide

## Recap

**CAP**: during a **partition**, choose between **consistency** (reject/delay to stay consistent) and **availability** (serve, possibly inconsistent). You don't get both.

**PACELC** extends CAP: **if P**artitioned, choose C or A; **E**lse (normal operation), choose **L**atency or **C**onsistency.

PACELC is more realistic. Partitions are rare; the everyday trade-off IS latency-vs-consistency.

## Decision framework

For each data store in your design, classify it along two axes:

1. **During partition**: CP or AP?
2. **Else (normal)**: EL (favor latency) or EC (favor consistency)?

## Common system classifications

| System | PACELC | Why |
|---|---|---|
| **Postgres (single primary + sync replica)** | PC/EC | Writes wait for sync replica; reads from primary are consistent |
| **Postgres (async replica)** | PC/EL | Writes only wait for primary; reads from replicas can be stale |
| **MySQL + semi-sync** | PC/EL | Mostly durable on primary; tunable |
| **MongoDB (majority write)** | PC/EC | Tunable; majority = CP-leaning |
| **Cassandra (tunable)** | PA/EL | AP by default; tunable per-request via consistency levels |
| **DynamoDB (strong consistency read)** | PC/EC | Single-region strongly consistent if you ask for it |
| **DynamoDB (eventual consistency read)** | PA/EL | Cheaper, faster; may read stale |
| **Cosmos DB** | Tunable across 5 levels | Strong, bounded staleness, session, consistent prefix, eventual |
| **Spanner** | PC/EC (global!) | TrueTime makes global strong consistency tractable |
| **CockroachDB** | PC/EC | Spanner-style across multi-region |
| **etcd / ZooKeeper / Consul** | PC/EC | Consensus-based; used FOR coordination, not as primary data store |
| **Kafka** | PC/EL (tunable) | Strong within partition; latency favored via `acks` |
| **Redis (single primary)** | PA/EL | Fast, simple; primary failure = data loss window |
| **Redis Cluster** | PA/EL | Partition-tolerant with some data loss possible |

## How to choose

### When you MUST pick CP

- Financial transactions (balance, transfers, order-matching)
- Inventory (prevent overselling)
- Unique constraints (usernames, SKUs)
- Any operation where "I saw X, then did Y based on X" must stay coherent

### When AP is fine (or required)

- Analytics event ingestion (slight dupe / loss acceptable)
- Social feeds (seeing a stale post is OK)
- Presence / session tracking (stale "online" OK for seconds)
- Caches (by definition)
- Shopping carts (eventual reconcile acceptable; some systems do this)

### When EL (latency) matters more than perfect EC

- User-facing read latency SLO < 100 ms across regions
- Any geographically distributed read-heavy workload
- Most content serving (blog posts, product detail)

### When EC matters over EL

- Single-writer domains where confusion costs real money
- Authoritative lookups for other services (service registry, feature flag store, billing data)

## Multi-region realities

Global strong consistency (EC during normal ops, across regions) costs ~100-200 ms per write due to cross-region consensus. Spanner / Cockroach / Yugabyte make this tractable but not free.

Common pattern:
- **Regional leader per tenant** — each tenant is primary in one region; writes stay fast there
- **Read-local replicas** elsewhere — fast reads, eventual consistency
- **Re-shard on relocation** — user moves regions → plan in advance

## Common mistakes

- Claiming "CA" — doesn't exist under CAP's definitions
- Treating consistency as a binary — there are many models (linearizable, sequential, causal, bounded-stale, eventual); pick the weakest one that works
- Strong consistency for a feature that never sees conflicts — wasted latency
- Eventual consistency where users can observe ordering violations — confusion, bug reports

## See also

- `cap-pacelc.md` — the formal theory (DDIA ch. 9 extract)
- `consistency-models.md` — specific models beyond "strong vs eventual"
- `consensus.md` — how CP systems actually do it
- `trade-off-catalog.md` — catalog of related trade-offs
