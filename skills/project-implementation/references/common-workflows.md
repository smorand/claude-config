# Common Workflows

Comprehensive guide for common development workflows in personal projects.

## Creating New Project

### From Scratch

#### 1. Initialize Project Directory
```bash
# Create and enter project directory
mkdir my-project && cd my-project
```

#### 2. Create pyproject.toml
```bash
cat > pyproject.toml << 'EOF'
[project]
name = "my-project"
version = "0.1.0"
description = "Project description"
authors = [
    {name = "Sebastien MORAND", email = "sebastien.morand@loreal.com"}
]
requires-python = ">=3.13"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "black>=23.11.0",
    "pylint>=3.0.0",
    "bandit>=1.7.5",
    "safety>=2.3.0",
]

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 120

[tool.pylint.messages_control]
max-line-length = 120
EOF
```

#### 3. Create Directory Structure
```bash
# Create source and test directories
mkdir -p src/{models,services,repositories,utils} tests

# Create __init__.py files
touch src/__init__.py
touch src/models/__init__.py
touch src/services/__init__.py
touch src/repositories/__init__.py
touch src/utils/__init__.py
touch tests/__init__.py
```

#### 4. Initialize UV and Dependencies
```bash
# Sync dependencies
uv sync

# Add dependencies based on project type
# For API projects:
uv add fastapi uvicorn pydantic pydantic-settings aiohttp

# For CLI projects:
uv add typer rich

# Add dev dependencies
uv add --dev pytest pytest-asyncio black pylint bandit safety
```

#### 5. Create Configuration Files

**Create .env.example:**
```bash
cat > .env.example << 'EOF'
# API Configuration
API_KEY=your-api-key-here
DATABASE_URL=postgresql://localhost/mydb

# Application Settings
DEBUG=false
LOG_LEVEL=INFO
EOF
```

**Create .gitignore:**
```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
.venv/
*.egg-info/

# Environment
.env

# IDE
.vscode/
.idea/

# Testing
.pytest_cache/
.coverage

# OS
.DS_Store
EOF
```

#### 6. Create Initial Application

**For FastAPI:**
```bash
cat > src/main.py << 'EOF'
from fastapi import FastAPI

app = FastAPI(
    title="My Project",
    version="0.1.0",
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF
```

**For Typer CLI:**
```bash
cat > src/main.py << 'EOF'
import typer

app = typer.Typer()

@app.command()
def hello(name: str = typer.Option(..., help="Your name")):
    """Say hello"""
    typer.echo(f"Hello {name}!")

if __name__ == "__main__":
    app()
EOF
```

#### 7. Initialize Git
```bash
git init
git add .
git commit -S -m "[STRY0000000](feat) Initial project setup"
```

#### 8. Create Documentation
```bash
# Create README.md (see project-structure.md for template)
# Create CLAUDE.md (see project-structure.md for template)
```

## Adding New Feature

### 1. Create Feature Branch
```bash
git checkout -b feat/STRY1234567/add-user-management
```

### 2. Add Required Dependencies
```bash
# If new dependencies needed
uv add new-package-name

# Update dev dependencies if needed
uv add --dev new-dev-package
```

### 3. Implement Feature

#### For FastAPI Endpoint
```bash
# 1. Create model
cat > src/models/user.py << 'EOF'
from pydantic import BaseModel, Field

class UserRequest(BaseModel):
    name: str = Field(..., min_length=1)
    email: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
EOF

# 2. Create service
cat > src/services/user_service.py << 'EOF'
from src.models.user import UserRequest, UserResponse

class UserService:
    """User management service"""

    async def create_user(self, user: UserRequest) -> UserResponse:
        """Create new user"""
        # Implementation
        pass
EOF

# 3. Add endpoint to main.py
# Edit src/main.py to add new route
```

#### For Typer Command
```bash
# Edit src/main.py to add new command
# Add proper type hints and help text
# Implement command logic
```

### 4. Format and Quality Check
```bash
# Format code
black -l 120 src/

# Quality checks
pylint src/
bandit -r src/
safety check
```

### 5. Test Feature
```bash
# For API
uv run uvicorn src.main:app --reload
# Test endpoints

# For CLI
uv run src/main.py command --help
# Test commands
```

### 6. Update Documentation
```bash
# Update README.md with new feature
# Update CLAUDE.md with implementation details
```

### 7. Commit Changes
```bash
git add .
git commit -S -m "[STRY1234567](feat) Add user management feature"
git push -u origin feat/STRY1234567/add-user-management
```

## Modifying Existing Project

### 1. Ensure Python 3.13 Compatibility
```bash
# Check pyproject.toml
# Verify requires-python = ">=3.13"

# Update if needed
# Edit pyproject.toml
```

### 2. Update Dependencies
```bash
# Sync existing dependencies
uv sync

# Update all dependencies to latest
uv sync --upgrade

# Or update specific dependency
uv add package-name@latest
```

### 3. Apply DRY Principle

#### Identify Duplication
```bash
# Search for similar code patterns
grep -r "def process_" src/
```

#### Extract to Utility
```python
# Before: Duplicated code in multiple files
# file1.py
def process_data(data):
    cleaned = data.strip()
    validated = validate(cleaned)
    return validated

# file2.py
def process_input(input):
    cleaned = input.strip()
    validated = validate(cleaned)
    return validated

# After: Extracted to utility
# src/utils/common.py
def clean_and_validate(data: str) -> str:
    """Clean and validate input data"""
    cleaned = data.strip()
    return validate(cleaned)

# file1.py and file2.py
from src.utils.common import clean_and_validate
result = clean_and_validate(data)
```

