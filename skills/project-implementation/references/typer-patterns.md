# Typer CLI Development Patterns

Comprehensive guide for Typer CLI development in personal projects.

## Basic CLI Structure

### Simple Command
```python
import typer

app = typer.Typer()

@app.command()
def main(name: str = typer.Option(..., help="User name")):
    typer.echo(f"Hello {name}!")

if __name__ == "__main__":
    app()
```

### Multiple Commands
```python
import typer

app = typer.Typer()

@app.command()
def create(name: str):
    """Create a new resource"""
    typer.echo(f"Creating {name}")

@app.command()
def delete(name: str):
    """Delete a resource"""
    if typer.confirm(f"Are you sure you want to delete {name}?"):
        typer.echo(f"Deleting {name}")
    else:
        typer.echo("Cancelled")

if __name__ == "__main__":
    app()
```

## Command Options and Arguments

### Arguments
```python
@app.command()
def process(
    input_file: str = typer.Argument(..., help="Input file path"),
    output_file: str = typer.Argument(None, help="Output file path (optional)"),
):
    """Process input file"""
    typer.echo(f"Processing {input_file}")
    if output_file:
        typer.echo(f"Output: {output_file}")
```

### Options
```python
from pathlib import Path

@app.command()
def run(
    config: Path = typer.Option(
        "config.yaml",
        "--config", "-c",
        help="Configuration file path",
        exists=True,
        dir_okay=False,
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Enable verbose output"
    ),
    workers: int = typer.Option(
        4,
        "--workers", "-w",
        help="Number of workers",
        min=1,
        max=16,
    ),
):
    """Run the application"""
    if verbose:
        typer.echo(f"Using config: {config}")
        typer.echo(f"Workers: {workers}")
```

## Type Hints

### Using Type Hints for Validation
```python
from typing import List, Optional
from pathlib import Path
from enum import Enum

class Environment(str, Enum):
    dev = "dev"
    staging = "staging"
    prod = "prod"

@app.command()
def deploy(
    environment: Environment = typer.Option(..., help="Target environment"),
    services: List[str] = typer.Option([], "--service", "-s", help="Services to deploy"),
    config_file: Optional[Path] = typer.Option(None, help="Configuration file"),
    dry_run: bool = typer.Option(False, help="Perform dry run"),
):
    """Deploy services to environment"""
    typer.echo(f"Deploying to {environment.value}")
    if services:
        typer.echo(f"Services: {', '.join(services)}")
    if dry_run:
        typer.echo("Dry run mode enabled")
```

## Rich Output Formatting

### Progress Bars
```python
import typer
from rich.progress import track
import time

@app.command()
def process_items():
    """Process items with progress bar"""
    items = range(100)
    for item in track(items, description="Processing..."):
        time.sleep(0.01)  # Simulate work
    typer.echo("Done!")
```

### Styled Output
```python
from rich.console import Console

console = Console()

@app.command()
def status():
    """Show status with styled output"""
    console.print("[bold green]Success:[/] Operation completed")
    console.print("[bold red]Error:[/] Something went wrong", style="on white")
    console.print("[bold yellow]Warning:[/] Check configuration")
```

### Tables
```python
from rich.table import Table

@app.command()
def list_items():
    """List items in a table"""
    table = Table(title="Items")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("Status", style="green")

    table.add_row("1", "Item A", "Active")
    table.add_row("2", "Item B", "Inactive")
    table.add_row("3", "Item C", "Active")

    console.print(table)
```

## Error Handling

### Graceful Error Handling
```python
import typer
import sys

@app.command()
def process_file(file_path: str):
    """Process a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = f.read()
        typer.echo(f"Processed {len(data)} characters")
    except FileNotFoundError:
        typer.secho(f"Error: File not found: {file_path}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    except PermissionError:
        typer.secho(f"Error: Permission denied: {file_path}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.secho(f"Unexpected error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
```

### Exit Codes
```python
@app.command()
def validate(config_file: str):
    """Validate configuration file"""
    if not Path(config_file).exists():
        typer.echo("Configuration file not found")
        raise typer.Exit(code=1)

    # Validation logic
    if is_valid:
        typer.echo("Configuration is valid")
        raise typer.Exit(code=0)
    else:
        typer.echo("Configuration is invalid")
        raise typer.Exit(code=1)
```

