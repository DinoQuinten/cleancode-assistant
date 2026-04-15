# Cross-Book Trade-off Catalog

A distilled index of trade-offs across DDIA, Fundamentals of Software Architecture, and Kimball. Each entry: the axis, the two extremes, and guidance for choosing.

## 1. Consistency ↔ Latency

**Strong consistency** = wait for all replicas/quorum → higher latency. **Eventual** = return fast, reconcile later.

Pick strong when staleness causes incorrect decisions (inventory, balances). Pick eventual when user-visible staleness is acceptable for the latency win.

## 2. Consistency ↔ Availability (during partition)

**CP** = refuse to serve when partitioned. **AP** = serve, accept divergence, reconcile later.

Pick CP for correctness-critical writes. Pick AP for high-read-volume, low-correctness-stakes data.

## 3. Normalize ↔ Denormalize

**Normal form** = one place per fact → cheap writes, expensive reads. **Denormalized** = many copies → cheap reads, expensive writes + drift risk.

Start normalized. Denormalize the hot read path only, with a single writer to prevent drift.

## 4. Latency ↔ Throughput

Optimizing for one usually costs the other. Batching improves throughput, worsens per-item latency. Pipelining helps both if stages are balanced.

## 5. Monolith ↔ Microservices

**Monolith**: fast change, simple deploy, easy cross-cutting tx, scaling is all-or-nothing. **Microservices**: team independence, independent scale, operational complexity, distributed-systems debugging.

Default to modular monolith. Split only when team or scale pressure forces it.

## 6. Sync ↔ Async

**Sync**: simple, request/response, tight coupling, cascading failures. **Async**: decoupled, retryable, eventual, harder to reason about and debug.

Sync for user-facing request paths. Async for slow work, multi-consumer events, and cross-team integration.

## 7. REST ↔ GraphQL ↔ gRPC

**REST**: public, cacheable, standard, verbose. **GraphQL**: flexible clients, N+1 trap, auth complexity. **gRPC**: fast, schemas, not browser-native.

Public → REST. Multi-client with varied needs → GraphQL. Internal service-to-service → gRPC.

## 8. SQL ↔ NoSQL

**Relational**: joins, constraints, transactions, rigid schema. **Document/KV/column**: flexible schema, horizontal scale, limited joins.

Default to Postgres. Pick NoSQL when workload demands outweigh the cost of giving up joins + transactions.

## 9. Range ↔ Hash partitioning

**Range**: efficient range scans, hot-spots on monotonic keys. **Hash**: uniform distribution, range queries require scatter-gather.

Range for timestamps / sorted access. Hash for point lookups, high write volume.

## 10. Synchronous ↔ Asynchronous replication

**Sync**: durability, write latency includes replica write. **Async**: fast writes, data-loss window on leader failure.

Use sync for critical financial data (even so, usually semi-sync: wait for 1 replica). Async for read-scaling replicas where durability is covered by sync primary.

## 11. Single-leader ↔ Multi-leader ↔ Leaderless

- **Single-leader**: simple, linearizable writes, SPOF + failover drama
- **Multi-leader**: multi-region writes, conflicts
- **Leaderless (Dynamo-style)**: high availability, client handles quorum math

Single-leader is the sane default. Multi-leader only when multi-region writes are mandatory.

## 12. 2PC ↔ Saga

**2PC**: strong consistency across services, coordinator is SPOF, blocking, slow. **Saga**: eventually consistent, compensating tx on failure, non-blocking.

Saga wins for microservices. 2PC only in single-DB with XA if at all.

## 13. Batch ↔ Stream

**Batch**: simple, large-volume, latency hours. **Stream**: real-time, stateful, complex.

Default batch. Stream only where the business value justifies the complexity.

## 14. CAP consistency levels (Cosmos DB model)

Strong > Bounded Staleness > Session > Consistent Prefix > Eventual.

Each step down buys lower latency, higher availability. Pick the weakest that satisfies the semantics the user can observe.

## 15. Index more ↔ Index less

More indexes: faster reads on more queries, slower writes, more storage. Fewer: opposite.

Index the top-N queries by latency impact × frequency. Remove unused indexes periodically.

## 16. Early optimization ↔ YAGNI

Distributed systems tempt premature optimization. Pick the simplest thing that satisfies your NON-functional requirements at current + next-year scale. Don't design for 10 years ahead.

## 17. Resilience ↔ Simplicity

Every resilience pattern (circuit breaker, retry, bulkhead) adds complexity. Don't sprinkle them "just in case." Add where failure modes are documented and tested.

## 18. Write-optimized ↔ Read-optimized

**LSM trees (RocksDB, Cassandra)**: fast writes, background compaction, reads may hit multiple files. **B-trees (Postgres, MySQL)**: balanced; writes slower due to page updates.

Write-heavy workloads favor LSM. Mixed / read-heavy favor B-tree.

## 19. ACID ↔ BASE

**ACID**: atomic, consistent, isolated, durable. **BASE**: basically available, soft state, eventual consistency.

ACID at the single-DB layer. BASE at the distributed system layer. Not really opposed — most real systems have ACID islands in a BASE sea.

## 20. Idempotency cost ↔ Correctness

Idempotency keys, dedup, and exactly-once semantics all cost storage and code complexity. But without them, retries cause duplicate side effects.

Budget idempotency at the external boundary (every external write accepts an idempotency key) and internal boundaries where retries occur.

## How to use

When a design decision is contested, identify the axis and the cost of each side. Make the trade-off explicit in the design doc. The decision is less important than the explicitness.

## See also

- `cap-vs-pacelc-decision.md` — applies trade-offs 1-2 concretely
- `../../review-architecture/references/anti-patterns.md` — what happens when trade-offs are ignored
