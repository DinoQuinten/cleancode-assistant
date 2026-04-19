---
name: restructure
description: Extract misplaced code from any folder (backend or frontend) and move it to a properly-named folder that fits this project's existing conventions. Plan-first - reads the codebase to infer style, proposes a move-plan grounded in clean-code principles (Rule 15, Martin ch 11, McConnell ch 5), waits for a single confirmation, then moves files + rewrites imports atomically with git-aware history preservation. Handles backend layouts (services, repositories, controllers, route handlers), frontend layouts (components, pages, features, hooks, stores, ui/design-system), and mixed monorepos. Auto-chains from /cleancode:rewrite when a file split would benefit from cross-folder relocation. Triggers on phrases like "restructure my project", "move this code to a proper folder", "extract this from routes/", "my routes folder is doing too much", "where should this code live", "reorganize my folders", "split this across modules", "extract feature folder", "move business logic out of pages/components", "promote this shared code", or /cleancode:restructure.
argument-hint: "[target folder, default=current dir]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 0.4.0
---

# Clean Code Restructure

Move misplaced code into folders that fit **this project's** existing conventions. Plan-first, single-confirmation, with full rollback on failure.

This is the only cleancode skill that touches the directory tree. Every other skill (`/refactor`, `/rewrite`, `/structure`) operates within existing files. `/restructure` exists because Rule 15 (Clean Module & Folder Structure) needs an active fixer that respects the project's domain — it can't be auto-applied silently.

## Core principle

**Read the codebase first, then propose.** Never apply a generic framework rule without first matching it against what this project actually does. The `references/framework-hints.md` cheatsheet is consulted for priors only when the codebase is genuinely ambiguous (new project, no clear pattern yet).

## Triggers

"restructure my project" · "reorganize folders" · "move this code to a proper folder" · "extract this from routes/" · "my `routes/` folder is doing too much" · "where should this code live" · "split this across modules" · "extract a feature folder" · "promote this shared component" · "move business logic out of `pages/`" · "my page file is too big" · "this component is duplicated across features" · `/cleancode:restructure [folder]`.

## Workflow

### 1. Discover the project's conventions

Before proposing anything, build a picture of how this project is organised. In parallel:

- `Glob` `**/*` (skip `node_modules`, `dist`, `build`, `.git`, `.next`, `.nuxt`, `.svelte-kit`, `.turbo`, `coverage`, `__pycache__`, `.venv`, `vendor`)
- `Glob` `package.json`, `requirements.txt`, `Gemfile`, `go.mod`, `Cargo.toml`, `pom.xml`, `composer.json`, `pyproject.toml`, `*.csproj` to identify language + ecosystem
- `Glob` framework config files (`next.config.*`, `nuxt.config.*`, `svelte.config.*`, `astro.config.*`, `vite.config.*`, `angular.json`, `nest-cli.json`, `Gemfile`, `manage.py`, `pom.xml`) — these are *hints*, not commands
- `Glob` for barrel files: `**/index.{ts,tsx,js,jsx}` — they reveal the project's intended public APIs
- Sample 5–10 representative files from each top-level folder via `Read` (limit 50 lines each) to infer the **kind** of content each folder contains

From this, identify:

| Question | Why it matters |
|---|---|
| Top-level shape: package-by-feature (`features/auth/`, `features/billing/`) or package-by-layer (`components/`, `services/`, `hooks/`)? | Proposals must match the existing pattern. Don't impose features/ on a layered project, or vice versa. |
| File naming convention: `kebab-case.ts`, `PascalCase.tsx`, `.service.ts` / `.repository.ts` suffixes? | New files we create must match. |
| Are barrel `index.ts` files present? Where? | Indicates intentional public APIs — preserve them with re-exports. |
| What does this project actually call its folders? (`lib/` vs `utils/`, `routes/` vs `pages/`, `ui/` vs `components/`) | Use the project's vocabulary in proposals. |
| Is this a monorepo? (`apps/`, `packages/`, `pnpm-workspace.yaml`, `turbo.json`) | Each subtree may have its own conventions; treat them independently. |

