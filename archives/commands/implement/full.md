# Full Implementation Protocol

## Purpose
Complete end-to-end feature implementation including git workflow, deployment, and pull request creation. Use this for new features that require full development lifecycle management.

## Prerequisites
- Clean working directory on develop branch
- Story number (STRYxxxxxxx) available for branch naming
- Access to deployment environment (default: dv)
- Required permissions for GCP resource verification

## Workflow Steps

You must follow this protocol completely. Create a Todo list according to these steps:

1. Ensure you are on develop branch with no uncommitted code (if there is, you stop).
2. Pull to ensure develop is up to date.
3. Create working branch with the following naming convention: `(fix|hotfix|feat)/STRYxxxxxxx/description`.
4. Understand the current implementation and code base to define the implementation steps. Ensure to follow the architecture patterns defined below. Remember to use appropriate tools to gather information on how to do it.
5. Make the implementation ensuring you are following the coding style of the current project (avoid code duplication).
6. Clean the code with `black -l 120` for formatting.
7. Build the project and solve all the issues. Never stop until you reach a pylint score of 10, with no security issues with bandit.
8. **Implement comprehensive error handling** throughout the codebase with proper exception types, error messages, and structured logging.
9. Deploy the solution in the specified environment. If no environment specified, you will use dv. Ensure the deployment is complete using the appropriate command. If not, search why and solve the issue until you succeed.
10. Check with gcloud command that the expected resources you deployed are present (BigQuery datasets and tables, Workflows, Cloud Run, Scheduler, Task Queue, PubSub topics & subscriptions, Secrets, Service Accounts - and check their permissions).
11. Update README.md and CLAUDE.md. In the README.md never forget to describe all the components, their usage and the permissions required. Don't forget also to mention the permission to trigger a functionality. **Include comprehensive error handling documentation** with common error scenarios and recovery procedures.
12. Commit the change with proper message format.
13. Push to the remote repository.
14. Create the appropriate pull request.

## Success Criteria
- [ ] New feature branch created and pushed
- [ ] Implementation follows project coding standards
- [ ] No code duplication (DRY principle applied)
- [ ] Code formatted with black -l 120
- [ ] Pylint score of 10 achieved
- [ ] **Error handling compliance achieved** (comprehensive error management validation)
- [ ] **Error documentation validated** (all error scenarios documented in README.md)
- [ ] Successful deployment verified in target environment
- [ ] GCP resources validated via gcloud commands
- [ ] Documentation updated (README.md and CLAUDE.md)
- [ ] Pull request created with proper description

## Workflow Integration

### Prerequisites Commands
- [ ] **Clean working directory**: Ensure `git status` shows no uncommitted changes
- [ ] **Updated develop branch**: Run `git checkout develop && git pull` to get latest changes
- [ ] **Story number available**: Have STRYxxxxxxx ready for branch naming
- [ ] **Environment access**: Verify deployment permissions for target environment

### Follow-up Commands
- [ ] **Security validation**: Run `gcpaudit/projects.md` after deployment for security compliance
- [ ] **Quality assurance**: Use `implement/compliance.md` if quality gates fail during build
- [ ] **Documentation review**: Consider updating enterprise documentation in Confluence via MCP servers

### Alternative Flows
- [ ] **Existing branch work**: Use `implement/change.md` instead if working on existing feature branch
- [ ] **Quality-first approach**: Run `implement/compliance.md` before this command if code quality is uncertain
- [ ] **Security-first approach**: Run `gcpaudit/projects.md` before deployment for high-risk changes

### Quality Gate Dependencies
- [ ] **Code quality**: Must achieve pylint 10/10 before proceeding to deployment
- [ ] **Security compliance**: Must resolve all bandit and safety issues before production deployment
- [ ] **Test coverage**: Must achieve 100% coverage before PR creation
- [ ] **Documentation**: Must update README.md and CLAUDE.md before PR creation

## Error Recovery Procedures

### Git Workflow Failures
| Error | Cause | Solution | Prevention |
|-------|-------|----------|------------|
| "Your branch is behind 'origin/develop'" | Develop branch outdated | `git pull origin develop`, resolve conflicts if any | Always pull before creating branch |
| "fatal: A branch named 'feat/STRYxxxx' already exists" | Branch naming conflict | Use different description or delete old branch if safe | Check existing branches: `git branch -a` |
| "error: failed to push some refs" | Remote branch conflicts | `git pull --rebase`, resolve conflicts, push again | Pull before pushing, use unique branch names |
| "Please tell me who you are" | Git config missing | `git config user.name/email` or use global config | Verify git configuration in new environments |

### Build and Quality Failures
| Error Type | Common Issues | Automatic Solutions | When to Use Alternative Commands |
|------------|---------------|-------------------|--------------------------------|
| **Pylint < 10** | Too many local variables, long functions, import issues | Extract helper methods, reorganize imports, split complex functions | Use `implement/compliance.md` for systematic quality fixing |
| **Bandit Security Issues** | Hardcoded secrets, SQL injection risks, subprocess calls | Move secrets to env vars, use parameterized queries, add `# nosec` with justification | Use `gcpaudit/projects.md` for comprehensive security audit |
| **Safety CLI Vulnerabilities** | Outdated dependencies with CVEs | `uv add package@latest` or pin to secure versions, no exceptions allowed | Check enterprise security policies for approved versions |

