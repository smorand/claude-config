# Code Quality Standards

Comprehensive guide for code quality standards in personal projects.

## Code Formatting

### Black (MANDATORY)
**Always run Black after ANY Python modifications**

```bash
# Format source directory
black -l 120 src/

# Format specific file
black -l 120 src/main.py

# Check formatting without changes
black --check -l 120 src/
```

### Configuration
Add to `pyproject.toml`:
```toml
[tool.black]
line-length = 120
target-version = ["py313"]
include = '\.pyi?$'
```

## Import Organization

### Standard Order
```python
# 1. Standard library imports
import os
import sys
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime

# 2. Third-party imports
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import typer
from rich.console import Console
import aiohttp

# 3. Local imports
from src.utils.common import validate_input
from src.services.data_service import DataService
from src.models.user import UserModel
```

### Import Guidelines
- Group imports by category (standard, third-party, local)
- Sort alphabetically within each group
- Use explicit imports when possible
- Avoid wildcard imports (`from module import *`)

## String Handling

### F-strings for Interpolation
```python
# Good: Use f-strings for interpolation
name = "John"
age = 30
message = f"Hello {name}, you are {age} years old"

# Bad: Using % or .format()
message = "Hello %s, you are %d years old" % (name, age)  # Don't use for interpolation
message = "Hello {}, you are {} years old".format(name, age)  # Don't use
```

### %-style for Logging
```python
import logging

logger = logging.getLogger(__name__)

# Good: Use % style for logging
logger.info("Processing user %s with ID %d", username, user_id)
logger.error("Failed to process %s: %s", item_name, error_message)

# Bad: Using f-strings in logging
logger.info(f"Processing user {username} with ID {user_id}")  # Don't use
```

### Why Different Styles?
- **F-strings**: Evaluated immediately, best for general string interpolation
- **%-style**: Lazy evaluation, only formats if log level is enabled (performance benefit)

## Pylint (MANDATORY: 10/10)

### Running Pylint
```bash
# Check entire source
pylint src/

# Check specific file
pylint src/main.py

# Generate reports
pylint --reports=y src/
```

### Configuration
Create `.pylintrc`:
```ini
[MASTER]
max-line-length=120
disable=

[FORMAT]
indent-string='    '

[MESSAGES CONTROL]
# NO DISABLING ALLOWED - must achieve 10/10
```

### Common Issues and Fixes

#### Missing Docstrings
```python
# Bad
def process_data(data):
    return data.strip()

# Good
def process_data(data: str) -> str:
    """
    Process input data by stripping whitespace.

    Args:
        data: Input string to process

    Returns:
        Processed string with whitespace removed
    """
    return data.strip()
```

#### Too Many Arguments
```python
# Bad: Too many arguments
def create_user(name, email, age, address, phone, city, country, zip_code):
    pass

# Good: Use data class or model
from pydantic import BaseModel

class UserData(BaseModel):
    name: str
    email: str
    age: int
    address: str
    phone: str
    city: str
    country: str
    zip_code: str

def create_user(user_data: UserData):
    """Create user with provided data"""
    pass
```

#### Line Too Long
```python
# Bad: Line exceeds 120 characters
result = some_function(argument1, argument2, argument3, argument4, argument5, argument6, argument7, argument8, argument9)

# Good: Break into multiple lines
result = some_function(
    argument1, argument2, argument3,
    argument4, argument5, argument6,
    argument7, argument8, argument9
)
```

## Bandit Security (MANDATORY: Zero Issues)

### Running Bandit
```bash
# Check entire source
bandit -r src/

# Generate detailed report
bandit -r src/ -f json -o bandit-report.json

# Exclude test files
bandit -r src/ --exclude src/tests/
```

### Common Security Issues

#### Hardcoded Secrets
```python
# Bad: Hardcoded credentials
API_KEY = "sk-1234567890abcdef"  # Security issue!
PASSWORD = "admin123"  # Security issue!

# Good: Use environment variables
import os

API_KEY = os.getenv("API_KEY")
PASSWORD = os.getenv("PASSWORD")
```

#### SQL Injection
```python
# Bad: String concatenation in SQL
user_id = request.get("user_id")
query = f"SELECT * FROM users WHERE id = {user_id}"  # SQL injection risk!

# Good: Use parameterized queries
query = "SELECT * FROM users WHERE id = :user_id"
result = await database.fetch_one(query=query, values={"user_id": user_id})
```

#### Insecure Random
```python
# Bad: Using random for security
import random
token = random.randint(1000, 9999)  # Insecure!

# Good: Use secrets module
import secrets
token = secrets.token_urlsafe(32)
```

### Documenting nosec
When `# nosec` is absolutely necessary:
```python
import subprocess

# This is safe because input is validated and sanitized above  # nosec B602
result = subprocess.call(["ls", validated_directory])
```

## Safety CLI (MANDATORY: Zero Vulnerabilities)

### Running Safety
```bash
# Check installed dependencies
safety check

# Check requirements file
safety check -r requirements.txt

# Generate detailed report
safety check --json
```

