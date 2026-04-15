#!/bin/bash
# cleancode plugin — UserPromptSubmit hook
# Fires every time the user submits a prompt. Detects plan-mode signals
# and, when clean code rules are active in the project, reminds Claude
# to incorporate clean code considerations into any plan.
#
# Coexistence: Claude Code merges UserPromptSubmit hooks from every enabled
# plugin and runs them in parallel. This hook only emits a systemMessage —
# it never blocks — so it's safe to stack alongside superpowers, plugin-dev,
# or any other plugin's hooks.

set -eo pipefail

# Guard: CLAUDE_PROJECT_DIR must be set
if [ -z "${CLAUDE_PROJECT_DIR:-}" ]; then
  exit 0
fi

RULES_FILE="${CLAUDE_PROJECT_DIR}/.cleancode-rules.md"

# Signal 1: project has cleancode rules active
if [ ! -f "$RULES_FILE" ]; then
  exit 0
fi

# Read the prompt JSON from stdin (best-effort; if jq isn't available we skip)
PROMPT=""
TRANSCRIPT_PATH=""
if command -v jq >/dev/null 2>&1; then
  INPUT=$(cat 2>/dev/null || true)
  if [ -n "$INPUT" ]; then
    PROMPT=$(echo "$INPUT" | jq -r '.user_prompt // empty' 2>/dev/null || true)
    TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path // empty' 2>/dev/null || true)
  fi
fi

# Signal 2: plan-mode indicators in the prompt text (case-insensitive)
PROMPT_LC=$(echo "$PROMPT" | tr '[:upper:]' '[:lower:]')

is_plan_mode=0

if echo "$PROMPT_LC" | grep -qE '(plan mode|make a plan|make me a plan|design a plan|write a plan|planning mode|let'"'"'s plan)'; then
  is_plan_mode=1
fi

# Signal 3: recent EnterPlanMode in transcript
if [ "$is_plan_mode" -eq 0 ] && [ -n "$TRANSCRIPT_PATH" ] && [ -f "$TRANSCRIPT_PATH" ]; then
  if tail -n 200 "$TRANSCRIPT_PATH" 2>/dev/null | grep -q 'EnterPlanMode'; then
    is_plan_mode=1
  fi
fi

# Signal 4: a plan file modified in the last 10 minutes (Windows + Unix friendly)
PLANS_DIR="${USERPROFILE:-$HOME}/.claude/plans"
if [ "$is_plan_mode" -eq 0 ] && [ -d "$PLANS_DIR" ]; then
  # find may not exist on all Windows bash shells; guard the call
  if command -v find >/dev/null 2>&1; then
    recent=$(find "$PLANS_DIR" -maxdepth 1 -type f -name '*.md' -mmin -10 2>/dev/null | head -n 1 || true)
    if [ -n "$recent" ]; then
      is_plan_mode=1
    fi
  fi
fi

if [ "$is_plan_mode" -eq 0 ]; then
  exit 0
fi

# Emit a short systemMessage reminder (JSON on stdout)
cat <<'EOF'
{"systemMessage": "cleancode: 15 clean code rules active in this project — include clean code considerations (file size, function size, interfaces, error handling, tests, Law of Demeter, folder structure) in any plan. See .cleancode-rules.md for thresholds."}
EOF

exit 0
