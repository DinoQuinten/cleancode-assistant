# cleancode — Clean Code Assistant Plugin (v0.3.0)

A Claude Code plugin that enforces clean code principles across your entire project and **actually fixes the code for you** — not just reports what's wrong. Locks in the same rules for Claude Code, Cursor, and Codex so every AI assistant follows the same standards from the first session onward.

**Plain language first.** Every rule is written so anyone — not just senior engineers — can follow it. The formal textbook name is in parentheses so experts still recognize it: "Don't Reach Through Objects (Law of Demeter)", "Check Inputs Early, Never Hide Errors (Fail Fast)".

Based on: *Clean Code: A Handbook of Agile Software Craftsmanship* (Robert C. Martin), *Code Complete 2nd Ed.* (McConnell), *The Art of Clean Code* (Mayer), *OOP vs. Functional Programming*.

---

## Features

**15 plain-language rules, 13 skills, 1 background reviewer, and 2 hooks.**

The **rules** are the standards (file size, function size, Law of Demeter, Fail Fast, folder structure, etc.) defined in `.cleancode-rules.md`. The **skills** are the commands you run (`/cleancode:analyze`, `/cleancode:fix`, `/cleancode:teach`, …). Multiple skills can enforce the same rule — e.g., Rule 12 (Fail Fast) shows up in `analyze`, `safety`, `fix`, and the background reviewer. Rule 15 (folder structure) is a **dynamic** rule — guidance that adapts to project size, language, and framework rather than a rigid template.

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
| **Todo** | `/cleancode:todo [scan\|add\|list\|close]` | Tracks known clean-code issues in `.cleancode-todo.md` at project root (team to-do list) |
| **Health** | `/cleancode:health [save]` | Project-wide dashboard with a Cleanliness Score out of 100 — read only |
| **Fix** | `/cleancode:fix [file] [critical-only\|all]` | One-shot: runs analyze, then delegates to each fixer skill in severity order |

**Auto-runs on every project open** — the `SessionStart` hook checks for `.cleancode-rules.md` and prompts to initialize if missing.

**Reminds Claude during plan mode** — the `UserPromptSubmit` hook detects when you're planning (plan-mode keywords, a recent plan file, or `EnterPlanMode` in the transcript) and injects a short reminder so clean-code thresholds factor into every plan. Coexists with other plugins' hooks — Claude Code merges and runs them in parallel.

**Background reviewer** — the `cleancode-reviewer` agent silently checks all code Claude writes and appends non-blocking suggestions.

**Report or fix, your choice.** Every detection skill (`test`, `untangle`, `safety`, `structure`) defaults to a report. Add `fix` to apply the changes. The reviewer agent stays read-only — nothing is ever rewritten without an explicit `/cleancode:*` command.

---

## Rationale for 13 skills (11 action + 1 knowledge + 1 orchestrator)

The skills split into four groups by purpose, so Claude (and you) always know which one to reach for.

**Knowledge (1):**
- `teach` — always-on reference for the 15 rules with book citations (including the dynamic folder-structure rule). Grounds Claude in shared vocabulary so every other skill can point at it without re-explaining the principle.

**Setup (2):**
- `init` — one-time project bootstrap. Writes `.cleancode-rules.md` + `CLAUDE.md`.
- `setup` — regenerates platform configs (`.cursorrules`, `AGENTS.md`) from the source of truth.

**Detect + fix (6, each with report/fix modes):**
- `analyze` — general scan across all 15 rules.
- `safety` — hidden errors and missing input checks (Rule 12).
- `untangle` — method chains and coupling (Rule 11).
- `test` — AAA, vague names, multi-assertion tests (Rule 14).
- `structure` — suggests Strategy / Command / Factory / State patterns when they'd help.
- `refactor` — applies one named refactoring (Extract Method, Replace Switch with Table, Guard Clauses, etc.).

**Whole-project (3):**
- `rewrite` — full cleaner rewrite of a single file.
- `todo` — persistent team backlog at `.cleancode-todo.md`.
- `health` — Cleanliness Score dashboard out of 100.

**Orchestrator (1):**
- `fix` — runs `analyze`, then delegates to each fixer in severity order. One command that cleans a file or project top-to-bottom.

This separation keeps each skill small and focused, while `fix` gives you a single entrypoint when you don't want to think about which fixer applies.

---

## Install

Claude Code:

```bash
/plugin marketplace add DinoQuinten/cleancode-assistant
/plugin install cleancode@cleancode-assistant
```

Codex CLI:

```bash
npx cleancode-codex init
```

Or point Claude Code directly at a local checkout:

