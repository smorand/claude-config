# Command Templates

## Overview

Commands are template files that define standard workflows for AI assistant interactions. They provide structured protocols for common development tasks, ensuring consistency and completeness across different project types.

## Usage

1. **Selection**: Choose the appropriate command template for your task
2. **Execution**: The AI assistant follows the defined protocol automatically
3. **Customization**: Replace `$ARGUMENTS` with your specific requirements
4. **Context**: The AI will apply the correct project type (BTDP Framework vs Personal Projects) based on your codebase structure

## Project Type Detection

The AI assistant automatically detects your project type:

**BTDP Framework Projects:**
- Located in `~/projects/oa-datafactory-packages/` paths
- Have `modules/` directory with individual service folders
- Use `Makefile` and `module.mk` files for build automation
- Dependencies managed via `requirements.txt` with exact versions
- Contains `.module_type` files (gcr, gcf, etc.)
- Have `api_portal_details.json` files in modules
- Enterprise infrastructure in `iac/` directories

**Personal Projects:**
- Use `pyproject.toml` and `uv` for dependency management with Hatchling build system
- Have single `src/` directory structure with proper packaging (ALL directories must have __init__.py)
- main.py includes sys.path configuration for local imports
- Support both UV environment and system-wide installation
- Manual DevOps workflows (no Makefiles)
- Can be located anywhere in the filesystem
- May have simple `iac/` for basic terraform

## Available Commands

### Implementation Commands

#### Core Implementation
- **`implement/full.md`** - Complete feature implementation with git workflow, testing, and PR creation
  - *Use when*: Starting new features from scratch
  - *Includes*: Branch creation, implementation, testing, deployment, PR

- **`implement/change.md`** - Implementation on existing branch without git workflow
  - *Use when*: Making changes to existing work-in-progress features
  - *Includes*: Implementation and testing only (no git operations)

- **`implement/standard.md`** - Basic implementation without deployment or PR
  - *Use when*: Simple code changes or prototyping
  - *Includes*: Implementation and basic testing

- **`implement/compliance.md`** - Code compliance and quality enforcement
  - *Use when*: Ensuring code meets standards (formatting, linting, security)
  - *Includes*: Quality checks, security scans, compliance fixes

- **`implement/release.md`** - Release management and deployment workflow
  - *Use when*: Preparing and executing production releases
  - *Includes*: Release preparation, version management, deployment coordination

- **`implement/e2etests/btdpframework.md`** - BTDP Framework enterprise pipeline testing
  - *Use when*: Testing complete SRC → DMN → SDDS enterprise data pipelines
  - *Includes*: Distributed project testing, workflow monitoring, state machine handling
  
- **`implement/e2etests/personalproject.md`** - Personal project application testing
  - *Use when*: Testing CLI, API, or local service applications
  - *Includes*: Modern testing patterns, dependency management with uv

#### Specialized Implementation
- **`implement/looker/code.md`** - Looker-specific development workflows
- **`implement/looker/deploy.md`** - Looker deployment and version management

#### Refactoring Commands
- **`implement/refactoring/btdpframework.md`** - BTDP Framework compliance refactoring
- **`implement/refactoring/personal.md`** - Personal project compliance refactoring

### Core Commands
- **`utilities/update_memory_bank.md`** - Update CLAUDE.md memory bank with project analysis
- **`utilities/claude_usage_metrics.md`** - Track and analyze Claude usage metrics

### Audit Commands
- **`gcpaudit/projects.md`** - GCP security audit and compliance procedures
- **`gcpaudit/best_practices_bq.md`** - BigQuery optimization and best practices analysis
- **`gcpaudit/optimize_context.md`** - Memory bank context optimization for BTDP framework

## Command Structure

Each command follows this standardized structure:

```markdown
# [Command Name]

## Purpose
[Brief description of when to use this command]

## Prerequisites
[What must be true before running this command]

## Workflow Steps
[Numbered list of steps the AI will follow]

## Success Criteria
[How to verify the command completed successfully]

## Description Template
$ARGUMENTS

## Examples
[Concrete usage examples]
```

## Best Practices

### When to Use Each Command Type

1. **New Feature Development**: Use `implement/full.md`
   - Creates proper git workflow
   - Ensures complete testing
   - Handles PR creation

2. **Iterative Development**: Use `implement/change.md`
   - Continues work on existing branches
   - Maintains development momentum
   - Skips redundant git operations

3. **Quick Fixes**: Use `implement/standard.md`
   - Minimal overhead for simple changes
   - No deployment complexity
   - Rapid prototyping

4. **Code Quality**: Use `implement/compliance.md`
   - Enforces coding standards
   - Security compliance
   - Pre-deployment validation

## Workflow Integration and Cross-References

### Enhanced Command Intelligence

All commands now include **Workflow Integration** sections that provide:

- **Prerequisites Commands**: What should be done before using this command
- **Follow-up Commands**: Recommended next steps after command completion
- **Alternative Flows**: When to use different commands instead
- **Quality Gate Dependencies**: Required conditions for successful completion

### Command Relationship Matrix

