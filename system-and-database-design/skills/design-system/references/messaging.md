# Messaging: Queues and Streams

_Source: Designing Data-Intensive Applications (DDIA), Chapter 11 — Stream Processing._

## Concepts (DDIA ch. 11 subset)

- **Messaging vs log-based streams** — transient delivery vs durable, replayable event log.
- **Consumer patterns** — load balancing (competing consumers) vs fan-out (pub/sub).
- **Partitioned logs** — Kafka / Kinesis / Pulsar model; ordering within partition only.
- **Consumer offsets** — explicit commit; at-least-once by default; careful for exactly-once.
- **Stream processing use cases** — event sourcing, CEP, materialized views, streaming joins.
- **Time in streams** — event time vs processing time; windowing; watermarks.
- **Fault tolerance** — microbatching vs checkpointing; rebalance on consumer group change.

## Queue vs stream decision

| Need | Pick |
|---|---|
| Task queue, one worker per job, ack-or-requeue | Queue (RabbitMQ, SQS, Redis Streams) |
| Event log, multiple consumers with independent positions, replayable | Stream (Kafka, Kinesis, Pulsar) |
| Simple notifications, one publisher → many subscribers, no durability | Pub/sub (Redis, NATS) |
| Scheduled / delayed messages | Queue with visibility delay (SQS, Rabbit delayed plugin) |

**Rule of thumb:** Kafka for "events other services will consume now or later." RabbitMQ/SQS for "work someone needs to do once."

## Delivery semantics

- **At-most-once** — fire and forget; messages can be lost. Almost never acceptable.
- **At-least-once** — the default; duplicates possible on retry. **Consumers must be idempotent.**
- **Exactly-once** — achievable in-platform for Kafka (transactional producer + read-committed consumer) but end-to-end exactly-once across external side effects is a myth. Use idempotency keys.

## Common anti-patterns

- **Using the DB as a queue** without FOR UPDATE SKIP LOCKED → lock contention storm.
- **Unbounded consumer lag** with no alerting → silent data loss on retention expiry.
- **No dead-letter queue** → poison messages block the whole consumer.
- **Schema drift** without a registry → consumers break on producer deploys.
- **Ordering assumptions** across partitions — Kafka orders within a partition only.

## See also

- `microservices-patterns.md` — saga, outbox, CQRS all rely on messaging
- `../../design-database/references/distributed-transactions.md` — outbox pattern in detail
- `../../design-principles/references/trade-off-catalog.md` — entries 6 (sync/async) and 13 (batch/stream)