If discovery returns nothing useful (very small project, brand-new repo), consult `references/framework-hints.md` for priors and **say so explicitly** in the plan: *"Project is too new to infer conventions — using <framework> defaults from cheatsheet."*

### 2. Classify the target

For the user's target (a folder, or the whole project if they didn't specify), Read each file and bucket it by **what the code actually does**. File extension is a hint; content is the truth.

Kinds:
- **Page** — declares a route (Next.js `page.tsx`, SvelteKit `+page.svelte`, Remix `route.tsx`); user-visible screen
- **Route handler** — server-only HTTP handler (`+server.ts`, `route.ts`, Express handler, Rails controller action)
- **Controller** — orchestrates request → service → response (NestJS controller, Spring `@RestController`)
- **Service** — business logic, transactions, orchestrates repositories
- **Repository / DAO** — data access only; talks to DB, ORM, or external API
- **Domain model / entity** — pure data shape with rules (no I/O)
- **Component** — UI element (React/Vue/Svelte/Angular component)
- **Layout** — page/screen scaffolding (`layout.tsx`, `+layout.svelte`)
- **Hook / composable / use-* function** — reactive UI logic
- **Store / context / signal** — UI state container
- **API client / fetcher** — frontend code that calls backend
- **Util / helper** — pure cross-cutting helpers
- **Type / interface** — type-only declaration
- **Style** — CSS/SCSS/Tailwind/CSS-in-JS extracted styles
- **Test** — unit / integration / e2e
- **Config** — env, settings, build config

### 3. Detect misplacements

A file is misplaced when **any** of these hold:

- It violates Rule 15 (Clean Module & Folder Structure):
  - Business logic inside a presentation layer (route handler, page, component)
  - Repeated cross-folder duplicates (e.g., the same `Button.tsx` copied into 3 feature folders)
  - Catch-all dump (`utils/`, `helpers/`, `common/`, `shared/`) accumulating dozens of unrelated files
  - Domain mixing (auth code scattered across `controllers/`, `services/`, `models/`, `routes/` with no `auth/` folder consolidating it)
- It breaks the project's own observed conventions (see §1)
- It exceeds size/cohesion thresholds that call for a split into multiple files in different folders (Rules 1, 6 — Single Responsibility)

Cite the specific principle for each finding (Rule 15, Martin ch 10/11, McConnell ch 5/6, or the Mayer principle).

### 4. Propose the move-plan

Output the plan in this exact format:

```
## Restructure plan — <target>

### Detected conventions
- Style: <package-by-feature | package-by-layer | mixed>
- Naming: <kebab-case | PascalCase | mixed>
- Barrel files: <yes/no, location>
- Framework signals: <Next App Router | SvelteKit | Express | none / new project>

### Proposed moves (N files)

| # | Source | Destination | Why |
|---|---|---|---|
| 1 | `routes/api/projects/+server.ts` (lines 45-180, the service block) | `src/lib/server/services/projects/project-service.ts` | Business logic doesn't belong in a route handler (Rule 15, Martin ch 11) |
| 2 | `routes/api/projects/+server.ts` (lines 200-260, DB queries) | `src/lib/server/repositories/project-repository.ts` | Data access should be isolated (SRP, Martin ch 10) |
| 3 | `src/features/billing/Button.tsx` | DELETE — duplicate of `src/ui/Button.tsx` | Cross-folder duplication (Rule 8 DRY) |

### Imports affected
- 7 files reference `routes/api/projects/+server.ts` exports → all rewritten
- 12 files reference `src/features/billing/Button.tsx` → rewritten to `src/ui/Button.tsx`

### Barrel re-exports proposed
- `src/lib/server/services/projects/index.ts` (NEW) re-exports `ProjectService` so callers needn't change deep imports

### Rollback strategy
- Git repo detected → all moves via `git mv`; rollback = `git restore -SW .`
- Or: non-git → backup before each move; manual rollback instructions provided

Apply this plan? [y/N]
```

### 5. Single confirmation

Wait for user response. **Do nothing** if they say no, ask questions, or want to amend the plan. If they amend, regenerate the plan and re-confirm.

### 6. Execute atomically

Order of operations:

