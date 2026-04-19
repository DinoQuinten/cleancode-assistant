# Folder Structure Principles

Distilled from the cleancode plugin's source books. Use these as the *why* behind every move proposed by `/cleancode:restructure`.

## The five rules of folder design

### 1. The folder tree is documentation

A first-time reader should be able to guess what a project does from top-level folder names alone.

- ❌ `src/`, `lib/`, `utils/` — tells you nothing about the system
- ✓ `auth/`, `billing/`, `orders/` — domain is obvious; new contributor knows where to look

> *"The folder tree should read like a table of contents."*
> — cleancode Rule 15

> *"A system should be composable from cohesive components, each of which has a clear name."*
> — Martin, *Clean Code* ch. 11 (Systems)

### 2. Group by what changes together

Files that are edited in the same PRs, touched by the same team, or owned by the same feature usually want to sit in the same folder — regardless of whether they're "types", "services", or "components" underneath.

This is the **cohesion** test. If two files always change together, splitting them across `services/` and `models/` and `controllers/` adds friction without separating any concern.

> *"The proper organization for classes is one in which classes that change together are placed together."*
> — Martin, *Clean Code* ch. 10 (Classes — Organizing for Change)

> *"Information hiding is one of the most important design heuristics."*
> — McConnell, *Code Complete* ch. 5 (Design in Construction)

### 3. Cohesion beats convention

Technical-layer folders (`controllers/`, `services/`, `models/`, `repositories/`) are fine for small projects where there are only a few of each. They become painful as the project grows — unrelated domains pile up in the same folder, and changing one feature touches files in 4 directories.

When that happens, switch to **domain-first**:

```
Before (layered, breaking)             After (domain-first)
src/                                   src/
├── controllers/                       ├── auth/
│   ├── auth.ts                        │   ├── controller.ts
│   ├── billing.ts                     │   ├── service.ts
│   └── orders.ts                      │   └── repository.ts
├── services/                          ├── billing/
│   ├── auth.ts                        │   ├── controller.ts
│   ├── billing.ts                     │   ├── service.ts
│   └── orders.ts                      │   └── repository.ts
└── repositories/                      └── orders/
    ├── auth.ts                            ├── controller.ts
    ├── billing.ts                         ├── service.ts
    └── orders.ts                          └── repository.ts
```

Both are valid. The second wins as soon as the team starts working on multiple domains in parallel.

### 4. Be skeptical of catch-all folders

`utils/`, `helpers/`, `common/`, `misc/`, `shared/`, `lib/` — when these grow, they're usually a symptom: code landed there because no one knew where else to put it.

A small `utils/` with 3 genuinely generic files (`debounce`, `formatDate`, `assertNever`) is fine. A `utils/` with 47 files is a missing domain folder.

> *"Functions should do one thing. Modules should do one thing. Catch-all packages do many things badly."*
> — paraphrasing Martin, *Clean Code* ch. 3 + 11

When restructuring a catch-all:
1. Read every file in it
2. Bucket by what it actually serves (`auth/utils.ts`, `billing/utils.ts`, …)
3. Move each into its real home
4. Delete the catch-all, or leave only the truly generic 2–3 files

### 5. Size shapes structure

Right structure scales with the codebase:

| Size | Right structure |
|---|---|
| < 30 files (script, CLI tool) | **Flat.** No folders. Reading time wins. |
| 30 – 300 files (small app, library) | **Layered or shallow domain.** A few top-level folders; one level of nesting. |
| 300 – 3,000 files (typical SaaS app) | **Domain-first.** `auth/`, `billing/`, `orders/`, each with internal layering as needed. |
| 3,000 – 10,000 files (large monorepo, multiple products) | **Bounded contexts.** Workspace packages, nested domains, possibly hexagonal architecture. |

Pre-emptively imposing a 5,000-file structure on a 50-file project just creates ceremony. Pre-emptively staying flat in a 5,000-file repo creates chaos.

## How to apply during restructuring

When `/cleancode:restructure` proposes moves, every move should be defensible against these five rules:

| Rule | The question every move must pass |
|---|---|
| 1. Tree is documentation | Does the new location's name reveal what's inside? |
| 2. Group by change | Will these files actually change together? |
| 3. Cohesion beats convention | Are we mixing unrelated domains in the same folder? |
| 4. Skeptical of catch-alls | Are we adding to a `utils/`/`helpers/`/`shared/` pile? |
| 5. Size shapes structure | Is this structure proportional to the codebase? |

If a proposed move can't answer all five, it's not a good move.

## When NOT to restructure

Restructuring has a real cost: stale PRs become merge-conflicted, IDE bookmarks break, `git blame` becomes a chain of moves, mental models invalidate.

Don't restructure when:
- The codebase is small enough that flat is fine
- The team is mid-sprint with many open PRs
- Imports are heavily dynamic (path strings constructed at runtime — risk of breaking silently)
- The proposed structure isn't a clear win — small improvements rarely justify the disruption

A good restructure should pass the *one-week test*: a week from now, does the team feel like the codebase got noticeably easier to work in?

## See also

- Martin, *Clean Code* ch. 10 (Classes), ch. 11 (Systems), ch. 12 (Emergence)
- McConnell, *Code Complete 2nd Ed.* ch. 5 (Design in Construction), ch. 6 (Working Classes)
- Mayer, *The Art of Clean Code* ch. 2 (Focus), Principle 8 (Principle of Least Surprise)
- cleancode plugin Rule 15 (`skills/init/references/rules.md` lines 169–191)
- `before-after-clean-code.md` at the project root — real-world case study of a 485-line monolith split into 4 cohesive modules with barrel re-exports
