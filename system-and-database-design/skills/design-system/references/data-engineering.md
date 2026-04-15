# Data Engineering

Authoritative sources: Martin Kleppmann "Designing Data-Intensive Applications" chs. 10-11, Ralph Kimball "The Data Warehouse Toolkit", dbt documentation, modern data stack writeups (Fivetran, Snowflake, Databricks).

## ETL vs ELT — what changed

**ETL** (classic): Extract → Transform → Load. Transforms happen in a specialized processing engine (Informatica, SSIS) before loading to the warehouse.

**ELT** (modern): Extract → Load → Transform. Raw data lands in the warehouse; transforms happen in SQL inside the warehouse.

ELT wins today because cloud warehouses (Snowflake, BigQuery, Redshift) decoupled storage from compute and made SQL-in-warehouse cheap and fast. dbt operationalizes it.

Use ELT unless you have a specific reason otherwise (PII that can't land raw, pre-aggregation for low-latency serving).

## The modern data stack

| Layer | Examples |
|---|---|
| Sources | Postgres, Kafka, SaaS APIs, event logs |
| Ingestion | Fivetran, Airbyte, Kafka Connect, Debezium (CDC) |
| Storage | Cloud warehouse (Snowflake, BigQuery, Redshift) OR lakehouse (Databricks, Iceberg on S3) |
| Transformation | dbt, Dataform, Spark |
| Orchestration | Airflow, Dagster, Prefect |
| Serving | BI tools (Looker, Tableau), reverse ETL (Hightouch, Census), APIs, ML features |

## CDC (Change Data Capture)

Replicates changes from a source DB to a destination in near real-time.

- **Log-based CDC** (preferred): read the DB's write-ahead log (Postgres logical replication, MySQL binlog, SQL Server CT). Debezium is the reference implementation.
- **Query-based CDC**: poll `WHERE updated_at > last_seen`; requires a reliable `updated_at`; misses deletes unless soft-deleted.
- **Trigger-based CDC**: DB triggers write to a shadow table. High overhead on the source DB.

Use CDC to:
- Replicate OLTP → OLAP without batch ETL latency
- Power search indexes (Postgres → Elasticsearch)
- Feed caches and materialized views
- Event sourcing adapter for legacy systems

## Batch vs stream

| Dimension | Batch (nightly, hourly) | Streaming (seconds or less) |
|---|---|---|
| Complexity | Low | High |
| Latency | High | Low |
| Cost | Low (bulk ops) | Higher (always-on compute) |
| Debugging | Easy (reproduce with data) | Hard (temporal state) |
| Exactly-once | Easy (idempotent batch) | Hard (needs checkpointing) |

Default: batch. Add streaming only where you can name the business value that's worth the complexity.

## Lakehouse architecture

Storage layer (S3/GCS/ADLS) + open table format (Apache Iceberg, Delta Lake, Hudi) + query engines (Spark, Trino, Snowflake).

- **Pro**: one copy of data; multiple engines (SQL, ML, streaming)
- **Pro**: schema evolution, ACID transactions on object storage
- **Pro**: cheap, scalable storage
- **Con**: more moving parts than a warehouse
- **Con**: governance is harder (many engines touching same tables)

Iceberg is winning as the standard format in 2026.

## Medallion architecture (bronze/silver/gold)

Three-layer data model inside the warehouse/lakehouse:

- **Bronze** — raw, schema-on-read, append-only landing zone
- **Silver** — cleaned, typed, de-duped, conformed entities (one fact per row)
- **Gold** — business-facing marts, aggregated, modeled for consumption (dimensional or wide flat)

Transform bronze → silver → gold with dbt or Spark. Silver is the "source of truth" for most analysis.

## Data contracts

Formal agreement between producer and consumer of data. Breaks if producer changes schema without notice.

- **Schema** (required fields, types)
- **SLA** (freshness, availability)
- **Ownership** (who fixes breakage)
- **Versioning** (how producer evolves without breaking consumers)
- Enforce via CI checks (dbt contract tests, schema registry, Great Expectations)

Without contracts, pipeline breakage is a 3am ops problem masquerading as a data problem.

## Data quality

- **Freshness** — alert when a table's `max(updated_at)` is too old
- **Volume** — alert on row-count drops > 30% day-over-day
- **Schema drift** — alert on unexpected column changes
- **Null ratio, uniqueness, range** — assert on critical columns (Great Expectations, dbt tests, Soda)
- **Referential integrity** — downstream FKs match upstream PKs

Treat data tests as production code. CI runs them on sample data; prod alerts on fresh data.

## Streaming frameworks

| Tool | Model | Use when |
|---|---|---|
| **Kafka Streams** | JVM, library-style, partitioned | Inside Java/Kotlin services; tight Kafka integration |
| **Flink** | Stateful, exactly-once, windowing | Complex event processing, large state, strict semantics |
| **Spark Structured Streaming** | Micro-batch, SQL-friendly | Batch + stream unified on same code |
| **Materialize, RisingWave** | SQL → streaming materialized views | Analyst-friendly; fresh dashboards |
| **ksqlDB** | SQL on Kafka | Quick streaming joins without Flink |

## Governance

- **Column-level lineage** (dbt, OpenLineage, Marquez) — know where data came from
- **PII tagging** — column-level metadata; drives masking rules
- **Access control** — row-level and column-level; warehouse-native policies (Snowflake row access, BigQuery column policies)
- **Retention** — drop old data automatically; aligns with GDPR obligations

## See also

- `../design-database/references/kimball-dimensional.md` — dimensional modeling for the gold layer
- `../design-database/references/replication.md` — CDC is a specific flavor of replication
- `messaging.md` — Kafka for ingest + stream
- `ml-ai-serving.md` — feature stores overlap with data engineering
