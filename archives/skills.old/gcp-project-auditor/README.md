# GCP Project Auditor

Comprehensive security and compliance auditing tool for Google Cloud Platform projects.

## Overview

The GCP Project Auditor skill enables thorough security audits of GCP projects, scanning for compliance violations, security issues, and best practice violations. It's specifically designed to enforce L'Oréal's security policies, particularly around production and non-production environments.

## Features

- **Complete Resource Inventory**: Scans all resources using GCP Cloud Asset Inventory
- **IAM Security Analysis**: Analyzes all IAM policies and identifies excessive permissions
- **Environment-Aware**: Enforces strict security policies for production (pd) and non-production (np) environments
- **Excessive Role Detection**: Flags prohibited roles based on L'Oréal's security standards
- **Network Security Review**: Checks firewall rules for overly permissive configurations
- **Service Account Analysis**: Identifies service account impersonation risks and user-managed keys
- **Comprehensive Reporting**: Generates detailed markdown audit reports with severity levels

## Asset Types Audited

### Data & Analytics
- BigQuery datasets and tables
- Dataflow, Dataproc, Composer, Workflows

### Compute & Applications
- Cloud Run services
- Cloud Functions
- App Engine
- Compute Engine instances
- GKE clusters

### Databases
- Cloud SQL
- AlloyDB
- Spanner
- Bigtable
- Firestore

### Storage & Networking
- Cloud Storage buckets
- VPC networks and subnets
- Firewall rules
- Load balancers

### IAM
- Service accounts
- Service account keys
- IAM policies at all levels

## Quick Start

### Using the Skill

Simply invoke the skill and ask to audit a GCP project:

```
Audit the project oa-data-btdpexploration-np
```

### Using the Script Directly

```bash
cd scripts
./run.sh <project_id> [output_dir]
```

Example:
```bash
./run.sh oa-data-btdpexploration-np ./audit-results
```

## Requirements

- Python 3.11+
- `gcloud` CLI installed and authenticated
- Access to sebastien.morand-adm@loreal.com account
- Appropriate permissions to read project resources and IAM policies

## Output

The audit generates:

1. **Markdown Report**: `audit-report-<project_id>.md`
   - Executive summary
   - Resource inventory
   - IAM analysis
   - Security findings (by severity)
   - Recommendations

2. **JSON Data**:
   - `audit-results.json` - Complete raw audit data
   - `resources.json` - All resources
   - `iam-policies.json` - All IAM policies

## Security Checks

### Critical Checks
- ✅ No excessive roles in production/non-production environments
- ✅ No public access to datasets, buckets, or databases
- ✅ No public Cloud Run services or Cloud Functions (unauthenticated access)
- ✅ No public IP addresses on databases (Cloud SQL, AlloyDB)
- ✅ No external IP addresses on Compute instances (especially in production)
- ✅ No overly permissive firewall rules (0.0.0.0/0 to sensitive ports)
- ✅ No user-managed service account keys

### Environment-Specific Policies

**Production (env=pd) and Non-Production (env=np):**
- Excessive roles (owner, editor, *admin, serviceAgent) are flagged as CRITICAL
- Users should have minimal, time-limited permissions
- Public access is prohibited
- Service accounts should use Workload Identity

**QA (env=qa) and Development (env=dv):**
- Relaxed policies but still reviewed
- Excessive roles are flagged as warnings

## Excessive Roles

The following roles are considered excessive in pd/np environments:

- `roles/owner`, `roles/editor`
- `roles/iam.securityAdmin`, `roles/iam.organizationRoleAdmin`
- `roles/compute.admin`, `roles/bigquery.admin`, `roles/storage.admin`
- All service agent roles when granted to users
- 200+ additional roles (see `references/excessive-roles.md`)

## Report Structure

