# Probabilistic Data Structures at Scale

Authoritative sources: DDIA (Bloom filter brief), original papers (Bloom 1970, Flajolet HLL 2007, Cormode & Muthukrishnan CMS 2005), RedisBloom module, ClickHouse docs.

These structures trade accuracy for massive space / time savings. Use them where "approximate but fast" beats "exact but slow."

## Bloom filter — "is this value maybe present?"

- Bitmap of `m` bits; `k` hash functions
- Insert: set bits at `hash_i(x) mod m` for each hash
- Query: check same bits; if all set, **maybe present** (false positives possible); any unset, **definitely absent**

**False positive rate** ≈ `(1 - e^(-kn/m))^k`. For n items, target FPR p, choose:
- `m = -n · ln(p) / (ln 2)^2`
- `k = (m/n) · ln 2`

For 1 M items at 1% FPR: m ≈ 9.6 M bits ≈ 1.2 MB, k ≈ 7.

### Uses

- Skip fetching items unlikely to exist (cache negative lookups, LSM-tree bloom per SSTable — massive I/O savings)
- Avoid re-processing already-seen URLs in crawlers
- Join reduction in distributed queries (ship Bloom filter; filter data before shuffle)

### Limits

- No deletion (unless counting Bloom, which uses more space)
- Size is fixed; plan for final n

### Variants

- **Counting Bloom** — cells are counters; supports deletion
- **Cuckoo filter** — deletion + lower FPR for same space; more complex
- **Quotient filter** — mergeable; better cache behavior

## HyperLogLog — "cardinality estimate"

Estimate the number of distinct values in a stream with fixed memory (~12 KB for ±1% error on up to 2^64 elements).

Core idea: hash each element; count trailing zeros in hash; the maximum zeros seen correlates with log2(n).

Redis `PFADD` / `PFCOUNT` / `PFMERGE` is this.

### Uses

- Unique visitors per day / hour
- Distinct-users-per-feature metrics
- Distinct-key dashboards in monitoring
- De-dup in analytics without materializing the set

### Limits

- Cardinality only; can't tell you WHICH values are present
- Merge semantics are great (union); intersection requires inclusion-exclusion

## Count-Min Sketch — "approximate frequency"

2D matrix of counters; each item hashed by `d` hash functions to one column per row; increment those counters; read: min of those counters.

Overestimates; never underestimates.

Parameters: width w = ⌈e/ε⌉ for ±ε error, depth d = ⌈ln(1/δ)⌉ for 1-δ confidence.

### Uses

- Top-K heavy hitters (streaming analytics)
- Rate limiting at massive scale (per-key counters)
- Anomaly detection (which keys are spiking?)
- Log analysis (most frequent errors, URLs, users)

## Merkle tree — "verify + pinpoint differences"

Tree of hashes; each parent is the hash of its children's hashes; root summarizes the entire dataset.

### Uses

- Git (tree objects)
- Blockchains
- Cassandra / DynamoDB anti-entropy — compare Merkle trees between replicas to find which partitions diverged, without transferring all data
- Content-addressable storage (IPFS, S3 multipart ETags)
- Certificate Transparency

### Property

O(log n) to prove "this record is in the set with root hash R" (Merkle proof).

## Skip list

Probabilistic balanced structure: ordered linked list with randomized "express lanes" at higher levels. O(log n) expected search/insert/delete.

### Uses

- Redis sorted sets (ZSET)
- Concurrent-friendly alternative to B-trees (easier lock-free implementations)
- LevelDB memtable

## Reservoir sampling — "uniform sample of a stream"

Keep k items; for the i-th item (i > k), replace a random one with probability k/i. Result: uniform random k-sample of an unknown-length stream.

### Uses

- Trace sampling (head sampling)
- A/B experiment audit samples
- Anything where the full stream is too big but a uniform sample suffices

## T-digest / HDR histogram — "accurate quantiles"

Compressed representation of a distribution accurate at the tails (p99, p99.9).

### Uses

- Latency percentile metrics (Prometheus histograms, Datadog, Honeycomb)
- SLO measurement — averages hide tails; medians hide worse; percentiles are the truth

## When to reach for these

If your problem matches any of these:

- "Count distinct X per day across 1B events" → HyperLogLog
- "Check if key exists, avoid expensive lookup for non-existent keys" → Bloom filter
- "Which items are the most frequent in a stream too large to sort?" → Count-Min + heap
- "Find which partitions diverged across replicas without shipping data" → Merkle
- "Accurate p99 latencies over a long window with bounded memory" → T-digest / HDR

## See also

- `../../design-database/references/indexing-tradeoffs.md` — Bloom filters inside LSM trees
- `../../design-system/references/observability.md` — percentile structures for SLOs
