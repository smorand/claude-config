# Personal Project End-to-End Tests Implementation

## Purpose
Implement comprehensive end-to-end tests for Personal Projects using modern testing patterns. Use this command for testing CLI applications, APIs, and local services with proper dependency management via `uv`.

## Prerequisites
- Personal project with `pyproject.toml` and single `src/` directory structure
- `uv` dependency manager configured
- Deployed or deployable services/applications
- Test environment setup and configuration

## Protocol

### Input Arguments
```
$ARGUMENTS: End-to-end test scenarios for Personal Projects (CLI, API, local services)
```

You must follow this protocol completely. Create a Todo list according to these steps:

1. Analyze Personal Project architecture and identify test scenarios
2. Create modern test structure using `uv` and `pytest`
3. **Implement comprehensive application testing** (CLI, API, or service-specific)
4. Add proper dependency management and environment setup
5. **Implement error scenario testing** for edge cases and failures
6. **Test authentication and configuration management** 
7. Format test code with `black -l 120`
8. **Document test procedures** with clear execution instructions
9. Add test execution instructions for `uv` commands
10. Commit test implementation and push to remote

## Success Criteria
- [ ] **Comprehensive application testing** implemented with modern patterns
- [ ] **CLI/API/Service testing** following personal project standards
- [ ] **Error scenario coverage** for robust testing
- [ ] **Dependency management** via `pyproject.toml` with test extras
- [ ] Test environment configuration and setup procedures
- [ ] All test scenarios documented with examples
- [ ] Test code formatted with black -l 120
- [ ] Changes committed and pushed to remote

## Personal Project Test Architecture

### Test Structure

Personal projects use a clean, modern structure:

```
personal-project/
├── .gitignore                      # Standard gitignore (mandatory)
├── README.md                       # Installation/usage instructions
├── CLAUDE.md                       # Global CLAUDE.md instruction
├── pyproject.toml                  # UV configuration with Hatchling build system and test extras
├── Dockerfile                      # Required if using Terraform
├── e2e-tests/                      # End-to-end test folder
│   ├── __init__.py                 # Test package initialization (MANDATORY)
│   ├── conftest.py                 # Pytest configuration and fixtures
│   ├── test_cli_e2e.py            # CLI application testing
│   ├── test_api_e2e.py            # API endpoint testing
│   ├── test_integration_e2e.py     # Integration testing
│   └── fixtures/                   # Test data and configuration files
├── src/                            # Python source code folder with __init__.py (MANDATORY)
│   ├── __init__.py                 # Package initialization file (MANDATORY for installation)
│   ├── main.py                     # Entry point with main() function and sys.path configuration
│   ├── commons/                    # Technical classes (APIs, databases, utils)
│   │   ├── __init__.py             # Package initialization (MANDATORY)
│   │   ├── api/                    # API wrapper
│   │   │   └── __init__.py         # Package initialization (MANDATORY)
│   │   ├── database/               # Database wrapper
│   │   │   └── __init__.py         # Package initialization (MANDATORY)
│   │   ├── models/                 # Common models definition
│   │   │   └── __init__.py         # Package initialization (MANDATORY)
│   │   └── utils/                  # Various utilities classes and functions
│   │       └── __init__.py         # Package initialization (MANDATORY)
│   └── {functionality}/            # One folder per functionality
│       ├── __init__.py             # Package initialization (MANDATORY)
│       ├── cli.py                  # sub-command for this functionality
│       ├── service.py              # Main business logic functionality
│       ├── controller.py           # Controller for API and WebApp input/output validation
│       ├── models.py               # Schema definitions for input and output
│       └── anything.py             # Additional functionality specific code
└── tests/                          # Unit tests (separate from e2e)
    └── __init__.py                 # Package initialization (MANDATORY)
```

### Dependencies Management

**`pyproject.toml` configuration:**
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "your-personal-project"
version = "0.1.0"
description = "Your project description"
authors = [
    {name = "Sebastien MORAND", email = "sebastien.morand@loreal.com"}
]
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "typer>=0.9.0",
    "fastapi>=0.104.0",
    "aiohttp>=3.9.0",
]

[project.optional-dependencies]
e2e = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "requests>=2.31.0",
    "httpx>=0.25.0",
    "google-cloud-bigquery>=3.13.0",
    "google-cloud-storage>=2.13.0",
]

