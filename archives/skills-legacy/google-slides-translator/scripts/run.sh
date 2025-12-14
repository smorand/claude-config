#!/usr/bin/env bash
#
# Generic Script Runner
# Executes Python scripts using uv-managed virtual environment
#
# Usage: run.sh <script_name> [args...]
# Example: run.sh translate_slides presentation_id all fr
#

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if script name is provided
if [ $# -lt 1 ]; then
    echo "Error: Script name required" >&2
    echo "Usage: run.sh <script_name> [args...]" >&2
    echo "Example: run.sh translate_slides presentation_id all fr" >&2
    exit 1
fi

# Get the script name and shift arguments
script="$1"
shift

# Ensure dependencies are installed
cd "$SCRIPT_DIR"
if [ ! -d ".venv" ]; then
    echo "Installing dependencies..." >&2
    uv sync --python "$(which python3)"
fi

# Run the Python script using uv
exec uv run "$SCRIPT_DIR/src/${script}.py" "$@"
