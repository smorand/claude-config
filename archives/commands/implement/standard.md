# Standard Implementation Protocol

## Purpose
Basic implementation without complex git workflows or extensive deployment procedures. Use this for simple code changes, prototyping, or when working within existing development cycles.

## Prerequisites
- Working directory in appropriate state for changes
- Access to deployment environment (default: dv) if deployment needed
- Understanding of current codebase architecture

## Workflow Steps

You must follow this protocol completely. Create a Todo list according to these steps:

1. Analyze current codebase to understand implementation requirements
2. Implement the requested functionality following project coding standards (avoid code duplication)
3. Format code with `black -l 120`
4. Run basic quality checks (pylint, bandit) and fix critical issues
5. **Implement proper error handling** for new functionality with appropriate exception types and error messages
6. Test implementation locally to verify functionality works
7. Update documentation if significant changes were made
8. **Document error scenarios** in code comments and relevant documentation
9. Commit changes with proper message format and push

## Success Criteria
- [ ] Implementation completed following project coding standards
- [ ] No code duplication (DRY principle applied)
- [ ] Code formatted with black -l 120
- [ ] Pylint score of 10 achieved
- [ ] **Error handling implemented** for new functionality with proper exception types
- [ ] **Error scenarios documented** in code and relevant documentation
- [ ] Successful deployment verified (if applicable)
- [ ] Documentation updated (README.md and CLAUDE.md)
- [ ] Changes committed and pushed with proper message format

## Workflow Integration

### Prerequisites Commands
- [ ] **Code understanding**: Review existing codebase architecture and patterns
- [ ] **Clean workspace**: Ensure working directory is ready for changes
- [ ] **Environment setup**: Verify development tools and dependencies are available

### Follow-up Commands
- [ ] **Quality validation**: Run `implement/compliance.md` for comprehensive quality assurance
- [ ] **Full deployment**: Use `implement/full.md` if complete deployment lifecycle needed
- [ ] **Security audit**: Consider `gcpaudit/projects.md` for security-sensitive changes
- [ ] **Refactoring**: Use `implement/refactoring/*` if significant code restructuring emerges

### Alternative Flows
- [ ] **Quality-first approach**: Run `implement/compliance.md` first if code quality is uncertain
- [ ] **Complete lifecycle**: Use `implement/full.md` instead for new features requiring full git workflow
- [ ] **Existing branch**: Use `implement/change.md` if working on existing feature branch
- [ ] **Prototype to production**: Upgrade to `implement/full.md` when prototype becomes production feature

### Quality Gate Recommendations
- [ ] **Basic quality**: Achieve pylint 10/10 and clean bandit scan
- [ ] **Test coverage**: Maintain 100% coverage for modified code
- [ ] **Documentation**: Update docs for user-facing changes
- [ ] **Code review**: Consider peer review for complex implementations

## Error Recovery Procedures

### Implementation Issues
| Problem Type | Common Causes | Quick Solutions | When to Escalate |
|-------------|---------------|-----------------|------------------|
| **Architecture mismatch** | Not following existing patterns | Review similar implementations, follow established patterns | Use `implement/refactoring/*` for architectural changes |
| **Dependency conflicts** | New code requires incompatible packages | Use existing dependencies, find compatible versions | Discuss architecture changes with team |
| **Performance issues** | Inefficient implementation | Optimize algorithms, use project-specific patterns | Consider design review for complex optimizations |

### Quality Check Failures
| Quality Issue | Quick Fix | Comprehensive Solution | Alternative Command |
|---------------|-----------|----------------------|-------------------|
| **Pylint < 10** | Fix most critical issues first | Use systematic approach to achieve 10/10 | `implement/compliance.md` for thorough quality improvement |
| **Bandit warnings** | Address high-severity issues | Comprehensive security review | `gcpaudit/projects.md` for security audit |
| **Format issues** | Run `black -l 120` formatting | Ensure consistent formatting across project | Automated formatting should handle most issues |

### Environment-Specific Issues
| Project Type | Common Problems | Detection | Solutions |
|--------------|-----------------|-----------|-----------|
| **BTDP Framework** | Module not found errors | Import failures, wrong PYTHONPATH | Verify module structure, check `src/` organization |
| **BTDP Framework** | Build failures | `make` command failures | Ensure in module directory, verify `module.mk` exists |
| **BTDP Framework** | Environment variables missing | Runtime configuration errors | Check `test_env.sh`, verify environment setup |
| **Personal Projects** | uv dependency issues | Package not found, version conflicts | Run `uv sync`, resolve dependency conflicts |
| **Personal Projects** | Import path issues | Module not found in development | Ensure `uv run pip install -e .` for development install |

### Deployment Issues (If Applicable)
| Deployment Stage | Error Type | Quick Resolution | Full Resolution |
|------------------|------------|------------------|-----------------|
| **Local testing** | Import/runtime errors | Fix immediate issues | `implement/compliance.md` for comprehensive testing |
| **Build process** | Dependency/configuration issues | Verify environment setup | Check project configuration files |
| **Basic deployment** | Permission/resource errors | Verify deployment permissions | `implement/full.md` for complete deployment workflow |
| **Functionality verification** | Feature not working as expected | Quick bug fixes | Comprehensive testing and validation |

### Recovery Decision Tree
```
Implementation Issue Encountered:
├── Simple code/logic fix needed?
│   ├── Yes → Fix in current workflow
│   └── No → Continue to next check
├── Quality standards not met?
│   ├── Yes → Use `implement/compliance.md`
│   └── No → Continue to next check
├── Significant refactoring needed?
│   ├── Yes → Use `implement/refactoring/*`
│   └── No → Continue to next check
├── Full deployment lifecycle needed?
│   ├── Yes → Use `implement/full.md`
│   └── No → Continue to next check
└── Security concerns identified?
    ├── Yes → Use `gcpaudit/projects.md`
    └── No → Escalate to senior developer
```

### Common Error Messages and Solutions
| Error Message | Likely Cause | Immediate Action | Prevention |
|---------------|-------------|------------------|------------|
| "ModuleNotFoundError: No module named 'X'" | Import path issues | Check imports, verify module structure | Use relative imports, verify PYTHONPATH |
| "pylint: command not found" | Missing development tools | Install tools: `uv add --dev pylint` | Ensure development environment setup |
| "Permission denied" during deployment | Insufficient permissions | Verify deployment credentials | Check deployment documentation |

## Environment Detection
This command automatically adapts based on project type:

**BTDP Framework Projects:**
- **Detection**: Look for `modules/` directory, `Makefile`, `module.mk`
- **Full Build**: `make -f ../../module.mk ENV=<env> build`
- **Deploy**: `make -f ../../module.mk ENV=<env> deploy`
- **Quality**: Enterprise standards (pylint 10/10, bandit clean)

**Personal Projects:**
- **Detection**: Look for `pyproject.toml`, single `src/` structure
- **Quality Check**: `uv run pylint src/`, `uv run bandit -r src/`
- **Install**: `uv run pip install -e .` (development mode)
- **Format**: `uv run black -l 120 src/`

## Task Description
$ARGUMENTS

## Example Usage
**BTDP Framework Example:**
```
$ARGUMENTS: Add input validation to the data processing service. Include schema validation for incoming JSON payloads, error handling for malformed data, and logging for validation failures.
```

**Personal Project Example:**
```
$ARGUMENTS: Refactor the configuration loading logic in the CLI tool. Extract configuration parsing into a separate class, add support for environment variable overrides, and improve error messages for invalid configurations.
```
