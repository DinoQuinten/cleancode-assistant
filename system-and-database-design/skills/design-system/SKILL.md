---
name: design-system
description: Produces a system design doc for a given requirement. Use when the user asks to "design a system", "architect a service", "design X at scale", or invokes /design-system. Grounded in DDIA and Fundamentals of Software Architecture.
argument-hint: "<requirement, e.g. 'URL shortener' or 'multi-tenant chat'>"
allowed-tools: Read, Write, Grep, Glob
---

# design-system

Produce a design doc a staff engineer would respect — opinionated, grounded, quantitative.

## Process

1. **Clarify requirements.** List functional, non-functional (QPS, latency, 9s, geo), and constraints. Mark guessed numbers as `ASSUMPTION:`. Do not pause to ask — iterate.
2. **Pick the architecture style.** Default bias: modular monolith. Split only with a reason. Load `references/arch-styles.md` for topologies.
3. **Capacity math.** Compute peak QPS (read/write), yearly storage, bandwidth, hot working set. Round to 2 sig figs. Refs: `latency-numbers.md`, `capacity-estimation.md`.
4. **Component graph.** Describe in words + a Mermaid sketch. Identify client → edge → app → data → async tiers.
5. **Data layer.** State primary store type, why it fits access patterns, sharding key, replication, cache. Delegate schema depth to the `design-database` skill.
6. **API surface.** Pick REST / GraphQL / gRPC / WebSocket (or a mix). Sketch 3–6 key endpoints with shapes.
7. **Async + real-time.** Specify queues/streams, delivery guarantees, WebSocket/SSE patterns if relevant.
8. **Resilience.** For every remote call: timeout, retry w/ backoff + idempotency key, circuit breaker, fallback, bulkhead.
9. **Observability.** Name SLOs, SLIs, logs/metrics/traces. RED for services, USE for infra.
10. **Security.** AuthN, AuthZ, secrets, TLS, data-at-rest encryption, OWASP angle if public.
11. **Deployment.** Runtime (containers/serverless/VM), release strategy (blue/green/canary/flags), multi-region.
12. **ML/AI features** (if any). Inline vs service, sync vs async inference, vector DB, feature store.
13. **Trade-offs.** Name rejected alternatives and the concrete reason.

## Reference lookup (load only what applies)

| Topic | File |
|---|---|
| Architecture style | `arch-styles.md` |
| Capacity / latency | `capacity-estimation.md`, `latency-numbers.md` |
| Caching | `caching.md` |
| Load balancing / rate limiting | `load-balancing.md`, `rate-limiting.md` |
| Queues / streams | `messaging.md` |
| APIs | `api-design.md` |
| Resilience | `resilience.md` |
| Observability | `observability.md` |
| Security | `security.md` |
| Deployment | `deployment.md` |
| Microservices patterns | `microservices-patterns.md` |
| Real-time / WebSocket / SSE | `real-time-systems.md` |
| ETL / CDC / lakehouse | `data-engineering.md` |
| ML / RAG / vector DB | `ml-ai-serving.md` |

Load at most 2–3 per question. Do not pre-load.

## Output skeleton

```markdown
# System Design: <name>

## 1. Requirements  (functional / non-functional / assumptions)
## 2. Capacity estimates  (numbers, not prose)
## 3. High-level architecture  (component list + Mermaid)
## 4. Data model  (store, sharding, replication, cache)
## 5. API  (endpoints or RPCs)
## 6. Async & real-time
## 7. Resilience & failure modes
## 8. Observability
## 9. Security
## 10. Deployment
## 11. Trade-offs
```

Offer to save to `./designs/<kebab-name>.md`. Offer to generate diagrams via `diagram`.
