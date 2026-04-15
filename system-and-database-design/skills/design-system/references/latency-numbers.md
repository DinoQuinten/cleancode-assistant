# Latency Numbers Every Engineer Should Know

Original: Jeff Dean (Google), ~2012. Updated for 2025 hardware.

## Reference table (2025 values)

| Operation | Latency | Scaled (1 ns = 1 s) |
|---|---|---|
| L1 cache reference | 1 ns | 1 s |
| Branch misprediction | 3 ns | 3 s |
| L2 cache reference | 4 ns | 4 s |
| Mutex lock/unlock (uncontended) | 17 ns | 17 s |
| Main memory reference | 100 ns | 1.5 min |
| Compress 1 KB with Zstd | ~2 μs | 33 min |
| Send 2 KB over 10 Gbps network (same DC) | 0.5 μs | 8 min |
| Read 1 MB sequentially from DRAM | 50 μs | 14 h |
| SSD random read (NVMe) | 10 μs | 2.8 h |
| Read 1 MB sequentially from NVMe SSD | 100 μs | 1.2 d |
| Round-trip within same datacenter | 0.5 ms | 5.8 d |
| Read 1 MB sequentially from spinning disk | 20 ms | 7.6 mo |
| Disk seek (spinning) | 3 ms | 1.2 mo |
| Round-trip within same region (cross-AZ) | 1-2 ms | 1-2 wk |
| TLS handshake (full, with CA chain verify) | 10-30 ms | 4-12 mo |
| Round-trip continent-to-continent (US-EU) | 80-100 ms | 2.5-3 yr |
| Round-trip continent-to-continent (US-Asia) | 150-200 ms | 5-6 yr |
| Typical Postgres simple query (well-indexed) | 1 ms | 12 d |
| Typical Redis GET | 0.1-0.5 ms | 1-5 d |
| HTTP request p50 to local service | 10-50 ms | 4-20 mo |
| LLM first-token (Claude/GPT-4-class, warm) | 400-800 ms | 13-25 yr |
| LLM full response (100 tokens, streaming) | 2-5 s | 60-150 yr |

Interpret "scaled" as: if 1 ns were 1 second, here's how long the operation would feel. A cross-continent round-trip is three years.

## Throughput rules of thumb

| Resource | Throughput |
|---|---|
| NVMe SSD sequential read | 3-7 GB/s |
| NVMe SSD random 4 KB IOPS | 500k-1M |
| Spinning disk sequential | 100-250 MB/s |
| 10 Gbps NIC | ~1.2 GB/s |
| 25 Gbps NIC | ~3 GB/s |
| Single Postgres connection | ~1k-10k simple queries/s |
| Redis single instance | ~100k ops/s |
| Kafka single partition | ~10-50k msgs/s (small msgs) |

## Design implications

- **Minimize round-trips.** One call that returns 1 MB beats 1000 calls each returning 1 KB (serial). Parallelize or batch.
- **Keep hot data in RAM.** Disk is 1000x slower than RAM; network RTT is another 10x on top.
- **Locality wins.** Same-AZ beats cross-AZ (~3x). Same-region beats cross-region (50-100x). Same-continent beats cross-continent (~80x).
- **Budget your latency.** If your SLO is 500 ms p99 and you have 3 serial hops, each hop gets 150 ms minus parsing/serialization.
- **Parallelize siblings.** If you need data from 3 services independently, parallel fanout costs max(a, b, c), not a+b+c.
- **Compress judiciously.** Over fast local networks (10 Gbps+), compression may cost more CPU than the bandwidth saves. Across WAN, nearly always worth it.

## See also

- `capacity-estimation.md` — applies these numbers to real designs
- `caching.md` — exists specifically to dodge the table's slow rows
- `load-balancing.md` — same-AZ routing vs cross-AZ is a latency decision
