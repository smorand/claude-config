# GCP Projects Security Audit

## Purpose
Perform comprehensive security audit on GCP projects to identify vulnerabilities, excessive permissions, and compliance issues. Produce detailed security report with findings classified by severity.

## Prerequisites
- Admin access to GCP projects (sebastien.morand-adm@loreal.com)
- Access to environment configuration files (np.json, pd.json)
- Required tools: gcloud, checkov, bandit, safety, oadwd, read_pdfs.py
- Audit folder access for external security reports

## Workflow Steps

You must follow this audit protocol completely. Create a Todo list according to these steps:

**Audit Tasks:**
1. Projects Permissions
2. Service Account Permissions
3. Datasets Permissions
4. Storage Permissions
5. Infrastructure Scan
6. Python Code Analysis
7. External Audit
8. Final Review and Report

## Methods

I will give you a list of scans to perform completly to complete the audit.

Severity will be measured with 4 levels:
- critical: Vulnerabilities that generally allow remote control or command execution and are relatively simple to exploit
- major: Vulnerabilities that allow remote control or command execution and are complex to exploit
- medium: Vulnerabilities with limited impact or requiring non-trivial initial conditions for exploitation
- minor: Vulnerabilities with little or no impact unless combined with other, more serious vulnerabilities

## Context

To get the projects to scan will search for np and pd projects. You can find information in environments np.json and pd.json. We don't scan dv or qa environment.

We don't care about the ancestors of the project, we will focus on the projects themselves.

When you get the project id, you will need the project number, you can find it by using the `gcloud` command to describe the project using adm account.

## Steps

**Quick review of todo list**:
1. Projects Permissions
2. Service Account Permissions
3. Datasets Permissions
4. Storage Permissions
5. Infrastructure Scan
6. Python Code analysis
7. External audit
8. Final review and report

### Projects Permissions

#### Task

Search in the IAM policty bindings of the project cloud platform projects for excessive role. Use the `gcloud` command in admin mode to do so.
- The following roles on @loreal.com account are critical vulnerabilities
  - Any permanent role named "Admin"
  - bigquery.dataViewer
  - storage.objectViewer
  - storage.objectUser
  - serviceAccountUser
  - serviceAccountTokenCreator
- The following general findings are a major vulnerability:
  - Any permission on an external service account of the project (a service account of the project must contain the project number or the project id in its name)
  - Any permission on native compute service account: PROJECT_ID@appspot.gserviceaccount.com or PROJECT_NUMBER-compute@developer.gserviceaccount.com
- The following roles are major vulnerabilities:
  - Any permanent role named "Editor" are major vulnerabilities
  - Project Editor role is a major vulnerability
- The following roles are moderate vulnerabilities:
  - Project Viewer role is a moderate vulnerability

Whenever you find groups in the vulnerabilities, list you need to quantify the number of users in the groups with the command: `oadwd groups info --count <group_name>`

#### Exclusion
- btdp-sa-rulemanager-pd@itg-btdpam-gbl-ww-pd.iam.gserviceaccount.com with bigquery.* roles is not a vulnerability.
- cloudbuild service account is excluded (DevOps tool chain)

#### Output

The list of service account classified by severity of vulnerability.

### Service Account Permissions

#### Task

List all service accounts using the `gcloud` command and for each service account, list IAM policy bindings. Any role serviceAccountUser or serviceAccountTokenCreator granted is a major vulnerability

#### Output

The list of service vulnerabilities and their severity: service account having the excessive role, the role granted and the service account target.

### Datasets Permissions

#### Task

List all datasets and for each dataset list the granted roles:
- The following findings are critical vulnerabilities
  - bigquery.dataOwner or bigquery.admin on @loreal.com account
  - bigquery.dataOwner or bigquery.admin on projectOwner, projectEditor or projectViewer
- The folling findings are major vulnerabilities
  - bigquery.dataOwner or bigquery.editor on @loreal.com account
  - bigquery.dataOwner or bigquery.editor on projectOwner, projectEditor or projectViewer
