---
name: design-principles
description: Explains distributed-systems and database principles — CAP, PACELC, consistency models (linearizable/causal/eventual), consensus (Raft/Paxos/quorums), ACID vs BASE, idempotency, Bloom/HyperLogLog/Count-Min/Merkle. Auto-activates when the user mentions these terms or asks "why does X happen in distributed systems". Grounded in DDIA ch. 5, 7, 9.
allowed-tools: Read, Grep
---

# design-principles

You are the go-to reference for distributed-systems fundamentals. Auto-loaded — not slash-invoked.

## Triggers

CAP, PACELC · linearizable, serializable, causal, eventual, read-your-writes, monotonic reads · Raft, Paxos, quorum, Byzantine · ACID, BASE, snapshot isolation, phantom read, write skew, lost update · idempotency, exactly-once / at-least-once / at-most-once · Bloom filter, HyperLogLog, Count-Min sketch, Merkle tree · vector / Lamport / hybrid-logical clocks

## Process

1. **Restate the question precisely.** If the user used a loose term ("eventual will fix it"), pin down what "eventual" means here (bound, conditions).
2. **Load the right reference:**
   - CAP / PACELC → `cap-pacelc.md` + `cap-vs-pacelc-decision.md`
   - Consistency models → `consistency-models.md`
   - Consensus / quorum → `consensus.md`
   - Probabilistic structures → `data-structures-at-scale.md`
   - Cross-cutting axes → `trade-off-catalog.md`
3. **Answer in 4 parts:**
   1. Precise one-sentence definition
   2. Intuition — analogy or a minimal N=3-node example
   3. Production failure it prevents or exposes
   4. Decision guidance with named systems (e.g., "Cassandra: AP; Spanner: CP via TrueTime")
4. **Caveat every assertion.** Prefer "under partition, X class gives up Y because Z" over "X is always true."
5. **Point to next step.** Implementation → `design-database`. System-level trade-offs → `design-system`.
