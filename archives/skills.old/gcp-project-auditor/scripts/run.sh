#!/bin/bash
# GCP Project Auditor - Run Script
# Usage: ./run.sh <project_id> [output_dir]

set -euo pipefail

PROJECT_ID="${1:-}"
OUTPUT_DIR="${2:-./audit-output}"

if [ -z "$PROJECT_ID" ]; then
    echo "Usage: $0 <project_id> [output_dir]"
    echo ""
    echo "Example: $0 oa-data-btdpexploration-np ./audit-results"
    exit 1
fi

# Navigate to script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Install dependencies if needed
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
uv pip install -e .

# Run the audit
echo ""
echo "Starting GCP Project Audit for: $PROJECT_ID"
echo "Output directory: $OUTPUT_DIR"
echo ""

python src/audit_project.py "$PROJECT_ID" --output-dir "$OUTPUT_DIR"

echo ""
echo "Audit complete! Results saved to: $OUTPUT_DIR"
