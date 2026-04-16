# .cleancode-todo.md Schema

Reference for `/cleancode:todo`. Defines the exact structure of the persistent todo file.

---

## File Location

`<project root>/.cleancode-todo.md`

- NOT gitignored — it's a shared team artifact.
- Committed alongside code.
- Auto-created by `/cleancode:todo scan` on first run.

---

## File Structure

```markdown
# Clean Code Todo

Generated and maintained by cleancode plugin. Edit thresholds in `.cleancode-rules.md`.
Last updated: YYYY-MM-DD

## Open

### CC-NNN · <Severity> · <rule-slug>
- **File:** `path/to/file.ts:LINE`
- **Rule:** Rule N — Short Name
- **Detected:** YYYY-MM-DD
- **Suggested fix:** <one-line description>

[more items...]

## Closed

### CC-NNN · <Severity> · <rule-slug> (closed YYYY-MM-DD)
- **File:** `path/to/file.ts:LINE`
- Fixed in commit <sha>
```

---

## Item Fields

| Field | Required | Format | Notes |
|---|---|---|---|
| ID | Yes | `CC-NNN` | Sequential, zero-padded to 3 digits. Never reused. |
| Severity | Yes | `Critical` \| `Warning` \| `Style` | Matches analyze output |
| Rule slug | Yes | lowercase-dashed | e.g., `file-too-long`, `reaching-through-objects` |
| File | Yes (for auto-added) | `path:line` | Line number is optional for manual items |
| Rule | Yes | `Rule N — Name` | Links to rules.md |
| Detected | Yes | `YYYY-MM-DD` | ISO date |
| Suggested fix | Optional | short sentence | One line; no long prose |
| Closed date | For closed items | `YYYY-MM-DD` | Added in the heading |
| Commit SHA | Optional | git short-sha | Used when closing via commit |

---

## ID Assignment

- Scan existing file for the highest `CC-NNN`.
- Next ID = highest + 1.
- Closed items count — IDs never reset.

---

## Parsing Rules

When reading the file:

1. Split on `## Open` and `## Closed` headers.
2. Within each section, split on `### CC-` to get items.
3. Each item's first line is the ID / Severity / Rule slug triple.
4. Subsequent `- **Field:**` lines are fields.

When writing:

1. Preserve order within each section (newest at the bottom of Open, newest at the bottom of Closed).
2. Update `Last updated:` in the file header.
3. Write via Write (whole file) — easier than surgical Edit.

---

## Rule Slug Vocabulary

Keep slugs consistent across the plugin:

| Slug | Rule | Source |
|---|---|---|
| `file-too-long` | Rule 1 | File > 300 lines |
| `function-too-long` | Rule 2 | Function > 40 lines |
| `too-many-parameters` | Rule 3 | > 4 params |
| `deep-nesting` | Rule 4 | Nesting > 4 |
| `bad-naming` | Rule 5 | Generic/short names |
| `solid-violation` | Rule 6 | SRP/OCP/etc |
| `missing-interface` | Rule 7 | TS public class without interface |
| `duplication` | Rule 8 | DRY violation |
| `what-comment` | Rule 9 | Comment explains what, not why |
| `human-readability` | Rule 10 | Unclear to a new reader |
| `reaching-through-objects` | Rule 11 | Demeter chain > 2 |
| `hidden-errors` | Rule 12 | Silent catch |
| `missing-input-check` | Rule 12 | Public function no guard |
| `unused-code` | Rule 13 | YAGNI — dead code |
| `messy-tests` | Rule 14 | AAA / naming / loops in tests |

---

## Migrating from Earlier Versions

If the file uses a pre-v0.2 format, the skill should:

1. Detect the format (older files may lack the `## Closed` section).
2. Re-emit in the new format, preserving all existing items and their IDs.
3. Note the migration in a one-line comment at the top:
   `<!-- Migrated to cleancode v0.2 schema on YYYY-MM-DD -->`

---

## Commit Hygiene

When the user commits a fix and references `closes CC-NNN` or `fixes CC-NNN` in the commit message, the skill offers to move the item to Closed. Always require user confirmation before modifying the file.