[project.scripts]
your-cli-name = "main:main"  # Standard entry point (works for both installation types)

[tool.hatch.build.targets.wheel]
packages = ["src"]

[tool.hatch.build.targets.wheel.sources]
"src" = ""

[tool.black]
line-length = 120
target-version = ["py311"]

[tool.pytest.ini_options]
testpaths = ["e2e-tests"]
asyncio_mode = "auto"
```

**Installation and execution:**
```bash
# Install with E2E test dependencies
uv sync --extra e2e

# Run all E2E tests
uv run pytest e2e-tests/

# Run specific test file
uv run pytest e2e-tests/test_cli_e2e.py

# Run with verbose output
uv run pytest e2e-tests/ -v -s

# Install for system-wide testing
pip install -e .[e2e]

# Run CLI command directly (after system installation)
your-cli-name --help
your-cli-name command --option value
```

## Test Implementation Patterns

### CLI Application Testing

```python
#!/usr/bin/env python3
"""
Personal Project CLI End-to-End Tests
====================================

Tests CLI application functionality with proper dependency management,
configuration handling, and error scenarios.
"""

import os
import sys
import tempfile
import shutil
import subprocess
import json
import pytest
from pathlib import Path
from typing import Dict, Any

class CLIApplicationE2ETest:
    """CLI application end-to-end testing for personal projects."""

    def __init__(self):
        """Initialize CLI test environment."""
        self.test_dir = None
        self.config_file = None
        
    def setup_test_environment(self) -> Dict[str, str]:
        """Setup isolated test environment."""
        # Create temporary directory for test isolation
        self.test_dir = tempfile.mkdtemp(prefix="cli_e2e_test_")
        
        # Create test configuration
        test_config = {
            "api_url": "http://localhost:8000",
            "output_dir": os.path.join(self.test_dir, "output"),
            "log_level": "INFO",
            "timeout": 30
        }
        
        # Create output directory
        os.makedirs(test_config["output_dir"], exist_ok=True)
        
        # Write test configuration file
        self.config_file = os.path.join(self.test_dir, "test_config.json")
        with open(self.config_file, 'w') as f:
            json.dump(test_config, f, indent=2)
            
        return test_config

    def cleanup_test_environment(self):
        """Clean up test environment."""
        if self.test_dir and os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def run_cli_command(self, args: list, expect_success: bool = True) -> subprocess.CompletedProcess:
        """Run CLI command with proper error handling."""
        # Use the CLI entry point defined in pyproject.toml
        cmd = ["uv", "run", "your-cli-name"] + args
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        if expect_success and result.returncode != 0:
            pytest.fail(f"CLI command failed: {' '.join(cmd)}\nStderr: {result.stderr}")
        elif not expect_success and result.returncode == 0:
            pytest.fail(f"CLI command should have failed: {' '.join(cmd)}")
            
        return result

    def test_cli_help_command(self):
        """Test CLI help functionality."""
        result = self.run_cli_command(["--help"])
        
        assert result.returncode == 0
        assert "usage:" in result.stdout.lower() or "help" in result.stdout.lower()
        assert len(result.stdout) > 50  # Ensure substantial help text

    def test_cli_version_command(self):
        """Test CLI version command."""
        result = self.run_cli_command(["--version"])
        
        assert result.returncode == 0
        # Should contain version information
        assert any(char.isdigit() for char in result.stdout)

    def test_cli_successful_execution(self):
        """Test successful CLI command execution."""
        config = self.setup_test_environment()
        
        try:
            # Test main functionality with configuration
            result = self.run_cli_command([
                "process",
                "--config", self.config_file,
                "--input", "test_input",
                "--output", config["output_dir"]
            ])
            
            assert result.returncode == 0
            assert "success" in result.stdout.lower() or "completed" in result.stdout.lower()
            
            # Verify output files were created
            output_files = os.listdir(config["output_dir"])
            assert len(output_files) > 0, "No output files were created"
            
        finally:
            self.cleanup_test_environment()

    def test_cli_configuration_errors(self):
        """Test CLI behavior with configuration errors."""
        # Test missing configuration file
        result = self.run_cli_command([
            "process",
            "--config", "nonexistent_config.json"
        ], expect_success=False)
        
        assert result.returncode != 0
        assert "config" in result.stderr.lower() or "file not found" in result.stderr.lower()

    def test_cli_invalid_arguments(self):
        """Test CLI error handling for invalid arguments."""
        # Test invalid command
        result = self.run_cli_command(["invalid_command"], expect_success=False)
        assert result.returncode != 0
        
        # Test invalid options
        result = self.run_cli_command([
            "process",
            "--invalid-option", "value"
        ], expect_success=False)
        assert result.returncode != 0

    def test_cli_input_validation(self):
        """Test CLI input validation."""
        config = self.setup_test_environment()
        
        try:
            # Test with invalid input format
            result = self.run_cli_command([
                "process",
                "--config", self.config_file,
                "--input", "",  # Empty input
                "--output", config["output_dir"]
            ], expect_success=False)
            
            assert result.returncode != 0
            assert "input" in result.stderr.lower() or "required" in result.stderr.lower()
            
        finally:
            self.cleanup_test_environment()

    def test_cli_permission_errors(self):
        """Test CLI behavior with permission errors."""
        # Create read-only directory
        readonly_dir = tempfile.mkdtemp(prefix="readonly_test_")
        try:
            os.chmod(readonly_dir, 0o444)  # Read-only
            
            result = self.run_cli_command([
                "process",
                "--output", readonly_dir
            ], expect_success=False)
            
            assert result.returncode != 0
            assert "permission" in result.stderr.lower() or "access" in result.stderr.lower()
            
        finally:
            os.chmod(readonly_dir, 0o755)  # Restore permissions for cleanup
            shutil.rmtree(readonly_dir)

    def test_cli_large_data_processing(self):
        """Test CLI with large data scenarios."""
        config = self.setup_test_environment()
        
        try:
            # Create large test input
            large_input_file = os.path.join(self.test_dir, "large_input.txt")
            with open(large_input_file, 'w') as f:
                for i in range(10000):
                    f.write(f"test_line_{i}\n")
            
            result = self.run_cli_command([
                "process",
                "--config", self.config_file,
                "--input", large_input_file,
                "--output", config["output_dir"]
            ])
            
            assert result.returncode == 0
            # Should handle large data without timeout
            
        finally:
            self.cleanup_test_environment()

    def test_cli_concurrent_execution(self):
        """Test CLI behavior with concurrent executions."""
        import threading
        import concurrent.futures
        
        config = self.setup_test_environment()
        results = []
        
        def run_concurrent_command(thread_id):
            thread_output_dir = os.path.join(config["output_dir"], f"thread_{thread_id}")
            os.makedirs(thread_output_dir, exist_ok=True)
            
            result = self.run_cli_command([
                "process",
                "--config", self.config_file,
                "--input", f"test_input_{thread_id}",
                "--output", thread_output_dir
            ])
            return result.returncode == 0
        
        try:
            # Run multiple CLI commands concurrently
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                futures = [executor.submit(run_concurrent_command, i) for i in range(3)]
                results = [future.result() for future in concurrent.futures.as_completed(futures)]
            
            # All concurrent executions should succeed
            assert all(results), "Some concurrent CLI executions failed"
            
        finally:
            self.cleanup_test_environment()
