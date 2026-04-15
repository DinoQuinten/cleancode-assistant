# Scalability Checklist

Use this list to find scaling gaps in an existing architecture. Each item: mark ✅ pass, ⚠️ risk, 🔴 violation, or ❓ unknown.

## Stateless services
- [ ] Every web/API tier process can be killed or added without session loss
- [ ] Session state is externalized (Redis, JWT, sticky only when unavoidable)
- [ ] No in-process locks that span requests
- [ ] No in-process caches serving as source of truth

## Horizontal scale at every tier
- [ ] Load balancer in front of every multi-instance tier
- [ ] Auto-scaling rules based on meaningful signals (CPU/RPS/queue depth), not just CPU
- [ ] Database has read replicas OR a plan for when reads saturate the primary
- [ ] Async workers pool can scale independently of API tier

## Bottleneck analysis
- [ ] Every single-point-of-failure identified and justified
- [ ] Every "singleton service" has a documented scale ceiling
- [ ] Database connection pool sized for peak concurrency (and monitored)
- [ ] File-system use explicit (local ephemeral, NFS, object storage) — and none of them is "local disk as source of truth"

## Caching
- [ ] Read-heavy endpoints cache appropriately (CDN, reverse proxy, app, DB)
- [ ] Cache invalidation strategy documented and tested
- [ ] Cache stampede protections in place (singleflight, early expiration, stale-while-revalidate)
- [ ] Hit ratios measured; low hit ratios investigated

## Async & queueing
- [ ] Slow/expensive work runs async, not inline in request paths
- [ ] Queue depth and consumer lag alerted
- [ ] Dead-letter queues for poison messages
- [ ] Back-pressure mechanism; work never enqueues forever without limit

## Database scale
- [ ] Partition / shard key chosen to avoid hotspots (not monotonic timestamps!)
- [ ] Read:write ratio understood; scale strategy matches (replicas for reads, sharding for writes)
- [ ] Slow query log monitored; p99 query times tracked
- [ ] Connection pooling at application tier (PgBouncer etc.)
- [ ] Plan for growth: next 1 year's volume fits comfortably in current infra OR there's a documented plan

## Data model shape
- [ ] Unbounded "grow forever" tables have archival/TTL strategy
- [ ] Indexes cover hot queries; no sequential scans on large tables in hot paths
- [ ] No "N+1" queries in request paths (profiled)

## Network
- [ ] No inter-region hops on request-critical paths unless necessary
- [ ] Serialization format appropriate (JSON for compat, Protobuf for perf)
- [ ] Request payloads bounded (max body size enforced)
- [ ] Response pagination for collections

## Failure isolation
- [ ] Blast radius limited — one tenant / one service cannot exhaust shared resources
- [ ] Bulkheads on thread/connection pools per downstream dep
- [ ] Timeouts and retries prevent cascading failures
- [ ] Multi-AZ deployment (at minimum)

## Observability for scale
- [ ] SLO targets documented for key user journeys
- [ ] Capacity headroom tracked (CPU, memory, IOPS, connections, queue) vs target (<70% under peak)
- [ ] Load test results recent and representative
- [ ] Error budget burn rate alerted

## Operational
- [ ] Deployments can handle 2x current traffic without manual intervention
- [ ] Runbook for scaling up fast (add capacity in <10 min)
- [ ] Rollback plan if scaling change misbehaves
- [ ] Cost forecast aligned with scale expectations

## Red flags to look for

- A monolithic DB table touched by every service
- "We scale by buying bigger instances" and nothing else
- No load testing in CI or staging
- Singleton processes labeled "the queue," "the scheduler," "the coordinator"
- Multiple services writing to the same table
- Manual interventions required for deploys or scale events

## See also

- `../../design-system/references/capacity-estimation.md` — numbers to validate claims
- `../../design-system/references/load-balancing.md`
- `../../design-system/references/caching.md`
