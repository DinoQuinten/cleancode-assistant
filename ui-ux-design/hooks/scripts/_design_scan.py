"""Scan a project for design assets so Claude can reference them.

Detects:
  - Design folders by convention (design/, mockups/, wireframes/, figma/, ...)
  - Native design files anywhere (.fig, .sketch, .xd, .ai, .psd)
  - Images inside design folders (.png, .jpg, .svg, .webp, .gif)

Excludes noisy directories (node_modules, dist, build, .git, .next, etc.) so
the scan is fast even on large repos.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


# Folders by convention. Checked at the project root and one level down.
DESIGN_FOLDERS = (
    "design", "designs", "mockup", "mockups",
    "wireframe", "wireframes", "figma", "sketches",
    ".design", "design-system",
    "assets/design", "assets/designs", "assets/mockups",
    "docs/design", "docs/designs", "docs/mockups",
    "public/design", "public/designs",
    "src/assets/design", "src/design",
    "ui/design",
)

# Native design source files. Strong signal regardless of folder.
DESIGN_FILE_EXTS = {".fig", ".sketch", ".xd", ".ai", ".psd", ".afdesign"}

# Image extensions — only counted *inside* a design folder to avoid
# false positives from project icons / logos / favicons everywhere.
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif", ".bmp", ".tiff", ".pdf"}

# Skip these dirs entirely — they're noise.
EXCLUDED_DIRS = {
    "node_modules", "dist", "build", ".next", ".nuxt", ".svelte-kit",
    ".git", ".cache", ".turbo", ".vercel", ".output", "out",
    "coverage", "__pycache__", ".venv", "venv", ".pytest_cache",
    "vendor", "target",
}


@dataclass
class DesignScan:
    folders: list[str] = field(default_factory=list)         # design folders found
    design_files: list[str] = field(default_factory=list)    # *.fig, *.sketch, etc.
    images: list[str] = field(default_factory=list)          # images inside design folders

    def is_empty(self) -> bool:
        return not (self.folders or self.design_files or self.images)

    def total(self) -> int:
        return len(self.folders) + len(self.design_files) + len(self.images)


def _excluded(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.parts)


def _rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def scan(project: Path, limit_per_kind: int = 25) -> DesignScan:
    result = DesignScan()
    if not project.is_dir():
        return result

    # 1. Convention folders.
    for name in DESIGN_FOLDERS:
        candidate = project / name
        if candidate.is_dir() and not _excluded(candidate):
            result.folders.append(_rel(candidate, project))

    # 2. Native design files anywhere (bounded scan).
    for ext in DESIGN_FILE_EXTS:
        for path in project.rglob(f"*{ext}"):
            if _excluded(path) or not path.is_file():
                continue
            result.design_files.append(_rel(path, project))
            if len(result.design_files) >= limit_per_kind:
                break

    # 3. Images, but ONLY inside detected design folders.
    for folder_str in result.folders:
        folder = project / folder_str
        for ext in IMAGE_EXTS:
            for path in folder.rglob(f"*{ext}"):
                if _excluded(path) or not path.is_file():
                    continue
                result.images.append(_rel(path, project))
                if len(result.images) >= limit_per_kind:
                    return result

    return result


def format_summary(scan_result: DesignScan, *, max_lines: int = 15) -> str:
    """Render a concise one-section summary for hook stdout / systemMessage."""
    if scan_result.is_empty():
        return ""
    parts = ["**Design assets detected in project:**"]
    if scan_result.folders:
        parts.append(f"- Design folders: {', '.join(scan_result.folders)}")
    if scan_result.design_files:
        files = scan_result.design_files[:max_lines]
        parts.append(f"- Design source files ({len(scan_result.design_files)}): {', '.join(files)}")
        if len(scan_result.design_files) > max_lines:
            parts.append(f"  …and {len(scan_result.design_files) - max_lines} more")
    if scan_result.images:
        files = scan_result.images[:max_lines]
        parts.append(f"- Images in design folders ({len(scan_result.images)}): {', '.join(files)}")
        if len(scan_result.images) > max_lines:
            parts.append(f"  …and {len(scan_result.images) - max_lines} more")
    parts.append(
        "When implementing UI from these assets: Read them first to "
        "ground your design decisions in the user's actual mockup, not in "
        "your assumptions."
    )
    return "\n".join(parts)
