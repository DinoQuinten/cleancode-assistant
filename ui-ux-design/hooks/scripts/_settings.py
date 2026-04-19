"""Shared settings loader for uix plugin hooks.

Reads `.uix-config.md` from the project root. The file uses a tiny
YAML-ish frontmatter (flat key: value pairs, no nesting) that we parse
with regex so we don't depend on PyYAML.

If the file is missing → the plugin is **not opted in** for this project
and all hooks should bail out. This is the cleancode pattern.

Settings recognised (all optional):

    enabled                   true | false   (master switch — default true)
    prompt_detect_enabled     true | false   (default true)
    file_guard_enabled        true | false   (default true)
    validator_enabled         true | false   (default true)
    validator_severity_floor  critical | warning | info  (default info)
    validator_exclude_rules   comma-separated rule IDs    (default empty)
    excluded_paths            comma-separated globs       (default empty)
"""
from __future__ import annotations

import fnmatch
import os
import re
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath


CONFIG_FILENAME = ".uix-config.md"


@dataclass
class Settings:
    opted_in: bool = False
    enabled: bool = True
    prompt_detect_enabled: bool = True
    file_guard_enabled: bool = True
    validator_enabled: bool = True
    validator_severity_floor: str = "info"
    validator_exclude_rules: list[str] = field(default_factory=list)
    excluded_paths: list[str] = field(default_factory=list)

    def is_active(self, hook: str) -> bool:
        """`hook` is one of: prompt_detect, file_guard, validator."""
        if not self.opted_in or not self.enabled:
            return False
        return getattr(self, f"{hook}_enabled", True)

    def path_excluded(self, file_path: str) -> bool:
        if not file_path or not self.excluded_paths:
            return False
        normalized = file_path.replace("\\", "/")
        path = PurePosixPath(normalized)
        for pattern in self.excluded_paths:
            # PurePath.match supports `**` recursive globs; fnmatch does not.
            try:
                if path.match(pattern):
                    return True
            except ValueError:
                pass
            # Fallback: also try fnmatch for simple patterns without `**`.
            if fnmatch.fnmatch(normalized, pattern):
                return True
        return False

    def severity_passes(self, severity: str) -> bool:
        order = {"info": 0, "warning": 1, "critical": 2}
        return order.get(severity, 0) >= order.get(self.validator_severity_floor, 0)


_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_KV_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*?)\s*$", re.MULTILINE)


def _parse_bool(value: str, default: bool) -> bool:
    v = value.strip().lower()
    if v in {"true", "yes", "on", "1"}:
        return True
    if v in {"false", "no", "off", "0"}:
        return False
    return default


def _parse_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _project_dir() -> Path | None:
    project = os.environ.get("CLAUDE_PROJECT_DIR")
    if project:
        return Path(project)
    return None


def load() -> Settings:
    """Load settings, returning Settings(opted_in=False) when no marker exists."""
    project = _project_dir()
    if project is None:
        return Settings()
    config_path = project / CONFIG_FILENAME
    if not config_path.is_file():
        return Settings()

    try:
        text = config_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return Settings()

    settings = Settings(opted_in=True)
    match = _FRONTMATTER_RE.search(text)
    if not match:
        return settings  # Marker present but no frontmatter — use defaults.

    for key, raw in _KV_RE.findall(match.group(1)):
        key = key.lower()
        if key == "enabled":
            settings.enabled = _parse_bool(raw, settings.enabled)
        elif key == "prompt_detect_enabled":
            settings.prompt_detect_enabled = _parse_bool(raw, True)
        elif key == "file_guard_enabled":
            settings.file_guard_enabled = _parse_bool(raw, True)
        elif key == "validator_enabled":
            settings.validator_enabled = _parse_bool(raw, True)
        elif key == "validator_severity_floor":
            v = raw.strip().lower()
            if v in {"critical", "warning", "info"}:
                settings.validator_severity_floor = v
        elif key == "validator_exclude_rules":
            settings.validator_exclude_rules = _parse_list(raw)
        elif key == "excluded_paths":
            settings.excluded_paths = _parse_list(raw)

    return settings
