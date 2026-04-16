#!/bin/bash
# cleancode plugin — SessionStart hook
# Fires every time a project session opens.
# Checks for .cleancode-rules.md and either reports it active
# or instructs Claude to run /cleancode:init.

set -eo pipefail

# Guard: CLAUDE_PROJECT_DIR must be set
if [ -z "${CLAUDE_PROJECT_DIR:-}" ]; then
  exit 0
fi

RULES_FILE="${CLAUDE_PROJECT_DIR}/.cleancode-rules.md"

if [ ! -f "$RULES_FILE" ]; then
  # No rules file found — instruct Claude to initialize
  echo "CLEANCODE: No .cleancode-rules.md found in this project."
  echo "Run /cleancode:init to set up clean code rules for all AI assistants."
  echo "This will create: .cleancode-rules.md, CLAUDE.md, .cursorrules, AGENTS.md"
else
  # Rules file exists — count the rules and report active
  echo "cleancode active — rules loaded from .cleancode-rules.md"
fi

exit 0
