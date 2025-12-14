# Code Compliance and Quality Enforcement

## Purpose
Ensure full code compliance with quality standards and security requirements. Use this for code quality enforcement, pre-deployment validation, or compliance audits.

## Prerequisites
- Clean working directory on develop branch
- Story number (STRYxxxxxxx) available for branch naming
- Full codebase access for comprehensive quality analysis
- Understanding of current project architecture and standards

## Workflow Steps

You must follow this protocol completely. Create a Todo list according to these steps:

1. Ensure you are on develop branch with clean working directory
2. Pull to ensure develop is up to date
3. Create compliance branch: `(fix|hotfix|feat)/STRYxxxxxxx/compliance-audit`
4. Run comprehensive code quality audit (pylint, bandit, safety CLI, code duplication analysis, coverage analysis)
5. **Perform error handling compliance audit** (validate exception handling, error documentation, logging standards)
6. Identify all compliance violations and create remediation plan
7. Analyze and eliminate code duplication (DRY principle enforcement)
8. Fix pylint issues by refactoring code (no rule disabling allowed)
9. **Implement comprehensive error handling** (proper try/except blocks, specific exceptions, contextual error messages)
10. Resolve all security issues identified by bandit and safety CLI check (document `# nosec` usage and address safety CLI vulnerabilities)
11. **Audit and improve error documentation** (document all error scenarios, recovery procedures, user impact)
12. Format all code with `black -l 120`
13. Update README.md with complete feature documentation, usage, and error handling guidance
14. Update CLAUDE.md for implementation clarity including error scenarios
15. Commit compliance improvements with detailed message
16. Push compliance branch to remote

## Success Criteria
- [ ] Code duplication eliminated (DRY principle enforced)
- [ ] Pylint score of 10/10 without disabling rules (refactor code as needed)
- [ ] Zero security issues with bandit and safety CLI check (use `# nosec` only with proper justification)
- [ ] **Error handling compliance achieved** (comprehensive error management validation)
- [ ] **Error documentation validated** (all error scenarios documented)
- [ ] Complete README.md with features, usage, permissions, and error handling documentation
- [ ] Updated CLAUDE.md for implementation understanding including error scenarios
- [ ] All code formatted with black -l 120
- [ ] New feature branch created and pushed
- [ ] Changes committed with proper message format

## Workflow Integration

### Prerequisites Commands
- [ ] **Clean working directory**: Ensure `git status` shows no uncommitted changes
- [ ] **Basic implementation**: Use `implement/standard.md` first if basic implementation is incomplete
- [ ] **Understanding current code**: Review existing codebase architecture and patterns
- [ ] **Development environment**: Ensure all quality tools are available and configured

### Follow-up Commands
- [ ] **Security validation**: Run `gcpaudit/projects.md` after compliance for comprehensive security audit
- [ ] **Deployment readiness**: Use `implement/full.md` for deployment after all quality gates pass
- [ ] **Major refactoring**: Consider `implement/refactoring/*` commands if significant code restructuring is needed
- [ ] **Documentation updates**: Update enterprise documentation in Confluence via MCP servers

### Alternative Flows
- [ ] **Pre-implementation quality**: Run this before `implement/standard.md` if starting with low-quality code
- [ ] **Continuous compliance**: Run periodically during development to maintain quality standards
- [ ] **Pre-deployment validation**: Always run before `implement/full.md` for production deployments
- [ ] **Refactoring validation**: Run after `implement/refactoring/*` to verify quality improvements

### Quality Gate Dependencies
- [ ] **Code duplication**: Must be eliminated before proceeding to deployment
- [ ] **Security compliance**: All bandit and safety issues must be resolved before production
- [ ] **Test coverage**: 100% coverage required before deployment
- [ ] **Documentation completeness**: README.md and CLAUDE.md must be current and complete

## Error Recovery Procedures

