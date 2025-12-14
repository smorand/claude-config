# Implementation on Existing Branch

## Purpose
Implement changes on an existing feature branch without creating new git workflows. Use this for iterative development on work-in-progress features or when continuing existing development.

## Prerequisites
- Must be on a feature branch (not develop/main)
- Branch should follow naming convention: `(fix|hotfix|feat)/STRYxxxxxxx/description`
- Access to deployment environment (default: dv)
- Required permissions for GCP resource verification

## Workflow Steps

You must follow this protocol completely. Create a Todo list according to these steps:
1. Verify you are on a feature branch (not develop/main) with proper naming: `(fix|hotfix|feat)/STRYxxxxxxx/description`
2. Analyze current implementation and identify changes needed for the enhancement
3. Implement the requested changes following project coding standards (avoid code duplication)
4. Format code with `black -l 120`
5. Run build and fix any issues until pylint score 10, zero bandit issues
6. **Implement proper error handling** for new/modified functionality with appropriate exception types and messages
7. Deploy to specified environment (default: dv) and verify deployment success
8. Validate deployed resources with gcloud commands (if applicable)
9. Add/update end-to-end tests for new functionality
10. Update README.md and CLAUDE.md with new functionality details
11. **Document error scenarios** for new functionality including recovery procedures
12. Commit changes with proper message format and push to remote

## Success Criteria
- [ ] Implementation completed on existing feature branch
- [ ] No code duplication (DRY principle applied)
- [ ] Code follows project standards (black formatting applied)
- [ ] Pylint score of 10 achieved
- [ ] **Error handling implemented** for new/modified functionality with proper exception types
- [ ] **Error scenarios documented** for new functionality including recovery procedures
- [ ] Successful deployment verified in target environment
- [ ] GCP resources validated via gcloud commands
- [ ] Documentation updated (README.md and CLAUDE.md)
- [ ] Changes committed and pushed to existing branch

## Workflow Integration

### Prerequisites Commands
- [ ] **Branch verification**: Ensure on feature branch with proper naming convention
- [ ] **Current state understanding**: Review existing implementation and changes made so far
- [ ] **Environment readiness**: Verify deployment environment access and credentials

### Follow-up Commands
- [ ] **Quality validation**: Run `implement/compliance.md` for comprehensive quality check
- [ ] **Security review**: Use `gcpaudit/projects.md` for security-sensitive changes
- [ ] **Deployment finalization**: Consider `implement/full.md` when ready for PR creation
- [ ] **Documentation updates**: Update enterprise documentation via MCP servers

### Alternative Flows
- [ ] **New feature start**: Use `implement/standard.md` or `implement/full.md` for new feature branches
- [ ] **Major refactoring**: Use `implement/refactoring/*` if significant architectural changes needed
- [ ] **Quality focus**: Run `implement/compliance.md` first if code quality needs improvement
- [ ] **Branch completion**: Use `implement/full.md` to complete feature development with PR creation

### Iteration Guidelines
- [ ] **Incremental development**: Build on existing work without breaking current functionality
- [ ] **Backward compatibility**: Ensure changes don't break existing features
- [ ] **Documentation continuity**: Keep documentation consistent with iterative changes

## Error Recovery Procedures

### Branch Management Issues
| Issue | Detection | Solution | Prevention |
|-------|-----------|----------|------------|
| **Wrong branch (develop/main)** | `git branch` shows develop/main | Switch to feature branch: `git checkout feat/STRYxxxx/desc` | Always verify branch before starting work |
| **Branch naming incorrect** | Branch doesn't follow `feat/STRYxxxx/desc` pattern | Rename branch: `git branch -m new-name` or create new branch | Follow naming conventions consistently |
| **Uncommitted changes conflict** | Git status shows uncommitted files | Commit or stash changes before switching | Regular commits during development |
| **Branch behind remote** | Local branch out of sync | `git pull origin branch-name`, resolve conflicts | Regular pulls from remote branch |

### Iterative Development Issues
| Problem | Common Causes | Solutions | Alternative Commands |
|---------|---------------|-----------|-------------------|
| **Breaking existing features** | Changes affect unchanged code paths | Review impact | `implement/compliance.md` for coplete validation |
| **Integration conflicts** | New changes don't integrate with existing work | Review existing implementation, ensure interface compatibility | Consider `implement/refactoring/*` for major changes |
| **Performance regression** | New code affects existing performance | Profile performance, optimize critical paths | Review architectural patterns |

