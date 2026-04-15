# Capacity Estimation

Back-of-envelope math: the skill that separates engineers who can defend a design from engineers who can only describe one.

## The template

For any proposed system, compute at minimum:

1. **Peak QPS (read)**
2. **Peak QPS (write)**
3. **Storage — 1 year growth**
4. **Bandwidth in/out**
5. **Memory — hot working set**

Round generously (2-3 sig figs). Use base-10 for user-ish counts, base-2 for bytes.

## Unit shortcuts

- 1 day = 86,400 s ≈ **100 k s**
- 1 year ≈ 365 days ≈ **30 M s**
- 1 day of 1 QPS = 86 k events → "average 1 QPS for a day yields ~100 k events"
- 1 year of 1 QPS = ~30 M events
- 1 M users × 10 actions/day = 10 M actions/day = **~120 actions/sec avg**
- **Peak = 2-10x average** for consumer products with diurnal patterns

## Storage base units

| Base-10 | Bytes (base-2 approx) |
|---|---|
| 1 KB = 10^3 | 1 KiB = 2^10 = 1,024 |
| 1 MB = 10^6 | 1 MiB = 2^20 ≈ 1.05 × 10^6 |
| 1 GB = 10^9 | 1 GiB = 2^30 ≈ 1.07 × 10^9 |
| 1 TB = 10^12 | 1 TiB = 2^40 |
| 1 PB = 10^15 | 1 PiB = 2^50 |

Close enough to treat interchangeably unless you're sizing a storage cluster to the GB.

## Row-size heuristics

- 1 UUID = 16 bytes binary, 36 bytes text
- 1 int = 4 bytes, 1 bigint = 8 bytes
- 1 timestamp = 8 bytes
- 1 typical string (name, slug) = 32-128 bytes
- 1 row with ~10 columns of mixed types = ~100-300 bytes
- Indexes commonly 1-3x the base table size

## Worked example: URL shortener

**Assumptions**:
- 100 M users, 10 % create a link per day → 10 M new links/day
- Read-to-write ratio: 100:1
- Avg click-through: 100 per link

Derived:
- **Write QPS**: 10 M / 100 k = **~100 writes/s avg**; peak ~1 k/s
- **Read QPS**: 100 × 100 = 10 k ×... wait, average reads = writes × read/write ratio = 100 × 100 = 10 k/s avg; peak ~100 k/s

- **Row size** for a link: shortcode (8 B) + longurl (~500 B) + metadata (~50 B) ≈ 600 B
- **1-year storage**: 10 M links/day × 365 days × 600 B ≈ **2.2 TB/year** for raw data; ~6 TB with indexes

- **Read bandwidth**: 10 k QPS × 600 B = 6 MB/s avg; peak ~60 MB/s
- **Write bandwidth**: negligible

- **Hot set**: 80/20 rule → 20% of links get 80% of clicks; 20 % × yearly links ≈ 700 M rows × 600 B ≈ 400 GB — fits in RAM on one large box, or a medium Redis cluster

**Design implications**:
- Write volume (100-1 k/s) is trivial — single Postgres instance handles it
- Read volume (10 k-100 k/s) needs caching; Redis or a fat read-replica tier
- Storage (~6 TB) is still single-machine territory on modern NVMe; no sharding needed
- Conclusion: **a monolith + Postgres + Redis cache scales this to 100 M users**

The lesson: consumer systems rarely need the heroics their hype suggests. Do the math first.

## Worked example: real-time chat

**Assumptions**:
- 10 M DAU
- Avg session: 30 min online
- Avg messages sent: 20 / user / day
- Avg recipients per message: 5 (small groups dominate)

Derived:
- **Concurrent WebSocket connections**: 10 M DAU × (30 min / 24 h avg over day) = ~200 k peak concurrent; multiply by 3-5x peak-vs-avg → **~600 k-1 M peak connections**
- **Inbound msgs/s**: 10 M × 20 / 100 k ≈ **2 k/s avg**; peak ~10 k/s
- **Fanout msgs/s**: 10 k × 5 = **50 k/s of fanout writes**
- **Storage per msg**: ~500 B (body + metadata) × 10 M × 20 = **100 GB/day** of raw chat history; **~35 TB/year**

**Design implications**:
- 1 M concurrent connections / 100 k per WebSocket gateway = **10-20 gateway servers**
- 35 TB/yr storage: use a TSDB or hot/cold Cassandra pattern; shard by user or chat room
- Fanout at 50 k/s needs pub/sub backbone (Kafka, Redis pub/sub)
- Hot read patterns: last 50 messages per chat → in-memory cache sized by active-chat count

## Heuristics

- If peak QPS < **1 k**, do NOT design a distributed system. One box + one DB + one cache.
- If storage < **1 TB**, no sharding. Single-instance + replication.
- If read:write > **10:1**, caching is ALWAYS the answer. Figure out cache invalidation before geography.
- If write:read > **1:1**, think carefully about the DB engine — LSM-based stores (Cassandra, RocksDB) beat B-tree engines on write-heavy workloads.
- **Don't confuse OPS throughput with CPU cost.** 100 k Redis GETs/sec is easy on 1 core; 100 k JWT verifications/sec needs 10+ cores.

## Cost estimation (2025 cloud prices, rough)

- EC2 `m7i.large` (2 vCPU, 8 GB RAM): ~$60/mo
- RDS Postgres `db.r7g.2xlarge`: ~$650/mo + storage
- DynamoDB 1k RCU + 1k WCU: ~$200/mo
- 1 TB S3 standard: ~$25/mo
- 1 TB egress (to internet): ~$90
- 1 TB egress (between AWS regions): ~$20
- 1 TB inter-AZ: ~$10

## See also

- `latency-numbers.md` — every QPS estimate is shaped by per-operation latency
- `../design-database/references/sharding-partitioning.md` — trigger for sharding is size AND QPS