### Handling Vulnerabilities
1. **Update dependencies**: `uv add package@latest`
2. **Review alternatives**: Find secure replacements
3. **NO EXCEPTIONS**: All vulnerabilities must be resolved

## Type Hints

### Complete Type Hints
```python
from typing import List, Dict, Optional, Union, Any
from pathlib import Path

# Function type hints
def process_items(
    items: List[str],
    config: Dict[str, Any],
    output_path: Optional[Path] = None
) -> Dict[str, int]:
    """Process items with configuration"""
    result: Dict[str, int] = {}
    for item in items:
        result[item] = len(item)
    return result

# Class type hints
class DataProcessor:
    """Process data with configuration"""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config: Dict[str, Any] = config
        self.results: List[str] = []

    def process(self, data: str) -> bool:
        """Process data and return success status"""
        self.results.append(data)
        return True
```

## Docstrings

### Function Docstrings
```python
def calculate_total(
    items: List[float],
    tax_rate: float = 0.0,
    discount: Optional[float] = None
) -> float:
    """
    Calculate total price with tax and discount.

    Args:
        items: List of item prices
        tax_rate: Tax rate as decimal (default: 0.0)
        discount: Optional discount amount

    Returns:
        Total price after tax and discount

    Raises:
        ValueError: If tax_rate is negative
        ValueError: If discount exceeds total

    Examples:
        >>> calculate_total([10.0, 20.0], tax_rate=0.1)
        33.0
        >>> calculate_total([10.0, 20.0], discount=5.0)
        25.0
    """
    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative")

    subtotal = sum(items)
    total = subtotal * (1 + tax_rate)

    if discount:
        if discount > total:
            raise ValueError("Discount exceeds total")
        total -= discount

    return total
```

### Class Docstrings
```python
class UserService:
    """
    Service for managing user operations.

    This service handles user creation, retrieval, and validation.
    It integrates with the user repository for data persistence.

    Attributes:
        repository: User repository instance
        validator: User validator instance

    Example:
        >>> repository = UserRepository()
        >>> service = UserService(repository)
        >>> user = await service.create_user("john@example.com")
    """

    def __init__(self, repository: UserRepository) -> None:
        """
        Initialize user service.

        Args:
            repository: User repository for data operations
        """
        self.repository = repository
        self.validator = UserValidator()
```

## Async/Await Patterns

### Use aiohttp Instead of requests
```python
# Bad: Synchronous HTTP
import requests
response = requests.get("https://api.example.com/data")

# Good: Async HTTP
import aiohttp

async def fetch_data(url: str) -> dict:
    """Fetch data asynchronously"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

### Async Context Managers
```python
import aiofiles

async def read_file(file_path: str) -> str:
    """Read file asynchronously"""
    async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
        content = await f.read()
    return content

async def write_file(file_path: str, content: str) -> None:
    """Write file asynchronously"""
    async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
        await f.write(content)
```

## Error Handling

### Proper Exception Handling
```python
import logging

logger = logging.getLogger(__name__)

async def process_user(user_id: str) -> dict:
    """
    Process user data.

    Args:
        user_id: User identifier

    Returns:
        Processed user data

    Raises:
        ValueError: If user_id is invalid
        HTTPException: If user not found
    """
    try:
        # Validate input
        if not user_id:
            raise ValueError("User ID cannot be empty")

        # Process
        user = await fetch_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return process_data(user)

    except ValueError as e:
        logger.error("Validation error for user %s: %s", user_id, e)
        raise

    except HTTPException:
        logger.warning("User not found: %s", user_id)
        raise

    except Exception as e:
        logger.exception("Unexpected error processing user %s", user_id)
        raise
```

## Quality Check Workflow

### Complete Quality Check
```bash
# 1. Format code
black -l 120 src/

# 2. Check pylint
pylint src/

# 3. Check security
bandit -r src/

# 4. Check vulnerabilities
safety check

# 5. Run tests (if available)
uv run pytest
```

### Pre-commit Hook
Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash

# Format code
black -l 120 src/

# Run quality checks
pylint src/
if [ $? -ne 0 ]; then
    echo "Pylint failed - commit aborted"
    exit 1
fi

bandit -r src/
if [ $? -ne 0 ]; then
    echo "Bandit security check failed - commit aborted"
    exit 1
fi

safety check
if [ $? -ne 0 ]; then
    echo "Safety vulnerability check failed - commit aborted"
    exit 1
fi

echo "All quality checks passed"
exit 0
```

## Best Practices Summary

1. **Always run Black** after ANY Python modifications
2. **Achieve Pylint 10/10** - no exceptions
3. **Zero Bandit issues** - resolve all security warnings
4. **Zero Safety vulnerabilities** - update or replace dependencies
5. **Use f-strings** for interpolation, **%-style** for logging
6. **Complete type hints** for all functions and classes
7. **Proper docstrings** following Google or NumPy style
8. **Async/await** for all I/O operations
9. **No hardcoded secrets** - use environment variables
10. **Test before commit** - run all quality checks
