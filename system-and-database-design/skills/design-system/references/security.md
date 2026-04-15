# Security

Authoritative sources: OWASP Top 10 2021, OWASP API Security Top 10 2023, NIST SP 800-207 (Zero Trust), RFC 6749/7636 (OAuth 2.0/PKCE), OIDC Core 1.0.

## Layering

Defense in depth. No single control is sufficient.

1. **Network** — VPC isolation, private subnets, security groups, egress control
2. **Transport** — TLS 1.3 everywhere, mTLS between internal services, HSTS for public
3. **Identity** — authN (who are you?) + authZ (what can you do?)
4. **Application** — input validation, output encoding, parameterized queries
5. **Data** — classification, encryption at rest, KMS-managed keys
6. **Audit** — tamper-evident logs of access and mutations

## Identity: authentication

### Public-facing APIs

- **OAuth 2.0 + PKCE** for user-facing OAuth flows (mobile, SPA)
- **OpenID Connect** on top for identity (id_token); don't roll your own login
- **Refresh tokens** short-lived (days), access tokens very short-lived (15 min); rotate refresh on use
- **No passwords in your own DB if you can avoid it** — delegate to an IdP (Auth0, Okta, Cognito, Clerk); if you must: Argon2id, not bcrypt, never MD5/SHA-1

### Service-to-service

- **mTLS** — each service has a cert issued by an internal CA (SPIFFE/SPIRE or service-mesh like Istio/Linkerd); mutual authentication built in
- **Short-lived tokens** from a workload identity provider (GCP IAM, AWS IAM roles, Azure MI); no long-lived secrets sitting in env vars
- **Never share API keys across services**; each service has its own identity

## Authorization

Pick a model:

- **RBAC (role-based)** — simplest; user→role→permissions. Breaks down when permissions are resource-specific.
- **ABAC (attribute-based)** — rules evaluate user attributes, resource attributes, action, context. Flexible, complex to reason about.
- **ReBAC (relationship-based)** — Google Zanzibar style; permissions flow along relationships ("user X is owner of org Y which owns doc Z"). Best for collaborative products; see OpenFGA, SpiceDB.

Whatever you pick, centralize authZ decisions in a policy engine (OPA, Cedar, OpenFGA). Don't scatter `if user.role == ...` across the codebase.

### The "IDOR" gap

Authenticated users accessing OTHER users' resources by guessing IDs. Always verify `resource.owner == current_user` (or your equivalent). Unit tests for every endpoint: "authenticated as user A, try to access user B's object; expect 403/404."

## Secrets management

- **No secrets in code, config files, env vars (for humans), or tickets.**
- Secret managers: AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault, 1Password Connect
- **Rotation** on a schedule (90 d) AND on incident
- **Scoped** — least privilege; don't give every service the DB admin password
- **Audited** — every secret read is logged

For dev: `.env` files are acceptable ONLY if in `.gitignore` AND you use a pre-commit hook that rejects high-entropy strings (`detect-secrets`, `gitleaks`).

## Zero trust

NIST SP 800-207. Key principles:

1. **No implicit trust** based on network location (no "inside the VPC means safe")
2. **Authenticate + authorize every request**, not just at the edge
3. **Least privilege** — users and services have only the permissions they need NOW
4. **Continuous verification** — session risk scoring, device posture checks

Service mesh + workload identity implement this for service-to-service. For user-to-service, conditional access + short-lived sessions + MFA.

## Transport security

- **TLS 1.3** — TLS 1.2 still acceptable; disable 1.0, 1.1, SSLv3
- **HSTS** with `max-age=31536000; includeSubDomains; preload`
- **Certificate pinning** is usually not worth the ops pain; prefer CT log monitoring
- **mTLS** internal — no unencrypted service-to-service, even "inside" the VPC

## Data protection

### Classification

Tag every column / field:
- **Public** — freely shareable
- **Internal** — not for outsiders
- **Confidential** — PII, credentials, business-sensitive
- **Restricted** — payment card data (PCI-DSS), health records (HIPAA)

### Encryption

- **At rest**: enable at the storage layer (cloud disks, RDS, S3) — it's free now; no excuse
- **Field-level** for restricted data — encrypt sensitive columns with KMS-managed keys; make key rotation possible without re-encrypting every row (use a key per customer or per year)
- **Tokenization** for PCI — replace PAN with a token; vault holds the mapping
- **Hashing**: passwords = Argon2id; searchable PII = HMAC with a secret

### PII minimization

Don't collect what you don't need. Don't keep it longer than you need. Data you don't have can't leak.

## Application-level

### OWASP Top 10 quick hits

- **Injection** — parameterized queries; NEVER concatenate SQL; same for NoSQL ($where in Mongo, etc.)
- **Broken auth** — lockout after N failed attempts; no enumeration via error messages
- **Sensitive data exposure** — don't log secrets/PII; configure logger scrubbing
- **XXE** — disable external entity resolution in XML parsers
- **Broken access control** — see IDOR above
- **Security misconfig** — no default creds; security headers; disabled directory listing
- **XSS** — output encoding, Content-Security-Policy, framework-default escaping
- **Insecure deserialization** — don't deserialize untrusted input; use signed payloads
- **Vulnerable dependencies** — SCA (Snyk, Dependabot, Trivy)
- **Insufficient logging** — see `observability.md`

### Headers for any HTTP response

- `Content-Security-Policy`: strict, no `'unsafe-inline'`
- `X-Content-Type-Options: nosniff`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy`: deny camera/mic/geolocation by default

## See also

- `api-design.md` — auth at API boundary
- `rate-limiting.md` — anti-abuse layer
- `../review-architecture/references/security-checklist.md` — review checklist derived from this
- `../review-architecture/references/compliance-checklist.md` — GDPR/HIPAA/SOC2 overlap