### Pylint Quality Issues
| Score Range | Common Issues | Automatic Solutions | When to Escalate |
|-------------|---------------|-------------------|------------------|
| **7.0-8.0** | Too many local variables (R0914), function too long (R0915) | Extract helper methods, split functions into smaller logical units | Use `implement/refactoring/*` for major restructuring |
| **8.0-8.5** | Too many branches (R0912), too many statements (R0915) | Simplify conditional logic, extract decision logic into separate methods | Consider design pattern improvements |
| **8.5-9.0** | Import organization (C0411), naming conventions (C0103) | Reorganize imports with isort, rename variables to follow conventions | Review coding standards documentation |
| **9.0-9.5** | Docstring format (C0111), line length (C0301) | Fix docstring format, break long lines | Automated formatting should handle most issues |
| **9.5-9.9** | Minor style issues, unused imports (W0611) | Remove unused imports, fix minor style inconsistencies | Quick automated fixes |

### Specific Pylint Error Solutions
| Error Code | Issue | Automatic Solution | Manual Intervention |
|------------|-------|-------------------|-------------------|
| **R0903** | Too few public methods | Add methods or convert to function/namedtuple | Consider if class is needed |
| **R0913** | Too many arguments | Use dataclass, config object, or **kwargs pattern | Redesign function interface |
| **R0801** | Duplicate code | Extract common code to utility functions | Use `implement/refactoring/*` for major deduplication |
| **W0613** | Unused argument | Remove argument or prefix with underscore | Check if argument needed for interface compliance |
| **C0116** | Missing function docstring | Add proper docstring with Args/Returns/Raises | Follow project docstring standards |

### Bandit Security Issues
| Error Code | Issue Type | Automatic Solution | Security Justification |
|------------|------------|-------------------|---------------------|
| **B101** | Assert used | Replace with proper error handling | Use proper exception handling instead |
| **B102** | exec used | Remove exec or validate input thoroughly | Document security review with `# nosec` |
| **B105** | Hardcoded password | Move to environment variables or secure config | Use secure secret management |
| **B108** | Probable insecure usage of temp file | Use tempfile module with secure permissions | Ensure temp files have proper permissions |
| **B608** | Possible SQL injection | Use parameterized queries, SQLAlchemy ORM | Document safe usage with `# nosec` if dynamic table names |
| **B603** | Subprocess call without shell=False | Add shell=False, validate all inputs | Document controlled input with `# nosec` |
| **B301** | Pickle usage | Use JSON or secure serialization | Document security review if pickle required |

### Safety CLI Dependency Issues
| Vulnerability Type | Common Packages | Solution Strategy | Enterprise Considerations |
|-------------------|-----------------|-------------------|--------------------------|
| **High/Critical CVE** | requests, urllib3, pillow | `uv add package@latest` immediately | Check enterprise approved versions |
| **Medium CVE** | pandas, numpy, Flask | Schedule upgrade, test thoroughly | Coordinate with dependent projects |
| **Low CVE** | Development dependencies | Upgrade during maintenance windows | Document risk acceptance if upgrade blocked |
| **No secure version** | Abandoned packages | Find alternative package | Enterprise security team consultation |

### Code Duplication Detection and Resolution
| Duplication Type | Detection Method | Resolution Strategy | Tools |
|------------------|------------------|-------------------|-------|
| **Exact duplicates** | Pylint duplicate-code | Extract to utility functions | Use IDE refactoring tools |
| **Similar business logic** | Manual code review | Create shared service classes | Apply design patterns |
| **Copy-paste patterns** | Code similarity analysis | Extract base classes or mixins | Use inheritance or composition |
| **Utility functions** | Function signature analysis | Create shared commons modules | Centralize in commons/ directory |

### Environment-Specific Quality Tool Issues
| Project Type | Tool | Common Problems | Solutions |
|--------------|------|-----------------|-----------|
| **BTDP Framework** | pylint | Custom .pylintrc not found | Ensure .pylintrc exists in project root |
| **BTDP Framework** | bandit | Enterprise security rules | Use enterprise bandit configuration |
| **BTDP Framework** | safety | VPN/proxy issues | Configure safety for enterprise network |
| **Personal Projects** | uv run pylint | Tool not installed | `uv add --dev pylint bandit safety` |

### Recovery Workflows
| Quality Issue | Immediate Action | Alternative Command | Escalation Path |
|---------------|-----------------|-------------------|-----------------|
| **Multiple pylint failures** | Focus on highest-impact issues first | `implement/refactoring/*` for major restructuring | Code review with senior developer |
| **Security vulnerabilities** | Address critical issues immediately | `gcpaudit/projects.md` for comprehensive audit | Enterprise security team review |
| **Dependency vulnerabilities** | Upgrade to secure versions immediately | Document risk if upgrade not possible | Enterprise security team exception request |
| **Code duplication** | Extract most common duplicates first | `implement/refactoring/*` for systematic cleanup | Architecture review for design improvements |

