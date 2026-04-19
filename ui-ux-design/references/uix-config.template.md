---
enabled: true
prompt_detect_enabled: true
file_guard_enabled: true
validator_enabled: true
validator_severity_floor: info
validator_exclude_rules:
excluded_paths:
---

# uix — project config

This file was auto-created by the `uix` plugin's SessionStart hook on first
session. While it exists with `enabled: true`, the three runtime hooks
(prompt-detect, file-guard, validator) fire on relevant UI/frontend work.

**To opt out of this project:** set `enabled: false` above. (Deleting this
file is *not* opt-out — `SessionStart` re-scaffolds it next session.)

## Settings (frontmatter above)

| Key | Values | Default | Effect |
|---|---|---|---|
| `enabled` | true / false | true | Master kill switch — false silences all hooks. |
| `prompt_detect_enabled` | true / false | true | UserPromptSubmit hook (UI-intent reminder). |
| `file_guard_enabled` | true / false | true | PreToolUse hook (component-reuse reminder before Write/Edit). |
| `validator_enabled` | true / false | true | PostToolUse hook (rule-based static validator after Write/Edit). |
| `validator_severity_floor` | critical / warning / info | info | Filter validator findings — only show this severity or higher. |
| `validator_exclude_rules` | comma-separated rule IDs | (none) | Skip specific rules (see catalog below). |
| `excluded_paths` | comma-separated globs | (none) | Skip files matching globs (e.g., `**/test/**, **/storybook/**, **/*.stories.tsx`). |

## Validator rule catalog

| Rule ID | Severity | What it catches |
|---|---|---|
| `wcag-1.1.1-missing-alt` | critical | `<img>` without `alt` |
| `wcag-2.4.7-focus-visible` | critical | `outline: none` without `:focus-visible` replacement |
| `wcag-2.5.8-target-size` | critical | Interactive width/height < 24px |
| `wcag-3.3.2-missing-label` | critical | `<input>` without `<label>` or `aria-label` |
| `wcag-2.1.1-non-semantic-click` | warning | `<div onClick>` / `<span onClick>` |
| `wcag-2.4.3-positive-tabindex` | warning | `tabindex` ≥ 1 |
| `inline-hex-color` | warning | Raw hex colors instead of design tokens |
| `named-css-color` | warning | `red`, `blue`, … in CSS instead of palette tokens |
| `readability-tiny-font` | warning | Font size below 12px |
| `file-too-long` | warning | File over 300 lines |
| `wcag-2.3.3-prefers-reduced-motion` | info | Motion without `prefers-reduced-motion` guard |
| `css-bang-important` | info | `!important` usage |

## Examples

**Disable just the validator (keep prompts and reminders active):**
```yaml
validator_enabled: false
```

**Only show critical findings:**
```yaml
validator_severity_floor: critical
```

**Skip stories and tests:**
```yaml
excluded_paths: **/*.stories.tsx, **/*.test.tsx, **/storybook/**
```

**Allow inline hex during a quick prototype phase:**
```yaml
validator_exclude_rules: inline-hex-color, named-css-color
```
