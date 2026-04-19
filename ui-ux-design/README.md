# ui-ux-design (`uix`)

A UI/UX design coach plugin for Claude Code. Grounds Claude in eight foundational design books plus WCAG 2.2, and turns that knowledge into actionable skills you invoke on demand.

## What it knows

| Source | Covers |
|---|---|
| Refactoring UI — Wathan & Schoger | Hierarchy, spacing, typography, color systems, depth |
| Don't Make Me Think (3rd ed.) — Krug | Usability laws, navigation, home-page rules, testing |
| Designing Interfaces (3rd ed.) — Tidwell, Brewer, Valencia | 50+ named UI patterns |
| UX for Beginners — Joel Marsh | Hick's/Fitts's/Miller's laws, motivation, IA, research |
| The Mom Test — Rob Fitzpatrick | How to talk to users without getting lied to |
| Change by Design — Tim Brown / IDEO | Design thinking, prototyping, 3 lenses |
| Interaction of Color — Albers | Color relativity, simultaneous contrast |
| Colour and Light — Hardin / Klarén / Arnkil | Light perception, shadows, surface modes |
| WCAG 2.2 | All four POUR principles + the nine new 2.2 criteria |

The complete distillation lives in `references/UI_MASTER_GUIDE.md`.

## Skills

All eight are user-invocable via `/uix:<skill>` and auto-activate on matching queries.

| Skill | What it does |
|---|---|
| `init` | Scaffolds `.uix-config.md` to activate the hooks in a project |
| `design-principles` | Explain/apply a core principle (hierarchy, spacing, scanning, laws) with book-grounded reasoning |
| `design-component` | Propose a component design using Tidwell patterns + Refactoring UI rules |
| `review-ui` | Audit an existing UI (file, URL, screenshot, description) against the master guide + WCAG 2.2 |
| `accessibility-audit` | Focused WCAG 2.2 AA audit with all nine new 2.2 criteria |
| `choose-pattern` | Recommend the right Tidwell interaction pattern for a problem |
| `color-system` | Build a full palette (greys + primary + accents) using Refactoring UI + Albers principles |
| `user-research` | Generate Mom-Test-compliant interview plans and analyze user-conversation notes |

## Hooks (auto-active on install — triggers ONLY on UI/UX work)

The plugin ships four hooks that **auto-activate the first time you open a UI/UX project** with the plugin installed — no manual init step, no Storybook dependency, no framework requirement. Works equally on React, Next, Vue, Nuxt, Svelte/SvelteKit, Angular, Solid, Astro, Qwik, Remix, Lit, plain HTML/CSS, and design-only repos.

### Strict triggering — three gates, all must pass

1. **Project gate** — `_project_detect.is_frontend_project()` runs before anything else. A project only qualifies if at least one of: (a) `package.json` declares a known frontend dependency, (b) a frontend framework config is present (`next.config.*`, `nuxt.config.*`, `vite.config.*`, `tailwind.config.*`, etc.), (c) an HTML entry file exists, (d) a `.tsx/.jsx/.vue/.svelte/.astro` file exists in a conventional UI directory (`src/`, `app/`, `components/`, `pages/`, `ui/`, `lib/`, `views/`, `screens/`, `widgets/`, `layouts/`, `routes/`), or (e) a design folder exists. **Pure backend, data-science, or infra repos see nothing from this plugin.**
2. **Opt-in gate** — `.uix-config.md` must exist (auto-scaffolded by `SessionStart` in qualifying projects). Set `enabled: false` inside to silence everything.
3. **Content gate** — for `UserPromptSubmit`: prompt must contain a hard UI keyword (`tsx`, `react`, `button`, `tailwind`, `figma`, …) or a design-implementation phrase (`build a login page`, `implement this figma`, …), AND must not be dominated by backend context (`database`, `schema`, `kafka`, `microservice`, `api design`, `sql`, `docker`, `terraform`, …). For `PreToolUse`/`PostToolUse`: file extension must be one of `.tsx .jsx .vue .svelte .astro .html .css .scss .sass .less .styl .mdx`.

