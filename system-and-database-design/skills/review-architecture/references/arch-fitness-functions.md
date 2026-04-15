# Architecture Fitness Functions

_Source: Fundamentals of Software Architecture (Richards & Ford), Chapter 6 — Measuring and Governing Architectural Characteristics._

## Concepts

- **Definition** — a fitness function is "any mechanism that performs an objective integrity assessment of some architecture characteristic." Originated from *Building Evolutionary Architectures* (Ford, Parsons, Kua).
- **Scope** — atomic (one characteristic) vs holistic (multiple characteristics interact).
- **Timing** — triggered (on demand) vs continual (always running) vs temporal (scheduled).
- **Implementation** — unit-test-like code, metrics thresholds, chaos experiments, static analysis rules.
- **Categories**:
  - **Structural** — layer dependencies, cyclic dependency detection (e.g. ArchUnit, NetArchTest, Dependency-Cruiser)
  - **Performance** — p99 latency budgets in CI load tests
  - **Security** — secret scanning, CVE scanning, policy-as-code (OPA)
  - **Reliability** — chaos tests that verify retry + failover work
  - **Cost** — budget caps on infra spend per environment
  - **Data** — schema drift detection, PII classification checks
- **Governance via automation** — replace "architect as gatekeeper" with "architect as rule-author." Rules live in the build pipeline.

## Common fitness functions 

| Characteristic | Fitness function |
|---|---|
| No cyclic module deps | ArchUnit rule, fails CI |
| API backwards compat | Schema diff in CI (buf, protolock, openapi-diff) |
| p99 latency < 200 ms | Load test in pre-prod, fails on regression |
| Zero secrets in commits | gitleaks / trufflehog in pre-commit + CI |
| No direct DB access outside repository layer | Static analysis rule |
| SLO error budget not exhausted | Alertmanager rule blocks deploy when budget burned > X |
| Zero production services without health checks | K8s admission controller |
| No privileged containers | OPA / Kyverno policy |

## How to roll these out 

1. **Pick one characteristic that got you burned** (not an exhaustive list).
2. **Write the function as a unit test or CI step** — pass/fail, not a dashboard.
3. **Make it blocking.** Non-blocking checks get ignored.
4. **Review quarterly.** Retire functions that no longer fit; add new ones as pain emerges.

## See also

- `anti-patterns.md` — what the fitness functions are defending against
- `../../design-system/references/observability.md` — where metric-based functions come from
- `../../design-principles/references/trade-off-catalog.md` — entry 17 (resilience vs simplicity)
