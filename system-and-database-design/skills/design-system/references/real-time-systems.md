# Real-time Systems

Authoritative sources: RFC 6455 (WebSocket), HTML Living Standard (EventSource/SSE), Slack engineering blog (fanout), WhatsApp/Discord engineering talks, Phoenix Channels docs.

## Push mechanisms — the four options

| Mechanism | Direction | Overhead | Sticky? | When to pick |
|---|---|---|---|---|
| **Short polling** | Client pulls | High | No | Prototype only |
| **Long polling** | Client holds; server replies when data ready | Medium | Yes (in flight) | Firewall-hostile environments; degraded WebSocket fallback |
| **SSE (Server-Sent Events)** | Server pushes text/event-stream | Low | Yes | Server→client only, HTTP-friendly, automatic reconnect |
| **WebSocket** | Bidirectional | Lowest per-msg | Yes | Interactive; both directions; custom protocols |

Default: SSE for notifications/feeds (client-to-server goes via separate HTTP). WebSocket for chat/games.

## Connection state

Real-time connections are **stateful** — they break the "stateless horizontal scale" dogma.

- Clients connect to a specific server; routing matters
- Use **sticky routing** at the LB (cookie-based or consistent hash on user_id)
- Use a **pub/sub backbone** (Redis pub/sub, NATS, Kafka) to deliver events to whichever server holds the target connection

Pattern (the "gateway" pattern):
1. User connects to any WebSocket gateway server
2. Gateway registers `(user_id → gateway_instance)` in a distributed directory (Redis, DynamoDB)
3. When an event for user X arrives, publisher looks up X's gateway, sends message via pub/sub to that gateway, which relays over the WebSocket

## Fanout patterns

### Write fanout (push on write)

On event, write to each recipient's inbox/feed immediately.
- **Pro**: fast reads (just read inbox)
- **Con**: expensive for high-fanout sources (celebrity problem — Justin Bieber posts, system writes 100M inboxes)

### Read fanout (pull on read)

On event, write to just the author's outbox. On read, merge outboxes of followees.
- **Pro**: cheap writes; scales with fanout-in (followers) not fanout-out (followees)
- **Con**: expensive reads; requires caching heavily-read timelines

### Hybrid (write for most, read for celebrities)

Production systems (Twitter, Instagram) use write fanout for normal users and read fanout for high-follower accounts. The cutoff is tuned empirically.

## Presence

"Is user X online right now?" Ops considerations:

- Maintain a **heartbeat** (client ping every 30 s; server considers offline after 2 missed)
- Store presence in fast KV (Redis sorted set keyed on expiry)
- **Don't** persist presence to primary DB; it's ephemeral and high-churn
- Subscribe-on-demand — only track presence for users someone is watching (scales to N^2 contact graphs)

## Delivery guarantees

- **At-most-once** — fire and forget; good for ephemeral ("user is typing…")
- **At-least-once** — durable; retries; consumer must dedupe; good for chat messages with message IDs
- **Exactly-once** — hard; achieve via at-least-once + idempotent consumer
- **Ordered** — per-sender ordering cheap; total ordering expensive; sequence numbers per sender

For chat: durable per-message store + per-user cursor tracking last-read. Deliver on (re)connect any messages after the cursor.

## Reconnection & offline

- Client tracks **last_event_id**; reconnect sends it; server replays from there (SSE `Last-Event-ID` header, WebSocket `?since=…`)
- Server retains a **replay window** (last N minutes or N events per stream)
- Beyond replay window → client re-syncs from canonical store (DB fetch)

## Scaling numbers

- **Per-gateway connections**: ~100k on a tuned box (Go/Erlang/Elixir), ~10k on Node, ~1k on vanilla JVM (without optimization). File descriptor and memory-per-conn are the limits.
- **Messages/sec**: 100k-1M per gateway depending on serialization (JSON ≪ Protobuf ≪ binary)
- **Load test early** — connection fanout surprises people; use k6, Artillery, or tsung

## Protocols on top

- **MQTT** — IoT, low-bandwidth pub/sub over TCP; QoS 0/1/2
- **STOMP** — text-based, easier to debug than raw WebSocket
- **JSON-RPC / WAMP** — structured RPC over WebSocket
- **Phoenix Channels** (Elixir) — opinionated topic model with presence built in

## Security

- **Auth on connect** — pass token in query param (logged; less secure) or in first message after connect (safer)
- **Re-auth periodically** — long-lived connections need refresh; disconnect on token revocation
- **Origin checks** for browser WebSockets — CSWSH attacks are real
- **Rate limit per connection** — not just per IP; a single connection can flood
- **Validate every frame** — don't trust length/opcode

## Common failures

- **No backpressure** — slow consumer's buffer grows unbounded; kill the slow client
- **Sticky routing lost on deploy** — reconnect storm; rate-limit reconnects with jitter
- **Broadcast amplification** — one message × 1M recipients = 1M writes; batch, throttle, or fan-out lazily
- **Presence flapping** — device sleep causes false offline; smooth with 10-30 s grace

## See also

- `messaging.md` — queues/streams power the fanout backbone
- `load-balancing.md` — sticky routing for WebSockets
- `resilience.md` — circuit breakers on gateway→core service calls
