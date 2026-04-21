# cleancode — Default Scope Policy

**This policy applies to every skill in the cleancode plugin.** Each skill's `SKILL.md` links here instead of restating the rules.

## The Rule

When a cleancode command is invoked, resolve scope in this order:

1. **Explicit path argument wins.** If the user passed a file path (`/cleancode:safety src/auth.ts`) or a folder path (`/cleancode:safety src/auth/`), use exactly that.
2. **Explicit contextual reference wins.** If the user's *current* message names a single file or folder — e.g. *"run safety on `src/auth.ts`"* or *"untangle the `payments/` folder"* — use that path. A filename mentioned only in an earlier turn does **not** count; the reference must be in the message that triggered the command.
3. **Otherwise: whole codebase.** No path argument and no in-message file reference → scan every source file in the project root (honor `.gitignore` and `.cleancode-ignore`, skip `node_modules`, `dist`, `build`, generated code, lock files).

> Rule of thumb: *if you'd have to guess which file the user meant, don't guess — scan the whole codebase instead.*

## What Counts as "Explicit"

| Signal | Scope |
|---|---|
| `/cleancode:fix src/auth.ts` | Single file |
| `/cleancode:fix src/auth/` (trailing `/`) | Single folder |
| `/cleancode:fix` | **Whole codebase** |
| `/cleancode:fix .` | **Whole codebase** (explicit) |
| User message: *"fix `src/auth.ts`"* + `/cleancode:fix` | Single file |
| User message three turns ago mentioned `auth.ts`, current message is just `/cleancode:fix` | **Whole codebase** |
| User says *"fix everything"*, *"clean the project"*, *"scan the repo"* | **Whole codebase** |
| User says *"fix this file"* with no file named anywhere | Ask: *"which file?"* |

## What "Whole Codebase" Means

Use the bash helper in `skills/fix/SKILL.md` (Step 0.1) to enumerate files. Summary:

- Start at the project root (the directory containing `.cleancode-rules.md`, falling back to the git root, falling back to the current working directory).
- Include: `.ts .tsx .js .jsx .py .go .rs .java .kt .rb .cs .cpp .c .h .hpp .swift .php`.
- Exclude: `node_modules/`, `dist/`, `build/`, `.next/`, `out/`, `target/`, `vendor/`, `__pycache__/`, `.venv/`, `coverage/`, `*.min.*`, `*.lock`, `package-lock.json`, `*.generated.*`.
- Honor `.gitignore` and `.cleancode-ignore` on top of the above.

## What Changes for Each Skill

- **analyze, fix, health, todo, restructure** — already whole-codebase by default. No behavior change.
- **safety, untangle, structure, test, refactor, rewrite** — *previously* required a file path. Now: no args = whole codebase; pass a path to narrow.
- **teach, init, setup** — scope-free (teach is educational; init/setup work on project-level config files). No change.

## Confirmation Gates

Any skill that *writes* to files (`fix`, `safety fix`, `untangle fix`, `structure fix`, `test fix`, `refactor`, `rewrite`, `restructure`) must still show a plan and wait for `yes` before editing — whole-codebase scope does **not** imply whole-codebase silent writes.

Read-only skills (`analyze`, `health`, report-mode `safety`/`untangle`/`structure`/`test`) can run immediately with no gate.

## One-line Summary (for SKILL.md bodies to reuse)

> **Default scope: whole codebase.** Pass a file or folder path to narrow. See `../SCOPE_POLICY.md`.