```

### API Testing Patterns

```python
#!/usr/bin/env python3
"""
Personal Project API End-to-End Tests
====================================

Tests API endpoints with authentication, error handling,
and integration scenarios.
"""

import asyncio
import pytest
import httpx
import time
from typing import Dict, Any

class APIApplicationE2ETest:
    """API application end-to-end testing for personal projects."""

    def __init__(self):
        """Initialize API test configuration."""
        self.base_url = "http://localhost:8000"
        self.timeout = 30
        self.test_data = {}

    async def setup_test_data(self):
        """Setup test data for API testing."""
        self.test_data = {
            "valid_user": {
                "username": "test_user",
                "email": "test@example.com",
                "password": "secure_password_123"
            },
            "invalid_user": {
                "username": "",
                "email": "invalid-email",
                "password": "short"
            },
            "test_payload": {
                "name": "Test Item",
                "description": "Test description",
                "value": 42
            }
        }

    async def cleanup_test_data(self):
        """Clean up test data."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # Clean up any created test resources
            try:
                await client.delete(f"{self.base_url}/test-cleanup")
            except Exception:
                pass  # Ignore cleanup errors

    @pytest.mark.asyncio
    async def test_api_health_check(self):
        """Test API health endpoint."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}/health")
            
            assert response.status_code == 200
            assert "status" in response.json()
            assert response.json()["status"] in ["ok", "healthy", "up"]

    @pytest.mark.asyncio
    async def test_api_authentication_flow(self):
        """Test complete authentication flow."""
        await self.setup_test_data()
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Test user registration
                register_response = await client.post(
                    f"{self.base_url}/auth/register",
                    json=self.test_data["valid_user"]
                )
                assert register_response.status_code in [200, 201]
                
                # Test user login
                login_response = await client.post(
                    f"{self.base_url}/auth/login",
                    json={
                        "username": self.test_data["valid_user"]["username"],
                        "password": self.test_data["valid_user"]["password"]
                    }
                )
                assert login_response.status_code == 200
                assert "access_token" in login_response.json()
                
                # Use token for authenticated request
                token = login_response.json()["access_token"]
                headers = {"Authorization": f"Bearer {token}"}
                
                profile_response = await client.get(
                    f"{self.base_url}/auth/profile",
                    headers=headers
                )
                assert profile_response.status_code == 200
                assert "username" in profile_response.json()
                
        finally:
            await self.cleanup_test_data()

    @pytest.mark.asyncio
    async def test_api_validation_errors(self):
        """Test API input validation."""
        await self.setup_test_data()
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # Test invalid registration data
            response = await client.post(
                f"{self.base_url}/auth/register",
                json=self.test_data["invalid_user"]
            )
            
            assert response.status_code in [400, 422]  # Validation error
            error_data = response.json()
            assert "error" in error_data or "detail" in error_data

    @pytest.mark.asyncio
    async def test_api_unauthorized_access(self):
        """Test API unauthorized access handling."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # Test access without token
            response = await client.get(f"{self.base_url}/auth/profile")
            assert response.status_code == 401
            
            # Test access with invalid token
            headers = {"Authorization": "Bearer invalid_token"}
            response = await client.get(
                f"{self.base_url}/auth/profile",
                headers=headers
            )
            assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_api_crud_operations(self):
        """Test API CRUD operations."""
        await self.setup_test_data()
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Create
                create_response = await client.post(
                    f"{self.base_url}/items",
                    json=self.test_data["test_payload"]
                )
                assert create_response.status_code in [200, 201]
                item_id = create_response.json().get("id")
                assert item_id is not None
                
                # Read
                read_response = await client.get(f"{self.base_url}/items/{item_id}")
                assert read_response.status_code == 200
                assert read_response.json()["name"] == self.test_data["test_payload"]["name"]
                
                # Update
                updated_data = {**self.test_data["test_payload"], "name": "Updated Test Item"}
                update_response = await client.put(
                    f"{self.base_url}/items/{item_id}",
                    json=updated_data
                )
                assert update_response.status_code == 200
                
                # Delete
                delete_response = await client.delete(f"{self.base_url}/items/{item_id}")
                assert delete_response.status_code in [200, 204]
                
                # Verify deletion
                verify_response = await client.get(f"{self.base_url}/items/{item_id}")
                assert verify_response.status_code == 404
                
        finally:
            await self.cleanup_test_data()

    @pytest.mark.asyncio
    async def test_api_error_handling(self):
        """Test API error handling scenarios."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # Test 404 for non-existent resource
            response = await client.get(f"{self.base_url}/items/999999")
            assert response.status_code == 404
            
            # Test 405 for wrong HTTP method
            response = await client.patch(f"{self.base_url}/items")
            assert response.status_code == 405

    @pytest.mark.asyncio
    async def test_api_performance(self):
        """Test API performance characteristics."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # Test response time
            start_time = time.time()
            response = await client.get(f"{self.base_url}/health")
            end_time = time.time()
            
            assert response.status_code == 200
            response_time = end_time - start_time
            assert response_time < 2.0, f"Response time too slow: {response_time}s"

    @pytest.mark.asyncio
    async def test_api_concurrent_requests(self):
        """Test API behavior under concurrent load."""
        async def make_request(client, request_id):
            response = await client.get(f"{self.base_url}/health?request_id={request_id}")
            return response.status_code == 200
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # Make multiple concurrent requests
            tasks = [make_request(client, i) for i in range(10)]
            results = await asyncio.gather(*tasks)
            
            # All requests should succeed
            assert all(results), "Some concurrent requests failed"
```

### Integration Testing Patterns

```python
#!/usr/bin/env python3
"""
Personal Project Integration End-to-End Tests
============================================

