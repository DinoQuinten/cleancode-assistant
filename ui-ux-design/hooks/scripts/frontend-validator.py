#!/usr/bin/env python3
"""PostToolUse validator for the uix plugin.

Bails out unless the project has opted in via `.uix-config.md`. When
active, runs fast rule-based static checks for WCAG risks, design-system
violations, and common smells. Silent on clean files.

Rule-based (no LLM) so it runs instantly in the background and never
blocks the user.
"""
from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
import _settings  # noqa: E402


FRONTEND_EXT = re.compile(
    r"\.(tsx|jsx|vue|svelte|astro|html?|css|scss|sass|less|styl|mdx)$",
    re.IGNORECASE,
)


@dataclass
class Finding:
    severity: str  # "critical" | "warning" | "info"
    rule: str
    line: int
    snippet: str
    fix: str


NAMED_COLORS = {
    "red", "green", "blue", "yellow", "orange", "purple", "pink",
    "cyan", "magenta", "black", "white", "gray", "grey", "brown",
    "lime", "navy", "teal", "maroon", "olive", "silver", "gold",
}


def _lines(content: str) -> list[str]:
    return content.splitlines()


def check_inline_hex(lines: list[str]) -> list[Finding]:
    out: list[Finding] = []
    pat = re.compile(r"#(?:[0-9a-fA-F]{3}){1,2}\b|#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{8}\b")
    for i, line in enumerate(lines, 1):
        if "//" in line and line.strip().startswith("//"):
            continue
        for m in pat.finditer(line):
            out.append(Finding(
                "warning", "inline-hex-color", i, m.group(),
                "Use a design token (theme.colors.*, var(--color-*), Tailwind class) instead of a raw hex.",
            ))
    return out


def check_named_colors(lines: list[str]) -> list[Finding]:
    out: list[Finding] = []
    pat = re.compile(r":\s*(" + "|".join(NAMED_COLORS) + r")\b\s*;?", re.IGNORECASE)
    for i, line in enumerate(lines, 1):
        for m in pat.finditer(line):
            out.append(Finding(
                "warning", "named-css-color", i, m.group().strip(),
                f"Replace '{m.group(1)}' with a semantic token from the palette.",
            ))
    return out


def check_outline_none(lines: list[str], full_text: str) -> list[Finding]:
    out: list[Finding] = []
    has_focus_visible = bool(re.search(r":focus(-visible)?\s*\{", full_text))
    pat = re.compile(r"outline\s*:\s*(none|0)\b")
    for i, line in enumerate(lines, 1):
        if pat.search(line) and not has_focus_visible:
            out.append(Finding(
                "critical", "wcag-2.4.7-focus-visible", i, line.strip(),
                "Replace with a visible :focus-visible style (≥3:1 contrast, ≥2px).",
            ))
    return out


def check_img_alt(lines: list[str]) -> list[Finding]:
    out: list[Finding] = []
    pat = re.compile(r"<img\b(?![^>]*\balt\s*=)[^>]*>", re.IGNORECASE)
    for i, line in enumerate(lines, 1):
        for m in pat.finditer(line):
            out.append(Finding(
                "critical", "wcag-1.1.1-missing-alt", i, m.group()[:80],
                "Add alt text; use alt=\"\" only for purely decorative images.",
            ))
    return out


def check_non_semantic_click(lines: list[str]) -> list[Finding]:
    out: list[Finding] = []
    pat = re.compile(r"<(div|span)\b[^>]*\bonClick\b", re.IGNORECASE)
    for i, line in enumerate(lines, 1):
        for m in pat.finditer(line):
            out.append(Finding(
                "warning", "wcag-2.1.1-non-semantic-click", i, m.group()[:80],
                f"Use <button> (or role='button' + keydown/keyup + tabindex) instead of <{m.group(1)} onClick>.",
            ))
    return out


def check_positive_tabindex(lines: list[str]) -> list[Finding]:
    out: list[Finding] = []
    pat = re.compile(r'tabindex\s*=\s*(?:\{\s*["\']?|["\']?)([1-9]\d*)', re.IGNORECASE)
    for i, line in enumerate(lines, 1):
        for m in pat.finditer(line):
            out.append(Finding(
                "warning", "wcag-2.4.3-positive-tabindex", i, m.group(),
                "Remove positive tabindex; use DOM order for focus sequence.",
            ))
    return out


def check_tiny_font(lines: list[str]) -> list[Finding]:
    out: list[Finding] = []
    pat = re.compile(r"font-?[sS]ize\s*:\s*['\"]?(\d+(?:\.\d+)?)px")
    for i, line in enumerate(lines, 1):
        for m in pat.finditer(line):
            if float(m.group(1)) < 12:
                out.append(Finding(
                    "warning", "readability-tiny-font", i, m.group(),
                    "Body text below 12px is hard to read; use ≥14px (or a type-scale token).",
                ))
    return out


def check_small_target(lines: list[str]) -> list[Finding]:
    out: list[Finding] = []
    pat = re.compile(r"(width|height)\s*:\s*['\"]?(\d+(?:\.\d+)?)px", re.IGNORECASE)
    interactive = re.compile(
        r"button|\[role=['\"]?button|<a\b|<input\b|onClick|role=['\"]?button",
        re.IGNORECASE,
    )
    for i, line in enumerate(lines, 1):
        if not interactive.search(line):
            continue
        for m in pat.finditer(line):
            if float(m.group(2)) < 24:
                out.append(Finding(
                    "critical", "wcag-2.5.8-target-size", i, m.group(),
                    "Target size must be ≥24×24 CSS px (prefer 44×44).",
                ))
    return out


