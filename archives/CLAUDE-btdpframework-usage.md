# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Framework Overview

This is the L'Oréal BTDP (Beauty Tech Data Platform) Agents repository - part of the BTDP Framework v2.26.2. This repository serves as the base framework for building data platform infrastructure on Google Cloud Platform, providing reusable templates, configuration patterns, and deployment automation for BTDP projects.

The framework uses Make-based workflows with Terraform for infrastructure management and supports multiple module types including Cloud Run services, Cloud Run jobs, Cloud Functions, Vertex AI pipelines, and configuration-only modules.

## Essential Commands

### Framework Infrastructure
```bash
# Deploy complete infrastructure for an environment (dv, qa, np, pd)
ENV=dv make deploy

# Clean and rebuild infrastructure  
ENV=dv make clean deploy

# Plan infrastructure changes
ENV=dv make plan

# Initialize new project infrastructure
ENV=dv make init

# Setup CI/CD pipeline
make cicd
```

### Module Development
```bash
# Deploy specific module
ENV=dv make <module-name>

# Create new module from template
make init-module

# Test specific module
ENV=dv make test-module-<module-name>

# Deploy only infrastructure for module
ENV=dv make iac-deploy-module-<module-name>
```

### Configuration Generator (Python Tool)
```bash
# Run full test suite for config generator
make test-dataflow

# Install development dependencies
python3.12 -m venv bin/config_generator/.venv
source bin/config_generator/.venv/bin/activate
python3.12 -m pip install -r bin/config_generator/requirements.txt

# Generate workflows from YAML configurations
python3.12 bin/config_generator/main.py
```

### Code Quality & Testing
```bash
# Format Python code (MANDATORY before commits)
black -l 120 src/

# Lint Python code
pylint --reports=n --rcfile=.pylintrc <files>

# Run tests with coverage
pytest -vv --cov <module> --cov-config=.coveragerc --cov-report term-missing

# Security scan
bandit -r <files> -c .bandit.yaml
```

## Repository Architecture

### Core Structure
```
btdp-agents/
├── iac/                    # Core Terraform infrastructure modules
├── modules/                # Application module templates and samples
│   ├── cloudrun-fastapi.sample/    # FastAPI service template
│   ├── cloudrun-job.sample/        # Cloud Run job template  
│   ├── vertex.sample/              # Vertex AI pipeline template
│   └── configurations.sample/      # Configuration-only template
├── configuration/          # YAML configuration templates for GCP services
│   ├── datasets/          # BigQuery dataset definitions
│   ├── tables/            # BigQuery table schemas
│   ├── workflows/         # Cloud Workflows definitions
│   ├── dataquality/       # Data quality scan configurations
│   └── monitoring/        # Alerting and monitoring setup
├── environments/          # Environment-specific JSON configurations
│   ├── dv.json           # Development environment
│   ├── qa.json           # Quality assurance environment
│   ├── np.json           # Non-production (UAT) environment
│   └── pd.json           # Production environment
├── bin/config_generator/  # Python tool for generating workflows from YAML
├── setup/                 # Infrastructure initialization scripts
├── Makefile              # Root-level build automation
└── module.mk             # Module-specific build targets and rules
```

### Module Types & Deployment Targets
- **gcr** - Google Cloud Run services (default API/web applications)
- **gcrjob** - Google Cloud Run jobs (batch processing, ETL)
- **gcf** - Google Cloud Functions v2 (event-driven functions)
- **vertex** - Vertex AI ML pipelines (machine learning workflows)
- **config** - Configuration-only modules (infrastructure without workloads)

### Environment Progression & Configuration
Environments follow strict progression: `dv → qa → np → pd`
Each environment can reference configurations from preceding environments.

**Key Environment Files** (`environments/` directory):
- **`dv.json`** - Development environment with project `oa-data-btdpagents-dv`
- **`qa.json`** - Quality assurance environment 
- **`np.json`** - Non-production (UAT) environment
- **`pd.json`** - Production environment
- **`cicd.json`** - CI/CD pipeline configuration
- **`apis.json`** - API gateway and proxy configurations

Each environment file defines project ID, developer groups, service accounts, and feature flags.

## Configuration System

### Environment Configuration
Environment files (`environments/<env>.json`) define:
- GCP project settings and naming
- Regional deployment configuration  
- Domain and networking settings
- Service account configurations
- Feature flags (Redis, front-end, etc.)

Example structure:
```json
{
    "project_env": "dv",
    "project": "oa-data-btdpagents-dv", 
    "developer_group": "DATA-GCP-BTDP-AGENTS-DEV@loreal.com",
    "app_service_number": "SNSVC1234567"
}
```

### YAML Configuration Templates
The `configuration/` directory provides reusable YAML templates for:
- **BigQuery**: datasets, tables, views, stored procedures
- **Cloud Workflows**: data pipelines and orchestration
- **Pub/Sub**: topics and subscriptions  
- **Monitoring**: alerting policies and notification channels
- **Data Quality**: validation rules and scans
- **Storage**: Cloud Storage buckets with lifecycle policies
- **GenAI**: AI agent configurations and contexts