Tests integration with external services, databases,
and file systems.
"""

import pytest
import os
import tempfile
import sqlite3
from pathlib import Path

class IntegrationE2ETest:
    """Integration testing for personal projects."""

    def __init__(self):
        """Initialize integration test environment."""
        self.temp_dir = None
        self.test_db = None

    def setup_test_database(self):
        """Setup test database."""
        self.temp_dir = tempfile.mkdtemp(prefix="integration_test_")
        self.test_db = os.path.join(self.temp_dir, "test.db")
        
        # Create test database with schema
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def cleanup_test_database(self):
        """Clean up test database."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)

    def test_database_integration(self):
        """Test database integration."""
        self.setup_test_database()
        
        try:
            # Test database connection and operations
            conn = sqlite3.connect(self.test_db)
            cursor = conn.cursor()
            
            # Insert test data
            cursor.execute(
                "INSERT INTO users (username, email) VALUES (?, ?)",
                ("test_user", "test@example.com")
            )
            conn.commit()
            
            # Verify data
            cursor.execute("SELECT * FROM users WHERE username = ?", ("test_user",))
            user = cursor.fetchone()
            assert user is not None
            assert user[1] == "test_user"
            assert user[2] == "test@example.com"
            
            conn.close()
            
        finally:
            self.cleanup_test_database()

    def test_file_system_integration(self):
        """Test file system operations."""
        temp_dir = tempfile.mkdtemp(prefix="fs_test_")
        
        try:
            # Test file creation and manipulation
            test_file = os.path.join(temp_dir, "test_output.txt")
            test_content = "Integration test content\nLine 2\nLine 3"
            
            # Write file
            with open(test_file, 'w') as f:
                f.write(test_content)
            
            # Verify file exists and content
            assert os.path.exists(test_file)
            
            with open(test_file, 'r') as f:
                content = f.read()
            
            assert content == test_content
            assert len(content.split('\n')) == 3
            
            # Test file processing
            processed_file = os.path.join(temp_dir, "processed_output.txt")
            with open(test_file, 'r') as infile, open(processed_file, 'w') as outfile:
                for line_num, line in enumerate(infile, 1):
                    outfile.write(f"{line_num}: {line}")
            
            # Verify processed file
            assert os.path.exists(processed_file)
            
        finally:
            import shutil
            shutil.rmtree(temp_dir)

    def test_configuration_integration(self):
        """Test configuration file integration."""
        temp_dir = tempfile.mkdtemp(prefix="config_test_")
        
        try:
            config_file = os.path.join(temp_dir, "app_config.json")
            test_config = {
                "database_url": f"sqlite:///{temp_dir}/app.db",
                "api_key": "test_api_key_12345",
                "debug": True,
                "max_connections": 10
            }
            
            # Write configuration
            import json
            with open(config_file, 'w') as f:
                json.dump(test_config, f, indent=2)
            
            # Test configuration loading
            with open(config_file, 'r') as f:
                loaded_config = json.load(f)
            
            assert loaded_config == test_config
            assert loaded_config["debug"] is True
            assert loaded_config["max_connections"] == 10
            
            # Test configuration validation
            assert "database_url" in loaded_config
            assert loaded_config["database_url"].startswith("sqlite://")
            
        finally:
            import shutil
            shutil.rmtree(temp_dir)

    def test_environment_integration(self):
        """Test environment variable integration."""
        # Set test environment variables
        test_env_vars = {
            "TEST_API_URL": "http://test.example.com",
            "TEST_DEBUG": "true",
            "TEST_MAX_RETRIES": "3"
        }
        
        original_values = {}
        
        try:
            # Set test environment variables
            for key, value in test_env_vars.items():
                original_values[key] = os.environ.get(key)
                os.environ[key] = value
            
            # Test environment variable access
            assert os.environ.get("TEST_API_URL") == "http://test.example.com"
            assert os.environ.get("TEST_DEBUG").lower() == "true"
            assert int(os.environ.get("TEST_MAX_RETRIES")) == 3
            
            # Test environment-based configuration
            debug_mode = os.environ.get("TEST_DEBUG", "false").lower() == "true"
            assert debug_mode is True
            
        finally:
            # Restore original environment
            for key, original_value in original_values.items():
                if original_value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = original_value
