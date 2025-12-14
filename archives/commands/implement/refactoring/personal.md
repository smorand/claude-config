# Personal Project Compliance Refactoring

## Purpose
Refactor existing code to comply with Personal Project standards including uv dependency management, modern Python patterns, and installable package structure.

## Prerequisites
- Clean working directory on develop branch
- Story number (STRYxxxxxxx) available for branch naming
- Understanding of Personal Project architecture patterns
- Access to uv package manager

## Workflow Steps

You must follow this protocol completely. Create a Todo list according to these steps:

1. Ensure you are on develop branch with no uncommitted code (if there is, you stop).
2. Pull to ensure develop is up to date.
3. Create working branch with the following naming convention: `(fix|hotfix|feat)/STRYxxxxxxx/description`.
4. Understand the current implementation and code base to define the implementation steps. Ensure to follow the architecture patterns defined below. Remember to use appropriate tools to gather information on how to do it.
5. Make the implementation ensuring you are following the coding style of the current project. Eliminate code duplication and apply DRY principle. Use the Compliance paragraph below for sub-steps here.
6. Clean the code with `black -l 120` for formatting.
7. Build the project and solve all the issues. Never stop until you reach a pylint score of 10/10 without disabling any rule (just using the .pylintrc at the root of the project), zero security issues with bandit and safety CLI check with no exceptions. Run compliance command after the refactoring to validate the new implementation.
8. Update README.md and CLAUDE.md. In the README.md never forget to describe all the components, their usage and the permissions required. Don't forget also to mention the permission to trigger a functionality.
9. Commit the change with proper message format.
10. Push to the remote repository.

## Success Criteria
- [ ] Dependencies managed via uv and pyproject.toml
- [ ] Code structure follows Personal Project patterns
- [ ] Code duplication eliminated (DRY principle applied)
- [ ] FastAPI used for APIs (if applicable)
- [ ] Typer used for CLI with proper script definitions
- [ ] Latest dependency versions with functionality-based organization
- [ ] Application is properly installable with Hatchling build system
- [ ] ALL directories have __init__.py files (including src/ and all subdirectories)
- [ ] main.py includes sys.path configuration for local imports
- [ ] Full async/await implementation
- [ ] Pylint score of 10/10 without disabling any rule (just using the .pylintrc at the root)
- [ ] Zero security issues with bandit
- [ ] Safety CLI check with no exceptions
- [ ] Complete README.md and CLAUDE.md documentation
- [ ] Changes committed and pushed with proper git workflow

## Environment Detection
This command is specifically for Personal Project compliance and uses:

**Personal Project Transformation:**
- **Target Structure**: Create single `src/` directory with functionality-based modules
- **Dependency Migration**: Convert to `pyproject.toml` and `uv` management
- **Package Setup**: Configure installable package with Hatchling build system and proper entry points
- **Package Structure**: Ensure ALL directories have __init__.py files for proper packaging
- **CLI Framework**: Implement `typer` for command-line interfaces with sys.path configuration
- **API Framework**: Use `FastAPI` for web APIs (if applicable)
- **Quality Tools**: Configure `pylint`, `bandit`, `black`
- **Development Tools**: Set up development installation and scripts with dual installation support

## Personal Project Compliance Requirements

The objective is to make the code compliant with Personal Project standards:

### Dependency Management
- **uv**: Use for all dependency management
- **pyproject.toml**: Define project configuration and dependencies
- **Latest Versions**: Ensure all dependencies use current stable versions

### Architecture Compliance
- **Code Duplication**: Eliminate duplicate code, apply DRY (Don't Repeat Yourself) principle
- **Code Organization**: Follow Personal Project directory structure with proper packaging
- **Package Structure**: ALL directories MUST have __init__.py files (including src/ and all subdirectories)
- **Entry Point**: main.py MUST include sys.path configuration before local imports
- **Build System**: Use Hatchling for packaging and distribution
- **FastAPI**: Use for API implementations (if relevant)
- **Typer**: Use for CLI with script definitions in pyproject.toml
- **Functionality Folders**: Organize code by functionality
- **Installable**: Ensure application supports both UV environment and system-wide installation

### Technical Standards
- **Async/Await**: Full asyncio implementation, prefer aiohttp over requests or non async API libraries
- **Quality**: Pylint score of 10/10 without disabling any rule (just using the .pylintrc at the root of the project), zero bandit issues, safety CLI check with no exceptions.
- **Documentation**: Complete README.md and CLAUDE.md

## Task Description
$ARGUMENTS

## Example Usage
```
$ARGUMENTS: Refactor the data analysis CLI tool to comply with Personal Project standards. Migrate from pip to uv dependency management, restructure code with functionality-based organization, implement typer for CLI commands, ensure async patterns throughout.
```
