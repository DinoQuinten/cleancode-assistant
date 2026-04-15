# Schema Evolution

_Source: Designing Data-Intensive Applications (DDIA), Chapter 4 — Encoding and Evolution._

## Concepts

- **Backward vs forward compatibility** — old code reads new data vs new code reads old data. Both matter for rolling deploys.
- **Encoding formats** — JSON, XML (readable but lossy); Protocol Buffers, Thrift, Avro (schema-ed, compact, evolvable).
- **Schema registries** — Confluent Schema Registry pattern; enforce compatibility rules per topic.
- **Database schema migrations** — add column nullable → backfill → make NOT NULL; never drop in one deploy.
- **Zero-downtime migrations** — expand-contract: write to old + new, read from new, then drop old.
- **Online DDL tools** — `pt-online-schema-change`, `gh-ost`, Postgres `ALTER ... ADD COLUMN` (metadata-only in PG 11+).
- **Data format evolution across services** — services deployed independently; both old and new formats in flight simultaneously.
- **Archaeology of real deploys** — dual-writing, shadow reads, feature flags to gate reads from the new field.

## Zero-downtime migration pattern 

1. **Add** new column / table — nullable, no default (fast).
2. **Dual-write** — app writes old AND new fields. Deploy.
3. **Backfill** — batch job fills new column for old rows.
4. **Dual-read** — app reads new, compares to old, logs divergence. Deploy.
5. **Switch** — app reads only new. Deploy.
6. **Stop dual-write** — app writes only new. Deploy.
7. **Drop old** — remove old column / table. Deploy.

Each step is a deploy. Never combine. Budget weeks for a real migration.

## See also

- `../../review-architecture/references/anti-patterns.md` — big-bang migration anti-pattern
- `../../design-system/references/deployment.md` — blue/green + feature flags that gate migrations
