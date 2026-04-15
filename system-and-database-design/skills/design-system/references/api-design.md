# API Design

Authoritative sources: "API Design Patterns" (JJ Geewax), Google AIP (aip.dev), gRPC docs, GraphQL spec, JSON:API, OpenAPI 3.1.

## Styles at a glance

| Style | When it wins | When it loses |
|---|---|---|
| **REST / HTTP+JSON** | Public APIs, CRUD-shaped resources, cacheable reads, partner ecosystems, third-party devs | Graph-like queries, high-throughput internal RPC, real-time updates |
| **GraphQL** | Varied clients (web + native) fetching heterogeneous subsets, rapid client evolution | Simple CRUD (overkill), caching (hard), authZ per-field (complex), strict SLOs (hard to reason about N+1 query cost) |
| **gRPC / Protobuf** | Internal service-to-service, strict schemas, polyglot backends, low latency, streaming | Browser clients (needs gRPC-Web + proxy), human-readable debugging, public APIs |
| **WebSocket / SSE** | Server push, real-time updates, chat, live dashboards | Stateless horizontal scale (sticky connections), cacheability, simple integration |
| **Webhook** | Async event delivery to partners | Reliable delivery (retries, dedup needed), partner reliability dependence |

## REST design essentials

- **Resources, not RPC** — `/orders/123/items` beats `/getOrderItems?orderId=123`
- **Nouns, not verbs** — HTTP methods ARE the verbs
- **Standard status codes** — 200, 201, 204, 400, 401, 403, 404, 409, 422, 429, 500, 503
- **Pagination** — cursor-based > offset-based for any collection that grows
- **Filtering/sorting** — query params (`?status=active&sort=-created_at`); don't invent a DSL
- **Versioning** — URL (`/v2/orders`) or header (`Accept: application/vnd.api+json; version=2`); URL is simpler and more visible
- **HATEOAS** — nice in theory, rarely worth it in practice for machine-to-machine
- **Idempotency** — ALL unsafe operations (POST, PATCH) accept an `Idempotency-Key` header that dedups for 24 h

Error response shape (RFC 7807 Problem Details):
```json
{
  "type": "https://api.example.com/errors/insufficient-funds",
  "title": "Insufficient funds",
  "status": 422,
  "detail": "Account balance 100 is less than requested amount 500",
  "instance": "/accounts/abc/withdrawals/xyz"
}
```

## GraphQL design essentials

- **Schema first** — it's the contract
- **Cursor-based pagination** via Relay spec (`edges { node { } cursor } pageInfo { } `)
- **Input types** for mutations
- **Avoid over-fetching on server** — use DataLoader to batch + cache per-request
- **Complexity limits** — every query costs points; reject queries above a budget
- **Persisted queries** for production clients — limits attack surface, enables CDN caching
- **N+1 is the default** — measure it; fix it with DataLoader
- **Auth per field, not per resolver** — granular authZ

Use GraphQL when you have **multiple client apps with diverging needs** (web, iOS, Android). Don't use it because "REST is old."

## gRPC design essentials

- **One `.proto` file per service**; version fields, don't remove or renumber
- **Four RPC kinds**: unary, server-streaming, client-streaming, bidi-streaming
- **Use `google.rpc.Status`** for errors; rich details beat HTTP status codes
- **Deadlines always** — gRPC has mandatory deadline propagation; use it
- **Interceptors** for auth, logging, tracing
- **gRPC-Web** needed for browsers (requires Envoy or similar proxy)

## Public vs internal

| Aspect | Public | Internal |
|---|---|---|
| Protocol | REST/JSON or GraphQL | gRPC or REST |
| Stability | Semver, deprecation cycles | Move fast |
| Auth | OAuth 2.0, API keys | Service mesh mTLS |
| Rate limits | Per tenant, documented | Less strict, more flexible |
| Schemas | OpenAPI, published | Protobuf, internal registry |

## Universal rules

1. **Document with OpenAPI/Protobuf** — not handwritten markdown
2. **Contract tests** — Pact, Spring Cloud Contract, or schema diffs in CI
3. **Never break compatibility silently** — add fields, don't repurpose them; deprecate with timelines
4. **Return enough in error responses** to let the caller self-recover (field, reason, suggested action)
5. **Pagination + filtering + sorting + sparse fieldsets** — all APIs will want them eventually; design in
6. **Idempotency keys for writes** — single most common gap in real-world APIs
7. **Correlation / trace IDs** in every request and response

## Versioning strategies

| Strategy | Pros | Cons |
|---|---|---|
| URL versioning (`/v1/…`) | Visible, simple, easy to route | Implies whole-API versioning |
| Header versioning | Fine-grained, URL stability | Invisible, harder to debug, hard to cache |
| Query param | Flexible | Mixes concerns with filters |
| No versioning (evolve only) | Simplest for clients | Requires strict backward compat discipline |

Default: URL versioning for public, evolve-only for internal.

## See also

- `resilience.md` — client side of API calls
- `security.md` — authN/authZ patterns for APIs
- `rate-limiting.md` — per-endpoint limits
- `microservices-patterns.md` — API gateway, BFF
