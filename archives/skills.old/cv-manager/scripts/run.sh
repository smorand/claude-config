#!/usr/bin/env bash
# Generic script runner using uv for isolated Python environments
# Usage: ./run.sh <script_name> [args...]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Get script name from first argument
if [ $# -eq 0 ]; then
    echo "Error: No script name provided"
    echo "Usage: $0 <script_name> [args...]"
    exit 1
fi

SCRIPT_NAME="$1"
shift

# Load environment variables in order of precedence
# 1. Current process.env (already loaded)
# 2. Skill-specific .env
if [ -f "$SKILL_DIR/.env" ]; then
    set -a
    source "$SKILL_DIR/.env"
    set +a
fi

# 3. Global skills .env
if [ -f "$HOME/.claude/skills/.env" ]; then
    set -a
    source "$HOME/.claude/skills/.env"
    set +a
fi

# 4. Global Claude .env
if [ -f "$HOME/.claude/.env" ]; then
    set -a
    source "$HOME/.claude/.env"
    set +a
fi

# Run the Python script using uv
cd "$SCRIPT_DIR"
exec uv run "src/${SCRIPT_NAME}.py" "$@"