def check_bang_important(lines: list[str]) -> list[Finding]:
    out: list[Finding] = []
    for i, line in enumerate(lines, 1):
        if "!important" in line:
            out.append(Finding(
                "info", "css-bang-important", i, line.strip()[:80],
                "!important signals specificity rot; prefer a clearer cascade or token.",
            ))
    return out


def check_missing_label(lines: list[str]) -> list[Finding]:
    out: list[Finding] = []
    pat = re.compile(r"<input\b(?![^>]*\baria-label\b)(?![^>]*\bid\s*=)[^>]*>", re.IGNORECASE)
    for i, line in enumerate(lines, 1):
        for m in pat.finditer(line):
            if re.search(r'type\s*=\s*["\']?(hidden|submit|button|reset)', m.group(), re.IGNORECASE):
                continue
            out.append(Finding(
                "critical", "wcag-3.3.2-missing-label", i, m.group()[:80],
                "Add a visible <label> associated by id, or an aria-label.",
            ))
    return out


def check_motion_no_reduced(lines: list[str], full_text: str) -> list[Finding]:
    out: list[Finding] = []
    has_motion = bool(re.search(r"\btransition\b\s*:|@keyframes\b|\banimation\b\s*:", full_text))
    if has_motion and "prefers-reduced-motion" not in full_text:
        out.append(Finding(
            "info", "wcag-2.3.3-prefers-reduced-motion", 0,
            "transitions/animations present without prefers-reduced-motion guard",
            "Wrap motion in @media (prefers-reduced-motion: no-preference) { ... } or provide a reduced variant.",
        ))
    return out


def check_file_length(lines: list[str]) -> list[Finding]:
    if len(lines) > 300:
        return [Finding(
            "warning", "file-too-long", len(lines), f"{len(lines)} lines",
            "Split this component — files over 300 lines hurt readability and reuse.",
        )]
    return []


def run_checks(path: Path, content: str) -> list[Finding]:
    lines = _lines(content)
    ext = path.suffix.lower()
    findings: list[Finding] = []
    findings += check_inline_hex(lines)
    if ext in {".css", ".scss", ".sass", ".less", ".styl"}:
        findings += check_named_colors(lines)
    findings += check_outline_none(lines, content)
    findings += check_img_alt(lines)
    findings += check_non_semantic_click(lines)
    findings += check_positive_tabindex(lines)
    findings += check_tiny_font(lines)
    findings += check_small_target(lines)
    findings += check_bang_important(lines)
    findings += check_missing_label(lines)
    findings += check_motion_no_reduced(lines, content)
    findings += check_file_length(lines)
    return findings


def filter_findings(findings: list[Finding], settings) -> list[Finding]:
    return [
        f for f in findings
        if settings.severity_passes(f.severity)
        and f.rule not in settings.validator_exclude_rules
    ]


def format_report(path: Path, findings: list[Finding]) -> str:
    groups: dict[str, list[Finding]] = {"critical": [], "warning": [], "info": []}
    for f in findings:
        groups[f.severity].append(f)

    counts = []
    if groups["critical"]:
        counts.append(f"{len(groups['critical'])} critical")
    if groups["warning"]:
        counts.append(f"{len(groups['warning'])} warning")
    if groups["info"]:
        counts.append(f"{len(groups['info'])} info")
    summary = "Found " + ", ".join(counts) + "."

    lines: list[str] = [f"🔎 **uix validator — {path.name}**", summary, ""]
    for sev in ("critical", "warning", "info"):
        if not groups[sev]:
            continue
        label = {"critical": "❌ Critical", "warning": "⚠ Warning", "info": "ℹ Info"}[sev]
        lines.append(f"**{label}**")
        for f in groups[sev][:8]:
            loc = f"L{f.line}" if f.line else "file"
            lines.append(f"- `{f.rule}` @ {loc} — `{f.snippet}` → {f.fix}")
        if len(groups[sev]) > 8:
            lines.append(f"  (…{len(groups[sev]) - 8} more {sev})")
        lines.append("")

    lines.append(
        "Run `/uix:review-ui @" + str(path).replace("\\", "/") +
        "` for a full deep audit, or `/uix:accessibility-audit` for WCAG 2.2 detail."
    )
    return "\n".join(lines)


def main() -> int:
    settings = _settings.load()
    if not settings.is_active("validator"):
        return 0

    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    tool = payload.get("tool_name", "")
    if tool not in {"Write", "Edit"}:
        return 0

    tool_input = payload.get("tool_input", {}) or {}
    file_path = str(tool_input.get("file_path", "") or "")
    if not file_path or not FRONTEND_EXT.search(file_path):
        return 0
    if settings.path_excluded(file_path):
        return 0

    path = Path(file_path)
    try:
        if path.exists():
            content = path.read_text(encoding="utf-8", errors="replace")
        else:
            content = str(tool_input.get("content", "") or "")
    except OSError:
        return 0

    if not content.strip():
        return 0

    findings = filter_findings(run_checks(path, content), settings)
    if not findings:
        return 0

    print(json.dumps({"systemMessage": format_report(path, findings)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
