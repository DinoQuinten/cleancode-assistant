# Consensus

_Source: Designing Data-Intensive Applications (DDIA), Chapter 9 — Consistency and Consensus._

## Concepts

- **The problem** — getting a group of nodes to agree on a value (or order of values) in the presence of network faults and crashes.
- **FLP impossibility** — in an asynchronous model with even one faulty process, no deterministic consensus algorithm can guarantee termination. Real systems get around this via partial synchrony + timeouts.
- **Paxos** — the original (Lamport). Hard to implement correctly; most real systems use Multi-Paxos or a variant.
- **Raft** — designed for understandability. Leader election + log replication + safety. Used in etcd, Consul, CockroachDB, TiKV, many others.
- **Zab** — ZooKeeper's atomic broadcast. Similar guarantees to Raft.
- **Viewstamped replication** — another family; less common in industry.
- **Common primitives built on consensus**:
  - Atomic commit / distributed locks
  - Leader election
  - Membership / failure detection
  - Configuration / metadata store
  - Fencing tokens (monotonic IDs to prevent split-brain writes)
- **Quorums** — N replicas, W writes, R reads; W + R > N for strong consistency.
- **Byzantine fault tolerance** — when nodes can lie or be malicious (blockchains, high-assurance systems); much more expensive than crash-fault-tolerance.

## Practical guidance 

- **Don't roll your own consensus.** Use etcd / ZooKeeper / Consul / a managed service. Implementing Raft correctly is a multi-year effort.
- **Use consensus stores FOR coordination, not AS a primary data store.** They are slow for high-volume workloads.
- **Typical cluster size: 3 or 5 nodes.** 3 tolerates 1 failure, 5 tolerates 2. Larger quorums buy you almost nothing in fault tolerance and cost a lot in write latency.
- **Leader election is cheap, fencing is what matters.** After election, zombie leaders can still write; use monotonically increasing fencing tokens on every protected resource.

## See also

- `cap-pacelc.md` — consensus is how CP systems stay consistent
- `consistency-models.md` — linearizability requires consensus
- `../../design-database/references/distributed-transactions.md` — 2PC + saga patterns that sit above consensus