```

## Test Data Management

### Personal Project Data Setup

```python
# e2e-tests/conftest.py
import pytest
import tempfile
import os
import shutil
from pathlib import Path

@pytest.fixture(scope="session")
def test_data_dir():
    """Create temporary directory for test data."""
    temp_dir = tempfile.mkdtemp(prefix="personal_project_e2e_")
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture(scope="function")
def clean_environment():
    """Ensure clean test environment for each test."""
    # Store original environment
    original_env = dict(os.environ)
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)

@pytest.fixture(scope="function")
def test_config(test_data_dir):
    """Create test configuration."""
    config = {
        "database_url": f"sqlite:///{test_data_dir}/test.db",
        "log_level": "DEBUG",
        "api_timeout": 30,
        "output_dir": os.path.join(test_data_dir, "output")
    }
    
    # Create output directory
    os.makedirs(config["output_dir"], exist_ok=True)
    
    return config
```

### Environment Configuration

```python
# Personal project environment configuration
PERSONAL_TEST_CONFIG = {
    "development": {
        "api_url": "http://localhost:8000",
        "database_url": "sqlite:///dev.db",
        "log_level": "DEBUG",
        "timeout": 30
    },
    "testing": {
        "api_url": "http://localhost:8001",
        "database_url": "sqlite:///test.db", 
        "log_level": "INFO",
        "timeout": 15
    },
    "ci": {
        "api_url": "http://test-api:8000",
        "database_url": "postgresql://test:test@postgres:5432/testdb",
        "log_level": "WARNING",
        "timeout": 10
    }
}
```

## Error Recovery Procedures

### Common Personal Project Issues

| Issue | Common Causes | Solutions | Alternative Commands |
|-------|---------------|-----------|---------------------|
| **Dependency conflicts** | Version mismatches | `uv sync --refresh` | Check `pyproject.toml` versions |
| **Import errors** | Path issues | Verify `src/` structure | Use absolute imports |
| **Test failures** | Environment setup | Check test fixtures | Run tests in isolation |
| **API connection errors** | Service not running | Start local services | Use mock services |
| **File permission errors** | Incorrect permissions | Check file ownership | Use temporary directories |

### Test Execution Commands

```bash
# Install all dependencies including E2E
uv sync --extra e2e

