# Resilience Patterns

Authoritative sources: Michael Nygard "Release It!", Hystrix / resilience4j docs, Google SRE book ch. 22 "Addressing Cascading Failures", Envoy outlier detection docs.

## The hierarchy of defenses

Order matters. Each line of defense protects the one behind it.

1. **Timeout** — every remote call MUST have one; unbounded waits cascade
2. **Retry (with budget)** — retry transient failures, not permanent ones
3. **Backoff + jitter** — never retry tight-loop; always add jitter
4. **Circuit breaker** — stop calling a failing dependency; let it recover
5. **Bulkhead** — isolate resource pools so one dep's slowness doesn't exhaust all threads
6. **Fallback** — degrade gracefully when the dep is gone
7. **Load shedding** — drop excess requests rather than collapse
8. **Idempotency** — make retries safe

## Timeouts

**Every. Remote. Call.** Default TCP timeouts are minutes; unacceptable.

- **Connect timeout**: 1-3 s
- **Read timeout**: < your SLO (if your SLO is 500 ms p99, downstream read timeout must be < 500 ms minus your own processing)
- **Propagate deadlines** — child call's timeout = parent_deadline - elapsed - buffer. gRPC does this automatically.

Hierarchy: outermost ingress has the loosest; each hop tighter.

## Retries

Safe to retry when:
- Request is idempotent (GET, PUT, DELETE, or POST with an `Idempotency-Key`)
- Failure is transient (network error, 502/503/504, specific 5xx with "retryable" semantics)

**Never retry**: 400-series except 408/429; non-idempotent mutations without an idempotency key.

### Budget

A **retry budget** caps retries globally (e.g., "retries ≤ 10% of successful requests in last 60s"). Prevents retry storms when the dep is down. Envoy and Finagle support this natively.

### Backoff + jitter

Exponential: `delay = min(cap, base * 2^attempt)`. Always add jitter: `delay = random(0, exp_delay)` ("full jitter" per AWS Arch Blog — beats equal jitter in simulations).

## Circuit breaker

States: **Closed** (normal) → **Open** (failing, trip threshold reached) → **Half-open** (probe a single request) → back to Closed on success.

Thresholds (starting points; tune on data):
- Open when failure rate > 50% over a window of 20+ requests
- Stay open for 30 s
- Half-open probes 1 request

Per-dependency, not global. A single global breaker is useless.

## Bulkhead

Isolate thread pools / connection pools per downstream. If Dep A is slow, it doesn't drain the pool used for Dep B.

- **Thread-pool bulkhead** — classic Hystrix approach
- **Semaphore bulkhead** — lighter; caps in-flight concurrency per dep
- **Container-level** — in k8s, one service per pod, resource limits per pod

## Fallbacks

For every critical read path, ask: "What if this returns nothing?"

Options (in order of preference):
1. **Stale cache** — serve the last known-good value
2. **Default value** — if it's a non-essential feature, return empty/default
3. **Static degrade** — "Reviews unavailable" instead of crashing the product page
4. **Fail fast** — if no safe degrade, return 503 quickly so upstream can degrade

Fallbacks have costs: stale data is wrong data. Make sure the downstream knows.

## Idempotency

Retries are pointless (or dangerous) without idempotency. Two ways:

1. **Naturally idempotent ops** — PUT, DELETE on a specific resource; set operations ("set balance to 100")
2. **Idempotency key** — client sends `Idempotency-Key: <uuid>`; server stores the response for N hours; duplicate key returns cached response

Server-side: store `(key → response)` for at least the retry window (usually 24 h). Stripe's API is the reference implementation.

## Load shedding

When the system is overloaded, **drop requests at the edge** rather than let them queue and collapse.

- **Priority shedding** — shed low-priority (batch, nice-to-have) before high-priority (user-facing payment)
- **Concurrency limits** — reject when queue > N
- **CoDel / adaptive** — drop requests that have been queued > target latency (avoids bufferbloat)

Return 503 with `Retry-After`. Log sheds as a first-class signal.

## Testing resilience

You can't claim resilience you haven't tested.

- **Chaos engineering** — kill pods, inject latency, drop packets (Chaos Mesh, Gremlin)
- **Game days** — planned outages with the team watching
- **Load tests with faults** — not just max throughput; degraded-dep throughput

## Common failure modes

- **Retry amplification** — each layer retries 3x; 4 layers = 81x load on the bottom
- **Timeout inversion** — inner timeout > outer timeout; outer gives up while inner still works
- **Circuit breaker per-instance** — each app instance opens independently; collectively behaves worse than a central breaker
- **No idempotency + retries** — duplicate charges, duplicate emails, duplicate orders

## See also

- `load-balancing.md` — outlier detection is a server-side circuit breaker
- `observability.md` — you can't tune what you can't see
- `rate-limiting.md` — self-limiting as a client is a resilience pattern