### Quality Tool Configuration Issues
| Tool | Configuration File | Common Issues | Solutions |
|------|-------------------|---------------|-----------|
| **pylint** | .pylintrc | Missing configuration, wrong Python path | Copy from project template, verify PYTHONPATH |
| **bandit** | .bandit | Enterprise rules not applied | Use enterprise .bandit configuration |
| **safety** | pyproject.toml | Proxy/network configuration | Configure enterprise network settings |
| **black** | pyproject.toml | Line length not set to 120 | Ensure black configuration: line-length = 120 |

### Error Handling Compliance Validation

#### **Error Handling Audit Checklist**
| Validation Area | Requirements | Detection Methods | Remediation |
|-----------------|-------------|------------------|-------------|
| **Exception Handling** | All external calls wrapped in try/except | Code review, search for API/DB calls | Add proper exception handling with specific exception types |
| **Error Messages** | Clear, actionable messages with context | Review all raise statements and log messages | Rewrite generic errors with specific context and user guidance |
| **Error Documentation** | All exceptions documented in docstrings | Verify docstring completeness | Add/update Exceptions section in all function docstrings |
| **Error Logging** | Structured logging for all errors | Review logging statements for context | Add structured logging with error_type, context, and relevant IDs |

#### **Error Handling Code Patterns Validation**
```python
# ✅ COMPLIANT: Proper error handling pattern
def process_user_data(user_id: str) -> UserData:
    """Process user data with comprehensive error handling.
    
    Arguments:
        user_id: Unique identifier for the user
        
    Returns:
        Processed user data object
        
    Exceptions:
        ValidationError: When user_id format is invalid
        ExternalServiceError: When external API fails
        DataConsistencyError: When user data is inconsistent
    """
    try:
        # Validate input
        if not user_id or len(user_id) < 3:
            raise ValidationError(f"Invalid user_id format: '{user_id}'. Expected format: minimum 3 characters")
        
        # External service call with proper error handling
        user_data = external_api.get_user(user_id)
        
        return UserData(user_data)
        
    except requests.HTTPError as e:
        logger.error(
            "External API failed for user %s: %s", 
            user_id, str(e),
            extra={"error_type": "ExternalServiceError", "user_id": user_id, "status_code": e.response.status_code}
        )
        raise ExternalServiceError(f"Failed to retrieve data for user {user_id}") from e
    except requests.Timeout as e:
        logger.warning("API timeout for user %s", user_id, extra={"error_type": "TimeoutError", "user_id": user_id})
        raise TimeoutError(f"Request timeout for user {user_id}") from e

# ❌ NON-COMPLIANT: Poor error handling
def process_user_data(user_id):
    try:
        data = external_api.get_user(user_id)
        return data
    except:  # Bare except - not allowed
        return None  # Silent failure - not allowed
```

#### **Error Documentation Requirements**
| Documentation Type | Required Content | Location | Validation Method |
|-------------------|------------------|----------|------------------|
| **Function Docstrings** | All possible exceptions with conditions | Every function/method | Automated docstring parsing |
| **README.md Error Section** | Common error scenarios and solutions | README.md | Manual review for completeness |
| **API Error Responses** | HTTP status codes and error formats | API documentation | API response testing |
| **Deployment Error Guide** | Environment-specific error solutions | CLAUDE.md | Manual validation during deployment |

#### **Error Handling Quality Gates**
| Quality Gate | Requirement | Measurement | Action if Failed |
|-------------|-------------|-------------|------------------|
| **No Bare Except** | Zero `except:` without specific exception | Code search for bare except | Refactor to use specific exceptions |
| **No Silent Failures** | Zero unhandled exceptions or empty except blocks | Code review + testing | Add proper error handling and logging |
| **Error Message Quality** | All error messages include context and guidance | Manual review of error messages | Rewrite messages with specific context |
| **Exception Documentation** | 100% of raised exceptions documented | Docstring analysis | Add missing exception documentation |
| **Error Path Coverage** | 100% coverage of exception blocks | Coverage analysis with branch coverage | Add tests for all error scenarios |

