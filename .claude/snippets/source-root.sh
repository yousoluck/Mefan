#!/usr/bin/env bash
# .claude/snippets/source-root.sh
#
# Standard ROOT resolution for all mefan agents/commands/hooks.
# Usage: source "$(dirname "${BASH_SOURCE[0]}")/../snippets/source-root.sh"
#
# Resolution order:
#   1. Environment variable $ROOT (if already set and valid, no-op)
#   2. .claude/project.conf (preferred)
#   3. Hardcoded fallback (development only, prints WARN to stderr)

if [ -n "${ROOT:-}" ] && [ -d "$ROOT/.claude" ]; then
    # Already set by caller, validate and return
    :
else
    # Locate project.conf via this script's location
    _SOURCE_ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    _CONF_FILE="$_SOURCE_ROOT_DIR/../project.conf"

    if [ -f "$_CONF_FILE" ]; then
        # shellcheck source=/dev/null
        source "$_CONF_FILE"
    else
        # Hardcoded fallback (warns to stderr)
        echo "[source-root.sh] WARN: project.conf not found at $_CONF_FILE, using hardcoded fallback" >&2
        export ROOT="/mnt/d/pycharmprojects/Mefan"
        export SCENARIO=upgrade
        export CURRENT_STAGE=0
        export GRAPHIFY_OUT="$ROOT/graphify-out"
        export SKILLS_DIR="$ROOT/.claude/skills"
        export TEMPLATE_DIR="$ROOT/.claude/templates"
        export HOOKS_DIR="$ROOT/.claude/hooks"
        export SCRIPTS_DIR="$ROOT/.claude/agents/scripts"
        export LOGS_DIR="$ROOT/logs"
        export ITERATIONS_DIR="$ROOT/.claude/iterations"
    fi
    unset _SOURCE_ROOT_DIR _CONF_FILE
fi

# Sanity check
if [ ! -d "$ROOT/.claude" ]; then
    echo "[source-root.sh] ERROR: \$ROOT=$ROOT does not contain .claude/ directory" >&2
    return 1 2>/dev/null || exit 1
fi