# Run all E2E tests
uv run pytest e2e-tests/ -v

# Run specific test category
uv run pytest e2e-tests/test_cli_e2e.py -v
uv run pytest e2e-tests/test_api_e2e.py -v

# Run tests with coverage
uv run pytest e2e-tests/ --cov=src --cov-report=html

# Run tests in parallel
uv run pytest e2e-tests/ -n auto

# Run tests with detailed output
uv run pytest e2e-tests/ -v -s --tb=short
```

## Example Usage

**Personal Project CLI Example:**
```
$ARGUMENTS: Implement end-to-end tests for the data processing CLI tool covering:
- Command line argument validation and help functionality
- Configuration file loading and validation
- Data processing with various input formats (CSV, JSON, XML)
- Output generation and file management
- Error handling for invalid inputs and permission errors
- Performance testing with large datasets
- Concurrent execution scenarios
- Integration with external APIs and databases
Use uv for dependency management and pytest for execution
```

**Personal Project API Example:**
```
$ARGUMENTS: Create comprehensive end-to-end tests for the FastAPI web service including:
- Authentication flow (registration, login, token validation)
- CRUD operations for all major entities
- Input validation and error response testing
- API performance and concurrent request handling
- Integration with database and external services
- File upload and download functionality
- Rate limiting and security features
- Health checks and monitoring endpoints
Use httpx for async HTTP testing and pytest-asyncio for async test support
```

**Personal Project Integration Example:**
```
$ARGUMENTS: Develop integration end-to-end tests for the data synchronization tool covering:
- Database connectivity and transaction handling
- File system operations and directory management
- Configuration management with environment variables
- External API integration with authentication
- Error recovery and retry mechanisms
- Data transformation and validation pipelines
- Logging and monitoring integration
- Multi-environment configuration (dev, test, prod)
Focus on real-world integration scenarios and robust error handling
```