1. **Pre-flight checks**
   - Confirm `.git/` exists (or user passed `--force-non-git`)
   - Confirm no destination paths already exist (no overwrites)
   - Confirm working tree is clean (or warn loudly that uncommitted changes exist)
2. **Move files**
   - Git repo: `git mv <source> <destination>` for each
   - Non-git: `mv <source> <destination>`; record originals for rollback
3. **Rewrite imports**
   - Use `Grep` to find every reference to the old path
   - Use `Edit` to replace each import string (only static `import` / `from` / `require` / `export … from` patterns)
   - Skip and report dynamic imports (`import(variable)`, string-concat paths) for manual review
4. **Create barrel files** (if proposed)
5. **Verify atomic completion** — if any step failed, abort and rollback

On any failure: `git restore -SW .` (git repo) or restore from backup (non-git), then report which step failed and why.

### 7. Verify

After successful execution:

- If `tsconfig.json` exists: run `npx tsc --noEmit` and report
- If `package.json` has `scripts.typecheck`: run `npm run typecheck` and report
- If `package.json` has `scripts.test`: suggest the user run it (don't run automatically — tests can be slow)
- If neither: suggest `/cleancode:analyze <target>` to verify no new violations

Print final summary:

```
✓ Moved N files
✓ Rewrote M imports across K files
✓ Created J barrel re-exports
✓ Type check: PASSED | FAILED (details)
Suggested next: npm test, /cleancode:analyze <target>, /cleancode:health
```

## Ground rules

- **Always read the codebase first.** Never propose moves based on cheatsheet alone.
- **NEVER move a file without explicit user confirmation.**
- **NEVER use `rm`.** Only `git mv` (git repo) or `mv` (fallback). Files must end up at their destination — no deletions.
- **If any import rewrite fails, abort the whole batch.** Roll back via `git restore -SW .` or restored backup. Report the failed file and let the user decide.
- **Prefer barrel re-exports** when a file's public API is imported from many places — preserves callers, avoids touching every file.
- **Respect the project's existing style.** If it uses `features/<name>/`, propose into feature folders. If it's layered, match the layers. Don't impose a style the project isn't already using.
- **Skip dynamic imports.** Only rewrite static `import x from '...'`, `require('...')`, `export … from '...'` patterns. List dynamic imports and string-concat paths in the report for manual review.
- **Per-subtree detection in monorepos.** A repo with `apps/web/` + `apps/api/` gets two independent restructuring contexts.
- **Cite the principle for every move.** Reference Rule 15, Martin chapter, or McConnell chapter so the user understands the *why*.
- **Don't fight the language.** Go's flat packages, Rails' MVC, Java's `src/main/java/com/...` are conventions for a reason. See `references/framework-hints.md`.

## When `/cleancode:rewrite` chains here

`/rewrite` invokes `/restructure` when its split-plan reveals files that belong elsewhere. In that case:
- The chain provides the specific files and proposed destinations as input.
- Skip the discovery step (already done by `/rewrite`).
- Go directly to step 4 (propose move-plan) with the inherited context.

## What this skill does NOT do

- Rename files within their existing folder (use `/cleancode:refactor` or `/cleancode:rewrite`)
- Apply design patterns (Strategy/Factory/Command/State) within a class (use `/cleancode:structure`)
- Fix in-file violations (long functions, deep nesting, bad names) (use `/cleancode:refactor` / `/cleancode:rewrite`)
- Touch dependencies, build configs, or CI files
- Move tests independently — tests follow the code they test

## Reference files

- `references/folder-structure-principles.md` — distilled from Martin / McConnell / Mayer + Rule 15
- `references/frontend-patterns.md` — feature folders, atomic design, page-file bloat, co-location vs promotion, hooks/stores placement
- `references/backend-patterns.md` — layered, hexagonal, feature modules, catch-all antipatterns
- `references/framework-hints.md` — cheatsheet for SvelteKit / Next / Remix / Nuxt / Astro / NestJS / Express / Rails / etc.; consulted only when the project's own style is ambiguous
- `examples/before-after-restructure.md` — three worked examples (Next.js page-file bloat, SvelteKit fat route handler, React cross-feature duplication) showing exactly what the skill proposes and how it cites the rules
