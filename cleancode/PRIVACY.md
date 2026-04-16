# Privacy Policy — cleancode plugin

**Effective date:** 2026-04-15

## Summary

The cleancode plugin for Claude Code does **not** collect, transmit, store, or share any personal data, source code, telemetry, or usage information.

## What the plugin does

The plugin runs entirely on the user's machine, inside the Claude Code environment the user already trusts. It:

- Reads source files the user explicitly targets with a `/cleancode:*` command.
- Writes clean-code configuration files (`.cleancode-rules.md`, `CLAUDE.md`, `.cursorrules`, `AGENTS.md`, `.cleancode-todo.md`, `.cleancode-health.md`) inside the user's own project directory.
- Appends non-blocking review suggestions to Claude's responses.

## What the plugin does NOT do

- It does **not** send source code anywhere outside the user's local Claude Code session.
- It does **not** contact any server, analytics service, or third-party API.
- It does **not** collect identifiers, telemetry, crash reports, or usage metrics.
- It does **not** read files outside the current project directory.

## Data handled by Claude Code itself

The plugin runs inside Claude Code. Any data transmission between the user and Anthropic's Claude models is governed by Anthropic's own privacy policy, not this one. See https://www.anthropic.com/privacy for details.

## Third-party services

None. The plugin has no network dependencies.

## Children's privacy

The plugin does not knowingly process data from children under 13, and does not process personal data at all.

## Changes to this policy

If the plugin ever adds behavior that handles user data, this policy will be updated in the same commit, and the change will appear in the repository history at https://github.com/DinoQuinten/cleancode-assistant.

## Contact

For questions about this policy, open an issue at https://github.com/DinoQuinten/cleancode-assistant/issues.