### 4. Refactor to Async/Await
```python
# Before: Synchronous
import requests

def fetch_data(url: str) -> dict:
    response = requests.get(url)
    return response.json()

# After: Asynchronous
import aiohttp

async def fetch_data(url: str) -> dict:
    """Fetch data asynchronously"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

### 5. Quality Gates
```bash
# Format
black -l 120 src/

# Quality checks
pylint src/
bandit -r src/
safety check

# Fix any issues found
```

### 6. Update Documentation
```bash
# Update README.md
# Update CLAUDE.md
# Update inline documentation
```

## Git Workflow

### Standard Feature Development

#### 1. Create Branch
```bash
# Feature branch
git checkout -b feat/STRY1234567/feature-description

# Bug fix branch
git checkout -b fix/STRY1234567/bug-description

# Refactoring branch
git checkout -b clean/STRY1234567/refactor-description
```

#### 2. Make Changes
```bash
# Edit files
# Format: black -l 120 src/
# Quality check: pylint src/ && bandit -r src/ && safety check
```

#### 3. Commit
```bash
# Stage changes
git add .

# Commit with signed commit
git commit -S -m "[STRY1234567](feat) Add feature description"
```

#### 4. Push
```bash
# First push
git push -u origin feat/STRY1234567/feature-description

# Subsequent pushes
git push
```

#### 5. Create Pull Request
```bash
# Using gh CLI
gh pr create --title "[STRY1234567] Feature description" --body "## Summary
- Change 1
- Change 2

## Test Plan
- [ ] Tested functionality
- [ ] Quality checks passed"
```

#### 6. Merge (ALWAYS SQUASH)
```bash
# Squash merge feature → develop
gh pr merge --squash
```

### Hotfix Workflow

#### 1. Create Hotfix Branch from Main
```bash
git checkout main
git pull
git checkout -b hotfix/STRY1234567/critical-bug
```

#### 2. Fix and Test
```bash
# Make fixes
# Run quality checks
# Test thoroughly
```

#### 3. Commit and Push
```bash
git add .
git commit -S -m "[STRY1234567](fix) Fix critical bug"
git push -u origin hotfix/STRY1234567/critical-bug
```

#### 4. Create PR to Main
```bash
gh pr create --base main --title "[STRY1234567] Critical bug fix"
```

#### 5. After Merge, Backport to Develop
```bash
git checkout develop
git pull
git merge main
git push
```

## Testing Workflow

### Writing Tests

#### 1. Create Test File
```bash
# tests/test_user_service.py
cat > tests/test_user_service.py << 'EOF'
import pytest
from src.services.user_service import UserService
from src.models.user import UserRequest

@pytest.mark.asyncio
async def test_create_user():
    """Test user creation"""
    service = UserService()
    request = UserRequest(name="John", email="john@example.com")
    result = await service.create_user(request)
    assert result.name == "John"
EOF
```

#### 2. Run Tests
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_user_service.py

# Run with coverage
uv run pytest --cov=src tests/

# Run with verbose output
uv run pytest -v
```

### Test-Driven Development (TDD)

#### 1. Write Test First
```python
# tests/test_validator.py
def test_email_validation():
    """Test email validation"""
    assert validate_email("user@example.com") == True
    assert validate_email("invalid-email") == False
```

#### 2. Run Test (Should Fail)
```bash
uv run pytest tests/test_validator.py
# Test fails - function doesn't exist yet
```

#### 3. Implement Feature
```python
# src/utils/validator.py
import re

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))
```

#### 4. Run Test Again (Should Pass)
```bash
uv run pytest tests/test_validator.py
# Test passes
```

#### 5. Refactor
```bash
# Improve implementation if needed
# Tests ensure functionality remains correct
```

## Deployment Workflow

### Local Development
```bash
# API
uv run uvicorn src.main:app --reload --port 8000

# CLI
uv run src/main.py --help
```

### Production Preparation

#### 1. Version Bump
```bash
# Update version in pyproject.toml
# from version = "0.1.0"
# to version = "0.2.0"
```

#### 2. Quality Check
```bash
black -l 120 src/
pylint src/
bandit -r src/
safety check
uv run pytest
```

#### 3. Build
```bash
# Build package
python -m build

# Creates:
# dist/my-project-0.2.0.tar.gz
# dist/my_project-0.2.0-whl
```

#### 4. Tag Release
```bash
git tag -s v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0
```

## Troubleshooting Workflows

### Dependency Issues
```bash
# Clear UV cache
uv cache clean

# Remove .venv and rebuild
rm -rf .venv
uv sync
```

### Quality Check Failures

#### Pylint Issues
```bash
# Get detailed report
pylint --reports=y src/

# Check specific file
pylint src/main.py
```

#### Bandit Issues
```bash
# Detailed report
bandit -r src/ -f json

# Check specific severity
bandit -r src/ -ll  # Low and above
```

#### Safety Vulnerabilities
```bash
# Full report
safety check --full-report

# Update vulnerable package
uv add package-name@latest
```

### Import Errors
```bash
# Verify __init__.py files exist
find src -type d -exec ls -la {}/\_\_init\_\_.py \;

# Check Python path
uv run python -c "import sys; print('\n'.join(sys.path))"
```

## Best Practices Summary

1. **Always create feature branches** - never commit to main/develop directly
2. **Quality check before commit** - format, pylint, bandit, safety
3. **Signed commits** - use `git commit -S`
4. **Squash merge** - keep history clean
5. **Update documentation** - README.md and CLAUDE.md
6. **Test before push** - run pytest if tests exist
7. **DRY principle** - eliminate duplication during refactoring
8. **Async/await** - refactor sync code to async when modifying
9. **Type hints** - add complete type hints to all new code
10. **Python 3.13** - ensure compatibility when updating projects
