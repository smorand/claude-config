### Personal Projects (Independent)

**Use Case:** All non-BTDP projects (utilities, tools, applications).

#### Python Projects Requirements
- **Git:** Repository initialization mandatory (`git init`).
- **Dependencies:** `uv` for management (`uv add <package>`).
- **Dependency Injection:** Implement in `main()` function.
- **Framework:** FastAPI for APIs, React.js for web frontends.
- **CLI:** Use typer for CLI management.
- **Build System:** Use Hatchling for packaging and distribution.

#### Commands
```bash
uv sync && uv run {package_name}  # Install dependencies and run CLI (using pyproject.toml script).
uv sync && uv run src/main.py     # Install dependencies and run API server directly.
```

```bash
uv run pip install -U -e .     # Local install on the system with auto update.

uv run pip install -U .        # Local install on the system standalone.
```

#### Package Structure and Installation Requirements

**Critical Installation Requirements:**
- **⚠️ Entry Point Naming:** Main entry file MUST have unique project-specific name (e.g., `simplerag.py`, `projectname.py`) - NEVER use generic `main.py` to avoid global installation conflicts
- **Python Path Management:** Entry point file MUST include `sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))` before any local imports
- **Package Initialization:** ALL directories must have `__init__.py` files (including src/ and all subdirectories)
- **Build Configuration:** Use Hatchling with proper wheel configuration in pyproject.toml
- **Entry Point Configuration:** pyproject.toml scripts entry must match unique filename: `"projectname:main"` not `"main:main"`

**Structure:**
```
personal-python-project/.
├── .gitignore                  # Standard gitignore (mandatory).
├── README.md                   # Installation/usage instructions.
├── CLAUDE.md                   # Global CLAUDE.md instruction for the projects based on the framework global.
├── pyproject.toml              # UV configuration with Hatchling build system and proper scripts entry
├── Dockerfile                  # Required if using Terraform.
└── src/                        # Python source code folder. MUST contain __init__.py for proper packaging
    ├── __init__.py             # Package initialization file (MANDATORY for installation)
    ├── projectname.py          # ⚠️ UNIQUE entry point name (NOT main.py) to avoid conflicts
    ├── commons/                # Technical classes (APIs, databases, utils).
    │   ├── __init__.py         # Package initialization (MANDATORY)
    │   ├── api/                # API wrapper. Only to hide the API call complexity.
    │   │   └── __init__.py     # Package initialization (MANDATORY)
    │   ├── database/           # Database wrapper, CRUD oriented functionality
    │   │   └── __init__.py     # Package initialization (MANDATORY)
    │   ├── models/             # Common models definition, transversal to all functionalities.
    │   │   └── __init__.py     # Package initialization (MANDATORY)
    │   └── utils/              # Various utilities classes and functions.
    │       └── __init__.py     # Package initialization (MANDATORY)
    └── {functionality}/        # One folder per functionality
        ├── __init__.py         # Package initialization (MANDATORY)
        ├── cli.py              # sub-command for this functionality
        ├── service.py          # Main business logic functionality
        ├── controller.py       # Controller for API and WebApp input/output validation
        ├── models.py           # Schema definitions for input and output
        └── anything.py         # Additional functionality specific code
```

#### Required pyproject.toml Configuration

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "your-project-name"
version = "0.1.0"
description = "Your project description"
authors = [
    {name = "Sebastien MORAND", email = "sebastien.morand@loreal.com"}
]
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "typer>=0.9.0",
    # Add your dependencies here
]

[project.scripts]
your-cli-name = "yourproject:main"  # Must match your unique entry file name (NOT main.py)

[tool.hatch.build.targets.wheel]
packages = ["src"]

[tool.hatch.build.targets.wheel.sources]
"src" = ""

[tool.black]
line-length = 120
target-version = ["py311"]
```

#### Required main.py Pattern

**⚠️ CRITICAL: main.py Naming Requirements**

**Main Entry File Naming:** The main entry point file MUST have a unique name related to your specific project to avoid global installation conflicts. When multiple packages install `main.py` files, they conflict with each other in the global Python installation.

**Recommended Naming Pattern:**
- Use project-specific names: `simplerag.py`, `yourproject.py`, `projectname.py`
- **NEVER** use generic names like `main.py` for Personal Projects intended for system-wide installation
- Update pyproject.toml entry point accordingly: `"yourproject:main"` or `"projectname:main"`

**Entry Point Pattern:** Call the typer app directly instead of using wrapper functions to avoid callback confusion.

```python
"""Main entry point for your CLI application."""

