# GCP Project Audit Guidelines

This document provides guidelines and best practices for conducting comprehensive GCP project audits.

## Audit Objectives

A thorough GCP project audit should achieve the following objectives:

1. **Security Compliance**: Ensure the project follows security best practices
2. **Access Control**: Verify that permissions follow the principle of least privilege
3. **Resource Inventory**: Document all resources in the project
4. **Cost Optimization**: Identify unused or underutilized resources
5. **Compliance**: Check against L'Oréal policies and industry standards
6. **Risk Assessment**: Identify security risks and vulnerabilities

## Pre-Audit Checklist

Before starting an audit:

- [ ] Confirm project ID
- [ ] Verify access with sebastien.morand-adm@loreal.com account
- [ ] Check gcloud authentication: `gcloud auth list`
- [ ] Ensure gcloud is up-to-date: `gcloud components update`
- [ ] Identify project environment (pd/np/qa/dv)
- [ ] Prepare output directory for audit results

## Audit Phases

### Phase 1: Project Discovery (15 mins)

**Objective**: Understand project context and hierarchy

**Tasks:**
1. Get project details and metadata
2. Identify parent folder/organization
3. Extract project tags and labels
4. Determine environment (pd/np/qa/dv)
5. Get project ancestry for inherited permissions

**Commands:**
```bash
# Project details
gcloud --account sebastien.morand-adm@loreal.com projects describe <PROJECT_ID> --format=json

# Project ancestry
gcloud --account sebastien.morand-adm@loreal.com projects get-ancestors <PROJECT_ID> --format=json

# Project IAM policy
gcloud --account sebastien.morand-adm@loreal.com projects get-iam-policy <PROJECT_ID> --format=json
```

**Key Questions:**
- What is the purpose of this project?
- What environment is it (production, non-production)?
- Who are the project owners?
- What folder/organization does it belong to?

### Phase 2: Resource Inventory (30 mins)

**Objective**: Create complete inventory of all GCP resources

**Tasks:**
1. Scan all resources using Cloud Asset Inventory
2. Categorize resources by type
3. Identify critical resources (databases, compute, storage)
4. Check resource configurations
5. Document resource counts

**Commands:**
```bash
# Get all resources
gcloud --account sebastien.morand-adm@loreal.com asset search-all-resources \
  --scope=projects/<PROJECT_ID> \
  --format=json > audit-resources.json

# Filter by specific types (example: BigQuery)
gcloud --account sebastien.morand-adm@loreal.com asset search-all-resources \
  --scope=projects/<PROJECT_ID> \
  --asset-types=bigquery.googleapis.com/Dataset,bigquery.googleapis.com/Table \
  --format=json
```

**Focus Areas:**
- Data resources (BigQuery, Cloud SQL, Cloud Storage)
- Compute resources (Cloud Run, Cloud Functions, VMs)
- Networking (VPC, firewall rules, load balancers)
- IAM resources (service accounts)

### Phase 3: IAM Security Analysis (45 mins)

**Objective**: Analyze all IAM policies and identify security issues

**Tasks:**
1. Scan all IAM policies using Cloud Asset Inventory
2. Get project-level IAM policy
3. Analyze service account impersonation
4. Check for excessive roles (especially in pd/np)
5. Identify external users
6. Check for public access

**Commands:**
```bash
# Get all IAM policies
gcloud --account sebastien.morand-adm@loreal.com asset search-all-iam-policies \
  --scope=projects/<PROJECT_ID> \
  --format=json > audit-iam-policies.json

# Get project IAM policy
gcloud --account sebastien.morand-adm@loreal.com projects get-iam-policy <PROJECT_ID> --format=json

# List service accounts
gcloud --account sebastien.morand-adm@loreal.com iam service-accounts list --project <PROJECT_ID> --format=json

# For each service account, check who can impersonate
gcloud --account sebastien.morand-adm@loreal.com iam service-accounts get-iam-policy <SA_EMAIL> --format=json
```

**Critical Checks:**
- **Excessive Roles**: Check against excessive-roles.md list for pd/np environments
- **Public Access**: Look for `allUsers` or `allAuthenticatedUsers`
- **External Users**: Identify non-@loreal.com users
- **Service Account Keys**: Check for user-managed keys (security risk)
- **Impersonation**: Who can impersonate service accounts
- **Owner/Editor Roles**: These should be limited in production

### Phase 4: Network Security Review (30 mins)

**Objective**: Assess network security posture

**Tasks:**
1. Review firewall rules
2. Check for overly permissive rules (0.0.0.0/0)
3. Analyze VPC configuration
4. Check for public IPs on resources
5. Review load balancer configuration

