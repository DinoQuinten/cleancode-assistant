# Compliance Checklist

Architecture-relevant compliance items. Legal and policy counsel own the full compliance program; this list captures what architects are responsible for.

## When to apply this checklist

- **GDPR** — any EU user data, regardless of where you are
- **CCPA / CPRA** — California residents
- **HIPAA** — US health data (providers, payers, business associates)
- **PCI-DSS** — any storage/processing of payment card data
- **SOC 2** — service providers demonstrating trust to customers
- **FedRAMP** — US federal customers
- **ISO 27001 / 27701** — international customers; common in EU enterprise

Most of these overlap in what architecture must support.

## Data inventory & classification

- [ ] Data inventory maintained — every data store catalogued, with sensitivity class
- [ ] PII/PHI/PCI columns tagged at schema level
- [ ] Lineage known (where data came from, where it goes)
- [ ] Third-party processors catalogued; DPAs (Data Processing Agreements) in place

## Data residency & sovereignty

- [ ] Regions documented for every store (primary, replicas, backups)
- [ ] EU data stayed-in-EU if required by DPA (or SCCs in place)
- [ ] US federal: FedRAMP-authorized providers only
- [ ] China: localized infrastructure if serving Chinese users (PIPL)

## GDPR-specific

- [ ] Right to access — user can export their data within 30 days; process works end to end
- [ ] Right to erasure (deletion) — deletion propagates to all stores including backups within policy
- [ ] Right to rectification — user can update their data
- [ ] Data minimization — no collection beyond purpose
- [ ] Lawful basis documented for each data use
- [ ] Consent recorded with proof (what, when, version of terms)
- [ ] Breach notification — process for 72-hour regulator notification
- [ ] DPO appointed (if required by scale)
- [ ] DPIAs (impact assessments) for high-risk processing

## HIPAA-specific

- [ ] BAAs (Business Associate Agreements) with all subprocessors handling PHI
- [ ] PHI encrypted in transit AND at rest
- [ ] Access logging — who accessed which patient's record, when
- [ ] Minimum necessary principle — access limited to the scope of duty
- [ ] Breach notification process (HHS + affected individuals)
- [ ] Physical/admin/technical safeguards documented

## PCI-DSS

- [ ] Reduce scope — tokenize PAN so your systems don't store card data
- [ ] Use a PCI-DSS-compliant processor (Stripe, Braintree, Adyen)
- [ ] If you MUST store card data: dedicated network segment, logging, scans, annual audit
- [ ] No card data in logs, ever

## SOC 2

- [ ] Change management documented (PRs, deploy records)
- [ ] Access reviews quarterly
- [ ] Vulnerability management program (scans, patching cadence)
- [ ] Incident response documented and exercised
- [ ] Vendor risk assessments

## Retention & deletion

- [ ] Retention policy per data class (not just "keep everything")
- [ ] Automated deletion jobs tested
- [ ] Legal hold process documented
- [ ] Backup retention aligned with deletion obligations (backups that retain "deleted" data are a GDPR problem)

## Logging & audit

- [ ] Audit logs tamper-evident (write-once storage, signed)
- [ ] Logs retained per regulation (varies; often 1-7 years)
- [ ] Access to logs restricted and logged itself
- [ ] Admin actions logged

## Cryptographic standards

- [ ] FIPS 140-2 / 140-3 validated modules if FedRAMP/government
- [ ] Approved algorithms — AES-256, SHA-256+, TLS 1.2+
- [ ] Keys in HSM-backed KMS for regulated data
- [ ] Key rotation policy documented and automated

## Architectural considerations

- [ ] Data flow diagrams kept current (required for most audits)
- [ ] Segmentation between regulated and unregulated workloads
- [ ] Clear boundary between "in scope" and "out of scope" systems (reduces audit surface)
- [ ] Subprocessor list maintained for transparency

## Red flags for architects

- "We'll figure out compliance later" — the design baked in choices that are now expensive to undo
- Backups retain deleted data forever with no plan
- Logs contain PII/PHI indiscriminately
- Region choices made for cost only, not data residency
- Shared DB across tenants where some are regulated

## See also

- `security-checklist.md` — many controls overlap
- `../../design-system/references/security.md` — crypto and AC patterns
