# Personal Configuration & Development Standards

## Personal Information

**Name:** Sebastien MORAND.
**Email:** sebastien.morand@loreal.com.
**Role:** CTO Data & AI at L'Oréal. In charge of Beauty Tech Data Platform (BTDP).
**ADM Identity:** sebastien.morand-adm@loreal.com (for sensitive GCP operations).
**L'Oréal GCP Organization ID:** 1090299993982.

---

## General rules

Whenever you make implementation on a project, you must ensure there is up-to-date following files:
- README.md to describe the project, how it works and how to use it
- CLAUDE.md for AI efficient interactions

When the user is refering to "Now" or "Today", you MUST use the `date` command to find exactly the date of today.

When the user says "We have an email" followed by a title or subject, it means the email is available in `~/Downloads/` folder as a `.eml` file. Search for `*.eml` files in that directory related to the provided title/subject.

---

## Information retrieval

To retrieve information use the mcp__mcprelay__rag_query_rag tool with the following index:
- when searching for a repository or a git repo or just a repo, you use the index "smo_repository_v1".
- when searching for an application or application service, you use the index "application_service_name_v1".
- when searching for a GCP project or a project, you use the index "smo_project_v1".
- when searching for a daset or bigquery dataset, you use the index "smo_dataset_v1".
- when searching for a table or bigquery table, you use the index "smo_table_v1". If you don't find the table, then you use the table itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.tables_v2 and the appropriate tools with a regexp to find the table.
- when searching for a domain, you use the index "domains_v1".
- when searching for an it_organization, you use the index "it_organizations_v3".

**Example:**
<< Using the projects table, I want to get the number of ... >>
=> You will run the rag_query_rag on the index "table" with the query "projects", then you continue the treatment.

<< Using the application services table, I want to get the number of ... >>
=> You will run the rag_query_rag on the index "table" with the query "application services", then you continue the treatment.

<< In the SDDS project, tell me if I have the permission ... >>
=> You will run the rag_query_rag on the index "project" with the query "SDDS", then you continue the treatment.

<< In the project SAP, list the bucket there ... >>
=> You will run the rag_query_rag on the index "project" with the query "SAP", then you continue the treatment.

<< In the repo tech project to find ... >>
=> You will run the rag_query_rag on the index "repository" with the query "tech project", then you continue the treatment.

<< In the repository btdp slt to find ... >>
=> You will run the rag_query_rag on the index "repository" with the query "btdp slt", then you continue the treatment.

<< Find information about the application "Finance Portal" ... >>
=> You will run the rag_query_rag on the index "application_service_name_v1" with the query "Finance Portal", then you continue the treatment.

<< Which application service handles customer data ... >>
=> You will run the rag_query_rag on the index "application_service_name_v1" with the query "customer data", then you continue the treatment.

<< What is the domain number of supply domain ... >>
=> You will run the rag_query_rag on the index "domains_v1" with the query "supply", then you get the domain information like the real domain name in the domain_name column of the domain_id (called sometimes domain_number) in the domain_id column.

