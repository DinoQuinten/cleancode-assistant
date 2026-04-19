# Frontend Folder Patterns

Frontend codebases have their own structural debt patterns. This document covers the common ones and what `/cleancode:restructure` should propose.

The cleancode plugin historically leans backend; this fills the gap. Apply alongside `folder-structure-principles.md`.

## The four most common frontend layouts

### Layout A — Layered by kind (small to medium projects)

```
src/
├── components/      # UI building blocks
├── pages/           # route-level screens
├── hooks/           # shared React hooks / Vue composables
├── stores/          # global state
├── lib/             # framework-agnostic helpers
├── api/             # HTTP client wrappers
├── styles/          # global styles
└── types/           # shared type definitions
```

**When it works:** ≤ 100 source files, ≤ 3 distinct domains. Easy onboarding, predictable.
**When it breaks:** Once you have `components/Login*.tsx`, `components/Billing*.tsx`, `components/Profile*.tsx`, `hooks/useLogin*`, `hooks/useBilling*`, … the same domain lives in 5 places.

### Layout B — Feature folders (screaming architecture)

```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── api.ts
│   │   ├── store.ts
│   │   ├── types.ts
│   │   └── index.ts          # public API
│   ├── billing/
│   └── orders/
├── ui/                       # cross-feature design system
├── lib/                      # framework helpers
└── app/ or pages/            # route definitions only — thin
```

**When it works:** Multiple distinct domains, multiple developers, separate release cadences. Strong fit for medium-to-large apps.
**Why it scales:** Adding a new feature is one new folder. Removing one is one `rm -rf`. Domain ownership is obvious.
**Common mistake:** Cross-feature dependencies sneak in (`features/billing/components/X.tsx` imports `features/auth/utils/Y.ts`). When this happens, promote shared code to `ui/` or `lib/`.

### Layout C — Atomic Design (less common but real)

```
src/
├── atoms/         # primitive UI: Button, Input, Label
├── molecules/     # combinations: SearchBar (Input + Button)
├── organisms/     # complex sections: Header, ProductCard
├── templates/     # page scaffolding
└── pages/         # composed templates with data
```

**When it works:** Heavy design-system focus, a clear visual taxonomy, strong design-developer collaboration.
**When it breaks:** "Is this a molecule or an organism?" debates eat time. Most apps don't need this level of taxonomy.

### Layout D — Framework-driven (App Router / SvelteKit / Remix)

```
app/                      # routes (Next App Router) — thin pages only
├── (auth)/
│   ├── login/page.tsx
│   └── signup/page.tsx
├── billing/page.tsx
└── layout.tsx
src/
├── features/             # the real logic lives here
├── ui/                   # design system
└── lib/                  # helpers, server-only code
```

**When it works:** Modern meta-frameworks where the routing folder *is* the URL structure. Keep route files thin (≤ 40 lines), put logic in `features/` or `lib/`.

## Six common debt patterns and the fix

### 1. Page-file bloat — the 500-line `page.tsx`

**Symptom:**
```
app/dashboard/page.tsx   ← 580 lines
- 12 sub-components inlined
- data fetching mixed with UI
- validation logic in event handlers
- types defined alongside the component
```

**Restructure proposal:**
```
app/dashboard/page.tsx              ← thin (~30 lines): fetches + renders
features/dashboard/
├── components/
│   ├── DashboardHeader.tsx
│   ├── MetricsGrid.tsx
│   ├── RecentActivityFeed.tsx
│   └── QuickActionsBar.tsx
├── hooks/
│   └── use-dashboard-data.ts       ← extracted data fetching
├── api.ts                          ← API calls
├── types.ts                        ← extracted types
└── index.ts                        ← re-exports for the page
```

**Why:** Rule 1 (file ≤ 300 lines), Rule 6 (Single Responsibility), Rule 15 (cohesion).

### 2. Cross-feature component duplication

**Symptom:** The same `Button.tsx` (or `Modal.tsx`, `Card.tsx`, …) exists in three feature folders, each slightly different.