- The folling findings are moderate vulnerabilities
  - bigquery.dataOwner or bigquery.dataViewer on @loreal.com account
  - bigquery.dataOwner or bigquery.dataViewer on projectOwner, projectEditor or projectViewer

#### Output

The list of datasets with vulnerabilities, the severity of the vulnerability and the findings.

### Storage Permissions

#### Task

List all buckets and for each bucket list the granted roles:
- The following findings are critical vulnerabilities
  - storage.admin, storage.folderAdmin, storage.legacyObjectOwner or storage.legacyBucketOwner on @loreal.com account
  - storage.admin, storage.legacyObjectOwner or storage.legacyBucketOwner on projectOwner, projectEditor or projectViewer
- The folling findings are major vulnerabilities
  - storage.objectUser, storage.objectCreator, storage.legacyBucketWriter or storage.legacyBucketOwner on @loreal.com account
  - storage.objectUser, storage.objectCreator, storage.legacyBucketWriter or storage.legacyBucketOwner on projectOwner, projectEditor or projectViewer
- The folling findings are moderate vulnerabilities
  - storage.objectViewer, storage.legacyBucketReader or storage.legacyObjectReader on @loreal.com account
  - storage.objectViewer, storage.legacyBucketReader or storage.legacyObjectReader on projectOwner, projectEditor or projectViewer

#### Output

The list of buckets with vulnerabilities, the severity of the vulnerability and the findings.

### Infrastructure Scan

#### Task

Scan for "iac" folders. Yoy should find them in iac/ or in modules/\*/iac/
For each folder use `checkov -d <folder>` to scan the terraform and classify the alerts by severity.

#### Exclusion

The following checks are exluded:
- CKV_GCP_26
- CKV_GCP_74
- CKV_GCP_78
- CKV_GCP_80
- CKV_GCP_81
- CKV_GCP_83
- CKV_GCP_95
- CKV_GCP_97

#### Output

The list of findings by severity.


### Python Code analysis

#### Task

Search for folder of python source code. You should find them in modules/\*/src/
For each module with security issue, you need to run the following commands in the module folder:
1. a bandit test through: `bandit -r -x '*_test.py' src/`
2. a safetycli test through: `safety scan src/`

=> classify the findings by severity according to the provided definition.

#### Output 

The list of vulnerabilities found by severity.

### External audit

#### Task

Scan the audit folder to get a security findings of an external audit information. Any PDF files found here, must be read using `read_pdfs.py` script.

#### Output

A summary of all the findings in the report.

## Success Criteria
- [ ] Complete permissions audit on all np/pd projects
- [ ] Service account permissions analyzed
- [ ] Dataset permissions reviewed for excessive access
- [ ] Storage bucket permissions audited
- [ ] Infrastructure code scanned with checkov
- [ ] Python code analyzed with bandit and safety
- [ ] External audit reports processed
- [ ] Comprehensive audit.md report created with severity classification
- [ ] Solutions and implementation timelines provided

## Workflow Integration

### Prerequisites Commands
- [ ] **Admin access verification**: Ensure `sebastien.morand-adm@loreal.com` access is active
- [ ] **Environment discovery**: Locate and review `environments/np.json` and `environments/pd.json`
- [ ] **Audit tools availability**: Verify `gcloud`, `checkov`, `bandit`, `safety`, `oadwd`, `read_pdfs.py` are available
- [ ] **Audit scope preparation**: Understand which projects and resources need auditing

### Follow-up Commands
- [ ] **Remediation implementation**: Use `implement/compliance.md` to fix identified code issues
- [ ] **Infrastructure fixes**: Use terraform commands to remediate infrastructure issues
- [ ] **Permission management**: Use appropriate GCP IAM commands to fix permission issues
- [ ] **Documentation updates**: Update security documentation in Confluence via MCP servers

### Alternative Flows
- [ ] **Pre-deployment audit**: Run before `implement/full.md` for security validation
- [ ] **Continuous compliance**: Run periodically for ongoing security monitoring
- [ ] **Incident response**: Use for security incident investigation and analysis
- [ ] **Compliance reporting**: Generate reports for enterprise security teams

