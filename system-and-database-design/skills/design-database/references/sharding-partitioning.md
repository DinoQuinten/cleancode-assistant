# Sharding and Partitioning

_Source: Designing Data-Intensive Applications (DDIA), Chapter 6 — Partitioning._

## Concepts

- **Why partition** — scaling beyond one machine; independent scale per partition.
- **Key-range partitioning** — Bigtable / HBase style; great for range scans, prone to hot-spots on monotonic keys (e.g. timestamps).
- **Hash-range partitioning** — hash the key, then range-partition the hash; uniform distribution, range queries require scatter-gather.
- **Consistent hashing** — minimal reshuffling when nodes join/leave (Dynamo, Cassandra, Riak).
- **Skewed workloads and hot spots** — celebrity problem, append hotspots, fix via random prefix or composite key.
- **Secondary indexes** — local (partitioned by document) vs global (partitioned by term); scatter-gather vs write fan-out.
- **Rebalancing** — fixed number of partitions, dynamic partitioning, partitioning proportional to nodes.
- **Request routing** — client routing, routing tier, server-side routing; ZooKeeper / etcd for metadata.

## Quick reference

| Scheme | Good for | Bad for |
|---|---|---|
| Range | Range scans, time-series (with salt) | Monotonic keys → hot shard |
| Hash | Uniform writes, point lookup | Range queries need scatter-gather |
| Consistent hash | Dynamic cluster size | Still needs virtual nodes to balance |
| Composite (tenant_id + hash) | Multi-tenant SaaS | Cross-tenant queries |

## See also

- `replication.md` — partitioning + replication are orthogonal; every real system does both
- `../../design-principles/references/trade-off-catalog.md` — entry 9 (range vs hash)