## User Interaction

### Confirmation
```python
@app.command()
def delete(resource_id: str):
    """Delete a resource"""
    if typer.confirm(f"Are you sure you want to delete {resource_id}?"):
        typer.echo(f"Deleting {resource_id}")
    else:
        typer.echo("Operation cancelled")
        raise typer.Exit()
```

### Prompts
```python
@app.command()
def create():
    """Create a new resource"""
    name = typer.prompt("Enter name")
    password = typer.prompt("Enter password", hide_input=True)
    confirm = typer.confirm("Proceed with creation?")

    if confirm:
        typer.echo(f"Creating resource: {name}")
```

## Subcommands and Groups

### Command Groups
```python
import typer

app = typer.Typer()
user_app = typer.Typer()
app.add_typer(user_app, name="user")

@user_app.command("create")
def create_user(username: str):
    """Create a new user"""
    typer.echo(f"Creating user: {username}")

@user_app.command("delete")
def delete_user(username: str):
    """Delete a user"""
    typer.echo(f"Deleting user: {username}")

@user_app.command("list")
def list_users():
    """List all users"""
    typer.echo("Listing users")

if __name__ == "__main__":
    app()
```

### Nested Subcommands
```python
app = typer.Typer()

# Database commands
db_app = typer.Typer()
app.add_typer(db_app, name="db", help="Database operations")

@db_app.command()
def migrate():
    """Run database migrations"""
    typer.echo("Running migrations")

@db_app.command()
def seed():
    """Seed database"""
    typer.echo("Seeding database")

# User commands
user_app = typer.Typer()
app.add_typer(user_app, name="user", help="User management")

@user_app.command()
def create(username: str):
    """Create user"""
    typer.echo(f"Creating user: {username}")
```

## Configuration and Context

### Using Context for Shared State
```python
from typing import Optional

class AppContext:
    def __init__(self):
        self.verbose = False
        self.config_file = None

ctx = AppContext()

@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v"),
    config: Optional[str] = typer.Option(None, "--config", "-c"),
):
    """Main application callback"""
    ctx.verbose = verbose
    ctx.config_file = config
    if verbose:
        typer.echo(f"Verbose mode enabled")

@app.command()
def run():
    """Run application"""
    if ctx.verbose:
        typer.echo("Running in verbose mode")
    if ctx.config_file:
        typer.echo(f"Using config: {ctx.config_file}")
```

## Testing

### Basic CLI Tests
```python
# tests/test_cli.py
from typer.testing import CliRunner
from src.main import app

runner = CliRunner()

def test_app():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output

def test_create_command():
    result = runner.invoke(app, ["create", "--name", "test"])
    assert result.exit_code == 0
    assert "Creating test" in result.output

def test_invalid_option():
    result = runner.invoke(app, ["create", "--invalid"])
    assert result.exit_code != 0
```

## Help Text

### Custom Help
```python
@app.command()
def deploy(
    environment: str = typer.Option(
        ...,
        help="Target environment (dev, staging, prod)",
        metavar="ENV",
    ),
    service: str = typer.Option(
        ...,
        help="Service to deploy",
        metavar="SERVICE",
    ),
):
    """
    Deploy a service to a specific environment.

    Example:
        $ python src/main.py deploy --environment prod --service api
    """
    typer.echo(f"Deploying {service} to {environment}")
```

## Running CLI Applications

### Development
```bash
uv run src/main.py --help
uv run src/main.py command --option value
```

### Installation as Script
Add to `pyproject.toml`:
```toml
[project.scripts]
mycli = "src.main:app"
```

Then:
```bash
uv sync
mycli --help
```

## Best Practices

1. **Use type hints** for all parameters
2. **Provide help text** for all options and commands
3. **Handle errors gracefully** with proper exit codes
4. **Use rich output** for better user experience
5. **Test commands** with CliRunner
6. **Validate inputs** using Typer's built-in validation
7. **Use enums** for restricted choices
8. **Document commands** with docstrings
9. **Organize complex CLIs** with command groups
10. **Use context** for shared state when needed