### Integration with Development Workflows
- [ ] **Code review integration**: Run after code quality improvements from `implement/compliance.md`
- [ ] **Deployment validation**: Validate security posture before production deployments
- [ ] **Risk assessment**: Identify security risks in new feature implementations
- [ ] **Compliance verification**: Ensure enterprise security policy adherence

## Error Recovery Procedures

### Authentication and Access Issues
| Error | Common Causes | Solutions | Prevention |
|-------|---------------|-----------|------------|
| "Permission denied" on GCP resources | Insufficient admin privileges | Use `reauthent` alias, verify admin account access | Ensure sebastien.morand-adm@loreal.com access is current |
| "Project not found" errors | Wrong project IDs in environment files | Verify project IDs in np.json/pd.json, check project existence | Regular validation of environment configuration |
| "Access token expired" | Authentication timeout | Run `gcloud auth login --account=sebastien.morand-adm@loreal.com` | Use `reauthent` alias for fresh authentication |
| "Quota exceeded" errors | API quota limits hit | Wait for quota reset or use different project for audit tools | Distribute audit calls across time, use multiple projects |

### Tool-Specific Issues
| Tool | Common Problems | Solutions | Workarounds |
|------|-----------------|-----------|-------------|
| **gcloud** | Command not found, wrong configuration | Verify gcloud installation, check active configuration | Use full path to gcloud, verify PATH |
| **checkov** | Module not found, wrong Python environment | `pip install checkov` or use correct Python environment | Use alternative security scanning tools |
| **bandit** | Configuration issues, false positives | Use project-specific .bandit config, document false positives | Focus on high-severity issues only |
| **safety** | Network/proxy issues, database outdated | Configure enterprise network settings, update safety database | Use alternative vulnerability scanning |
| **oadwd** | Group membership command failures | Verify oadwd tool availability and configuration | Use alternative group analysis methods |
| **read_pdfs.py** | PDF processing errors, missing dependencies | Verify script location and dependencies | Manual PDF review if automated processing fails |

### Project Discovery and Analysis Issues
| Issue Type | Common Problems | Detection Methods | Solutions |
|------------|-----------------|------------------|-----------|
| **Missing projects** | Projects not in environment files | Manual project listing, cross-reference with known projects | Update environment configuration files |
| **Inaccessible projects** | Permission issues on specific projects | Individual project access testing | Request access or exclude from audit scope |
| **Project structure changes** | New project patterns not covered | Review project metadata and structure | Update audit methodology for new patterns |
| **Environment-specific issues** | Different configurations between np/pd | Compare environment configurations | Document differences and adjust audit accordingly |

### Data Collection Failures
| Audit Stage | Common Failures | Quick Recovery | Comprehensive Recovery |
|-------------|-----------------|----------------|---------------------|
| **IAM Policy Collection** | API errors, large policy responses | Retry with smaller batches, use pagination | Use alternative collection methods, manual analysis |
| **Service Account Discovery** | Incomplete listings, permission errors | Use different API endpoints, verify permissions | Cross-reference multiple data sources |
| **Dataset Permission Analysis** | BigQuery API limits, complex permissions | Focus on critical datasets first | Batch processing, extended time windows |
| **Storage Bucket Analysis** | Access denied on bucket listing | Skip inaccessible buckets, document exclusions | Request additional permissions, use service accounts |

### Infrastructure Scanning Issues
| Scanning Type | Common Problems | Immediate Solutions | Systematic Solutions |
|---------------|-----------------|-------------------|---------------------|
| **Terraform Code Scanning** | Checkov configuration issues | Use default checkov configuration | Implement enterprise checkov rules |
| **Missing Infrastructure Code** | Code not in expected locations | Search alternative locations, check git history | Document infrastructure code organization |
| **Complex Terraform Modules** | Scanning timeouts, complex dependencies | Focus on critical modules first | Optimize scanning approach, use incremental scans |
| **Version Compatibility** | Tool version mismatches | Use compatible tool versions | Standardize tool versions across environment |

