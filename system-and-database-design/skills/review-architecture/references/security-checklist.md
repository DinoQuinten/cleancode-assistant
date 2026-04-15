# Security Checklist

Based on OWASP Top 10 2021, OWASP API Security Top 10 2023, NIST SP 800-207 (Zero Trust), CIS Benchmarks.

## Identity & Access

- [ ] AuthN is centralized (IdP, not per-service custom logic)
- [ ] Passwords (if self-hosted) hashed with Argon2id or bcrypt ≥ 12 rounds
- [ ] MFA available and required for privileged accounts
- [ ] No password reuse across services; no long-lived shared secrets
- [ ] Sessions have reasonable expiry (idle + absolute); logout invalidates server-side
- [ ] AuthZ decisions centralized (policy engine); not scattered across codebase
- [ ] Least privilege — users and services have only needed permissions
- [ ] IDOR tested — users cannot access other users' objects by ID manipulation
- [ ] Admin surface is segregated (separate domain, stricter auth)

## API & input

- [ ] All inputs validated at boundary (type, range, length, format)
- [ ] Parameterized queries everywhere — no SQL/NoSQL injection
- [ ] Output encoded for context (HTML, JSON, URL)
- [ ] CORS configured restrictively; no `*` for authenticated endpoints
- [ ] CSRF protection for state-changing non-JSON endpoints
- [ ] Rate limiting per user AND per IP, tighter on sensitive endpoints (login, password reset)
- [ ] File uploads: size limited, type validated (magic bytes, not extension), stored outside webroot
- [ ] No sensitive data in URLs (tokens, IDs, PII in query string get logged everywhere)

## Transport

- [ ] TLS 1.2+ only; TLS 1.0/1.1 disabled
- [ ] HSTS with `max-age=31536000; includeSubDomains; preload`
- [ ] Certificates auto-renewed (Let's Encrypt, ACM); expiry alerts
- [ ] Service-to-service uses mTLS or equivalent (mesh, workload identity)
- [ ] Internal traffic not bypassing encryption ("inside the VPC is safe" is NOT security)

## Data protection

- [ ] Data classified (public / internal / confidential / restricted)
- [ ] PII/PHI minimized (collect only what's needed)
- [ ] Encryption at rest enabled (disks, RDS, object storage)
- [ ] Field-level encryption for restricted data (PCI PAN, health identifiers)
- [ ] KMS-managed keys with rotation
- [ ] PII is NOT logged (scrubbed at logger layer)
- [ ] Backups encrypted; restore tested

## Secrets

- [ ] Zero secrets in code, config files, env vars (for humans), or chat
- [ ] Secrets in managed store (Vault, AWS SM, GCP SM, Azure KV)
- [ ] Secret rotation scheduled (90 d) AND incident-driven
- [ ] Least-privilege secret access (audited)
- [ ] Pre-commit hooks + CI check for leaked secrets (gitleaks, detect-secrets)

## Headers & cookies

- [ ] `Content-Security-Policy` (no `'unsafe-inline'` or `'unsafe-eval'`)
- [ ] `X-Content-Type-Options: nosniff`
- [ ] `Strict-Transport-Security` (see above)
- [ ] `Referrer-Policy: strict-origin-when-cross-origin`
- [ ] `Permissions-Policy` denies unused features
- [ ] Cookies: `Secure`, `HttpOnly`, `SameSite=Lax` (or `Strict`)

## Dependencies

- [ ] SCA (Snyk / Dependabot / Trivy) runs on every PR
- [ ] Known-vulnerable dependencies fail the build
- [ ] Base images pinned by digest, not floating tag
- [ ] Supply-chain attestation (SLSA, Sigstore) — at least aspirational

## Infrastructure

- [ ] Public surfaces minimized (only LB ingress is public; app tier private)
- [ ] Security groups / firewall rules default-deny
- [ ] No SSH bastions with keys in personal machines; prefer SSM/OSLogin
- [ ] Admin access requires MFA, logged, auditable
- [ ] Cloud root / org admin accounts locked down, MFA, rarely used
- [ ] Isolated dev/staging/prod — no cross-env access by default

## Logging & detection

- [ ] Authn events (login, logout, failed login, password change) logged
- [ ] Authz denials logged
- [ ] Admin actions logged (who, what, when, from where)
- [ ] Centralized log storage, read-only (tamper-evident)
- [ ] SIEM/alerting on anomalous patterns (brute force, privilege escalation, data exfil)

## Incident readiness

- [ ] Documented incident response plan
- [ ] On-call rotation, escalation paths
- [ ] Runbooks for common breach scenarios
- [ ] Data breach notification process (for GDPR and similar)
- [ ] Post-mortem template and culture

## Red flags to look for

- "We're behind a VPN, so we don't need X"
- "The SDK handles auth" (but nobody reviewed what it does)
- Hardcoded API keys in repo history
- Admin endpoints on same port as user endpoints, no segmentation
- Any service with root equivalent in its IAM role/permissions

## See also

- `../../design-system/references/security.md` — implementation patterns
- `compliance-checklist.md` — regulatory overlay
- `reliability-checklist.md` — security incidents ARE reliability incidents
