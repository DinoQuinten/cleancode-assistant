# Before / After — `/cleancode:restructure` worked examples

Three real scenarios showing what the skill proposes and why. Use these as ground truth when adapting the skill to a new project.

---

## Example 1 — Frontend page-file bloat (Next.js App Router)

### Before

```
app/dashboard/
└── page.tsx                       (583 lines)
```

`page.tsx` mixes:
- 12 inlined sub-components (DashboardHeader, MetricsGrid, RecentActivityFeed, …)
- Two server actions inside the file
- A 90-line `useDashboardData` hook
- Inline data validation (zod schema)
- API helpers (`fetchMetrics`, `formatCurrency`)
- Component-local types

Detected conventions: project uses `src/features/<name>/` pattern (auth/, billing/ already exist), naming is PascalCase for components, hooks use `use-*.ts` kebab-case.

### Restructure plan

```
| # | Source                                          | Destination                                       | Why                                          |
|---|-------------------------------------------------|---------------------------------------------------|----------------------------------------------|
| 1 | app/dashboard/page.tsx (lines 45-93)            | src/features/dashboard/components/Header.tsx      | UI block belongs in feature components       |
| 2 | app/dashboard/page.tsx (lines 95-180)           | src/features/dashboard/components/MetricsGrid.tsx | UI block belongs in feature components       |
| 3 | app/dashboard/page.tsx (lines 182-265)          | src/features/dashboard/components/Activity.tsx    | UI block belongs in feature components       |
| 4 | app/dashboard/page.tsx (lines 267-330)          | src/features/dashboard/components/Actions.tsx     | UI block belongs in feature components       |
| 5 | app/dashboard/page.tsx (lines 332-422)          | src/features/dashboard/hooks/use-data.ts          | Data-fetching hook belongs in feature/hooks  |
| 6 | app/dashboard/page.tsx (lines 424-478)          | src/features/dashboard/api.ts                     | API calls belong in feature/api              |
| 7 | app/dashboard/page.tsx (lines 480-535)          | src/features/dashboard/types.ts                   | Types belong in feature/types                |
| 8 | app/dashboard/page.tsx (lines 538-560)          | src/features/dashboard/lib/format.ts              | Formatting helper belongs in feature/lib     |
| 9 | NEW                                             | src/features/dashboard/index.ts                   | Barrel re-export of feature public API       |
```

After: `app/dashboard/page.tsx` shrinks to ~30 lines (route + composition).

### Imports affected