### Workflow Auto-Generation
The Python tool `bin/config_generator/main.py` automatically generates Cloud Workflows from YAML configurations:
- Processes data pipeline definitions
- Creates parameterized workflow templates
- Generates environment-specific deployments
- Handles dependencies and orchestration logic

### GenAI Configuration Management
The framework provides automated deployment of GenAI configurations via Terraform integration with the BTDP GenAI Config API:

**Directory Structure:**
```
configuration/genai/
├── <context>/
│   ├── <config>.yaml          # Configuration definition
│   └── <config>-prompt.txt    # Optional system prompt file
└── README.md
```

**Context Naming Convention:**
- Context names follow kebab-case (e.g., `financial-analyst`, `data-expert`)
- Environment suffix automatically appended: `<context>-<env>`
- Special environment mapping:
  - `dv`, `qa` environments → use `dv` suffix
  - `np` environment → use `np` suffix
  - `pd` environment → use `pd` suffix
  - Example: `financial-analyst` in `dv` becomes `financial-analyst-dv`

**Configuration Example:**
```yaml
# configuration/genai/financial-analyst/default.yaml
name: Financial Data Analyst
type: chat
is_active: true
accept_attachments: true
description: 'Expert in financial data analysis and reporting'
params:
  is_single_turn: false
  llm:
    model: claude-37-sonnet
    args:
      temperature: 0.1
  tools:
    toolkit:
      - name: mcp
        params:
          url: https://cloudrun.....a.run/sse
      - name: semantic
        params:
          domain: finance_domain
          env: np
          views: ['revenue', 'costs', 'margins']
    tools_max_rounds: 15
```

**System Prompts:**
- Optional prompt files: `<config>-prompt.txt`
- Automatically injected into configuration during deployment
- Enable specialized agent behaviors and instructions

**Deployment:**
- Configurations automatically deployed via `ENV=<env> make deploy`
- Terraform manages CRUD operations via REST API
- Authentication handled via workflows service account

### Critical Configuration Directories
The `configuration/` directory contains these essential components:
- **`datasets/`** - BigQuery dataset definitions with permissions
- **`tables/`** - Table schemas with partitioning and clustering
- **`workflows/`** - Cloud Workflows for data orchestration
- **`triggers/`** - Event-driven triggers (schedulers, eventarc)
- **`statemachine/`** - State machine definitions for workflow triggers
- **`sql-scripts/sprocs/`** - Stored procedures for data processing
- **`buckets/`** - Cloud Storage configurations
- **`monitoring/`** - Alert policies and notification channels

## Development Workflow

### Creating Data Workflows (6-Step Process)

1. **Create Dataset** (`configuration/datasets/`)
   ```yaml
   # dataset.yaml
   description: "My dataset description"
   confidentiality: c1  # c1=public, c2=internal, c3=restricted
   deletion_protection: true
   ```

2. **Create Table** (`configuration/tables/`)
   ```yaml
   # table_v1.yaml  
   table_id: my_table
   dataset: dataset  # References dataset.yaml filename
   version: 1
   schema:
     - name: id
       type: STRING
       mode: REQUIRED
     - name: updated_at
       type: TIMESTAMP
       mode: REQUIRED
   ```

3. **Create Stored Procedure** (`configuration/sql-scripts/sprocs/`)
   ```yaml
   # my_procedure.yaml
   routine_id: load_my_table
   dataset_id: dataset  # References dataset.yaml filename
   definition_body: |-
     BEGIN
       -- Use table reference for project tables
       MERGE ${tables["table_v1"].reference} AS target
       USING source_table AS source
       ON source.id = target.id
       WHEN MATCHED THEN UPDATE SET updated_at = source.updated_at
       WHEN NOT MATCHED BY TARGET THEN INSERT VALUES(source.id, source.updated_at);
       -- Note: DELETE not considered for this MERGE pattern
     END;
   ```

   **MERGE Patterns:**
   - **Pattern A (Full Sync)**: `ON FALSE` with INSERT when NOT MATCHED BY TARGET, DELETE when NOT MATCHED BY SOURCE
   - **Pattern B (Incremental)**: `ON source.primary_key = target.primary_key` with standard UPDATE/INSERT (comment: DELETE not considered)
   
   **SDDS Table References** (for external datasets):
   ```sql
   -- Format: itg-btdppublished-gbl-ww-${project_env}.btdp_ds_c<confidentiality>_<reference>_<label>_eu_${project_env}.<table_name>
   itg-btdppublished-gbl-ww-${project_env}.btdp_ds_c1_201_elix_eu_${project_env}.product_reference
   ```

4. **Create Workflow** (`configuration/workflows/`)
   ```yaml
   # my_workflow.yaml
   workflow_name: load_data_workflow
   steps:
     - name: check_new_data
       # Check timestamp for lazy execution - only process if new data
     - name: call_procedure
       call: googleapis.bigquery.v2.jobs.query
       args:
         query: CALL ${datasets["dataset"].project}.${datasets["dataset"].dataset_id}.load_my_table()
   ```

