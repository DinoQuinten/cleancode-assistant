#!/usr/bin/env bash
# SessionStart banner for system-and-database-design plugin.
# Emits a short notice to stderr so Claude Code picks it up as session context.
cat <<'EOF' >&2
[system-and-database-design] loaded.
  /system-and-database-design:design-system <requirement>    - produce a system design doc
  /system-and-database-design:design-database <domain>       - propose a database schema
  /system-and-database-design:review-architecture <input>    - critique against checklists + fitness functions
  /system-and-database-design:diagram <desc> --format=X      - generate Mermaid / Excalidraw / DBML
  design-principles               - auto-triggers on CAP/ACID/sharding/consensus/etc.
Reference library: DDIA, Fundamentals of Software Architecture, Kimball.
EOF
