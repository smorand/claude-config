#!/bin/bash

# Script runner for note-manager
# Usage: ./run.sh <script_name> [args...]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Initialize virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv
    echo "Installing dependencies..."
    uv pip install gkeepapi
fi

# Activate virtual environment and run the script
source .venv/bin/activate

SCRIPT_NAME=$1
shift

# Run the Python script
PYTHONPATH="$SCRIPT_DIR/src:$PYTHONPATH" python3 src/"${SCRIPT_NAME}.py" "$@"
