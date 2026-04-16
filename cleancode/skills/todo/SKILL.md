---
name: Clean Code Todo
description: This skill should be used when the user asks to "track to-fix items", "track technical debt", "scan for tech debt", "add a debt item", "what needs cleaning", "list known issues", "close a tech debt item", or mentions keeping a running list of cleanup work. Maintains a persistent .cleancode-todo.md file at the project root with entries for each known violation.
argument-hint: "[scan | add <description> | list | close <id>]"
allowed-tools: Read, Write, Grep, Glob
version: 0.2.0
---

# Clean Code Todo

Keep a running list of known clean-code issues in a file called `.cleancode-todo.md` at the project root. Think of it as a team to-do list for code quality — like TODO comments, but in one place where you can sort, prioritize, and close them.

**Source:** Code Complete 2nd Ed., Ch. 20 — tracking and managing technical debt.

## When This Runs

- User asks to scan, list, add, or close debt items
- Auto-triggered after a major analyze run (`/cleancode:analyze .`) if the user wants findings persisted

## Arguments

```
/cleancode:todo                  # defaults to scan
/cleancode:todo scan             # scan project and add any new findings
/cleancode:todo list             # show current open items
/cleancode:todo add "<description>"   # manually add an item
/cleancode:todo close <id>       # mark an item as done
```

## File Format

`.cleancode-todo.md` lives at the project root and is NOT gitignored (it's a shared team list).

```markdown
# Clean Code Todo

Generated and maintained by cleancode plugin. Edit thresholds in `.cleancode-rules.md`.
Last updated: 2026-04-15

## Open

### CC-001 · Critical · file-too-long
- **File:** `src/services/userService.ts:1`
- **Rule:** Rule 1 — File Size (> 300 lines)
- **Detected:** 2026-04-10
- **Suggested fix:** split into `userReader.ts`, `userWriter.ts`, `userAuth.ts`

### CC-002 · Warning · reaching-through-objects
- **File:** `src/order.ts:47`
- **Rule:** Rule 11 — Law of Demeter
- **Detected:** 2026-04-11
- **Suggested fix:** add `order.getZip()` helper

## Closed

### CC-000 · Warning · function-too-long (closed 2026-04-09)
- **File:** `src/auth.ts:12`
- Fixed in commit abc123
```

Each item has:
- **ID** — `CC-NNN` sequential
- **Severity** — Critical / Warning / Style
- **Rule** — which rule is violated
- **File + line** — exact location
- **Detected** — ISO date
- **Suggested fix** — short action

See `references/todo-schema.md` for the full schema and parsing rules.

## Command: scan (default)

1. Check if `.cleancode-todo.md` exists.
   - If not, create the file with the header above.
2. Run a project-wide scan (delegate to the analyze logic — use the same detection rules).
3. For each finding:
   - Check if an item already exists for this file + line + rule.
   - If yes, skip.
   - If no, append as a new open item with the next `CC-NNN` ID.
4. Print a summary:
   ```
   cleancode todo scan complete
     • 3 new items added (CC-023, CC-024, CC-025)
     • 12 existing items unchanged
     • 47 open, 18 closed total

   Run /cleancode:todo list to see open items.
   ```

## Command: list

1. Read `.cleancode-todo.md`.
2. Parse the Open section.
3. Print grouped by severity:
   ```
   Open clean code items (3 critical, 8 warning, 5 style):

   🔴 Critical
     CC-001  file-too-long           src/services/userService.ts:1
     CC-008  hidden-errors            src/auth/middleware.ts:34
     CC-015  god-class                src/App.tsx:1

   🟡 Warning
     CC-002  reaching-through-objects src/order.ts:47
     ...

   🔵 Style
     CC-020  magic-number             src/constants.ts:12
     ...
   ```

## Command: add

1. Parse the description from args.
2. Append a new item with the next `CC-NNN` ID, severity = Warning (default), no file/line (manual entry).
3. Confirm: `Added CC-026.`

## Command: close

1. Parse the ID from args.
2. Find the item in Open, move to Closed, add `(closed YYYY-MM-DD)`.
3. If the user wants to link a commit, allow: `/cleancode:todo close CC-001 --commit abc123`.
4. Confirm: `Closed CC-001.`

## Auto-Close on Commit (optional)

If a commit message contains `closes CC-NNN` or `fixes CC-NNN`, suggest auto-closing those items. Don't auto-close without user confirmation.

## Update Last-Updated

Every time the file is modified, update the `Last updated:` line at the top to today's date.

## Rules

- **Never delete items.** Closed items stay in the Closed section for history.
- **IDs are stable.** Once assigned, never reused.
- **One entry per file + line + rule.** Don't duplicate.
- **Don't auto-add from the reviewer agent.** Only explicit `/cleancode:todo scan` adds items; the reviewer stays non-blocking.

## Additional Resources

- **`references/todo-schema.md`** — full schema, parsing rules, migration notes
