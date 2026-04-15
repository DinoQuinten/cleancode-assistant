# Rate Limiting

Authoritative sources: Stripe engineering blog ("Scaling your API with rate limiters"), GitHub API docs, Cloudflare rate limiting docs.

## Purpose

- **Protect** the system from overload (self-imposed DoS via retry storms; external abuse)
- **Fair-share** constrained resources across tenants
- **Enforce commercial tiers** (free vs paid quotas)
- **Reduce blast radius** of a single bad actor

Rate limiting is a safety mechanism, not a pricing mechanism. Use it alongside authN so you know WHO to limit.

## Algorithms

### Token bucket

Conceptually: a bucket holds up to `B` tokens. Each request consumes `1` (or more). Tokens refill at rate `R/s`. Request allowed if tokens available, denied if not.

- **Allows bursts up to `B`**, sustained rate `R`
- **Simple**, memory-efficient (one counter + timestamp per key)
- **Standard for API gateways** (Kong, Apigee, AWS API Gateway all use this)

Pseudocode:
```
def allow(key):
    now = monotonic()
    tokens, last = state[key]
    elapsed = now - last
    tokens = min(B, tokens + elapsed * R)
    if tokens >= 1:
        state[key] = (tokens - 1, now)
        return True
    return False
```

### Leaky bucket

Requests enter a fixed-size queue; a worker drains it at rate `R`. Overflow = drop. Smooths traffic; used for scheduler/egress shaping more than for API gateways.

### Fixed window

Count requests per calendar minute/hour. Easy but has the "double-burst at window edge" flaw (a client can send 2N requests in 1 second spanning a minute boundary).

### Sliding window log

Store every request timestamp; allow if fewer than N timestamps in the last W seconds. Exact but O(N) memory. Use for low-volume tiers (per-user admin API).

### Sliding window counter (approximation)

Blend the current window count with a weighted prior window. Close to fixed window in memory, close to sliding log in accuracy. **This is usually the right choice** for high-volume API gateways that need near-exact limits.

## Distributed rate limiting

Single-instance counters break when the LB routes a user's requests to different app servers. Options:

1. **Centralized store** (Redis with Lua scripts for atomicity) — canonical approach; ~0.5 ms per check
2. **Probabilistic / gossip** (DynamoDB Streams, CRDTs) — eventually consistent; tolerates some overshoot
3. **Sticky routing + local counters** — route a user always to the same app; simple but fragile (session stickiness)
4. **Envoy global rate limit service** — gRPC service with Redis backend; battle-tested at scale

For Redis, use a Lua script so increment + compare is atomic:
```lua
local tokens = tonumber(redis.call('GET', KEYS[1]) or ARGV[2])
if tokens < 1 then return 0 end
redis.call('SET', KEYS[1], tokens - 1, 'EX', ARGV[3])
return 1
```

## Dimensions to limit on

- **Per IP** — crude; breaks NAT; use only as last-ditch abuse defense
- **Per API key / user ID** — primary for authenticated APIs
- **Per tenant** — SaaS fair-sharing
- **Per endpoint / per method** — expensive endpoints deserve tighter limits
- **Per combination** — `(user, endpoint)` is common

Layer multiple limits. A user can hit the per-user limit OR the per-endpoint limit, whichever is lower.

## Response behavior

- **HTTP 429 Too Many Requests**
- **`Retry-After` header** with seconds or HTTP-date (RFC 6585)
- **`RateLimit-Limit`**, **`RateLimit-Remaining`**, **`RateLimit-Reset`** headers (draft standard)
- **Hard-fail** for hostile traffic (WAF integration); **soft-fail** (queue, delay) for paying customers near their limit
- **Log** every 429 with the key and reason; abuse patterns hide in this data

## Integration points

- **Edge / WAF** — block floods before they reach your app (Cloudflare, AWS WAF)
- **API gateway** — per-tenant quotas
- **Service mesh / sidecar** — service-to-service limits (Envoy local or global)
- **Application** — business-logic limits (e.g., "max 10 password resets per hour per email")

Use all four, with progressively tighter limits inward.

## Common mistakes

- Limiting only on IP in a world of CGNAT / mobile carriers → legitimate users DoS themselves
- Returning 200 instead of 429 → clients retry forever
- No jitter in `Retry-After` → synchronized retries cause a thundering herd when the window resets
- Treating rate limit as a hard security control → it's not; a botnet rotates IPs and keys

## See also

- `load-balancing.md` — rate limiting often lives here
- `resilience.md` — from the client side, use a token bucket locally too to avoid getting 429'd
- `security-checklist.md` — rate limiting is one of OWASP's API security controls
