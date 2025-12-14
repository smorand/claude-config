# Project Structure and Configuration

Comprehensive guide for project structure and configuration in personal projects.

## Directory Structure

### Basic Project Structure
```
my-project/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── data_service.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── data_repository.py
│   └── utils/
│       ├── __init__.py
│       ├── common.py
│       └── http.py
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_services.py
├── .env.example
├── .gitignore
├── .pylintrc
├── pyproject.toml
├── README.md
└── CLAUDE.md
```

### Key Differences from BTDP Framework
- **Single `src/` directory**: All source code in one location
- **No `modules/` directory**: Unlike BTDP Framework projects
- **Flat structure**: Simpler organization for personal projects

## pyproject.toml Configuration

### Complete Example
```toml
[project]
name = "my-project"
version = "0.1.0"
description = "Project description"
authors = [
    {name = "Sebastien MORAND", email = "sebastien.morand@loreal.com"}
]
readme = "README.md"
requires-python = ">=3.13"
license = {text = "MIT"}

dependencies = [
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    "aiohttp>=3.9.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.11.0",
    "pylint>=3.0.0",
    "bandit>=1.7.5",
    "safety>=2.3.0",
]

cli = [
    "typer>=0.9.0",
    "rich>=13.7.0",
]

[project.scripts]
mycli = "src.main:app"

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 120
target-version = ["py313"]
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.venv
  | build
  | dist
)/
'''

[tool.pylint.messages_control]
max-line-length = 120
disable = []

[tool.pylint.format]
max-line-length = 120

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

### Minimal Example
```toml
[project]
name = "simple-project"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = []

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 120
```

## UV Package Manager

### Installation
```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Common Commands

#### Project Initialization
```bash
# Create new project directory
mkdir my-project && cd my-project

# Create pyproject.toml
cat > pyproject.toml << 'EOF'
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = []

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"
EOF

# Create source structure
mkdir -p src tests

# Initialize uv
uv sync
```

#### Dependency Management
```bash
# Sync dependencies from pyproject.toml
uv sync

# Add production dependency
uv add fastapi
uv add "uvicorn[standard]"

# Add development dependency
uv add --dev pytest
uv add --dev black

# Add optional dependency group
uv add --optional cli typer

# Remove dependency
uv remove package-name

# Update specific dependency
uv add fastapi@latest

# Update all dependencies
uv sync --upgrade
```

#### Running Applications
```bash
# Run Python script
uv run src/main.py

# Run with arguments
uv run src/main.py --help

# Run pytest
uv run pytest

# Run uvicorn
uv run uvicorn src.main:app --reload
```

#### Virtual Environment
```bash
# uv automatically manages virtual environment in .venv/
# No manual activation needed when using 'uv run'

# To activate manually (if needed):
source .venv/bin/activate  # Unix/macOS
.venv\Scripts\activate     # Windows
```

### UV vs Other Tools

#### UV vs pip
```bash
# pip
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install package-name

# uv (simpler, faster)
uv sync
uv add package-name
```

#### UV vs Poetry
```bash
# Poetry
poetry init
poetry add package-name
poetry install

# uv (faster, simpler)
# Create pyproject.toml manually
uv add package-name
uv sync
```

## Environment Variables

### .env File
```bash
# .env (never commit to git)
API_KEY=your-api-key-here
DATABASE_URL=postgresql://localhost/mydb
REDIS_URL=redis://localhost:6379
DEBUG=true
LOG_LEVEL=INFO
```

### .env.example
```bash
# .env.example (commit this to git)
API_KEY=your-api-key-here
DATABASE_URL=postgresql://localhost/mydb
REDIS_URL=redis://localhost:6379
DEBUG=false
LOG_LEVEL=INFO
```

### Loading Environment Variables

#### Using pydantic-settings
```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    api_key: str
    database_url: str
    redis_url: str = "redis://localhost:6379"
    debug: bool = False
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    return Settings()

# Usage
settings = get_settings()
print(settings.api_key)
```

#### Using python-dotenv
```python
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Access variables
api_key = os.getenv("API_KEY")
debug = os.getenv("DEBUG", "false").lower() == "true"
```

## Git Configuration

### .gitignore
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.venv/
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Environment variables
.env
.env.local