```bash
claude --plugin-dir /path/to/cleancode-assistant
```

---

## Quick Start

Open any project and run:

```
/cleancode:init
```

This creates:
- `.cleancode-rules.md` — the source of truth (edit thresholds here)
- `CLAUDE.md` — rules for Claude Code
- `.cursorrules` — rules for Cursor
- `AGENTS.md` — rules for OpenAI Codex CLI

From then on, every session opens with:
```
cleancode active: 15 rules loaded from .cleancode-rules.md
```

---

## Rules (Defaults)

| Rule | Threshold | Severity |
|---|---|---|
| File length | > 300 lines | Critical |
| Function length | > 40 lines | Critical |
| Function length | > 20 lines | Warning |
| Parameter count | > 4 | Critical |
| Nesting depth | > 4 | Critical |
| Missing TS interface | Public class/service | Warning |
| Duplicated logic | > 3 lines | Warning |
| Reaching through objects (`a.b().c().d()`) | chain depth > 2 | Warning |
| Hidden errors (`catch {}`, `except: pass`) | any occurrence | Critical |
| Missing input check on a public function | no guard in first 3 lines | Warning |
| `if` / `for` / `while` inside a test body | any occurrence | Warning |
| Test name doesn't describe behavior | `test1`, `testIt`, no verb | Style |
| Folder structure (domain vs. layer, catch-all folders) | *dynamic* — context-dependent hint | Style |

To customize thresholds, edit `.cleancode-rules.md` in your project and re-run `/cleancode:setup all`.

**Dynamic rule** = guidance that adapts to the project's size, language, and framework. Rule 15 (folder structure) is the only dynamic rule so far — the plugin surfaces hints when signals accumulate (oversized catch-all folders, growing flat `src/`, etc.) rather than enforcing a universal template. No auto-fix, ever — folder moves ripple through imports and belong to humans who know the domain.

---

## Language Support

Works with all languages. TypeScript/JavaScript has additional interface enforcement.

- **TypeScript/JavaScript** — interfaces, type checking, test file exemptions
- **Python** — function/file length, naming
- **Java / C#** — SOLID, interface usage, method length
- **Go** — function length, naming conventions
- **Any other language** — file size, function size, naming, nesting

---

## The cleancode-reviewer Agent

After every code edit, this agent silently appends a non-blocking review:

```
---
🧹 Clean code review (non-blocking)
🔴 Critical
• auth.ts:47 — function `handleLogin` is 68 lines (limit: 40) → try: extract validateCredentials() and generateSession()
🟡 Warnings
• auth.ts:12 — class `AuthService` has no TypeScript interface → try: extract IAuthService
---
```

It never blocks or rewrites — only suggests. You decide what to act on.

---

## Skill Details

### `/cleancode:analyze`

```bash
/cleancode:analyze src/services/user.ts   # single file
/cleancode:analyze .                       # whole project
/cleancode:analyze                         # whole project (same)
```

Output: grouped report (🔴 Critical / 🟡 Warning / 🔵 Style) with line numbers and fix suggestions.

### `/cleancode:rewrite`

```bash
/cleancode:rewrite src/services/user.ts   # rewrite a file
```

Output: full rewrite preserving behavior + table showing what changed and why.

### `/cleancode:teach`

```bash
/cleancode:teach function-too-long
/cleancode:teach missing-interface
/cleancode:teach solid
/cleancode:teach                          # shows menu
```

### `/cleancode:setup`

```bash
/cleancode:setup cursor    # writes .cursorrules
/cleancode:setup codex     # writes AGENTS.md
/cleancode:setup all       # writes both + CLAUDE.md
```

### `/cleancode:refactor`

Applies **one** specific, well-known cleanup to a file — pull a block out into its own named function ("Extract Method"), turn a giant switch into a lookup table ("Replace Switch with Table"), swap a deep if/else for polymorphism, and so on. Different from `rewrite`: `refactor` is surgical, named, and shows the user what was done and why.

```bash
/cleancode:refactor src/order.ts "pull out function"
/cleancode:refactor src/router.ts "swap switch for table"
/cleancode:refactor src/auth.ts                             # skill suggests the best one
```

### `/cleancode:test`

Looks at a test file and flags tests that miss Arrange / Act / Assert, have vague names (`test1`, `testUser`), check several things at once, or contain `if`/`for`/`while`. `fix` rewrites each flagged test into AAA blocks, splits multi-assertion tests, and moves repeated setup into a helper.

```bash
/cleancode:test src/auth.test.ts          # report only
/cleancode:test src/auth.test.ts fix      # rewrite flagged tests
```

### `/cleancode:untangle`