### Python Code Security Analysis Issues
| Analysis Stage | Common Problems | Quick Fixes | Comprehensive Fixes |
|----------------|-----------------|-------------|-------------------|
| **Code Discovery** | Missing source code directories | Search for alternative source locations | Document code organization patterns |
| **Bandit Analysis** | False positives, configuration issues | Use severity filtering, focus on high-risk issues | Implement enterprise bandit configuration |
| **Safety Scanning** | Dependency resolution issues | Focus on production dependencies | Comprehensive dependency audit |
| **Tool Integration** | Multiple tool conflicts | Run tools separately, avoid conflicts | Integrate tools into unified scanning workflow |

### Report Generation and Analysis Issues
| Report Stage | Common Problems | Recovery Methods | Quality Assurance |
|--------------|-----------------|------------------|------------------|
| **Data Aggregation** | Inconsistent data formats | Standardize data processing | Implement data validation |
| **Severity Classification** | Inconsistent severity assignment | Use severity mapping tables | Review and validate severity assignments |
| **Report Formatting** | Markdown formatting issues | Use simple formatting, focus on content | Implement report templates |
| **Recommendation Generation** | Generic recommendations | Focus on specific, actionable recommendations | Validate recommendations with security team |

### Recovery Decision Framework for Security Audits
```
Security Audit Issue Encountered:
├── Authentication/access problem?
│   ├── Yes → Use reauthent, verify admin access
│   └── No → Continue to next check
├── Tool availability issue?
│   ├── Yes → Install missing tools, use alternatives
│   └── No → Continue to next check
├── Data collection failure?
│   ├── Yes → Use alternative collection methods
│   └── No → Continue to next check
├── Analysis/scanning error?
│   ├── Yes → Focus on critical issues first
│   └── No → Continue to next check
└── Report generation problem?
    ├── Yes → Use simplified reporting
    └── No → Escalate to security team
```

### Critical Security Issue Response
| Severity | Response Time | Immediate Actions | Follow-up Actions |
|----------|---------------|------------------|------------------|
| **Critical** | Immediate | Document and report immediately | Coordinate with security team for remediation |
| **Major** | Same day | Document with context and impact | Plan remediation within 24-48 hours |
| **Medium** | Within week | Document and prioritize in remediation plan | Schedule remediation in next sprint |
| **Minor** | Next audit cycle | Document for trend analysis | Include in regular maintenance activities |

### Audit Quality Validation
| Validation Type | Quality Checks | Success Criteria | Escalation Triggers |
|-----------------|----------------|------------------|-------------------|
| **Completeness** | All planned scopes covered | 100% scope coverage or documented exclusions | Missing critical systems or data |
| **Accuracy** | Cross-validation of findings | Consistent results across multiple collection methods | Conflicting or inconsistent findings |
| **Actionability** | Recommendations are specific and implementable | Each finding has clear remediation path | Generic or unactionable recommendations |
| **Compliance** | Audit meets enterprise requirements | Satisfies security team requirements | Audit methodology questions |

## Environment Detection
This command works specifically with L'Oréal GCP infrastructure:

**GCP Security Audit Environment:**
- **Authentication**: Uses `sebastien.morand-adm@loreal.com` for privileged operations
- **Target Projects**: Scans np (non-production) and pd (production) environments only
- **Project Discovery**: Reads from `environments/np.json` and `environments/pd.json` files
- **Security Tools**: 
  - `gcloud` for IAM and resource scanning
  - `checkov` for infrastructure code analysis
  - `bandit` and `safety` for Python code security
  - `oadwd groups info` for group membership analysis
  - `read_pdfs.py` for external audit report processing
- **Output**: Generates comprehensive `audit.md` report with severity classification
- **Scope**: Focus on project-level security, excludes ancestor permissions

## Final Report Creation

With all the findings found, create an exhaustive final report with all the findings in a table classified by severity. Store this report properly in audit.md file. Use tables, style and color to make easy to read. Propose as much as possible solutions and implementation delay.

## Description Template
$ARGUMENTS

## Example Usage
```
$ARGUMENTS: Perform complete security audit on all BTDP production and non-production projects. Focus on IAM permissions, service account usage, BigQuery dataset access, and infrastructure compliance. Include analysis of external audit findings and provide comprehensive remediation recommendations.
```
