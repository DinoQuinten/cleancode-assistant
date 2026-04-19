#!/usr/bin/env python3
"""UserPromptSubmit hook for the uix plugin.

Strict gate: bails out unless ALL of these are true:
  1. The project has opted in via `.uix-config.md` (auto-scaffolded by
     SessionStart in frontend projects).
  2. The project is detected as a frontend/UI project.
  3. The user's prompt clearly involves UI/UX work (hard UI keyword,
     framework name, or a design-implementation phrase) — and is NOT
     dominated by backend/data/infra context.

When all three pass, emit a systemMessage that:
  - Points Claude at the uix skills + component-reuse check.
  - Lists detected design assets in the project so Claude reads them
    before implementing.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
import _settings  # noqa: E402
import _design_scan  # noqa: E402
import _project_detect  # noqa: E402


# HARD keywords — strong UI signal, fire on their own.
HARD_UI_KEYWORDS = re.compile(
    r"""\b(
        ui | ux | a11y | accessibility | wcag |
        frontend | front-end | jsx | tsx |
        button | modal | dialog | dropdown | combobox | navbar | sidebar |
        toast | tooltip | accordion | tabs |
        dashboard | landing |
        typography | palette |
        tailwind | shadcn | chakra | mantine | radix | mui | material-ui |
        react | next(\.?js)? | vue | nuxt | svelte(kit)? | astro |
        solid(js)? | qwik | remix | angular | lit |
        scss | sass |
        mockup | wireframe | figma | sketch
    )\b""",
    re.IGNORECASE | re.VERBOSE,
)

# Phrases that imply design-implementation work even without a hard UI keyword.
# Covers:
#   "build/create/make/implement/code/design a [optional adjective] page/screen/component/..."
#   "implement/recreate/replicate/match/turn this design/mockup/figma..."
#   "from this design/mockup/wireframe..."
_UI_NOUNS = (
    r"(?:page|screen|view|component|widget|button|form|modal|dialog|dropdown|"
    r"navbar|nav|sidebar|header|footer|hero|card|tooltip|toast|wizard|"
    r"layout|landing|dashboard|admin|app|webapp|website|web\s*page|"
    r"web\s*app|mobile\s*app|ui|interface|frontend|onboarding|signup|"
    r"login|checkout|profile|settings|menu)"
)
_DESIGN_NOUNS = r"(?:design|mockup|wireframe|figma|sketch|comp|prototype)"

DESIGN_INTENT_PHRASES = re.compile(
    r"""(
        (?:build|create|make|develop|implement|code|design|spec|prototype)
        \s+(?:a|an|the|this|that|my|new|some)
        (?:\s+\w+){0,2}                           # 0-2 adjective words
        \s+""" + _UI_NOUNS + r"""\b
        |
        (?:implement|build|recreate|replicate|match|turn|copy)
        \s+(?:this|the|that|my)
        (?:\s+\w+){0,2}
        \s+""" + _DESIGN_NOUNS + r"""\b
        |
        from\s+(?:this|the|my)\s+""" + _DESIGN_NOUNS + r"""\b
        |
        turn\s+(?:this|the|my)\s+""" + _DESIGN_NOUNS + r"""\s+into\s+code
    )""",
    re.IGNORECASE | re.VERBOSE,
)

# Strong negative signals — backend / infra / data work.
NEGATIVE_CONTEXT = re.compile(
    r"""\b(
        database | schema | er\s*diagram | data\s*model |
        microservice | api\s*design | rest\s*api | graphql\s+server |
        backend\s*service | message\s*queue | event\s*bus |
        sql | postgres(ql)? | mysql | mongodb | redis | dynamodb | cassandra | kafka |
        kubernetes | docker | terraform | ansible | helm | nginx |
        ci/cd | pipeline | airflow | dag | etl |
        cron | worker | lambda | serverless |
        data\s+warehouse | data\s+lake | bigquery | snowflake |
        algorithm\s+design | system\s+design\s+(for|of)\s+(scaling|throughput|consistency)
    )\b""",
    re.IGNORECASE | re.VERBOSE,
)

GUIDANCE_HEADER = (
    "UI/UX task detected. Use the `uix` plugin skills to guide this work: "
    "design-principles, design-component, choose-pattern, color-system, "
    "review-ui, accessibility-audit, user-research. "
    "Master reference lives at ${CLAUDE_PLUGIN_ROOT}/references/UI_MASTER_GUIDE.md "
    "(14 parts + WCAG 2.2)."
)

REUSE_BLOCK = (
    "Before creating any new component:\n"
    "1. **Glob the project** for existing reusable components in "
    "`src/components/**`, `components/**`, `app/components/**`, "
    "`packages/ui/**`, `src/ui/**`, `lib/components/**`, `shared/ui/**`, "
    "`web/components/**`, `frontend/components/**`, `apps/*/components/**`.\n"
    "2. If the framework supports component reuse (React, Next, Vue, Nuxt, "
    "Svelte, SvelteKit, Angular, Solid, Astro, Qwik, Remix, Lit, etc.), "
    "**reuse or extend** an existing component instead of duplicating — "
    "match by purpose/props, not just name.\n"
    "3. Only create a new component if nothing existing fits. When you do, "
    "follow the design-component skill spec (pattern + states + spacing + "
    "WCAG 2.2 AA) and place it in the project's component directory.\n"
    "4. When styling, reuse the project's design tokens (CSS vars, theme "
    "config, Tailwind config) — never invent hex/rem values inline."
)


def looks_like_ui_work(prompt: str) -> bool:
    if not prompt.strip():
        return False
    has_design_phrase = bool(DESIGN_INTENT_PHRASES.search(prompt))
    has_hard_keyword = bool(HARD_UI_KEYWORDS.search(prompt))
    if not (has_design_phrase or has_hard_keyword):
        return False
    # Negative context blocks when the only signal is a design-intent phrase
    # (which can be ambiguous — "design the view" could be an ORM view). A
    # hard UI keyword like "react" / "tsx" / "button" overrides negatives.
    if NEGATIVE_CONTEXT.search(prompt) and not has_hard_keyword:
        return False
    return True


def main() -> int:
    settings = _settings.load()
    if not settings.is_active("prompt_detect"):
        return 0

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_dir:
        is_fe, _reason = _project_detect.is_frontend_project(Path(project_dir))
        if not is_fe:
            return 0

    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    prompt = str(payload.get("user_prompt") or payload.get("prompt") or "")
    if not looks_like_ui_work(prompt):
        return 0

    sections: list[str] = [GUIDANCE_HEADER, "", REUSE_BLOCK]

    if project_dir:
        scan_result = _design_scan.scan(Path(project_dir))
        summary = _design_scan.format_summary(scan_result)
        if summary:
            sections.append("")
            sections.append(summary)

    print(json.dumps({"systemMessage": "\n".join(sections)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