NB: remember when you have identified the right index to use, to not put the index name in the query except if you are sure the redundancy is required (for example if I search GCP Datasets table, the query is "GCP datasets" on the index table and the query isn't "GCP datasets table". But if I search for GCP Tables table, it means I want the query "GCP Tables" in the index table, the redundancy is normal.

**SDDS Context**: When the user is requesting information about SDDS, don't forget it's always refering to the itg-btdppublished-gbl-ww-pd.
In SDDS, to understand the context, datasets are always following this convention: `btdp_ds_c[123]_(?P<domain_id>[O-9a-z])[0-9a-z]{2}_(?P<dataset_label>[0-9a-z]+)_eu_pd`.


---

## Data Exploration

To explorate data, you can use Looker Studio, the template URL to explore a table is the following:
https://lookerstudio.google.com/u/1/reporting/create?c.mode=edit&c.source=BQ_UI&ds.type=TABLE&ds.connector=BIG_QUERY&ds.billingProjectId=<BILLING_PROJECT>&ds.projectId=<PROJECT_ID>&ds.datasetId=<DATASET_ID>&ds.tableId=<TABLE_ID>

The default billing project to use if not mentionned is oa-data-btdpexploration-np.

---

## Google Cloud Platform

**Note:** For detailed GCP operations, infrastructure management, permission scanning, and deployment validation, use the `gcp-specialist` subagent. All GCP-specific configurations, commands, and workflows have been moved to the specialized subagent for better context management.

---

## Implementation Delegation

### BTDP Framework Implementation
**Pattern:** "implement the user story STRYxxxxxxx", "create new feature", "build API", "data workflow"
**Action:** Use the `btdp-implementation` subagent for end-to-end BTDP development:
- Full 14-step implementation protocol with TodoWrite tracking
- BTDP Framework patterns and configurations
- Quality gates (pylint 10/10, bandit security, comprehensive error handling)
- Data workflow creation (datasets, tables, workflows, triggers)
- FastAPI module development with proper dependency injection
- Complete deployment and validation cycle

### Google Cloud Platform Operations
**Pattern:** "check gcp", "bigquery permissions", "cloud run deployment", "gcp resources"
**Action:** Use the `gcp-specialist` subagent for all GCP operations:
- Permission scanning and IAM management
- Infrastructure validation and deployment verification
- BigQuery operations and resource management
- L'Oréal BTDP environment-specific configurations
- Error handling compliance with CLAUDE.md standards

### SQL Implementation
**Pattern:** "implement SQL query", "Generate a query", "Generate SQL", "Update SQL in the file"
**Actions:** Use the `sql-specialist` subagent for all SQL code generation.
- SQL Generation from SDDS
- SQL Modificaiton
- Stored procedure creation
- View or Materialized view Creation

Whenever you need to generate a time based queries where the request mention "since" a date, you must not hardcode the date but use current_date/current_datetime/current_timestamp method with date_sub/datetime_sub/timestamp_sub function to get the correct delay.

---

## Quick Reference

### Essential Commands

**Git Workflow:**

**Standard Feature Development:**
```bash
git checkout develop && git pull     # Switch to develop
git checkout -b feat/STRYxxxxxxx/desc # Create feature branch
git add . && git commit -S -m "[STRYxxxxxxx](feat) MESSAGE" && git push
# Create PR: develop ← feature branch (squash merge)
```

**GitHub CLI (Pull Requests):**
```bash
# Check if PR is mergeable with review status
gh pr view 528 --json reviewDecision,mergeable,statusCheckRollup

# Create PR with description
gh pr create --title "Title" --body "Description"

# View PR details with comments
gh api repos/owner/repo/pulls/123/comments
```

**Copy to Clipboard:**
```bash
cat <file> | pbcopy                # Copy file to clipboard.
```

### Common Patterns

**Branch Naming:**
- `feat/STRYxxxxxxx/description` - New features.
- `fix/STRYxxxxxxx/description` - Bug fixes.
- `hotfix/STRYxxxxxxx/description` - Critical fixes.
- `clean/STRYxxxxxxx/description` - Code cleaning and refactoring.
- `release/RLSExxxxxxx` - Release branches (release number format).

**Commit Messages:**
- `[STRYxxxxxxx](feat) Add new feature` - Feature commits.
- `[STRYxxxxxxx](fix) Fix bug in service` - Bug fix commits.
- `[STRYxxxxxxx](refactor) Improve code structure` - Refactoring commits.
- `[RLSExxxxxxx](release) Release RLSExxxxxxx` - Release commits.

**Pull Request Types:**
- **Standard PR:** Feature/fix branches → develop (ALWAYS squash merge)
- **Release PR:** develop → master (NEVER squash - use merge commit to preserve history)

---

## Utilities & Templates

### PDF Processing

Use the script `/Users/sebastien.morand/bin/read_pdfs.py`.

### Open File

When requested to open file, run a command `open`

Examples:
```bash
# Open a SVG file.
open <file>.svg

# Open an Excel file.
open <file>.xlsx

# Open an URL
open https://monsite.com/url?param1=toto&param2=tata
```

### Exploration
To explore a BigQuery table, you generate the following URL:
```
https://lookerstudio.google.com/u/1/reporting/create?c.mode=edit&c.source=BQ_UI&ds.type=TABLE&ds.connector=BIG_QUERY&ds.billingProjectId=<BILLING_PROJECT>&ds.projectId=<PROJECT_ID>&ds.datasetId=<DATASET_ID>&ds.tableId=<TABLE_ID>
```

To explore a BigQuery SQL statment, you generate the following URL:
```
https://lookerstudio.google.com/u/1/reporting/create?c.mode=edit&c.source=BQ_UI&ds.type=CUSTOM_QUERY&ds.connector=BIG_QUERY&ds.billingProjectId=<BILLING_PROJECT>&ds.sql=<SQL_STATEMENT>
```

### Lib version & information

Use context7 tool to ensure to have correct information about lib required while coding.


### Dependency Version Check
```bash
python3.11 -m venv /tmp/version_check_env
source /tmp/version_check_env/bin/activate && python3.11 -m pip install <package>
source /tmp/version_check_env/bin/activate && python3.11 -m pip freeze | grep <pattern>
rm -rf /tmp/version_check_env
```

### Mermaid Charts

```bash
mmdc -i diagram.mmd -o diagram.svg
```

### Todo List Management

**Method:** Automated extraction of action items from meeting archives to generate centralized todo list.

**Process:**
1. Scan archives/*.md files for action items and "Next Actions" sections
2. Extract todos and categorize by: Organizational, Technical Infrastructure, Data & Analytics, External Partnerships, Meetings, Administrative
3. Generate `/Users/sebastien.morand/meetings/todo-list.md` with checkboxes for team tracking
4. Avoid duplicates and assign ownership when clear from context

**Files Processed (Last Update: 2025-09-20):**
- 2025-09-02 - Co-Decision Meeting EMEA & Global BTDP.md
- 2025-09-02 - Co-Decision Meeting O+O & Global BTDP.md
- 2025-09-04 - TBR Google Cloud Platform.md
- 2025-09-04 - Test Results SSBI.md
- 2025-09-05 - Service Contract.md
- 2025-09-08 - PowerBI Microsoft CapaPrem issue.md
- 2025-09-11 - SAP Technical Review.md
- 2025-09-12 - AMaaS Steerco.md
- [35 total meeting files processed]

**Command to update:** Request scan of archives/*.md files for new todo items when new meeting files are added.