## Environment Detection
This command automatically adapts based on project type:

**BTDP Framework Projects:**
- **Detection**: Look for `modules/` directory, `Makefile`, `module.mk`
- **Quality Suite**: `make -f ../../module.mk ENV=<env> build` (full compliance pipeline)
- **Individual Tools**: Access to pylint, bandit, safety CLI, pytest through enterprise environment
- **Security Scanning**: `bandit -r src/` and `safety check` (or `safety scan` for newer versions)
- **Coverage**: Enforced through enterprise CI/CD pipeline
- **Documentation**: Must include enterprise compliance sections

**Personal Projects:**
- **Detection**: Look for `pyproject.toml`, single `src/` structure  
- **Quality Tools**: `uv run pylint src/`, `uv run bandit -r src/`, `uv run safety check` (or `safety scan`), `uv run pytest --cov=src`
- **Security Scanning**: `uv run bandit -r src/` for code security, `uv run safety check` for dependency vulnerabilities
- **Formatting**: `uv run black -l 120 src/` and `uv run isort src/`
- **Type Checking**: `uv run mypy src/` (if configured)

## Security Tools Usage

### Bandit (Code Security Analysis)
**Purpose**: Static security analysis of Python code to identify common security issues.

**Commands**:
- **BTDP Framework**: `bandit -r src/` (run from module directory)
- **Personal Projects**: `uv run bandit -r src/`

**Common Issues**: SQL injection, hardcoded passwords, shell injection, insecure random generators
**Resolution**: Fix code issues or use `# nosec` with clear justification

### Safety CLI (Dependency Vulnerability Scanning)
**Purpose**: Scan Python dependencies for known security vulnerabilities.

**Commands**:
- **BTDP Framework**: `safety check` or `safety scan` (depending on version)
- **Personal Projects**: `uv run safety check` or `uv run safety scan`

**Common Issues**: Vulnerable package versions with known CVEs
**Resolution**: 
- Upgrade to secure versions: `uv add package@latest` or update `requirements.txt`
- Pin secure versions if latest has breaking changes
- No exceptions allowed - all vulnerabilities must be resolved

### Code Duplication Detection
**Purpose**: Identify and eliminate duplicated code to improve maintainability and follow DRY principle.

**Detection Methods**:
- **Manual Analysis**: Review code for repeated patterns, similar functions, or copy-pasted blocks
- **Pylint Duplication**: Use `pylint` with `--disable=all --enable=duplicate-code` to detect duplicated blocks
- **IDE Tools**: Use IDE duplicate code detection features

**Common Duplication Patterns**:
- Repeated business logic across different modules
- Similar data validation in multiple functions
- Copy-pasted error handling code
- Duplicate utility functions

**Resolution Strategies**:
- Extract common code into utility functions or classes
- Create shared modules for common functionality
- Use inheritance or composition to reduce duplication
- Implement factory patterns for similar object creation
- Create configuration-driven solutions for similar workflows

## Compliance Requirements

The objective is to ensure full compliance of the code. You must not stop until you reach all the following goals:

### Code Quality
- **Code Duplication**: Eliminate all code duplication following DRY (Don't Repeat Yourself) principle
- **Pylint**: Score of 10/10 without disabling any rule (just using the .pylintrc at the root of the project)
- **Security - Code Analysis**: Zero issues with bandit (use `# nosec` only with proper documentation explaining safety)
- **Security - Dependency Vulnerabilities**: Zero issues with safety CLI check with no exceptions (upgrade vulnerable dependencies or pin secure versions)
- **Formatting**: All code properly formatted with black -l 120

### Documentation
- **README.md**: Complete documentation of features, tested scenarios, and implementation
- **CLAUDE.md**: Updated for easy understanding of implementation and new features

## Task Description
$ARGUMENTS

## Example Usage
**BTDP Framework Example:**
```
$ARGUMENTS: Perform full compliance audit of the data-processing module. Fix all pylint issues, resolve security vulnerabilities, and update documentation to reflect all current features and deployment procedures.
```

**Personal Project Example:**
```
$ARGUMENTS: Bring the CLI utility up to full compliance standards. Refactor code to achieve pylint 10/10, implement security best practices, and create complete usage documentation.
```
