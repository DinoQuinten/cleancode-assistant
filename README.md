# DinoQuinten's Claude Code plugins

A multi-plugin [Claude Code marketplace](https://docs.claude.com/en/docs/claude-code/plugins). Each plugin ships independently and is versioned on its own cadence.

## Plugins

| Plugin | Version | What it does |
|---|---|---|
| [`cleancode`](#cleancode) | `v0.3.0` | 15 plain-language clean-code rules with auto-fix for silent errors, method chains, messy tests, long functions, folder structure, and more |
| [`system-and-database-design`](#system-and-database-design) | `v0.1.0` | Architect and database-design coach grounded in DDIA, *Fundamentals of Software Architecture*, and Kimball's *Data Warehouse Toolkit* — produces design docs, Mermaid / Excalidraw / DBML diagrams, and architecture reviews |

## Install

From Claude Code, add the marketplace once:

```
/plugin marketplace add DinoQuinten/claude-plugins
```

Then install either (or both) plugins:

```
/plugin install cleancode@claude-plugins
/plugin install system-and-database-design@claude-plugins
```

---

## `cleancode`

A Claude Code plugin that enforces clean code principles across your entire project and **actually fixes the code for you** — not just reports what's wrong. Locks in the same rules for Claude Code, Cursor, and Codex so every AI assistant follows the same standards from the first session onward.

**Plain language first.** Every rule is written so anyone — not just senior engineers — can follow it. The formal textbook name is in parentheses so experts still recognize it: "Don't Reach Through Objects (Law of Demeter)", "Check Inputs Early, Never Hide Errors (Fail Fast)".

Based on: *Clean Code: A Handbook of Agile Software Craftsmanship* (Robert C. Martin), *Code Complete 2nd Ed.* (McConnell), *The Art of Clean Code* (Mayer), *OOP vs. Functional Programming*.

**15 plain-language rules, 13 skills, 1 background reviewer, and 2 hooks.**

| Skill | Command | What it does |
|---|---|---|
| **Init** | `/cleancode:init` | Sets up clean code rules for your project — generates `.cleancode-rules.md`, `CLAUDE.md`, `.cursorrules`, `AGENTS.md` |
| **Analyze** | `/cleancode:analyze [file]` | Scans code for violations — file length, function length, nesting, naming, missing interfaces |
| **Rewrite** | `/cleancode:rewrite [file]` | Produces a clean version of messy code, preserving all behavior |
| **Teach** | `/cleancode:teach [rule]` | Explains any clean code principle with a book citation and example |
| **Setup Platform** | `/cleancode:setup [cursor\|codex\|all]` | Writes platform-native config files from `.cleancode-rules.md` |
| **Refactor** | `/cleancode:refactor [file] [name]` | Applies one named refactoring (Extract Function, Replace Switch with Table, Guard Clauses, Strategy, …) |
| **Test** | `/cleancode:test [file] [fix]` | Flags tests missing Arrange / Act / Assert, bad names, multi-assertion bodies; `fix` rewrites them |
| **Untangle** | `/cleancode:untangle [file] [fix]` | Finds `a.b().c().d()` chains and god-class imports; `fix` introduces helper methods |
| **Safety** | `/cleancode:safety [file] [fix]` | Finds empty catches, missing guards, division without zero-check; `fix` adds guard clauses and surfaces errors |
| **Structure** | `/cleancode:structure [file] [fix]` | Suggests Strategy / Command / Factory / State patterns when they'd help; `fix` applies them |
| **Todo** | `/cleancode:todo [scan\|add\|list\|close]` | Tracks known clean-code issues in `.cleancode-todo.md` at project root |
| **Health** | `/cleancode:health [save]` | Project-wide dashboard with a Cleanliness Score out of 100 — read only |
| **Fix** | `/cleancode:fix [file] [critical-only\|all]` | One-shot: runs analyze, then delegates to each fixer skill in severity order |

**Auto-runs on every project open** — the `SessionStart` hook checks for `.cleancode-rules.md` and prompts to initialize if missing.

**Background reviewer** — the `cleancode-reviewer` agent silently checks all code Claude writes and appends non-blocking suggestions.

**Report or fix, your choice.** Every detection skill defaults to a report. Add `fix` to apply changes. The reviewer agent stays read-only — nothing is ever rewritten without an explicit `/cleancode:*` command.

Full details, rule list, language support, and troubleshooting live in the plugin's own docs at [tag `v0.3.0`](https://github.com/DinoQuinten/claude-plugins/blob/v0.3.0/README.md).

---

## `system-and-database-design`

A Claude Code plugin that helps you design real-world software architecture and databases. Ships with 39 curated reference chunks distilled from three canonical texts:

- **Designing Data-Intensive Applications** (Kleppmann) — data systems, consistency, replication, partitioning
- **Fundamentals of Software Architecture** (Richards & Ford) — architecture styles, characteristics, fitness functions
- **The Data Warehouse Toolkit** (Kimball) — dimensional modeling, star schemas, SCDs

…plus authored chunks covering topics the books don't: API design, observability, security, ML/AI serving, real-time systems, compliance. **You do not need the source books.** Zero setup — no dependencies, no downloads, no build step.

| Skill | Command | What it does |
|---|---|---|
| **Design System** | `/design-system <requirement>` | Full design doc with components, trade-offs, and capacity math |
| **Design Database** | `/design-database <domain>` | Schema recommendation (SQL or NoSQL) with ER-style breakdown |
| **Review Architecture** | `/review-architecture <path or text>` | Critique via fitness functions and checklists (scale, security, reliability, compliance, anti-patterns) |
| **Diagram** | `/diagram <desc> --format=mermaid\|excalidraw\|dbml` | Generates diagrams in your tool of choice |
| **Design Principles** | *(auto-triggered)* | Kicks in when you mention CAP, consistency, sharding, consensus, etc. |

A lightweight `SessionStart` hook announces the plugin at the start of each session.

Full details in [`system-and-database-design/README.md`](./system-and-database-design/README.md).

---

## License

MIT — see [LICENSE](./LICENSE).
