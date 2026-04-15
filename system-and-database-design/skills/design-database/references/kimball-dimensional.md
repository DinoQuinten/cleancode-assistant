# Kimball Dimensional Modeling

_Source: The Data Warehouse Toolkit (Kimball & Ross), primarily Chapters 1–3, 5._

## Concepts

- **Dimensional modeling vs 3NF** — why analytical workloads denormalize into stars.
- **Fact tables** — measurements of business processes. Grain (one row per …) is the most important decision.
  - **Transaction fact** — one row per event (order line, click)
  - **Periodic snapshot** — one row per entity per period (daily account balance)
  - **Accumulating snapshot** — one row per tracked process, updated as milestones pass (order: placed → paid → shipped → delivered)
- **Dimension tables** — context of a measurement: who, what, where, when, how.
- **Star schema** — fact surrounded by dimensions; best performance, easiest to query.
- **Snowflake schema** — normalized dimensions; saves space, costs joins. Only where dim tables are massive.
- **Slowly Changing Dimensions (SCDs)**:
  - **Type 0** — retain original, never update
  - **Type 1** — overwrite (no history)
  - **Type 2** — add new row with effective dates (full history)
  - **Type 3** — add column for previous value (limited history)
  - **Type 4** — separate history table
  - **Type 6** — hybrid (1 + 2 + 3)
- **Conformed dimensions** — shared across multiple fact tables, enabling drill-across.
- **The enterprise bus matrix** — Kimball's planning artifact: rows = business processes, columns = dimensions.
- **Role-playing dimensions** — same dim table used multiple times (order_date, ship_date, delivery_date all → date_dim).
- **Junk dimensions** — combine low-cardinality flags into one dim.
- **Degenerate dimensions** — transaction IDs kept on the fact with no dim table.
- **Factless fact tables** — capture events with no additive measures (attendance, eligibility).

## Quick reference

| Artifact | Purpose |
|---|---|
| Fact | What was measured (quantity, amount, duration) |
| Dimension | Context for the measurement |
| Grain | Exactly what one row of a fact represents |
| SCD Type 2 | History-preserving dim changes |
| Conformed dim | Shared across facts; enables drill-across |
| Bus matrix | Planning grid for the whole warehouse |

## See also

- `../../design-system/references/data-engineering.md` — ETL/ELT, CDC, lakehouse — the pipe that feeds Kimball models
- `normalization.md` — the OLTP side; Kimball is the OLAP side
