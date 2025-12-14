# Repository Context & Locations

**Purpose:** Quick reference for repository locations and basic git workflow.

---

## Repository Mappings

### BTDP Services & Analytics
`~/projects/oa-datafactory-services/`

- analytics-services, btdp-am, btdp-amaas-cockpit, btdp-billingmgt, btdp-crunch
- btdp-dataexchange, btdp-eda, btdp-identitymgt, btdp-logs, btdp-notification
- btdp-serviceaccess, btdp-slots, btdp-slt, btdp-techprojectmgt, btdp-workstations, datavirt

### L'Oréal Data Factory Core
`~/projects/loreal-datafactory/`

- btdp-domains, project-framework, p360api

### AI/ML & Generative AI
`~/projects/oa-datafactory-aiml/`

- genai-mcp-servers, genai-mcp-servers-atlassian, btdp-generativeai-services

### Tooling & Packages
`~/projects/oa-datafactory-tooling/`

- btdp-python-packages

### Security & Compliance
`~/projects/oa-datafactory-intsec/`

- dataleak-prevention, housekeeping, vault

---

## Smart Git Workflow

**Always check state first:** `git status && git branch --show-current`

**Apply appropriate workflow:**
1. **On develop + no changes:** `git pull`
2. **On develop + changes:** `git stash && git pull && git stash pop`
3. **On branch + no changes:** `git checkout develop && git pull`
4. **On branch + changes:** `git commit && git checkout develop && git pull`

---

## Repository Context Loading

When working with repositories:
1. Navigate to correct path based on organization above
2. Apply smart git workflow
3. Read README.md and CLAUDE.md if present (repository-specific context)
4. Check recent activity: `git log --oneline -10`