# GCP Project Auditor - AI Instructions

This document provides AI-oriented instructions for using the GCP Project Auditor skill effectively.

## Skill Invocation

This skill should be invoked when the user asks to:
- Audit a GCP project
- Check GCP project security
- Scan a GCP project for compliance
- Review GCP project permissions
- Find security issues in a GCP project
- Assess GCP project risk

## Core Capabilities

1. **Resource Discovery**: Scan all resources using `gcloud asset search-all-resources`
2. **IAM Analysis**: Scan all IAM policies using `gcloud asset search-all-iam-policies`
3. **Security Validation**: Check against L'Oréal security policies
4. **Report Generation**: Create detailed markdown reports with findings

## Critical Security Checks

The skill performs the following CRITICAL checks:

### 1. Excessive Roles in Production/Non-Production
- **Trigger**: Project tag `env=pd` or `env=np`
- **Check**: Scan for 240+ excessive roles (see `references/excessive-roles.md`)
- **Severity**: CRITICAL
- **Examples**: roles/owner, roles/editor, roles/*admin, roles/*serviceAgent
- **Remediation**: Remove excessive roles, grant minimal permissions

### 2. Public Access to Resources
- **Resources**: BigQuery datasets/tables, Cloud Storage buckets
- **Check**: Look for `allUsers` or `allAuthenticatedUsers` in IAM bindings
- **Severity**: CRITICAL
- **Remediation**: Remove public access, grant specific permissions

### 3. Public Cloud Run Services
- **Check**: Cloud Run services with `allUsers` having `roles/run.invoker`
- **Severity**: CRITICAL
- **Remediation**: Require authentication, use IAP if needed

### 4. Public Cloud Functions
- **Check**: Cloud Functions with `allUsers` having `roles/cloudfunctions.invoker`
- **Supports**: Both 1st gen and 2nd gen functions
- **Severity**: CRITICAL
- **Remediation**: Require authentication, restrict to specific service accounts

### 5. Public IP on Databases
- **Databases**: Cloud SQL, AlloyDB
- **Check**: Cloud SQL with `ipv4Enabled=true`, AlloyDB with public IP
- **Severity**: CRITICAL
- **Remediation**: Disable public IP, use private IP only, use Cloud SQL Auth Proxy

### 6. External IP on Compute Instances
- **Check**: Compute instances with `natIP` (ONE_TO_ONE_NAT)
- **Severity**: CRITICAL (especially in production)
- **Remediation**: Remove external IP, use Cloud NAT or Identity-Aware Proxy

### 7. Overly Permissive Firewall Rules
- **Check**: Firewall rules with source `0.0.0.0/0` to sensitive ports
- **Sensitive Ports**: 22 (SSH), 3389 (RDP), 3306 (MySQL), 5432 (PostgreSQL), 1433 (MSSQL), 27017 (MongoDB)
- **Severity**: HIGH (firewall) or CRITICAL (if combined with public IPs)
- **Remediation**: Restrict source IP ranges, use Identity-Aware Proxy

### 8. User-Managed Service Account Keys
- **Check**: Service accounts with `keyType=USER_MANAGED`
- **Severity**: HIGH
- **Remediation**: Delete keys, use Workload Identity or short-lived tokens

## Execution Workflow

When the user requests an audit:

1. **Validate Project Access**
   ```bash
   gcloud projects describe <PROJECT_ID> --account sebastien.morand-adm@loreal.com
   ```

2. **Determine Environment**
   - Extract `labels.env` from project metadata
   - Classify as: pd (production), np (non-production), qa, dv (development)
   - Apply strict policies for pd/np environments

3. **Scan Resources**
   ```bash
   gcloud asset search-all-resources --scope=projects/<PROJECT_ID> --format=json
   ```
   - Store results in `resources.json`
   - Count by asset type
   - Flag specific types for deeper checks

4. **Scan IAM Policies**
   ```bash
   gcloud asset search-all-iam-policies --scope=projects/<PROJECT_ID> --format=json
   ```
   - Store results in `iam-policies.json`
   - Get project-level IAM policy
   - Check service account impersonation

5. **Analyze Security**
   - **If pd/np**: Check excessive roles against the 240+ role list
   - Check for public access (allUsers, allAuthenticatedUsers)
   - Check for public Cloud Run/Functions
   - Check for public IPs on databases and compute instances
   - Check firewall rules for overly permissive configurations
   - Check service account keys

6. **Generate Report**
   - Create markdown report with:
     - Executive summary (risk level: CRITICAL/HIGH/MEDIUM/LOW)
     - Resource inventory by type
     - Security findings by severity
     - Actionable recommendations
   - Save to `audit-report-<project_id>.md`

## Environment-Specific Policies

### Production (env=pd)
- **CRITICAL**: Excessive roles are security violations
- **CRITICAL**: Public access is prohibited
- **CRITICAL**: Public IPs are prohibited
- Must have encryption enabled
- Must have audit logging enabled
- Must have proper tagging

### Non-Production (env=np)
- **CRITICAL**: Excessive roles are security violations
- **CRITICAL**: Public access should be justified
- **CRITICAL**: Public IPs should be justified
- Should have encryption enabled
- Should have audit logging enabled

### QA (env=qa) and Development (env=dv)
- **WARNING**: Excessive roles should be reviewed
- **INFO**: Public access should be documented
- **INFO**: Public IPs should be documented

## Report Structure

```markdown
# GCP Project Audit Report: <project_id>

**Audit Date**: YYYY-MM-DD HH:MM UTC
**Auditor**: sebastien.morand-adm@loreal.com
**Project Environment**: pd/np/qa/dv
**Overall Risk Level**: 🔴 CRITICAL / 🟠 HIGH / 🟡 MEDIUM / 🟢 LOW

## Executive Summary
- Total Resources: X
- Critical Findings: X
- High Findings: X
- Medium Findings: X

## 1. Project Overview
[Project details]

## 2. Resource Inventory
[Resources by type]

## 3. IAM Security Analysis
[Permissions analysis]

## 4. Security Findings

### 🔴 CRITICAL Findings
[List with remediation steps]

### 🟠 HIGH Findings
[List with remediation steps]

### 🟡 MEDIUM Findings
[List with remediation steps]

## 5. Recommendations
[Prioritized action items]

## Appendix
[Full data references]
```

## Severity Classification

- **🔴 CRITICAL**: Immediate action required (within 24-48 hours)
  - Excessive roles in production
  - Public access to data
  - Public Cloud Run/Functions
  - Public IPs on databases/compute
  - Open firewall to sensitive ports

- **🟠 HIGH**: Urgent attention needed (within 1 week)
  - User-managed service account keys
  - Overly permissive firewall rules
  - Missing encryption

- **🟡 MEDIUM**: Should be addressed (within 1 month)
  - Missing labels/tags
  - Suboptimal configurations

- **🔵 LOW**: Best practices (as time permits)
  - Optimization opportunities

## Available Tools & Scripts

### Main Script
```bash
cd /Users/sebastien.morand/.claude/skills/gcp-project-auditor/scripts
./run.sh <project_id> [output_dir]
```

### Python Script
```bash
python src/audit_project.py <project_id> --output-dir ./audit-results
```

### Key Functions
- `get_project_info()`: Get project details and tags
- `scan_resources()`: Scan all resources
- `scan_iam_policies()`: Scan all IAM policies
- `scan_service_accounts()`: Analyze service accounts
- `scan_firewall_rules()`: Check firewall rules
- `analyze_findings()`: Perform security analysis
- `generate_report()`: Create markdown report

## Reference Files

- **references/excessive-roles.md**: 240+ forbidden roles
- **references/asset-types.md**: All GCP asset types and checks
- **references/audit-guidelines.md**: Detailed methodology

## Response Style

When using this skill:

1. **Start with Context**
   - "Auditing project `<project_id>`..."
   - "Environment detected: `env=pd` (production)"

2. **Show Progress**
   - "Phase 1: Project Discovery ✓"
   - "Phase 2: Resource Inventory (found 47 resources) ✓"
   - "Phase 3: IAM Security Analysis ✓"

3. **Highlight Critical Findings**
   - "🔴 **CRITICAL**: Found 3 security violations"
   - List each critical finding with severity and remediation

4. **Provide Report Location**
   - "Full audit report: `./audit-output/audit-report-<project_id>.md`"
   - "Raw data: `./audit-output/audit-results.json`"

5. **Offer Next Steps**
   - "Immediate actions required:"
   - Prioritized list of remediations

## Error Handling

- **Authentication Errors**: Remind user to authenticate with ADM account
- **Permission Errors**: Check for required roles (viewer, cloudasset.viewer)
- **API Not Enabled**: Some checks require specific APIs
- **Project Not Found**: Verify project ID and access

## Best Practices

1. Always use `sebastien.morand-adm@loreal.com` for audits
2. Save all outputs to files for traceability
3. Timestamp all reports
4. Compare against excessive roles list for pd/np
5. Flag public access as CRITICAL
6. Flag public IPs as CRITICAL
7. Provide actionable recommendations
8. Track findings over time

## Example Invocations

### Basic Audit
```
Audit project oa-data-btdpexploration-np
```

### Quick Security Check
```
Check for critical security issues in project oa-data-btdpprd-pd
```

### Focus on Specific Resource
```
Audit Cloud Run services in project oa-data-btdpexploration-np
```

### Compare Against Policy
```
Check if project oa-data-btdpprd-pd complies with L'Oréal security policies
```

## Integration with Other Skills

This skill can be combined with:
- **gcp-specialist**: For remediation actions (grant/revoke permissions)
- **data-retrieval**: To look up additional context from SDDS/Confluence
- **email-manager**: To send audit reports to stakeholders

## Continuous Improvement

After each audit:
- Note any new security patterns
- Update excessive roles list if needed
- Refine detection logic
- Improve report clarity
- Add new asset type checks

## Compliance & Governance

This skill enforces:
- L'Oréal security policies
- Principle of least privilege
- Defense in depth
- Zero trust architecture
- Data protection regulations
- Network security best practices

## Success Criteria

An audit is successful when:
1. All resources are scanned
2. All IAM policies are analyzed
3. Security violations are identified
4. Report is generated with actionable recommendations
5. Severity levels are correctly assigned
6. User understands next steps

## Output Files

Every audit generates:
1. **audit-report-<project_id>.md**: Human-readable markdown report
2. **audit-results.json**: Complete raw audit data (for automation)
3. **resources.json**: All resources found
4. **iam-policies.json**: All IAM policies

These files enable:
- Tracking findings over time
- Compliance reporting
- Automated remediation
- Trend analysis
- Evidence for audits