### Quality Issues Specific to Iterative Work
| Quality Problem | Iteration-Specific Causes | Quick Fixes | Comprehensive Solutions |
|-----------------|-------------------------|-------------|----------------------|
| **Pylint score decrease** | New code doesn't follow existing patterns | Follow established patterns in codebase | `implement/compliance.md` for systematic quality improvement |
| **Code duplication introduction** | Copy-paste from existing code | Extract common functionality to shared utilities | Review existing abstractions and patterns |
| **Security issues** | New code introduces vulnerabilities | Fix immediate security issues | `gcpaudit/projects.md` for comprehensive security review |

### Deployment Issues in Iterative Context
| Deployment Problem | Iteration Context | Solutions | Recovery Commands |
|-------------------|------------------|-----------|------------------|
| **Resource conflicts** | New resources conflict with existing deployment | Check existing resources, update terraform state | Review infrastructure configuration |
| **Environment drift** | Development environment differs from previous state | Redeploy infrastructure, verify environment consistency | `make ENV=<env> deploy` from project root |
| **Feature flag issues** | New features conflict with existing feature flags | Coordinate feature flag management | Review feature flag configuration |
| **Database migration conflicts** | Schema changes conflict with existing data | Plan migration strategy, test with sample data | Coordinate with database team |

### Environment-Specific Iterative Issues
| Project Type | Iteration Challenges | Detection Methods | Solutions |
|--------------|---------------------|------------------|-----------|
| **BTDP Framework** | Module dependencies change | Build failures, import errors | Review `requirements.txt`, check module structure |
| **BTDP Framework** | Environment variable changes | Runtime configuration errors | Update `test_env.sh`, sync with `iac/locals.tf` |
| **BTDP Framework** | Service account permission changes | Deployment permission errors | Review IAM policies, update terraform permissions |
| **Personal Projects** | Dependency version conflicts | Package resolution errors | `uv sync` to resolve, update `pyproject.toml` |
| **Personal Projects** | Configuration format changes | Application startup errors | Update configuration files, maintain backward compatibility |

### Recovery Decision Framework for Iterative Work
```
Issue During Iterative Development:
├── Breaking existing functionality?
│   ├── Yes → Fix immediately, ensure backward compatibility
│   └── No → Continue to next check
├── Quality standards dropping?
│   ├── Yes → Use `implement/compliance.md`
│   └── No → Continue to next check
├── Major architectural changes needed?
│   ├── Yes → Consider `implement/refactoring/*`
│   └── No → Continue to next check
├── Security concerns introduced?
│   ├── Yes → Use `gcpaudit/projects.md`
│   └── No → Continue to next check
└── Ready for branch completion?
    ├── Yes → Use `implement/full.md` for PR creation
    └── No → Continue iterative development
```

### Common Iterative Development Patterns
| Pattern | When to Use | Implementation | Considerations |
|---------|-------------|----------------|----------------|
| **Feature Flag Implementation** | Gradual feature rollout | Add feature flags for new functionality | Coordinate with existing flag management |
| **Incremental Refactoring** | Improving code while adding features | Refactor small sections with each iteration | Maintain backward compatibility |
| **Progressive Enhancement** | Building on existing features | Extend existing APIs and interfaces | Ensure existing clients continue to work |
| **Parallel Development** | Multiple features in same codebase | Use feature branches, coordinate integration | Regular merges from develop branch |

## Environment Detection
This command automatically adapts based on project type:

**BTDP Framework Projects:**
- **Detection**: Look for `modules/` directory, `Makefile`, `module.mk`
- **Build & Test**: `make -f ../../module.mk ENV=<env> build`
- **Deploy**: `make -f ../../module.mk ENV=<env> deploy`
- **Quality Gates**: Enterprise compliance (pylint 10/10, bandit, 100% coverage)
- **Documentation**: Update module README.md and CLAUDE.md

**Personal Projects:**
- **Detection**: Look for `pyproject.toml`, single `src/` structure
- **Dependencies**: `uv sync`
- **Testing**: `uv run pytest e2e-tests/`
- **Quality**: `uv run pylint src/`, `uv run bandit -r src/`
- **Formatting**: `uv run black -l 120 src/`

## Task Description
$ARGUMENTS

## Example Usage
**BTDP Framework Example:**
```
$ARGUMENTS: Enhance the existing authentication middleware to support multi-factor authentication. Add TOTP validation, backup codes generation, and user preference management.
```

**Personal Project Example:**
```
$ARGUMENTS: Add filtering capabilities to the existing data export command. Include support for date ranges, user ID filtering, and data type selection.
```