Verified strict: 17/17 test cases pass — fires on every real UI task, silent on every backend / data / infra false-positive.

A `SessionStart` hook scaffolds a `.uix-config.md` marker at the project root from a bundled template; the other three hooks then read settings from that file on every event.

**To opt out of a project:** open `.uix-config.md` and set `enabled: false`. (Just deleting the file isn't opt-out — `SessionStart` re-creates it. This is intentional: the file is the config surface.) To remove entirely, uninstall the plugin.

| Event | Matcher | What it does |
|---|---|---|
| `SessionStart` | `*` | First session: scaffolds `.uix-config.md`. Every session: scans the project for design assets (`design/`, `mockups/`, `wireframes/`, `figma/`, `*.fig`, `*.sketch`, `*.xd`, `*.psd`, plus images inside design folders) and announces them so Claude knows to read them when implementing. |
| `UserPromptSubmit` | `*` | Detects UI/UX intent in the user's prompt — including phrases like "implement this design", "build this mockup", "from this Figma" that don't even mention a UI keyword — and injects a reminder pointing Claude at the `uix` skills, the component-reuse check, **and the list of detected design assets in the project**. |
| `PreToolUse` | `Write\|Edit` | Before Claude writes or edits a frontend file, reminds it to glob for existing reusable components (if the framework supports composition) and apply uix principles + WCAG 2.2 AA. |
| `PostToolUse` | `Write\|Edit` | After the file is written, runs a static validator that flags WCAG risks (missing alt, `outline:none`, positive tabindex, small targets, missing labels), design-system violations (inline hex, named CSS colors, `!important`, tiny fonts), and smells (files over 300 lines, motion without `prefers-reduced-motion`). |

**Design-asset detection** scans these locations (excluding `node_modules`, `dist`, `.git`, etc.):
- Folders: `design/`, `designs/`, `mockup/`, `mockups/`, `wireframe/`, `wireframes/`, `figma/`, `sketches/`, `.design/`, `design-system/`, `assets/design/`, `docs/design/`, `public/design/`, `src/assets/design/`, `src/design/`, `ui/design/`
- Native design files anywhere: `.fig`, `.sketch`, `.xd`, `.ai`, `.psd`, `.afdesign`
- Images **only inside** detected design folders: `.png`, `.jpg`, `.svg`, `.webp`, `.gif`, `.pdf` (so we don't list every favicon)

**File extensions watched:** `.tsx .jsx .vue .svelte .astro .html .css .scss .sass .less .styl .mdx`

**Severity tiers:** ❌ Critical (WCAG blocker) · ⚠ Warning (design-system violation) · ℹ Info (smell).

### Tuning per project

The `.uix-config.md` frontmatter lets you customize without restarting Claude Code:

```yaml
---
enabled: true                          # master kill switch
prompt_detect_enabled: true            # disable UserPromptSubmit
file_guard_enabled: true               # disable PreToolUse reminders
validator_enabled: true                # disable the validator
validator_severity_floor: info         # critical | warning | info
validator_exclude_rules:               # comma-separated rule IDs to skip
excluded_paths:                        # comma-separated globs (supports **)
---
```

Full rule catalog and examples live inside the scaffolded file itself.

> **Note:** Hooks load at session start, so adding/removing the `.uix-config.md` file takes effect on the next Claude Code session. Editing values *inside* the file takes effect on the next hook invocation.

## Installation

Clone `claude-plugins` and add this plugin directory to Claude Code, or install via your plugin marketplace of choice. Then in any Claude Code session:

```
/uix:design-principles hierarchy
/uix:review-ui @path/to/component.tsx
/uix:accessibility-audit @path/to/page.html
```

## License

MIT — Prasanna Anthony
