# System and Database Design Instructions

Source of truth: .sdd-principles.md
Package: sdd-codex

## Purpose

Use these instructions whenever the user asks for architecture, database design, distributed-systems trade-offs, reliability, scaling, consistency, consensus, idempotency, or design review. Be concrete, quantitative when possible, and explicit about trade-offs.

## Trigger Topics

Apply this guidance when the user mentions CAP, PACELC, linearizable, serializable, causal, eventual, read-your-writes, monotonic reads, Raft, Paxos, quorum, Byzantine, ACID, BASE, snapshot isolation, phantom read, write skew, lost update, idempotency, delivery guarantees, Bloom filters, HyperLogLog, Count-Min sketches, Merkle trees, vector clocks, Lamport clocks, or hybrid logical clocks.

## Answer Shape for Principles

When explaining a principle, answer in four parts:

1. Precise one-sentence definition.
2. Intuition with a minimal example, preferably a 3-node or single-request scenario.
3. Production failure the concept prevents or exposes.
4. Decision guidance with named systems or concrete design choices.

Always caveat distributed-systems claims. Prefer "under partition this design gives up X because Y" over universal statements.

## Core Design Rules

### CAP and PACELC

- CAP only matters during a network partition: choose consistency by rejecting or delaying, or choose availability by serving potentially divergent data.
- Do not describe systems as CA. Partitions are part of the model.
- PACELC is the everyday framing: if partitioned, choose consistency or availability; else choose latency or consistency.
- Classify each data store by partition behavior and normal-operation behavior, for example PC/EC, PC/EL, PA/EL.

### Consistency Models

- Pick the weakest consistency model the user-visible semantics tolerate.
- Linearizability is for locks, uniqueness, account debits, inventory decrement, and compare-and-swap.
- Session guarantees are enough for many user workflows: read-your-writes, monotonic reads, and writes-follow-reads.
- Eventual consistency only promises convergence when writes stop; it does not give a time bound.
- If ordering matters to users, consider causal consistency or consistent-prefix instead of raw eventual consistency.

### Consensus and Quorums

- Do not roll your own consensus. Use etcd, ZooKeeper, Consul, a database that already implements it, or a managed coordination service.
- Use consensus stores for coordination, not high-volume primary data.
- Prefer 3 or 5 nodes. Larger quorums usually add latency without much practical fault-tolerance benefit.
- For split-brain risk, leader election is not enough; require fencing tokens or another monotonic ownership proof.
- Quorum reads and writes need W + R > N for strong read-after-write behavior.

### Idempotency and Delivery

- Retries turn partial failures into duplicate side effects unless write operations are idempotent.
- External write APIs should accept idempotency keys when clients may retry.
- Internal async workflows need deduplication at every boundary that can redeliver.
- "Exactly once" usually means at-least-once delivery plus idempotent processing and transactional offset/state updates.
- Use outbox or saga patterns for cross-service workflows instead of pretending a distributed transaction is free.

### Probabilistic Sketches

- Bloom filter: "definitely absent or maybe present"; use for negative lookup avoidance and duplicate prechecks.
- HyperLogLog: approximate distinct counts with fixed memory; use for unique visitors or cardinality dashboards.
- Count-Min sketch: approximate frequencies; use for heavy hitters, rate-limit estimation, and stream analytics.
- Merkle tree: compare large replicated datasets by hashes; use for anti-entropy and content verification.
- State the approximation cost: false positives, no item identity, overestimation, or hash-tree maintenance.

## Workflow Mappings

Codex does not have Claude plugin slash commands. Treat the system-and-database-design commands as natural-language behaviors:

- When the user asks to design a system, produce a design doc with requirements, assumptions, capacity math, components, data layer, APIs, async behavior, resilience, observability, security, deployment, and rejected alternatives.
- When the user asks to design a database, start from workload and top queries. Default to Postgres unless the workload requires NoSQL. Cover schema, indexes, transactions, consistency, replication, sharding, schema evolution, and operations.
- When the user asks to review architecture, inspect only available evidence. Classify findings as pass, risk, violation, or unknown. Sort risks by severity and propose executable fitness functions.
- When the user asks for a diagram, default to Mermaid unless they request DBML or Excalidraw JSON. Keep diagrams small, label edges, group related components, and validate syntax before returning.

## System Design Skeleton

Use this shape for system design requests:

1. Requirements: functional, non-functional, constraints, assumptions.
2. Capacity estimates: QPS, storage, bandwidth, hot working set.
3. High-level architecture: components plus Mermaid sketch.
4. Data model: store choice, sharding key, replication, cache.
5. API: endpoints, RPCs, events, or sockets.
6. Async and real-time behavior.
7. Resilience and failure modes.
8. Observability: SLOs, SLIs, logs, metrics, traces.
9. Security: authn, authz, secrets, TLS, encryption.
10. Deployment and rollout.
11. Trade-offs and alternatives rejected.

## Database Design Skeleton

Use this shape for database requests:

1. Workload: read/write ratio, top queries, volume, transactional boundaries, consistency.
2. Store choice: engine and concrete justification.
3. Schema: tables or collections, constraints, keys, indexes.
4. Transactions and consistency: isolation per operation.
5. Scale strategy: replication, sharding, hotspots, cache.
6. Schema evolution: expand-contract, backfill, rollback.
7. Operations: backup, PITR, RPO/RTO, restore drills.
8. Trade-offs and alternatives considered.

## Review Stance

- Be direct and evidence-based.
- Do not invent findings that are not supported by files, docs, or pasted text.
- Treat missing information as unknown, not as a violation.
- Focus on issues that fail in production: scale, correctness, reliability, security, compliance, and operability.
- Put critical and high-severity findings first.

## Practical Default

Choose the simplest design that satisfies current and next-year non-functional requirements. Default to a modular monolith and Postgres until team boundaries, scale, workload shape, or availability requirements justify more distributed machinery.
