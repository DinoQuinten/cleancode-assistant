"""Detect whether the current project is actually a UI/UX project.

Used to gate uix plugin auto-activation so we NEVER scaffold or fire in
pure backend / data / infrastructure repos. This is the strictness gate:
if `is_frontend_project()` returns False, no uix hook should do anything.

A project counts as frontend if ANY of these signals exist:
  1. package.json declares a known frontend dependency
  2. A frontend framework config file is present
  3. An HTML entry file is present
  4. A frontend source file (.tsx/.jsx/.vue/.svelte/.astro) exists in
     conventional UI directories (src/, app/, components/, pages/, ui/,
     lib/, views/, screens/, widgets/, layouts/, routes/) — bounded scan
  5. A design assets folder exists (design/, mockups/, figma/, ...)

Bounded scan + early-exit on first match → fast even on large repos.
"""
from __future__ import annotations

import json
from pathlib import Path


FRONTEND_DEPS = {
    # React family
    "react", "react-dom", "react-native", "preact", "preact/hooks",
    "next", "@remix-run/react", "@remix-run/node", "remix",
    "gatsby", "@gatsbyjs/reach-router",
    # Vue family
    "vue", "@vue/runtime-core", "@vue/runtime-dom",
    "nuxt", "@nuxt/core",
    "quasar", "@quasar/app",
    # Svelte family
    "svelte", "@sveltejs/kit",
    # Angular family
    "@angular/core", "@angular/common",
    # Solid family
    "solid-js", "@solidjs/start", "@solidjs/router",
    # Qwik
    "@builder.io/qwik", "@builder.io/qwik-city",
    # Astro
    "astro", "@astrojs/core",
    # Lit / Web Components
    "lit", "lit-element", "lit-html",
    "@stencil/core", "stencil",
    # Other UI frameworks
    "alpinejs", "htmx.org", "htmx",
    "ember-source", "@ember/component",
    "@inertiajs/react", "@inertiajs/vue3", "@inertiajs/svelte",
    # Major component libraries (strong UI signal even without framework)
    "@chakra-ui/react", "@mui/material", "@mantine/core",
    "antd", "shadcn-ui", "@radix-ui/react-primitive",
    "@headlessui/react", "@headlessui/vue",
    # Style frameworks
    "tailwindcss", "@tailwindcss/postcss",
    "@emotion/react", "@emotion/styled", "styled-components",
}

FE_CONFIG_FILES = {
    "next.config.js", "next.config.ts", "next.config.mjs", "next.config.cjs",
    "nuxt.config.js", "nuxt.config.ts", "nuxt.config.mjs",
    "svelte.config.js", "svelte.config.ts",
    "astro.config.mjs", "astro.config.js", "astro.config.ts",
    "gatsby-config.js", "gatsby-config.ts",
    "angular.json", "vue.config.js", "vue.config.ts",
    "quasar.config.js", "remix.config.js",
    "tailwind.config.js", "tailwind.config.ts", "tailwind.config.mjs", "tailwind.config.cjs",
    "postcss.config.js", "postcss.config.cjs", "postcss.config.mjs",
    "vite.config.js", "vite.config.ts",  # commonly frontend; below we also check for FE deps
}

FE_FILE_EXTS = {".tsx", ".jsx", ".vue", ".svelte", ".astro"}

# Conventional FE source directories — we only scan these for FE files.
UI_DIRS = (
    "src", "app", "apps", "components", "pages", "screens", "ui", "views",
    "widgets", "layouts", "routes", "lib", "client", "frontend",
    "web", "www", "webapp", "site", "sites", "packages",
)

DESIGN_FOLDERS = (
    "design", "designs", "mockup", "mockups", "wireframe", "wireframes",
    "figma", "sketches", ".design", "design-system",
)

EXCLUDED_DIRS = {
    "node_modules", "dist", "build", ".next", ".nuxt", ".svelte-kit",
    ".git", ".cache", ".turbo", ".vercel", ".output", "out",
    "coverage", "__pycache__", ".venv", "venv", ".pytest_cache",
    "vendor", "target", ".gradle", ".idea", ".vscode",
}


def _read_package_json(pkg_path: Path) -> dict | None:
    try:
        return json.loads(pkg_path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, json.JSONDecodeError, ValueError):
        return None


def has_frontend_dep(project: Path) -> bool:
    pkg = project / "package.json"
    if not pkg.is_file():
        return False
    data = _read_package_json(pkg)
    if not data:
        return False
    for section in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        deps = data.get(section) or {}
        if any(name in FRONTEND_DEPS for name in deps):
            return True
    return False


def has_fe_config(project: Path) -> bool:
    return any((project / name).is_file() for name in FE_CONFIG_FILES)


def has_html_entry(project: Path) -> bool:
    candidates = (
        "index.html",
        "public/index.html", "static/index.html",
        "src/index.html", "app/index.html", "client/index.html",
        "web/index.html", "www/index.html", "frontend/index.html",
        "webapp/index.html", "site/index.html",
    )
    return any((project / c).is_file() for c in candidates)


def has_fe_file(project: Path, max_dirs_scanned: int = 200) -> bool:
    """Look for a frontend source file inside conventional UI directories.

    Bounded: skips excluded dirs, walks at most `max_dirs_scanned` directories.
    Early-exits on first match.
    """
    bases = [project] + [project / d for d in UI_DIRS if (project / d).is_dir()]
    dirs_scanned = 0
    for base in bases:
        if not base.is_dir():
            continue
        try:
            stack = [base]
            while stack and dirs_scanned < max_dirs_scanned:
                current = stack.pop()
                dirs_scanned += 1
                try:
                    entries = list(current.iterdir())
                except (OSError, PermissionError):
                    continue
                for entry in entries:
                    if entry.is_file() and entry.suffix.lower() in FE_FILE_EXTS:
                        return True
                    if entry.is_dir() and entry.name not in EXCLUDED_DIRS:
                        stack.append(entry)
        except (OSError, PermissionError):
            continue
    return False


def has_design_folder(project: Path) -> bool:
    return any((project / name).is_dir() for name in DESIGN_FOLDERS)


def is_frontend_project(project: Path) -> tuple[bool, str]:
    """Returns (is_frontend, reason)."""
    if not project.is_dir():
        return False, "not a directory"

    if has_frontend_dep(project):
        return True, "package.json declares a frontend dependency"
    if has_fe_config(project):
        return True, "frontend framework config file present"
    if has_html_entry(project):
        return True, "HTML entry file present"
    if has_fe_file(project):
        return True, "frontend source file present in UI directory"
    if has_design_folder(project):
        return True, "design assets folder present"

    return False, "no frontend signals (no FE deps, no FE config, no HTML, no FE source, no design folder)"
