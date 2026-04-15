# Deployment Strategies

Authoritative sources: Google SRE book ch. 8 "Release Engineering", Jez Humble "Continuous Delivery", LaunchDarkly feature flag docs, AWS / GCP deployment docs.

## Strategies

### Rolling update — DEFAULT for stateless services

- Replace N pods at a time; wait for readiness before next batch
- Fast, cheap, no duplicate infra
- **Weakness**: new and old versions serve traffic simultaneously during rollout; requires backward-compatible schema and API changes
- Kubernetes default (`RollingUpdate`)

### Blue/green

- Stand up full "green" environment alongside "blue"; flip all traffic at once (LB or DNS switch)
- **Pro**: instant rollback (flip back)
- **Pro**: smoke test green with production traffic before flipping
- **Con**: 2× infra during deploy
- **Con**: all-or-nothing — one bad deploy affects 100% of users at flip

### Canary

- Route small fraction (1%, 5%, 25%) of traffic to new version; monitor; expand if healthy
- **Pro**: gradual blast-radius expansion; catches issues before full rollout
- **Pro**: compatible with automated rollback on SLI breach
- **Con**: requires good observability to detect regressions quickly
- **Con**: new/old coexistence — same backward-compat requirements as rolling

Canary is the default for any service where incidents matter.

### Shadow / dark launch

- Duplicate production traffic to new version; discard its responses
- No user impact; tests load, correctness against real payloads
- **Use case**: rewrites, cache layer upgrades, database migrations (read side)
- Never shadow writes without the new system being idempotent + write-isolated

### A/B testing

- Split users across variants for business metric comparison, not release safety
- Powered by feature flags, NOT deploy machinery
- Requires statistical analysis; don't call winners on p = 0.12

### Feature flags

Separate **code deploy** from **feature release**. Deploy dark; launch on flag.

- **Release flags** — short-lived, flip on/off during launch; remove after
- **Ops flags** — kill switches for expensive features (degrade under load)
- **Experiment flags** — A/B test; owned by product analytics
- **Permission flags** — entitlements; owned by billing/product

Flag discipline:
- **Every flag has an owner and an expiry** (date or condition)
- **Default to "off"** — new code path gated off
- **Automated flag audit** — CI reports flags past expiry
- **Test both paths** — forever as long as the flag exists

## Deployment pipeline

Minimum stages:

1. **Build** — deterministic, reproducible; produce an image with a content-addressed tag
2. **Unit tests** — fast (<5 min); gate merge
3. **Integration tests** — run in CI; gate deploy
4. **Deploy to staging** — automatic on main merge
5. **End-to-end tests** — run against staging
6. **Canary to prod** — 5% for 15 min, then 25%, then 100%; automated rollback on SLI breach
7. **Post-deploy verification** — synthetic tests confirm critical paths

Deploy often. Multiple times a day beats once a week — smaller diffs = easier rollback.

## Rollback plans

**Every deploy must have a rollback path known BEFORE deploy.** Rollback via:
- Previous image tag (trivial if deploys are immutable + versioned)
- Previous DB migration (requires expand-contract pattern — see `../design-database/references/schema-evolution.md`)
- Feature flag off (fastest; seconds)

Time-to-rollback is an SLO. Target: under 5 minutes from "oh no" to "stable."

## Expand / contract for schema

Deploying a DB change alongside code:

1. **Expand**: add new column/table (nullable, default); deploy code that writes to both old and new
2. **Backfill**: populate new from old (offline job)
3. **Migrate reads**: deploy code that reads from new
4. **Contract**: drop old column (in a later, separate deploy)

Never do destructive schema changes in the same deploy as code that uses the new schema. Rollback paths evaporate.

## Container runtime specifics (Kubernetes)

- **Readiness probe** — "am I ready to serve traffic?" — gates LB inclusion
- **Liveness probe** — "am I dead and need restart?" — gates restart
- **Startup probe** — gives slow-starting apps more time before liveness kicks in
- **PodDisruptionBudget** — "don't evict more than N at once"; critical for rolling updates
- **Resource requests + limits** — set both; let the scheduler pack efficiently

## Serverless specifics

- **Cold starts** — mitigate with provisioned concurrency (AWS Lambda) or keep-warm pings
- **Max execution time** — Lambda 15 min, GCP Cloud Run 60 min; not suitable for long-running jobs
- **State** — none in the function; use external KV, DB, or queue
- **Cost model** — billed per invocation; can beat containers at low QPS, loses at high QPS

## Multi-region

- **Active/passive** — standby region gets writes replicated; failover on DR event
- **Active/active** — both serve; conflict resolution required for writes (last-write-wins or CRDTs)
- **Pilot light** — infra provisioned but not running; fastest DR at lowest cost

Multi-region is expensive and complex. Don't adopt until single-region genuinely isn't meeting SLO.

## See also

- `resilience.md` — canary protects against bad code; resilience protects against bad days
- `observability.md` — automated canary analysis depends on good SLIs
- `../design-database/references/schema-evolution.md` — expand/contract discipline