# Testing
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db

# UV
uv.lock

# Logs
*.log
```

## Pylint Configuration

### .pylintrc
```ini
[MASTER]
# Python 3.13
py-version=3.13

# Use multiple processes for faster checking
jobs=4

# Ignore patterns
ignore=CVS,.git,__pycache__,.venv,venv

[MESSAGES CONTROL]
# NO DISABLING - must achieve 10/10
disable=

[FORMAT]
# Maximum line length
max-line-length=120

# String used for indentation
indent-string='    '

# Maximum number of lines in a module
max-module-lines=1000

[BASIC]
# Good variable names
good-names=i,j,k,ex,_,id,db,app

# Minimum line length for functions/classes needing a docstring
docstring-min-length=10

[DESIGN]
# Maximum number of arguments for function/method
max-args=5

# Maximum number of attributes for a class
max-attributes=7

# Maximum number of boolean expressions in an if statement
max-bool-expr=5

# Maximum number of branch for function/method body
max-branches=12

# Maximum number of locals for function/method body
max-locals=15

# Maximum number of return/yield for function/method body
max-returns=6

# Maximum number of statements in function/method body
max-statements=50

[SIMILARITIES]
# Minimum lines number of a similarity
min-similarity-lines=4

# Ignore comments when computing similarities
ignore-comments=yes

# Ignore docstrings when computing similarities
ignore-docstrings=yes

# Ignore imports when computing similarities
ignore-imports=yes
```

## README.md Template

```markdown
# Project Name

Brief description of what this project does.

## Features

- Feature 1
- Feature 2
- Feature 3

## Prerequisites

- Python 3.13+
- UV package manager

## Installation

\```bash
# Clone repository
git clone <repository-url>
cd my-project

# Sync dependencies
uv sync
\```

## Configuration

Copy `.env.example` to `.env` and configure:

\```bash
cp .env.example .env
# Edit .env with your settings
\```

## Usage

### Running the API
\```bash
uv run uvicorn src.main:app --reload
\```

### Running the CLI
\```bash
uv run src/main.py --help
\```

## Development

### Code Quality
\```bash
# Format code
black -l 120 src/

# Check quality
pylint src/
bandit -r src/
safety check
\```

### Testing
\```bash
uv run pytest
\```

## Project Structure

\```
src/
  ├── main.py          # Application entry point
  ├── models/          # Data models
  ├── services/        # Business logic
  ├── repositories/    # Data access layer
  └── utils/           # Utility functions
\```

## License

MIT License
```

## CLAUDE.md Template

```markdown
# Claude Implementation Guide

AI-focused documentation for development and maintenance.

## Project Overview

Brief description of project purpose and architecture.

## Technology Stack

- Python 3.13
- FastAPI / Typer
- UV package manager
- Key dependencies and their roles

## Architecture Decisions

### Dependency Injection
Explain how dependencies are managed and injected.

### Async/Await
Describe async patterns used in the project.

### Data Validation
How Pydantic models are used for validation.

## Common Workflows

### Adding New Endpoint (FastAPI)
1. Create Pydantic models in `src/models/`
2. Add route handler in `src/main.py`
3. Implement service logic in `src/services/`
4. Update tests

### Adding New Command (Typer)
1. Define command in `src/main.py`
2. Add type hints and help text
3. Implement command logic
4. Test with `uv run src/main.py command --help`

## Development Guidelines

### Code Quality
- Always run `black -l 120 src/` after changes
- Ensure Pylint 10/10 score
- Zero Bandit security issues
- Zero Safety vulnerabilities

### Testing
How to run and write tests for this project.

## Troubleshooting

Common issues and solutions.
```

## Best Practices

1. **Use pyproject.toml** for all project configuration
2. **UV for dependency management** - faster and simpler than pip/poetry
3. **Keep .env out of git** - use .env.example for reference
4. **Single src/ directory** - no modules/ subdirectory
5. **Python 3.13 required** - update old projects
6. **Complete .gitignore** - exclude all generated files
7. **Proper .pylintrc** - configure for 10/10 score
8. **Document in README.md** - user-focused documentation
9. **Document in CLAUDE.md** - AI-focused implementation guide