5. **Create State Machine** (`configuration/statemachine/`)
   ```yaml
   # trigger_workflow.yaml
   workflow_name: my_workflow
   trigger_type: http  # or workflow
   source_objects:
     - bucket: source-bucket
       prefix: data/
   ```

6. **Create Triggers** (`configuration/triggers/`)
   
   **Pattern A - External Data Dumps (EventArc)**:
   ```yaml
   # eventarc/loadfile.yaml
   name: external_data_trigger
   event_type: google.cloud.storage.object.v1.finalized
   bucket: external-data-bucket
   # Use external table on bucket when possible
   ```
   
   **Pattern B - Internal Data Dumps (Scheduler)**:
   ```yaml
   # schedulers/data_dump.yaml
   name: internal_dump_scheduler
   schedule: "0 2 * * *"  # Daily at 2 AM
   # Should dump data and prepare using external table (most efficient)
   ```

### Creating Application Modules
1. **Initialize from template**: Use sample modules in `modules/*.sample/` as starting points
2. **Configure**: Update YAML configurations in module's `configurations/` directory  
3. **Implement**: Add business logic in module's `src/` directory
4. **Test**: Run `ENV=dv make test-module-<name>` for validation
5. **Deploy**: Use `ENV=dv make <module-name>` for deployment

### Module Structure
Each module follows this standard structure:
```
my-module/
├── Dockerfile                    # Container definition
├── requirements.txt              # Python dependencies (version pinned)
├── src/                         # Source code
│   ├── application.py           # Dependency injection setup
│   └── <feature>/               # Feature-specific code
├── configurations/              # YAML config files
│   ├── monitoring/             # Alert policies
│   ├── permissions_*.yaml      # IAM permissions per environment
│   └── sql/                    # SQL queries
├── iac/                        # Terraform infrastructure
└── test_env.sh                 # Environment setup for testing
```

### Key Development Rules

#### Python Standards
- **Version**: Use `python3.12` (fallback to `python3`)
- **Dependencies**: Pin exact versions in `requirements.txt` (e.g., `requests==2.31.0`)
- **Code Quality**: Format with `black -l 120` before any git operations
- **Dependency Injection**: Objects MUST be instantiated in `application.py`
- **Framework**: API modules MUST use `btdp-fastapi==1.1.*`

#### Configuration Syntax
- **File naming**: Use only core identifiers (e.g., `dataset.yaml` not `btdp_ds_c1_dataset_eu_dv.yaml`)
- **Template variables**: Use lowercase (e.g., `${project}` not `${PROJECT}`)
- **Cloud Workflows**: Escape expressions with `$${...}` to avoid Terraform conflicts
- **YAML**: Avoid colons in quoted strings to prevent parsing errors

## Application Name and Project Context

**App Name**: `btdpagt` (from `.app_name` file)
**Project Pattern**: `oa-data-btdpagents-<env>` where env is `dv`, `qa`, `np`, or `pd`

## Resource Naming Conventions

### Standard Patterns
All resources follow the BTDP naming convention with the `btdpagt` app name:
- **Cloud Run**: `btdpagt-gcr-<service>-ew4-<env>`  
- **Service Accounts**: `btdpagt-sa-<purpose>-<env>`
- **BigQuery Datasets**: `btdpagt_ds_<confidentiality>_<name>_eu_<env>`
- **Storage Buckets**: `btdpagt-gcs-<purpose>-eu-<env>`
- **Workflows**: `btdpagt-wkf-<workflow>-ew4-<env>`

### Environment Codes
- `dv` - Development environment
- `qa` - Quality assurance/testing environment  
- `np` - Non-production (UAT) environment
- `pd` - Production environment

## Important Notes

- Always specify `ENV=<environment>` when running Make commands
- The framework requires Python 3.12, Terraform 1.3.7+, and authenticated gcloud CLI
- App names should be 7 characters or fewer to avoid GCP resource naming conflicts
- Use `make help` in any directory for available targets specific to that context
- Configuration files support Jinja2 templating with environment-specific variable substitution

## Build System

### Makefile vs module.mk
- **`Makefile`** - Root-level infrastructure commands (`make deploy`, `make plan`, `make init`)
- **`module.mk`** - Module-specific targets for individual module development

**Module Operations**:
```bash
# Within a module directory, use module.mk targets
make -f ../../module.mk build    # Build module container
make -f ../../module.mk deploy   # Deploy module to GCP
make -f ../../module.mk test     # Run module tests
make -f ../../module.mk lint     # Code quality checks

# Or from root directory
ENV=dv make <module-name>        # Deploy specific module
ENV=dv make test-module-<name>   # Test specific module
```

## Repository Purpose

This `btdp-agents` repository serves as the **foundational framework** for BTDP (Beauty Tech Data Platform) projects. It provides:

- **Reusable Templates**: Standard module templates for common deployment patterns
- **Infrastructure as Code**: Terraform modules for consistent GCP resource provisioning  
- **Configuration Patterns**: YAML-based configuration system with environment promotion
- **Deployment Automation**: Make-based workflows for streamlined deployments
- **Best Practices**: Enforced coding standards, testing, and security requirements

When creating new BTDP projects, teams typically fork or reference this repository to inherit the standardized framework architecture and deployment patterns.
