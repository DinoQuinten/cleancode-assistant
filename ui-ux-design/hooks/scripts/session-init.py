#!/usr/bin/env python3
"""SessionStart hook for the uix plugin.

Strict gate: only auto-activates in projects that are demonstrably
frontend/UI projects (per `_project_detect.is_frontend_project`).
Backend, data, infra, or unrelated repos see NOTHING from this plugin.

When the gate passes:
  1. If `.uix-config.md` doesn't exist, scaffold it from the bundled
     template so the plugin auto-activates with no manual init step.
  2. Scan for design assets (design folders, .fig/.sketch files,
     mockup images) and announce them so Claude knows to read them
     before implementing UI.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
import _design_scan  # noqa: E402
import _project_detect  # noqa: E402


def ensure_config(project: Path, plugin_root: Path) -> str:
    config = project / ".uix-config.md"
    template = plugin_root / "references" / "uix-config.template.md"

    if config.exists():
        return "uix active — config at .uix-config.md"

    if not template.is_file():
        return ""

    try:
        config.write_text(
            template.read_text(encoding="utf-8", errors="replace"),
            encoding="utf-8",
        )
    except OSError as err:
        print(f"uix: could not auto-scaffold .uix-config.md ({err})", file=sys.stderr)
        return ""

    return (
        "uix auto-activated — created .uix-config.md from template. "
        "Edit settings inside the file (severity_floor, excluded_paths, "
        "validator_exclude_rules), or set `enabled: false` to opt out."
    )


def main() -> int:
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if not project_dir or not plugin_root:
        return 0

    project = Path(project_dir)

    is_fe, reason = _project_detect.is_frontend_project(project)
    if not is_fe:
        # Not a UI/UX project — stay completely silent.
        return 0

    banner_lines: list[str] = []

    line = ensure_config(project, Path(plugin_root))
    if line:
        banner_lines.append(line)

    scan_result = _design_scan.scan(project)
    summary = _design_scan.format_summary(scan_result)
    if summary:
        banner_lines.append("")
        banner_lines.append(summary)

    if banner_lines:
        print("\n".join(banner_lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