**Commands:**
```bash
# List firewall rules
gcloud --account sebastien.morand-adm@loreal.com compute firewall-rules list --project <PROJECT_ID> --format=json

# List VPCs
gcloud --account sebastien.morand-adm@loreal.com compute networks list --project <PROJECT_ID> --format=json

# List subnets
gcloud --account sebastien.morand-adm@loreal.com compute networks subnets list --project <PROJECT_ID> --format=json
```

**Red Flags:**
- Firewall rule with source `0.0.0.0/0` and ports `22`, `3389`, `3306`, `5432`
- Compute instances with external IPs in production
- Cloud SQL with public IP enabled
- Overly broad ingress rules

### Phase 5: Resource-Specific Audits (30 mins)

**Objective**: Deep dive into specific resource types

#### BigQuery
```bash
# List datasets
gcloud --account sebastien.morand-adm@loreal.com alpha bq datasets list --project <PROJECT_ID>

# For each dataset, check IAM
gcloud --account sebastien.morand-adm@loreal.com alpha bq datasets get-iam-policy <DATASET> --project <PROJECT_ID>
```

**Check for:**
- Public datasets
- Authorized views
- Encryption settings

#### Cloud Run
```bash
# List services
gcloud --account sebastien.morand-adm@loreal.com run services list --project <PROJECT_ID> --region europe-west1

# For each service, check config
gcloud --account sebastien.morand-adm@loreal.com run services describe <SERVICE> --project <PROJECT_ID> --region europe-west1
```

**Check for:**
- Unauthenticated access
- Ingress settings
- Service account permissions

#### Cloud Storage
```bash
# List buckets
gcloud --account sebastien.morand-adm@loreal.com storage buckets list --project <PROJECT_ID>

# For each bucket, check IAM
gcloud --account sebastien.morand-adm@loreal.com storage buckets get-iam-policy gs://<BUCKET>
```

**Check for:**
- Public buckets
- Uniform bucket-level access
- Encryption settings

### Phase 6: Compliance Checks (15 mins)

**Objective**: Verify compliance with L'Oréal policies

**L'Oréal Specific Checks:**

1. **Environment Segregation**
   - Production (pd) and non-production (np) are properly separated
   - No excessive roles in pd/np environments
   - Proper tagging (env=pd, env=np)

2. **Service Account Best Practices**
   - No user-managed service account keys
   - Service accounts use Workload Identity where possible
   - Service accounts have minimal permissions

3. **Data Protection**
   - BigQuery datasets are not public
   - Cloud Storage buckets are not public
   - Encryption is enabled (Google-managed or CMEK)

4. **Network Security**
   - No overly permissive firewall rules
   - Private Google Access enabled on subnets
   - VPC Flow Logs enabled

5. **Logging & Monitoring**
   - Audit logs are enabled
   - Log sinks are configured
   - Admin activity logs are retained

### Phase 7: Report Generation (30 mins)

**Objective**: Create comprehensive audit report

**Report Sections:**
1. Executive Summary
2. Project Overview
3. Resource Inventory (by type)
4. IAM Security Analysis
5. Network Security Review
6. Compliance Status
7. Findings & Recommendations (by severity)
8. Appendices (detailed data)

**Severity Levels:**
- **CRITICAL**: Immediate action required (e.g., public database, owner role in production)
- **HIGH**: Should be addressed urgently (e.g., overly permissive firewall rule)
- **MEDIUM**: Should be addressed soon (e.g., missing encryption)
- **LOW**: Nice to have (e.g., missing labels)
- **INFO**: Informational (e.g., resource counts)

## Environment-Specific Guidelines

### Production (env=pd)

**Strictest Controls:**
- ❌ No owner/editor roles for users
- ❌ No excessive roles (see excessive-roles.md)
- ❌ No public access to resources
- ❌ No external IPs on compute instances
- ❌ No user-managed service account keys
- ✅ Must have encryption enabled
- ✅ Must have audit logging enabled
- ✅ Must have proper tagging

### Non-Production (env=np)

**Strict Controls:**
- ❌ No excessive roles (see excessive-roles.md)
- ⚠️ Owner/editor roles should be limited
- ⚠️ Public access should be justified
- ✅ Should have encryption enabled
- ✅ Should have audit logging enabled
- ✅ Should have proper tagging

### QA (env=qa) and Development (env=dv)

**Relaxed Controls:**
- ⚠️ Excessive roles should be reviewed
- ⚠️ Public access should be documented
- ✅ Should follow basic security practices

## Common Security Issues

### Critical Issues

1. **Public Datasets/Buckets**
   - Finding: Resource allows access by `allUsers` or `allAuthenticatedUsers`
   - Impact: Data exposure, data breach risk
   - Remediation: Remove public access, grant specific permissions

2. **Excessive Roles in Production**
   - Finding: User has roles/owner, roles/editor, or other excessive role in pd/np project
   - Impact: Over-privileged access, compliance violation
   - Remediation: Remove excessive role, grant minimal permissions

