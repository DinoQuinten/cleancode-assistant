# cleancode

A Claude Code plugin that turns 15 clean-code rules into enforcement, not advice. Built for teams where juniors ship AI-generated code faster than seniors can review it.

## What it gives you

- **Whole-codebase by default** — every `/cleancode:*` command scans the whole project unless you pass a file or folder path (or name one in the message). Narrow scope is opt-in, wide scope is free. See `SCOPE_POLICY.md` for the exact rules.
- **15 plain-language rules** — Law of Demeter, Fail Fast, function size, naming, folder structure, AAA tests, and more. Formal names stay in parentheses so seniors still recognise them.
- **Auto-fix, not just flag** — method chains (`a.b().c().d()`) become named helpers, empty catches become surfaced errors with guards, messy tests get rewritten with Arrange / Act / Assert.
- **Cross-folder restructure** — `/cleancode:restructure` reads the project's own conventions, proposes a plan to move misplaced code into properly-named folders (`features/`, `services/`, `ui/`, `lib/`, etc.), waits for one confirmation, then moves files atomically with `git mv` and rewrites every affected import. Covers both **backend** (route handlers, services, repositories) and **frontend** (page-file bloat, component duplication, feature folders, hooks/stores) layouts.
- **Cleanliness score** — `/cleancode:health` gives a 0–100 score and a prioritised checklist for whatever file or folder you point it at.
- **Session-start nudge** — a `UserPromptSubmit` hook quietly reminds Claude of the rules before every turn, so the rules apply to new generations too, not just reviews.
- **Reviewer sub-agent** — `cleancode-reviewer` can be invoked on any diff to surface violations with concrete rewrites.

## Install

From Claude Code:

```
/plugin marketplace add DinoQuinten/claude-plugins
/plugin install cleancode@dinoquinten-plugins
```

**That's it.** Zero setup — no dependencies, no downloads, no build step.

## Using Codex CLI instead of Claude Code?

See [`../codex/`](../codex/) for the Codex CLI installer: `npx cleancode-codex init`.

## More

See the [root README](../README.md) for the full marketplace overview and the [repo](https://github.com/DinoQuinten/claude-plugins) for issues and contributions.
