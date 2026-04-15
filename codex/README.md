# cleancode-codex

Codex CLI installer for the same 15 clean code rules used by the Claude Code cleancode plugin.

## Install

Run this in any project where Codex CLI should follow the clean code standards:

```bash
npx cleancode-codex init
```

This writes:

- `AGENTS.md`
- `.cleancode-rules.md`

`init` refuses to overwrite existing files. Use `--force` when you intentionally want to replace them:

```bash
npx cleancode-codex init --force
```

## Commands

```bash
npx cleancode-codex init
npx cleancode-codex update
npx cleancode-codex rules
```

`rules` prints the 15 rules in plain language with the formal term in parentheses.

`update` refreshes `AGENTS.md` from the package templates. If `.cleancode-rules.md` has local edits, it keeps that file unchanged and writes `.cleancode-rules.md.latest` so you can review the new canonical rules before merging them.

To update from the latest published npm package, run:

```bash
npx cleancode-codex@latest update
```

## Publishing

Before publishing, regenerate templates from the Claude plugin source of truth:

```bash
node codex/scripts/sync-rules.js
npm publish
```

The canonical rules come from `claude-code/skills/init/references/rules.md` in the repository layout, or `skills/init/references/rules.md` when this package is developed from the current plugin-root checkout.
