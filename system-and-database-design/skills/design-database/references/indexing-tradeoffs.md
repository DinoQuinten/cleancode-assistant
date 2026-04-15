# Indexing Trade-offs

_Source: Designing Data-Intensive Applications (DDIA), Chapter 3 — Storage and Retrieval._

## Concepts

- **Hash indexes** — Bitcask-style: in-memory hash map + append-only log. Great for keys that fit in RAM.
- **SSTables + LSM-trees** — sorted, merged segments (LevelDB, RocksDB, Cassandra). Fast writes, compaction overhead, tombstones.
- **B-trees** — the default relational index (Postgres, MySQL, SQLite). Balanced, in-place updates, WAL for crash recovery.
- **LSM vs B-tree trade-offs** — write amplification vs read amplification; which workload prefers each.
- **Secondary indexes** — non-unique, with row references or clustered index lookups.
- **Covering / clustered indexes** — index contains all queried columns; avoid heap lookup.
- **Multi-column indexes** — order matters; concatenated index vs independent.
- **Fuzzy / full-text indexes** — Lucene, trigrams, GIN in Postgres.
- **In-memory databases** — Redis, Memcached — different durability trade-offs.

## Quick reference

| Index type | Best for | Write cost | Read cost |
|---|---|---|---|
| Hash | Point lookup by key | O(1) write | O(1) point, no range |
| LSM-tree | Write-heavy, range scan | Log-structured, cheap | Multiple SSTable reads + bloom |
| B-tree | Mixed / read-heavy | Page update + WAL | O(log n) |
| Bitmap | Low-cardinality columns, analytics | Expensive on update | Fast boolean ops |
| Inverted | Full-text search | High (tokenization) | Fast term lookup |
| GIN (Postgres) | Array / JSON / FTS | High | Fast containment |
| BRIN (Postgres) | Huge time-series tables | Minimal | Good for correlated columns |

## See also

- `../../design-system/references/capacity-estimation.md` — rough cost per index in storage + write latency
- `../../design-principles/references/trade-off-catalog.md` — entries 15 (index more/less) and 18 (LSM vs B-tree)
