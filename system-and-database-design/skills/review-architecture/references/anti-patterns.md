# Anti-Patterns

Patterns that look like good ideas but cause disproportionate grief. Organized by system layer.

## Data layer anti-patterns

### Shared database across services

Two services write to the same DB schema. Now they're coupled through invisible schema contracts. A change in one can break the other. No single owner; changes are slow and risky.

**Fix**: one service owns the schema. Others get data via APIs or async events (CDC → their own store).

### Dual write

Application writes to DB and to another system (cache, search, queue) in two separate calls, hoping both succeed.

```
db.write(x)      # succeeds
cache.invalidate(x.key)   # fails — network blip
# cache now serves stale data; no recovery
```

**Fix**: outbox pattern — write business change + "event to emit" in the same DB transaction; separate poller/CDC propagates reliably.

### Distributed transaction (2PC) across microservices

Works in theory, pain in practice. Coordinator becomes a bottleneck; blocked participants hold locks; failure modes proliferate.

**Fix**: saga pattern (compensating transactions) or restructure to avoid the cross-service atomic need.

### Monotonic sharding key

Sharding on `auto_increment_id` or `created_at` puts all new writes on the last shard. Hotspot.

**Fix**: hash-based sharding; or composite key with a random prefix; or time-bucketed + modulo.

### Unbounded tables

`events`, `audit_log`, `sessions` growing forever with no archival or TTL. One day, a migration takes 8 hours; queries time out.

**Fix**: time-based partitioning + archival to cheaper storage; TTL for truly ephemeral data.

### N+1 queries

One query to list items, then one query per item to load a detail. 100 items = 101 queries.

**Fix**: eager loading (JOIN or batched IN query); DataLoader for GraphQL.

### Big ball of null

Nullable everywhere because "we might need it later." Queries become minefields. Indexes degrade.

**Fix**: NOT NULL by default; explicit nullables with documented semantics; separate tables for optional relationships.

## Service layer anti-patterns

### Distributed monolith

Microservices that MUST deploy together to avoid breakage. You pay all the ops cost of microservices with none of the independence.

**Fix**: contract tests; versioning discipline; actually bound contexts before splitting.

### Chatty API

Rendering a page requires 50 inter-service calls. Tail latency dominated by slowest.

**Fix**: BFF or composition layer; batched endpoints; materialized read models.

### God service

One service contains 80% of the logic. Other services are façades. Everyone blocks on god service deploys.

**Fix**: extract along bounded contexts; accept temporary double-home of data during migration.

### Retry storm

Dependency is slow → clients retry aggressively → dep gets more load → fully dies. A "retry" that's tight-loop is a DoS.

**Fix**: backoff + jitter; retry budget; circuit breaker.

### No timeouts

Default TCP/HTTP client timeouts are minutes. One slow dep hangs threads everywhere.

**Fix**: explicit timeouts on every call; propagate deadlines; timeout hierarchy (inner < outer).

### Thundering herd / cache stampede

Hot key expires; 1000 simultaneous misses hammer the DB.

**Fix**: singleflight / request coalescing; probabilistic early expiration; stale-while-revalidate.

## Deployment anti-patterns

### Snowflake servers

Hand-tweaked instances, impossible to recreate. "The box that knows things."

**Fix**: immutable infra; IaC (Terraform); containers or AMI bakes.

### Manual deploy steps

Runbook with "and then run `./migrate.sh` and then restart X." Humans forget; humans mistype.

**Fix**: automated pipeline; idempotent scripts; deploy === merged PR.

### Schema change + code change in same deploy

Code change requires new schema; if either fails mid-deploy, rollback is a nightmare.

**Fix**: expand/contract — two separate deploys; code is backward-compatible across the window.

### Big bang migration

"We'll rewrite it all and switch over in one weekend." The weekend becomes six months.

**Fix**: Strangler Fig; incremental route-switching behind the API gateway.

### Flag creep

50 feature flags, no owners, no expiry; code paths explode.

**Fix**: flag registry; expiry dates; CI-enforced cleanup.

## Operational anti-patterns

### No backpressure

Any tier that accepts unlimited work will eventually collapse. Kafka consumer reads faster than it processes → lag grows forever.

**Fix**: bounded queues; reject-when-full at edges; adaptive concurrency.

### Alerts only on symptoms the user already noticed

By the time the alert fires, customers are already writing in.

**Fix**: leading indicators — queue depth, error budget burn, saturation — alert before symptoms.

### Alerts that always need a restart

If the fix is always "restart X," automate the restart and stop paging a human.

### Logging every request's full body

Disk fills; compliance leaks; query costs.

**Fix**: sample; redact; separate audit logs from ops logs.

### Hugging the DB

Every feature adds a column; table has 200 columns; all queries `SELECT *`.

**Fix**: narrow SELECTs; split columns into purpose-specific tables; project smaller indexes.

## Organizational anti-patterns

### Architecture by committee

No single owner; decisions delayed; compromises with everyone's favorite tech.

### Resume-driven development

"Let's use Kubernetes for our 3-service app" because it's on the interview radar.

### Cargo cult

"BigCo uses X, so we need X." BigCo has problems your scale will never produce.

### No design docs for big changes

Six-month projects launched on a conversation. Problems surface only at integration.

**Fix**: RFC process; fitness functions as verifiable acceptance criteria.

## How to flag during review

Match the target's symptoms to the patterns above. For each hit:

- **Name the anti-pattern** explicitly — forces clarity
- **Cite the evidence** in the target
- **Name the specific failure mode** it will produce
- **Recommend the concrete fix** (link to the matching reference file)

## See also

- All the other checklists; anti-patterns are symptoms that checklists catch earlier
- `../../design-system/references/microservices-patterns.md` — most service-layer anti-patterns