### Deployment Failures
| Error Message | Cause | Solution | Recovery Command |
|---------------|-------|----------|------------------|
| "Permission denied: iam.serviceAccounts.actAs" | Missing service account permissions | Grant serviceAccountUser role: `gcloud projects add-iam-policy-binding PROJECT --member=user:email --role=roles/iam.serviceAccountUser` | Use admin account for permission grants |
| "Error: resource X already exists" | Infrastructure conflict | Check existing resources: `gcloud <resource> list`, update terraform state if needed | Review and clean existing infrastructure |
| "Cloud Run service failed to start" | Application startup errors | Check logs: `gcloud run services logs read SERVICE --region=REGION`, fix application issues | Debug application locally first |
| "Build failed: MODULE not found" | Missing dependencies or wrong directory | Verify in module directory, run dependency install, check requirements.txt | Use `make -f ../../module.mk ENV=<env> clean build` |

### Environment-Specific Issues
| Project Type | Common Problems | Detection Commands | Solutions |
|--------------|-----------------|-------------------|-----------|
| **BTDP Framework** | Module.mk not found, wrong environment variables | `ls -la \| grep module.mk`, check `test_env.sh` exists | Navigate to module directory, verify environment configuration |
| **BTDP Framework** | Service account missing | `gcloud iam service-accounts list`, check `iac/locals.tf` | Deploy infrastructure: `make ENV=<env> deploy` from project root |
| **Personal Projects** | uv not available, pyproject.toml missing | `which uv`, `ls pyproject.toml` | Install uv: `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| **Personal Projects** | Terraform not configured | Check `iac/` directory exists, verify terraform state | Initialize terraform: `cd iac && terraform init` |

### GCP Resource Validation Failures
| Resource Type | Validation Command | Common Issues | Solutions |
|---------------|-------------------|---------------|-----------|
| **BigQuery Datasets** | `gcloud bq datasets list --project=PROJECT` | Dataset not created, wrong permissions | Check terraform configuration, verify BigQuery admin role |
| **Cloud Run Services** | `gcloud run services list --region=REGION` | Service not deployed, wrong region | Verify deployment logs, check region configuration in locals.tf |
| **Service Accounts** | `gcloud iam service-accounts list` | Service account missing, wrong project | Check iac/permissions.tf, ensure terraform apply completed |
| **Pub/Sub Topics** | `gcloud pubsub topics list` | Topics not created, subscription missing | Verify terraform modules, check pub/sub configuration |
| **Cloud Scheduler** | `gcloud scheduler jobs list --location=REGION` | Jobs not created, wrong schedule format | Check schedule configuration, verify timezone settings |

### Recovery Workflows
| Failure Stage | Recommended Recovery | Alternative Command | Notes |
|---------------|---------------------|-------------------|-------|
| **Git Operations** | Fix git issues, retry from step 1 | `implement/change.md` if branch exists | Clean working directory first |
| **Code Quality** | Use systematic quality improvement | `implement/compliance.md` | Focus on quality before deployment |
| **Security Issues** | Run comprehensive security audit | `gcpaudit/projects.md` | Address security before production |
| **Deployment** | Fix infrastructure, retry deployment | Check enterprise infrastructure docs | Verify environment configuration |
| **Resource Validation** | Investigate infrastructure configuration | Review terraform state and logs | May need infrastructure team support |

## Environment Detection
This command automatically adapts based on project type:

**BTDP Framework Projects:**
- **Detection**: Look for `modules/` directory, `Makefile`, `module.mk`, and `requirements.txt`
- **Build Commands**: `make -f ../../module.mk ENV=<env> build`
- **Deploy Commands**: `make -f ../../module.mk ENV=<env> deploy`
- **Test Commands**: `make -f ../../module.mk ENV=<env> e2e-test`
- **Infrastructure**: `make ENV=<env> deploy` (from project root)
- **Default Environment**: dv (development)
- **Available Environments**: dv, qa, np, pd

**Personal Projects:**
- **Detection**: Look for `pyproject.toml`, `uv.lock`, single `src/` directory
- **Dependencies**: `uv sync` (install/update dependencies)
- **Code Quality**: `uv run pylint src/`, `uv run bandit -r src/`, `uv run black -l 120 src/`
- **Installation**: `uv run pip install -e .` (development install)
- **Deployment**: Manual terraform or simple deployment patterns

## Task Description
$ARGUMENTS

## Example Usage
**BTDP Framework Example:**
```
$ARGUMENTS: Add data lineage tracking to the data-processing module. Implement BigQuery job monitoring, metadata collection from btdp_fastapi, and lineage graph generation. Include service layer for lineage API, controller for REST endpoints, and models for lineage schemas. Deploy to dv environment and validate BigQuery permissions.
```

**Personal Project Example:**
```
$ARGUMENTS: Create a CLI tool for GCP project analysis. Include commands for listing projects, analyzing IAM policies, and generating security reports. Use typer for CLI framework, aiohttp for async GCP API calls, and pandas for data processing.
```
