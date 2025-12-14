#!/usr/bin/env bash
#
# Office 365 Manager Runner
# Executes o365_manager script using uv-managed virtual environment
#
# Usage: run.sh [command] [args...]
# Example: run.sh list-emails --limit 10
#

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Ensure dependencies are installed
cd "$SCRIPT_DIR"
if [ ! -d ".venv" ]; then
    echo "Installing dependencies..." >&2
    uv sync --python "$(which python3)"
fi

# Run the Python script using uv
exec uv run "$SCRIPT_DIR/src/o365_manager.py" "$@"
