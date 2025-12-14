# Script Patterns for Skills

## Recommended Pattern: run.sh + uv + pyproject.toml

This pattern provides isolated Python environments with automatic dependency management.

### Directory Structure

```
skill-name/
└── scripts/
    ├── run.sh              # Generic script runner
    ├── pyproject.toml      # Python dependencies
    ├── .venv/              # Auto-created by uv (gitignored)
    └── src/
        ├── script1.py
        └── script2.py
```

### run.sh Template

```bash
#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if script name provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <script_name> [args...]"
    echo "Available scripts: $(ls src/*.py | xargs -n1 basename | sed 's/\.py$//' | tr '\n' ' ')"
    exit 1
fi

SCRIPT_NAME="$1"
shift

# Run script with uv (auto-creates .venv and installs dependencies)
uv run "src/${SCRIPT_NAME}.py" "$@"
```

### pyproject.toml Template

```toml
[project]
name = "skill-scripts"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    # Add your dependencies here
    # "requests>=2.31.0",
]

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"
```

### Usage Example

```bash
# First run: Creates .venv, installs dependencies, runs script
~/.claude/skills/my-skill/scripts/run.sh my_script arg1 arg2

# Subsequent runs: Uses existing .venv, runs instantly
~/.claude/skills/my-skill/scripts/run.sh my_script arg1 arg2
```

### Benefits

1. **Isolated environments**: Each skill has own .venv
2. **Auto dependency management**: uv handles everything
3. **No manual setup**: User doesn't install dependencies
4. **Fast**: uv is faster than pip
5. **Reliable**: Same versions every time
6. **Multiple scripts**: One run.sh for all scripts in skill

### Real-World Examples

See these skills for working implementations:
- `pdf-extractor/scripts/`
- `speech-to-text/scripts/`
- `google-slides-translator/scripts/`
- `video-creator/scripts/` (if applicable)

## Alternative Pattern: Standalone Python Script

For simple scripts without dependencies:

```python
#!/usr/bin/env python3
"""Simple standalone script"""
import sys

def main():
    print(f"Hello {sys.argv[1] if len(sys.argv) > 1 else 'World'}!")

if __name__ == "__main__":
    main()
```

Make executable: `chmod +x script.py`

Use when:
- No external dependencies
- Single, simple operation
- Standard library only