3. **Overly Permissive Firewall Rules**
   - Finding: Firewall rule allows 0.0.0.0/0 on sensitive ports (22, 3389, 3306, 5432)
   - Impact: Unauthorized access, potential breach
   - Remediation: Restrict source IP ranges, use Identity-Aware Proxy

4. **Service Account Key Exposure**
   - Finding: User-managed service account keys exist
   - Impact: Key theft, unauthorized access
   - Remediation: Delete keys, use Workload Identity or short-lived tokens

### High Issues

1. **Cloud SQL Public IP**
   - Finding: Cloud SQL instance has public IP enabled
   - Impact: Database exposure to internet
   - Remediation: Disable public IP, use Private IP or Cloud SQL Auth Proxy

2. **Unauthenticated Cloud Run Service**
   - Finding: Cloud Run service allows unauthenticated invocations
   - Impact: Unauthorized access, potential abuse
   - Remediation: Enable authentication, use IAP if needed

3. **External IPs on Compute Instances**
   - Finding: Compute instances in production have external IPs
   - Impact: Increased attack surface
   - Remediation: Remove external IPs, use Cloud NAT or IAP

### Medium Issues

1. **Missing Encryption**
   - Finding: Resource does not have encryption enabled
   - Impact: Data protection concern
   - Remediation: Enable Google-managed or customer-managed encryption

2. **Missing Labels/Tags**
   - Finding: Resources missing env, owner, or cost-center labels
   - Impact: Difficult to track ownership and costs
   - Remediation: Add proper labels to all resources

3. **Old Service Account Keys**
   - Finding: Service account keys older than 90 days
   - Impact: Increased risk if keys are compromised
   - Remediation: Rotate keys or migrate to Workload Identity

## Best Practices

### During Audit

1. **Document Everything**: Save all command outputs to files
2. **Take Screenshots**: Capture critical findings in console
3. **Timestamp**: Record when the audit was conducted
4. **Version Control**: Save audit reports in git with timestamps
5. **Follow-up**: Schedule follow-up to verify remediations

### After Audit

1. **Share Report**: Distribute to project owners and security team
2. **Track Remediation**: Create tickets for each finding
3. **Set Deadlines**: Critical issues should be fixed within 24-48 hours
4. **Re-audit**: Conduct follow-up audit after remediation
5. **Update Policies**: If new issues found, update security policies

### Automation

Consider automating audits:
- Schedule regular audits (monthly for production projects)
- Use Cloud Asset Inventory export to BigQuery
- Create dashboards for real-time compliance monitoring
- Set up alerts for policy violations

## Report Template

Use this structure for audit reports:

```markdown
# GCP Project Audit Report: <PROJECT_ID>

**Audit Date**: YYYY-MM-DD HH:MM UTC
**Auditor**: sebastien.morand@loreal.com
**Project Environment**: pd/np/qa/dv
**Audit Version**: 1.0

---

## Executive Summary

- **Total Resources**: X
- **Critical Findings**: X
- **High Findings**: X
- **Medium Findings**: X
- **Compliance Status**: ✓ PASS / ✗ FAIL

**Overall Risk Level**: CRITICAL / HIGH / MEDIUM / LOW

---

## 1. Project Overview
[Details about the project]

## 2. Resource Inventory
[Breakdown by resource type]

## 3. IAM Security Analysis
[Permissions analysis]

## 4. Network Security Review
[Firewall and VPC analysis]

## 5. Findings & Recommendations

### Critical Findings (Immediate Action Required)
1. [Finding 1]
2. [Finding 2]

### High Findings (Urgent)
1. [Finding 1]

### Medium Findings
1. [Finding 1]

### Low Findings
1. [Finding 1]

## 6. Compliance Status
- [ ] No excessive roles in production
- [ ] No public resources
- [ ] Encryption enabled
- [ ] Audit logging enabled
- [ ] Proper network segmentation

## 7. Next Steps
1. [Action 1]
2. [Action 2]

---

## Appendices

### Appendix A: Full Resource List
[JSON or table]

### Appendix B: Full IAM Policy
[JSON]

### Appendix C: Command History
[All commands executed]
```

## Tools & Scripts

Use the following scripts from the `scripts/` directory:

1. **audit_project.py** - Main audit orchestration script
2. **scan_resources.py** - Resource scanning
3. **scan_iam.py** - IAM policy scanning
4. **generate_report.py** - Report generation
5. **check_compliance.py** - Compliance checking

## References

- [GCP Security Best Practices](https://cloud.google.com/security/best-practices)
- [CIS Google Cloud Platform Foundation Benchmark](https://www.cisecurity.org/benchmark/google_cloud_computing_platform)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- L'Oréal Security Policies (internal)

## Continuous Improvement

After each audit:
1. Review what went well and what could be improved
2. Update this guide with new learnings
3. Add new asset types or checks as needed
4. Share best practices with the team
