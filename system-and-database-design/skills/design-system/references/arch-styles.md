# Architecture Styles

_Source: Fundamentals of Software Architecture (Richards & Ford), Part II — Architecture Styles (chapters on layered, pipeline, microkernel, service-based, event-driven, space-based, orchestration-driven SOA, microservices)._

## Concepts

For each style: **topology, partitioning, quanta, trade-offs across fitness-function axes** (deployability, elasticity, evolutionary, fault tolerance, modularity, overall simplicity, overall cost, performance, reliability, scalability, testability).

- **Layered (n-tier)** — presentation / business / persistence / DB. Default corporate style. Simple. Poor isolation of change.
- **Pipeline** — sequence of filters on a stream. Unix shell, batch ETL.
- **Microkernel (plug-in)** — small core + plug-ins. IDEs, browsers, Eclipse.
- **Service-based** — a few large services over a shared DB. A pragmatic step between monolith and microservices.
- **Event-driven** — brokers + mediators; mediator (orchestration) vs broker (choreography) topologies.
- **Space-based** — replicated in-memory grid, processing units + messaging grid. High scale with bursty load.
- **Orchestration-driven SOA** — ESB era. Heavy, vendor-coupled. Mostly historical.
- **Microservices** — bounded contexts; own DB; deployed independently; high operational cost.
- **Modular monolith** — often the right answer; monolith deployment with strict module boundaries.

## Quick-pick cheat sheet 

| Starting point | Default to |
|---|---|
| New product, small team | Modular monolith |
| Tight latency budgets inside one process | Layered monolith |
| Several independent teams, uneven scale per domain | Microservices |
| Workflow across domains | Event-driven (orchestration) |
| Extreme elasticity + in-memory state | Space-based |
| Data pipeline | Pipeline / stream processing |

## See also

- `microservices-patterns.md` — gateway, BFF, service mesh, sidecar, saga
- `../../review-architecture/references/arch-fitness-functions.md` — how to measure whether an architecture is holding
- `../../design-principles/references/trade-off-catalog.md` — entry 5 (monolith vs microservices)
