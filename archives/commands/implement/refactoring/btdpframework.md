# BTDP Framework Compliance Refactoring

## Purpose
Refactor existing code to comply with BTDP Framework enterprise standards including dependency management, async patterns, code organization, and quality requirements.

## Prerequisites
- Clean working directory on develop branch
- Story number (STRYxxxxxxx) available for branch naming
- Understanding of BTDP Framework architecture patterns
- Access to btdp_fastapi library documentation

## Workflow Steps

You must follow this protocol completely. Create a Todo list according to these steps:

1. Ensure you are on develop branch with no uncommitted code (if there is, you stop).
2. Pull to ensure develop is up to date.
3. Create working branch with the following naming convention: `(fix|hotfix|feat)/STRYxxxxxxx/description`.
4. Understand the current implementation and code base to define the implementation steps. Ensure to follow the architecture patterns defined below. Remember to use appropriate tools to gather information on how to do it.
5. Make the implementation ensuring you are following the coding style of the current project. Eliminate code duplication and apply DRY principle.
6. Clean the code with `black -l 120` for formatting.
7. Build the project and solve all the issues. Never stop until you reach a pylint score of 10/10 without disabling any rule (just using the .pylintrc at the root of the project), zero security issues with bandit and safety CLI check with no exceptions. Run compliance command after the refactoring to validate the new implementation.
9. Update README.md and CLAUDE.md. In the README.md never forget to describe all the components, their usage and the permissions required. Don't forget also to mention the permission to trigger a functionality.
9. Commit the change with proper message format.
10. Push to the remote repository.

## Success Criteria
- [ ] Dependencies managed via requirements.txt with latest versions
- [ ] btdp_fastapi==1.1.* as main framework dependency
- [ ] Full async/await implementation (no blocking libraries)
- [ ] Code structure follows BTDP Framework patterns
- [ ] Code duplication eliminated (DRY principle applied)
- [ ] Pylint score of 10/10 without disabling any rule (just using the .pylintrc at the root)
- [ ] Zero security issues with bandit
- [ ] Safety CLI check with no exceptions
- [ ] Complete README.md and CLAUDE.md documentation
- [ ] Changes committed and pushed with proper git workflow

## Environment Detection
This command is specifically for BTDP Framework compliance and uses:

**BTDP Framework Transformation:**
- **Target Structure**: Create `modules/` directory with proper module organization
- **Dependency Migration**: Convert from any format to `requirements.txt` with exact versions
- **Framework Integration**: Implement btdp_fastapi==1.1.* as core dependency
- **Build System**: Set up `Makefile` and `module.mk` for enterprise CI/CD
- **Module Type**: Create `.module_type` file (gcr, gcf, etc.)
- **Infrastructure**: Add terraform in `iac/` directories
- **Documentation**: Create enterprise-compliant README.md and CLAUDE.md

## BTDP Framework Compliance Requirements

The objective is to make the code compliant with BTDP Framework enterprise standards:

### Dependency Management
- **requirements.txt**: Use for all dependencies with exact versions
- **btdp_fastapi**: Main framework dependency (version 1.1.*)
- **Latest Versions**: Ensure all dependencies use current stable versions

### Architecture Compliance
- **Code Duplication**: Eliminate duplicate code, apply DRY (Don't Repeat Yourself) principle
- **Async/Await**: Full asyncio implementation, prefer aiohttp over requests or non-async API libraries
- **aiohttp**: Prefer async HTTP client over requests
- **Code Structure**: Follow BTDP Framework directory organization patterns
- **Dependency Injection**: Implement in application.py

### Quality Standards
- **Pylint**: Score of 10/10 without disabling any rule (just using the .pylintrc at the root of the project)
- **Security**: Zero bandit issues (use `# nosec` with proper justification only) and safety CLI check with no exceptions
- **Documentation**: Complete README.md and CLAUDE.md

## Task Description
$ARGUMENTS

## Example Usage
```
$ARGUMENTS: Refactor the legacy data-processing module to comply with BTDP Framework standards. Convert synchronous code to async/await patterns, update dependencies to use btdp_fastapi 1.1.*, reorganize code structure according to BTDP patterns.
```
