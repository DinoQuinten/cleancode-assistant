# Reliability Checklist

Based on Google SRE book, Amazon Well-Architected Reliability Pillar, Nygard "Release It!".

## Targets & measurement

- [ ] SLOs defined for each user-facing service (latency, availability, freshness)
- [ ] SLIs measured and alerted on burn rate (not just breach)
- [ ] Error budget tracked; used to decide release velocity
- [ ] p50 AND p99 latencies measured (averages hide tail)

## Failure modes considered

- [ ] Graceful degradation path for every critical dependency
- [ ] Fallbacks documented (stale cache, default, static page, 503)
- [ ] Chaos / fault injection run at least quarterly
- [ ] Load testing at 1.5x peak, including degraded-dep scenarios

## Resilience patterns

- [ ] Every remote call has explicit timeout (not default TCP minutes)
- [ ] Retries only for idempotent operations
- [ ] Retries use exponential backoff + full jitter
- [ ] Retry budget caps retries globally (protect stressed deps)
- [ ] Circuit breakers on all downstream calls, per-dependency
- [ ] Bulkheads isolate thread/connection pools per downstream
- [ ] Idempotency keys accepted on unsafe operations

## Data durability

- [ ] Primary data stores replicated (multi-node, preferably multi-AZ)
- [ ] Backups automated, encrypted, tested (restore drill quarterly)
- [ ] RPO / RTO targets documented; infra sized to meet them
- [ ] Point-in-time recovery window defined and tested
- [ ] No "single replica is fine" shortcuts on critical data

## Deployment safety

- [ ] Canary or blue/green for risky changes
- [ ] Automated rollback on SLI breach during deploy
- [ ] Feature flags for risky features (kill switch)
- [ ] Dependency order respected in deploys (API compatibility)
- [ ] Schema migrations expand/contract pattern, reversible

## Multi-zone / multi-region

- [ ] At least 2 AZs for any production service
- [ ] Stateless tier survives AZ loss transparently
- [ ] Stateful tier has automated failover with quantified RTO
- [ ] If multi-region required, tested failover drills run

## Traffic management

- [ ] Load balancer health checks appropriate (shallow for liveness, deep for readiness)
- [ ] Rate limiting protects against self-inflicted DoS (retry storms)
- [ ] Load shedding engages before collapse (queue > threshold → reject)
- [ ] Clients back off on 429/503 (not just `sleep 1; retry`)

## Observability for reliability

- [ ] Traces cover every service hop
- [ ] Logs structured, centralized, searchable
- [ ] Metrics cover RED + USE; dashboards per service
- [ ] Alerts are actionable; no alerts that always need "restart X"

## Incident response

- [ ] On-call rotation documented, sustainable (not one heroic person)
- [ ] Runbooks for top-10 incident types
- [ ] Post-mortems written for all SEV-1/2; blameless
- [ ] Tracked follow-ups; they actually get done

## People + process

- [ ] No single point of human failure (key person bus-factor)
- [ ] Access to production granted on least-privilege; audited
- [ ] Production changes require review (PR, infra-as-code)
- [ ] Game days run regularly — team practices incident response

## Recovery testing

- [ ] Restore from backup actually tested (not just "we have backups")
- [ ] Failover tested end-to-end
- [ ] Secret rotation tested (not just theorized)
- [ ] DNS TTLs appropriate for failover speed

## Red flags to look for

- "We haven't tested the restore, but the backups are running"
- Single leader DB with no replication, no plan
- 3am pages for issues the team can't actually fix at 3am
- Alerts always fire together (noise); real signals get lost
- "We'll add monitoring after we ship"
- No capacity headroom; running at 95% of instance limits in steady state

## See also

- `../../design-system/references/resilience.md` — implementation patterns
- `../../design-system/references/observability.md` — measurement fundamentals
- `scalability-checklist.md` — capacity is half of reliability