| Current Command | Recommended Follow-up | Alternative if Issues | Quality Gate |
|-----------------|----------------------|---------------------|--------------|
| `implement/standard.md` | `implement/compliance.md` | `implement/full.md` | Basic quality checks |
| `implement/compliance.md` | `gcpaudit/projects.md` | `implement/refactoring/*` | All quality gates |
| `implement/full.md` | `gcpaudit/projects.md` | `implement/compliance.md` | Complete workflow |
| `implement/change.md` | `implement/compliance.md` | `implement/full.md` | Iterative quality |
| `implement/e2etests/btdpframework.md` | `implement/compliance.md` | `implement/refactoring/*` | Enterprise pipeline testing |
| `implement/e2etests/personalproject.md` | `implement/compliance.md` | `implement/refactoring/*` | Personal project testing |
| `implement/release.md` | `implement/compliance.md` | `implement/full.md` | Release workflow |
| `gcpaudit/projects.md` | `implement/compliance.md` | Security team review | Security compliance |
| `gcpaudit/best_practices_bq.md` | `implement/compliance.md` | Manual optimization | BigQuery optimization |
| `gcpaudit/optimize_context.md` | `utilities/update_memory_bank.md` | Manual optimization | Memory bank optimization |
| `utilities/update_memory_bank.md` | `implement/compliance.md` | Manual update | Documentation quality |
| `utilities/claude_usage_metrics.md` | Analysis and reporting | Manual tracking | Usage monitoring |

### Intelligent Command Progression

The AI now provides **proactive workflow guidance**:

#### Example Workflow Progression:
```
User: "/implement/standard.md Add user validation"
AI: ✅ Completes implementation
    🎯 "Implementation complete! Based on workflow integration:
       → RECOMMENDED: /implement/compliance.md for quality validation
       → IF DEPLOYING: /implement/full.md for complete deployment
       → IF SECURITY-SENSITIVE: /gcpaudit/projects.md for security audit"

User: "Run compliance check"
AI: ✅ Runs /implement/compliance.md automatically
    🎯 "Compliance achieved! Based on cross-references:
       → NEXT: /gcpaudit/projects.md for security validation
       → THEN: Ready for production deployment"
```

### Error Recovery Integration

Commands now include **Error Recovery Procedures** with:

- **Specific error message matching** for immediate solutions
- **Alternative command suggestions** when current approach fails
- **Escalation pathways** for complex issues
- **Recovery decision trees** for systematic problem-solving

### Quality Gate Enforcement

The enhanced commands automatically enforce **quality gates**:

- **Prerequisite Validation**: AI checks prerequisites before command execution
- **Quality Dependencies**: AI ensures quality standards before proceeding
- **Security Checkpoints**: AI recommends security audits at appropriate points
- **Documentation Gates**: AI ensures documentation updates for user-facing changes

### Command Selection Decision Tree

```
Is this a new feature?
├── Yes → Use implement/full.md
└── No
    ├── Working on existing branch?
    │   ├── Yes → Use implement/change.md
    │   └── No → Is this a quick fix?
    │       ├── Yes → Use implement/standard.md
    │       └── No → Do you need comprehensive testing?
    │           ├── Yes → BTDP Framework? → Use implement/e2etests/btdpframework.md
    │           │                      → Personal Project? → Use implement/e2etests/personalproject.md
    │           └── No → Use implement/compliance.md
```

## Variable Substitution

Commands use `$ARGUMENTS` as a placeholder for specific requirements. When using a command:

1. Replace `$ARGUMENTS` with detailed description of your task
2. Include relevant context (files, requirements, constraints)
3. Specify expected outcomes

**Example:**
```
Command: implement/full.md
$ARGUMENTS: Add user authentication feature with JWT tokens, including login/logout endpoints, middleware for protected routes, and unit tests. Update the user service to handle password hashing and validation.
```

## Integration with CLAUDE.md

Commands work in conjunction with your CLAUDE.md configuration:

- **Project Standards**: Commands apply appropriate coding standards based on project type
- **Testing Requirements**: Commands enforce testing policies from CLAUDE.md
- **Deployment Patterns**: Commands use correct deployment procedures
- **Quality Gates**: Commands apply linting, formatting, and security requirements

## Troubleshooting

**Command Not Working as Expected?**
1. **Project Detection Issues:**
   - Check for `modules/` directory + `Makefile` (BTDP Framework)
   - Check for `pyproject.toml` + single `src/` (Personal Project)
   - Verify path location matches expected patterns
   
2. **Prerequisites Not Met:**
   - Ensure clean working directory for new branches
   - Verify access to deployment environments
   - Check for required tools (gcloud, uv, make)
   
3. **Arguments Insufficient:**
   - Provide specific implementation details
   - Include expected behavior and outcomes
   - Mention relevant files or components
   
4. **Build/Deployment Failures:**
   - Check environment variables in `test_env.sh` (BTDP)
   - Verify infrastructure is deployed (`make ENV=<env> deploy`)
   - Ensure service accounts have proper permissions
   - Review module-specific `iac/locals.tf` configuration

**Common Error Scenarios:**
- **"Module not found"** → Run dependency installation first
- **"Deployment failed"** → Check GCP permissions and project access
- **"Tests failing"** → Verify test data setup and environment configuration
- **"Pylint score < 10"** → Refactor code structure, don't disable rules

**Missing Command for Your Use Case?**
Commands can be extended or customized. Follow the standard structure and add new command files as needed.