Finds places where one file reaches through several others. Flags method chains deeper than 2 (`a.b().c().d()`), files that import from too many places, circular imports, and god classes. `fix` introduces helper methods to hide chains — `order.getZip()` replaces `order.getCustomer().getAddress().getZip()`.

```bash
/cleancode:untangle src/order.ts
/cleancode:untangle src/order.ts fix
/cleancode:untangle .                     # whole project scan
```

### `/cleancode:safety`

Finds silent failures and missing guards: empty `catch {}`, `except: pass`, public functions without input checks, division without zero-guards, external I/O without error handling. `fix` adds guard clauses at function entry and replaces silent catches with real error handling. Intentional-looking catches are shown but never auto-changed.

```bash
/cleancode:safety src/payment.ts
/cleancode:safety src/payment.ts fix
```

### `/cleancode:structure`

Spots places where a well-known structural pattern would help: big switches → **Strategy**, repeated do-and-remember → **Command**, many similar constructions → **Factory**, tangled mutable state → **State**. `fix` applies the pattern — e.g., extracts each switch branch into its own small class and replaces the switch with a lookup.

```bash
/cleancode:structure src/billing.ts
/cleancode:structure src/billing.ts fix
```

### `/cleancode:todo`

Keeps a running team to-do list of known clean-code issues in `.cleancode-todo.md` at the project root. `scan` runs analyze across the whole project and appends any new Critical/Warning findings; `list` shows current items; `add`/`close` manage entries by id. Not gitignored — the list is meant to be shared.

```bash
/cleancode:todo scan
/cleancode:todo list
/cleancode:todo close CC-042
/cleancode:todo add "split utils.ts into auth/ and format/"
```

### `/cleancode:health`

Project-wide dashboard: total LoC, files over 300 lines, functions over 40 lines, average nesting, interface coverage, rough duplication estimate, and one **Cleanliness Score** out of 100. Read-only — for fixing, run the specific skill or `/cleancode:fix`.

```bash
/cleancode:health                    # print the dashboard
/cleancode:health save               # also writes .cleancode-health.md for tracking over time
```

### `/cleancode:fix`

One-shot fix-all. Runs analyze, then walks through each finding and delegates to the right fixer skill (`safety fix` for hidden errors, `untangle fix` for chains, `test fix` for test files, `refactor` for long functions/deep nesting). Prints a summary first, asks to confirm, then applies fixes in severity order. Stops on any error, never commits, never pushes.

```bash
/cleancode:fix src/order.ts                   # critical-only (default)
/cleancode:fix src/order.ts all               # also fix warnings
/cleancode:fix .                              # whole project, critical-only
```

---

## Project Structure

```
claude-code/
├── .claude-plugin/plugin.json        — plugin manifest (v0.2.0)
├── settings.json                     — activates cleancode-reviewer agent
├── skills/
│   ├── init/                         — /cleancode:init
│   ├── analyze/                      — /cleancode:analyze
│   ├── rewrite/                      — /cleancode:rewrite
│   ├── teach/                        — /cleancode:teach
│   ├── setup/                        — /cleancode:setup
│   ├── refactor/                     — /cleancode:refactor
│   ├── test/                         — /cleancode:test
│   ├── untangle/                     — /cleancode:untangle
│   ├── safety/                       — /cleancode:safety
│   ├── structure/                    — /cleancode:structure
│   ├── todo/                         — /cleancode:todo
│   ├── health/                       — /cleancode:health
│   └── fix/                          — /cleancode:fix
├── agents/
│   └── cleancode-reviewer.md         — background code reviewer (read-only)
└── hooks/
    ├── hooks.json                    — SessionStart + UserPromptSubmit triggers
    └── scripts/
        ├── session-start.sh          — startup check script
        └── plan-mode-inject.sh       — injects clean-code reminder during plan mode
```

---

## Troubleshooting

**Plugin not loading:**
```bash
claude --plugin-dir ./claude-code --debug
```
Check the Errors tab in `/plugin`.

**SessionStart hook not firing:**
Verify `hooks/hooks.json` is at the plugin root (not inside `.claude-plugin/`). Run `/reload-plugins` after installing.

**Skills not appearing:**
Run `/reload-plugins`. Check `/help` for `/cleancode:init` etc.

**Reviewer too noisy:**
The reviewer caps output at 5 items. If it's still too much, you can say "no review needed" in your request.

---

## Contributing

Phase 1 (Claude Code plugin) — this directory.
Phase 2 (Cursor VS Code extension) — `../cursor/`
Phase 3 (Codex CLI config) — `../codex/`

Rules source of truth: `skills/init/references/rules.md`
