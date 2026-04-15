# Observability

Authoritative sources: Google SRE book ch. 4, 6, Brendan Gregg "Systems Performance", Tom Wilkie's RED method, USE method, OpenTelemetry docs.

## The three pillars (+ one)

1. **Logs** — discrete events; rich context; expensive at scale
2. **Metrics** — numeric aggregates over time; cheap; low cardinality
3. **Traces** — causal chain across services; essential for distributed debugging
4. **(Profiles)** — continuous profiling (eBPF, pprof); the fourth pillar in 2026

Use all four. They answer different questions.

## Metrics

### RED method (for SERVICES)

For every service / endpoint, emit:
- **Rate** — requests per second
- **Errors** — error rate (per second or percentage)
- **Duration** — histogram of latencies (p50, p95, p99)

This is enough for 80% of alerting on user-facing services.

### USE method (for RESOURCES)

For every resource (CPU, disk, NIC, DB connection pool):
- **Utilization** — % busy
- **Saturation** — queue depth / wait time
- **Errors** — count

Saturation is the underrated one — it catches problems before utilization hits 100%.

### Four golden signals (SRE book)

Latency, traffic, errors, saturation. Essentially RED + Saturation. Use this name when talking to ops.

### Cardinality discipline

Labels × label values = cardinality. Prometheus dies at ~1M active series. Rules:
- **Never** put `user_id`, `session_id`, or `request_id` in a metric label
- Keep label sets bounded: `method` × `status_code` × `route` is fine; `route` should be templated (`/users/:id` not `/users/123`)
- If you need per-user data, use logs/traces, not metrics

## Logs

### Structured, not free-text

JSON logs with consistent fields. Minimum per line:
- `timestamp` (RFC3339 with timezone)
- `level` (DEBUG / INFO / WARN / ERROR)
- `service` / `component`
- `trace_id` / `span_id` (enables log → trace jump)
- `message`

### Levels

- **DEBUG** — off in prod; verbose dev aid
- **INFO** — significant events: requests, jobs, state transitions
- **WARN** — recoverable problems; retry succeeded; circuit breaker tripped
- **ERROR** — actual failure visible to user or downstream
- **FATAL** — service cannot continue; exit after

Use warn sparingly. If you'd never page on it, it's probably info.

### Sampling

At scale, sample logs (and traces) to stay affordable:
- **Head sampling** — decide at request start; deterministic but misses rare errors
- **Tail sampling** — decide at request end; keeps all errors + slow requests; needs buffering

## Traces

### Instrument at every hop

Every incoming request creates a root span; every outgoing call creates a child span. Propagate `traceparent` (W3C) across service boundaries.

### What to include in spans

- `service.name`, `span.kind` (server / client / producer / consumer / internal)
- HTTP method, route, status
- DB statement (redacted of PII), DB instance
- Messaging destination, message ID

OpenTelemetry is the standard. Avoid vendor lock-in at the SDK level.

### Reading a trace

1. Look at the **critical path** (longest chain of dependent spans)
2. Look for **wide spans** (parallel calls — could you add more?)
3. Look for **gaps** (dead time between spans — queueing, GC)
4. Look for **retries** (duplicate spans at the same level)

## SLO / SLI / error budget

- **SLI (Service Level Indicator)** — a measurement: "% of requests in the last 30 days that returned 2xx or 3xx within 500 ms"
- **SLO (Service Level Objective)** — the target for that SLI: "99.9%"
- **SLA** — contractual version of SLO with penalties; usually laxer than SLO
- **Error budget** — `1 - SLO`. For 99.9%, budget is 0.1% of the month ≈ 43 minutes downtime

Alert on **burn rate** of the error budget, not on raw thresholds. Multi-window: fast burn (1 h consuming 2% of month's budget) AND slow burn (6 h consuming 5%).

## Alerting rules

1. **Alert on symptoms, not causes.** "Requests failing" beats "CPU at 80%." Causes should be alerts only if unhandled they ALWAYS cause symptoms.
2. **Every page must be actionable.** If the responder can't fix it at 3am, it's not a page — make it a ticket.
3. **No toil pages.** If the fix is always "restart X," automate the restart.
4. **SLO-based alerting** — see "error budget" above.

## Dashboards

- One **overview** per service: RED + dependencies
- One **service map** for the whole system
- Per-incident **runbooks** linked from every alert

Dashboards aren't observability — they're one view. Prioritize exploration tools (ad-hoc queries, log search) over pre-built dashboards.

## Continuous profiling

eBPF-based (Parca, Pyroscope, Google Cloud Profiler). Low overhead (<2% CPU). Catches:
- CPU hotspots in prod that don't show in staging
- Lock contention
- Memory allocation storms
- Regressions tied to a commit

Should be default-on in 2026.

## See also

- `resilience.md` — alerts feed into circuit-breaker tuning
- `../review-architecture/references/reliability-checklist.md` — observability is a reliability gate
