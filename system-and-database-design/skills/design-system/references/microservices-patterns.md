# Microservices Patterns

Authoritative sources: Sam Newman "Building Microservices" 2nd ed., Chris Richardson "Microservices Patterns", Netflix/Uber engineering blogs, Istio/Linkerd docs.

## First: do you need microservices at all?

Default to **modular monolith**. Migrate to microservices when at least two apply:

- Team topology — independent teams blocked by shared deploys
- Scaling asymmetry — one part needs 10x infra of the rest
- Tech heterogeneity — different runtimes genuinely needed
- Compliance isolation — one subset touches PCI/HIPAA

If none apply, microservices will cost you more than they give you.

## Core patterns

### API Gateway

Single entry point for clients. Handles:
- AuthN (validates tokens)
- Rate limiting
- Routing to internal services
- Response aggregation (optional)
- Protocol translation (HTTPS/JSON ↔ gRPC)

Products: Kong, Envoy, AWS API Gateway, Apigee, Tyk.

**Don't** put business logic in the gateway. It's a router, not a service.

### Backend-for-Frontend (BFF)

Per-client-type gateway. Web BFF, mobile BFF, partner BFF — each tailored to its client's needs.

- **Why**: different clients have different data shapes, caching, auth flows
- **Cost**: one more service per client type
- Fits GraphQL naturally (BFF = GraphQL layer)

### Service Mesh

Sidecar proxy per service handles:
- mTLS between services
- Load balancing
- Retries, timeouts, circuit breaking
- Observability (metrics, traces)
- Traffic policies (canary routing)

Products: Istio, Linkerd, Consul Connect, Cilium (eBPF-based, no sidecar).

**Cost**: +10-30% latency, +ops complexity. Worth it only once you have 10+ services.

### Sidecar

General pattern: attach a helper process to the main app. Mesh proxies are one case; log shippers, secret rotators, metrics agents are others.

### Saga

Distributed transaction without 2PC. Break a long operation into a sequence of local transactions, each with a compensating action on failure.

Two styles:
- **Orchestration** — central saga coordinator invokes each step and handles rollback
- **Choreography** — services react to events; no central coordinator; emergent workflow

Choreography scales organizationally; orchestration is easier to reason about. Start with orchestration.

### Outbox pattern

Atomic "update DB + emit event" without 2PC:

1. In the same DB transaction, write business change AND insert a row into an `outbox` table
2. Separate poller/CDC reads outbox, publishes to message bus, marks row sent

Prevents dual-write problem (DB committed but event lost, or event sent but DB rolled back).

### CQRS (Command Query Responsibility Segregation)

Separate write model from read model:
- **Write side** — normalized, enforces invariants (e.g., Postgres)
- **Read side** — denormalized, optimized per query (e.g., Elasticsearch, materialized views)
- Connect via events (write side publishes; read side projects)

Not every service needs CQRS. Use when read and write models diverge significantly.

### Event Sourcing

Store the sequence of state-change events, not just current state. Current state = fold over events.

- **Pro**: perfect audit log; can rebuild state or derive new views; temporal queries ("what was the balance last month?")
- **Con**: schema evolution is hard (events are immutable, forever); snapshotting for performance; eventual consistency on reads

Use for domains where history is the domain (accounting, audit, versioned docs). Overkill for CRUD.

### Strangler Fig

Migrate legacy monolith to services by gradually routing specific functions to new services while the monolith keeps serving the rest. Eventually the monolith is gone ("strangled").

Key: route at the API gateway, not in code. Rollback = route back.

## Service-to-service communication

| Pattern | Style | Coupling | Use when |
|---|---|---|---|
| Synchronous REST/gRPC | request/response | tight | Immediate response needed |
| Async messages (queue) | fire-and-forget | loose | Work can happen later |
| Async events (pub/sub) | broadcast | loosest | Multiple consumers; future unknowns |
| Batch | scheduled | n/a | Not latency-sensitive |

Default: sync for user-facing request paths; async for everything else.

## Data ownership

**Each service owns its data.** No other service queries its DB directly. Period.

- Need data across services? API call or event-driven replication, not a DB join
- The "shared database" anti-pattern is the #1 reason microservices fail

## Testing

- **Unit** — fast; mock external deps
- **Contract** — Pact; verify each service honors the API contract
- **Integration** — spin up real deps (testcontainers); tests your service + DB/cache + queue
- **End-to-end** — sparingly; fragile; use for critical flows only

## Distributed tracing mandatory

Without `trace_id` propagation across services, you will not be able to debug prod. Enable OpenTelemetry from day one.

## Common mistakes

- Distributed monolith — services that must deploy together; you have all the cost of microservices and none of the benefits
- Chatty APIs — one user action = 50 service-to-service calls; batch endpoints instead
- Shared DB — see above
- Async-by-default for everything — debugging eventual consistency is expensive; use sync where simple
- No service ownership — someone must own each service; orphaned services rot fast

## See also

- `api-design.md` — internal vs external API discipline
- `messaging.md` — async communication patterns
- `resilience.md` — each service-to-service call needs timeouts, retries, breakers