**Restructure proposal:**
1. Read all copies, identify the canonical version (most-used, most-complete, least-buggy)
2. Promote it to `ui/Button.tsx` (or `components/Button.tsx`)
3. Delete the duplicates
4. Rewrite imports across the codebase

**Why:** Rule 8 (DRY) — duplication is the root of inconsistency bugs.

### 3. Co-located vs. shared — when to promote

Co-location (`PageX.tsx` next to `PageX.helpers.ts` next to `PageX.types.ts`) is a strength when the helpers serve only that page. It becomes a problem when the helpers start being imported from elsewhere.

**Heuristic:**
- Used by 1 caller → keep co-located
- Used by 2 callers in the same feature → keep co-located in that feature
- Used by callers across features → promote to `ui/`, `lib/`, or `hooks/` (whichever fits its kind)

### 4. The `components/` swamp

**Symptom:** `src/components/` has 80+ files; finding anything requires Ctrl-F; the same domain has 6 components scattered across alphabetical neighbors.

**Restructure proposal:**
- Bucket components by domain: `auth*.tsx` → `features/auth/components/`, `billing*.tsx` → `features/billing/components/`
- Keep truly cross-cutting components in `ui/` (Button, Input, Modal, etc.)

### 5. Hooks scattered everywhere

**Symptom:** `useAuth` in `hooks/`, `useBillingPlans` in `pages/billing/`, `useUser` in `lib/`, `useNotifications` inlined in a component.

**Restructure proposal:**
- Per-feature hooks → `features/<feature>/hooks/`
- Truly cross-cutting hooks → `hooks/` (or `lib/hooks/`)
- Inlined hooks → extract to `features/<feature>/hooks/use-<thing>.ts`

### 6. State scattered: store / context / signal everywhere

**Symptom:** `stores/userStore.ts`, but also a `UserContext.tsx` in `components/`, plus `useUserSignal.ts` in `hooks/`, all wrapping the same data.

**Restructure proposal:**
- Per-feature state → `features/<feature>/store.ts`
- Truly global state (auth, theme, locale) → `stores/` or `app/providers/`
- Eliminate redundancy — pick one mechanism per concern

## Frontend-specific principles

### Routes / pages / layouts must stay thin

The file that maps to a URL (`page.tsx`, `+page.svelte`, `route.tsx`) is presentation. It composes; it doesn't compute. Anything beyond:
- fetching data
- passing it to components
- rendering layout
- handling routing-level concerns

…belongs in `features/` or `lib/`. A page over 40 lines is usually a smell.

### The design system is a first-class folder

Whether you call it `ui/`, `design-system/`, `components/primitives/`, or have a separate package, primitives (Button, Input, Modal, Card) deserve their own home. Keep them framework-only — no domain knowledge, no business logic, no API calls.

### Styles follow the component, not the global pile

- CSS Modules: `Button.tsx` + `Button.module.css` co-located
- Styled-components / Emotion / CVA: in-file or sibling
- Tailwind: classes inline; truly global utilities in `styles/` or `app/globals.css`
- Avoid: a single mega `styles.css` with selectors targeting deep nested elements

### Feature folder vs page folder

These often overlap. The clearest split:
- **`pages/` or `app/`** — what the user sees (URL → page → composed components)
- **`features/`** — the building blocks of those pages (components, hooks, state, API per domain)

A page imports from a feature, never the reverse. If a feature imports a page, the boundary has been crossed.

## See also

- `folder-structure-principles.md` — the universal principles (cohesion, change-together, catch-all caution)
- `framework-hints.md` — typical layouts per framework (consult only when the project's own style is ambiguous)
- `before-after-clean-code.md` at the project root — full case study of a clean split using barrel re-exports
- Martin, *Clean Code* ch. 10 (Classes), ch. 11 (Systems)
- Mayer, *The Art of Clean Code* Principle 8 (Least Surprise) — applies strongly to UI folder layout
