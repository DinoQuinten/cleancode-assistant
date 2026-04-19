#!/usr/bin/env python3
"""PreToolUse hook for the uix plugin.

Bails out unless the project has opted in via `.uix-config.md`. When
active, watches Write/Edit on frontend files and injects a reuse + uix
principles reminder.
"""
from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import _settings  # noqa: E402


FRONTEND_EXT = re.compile(
    r"\.(tsx|jsx|vue|svelte|astro|html?|css|scss|sass|less|styl|mdx)$",
    re.IGNORECASE,
)

COMPONENT_HINT = re.compile(
    r"[\\/](components?|ui|widgets?|views?|pages?|screens?|app)[\\/]",
    re.IGNORECASE,
)

REUSE_REMINDER = """Frontend file write detected: `{path}`. Before proceeding:
1. **Glob existing components** (`src/components/**`, `components/**`, `app/components/**`, `packages/ui/**`, `src/ui/**`, `lib/components/**`, `web/components/**`, `frontend/components/**`, `apps/*/components/**`). If one matches this purpose, **reuse or extend** it instead.
2. If the framework supports composition (React/Vue/Svelte/Angular/Solid/Astro/Qwik/Lit/etc.), prefer reuse over duplication.
3. Apply uix principles ($CLAUDE_PLUGIN_ROOT/references/UI_MASTER_GUIDE.md): hierarchy via weight+color (not size), fixed spacing scale, modular type scale, tinted greys, systemic palette. No invented colors or spacing values.
4. Meet WCAG 2.2 AA: text contrast 4.5:1 (3:1 large/UI), visible focus ring ≥3:1, target size ≥24×24 CSS px (prefer 44×44), keyboard-reachable, no color-only semantics.
5. Reuse the project's design tokens (theme config, CSS vars, Tailwind config) — never hardcode values."""

EDIT_REMINDER = """Frontend file edit: `{path}`. Keep the uix principles in mind ($CLAUDE_PLUGIN_ROOT/references/UI_MASTER_GUIDE.md): preserve hierarchy, don't break the spacing/type scale, don't weaken WCAG 2.2 AA (contrast, focus visibility, target size, keyboard)."""


def build_message(tool: str, path: str) -> str | None:
    if tool == "Write":
        msg = REUSE_REMINDER.replace("{path}", path)
        if COMPONENT_HINT.search(path):
            msg = (
                "⚠ Likely new component path. "
                "If similar components already exist, reuse before creating.\n\n"
                + msg
            )
        return msg
    if tool == "Edit":
        return EDIT_REMINDER.replace("{path}", path)
    return None


def main() -> int:
    settings = _settings.load()
    if not settings.is_active("file_guard"):
        return 0

    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    tool = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {}) or {}
    file_path = str(tool_input.get("file_path", "") or "")

    if not file_path or not FRONTEND_EXT.search(file_path):
        return 0
    if settings.path_excluded(file_path):
        return 0

    msg = build_message(tool, file_path)
    if msg is None:
        return 0

    print(json.dumps({"systemMessage": msg}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