```markdown
# GCP Project Audit Report: <project_id>

## Executive Summary
- Total Resources
- Critical/High/Medium Findings
- Overall Risk Level

## 1. Project Overview
- Project details, environment, tags

## 2. Resource Inventory
- Resources by type with counts

## 3. IAM Security Analysis
- Project-level permissions
- Excessive role assignments
- Service account impersonation risks

## 4. Security Findings
- Critical (immediate action)
- High (urgent)
- Medium (should fix)
- Low (nice to have)

## 5. Recommendations
- Immediate actions
- General best practices

## Appendix
- Full audit data references
```

## Severity Levels

- **🔴 CRITICAL**: Immediate action required (e.g., excessive roles in production, public databases)
- **🟠 HIGH**: Urgent attention needed (e.g., user-managed SA keys, permissive firewall rules)
- **🟡 MEDIUM**: Should be addressed (e.g., missing encryption, missing labels)
- **🔵 LOW**: Best practices (e.g., optimization opportunities)
- **ℹ️ INFO**: Informational (e.g., resource counts)

## Workflow

1. **Invoke Skill**: Ask Claude to audit a project
2. **Project Discovery**: Get project details and environment tag
3. **Resource Scan**: Scan all resources using `gcloud asset search-all-resources`
4. **IAM Scan**: Scan all IAM policies using `gcloud asset search-all-iam-policies`
5. **Service Account Analysis**: Check service accounts and impersonation
6. **Network Review**: Check firewall rules and VPC configuration
7. **Analysis**: Compare against security policies and best practices
8. **Report Generation**: Create comprehensive markdown report

## Reference Files

- **excessive-roles.md**: Complete list of 200+ excessive roles
- **asset-types.md**: All GCP asset types and what to check
- **audit-guidelines.md**: Detailed audit methodology and best practices

## Example Usage

### Audit a Production Project

```
Audit the production project oa-data-btdpprd-pd and check for security violations
```

This will:
1. Scan all resources in the project
2. Check for excessive roles (stricter rules for pd environment)
3. Flag any security violations
4. Generate a detailed report with recommendations

### Quick Security Check

```
Check if project oa-data-btdpexploration-np has any critical security issues
```

This will focus on critical checks:
- Excessive roles
- Public access
- Permissive firewall rules

## Common Findings

### Critical Issues
1. **Excessive Roles in Production**: Users with owner/editor roles in pd/np projects
2. **Public Datasets**: BigQuery datasets accessible by allUsers
3. **Public Buckets**: Cloud Storage buckets with public access
4. **Public Cloud Run/Functions**: Services allowing unauthenticated access (allUsers)
5. **Public IP on Databases**: Cloud SQL or AlloyDB with public IP enabled
6. **External IP on Compute**: Compute instances with external IP addresses
7. **Open Firewall**: Rules allowing 0.0.0.0/0 to SSH (22) or databases (3306, 5432)

### High Issues
1. **Service Account Keys**: User-managed keys (security risk)
2. **Overly Permissive Firewall Rules**: Broad source ranges on sensitive ports

## Remediation

After receiving an audit report:

1. **Critical Findings**: Address immediately (within 24-48 hours)
2. **High Findings**: Address urgently (within 1 week)
3. **Medium Findings**: Plan remediation (within 1 month)
4. **Low Findings**: Include in regular maintenance

## Best Practices

- Run audits monthly for production projects
- Run audits after major changes
- Track findings over time
- Automate remediation where possible
- Update security policies based on findings

## Troubleshooting

### Authentication Issues
```bash
# Re-authenticate with admin account
gcloud auth login sebastien.morand-adm@loreal.com
gcloud config set account sebastien.morand-adm@loreal.com
```

### Permission Errors
Ensure you have the following roles:
- `roles/viewer` (at minimum)
- `roles/cloudasset.viewer` (for asset inventory)
- `roles/iam.securityReviewer` (for IAM analysis)

### API Not Enabled
Some checks require specific APIs:
- Cloud Asset API
- Compute Engine API (for firewall rules)
- IAM API

## Support

For issues or questions:
- **Author**: Sebastien MORAND
- **Email**: sebastien.morand@loreal.com
- **Role**: CTO Data & AI, L'Oréal BTDP

## License

Internal L'Oréal tool - Not for external distribution