- 0 external callers of the page (it's a route, not imported)
- Internal: page.tsx now imports from `@/features/dashboard` via barrel

### Citations

- Rule 1 (file ≤ 300 lines) — original is 583 lines
- Rule 6 (Single Responsibility) — page mixed 4+ concerns
- Rule 15 (cohesion + feature folders) — project already established `features/<name>/` pattern; this aligns
- Martin, *Clean Code* ch. 11 (Systems — separation of concerns)
- Frontend pattern reference: page-file bloat is the most common frontend debt

---

## Example 2 — Backend fat route handler (SvelteKit)

### Before

```
src/routes/api/projects/+server.ts    (286 lines)
```

`+server.ts` mixes:
- HTTP method exports (`GET`, `POST`, `PUT`, `DELETE`)
- 6 SQL queries (raw `sql` template literals)
- 3 business rules (slug normalization, project-existence checks, cascade-delete logic)
- Input validation (manual `if/throw error(400)` chains)
- Response formatting

Detected conventions: layered backend pattern, existing folders are `src/lib/server/{db,services,repositories}/`, naming uses kebab-case files with `*-service.ts` / `*-repository.ts` suffixes.

### Restructure plan

```
| # | Source                                         | Destination                                                 | Why                                              |
|---|------------------------------------------------|-------------------------------------------------------------|--------------------------------------------------|
| 1 | +server.ts (business rules block)              | src/lib/server/services/projects/project-service.ts         | Business rules don't belong in route handler     |
| 2 | +server.ts (SQL queries block)                 | src/lib/server/repositories/project-repository.ts           | Data access should be isolated (SRP, DI)         |
| 3 | +server.ts (slug normalization)                | src/lib/server/services/projects/project-normalization.ts   | Pure utility, single responsibility              |
| 4 | +server.ts (validation block)                  | src/lib/server/services/projects/project-validator.ts       | Validation is a service concern                  |
| 5 | +server.ts (DTO mappers)                       | src/lib/server/services/projects/project-row-mapper.ts      | Row → DTO mapping is repository-adjacent         |
| 6 | NEW                                            | src/lib/server/services/projects/index.ts                   | Barrel re-export of public API                   |
```

After: `+server.ts` shrinks to ~40 lines (parse → call service → format response).

### Imports affected

- 7 files import `ProjectService` and `ProjectRepository` from old paths → all rewritten to `@/lib/server/services/projects`
- Tests in `tests/projects/*.test.ts` reference old paths → rewritten

### Citations

- Rule 1 (file size), Rule 6 (SRP), Rule 7 (Interfaces — `IProjectRepository` extracted)
- Rule 15 (cohesion at module level)
- Martin, *Clean Code* ch. 10 (Classes), ch. 11 (Systems)
- This pattern is documented in `before-after-clean-code.md` at the project root

---

## Example 3 — Cross-feature component duplication (React + Vite)

### Before

```
src/features/billing/Button.tsx         (78 lines, with billing-specific styling)
src/features/auth/Button.tsx            (62 lines, simpler variant)
src/features/orders/Button.tsx          (95 lines, with loading state)
```

Three near-identical buttons exist in three feature folders, each slightly diverged. They serve the same user goal but have drift.

Detected conventions: `src/ui/` exists with primitives (Input, Modal, Card) — Button just isn't there yet. Naming PascalCase. Project uses `clsx` + Tailwind.

### Restructure plan

```
| # | Source                                  | Destination                | Why                                                   |
|---|-----------------------------------------|----------------------------|-------------------------------------------------------|
| 1 | src/features/orders/Button.tsx          | src/ui/Button.tsx          | Most complete variant becomes canonical               |
| 2 | src/features/billing/Button.tsx         | DELETE                     | Duplicate (Rule 8 DRY)                                |
| 3 | src/features/auth/Button.tsx            | DELETE                     | Duplicate (Rule 8 DRY)                                |
| 4 | src/ui/Button.tsx                       | (merge billing styles via variant prop)             | Preserve all variants from the 3 originals            |
```

### Imports affected

- 8 files import `from '@/features/billing/Button'` → rewritten to `'@/ui/Button'`
- 5 files import `from '@/features/auth/Button'` → rewritten
- 12 files import `from '@/features/orders/Button'` → rewritten

### Citations

- Rule 8 (DRY) — duplication is the source of inconsistency bugs
- Rule 15 (cohesion + ui/ design system pattern already established)
- Frontend pattern reference: cross-feature component duplication
- Martin, *Clean Code* ch. 12 (Emergence — No Duplication)

---

## What plans look like when the skill chooses NOT to move

Sometimes the answer is "leave it alone". The skill should be honest about this. Examples:

- A 280-line file is below the 300-line threshold — no split needed
- A `utils/` folder with 4 truly generic helpers (debounce, formatDate, assertNever, exhaustiveCheck) — that's the right size
- Co-located helpers used by exactly one component — keep them next to it
- A hook used only inside one feature — it's already in the right place

The skill should output:

```
## Restructure scan — <target>

No changes proposed. Findings:
- N files, all within size thresholds
- Folder structure matches project conventions (<package-by-feature|layered>)
- No cross-folder duplication detected
- No catch-all folders growing unmanageably

If you want to force-restructure anyway (e.g., move from layered to feature-folders), invoke with `/cleancode:restructure --strategy=feature-folders` and provide a target structure.
```
