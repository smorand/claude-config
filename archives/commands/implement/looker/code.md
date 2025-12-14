# Looker Code Implementation

## Purpose
Implement Looker-specific code changes including LookML development, model updates, dashboard modifications, and data layer enhancements for Looker projects.

## Prerequisites
- Working on feature branch (not develop/main)
- Understanding of LookML syntax and Looker development patterns
- Access to Looker project repository
- Story number (STRYxxxxxxx) for branch naming if new branch needed

## Workflow Steps

You must follow this protocol completely. Create a Todo list according to these steps:

1. Ensure you are on a dedicated branch for the feature and that you are not on develop. If required create a new branch following the standards naming conventions: `(fix|hotfix|feat)/STRYxxxxxxx/description`.
2. Understand the current implementation and code base to define the implementation steps.
3. Make the implementation ensuring you are following the coding style of the current project.
4. Commit and push the code.

## Success Criteria
- [ ] Working on appropriate feature branch
- [ ] LookML code follows project standards and conventions
- [ ] Implementation tested for syntax and logical correctness
- [ ] Changes committed with proper message format
- [ ] Code pushed to remote repository

## Environment Detection
This command is specifically for Looker development and uses:

**Looker Development Environment:**
- **Detection**: Look for `.lkml` files, `manifest.lkml`, Looker project structure
- **LookML Syntax**: Follow Looker modeling language conventions and best practices
- **Project Structure**: Maintain views/, models/, dashboards/ organization
- **Development Workflow**: Feature branch → develop → uat → production workflow
- **Code Standards**: Proper naming conventions, documentation, and performance optimization
- **Testing**: Validate LookML syntax and logical correctness before commit

## Description Template
$ARGUMENTS

## Example Usage
```
$ARGUMENTS: Add new measures to the sales dashboard model including year-over-year growth calculations, regional performance metrics, and product category analysis. Update the corresponding views and ensure proper dimension groupings for optimal performance.
```

