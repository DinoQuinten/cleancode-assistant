# Load Balancing

Authoritative sources: HAProxy docs, NGINX documentation, Google SRE book ch. 19, Envoy docs.

## L4 vs L7

| Dimension | L4 (transport) | L7 (application) |
|---|---|---|
| Operates on | TCP/UDP connections | HTTP requests |
| Terminates TLS | No (passthrough) or yes | Usually yes |
| Routes on | IP:port | Path, header, cookie, method |
| Latency | ~0.1 ms added | ~1-5 ms added |
| Sticky sessions | Source-IP hash (crude) | Cookie-based (precise) |
| Observability | Connections, bytes | Requests, status codes, routes |
| Example products | AWS NLB, HAProxy (L4), IPVS | AWS ALB, NGINX, Envoy, Traefik |

Rule: use L7 unless you need raw throughput (>100 Gbps) or are handling non-HTTP protocols.

## Algorithms

1. **Round-robin** — simplest; each backend gets the next request in rotation. Fine when backends are identical and requests are uniform.
2. **Weighted round-robin** — assigns weights for heterogeneous backend capacity (e.g., c5.large : c5.xlarge = 1 : 2).
3. **Least connections** — routes to the backend with the fewest open connections. Good for long-lived connections or uneven request costs.
4. **Least response time** — hybrid of least-conn + latency. Picks the backend expected to respond fastest.
5. **Consistent hashing** — routes the same key (session ID, user ID, cache key) to the same backend (or its replicas). Essential for:
   - Sticky sessions (though use cookies if possible)
   - Cache locality (L7 cache layers, edge caches)
   - Sharded state (sticky-at-protocol-level)
6. **Random (power of two choices)** — pick 2 backends at random, send to the one with fewer connections. Near-optimal, cheap; what Envoy defaults to.

## Health checks

A load balancer is only as good as its health checks. Design them to be:

- **Independent of downstream deps** — don't fail health when a dep is slow; fail the dep's health instead. Else cascading failures.
- **Fast** — 1-5 s interval, 1-2 s timeout, 3 consecutive failures before ejection.
- **Realistic** — hit a `/healthz` endpoint that actually exercises critical code paths; a literal `return 200` is lying.
- **Graceful shutdown** — when a backend is draining, the LB sees it failing health, stops routing, lets in-flight requests finish.

Use **deep health** (checks database, disk) for startup/readiness only. Use **shallow health** for ongoing liveness.

## Sticky sessions

Avoid if possible — they break horizontal scaling and complicate deploys. Use only when the backend holds in-memory state that can't be externalized. Externalize session state to Redis instead.

If you must: cookie-based L7 stickiness (not source-IP, which fails behind NAT/proxies).

## Global load balancing (multi-region)

- **DNS-based** (AWS Route53, Cloudflare) — client resolves a geo-aware CNAME; cheap but slow to react (TTL-bound)
- **Anycast** — same IP announced from multiple regions; BGP routes client to nearest; fastest failover but complex
- **Active/active with app-level routing** — each region serves fully; app-level replication; best for read-heavy workloads

Failover decision: health-check-driven, with a minimum failover time to avoid flapping.

## Common failure modes

- **Retry storms** — client retries amplify traffic to a struggling backend; use exponential backoff + jitter + budget
- **Bad node accepting all traffic** — least-connections can pile onto a slow-but-alive backend; add outlier detection (Envoy calls this "outlier ejection")
- **Sticky session traps** — one user's session pinned to a dying backend; implement eviction
- **Slow path starvation** — long-running requests starve short ones; use separate pools or concurrency limits per route

## See also

- `rate-limiting.md` — often co-located at the LB layer
- `resilience.md` — circuit breakers, outlier ejection, timeout hierarchies
- `deployment.md` — blue/green and canary routing happens at the LB
