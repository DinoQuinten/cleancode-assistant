# Consistency Models

_Source: Designing Data-Intensive Applications (DDIA), Chapter 9 — Consistency and Consensus._

## Concepts

The consistency spectrum — from strongest to weakest, each one buys something and costs something.

- **Linearizability (external consistency)** — operations appear to take effect instantaneously, in a total order consistent with real time. Strongest. Used for locks, uniqueness, compare-and-swap. Expensive in latency + availability.
- **Sequential consistency** — total order across all operations, but not tied to real time. Rare in practice.
- **Causal consistency** — operations causally related to each other are seen in that order; concurrent operations may be reordered. Practical upper bound for many distributed systems.
- **Consistent prefix** — reads never see out-of-order writes; no time travel.
- **Bounded staleness** — reads may be stale, but by a bounded amount (N versions or T milliseconds).
- **Session guarantees**:
  - **Read-your-writes** — after you write X, you read X (or later)
  - **Monotonic reads** — you never read older than what you already saw
  - **Writes-follow-reads** — your writes happen-after writes you read
- **Eventual consistency** — given no new writes, all replicas converge. No bound on "eventually."

## Picking a level 

Pick the **weakest** model that your users and invariants tolerate. Each step up costs latency or availability.

| Scenario | Model that usually suffices |
|---|---|
| User profile display | Session (read-your-writes) |
| Social feed | Eventual or causal |
| Shopping cart | Session + causal |
| Account balance (display) | Bounded staleness (≤ seconds) |
| Funds transfer / debit | Linearizable (or single-shard serializable) |
| Uniqueness (username) | Linearizable |
| Distributed lock | Linearizable (use consensus store) |

## See also

- `cap-pacelc.md` — the theoretical framing
- `cap-vs-pacelc-decision.md` — the per-use-case decision guide
- `consensus.md` — how to implement linearizable ops
