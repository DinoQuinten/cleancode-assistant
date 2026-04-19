# Framework Hints — consulted, not obeyed

This is a cheatsheet of typical folder layouts per framework.

**Rule of use:** consult only when the project's own conventions are ambiguous (very small project, brand-new repo, or no clear pattern after sampling). Whenever the project demonstrates its own style, follow that — even if it diverges from the convention here.

## Frontend frameworks

### Next.js — App Router

```
app/                          # routes — thin pages and route handlers
├── (auth)/
│   ├── login/page.tsx
│   └── signup/page.tsx
├── billing/
│   ├── page.tsx
│   └── route.ts              # API route
├── api/
│   └── webhooks/route.ts
└── layout.tsx
src/                          # alternate root for non-route code
├── features/                 # domain-first
├── ui/ or components/        # design system
└── lib/                      # helpers, server-only code, db client
```

**Conventions:**
- Pages and route handlers (`page.tsx`, `route.ts`) stay thin (≤ 40 lines)
- Server components by default; mark with `'use client'` only when needed
- Server-only code goes in `lib/server/` or files that import server-only modules
- Logic and data shapes belong in `features/` or `lib/`, not in `app/`

### Next.js — Pages Router

```
pages/
├── api/                      # API routes
├── _app.tsx
└── billing/index.tsx
src/
├── components/
├── lib/
└── features/                 # if domain-first
```

### SvelteKit

```
src/
├── routes/                   # pages and `+server.ts` endpoints — thin
├── lib/                      # path alias `$lib/`
│   ├── server/               # server-only code (DB, secrets)
│   ├── components/           # client components
│   └── ...
├── app.html
├── hooks.server.ts
└── hooks.client.ts
```

**Conventions:**
- `+page.svelte` / `+page.server.ts` / `+server.ts` stay thin
- Real logic in `src/lib/server/services/`, `src/lib/server/repositories/`
- Anything in `src/lib/server/` is automatically excluded from client bundles

### Remix

```
app/
├── routes/                   # routes (file-based or flat)
├── components/
├── lib/
└── root.tsx
```

**Conventions:**
- `loader` and `action` exports in route files do data fetching/mutations
- Heavy logic moves to `lib/` or `services/`

### Nuxt

```
pages/
components/
composables/                  # auto-imported composables
server/
├── api/
├── routes/
└── utils/
plugins/
middleware/
stores/                       # Pinia stores
```

### Astro

```
src/
├── pages/                    # routes
├── components/
├── layouts/
├── content/                  # content collections
└── lib/
```

### React (Vite, no meta-framework)

No prescribed layout. Common choices:
```
src/
├── components/
├── pages/                    # if using react-router
├── hooks/
├── stores/
├── api/
└── lib/
```
or feature-folders (`src/features/<name>/{components,hooks,api,store,types}`).

### Vue 3 (Vite)

```
src/
├── components/
├── views/                    # route components
├── composables/              # use-* functions
├── stores/                   # Pinia
├── router/
└── lib/
```

### Angular

```
src/app/
├── core/                     # singleton services, guards, interceptors
├── shared/                   # shared components, pipes, directives
├── features/                 # feature modules
│   └── <feature>/
│       ├── components/
│       ├── services/
│       ├── <feature>.module.ts
│       └── <feature>-routing.module.ts
```

## Backend frameworks

### NestJS

```
src/
├── modules/
│   └── <feature>/
│       ├── <feature>.controller.ts
│       ├── <feature>.service.ts
│       ├── <feature>.module.ts
│       ├── dto/
│       └── entities/
├── common/                   # filters, guards, interceptors, pipes
└── main.ts
```

**Conventions:** module-per-feature is idiomatic; controllers thin, services do work, repositories via TypeORM/Prisma.

### Express / Fastify

No prescribed layout. Common choices:

**Layered:**
```
src/
├── routes/ or controllers/   # thin handlers
├── services/
├── repositories/
├── middleware/
└── models/
```

**Domain-first:**
```
src/
├── modules/<feature>/{controller,service,repository,routes}
└── shared/
```

### Rails

```
app/
├── controllers/
├── models/
├── views/
├── helpers/
├── jobs/
├── mailers/
├── services/                 # service objects (community convention)
└── policies/                 # Pundit
```

**Convention:** Honor MVC. Service objects under `app/services/` for orchestration. Don't fight Rails.

### Django

```
<project>/
├── <app>/                    # one folder per Django app
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py
│   └── migrations/
├── settings/
└── manage.py
```

**Convention:** Django apps are the unit of cohesion. Cross-app utilities go in a shared app.

### FastAPI

No prescribed layout. Common choice:
```
app/
├── api/
│   └── v1/
│       ├── endpoints/
│       └── deps.py
├── core/                     # config, security
├── crud/                     # data access
├── models/                   # SQLAlchemy
├── schemas/                  # Pydantic
└── services/
```

### Spring Boot

```
src/main/java/com/example/<project>/
├── controller/
├── service/
├── repository/
├── model/ or entity/
├── dto/
└── config/
```

or feature-packages:
```
src/main/java/com/example/<project>/
├── auth/
│   ├── AuthController.java
│   ├── AuthService.java
│   └── User.java
└── billing/
```

Tests in parallel tree at `src/test/java/...`.

### Go

```
cmd/                          # main packages (one per binary)
├── api/main.go
└── worker/main.go
internal/                     # private packages — most code here
├── auth/
├── billing/
└── shared/
pkg/                          # public packages (importable by other modules)
```

**Convention:** Flat packages with descriptive names. Each package = one cohesive concept. No `utils.go` — name it for what it does.

### Ruby on Rails Engines

Treat each engine like a mini Rails app under `engines/<name>/`.

## Monorepos

**Turborepo / pnpm workspaces / Nx:**
```
apps/
├── web/                      # frontend app
├── api/                      # backend service
└── docs/
packages/
├── ui/                       # shared design system
├── config/                   # shared eslint/tsconfig
├── types/                    # shared types
└── utils/                    # cross-app utilities
```

**Per-subtree restructure:** `apps/web/` and `apps/api/` are independent contexts. Detect their conventions separately.

## When the project shows none of these conventions

If the project is too small or too new to have established a pattern:

1. **Pick based on size** (per `folder-structure-principles.md` rule 5):
   - < 30 files: stay flat
   - 30 – 300 files: layered or shallow domain
   - > 300 files: domain-first
2. **Pick based on language** (per the framework above)
3. **Tell the user explicitly** in the proposal: *"This project hasn't established conventions yet — proposing <pattern> based on <reason>. Confirm or override."*

## Reminder

These are **hints**, not rules. The cleancode philosophy is that folder structure is a domain decision, not a framework decision. The framework defaults are useful starting points; the project's own observed patterns are authoritative.
