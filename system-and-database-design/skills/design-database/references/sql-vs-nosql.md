# SQL vs NoSQL

_Source: Designing Data-Intensive Applications (DDIA), Chapter 2 — Data Models and Query Languages._

## Concepts

- **Relational model** — tables, rows, joins, declarative queries (SQL). Decades of optimization; rich constraints; transactional by default.
- **Document model** — JSON-like, nested, self-contained per document (MongoDB, CouchDB). Schema-on-read; great for tree-shaped data; joins are weak.
- **Key-value** — the simplest (Redis, DynamoDB KV mode, Memcached). O(1) access; no query language.
- **Wide-column / column-family** — Cassandra, HBase. Sparse rows; good for time-series, IoT; eventual consistency default.
- **Graph model** — Neo4j, Neptune. Vertices + edges + Cypher/Gremlin; excels at traversal.
- **Time-series** — TimescaleDB, InfluxDB, Prometheus. Range partitioning by time; compression; retention.
- **Search** — Elasticsearch, OpenSearch. Inverted indexes; not a system of record.
- **Object-relational impedance mismatch** — why developers love documents and DBAs love normalized tables; one fact, one place.

## Quick decision

Default to **Postgres**. It covers 80% of workloads: relational + JSONB + full-text + geospatial + time-series extensions + vector (pgvector).

Pick NoSQL only when you have a specific reason:

| Need | Pick |
|---|---|
| Write rate > 100k/s, acceptable eventual consistency | Cassandra / Scylla |
| Global low-latency reads, schema flexibility | DynamoDB / Cosmos |
| Fast cache, ephemeral data | Redis |
| Nested document model, mobile sync | MongoDB / CouchDB |
| Graph traversals (social, fraud, knowledge graph) | Neo4j |
| High-ingest metrics | Prometheus / Influx |
| Full-text / fuzzy / faceted search | Elasticsearch (beside system of record) |
| Vector similarity / RAG | pgvector, Pinecone, Weaviate |

## See also

- `../../design-principles/references/trade-off-catalog.md` — entry 8 (SQL vs NoSQL)
- `../../design-system/references/ml-ai-serving.md` — vector DB trade-offs
