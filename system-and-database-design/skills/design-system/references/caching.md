# Caching

Authoritative sources: DDIA ch. 1 (brief), Martin Kleppmann's talks, "Caching at Netflix" / EVCache papers, Varnish docs.

## Tiers (outermost → innermost)

1. **Client / browser** — HTTP cache headers (`Cache-Control`, `ETag`, `Last-Modified`). Free; stops requests entirely.
2. **CDN** (CloudFront, Fastly, Cloudflare) — global edge; ideal for static assets and cacheable API responses (public, short TTL).
3. **Reverse proxy** (Varnish, NGINX) — in front of your app; sheds read load from app servers.
4. **Application in-memory** (Caffeine in Java, `lru_cache` in Python, in-process LRU) — nanosecond access; dies with the process.
5. **Distributed cache** (Redis, Memcached) — shared across instances; millisecond access.
6. **Materialized view / read replica** — persisted, queryable cache in the database itself.

Caches are NOT free: every added layer is a consistency hazard and an ops surface.

## Patterns

### Cache-aside (lazy loading) — DEFAULT

```
read:
  x = cache.get(key)
  if x is None:
    x = db.query(key)
    cache.set(key, x, ttl=...)
  return x

write:
  db.write(key, value)
  cache.delete(key)         # invalidate, don't repopulate
```

- Pro: simple; only cache what's requested
- Con: first read after invalidation is slow (cache miss); thundering herd on hot keys

### Write-through

Writes go to cache AND DB synchronously. Keeps cache warm but increases write latency.

### Write-back / write-behind

Writes go to cache; DB written asynchronously. Fast writes; **risk of data loss** on crash. Almost never correct unless you have a durable queue between cache and DB.

### Read-through

Cache itself fetches from DB on miss. Pushes cache logic into the cache library. Common with DynamoDB Accelerator, Caffeine loaders.

### Refresh-ahead

Cache proactively refreshes entries before TTL expires (background). Good for hot, predictable keys; wasteful otherwise.

## Invalidation strategies

1. **TTL (time-to-live)** — simplest; tolerate staleness window
2. **Explicit invalidation** — on write, delete the key; fragile (easy to miss a write path)
3. **Event-driven** — CDC or pub/sub invalidates caches; most robust for complex keys
4. **Versioned keys** — include a version token in the key; bumping the version invalidates all old entries atomically (useful for user-scoped caches)

> "There are only two hard things in Computer Science: cache invalidation and naming things." — Phil Karlton

## Cache stampede / thundering herd

When a hot key expires and 1,000 requests simultaneously miss. Mitigations:

- **Probabilistic early expiration** — each request has a small random chance to refresh before TTL (XFetch algorithm)
- **Request coalescing / singleflight** — only the first miss recomputes; others wait for its result (Go's `singleflight`, Guava's `LoadingCache`)
- **Mutex on key** — lock per-key while one worker recomputes; others serve stale
- **Stale-while-revalidate** — serve stale for up to N seconds while async refresh runs

## Sizing

- **Working set estimate** = 80th-percentile hot keys × average value size
- **Hit ratio target** — below 90% for most caches is not worth the complexity; aim for 95%+ for front-door caches
- **Eviction policy** — LRU for recency-heavy access, LFU for frequency-heavy (Redis supports both; pick based on your key distribution)

## When NOT to cache

- **Write-heavy workloads** with low read:write ratio — cache churn outweighs hit rate
- **Fresh-data requirements** (price quotes, auctions, inventory) — use materialized views with CDC instead of TTL caches
- **Uncacheable responses** (per-user, unique every request) — add caching at a lower layer (query result caching, join caching)

## Failure modes to plan for

- **Cache down** — does the app serve from DB? Thundering herd protection? Circuit breaker to fail fast?
- **Cache returns stale on schema change** — versioned keys or flush on deploy
- **Cache poisoning** — never cache responses from unauthenticated code paths without careful key scoping

## See also

- `load-balancing.md` — CDN edges use consistent hashing for cache locality
- `rate-limiting.md` — rate limiters themselves need fast counters; usually Redis-backed
- `../design-database/references/indexing-tradeoffs.md` — covering indexes and materialized views are caches too
