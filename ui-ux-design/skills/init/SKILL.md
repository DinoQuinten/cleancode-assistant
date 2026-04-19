---
name: init
description: Re-scaffolds or customizes `.uix-config.md` for the uix plugin. Note that the plugin auto-creates this file via its SessionStart hook on first session — manual init is only needed to reset to defaults, force-overwrite, or walk through tuning options interactively. Auto-activates on "reset uix config", "re-init uix", "customize uix settings", "tune uix validator", "uix exclude this rule/path", or /uix:init.
argument-hint: ""
version: 0.1.0
allowed-tools: Read, Write, Bash
---

# init

Re-scaffold or customize `.uix-config.md` interactively. Auto-activates on init/reset/tune phrases or via `/uix:init`. Note: a fresh project does *not* need this — the SessionStart hook auto-scaffolds the file on first session.

## Triggers

"reset uix config" · "re-init uix" · "re-scaffold uix" · "force overwrite uix config" · "customize uix settings" · "tune uix validator" · "uix exclude this rule" · "uix exclude this path" · "set uix severity to critical" · "disable the uix validator in this project".

## Process

1. **Confirm target.** Determine the project root: `$CLAUDE_PROJECT_DIR` (or the current working directory if not set). Confirm with the user if it looks wrong.

2. **Check whether `.uix-config.md` already exists.**
   - If it does (the common case — auto-scaffolded by SessionStart):
     - Read the file.
     - Report the current settings to the user.
     - Ask what they want to do: **edit specific values**, **reset to defaults**, or **leave alone**. Default to "leave alone".
     - If "edit", offer the specific knob they likely want (severity_floor / validator_exclude_rules / excluded_paths / per-hook enable) and apply via `Edit`.
     - If "reset", overwrite from template only after explicit user confirmation.
   - If it doesn't (rare — only if SessionStart hasn't run yet, or file was deleted mid-session):
     - Copy the template from `${CLAUDE_PLUGIN_ROOT}/references/uix-config.template.md` to `<project>/.uix-config.md`.

3. **After any change**, briefly explain:
   - To opt out of this project: set `enabled: false` (don't delete — SessionStart re-creates it).
   - Settings inside the file take effect on the next hook invocation (no restart needed).
   - The hooks themselves only reload on Claude Code restart.
   - Point at the rule catalog and tuning examples inside the file itself.

5. **Optional follow-ups** (offer, don't auto-do):
   - Add `.uix-config.md` to the project's `.gitignore` if it should be developer-local, or commit it if the team should share the same config.
   - Tighten `validator_severity_floor` to `warning` for stricter projects.
   - Add common `excluded_paths` for the project's framework (e.g., `**/*.stories.tsx, **/*.test.tsx`).

## Ground rules

- Never modify `.uix-config.md` without showing the user the diff first.
- Never overwrite an existing file without explicit confirmation.
- If `$CLAUDE_PROJECT_DIR` isn't set and the cwd is a subfolder of a git repo, walk up to the repo root and use that — do not scaffold inside a subfolder.
- Stay quiet if the user is clearly using a different plugin (e.g., they invoked `/uix:init` accidentally inside a non-frontend repo) — confirm before writing.

## Reference

Template: `${CLAUDE_PLUGIN_ROOT}/references/uix-config.template.md`
Master guide: `${CLAUDE_PLUGIN_ROOT}/references/UI_MASTER_GUIDE.md`
