# Claude Code Configuration & Commands

This repository contains a comprehensive Claude Code configuration system with standardized development workflows, quality standards, and project-specific instructions for both enterprise (BTDP Framework) and personal projects.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Configuration Structure](#configuration-structure)
3. [CLAUDE.md Files](#claudemd-files)
4. [Commands System](#commands-system)
5. [MCP Servers Configuration](#mcp-servers-configuration)
6. [CLAUDE Environment Setup](#claude-environment-setup)
7. [Integration Workflows](#integration-workflows)
8. [Quality Standards](#quality-standards)
9. [Project Types](#project-types)
10. [Getting Started](#getting-started)
11. [References](#references)

## 🎯 Overview

This configuration system provides:

- **Unified Development Standards**: Consistent coding practices across all projects
- **Quality Enforcement**: Mandatory pylint 10/10, bandit security, safety CLI checks
- **Code Quality**: DRY principle enforcement and code duplication elimination
- **Automated Workflows**: Standardized commands for implementation, refactoring, and compliance
- **Project-Specific Guidance**: Tailored instructions for BTDP Framework vs Personal projects
- **Optional Testing Framework**: E2E tests available via dedicated command when needed

## 📁 Configuration Structure

```
~/.claude/
├── README.md                           # This file - complete system overview
├── CLAUDE.md                          # Main global configuration & standards
├── CLAUDE-btdpframework.md            # BTDP Framework specific patterns
├── CLAUDE-personalprojects.md         # Personal projects specific patterns
├── CLAUDE-projects.md                 # GCP project references
├── CLAUDE-tables.md                   # BigQuery table references
├── CLAUDE-repo.md                     # Repository locations & git workflow
├── CLAUDE-gcpaudit.md                 # GCP audit configuration
└── commands/                          # Standardized development commands (10 total commands)
    ├── README.md                      # Commands system overview & usage guide
    ├── implement/                     # Implementation workflows (9 commands)
    │   ├── standard.md               # Basic feature implementation
    │   ├── change.md                 # Changes on existing branches  
    │   ├── full.md                   # Complete feature with deployment
    │   ├── compliance.md             # Quality enforcement & auditing
    │   ├── e2etests/                 # End-to-end tests workflows
    │   │   ├── btdpframework.md     # BTDP Framework enterprise pipeline testing
    │   │   └── personalproject.md   # Personal project application testing
    │   ├── refactoring/              # Code refactoring workflows
    │   │   ├── btdpframework.md     # BTDP Framework compliance refactoring
    │   │   └── personal.md          # Personal projects compliance refactoring
    │   └── looker/                   # Looker development workflows
    │       ├── code.md              # Looker LookML development
    │       └── deploy.md            # Looker deployment & version management
    └── gcpaudit/                     # GCP security auditing (1 command)
        └── projects.md               # Comprehensive GCP project security audit
```

## 📄 CLAUDE.md Files

### Main Configuration (`CLAUDE.md`)

**Purpose**: Global development standards and critical requirements that apply to ALL projects.

**Key Sections**:
- **Project Type Detection**: How to identify BTDP Framework vs Personal projects
- **Critical Requirements**: Non-negotiable rules (Python formatting, Git workflow, Quality standards)
- **Code Standards**: Architecture principles, coding rules, documentation standards
- **Google Cloud Platform**: Permission management, project references
- **Smart Pattern Detection**: Repository context, API integration, user story workflows

**Critical Rules**:
- `black -l 120` formatting after ANY Python modifications
- Git workflow: develop branch, proper commit messages, signed commits (key F1DD138F3FF39561)
- DRY principle enforcement (no code duplication)
- Quality enforcement: pylint 10/10, bandit security scans

### Framework-Specific Files

#### `CLAUDE-btdpframework.md`
- **Target**: Enterprise BTDP Framework projects
- **Structure**: `modules/` directory with `Makefile` and `module.mk`
- **Dependencies**: `requirements.txt` with `btdp_fastapi==1.1.*`
- **Commands**: `make -f ../../module.mk ENV=<env> build|deploy|test`
- **Features**: Multi-environment deployment, terraform infrastructure

#### `CLAUDE-personalprojects.md`
- **Target**: Independent utility and application projects
- **Structure**: Single `src/` directory with `pyproject.toml`
- **Dependencies**: `uv` package manager
- **Commands**: `uv sync && uv run src/main.py`
- **Features**: FastAPI for APIs, Typer for CLI, installable packages

#### Reference Files
- `CLAUDE-projects.md`: GCP project ID mappings for L'Oréal environments
- `CLAUDE-tables.md`: BigQuery table references for SDDS datasets
- `CLAUDE-repo.md`: Repository locations and smart git workflow patterns
- `CLAUDE-gcpaudit.md`: GCP security audit configuration and procedures

## ⚙️ Commands System

Standardized development workflows accessible via Claude Code commands. See [`commands/README.md`](commands/README.md) for complete details.

## 🔌 MCP Servers Configuration

Claude Code is extended with Model Context Protocol (MCP) servers that provide enhanced capabilities for enterprise integration and development workflows. The configuration is managed through `mcp_servers.json`.

### Current MCP Server Setup

```json
{
  "mcpServers": {
    "mcp-relay": {
      "type": "stdio",
      "command": "mcprelay"
    },
    "godri": {
      "command": "godri", 
      "args": ["mcp", "stdio"]
    },
    "context7": {
      "type": "http",
      "url": "https://mcp.context7.com/mcp"
    }
  }
}
```

### MCP Server Capabilities

#### 🏢 **mcp-relay** - L'Oréal Enterprise Integration
**Purpose**: Provides direct access to L'Oréal enterprise systems and BTDP infrastructure.

**Available Tools**:
- **Confluence Integration**: Search, read, create, and update Confluence pages
  - Search content across spaces with CQL queries
  - Create documentation and technical specifications
  - Manage page hierarchies and comments
- **SDDS (Data Platform)**: BigQuery dataset and table management
  - List and search datasets/tables across environments
  - Execute SQL queries with proper permissions
  - Manage dataset permissions and access control
- **ITBM (ServiceNow)**: Agile project management integration
  - Get epics, stories, sprints, and enhancements
  - Search application services and assignment groups
  - Track project progress and resource allocation
- **Group Management**: L'Oréal group membership and access control
  - Add/remove members from distribution lists
  - Search for similar groups using semantic matching
  - Manage access permissions across systems
- **API Portal**: L'Oréal API catalog integration
  - List available APIs and their specifications
  - Search API documentation and endpoints
  - Access OpenAPI/Swagger specifications
- **Notifications**: Enterprise notification system
  - Send emails with proper L'Oréal formatting
  - Manage notification quotas and delivery
  - Integrate with project workflows
- **Looker Integration**: BI platform deployment and management
  - Deploy Looker projects across environments
  - Manage LookML code and version control

#### 📁 **godri** - Google Workspace Integration
**Purpose**: Comprehensive Google Workspace automation for documentation, data processing, and collaboration.

**Available Tools**:
- **Google Drive**: File and folder management
  - Search, upload, download files with smart format conversion
  - Create and manage folder structures
  - Handle Google Workspace file formats automatically
- **Google Docs**: Document creation and management
  - Create documents with markdown support
  - Read and update content programmatically
  - Translate documents to different languages
  - Version control and collaboration features
- **Google Sheets**: Spreadsheet automation and data processing
  - Create and manage spreadsheets and worksheets
  - Read/write values, formulas, and formatting
  - Import CSV data and handle complex data transformations
  - Apply formatting, charts, and data analysis
- **Google Slides**: Presentation creation and management
  - Create presentations with themes and layouts
  - Add content (text, images, tables) programmatically
  - Copy slides between presentations
  - Version control and collaborative editing
- **Google Forms**: Form creation and management
  - Create forms with multiple question types
  - Manage sections and question logic
  - Translate forms to different languages
  - Handle form responses and data collection
- **Translation Services**: Multi-language support
  - Translate text, documents, and forms
  - Support for automatic language detection
  - Integration with Google Translate API
- **Speech-to-Text**: Audio transcription capabilities
  - Transcribe audio files in multiple formats
  - Support for multiple languages and dialects
  - Word timing and confidence scoring

#### 🧠 **context7** - Enhanced Context and Search
**Purpose**: Provides advanced semantic search and contextual understanding capabilities.

**Available Tools**:
- **Semantic Search**: Intelligent content discovery
- **Context Enhancement**: Improved understanding of code and documentation
- **Knowledge Integration**: Connection between different information sources

### MCP Configuration Management

#### Modifying MCP Servers
To add or modify MCP servers, edit `~/.claude/mcp_servers.json`:

```bash
# Edit MCP configuration
vi ~/.claude/mcp_servers.json

# Validate JSON syntax
cat ~/.claude/mcp_servers.json | jq '.'
```

#### Server Types
- **stdio**: Local command-line tools that communicate via standard input/output
- **http**: Remote servers accessed via HTTP/HTTPS endpoints
- **Custom**: Specialized integration protocols

#### Integration with Commands
MCP servers are automatically available when using command templates:
- **Data Operations**: Use SDDS tools for BigQuery queries and dataset management
- **Documentation**: Use Google Workspace tools for README and technical documentation
- **Project Management**: Use ITBM tools for story tracking and sprint management
- **Security Audits**: Use enterprise tools for permission and compliance checking

## 🖥️ CLAUDE Environment Setup

Claude Code is configured through environment variables and aliases defined in `~/.bashrc` for optimal integration with L'Oréal enterprise systems.

### Vertex AI Configuration

Claude Code uses Google Vertex AI for enterprise compliance and data residency:

```bash
# Vertex AI Configuration
export CLAUDE_CODE_USE_VERTEX=1              # Use Vertex AI instead of direct Anthropic API
export CLOUD_ML_REGION=europe-west1          # EU data residency compliance
export ANTHROPIC_VERTEX_PROJECT_ID=oa-data-btdpexploration-np  # L'Oréal exploration project
export DISABLE_PROMPT_CACHING=1              # Disable caching for security
export MCP_SERVERS_CONFIG=""                 # MCP servers loaded from mcp_servers.json
```

**Benefits of Vertex AI Integration**:
- **Data Residency**: All processing stays within EU regions
- **Enterprise Security**: Integrated with L'Oréal GCP security policies
- **Audit Compliance**: Full logging and monitoring through GCP
- **Cost Management**: Centralized billing and quota management

### Enhanced Claude Alias

The `claudio` function provides enhanced workflow integration:

```bash
claudio() {
    if [ "$1" == "" ]; then
        # Continue previous conversation with MCP servers enabled
        claude --mcp-config "$(cat ~/.claude/mcp_servers.json|jq -c)" --continue || \
            claude "$(cat ~/.claude/mcp_servers.json|jq -c)";
    else
        # Start new conversation with MCP servers and arguments
        claude --mcp-config "$(cat ~/.claude/mcp_servers.json|jq -c)" "$@";
    fi;
    reset;  # Clear terminal after session
}
```

**Usage Examples**:
```bash
# Continue previous conversation with all MCP servers
claudio

# Start new conversation with specific prompt
claudio "Help me implement a new data pipeline"

# Use from specific project directory
claudio-misc  # Runs from ~/projects/claude directory
```

### L'Oréal Integration Variables

Additional environment variables for enterprise integration:

```bash
# L'Oréal Specific Configuration
export SANDBOX_ENV="scm"                     # Current sandbox environment
export PROJECT_ENV="${SANDBOX_ENV}"          # Project environment context
export PROJECT="${GCP_PROJECT}"              # Active GCP project
export PYTHONPATH="src"                      # Python import path for development
export BTDP_DEPLOY_BUCKET="btdp-gcs-deploy-eu-${SANDBOX_ENV}"  # Deployment bucket
export EXCHANGE_TOKEN_API="https://api.loreal.net/global/it4it/btdp-exchangetoken/v1/tokens"

# Google Workspace Integration
export GODRI_CLIENT_FILE=$HOME/.gcp/scm-pwd.json  # Service account for Google Workspace
```

### Authentication Setup

Multiple authentication contexts for different enterprise systems:

```bash
# GCP Authentication Functions
curl_i()      # Identity token for internal APIs
curl_a()      # Access token for GCP resources  
curl_adm()    # Admin access token for privileged operations
curl_ia()     # Combined identity + access tokens
curl_iadm()   # Combined identity + admin tokens

# Convenience Aliases
alias reauthent='tmux new-session -d "(gcloud auth login && gcloud auth application-default login )"'
alias gclouda="gcloud --format=json --account=sebastien.morand-adm@loreal.com"
```

### Log Management

Centralized logging for development and debugging:

```bash
# Log Reading Function
oalogs() {
    tail -f $(ls -1 $HOME/.logs/${1}.log* | tail -n ${2:-1} | head -n 1);
}

# Usage Examples
oalogs mymodule     # Tail latest log for mymodule
oalogs api 2        # Tail second-latest log for api
```

## 🔄 Integration Workflows

The combination of MCP servers, commands, and environment configuration creates powerful integrated workflows for L'Oréal development.

### Enterprise Development Workflow

#### 1. **Project Initialization with Enterprise Integration**
```bash
# Setup environment
claudio "Initialize new BTDP Framework project with proper structure"

# Automatic capabilities:
# - Creates modules/ structure via commands
# - Sets up GCP projects via mcp-relay SDDS integration  
# - Configures permissions via mcp-relay group management
# - Creates documentation via godri Google Docs integration
```

#### 2. **Development with Real-time Enterprise Data**
```bash
# Start development session
claudio "Implement user authentication for the API module"

# Enhanced capabilities:
# - Access ITBM stories and requirements via mcp-relay
# - Query existing datasets via SDDS integration
# - Reference enterprise APIs via API Portal
# - Create technical documentation via Google Workspace
```

#### 3. **Quality Assurance with Enterprise Compliance**
```bash
# Run compliance checks
claudio "/implement/compliance.md Full compliance audit with enterprise standards"

# Integrated scanning:
# - Code quality via standard tools
# - Security compliance via enterprise policies
# - Data permissions via SDDS dataset auditing
# - Documentation completeness via Confluence integration
```

#### 4. **Deployment with Enterprise Validation**
```bash
# Deploy and validate
claudio "/implement/full.md Deploy to production with security validation"

# Automated validation:
# - GCP resource verification via mcp-relay
# - Permission auditing via group management tools
# - Documentation updates via Confluence
# - Notification to stakeholders via enterprise notification system
```

### Data Engineering Workflow

#### 1. **Dataset Discovery and Analysis**
```bash
claudio "Find all tables related to customer data in the BTDP platform"

# MCP-enabled discovery:
# - Search SDDS catalog for relevant datasets
# - Query table schemas and lineage
# - Check data permissions and access patterns
# - Generate data documentation in Google Sheets
```

#### 2. **Pipeline Development with Compliance**
```bash
claudio "Create data transformation pipeline with proper governance"

# Integrated development:
# - Reference existing pipelines via SDDS
# - Apply enterprise data governance policies
# - Create technical specifications in Confluence
# - Track development progress in ITBM
```

### Documentation and Knowledge Management

#### 1. **Automated Documentation Generation**
```bash
claudio "Generate complete technical documentation for this module"

# Multi-platform documentation:
# - Code documentation in repository
# - Technical specifications in Confluence
# - User guides in Google Docs
# - API documentation in API Portal
```

#### 2. **Knowledge Sharing and Collaboration**
```bash
claudio "Create training materials for the new data platform features"

# Collaborative creation:
# - Presentation materials via Google Slides
# - Interactive forms via Google Forms
# - Video transcription via speech-to-text
# - Multi-language support via translation services
```

### Security and Compliance Workflows

#### 1. **Enterprise Security Auditing**
```bash
claudio "/gcpaudit/projects.md Complete security audit of production environment"

# Comprehensive auditing:
# - GCP permissions via mcp-relay
# - Dataset access patterns via SDDS
# - Group memberships via enterprise directory
# - Compliance reporting via Google Sheets
```

#### 2. **Access Management and Governance**
```bash
claudio "Review and update access permissions for the data platform"

# Integrated access management:
# - Group membership management
# - Dataset permission auditing
# - Compliance documentation updates
# - Stakeholder notification workflows
```

### Implementation Commands (`commands/implement/`)

#### Core Workflows
- **`standard.md`**: Basic feature implementation with quality checks
  - *Use for*: Simple code changes, prototyping, quick fixes
  - *Features*: Local testing, basic quality checks, minimal deployment
  - *Quality Gates*: Pylint 10/10, bandit clean, test coverage maintenance
  
- **`change.md`**: Enhancements on existing feature branches
  - *Use for*: Iterative development on work-in-progress features
  - *Features*: Continues existing branch work, maintains development momentum
  - *Quality Gates*: Builds on existing quality foundation, regression testing
  
- **`full.md`**: Complete feature development with deployment and PR creation
  - *Use for*: New features requiring full development lifecycle
  - *Features*: Git workflow, deployment, GCP validation, PR creation
  - *Quality Gates*: 100% coverage, comprehensive testing, documentation updates
  
- **`compliance.md`**: Quality enforcement and comprehensive code auditing
  - *Use for*: Code quality enforcement, pre-deployment validation, compliance audits
  - *Features*: Comprehensive quality audit, security scanning, documentation validation
  - *Quality Gates*: Pylint 10/10, zero security issues, 100% coverage, DRY principle

#### Specialized Workflows

##### Refactoring Commands (`refactoring/`)
- **`btdpframework.md`**: BTDP Framework compliance refactoring
  - *Use for*: Converting projects to BTDP Framework standards
  - *Features*: btdp_fastapi integration, async/await patterns, enterprise compliance
  - *Quality Gates*: Framework compliance, dependency management, security standards
  
- **`personal.md`**: Personal project compliance refactoring
  - *Use for*: Upgrading personal projects to modern standards
  - *Features*: pyproject.toml migration, uv integration, code modernization
  - *Quality Gates*: Modern Python practices, dependency management, quality standards

##### Looker Development Commands (`looker/`)
- **`code.md`**: Looker LookML development workflows
  - *Use for*: LookML model development, dashboard creation, view modifications
  - *Features*: LookML syntax validation, project structure maintenance
  - *Quality Gates*: LookML best practices, naming conventions, performance optimization
  
- **`deploy.md`**: Looker deployment and version management
  - *Use for*: Deploying Looker changes through environment progression
  - *Features*: Commit squashing, branch merging, environment-specific deployment
  - *Quality Gates*: Proper git workflow, deployment validation, environment mapping

#### Audit Commands (`commands/gcpaudit/`)
- **`projects.md`**: Comprehensive GCP project security auditing
  - *Use for*: Security audits, compliance verification, permission analysis
  - *Features*: IAM analysis, dataset permissions, infrastructure scanning, external audit integration
  - *Scope*: Project permissions, service accounts, datasets, storage, Python code security
  - *Output*: Comprehensive audit.md report with severity classification and remediation guidance

### Command Selection Guide

#### Quick Decision Tree
```
What do you need to do?
├── New feature from scratch?
│   ├── Simple/prototype → `implement/standard.md`
│   └── Full lifecycle → `implement/full.md`
├── Working on existing feature branch?
│   └── Iterative changes → `implement/change.md`
├── Code quality issues?
│   ├── Quick fixes → `implement/standard.md`
│   └── Comprehensive audit → `implement/compliance.md`
├── Major refactoring needed?
│   ├── BTDP Framework migration → `implement/refactoring/btdpframework.md`
│   ├── Personal project upgrade → `implement/refactoring/personal.md`
│   └── General refactoring → `implement/compliance.md`
├── Looker development?
│   ├── LookML changes → `implement/looker/code.md`
│   └── Deployment → `implement/looker/deploy.md`
└── Security audit needed?
    └── GCP security review → `gcpaudit/projects.md`
```

#### Command Progression Workflows

**New Feature Development**:
1. `implement/standard.md` → Quick prototype/implementation
2. `implement/compliance.md` → Quality validation
3. `implement/full.md` → Full deployment and PR

**Quality Improvement**:
1. `implement/compliance.md` → Comprehensive quality audit
2. `implement/refactoring/*` → If major changes needed
3. `gcpaudit/projects.md` → Security validation

**Production Deployment**:
1. `implement/compliance.md` → Pre-deployment quality check
2. `gcpaudit/projects.md` → Security audit
3. `implement/full.md` → Complete deployment workflow

### Command Usage Pattern

All commands follow a consistent workflow pattern:

1. **Prerequisites Check**: Branch status, story numbers, environment setup
2. **Implementation Steps**: Detailed step-by-step workflow
3. **Quality Gates**: Pylint 10/10, bandit security, safety CLI, coverage 100%
4. **Success Criteria**: Clear completion requirements
5. **Environment Detection**: Automatic BTDP Framework vs Personal project detection
6. **Error Recovery**: Comprehensive troubleshooting and alternative flows
7. **Workflow Integration**: Prerequisites, follow-ups, and alternative commands

## 🔧 Quality Standards

### Mandatory Quality Gates

**Code Quality**:
- **Pylint**: Score of 10/10 without disabling any rule (using `.pylintrc`)
- **Code Duplication**: Zero tolerance - DRY principle enforcement
- **Formatting**: `black -l 120` mandatory before commits

**Security**:
- **Bandit**: Zero security issues (document `# nosec` with justification)
- **Safety CLI**: Zero dependency vulnerabilities (no exceptions allowed)

**Testing**:
- **Optional Testing**: Use `/implement/e2etests.md` command when comprehensive testing is needed
- **Quality-First Approach**: Focus on code quality and security over mandatory test coverage

**Documentation**:
- **README.md**: Complete feature documentation, usage, permissions
- **CLAUDE.md**: Implementation guidance for future development

### Code Standards

**Architecture Principles**:
- **DRY Principle**: Eliminate code duplication via utilities and shared modules
- **Async/Await**: Full asyncio implementation (`aiohttp` over `requests`)
- **Object-Oriented**: Class-based design with separation of concerns
- **Dependency Injection**: Centralized in `application.py` (BTDP) or `main()` (Personal)

**Technical Requirements**:
- **Python**: Always use `python3.11`
- **Import Organization**: Clean, properly ordered imports
- **String Handling**: f-strings for interpolation, `%` style for logging
- **Security**: Never store credentials in code

## 🏗️ Project Types

### Detection Matrix

| Aspect | BTDP Framework | Personal Projects |
|--------|----------------|-------------------|
| **Structure** | `modules/` directory | Single `src/` directory |
| **Dependencies** | `requirements.txt` | `pyproject.toml` + `uv` |
| **Build System** | `make` + enterprise tools | Manual + `uv` commands |
| **Framework** | `btdp_fastapi==1.1.*` | FastAPI + Typer |
| **Testing** | Enterprise compliance | Standard pytest |
| **Deployment** | Multi-env + terraform | Manual/simple terraform |
| **Location** | Can be anywhere | Can be anywhere |

### When to Use Each Type

**BTDP Framework**:
- Data transformation and BI projects
- Enterprise APIs and MCP servers
- Multi-environment deployment (dv, qa, np, pd)
- L'Oréal compliance and security standards

**Personal Projects**:
- Standalone utilities and tools
- Rapid prototyping
- Individual applications
- CLI tools and scripts

## 🚀 Getting Started

### Quick Start Guide

#### 1. **Identify Your Project Type**
Run these commands in your project directory:

```bash
# Check for BTDP Framework indicators
ls -la | grep -E "(modules|Makefile|module.mk|requirements.txt)"

# Check for Personal Project indicators  
ls -la | grep -E "(pyproject.toml|uv.lock|src)"
```

**BTDP Framework** if you see: `modules/` directory + `Makefile` + `requirements.txt`  
**Personal Project** if you see: `pyproject.toml` + single `src/` directory

#### 2. **Choose Your Command**
Use the [Command Selection Guide](#command-selection-guide) decision tree, or:

```bash
# Quick command selection
claudio "I need to [describe your task]"
# Claude will automatically suggest the appropriate command
```

#### 3. **Execute Command**
```bash
# Using Claude Code with MCP servers
claudio "/implement/standard.md Add user validation with proper error handling"

# Or specify exact requirements
claudio "/implement/full.md [STRYxxxxxxx] Complete user authentication feature with JWT tokens, unit tests, and deployment to dv environment"
```

### Common Scenarios

#### 🆕 **Starting New Feature Development**
```bash
# For simple features or prototypes
claudio "/implement/standard.md Add configuration validation to the API"

# For complete feature lifecycle
claudio "/implement/full.md [STRY1234567] Implement user authentication with OAuth2, including tests and deployment"
```

#### 🔄 **Working on Existing Features** 
```bash
# Continue work on existing branch
claudio "/implement/change.md Add password strength validation to existing user registration"
```

#### 🔍 **Code Quality & Compliance**
```bash
# Comprehensive quality audit
claudio "/implement/compliance.md Full compliance audit including security, testing, and documentation"

# Framework migration
claudio "/implement/refactoring/btdpframework.md Convert project to BTDP Framework standards"
```

#### 🔒 **Security & Auditing**
```bash
# GCP security audit
claudio "/gcpaudit/projects.md Complete security audit of production and non-production environments"
```

#### 📊 **Looker Development**
```bash
# LookML development
claudio "/implement/looker/code.md Add sales performance metrics to dashboard model"

# Looker deployment
claudio "/implement/looker/deploy.md Deploy dashboard changes to production environment"
```

### Project-Specific Setup

#### **BTDP Framework Projects**
```bash
# Navigate to module directory
cd modules/your-module-name

# Verify framework setup
ls -la | grep -E "(src|iac|.module_type|api_portal_details.json)"

# Ready for development
claudio "/implement/full.md [STRYxxxxxxx] Your feature description"
```

#### **Personal Projects**
```bash
# Ensure uv environment
uv sync

# Verify project structure
ls -la | grep -E "(src|pyproject.toml)"

# Ready for development  
claudio "/implement/standard.md Your feature description"
```

### Troubleshooting Setup

#### **Environment Issues**
```bash
# Re-authenticate GCP
reauthent

# Check Claude configuration
cat ~/.claude/mcp_servers.json | jq '.'

# Verify environment variables
echo $CLAUDE_CODE_USE_VERTEX
echo $ANTHROPIC_VERTEX_PROJECT_ID
```

#### **Project Structure Issues**
```bash
# BTDP Framework: Wrong directory
# Solution: Navigate to modules/your-module/ directory

# Personal Project: Missing dependencies
uv sync  # Install/update dependencies

# Missing files: Copy from framework template
cp -r @.framework modules/your-new-module  # For BTDP Framework
```

### Next Steps After Setup

1. **Read Configuration**: Review relevant `CLAUDE-*.md` files for your project type
2. **Understand Standards**: Familiarize yourself with quality gates and requirements
3. **Start Development**: Use appropriate command from the selection guide
4. **Follow Workflows**: Each command provides detailed step-by-step instructions

## 📚 References

### Quick Commands
```bash
# Python formatting (mandatory)
black -l 120 src/

# Git workflow
git checkout develop && git pull
git checkout -b feat/STRYxxxxxxx/description
git add . && git commit -S -m "[STRYxxxxxxx](feat) MESSAGE" && git push

# BTDP Framework build
make -f ../../module.mk ENV=<env> build

# Personal project run
uv sync && uv run src/main.py
```

### Complete Command Reference

#### **Core Implementation Commands**
| Command | Purpose | Use When | Key Features |
|---------|---------|----------|--------------|
| `/implement/standard.md` | Basic implementation | Quick fixes, prototypes | Local testing, basic quality |
| `/implement/change.md` | Existing branch changes | Iterative development | Maintains momentum, regression testing |
| `/implement/full.md` | Complete lifecycle | New features | Git workflow, deployment, PR creation |
| `/implement/compliance.md` | Quality enforcement | Code audits, pre-deployment | Comprehensive quality, security scanning |

#### **Specialized Commands**
| Command | Purpose | Target | Key Features |
|---------|---------|---------|--------------|
| `/implement/refactoring/btdpframework.md` | BTDP compliance | Enterprise projects | Framework migration, async patterns |
| `/implement/refactoring/personal.md` | Modern standards | Personal projects | pyproject.toml, uv integration |
| `/implement/looker/code.md` | LookML development | Looker projects | Syntax validation, best practices |
| `/implement/looker/deploy.md` | Looker deployment | Looker releases | Environment progression, git workflow |
| `/gcpaudit/projects.md` | Security audit | Production systems | IAM analysis, compliance reporting |

#### **Command Usage Examples**
```bash
# Quick feature implementation
claudio "/implement/standard.md Add input validation with error handling"

# Complete feature development
claudio "/implement/full.md [STRY1234567] OAuth2 authentication with JWT tokens"

# Quality enforcement
claudio "/implement/compliance.md Full compliance audit with security scanning"

# Framework migration
claudio "/implement/refactoring/btdpframework.md Convert to BTDP Framework standards"

# Security audit
claudio "/gcpaudit/projects.md Complete security audit of production environment"
```

### Essential Files
- [`commands/README.md`](commands/README.md): Complete commands documentation
- `CLAUDE.md`: Global development standards
- Framework-specific configuration files

### Enterprise References
- Project mappings: `CLAUDE-projects.md`
- Table references: `CLAUDE-tables.md`
- Repository locations: `CLAUDE-repo.md`
- Security auditing: `CLAUDE-gcpaudit.md`

---

## 🔄 Workflow Integration

This configuration system integrates with Claude Code to provide:

1. **Automatic Project Detection**: Commands automatically detect BTDP Framework vs Personal projects
2. **Quality Enforcement**: Mandatory quality gates ensure consistent code standards
3. **Workflow Standardization**: Consistent development processes across all projects
4. **Documentation Standards**: Clear documentation requirements for maintainability

For detailed command usage and workflows, see [`commands/README.md`](commands/README.md).