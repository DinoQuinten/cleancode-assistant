# Backend Folder Patterns

Backend codebases tend toward layered or domain-driven structures. This document covers the common ones and what `/cleancode:restructure` should propose.

Apply alongside `folder-structure-principles.md`.

## The four most common backend layouts

### Layout A — Layered (Controller / Service / Repository / Model)

```
src/
├── routes/ or controllers/    # thin HTTP handlers
├── services/                  # business logic
├── repositories/              # data access
├── models/ or entities/       # domain types
├── middleware/
├── validators/
└── utils/
```

**When it works:** Small to medium services with one or a few domains. Easy onboarding, predictable.
**When it breaks:** Once you have `services/auth.ts`, `services/billing.ts`, `services/orders.ts`, … and the same for repositories, controllers, validators — the auth team touches 5 folders to ship one feature.

### Layout B — Feature modules / domain-first

```
src/
├── modules/
│   ├── auth/
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   ├── auth.repository.ts
│   │   ├── auth.types.ts
│   │   ├── auth.module.ts        # NestJS, or just an index.ts
│   │   └── tests/
│   ├── billing/
│   └── orders/
├── shared/
│   ├── middleware/
│   ├── errors/
│   └── types/
└── infrastructure/                 # db, queue, cache adapters
```

**When it works:** Multiple distinct domains; teams own modules end-to-end; module-level tests; possible future extraction into separate services.
**Why it scales:** A new feature is a new folder. Removing one is one `rm -rf`. Modules can be split into separate services later without restructuring.

### Layout C — Hexagonal / Clean Architecture / DDD

```
src/
├── domain/
│   ├── auth/
│   │   ├── entities/
│   │   ├── value-objects/
│   │   └── ports/                 # interfaces (driven + driving)
│   └── billing/
├── application/
│   ├── auth/
│   │   ├── use-cases/             # one file per business operation
│   │   └── dto/
│   └── billing/
├── infrastructure/
│   ├── persistence/               # adapter implementations of domain ports
│   ├── http/                      # controllers (driving adapters)
│   ├── messaging/
│   └── external-apis/
└── shared/
```

**When it works:** Long-lived systems where business rules outlive frameworks; teams want testable domain code free of framework imports; multi-database or multi-transport requirements.
**When it's overkill:** Small CRUD services. Adds significant ceremony for little benefit.

### Layout D — Framework-conventional

Some frameworks prescribe layout strongly enough that fighting them costs more than yielding to them:

- **Rails:** `app/{controllers,models,views,helpers,services,jobs}` — go with the grain
- **Django:** `<project>/<app>/{models,views,serializers,urls,admin}.py` per Django app
- **NestJS:** modules with controllers, services, providers — feature-modules baked in
- **Spring Boot:** packages by feature recommended, but layered (`controller/`, `service/`, `repository/`) is also common
- **Go:** flat packages with descriptive names; `internal/` for private packages

When the framework has strong conventions, **honor them**. Restructuring a Rails app away from `app/services/` is fighting the river.

## Five common debt patterns and the fix

### 1. Fat route handler / fat controller

**Symptom:**
```
routes/api/projects/+server.ts   ← 280 lines
- HTTP parsing                       (should stay)
- input validation                   (should be in validator or service)
- 6 SQL queries                      (should be in repository)
- 3 business rules                   (should be in service)
- response formatting                (should stay)
```

**Restructure proposal:**
```
routes/api/projects/+server.ts                 ← thin (~30 lines)
src/lib/server/services/projects/
├── project-service.ts                         ← business rules
├── project-repository.ts                      ← SQL queries
├── project-validator.ts                       ← input validation
├── project-types.ts                           ← request/response shapes
└── index.ts                                   ← public API barrel
```

**Why:** Rule 15 (cohesion), Rule 6 (SRP), Martin ch 11 (Systems — separation of concerns). This pattern is documented in `before-after-clean-code.md` at the project root.

### 2. Service files mixing repository concerns

**Symptom:** `userService.ts` directly calls the database, runs SQL, transforms rows, and also implements business rules.

**Restructure proposal:**
- Extract `UserRepository` (data access only) — depends on the DB driver
- Keep `UserService` (business rules) — depends on the repository interface
- Inject the repository into the service via constructor

**Why:** Dependency Inversion (Rule 6 — D in SOLID). Services become testable with mock repositories.

### 3. Catch-all backend folder: `lib/`, `utils/`, `helpers/`

**Symptom:** `src/utils/` has 47 files: date helpers, crypto helpers, slack notifier, PDF generator, postgres connection pool, …

**Restructure proposal:**
- Pure cross-cutting utilities (date, crypto, formatting) → keep in `utils/` (the genuine 5–10 files)
- Anything domain-specific → move to its domain (`auth/crypto.ts`)
- Anything infrastructure (DB pool, external API client) → move to `infrastructure/` or `shared/clients/`
- Everything else: justify why it's "shared" or move it

### 4. Cross-cutting concerns scattered

**Symptom:** auth middleware in `routes/middleware.ts`, logging middleware in `utils/logger.ts`, error handling in `controllers/baseController.ts`.

**Restructure proposal:**
- All HTTP middleware → `middleware/` or `shared/middleware/`
- All cross-cutting concerns by purpose: `middleware/auth.ts`, `middleware/logging.ts`, `middleware/error-handler.ts`

### 5. Domain mixing in `models/`

**Symptom:** `models/` has `User.ts`, `Order.ts`, `Invoice.ts`, `Subscription.ts`, `OAuthToken.ts`, `WebhookEvent.ts` — six unrelated domains in one folder.

**Restructure proposal (when project is large enough):** move each model into its domain folder (`auth/User.ts`, `billing/Subscription.ts`, etc.) and convert `models/` into a folder of *only* truly shared types.

## Backend-specific principles

### Route handlers must stay thin

A route handler / controller action has one job: parse the request, call the service, format the response. Branching business logic in a handler is misplaced.

**Threshold:** ≤ 40 lines per handler. If it's longer, the logic belongs in a service.

### Repositories return domain objects, not raw rows

A `UserRepository.findById(id)` returns a `User` (domain entity), not a `Record<string, any>` from the DB driver. Mapping happens inside the repository, not at every caller.

### Services don't import the framework

A service that imports `from 'express'` or `from 'next/server'` is leaking transport concerns into business logic. Pass framework-agnostic data into the service; let controllers handle the framework.

### Tests live next to the code or in a parallel tree (per language)

- TS/JS: colocate (`user-service.ts` + `user-service.test.ts`) or use `__tests__/`
- Python: `tests/` parallel directory or pytest-discovered `test_*.py`
- Java: `src/test/java/...` parallel to `src/main/java/...`
- Go: `_test.go` files alongside the code being tested

Match the ecosystem.

## See also

- `folder-structure-principles.md` — the universal principles
- `framework-hints.md` — per-framework defaults (Rails, NestJS, Express, Spring, etc.)
- `before-after-clean-code.md` at the project root — case study: SvelteKit + Postgres, fat handler split into 4 cohesive modules with barrel re-exports
- Martin, *Clean Code* ch. 10 (Classes), ch. 11 (Systems)
- McConnell, *Code Complete* ch. 5 (Design in Construction), ch. 6 (Working Classes)