import logging
import os
import sys
import warnings
from datetime import datetime
from pathlib import Path

import typer

# Add src directory to Python path for local imports (CRITICAL for installation)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Local imports (after path modification)
# pylint: disable=wrong-import-position
from your_functionality.cli import app as your_app

app = typer.Typer(
    name="your-cli",
    help="Your CLI description",
    no_args_is_help=True,
)

app.add_typer(your_app, name="")

def setup_logging(debug: bool = False) -> str:
    """Setup logging configuration with file output only."""
    log_dir = Path.home() / ".logs"
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"yourproject.log.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter("[ %(asctime)s ] %(levelname)7s: %(module)s.%(funcName)s: %(message)s"))
    
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, handlers=[file_handler], force=True)
    
    return str(log_file)

@app.callback()
def callback(
    debug: bool = typer.Option(False, "--debug", help="Enable debug logging"),
) -> None:
    """Your CLI description."""
    log_file = setup_logging(debug)
    typer.echo(f"Logging to: {log_file}", err=True)

def main() -> None:
    """Entry point for the CLI when installed as a package."""
    app()

if __name__ == "__main__":
    app()
```

#### Installation Testing Process

Personal projects support two installation approaches depending on the use case:

##### 1. Development Installation (UV Environment - Isolated)
For development work with isolated dependencies:

```bash
# Install dependencies in UV virtual environment
uv sync

# Run CLI within UV environment
uv run your-cli-name --help
uv run your-cli-name command --option value

# Install as editable package in UV environment
uv add --editable . --dev
```

**Use this approach when:**
- Working on the project locally
- Need dependency isolation
- Building/testing in CI/CD
- Want reproducible builds

##### 2. System-wide Installation (Like dwd project)
For system-wide CLI availability:

```bash
# Install to system Python with dependencies
pip install -e .

# CLI becomes available globally
your-cli-name --help
your-cli-name command --option value
```

**Use this approach when:**
- Want CLI available system-wide
- Similar behavior to existing tools like `oadwd`
- Production deployment
- End-user installation

##### Key Differences

| Aspect | UV Environment | System-wide |
|--------|----------------|-------------|
| **Installation** | `uv sync` + `uv add --editable . --dev` | `pip install -e .` |
| **Usage** | `uv run your-cli-name` | `your-cli-name` directly |
| **Dependencies** | Isolated in `.venv/` | Installed to system Python |
| **Availability** | Project directory only | Available globally |
| **Entry Point** | Works with both patterns | Uses standard `"main:main"` |

##### Troubleshooting Installation Issues

**Problem:** `uv run your-cli-name` works but `your-cli-name` doesn't work after system installation
**Solution:** Dependencies are only in UV environment. Run `pip install -e .` to install to system Python

**Problem:** CLI entry point not found after installation  
**Solution:** Check that `[project.scripts]` in pyproject.toml points to correct function

**Problem:** Import errors after system installation
**Solution:** Ensure all `__init__.py` files exist and sys.path modification is in main.py

**Problem:** CLI entry point calls Typer callback instead of app launcher (system installation fails silently)
**Solution:** Entry point must call the CLI app, not a Typer callback function. Use this pattern:
```python
# ❌ WRONG: Don't use Typer callback as entry point
@app.callback()
def main():  # This is a callback, not an entry point
    pass

# ✅ CORRECT: Separate callback and entry point
@app.callback() 
def callback():  # Typer callback for options
    pass

def main():  # Entry point for pip installation
    app()

if __name__ == "__main__":
    app()
```

**Problem:** Global CLI installation conflicts - CLI works in project directory but not system-wide
**Solution:** Multiple packages with `main.py` files conflict when installed globally. Use unique entry point names:
- **Root Cause:** When multiple packages install `main.py` files, they overwrite each other in the global Python installation
- **Solution:** Use project-specific names: `simplerag.py`, `projectname.py`, etc.
- **Configuration:** Update pyproject.toml: `your-cli = "projectname:main"` (not `"main:main"`)
- **Pattern:** Call typer app directly in main() function instead of using wrapper functions

Personal projects use pyproject.toml and uv for development, but can be installed system-wide like traditional Python packages.

#### Common Installation Issues and Solutions

**Problem:** `ModuleNotFoundError: No module named 'commons.xxx'` after installation
**Solution:** Ensure all directories have `__init__.py` files and main.py includes the sys.path modification

**Problem:** CLI script not found after installation
**Solution:** Verify [project.scripts] entry in pyproject.toml points to correct entry point

**Problem:** Import errors during runtime
**Solution:** Check that Hatchling build configuration properly packages src/ directory
