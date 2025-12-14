#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if script name provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <script_name> [args...]"
    echo "Available scripts: $(ls src/*.py 2>/dev/null | xargs -n1 basename | sed 's/\.py$//' | tr '\n' ' ')"
    exit 1
fi

SCRIPT_NAME="$1"
shift

# Run script with uv (auto-creates .venv and installs dependencies)
uv run "src/${SCRIPT_NAME}.py" "$@"
