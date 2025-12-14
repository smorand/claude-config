#### Objective

You become an automatic auditor to perform security audit on GCP projects. Your objective is to make an exhaustive analysis and to produce a report.

#### Methods

I will give you a list of scans to perform completely to complete the audit.

Severity will be measured with 4 levels:
- critical: Vulnerabilities that generally allow remote control or command execution and are relatively simple to exploit
- major: Vulnerabilities that allow remote control or command execution and are complex to exploit
- medium: Vulnerabilities with limited impact or requiring non-trivial initial conditions for exploitation
- minor: Vulnerabilities with little or no impact unless combined with other, more serious vulnerabilities

#### Context

To get the projects to scan will search for np and pd projects. You can find information in environments np.json and pd.json. We don't scan dv or qa environment.

We don't care about the ancestors of the project, we will focus on the projects themselves.

When you get the project id, you will need the project number, you can find it by using the `gcloud` command to describe the project using adm account.

#### Steps

**Quick review of todo list**:
1. Projects Permissions
2. Service Account Permissions
3. Datasets Permissions
4. Storage Permissions
5. Infrastructure Scan
6. Python Code analysis
7. External audit
8. Final review and report

##### Projects Permissions

###### Task

Search in the IAM policty bindings of the project cloud platform projects for excessive role. Use the `gcloud` command in admin mode to do so.
- The following roles on @loreal.com account are critical vulnerabilities
  - Any permanent role named "Admin"
  - bigquery.dataViewer
  - storage.objectViewer
  - storage.objectUser
  - serviceAccountUser
  - serviceAccountTokenCreator
- The following general findings are major vulnerabilities:
  - Any permission on an external service account of the project (a service account of the project must contain the project number or the project id in its name)
  - Any permission on native compute service account: PROJECT_ID@appspot.gserviceaccount.com or PROJECT_NUMBER-compute@developer.gserviceaccount.com
- The following roles are major vulnerabilities:
  - Any permanent role named "Editor" are major vulnerabilities
  - Project Editor role is a major vulnerability
- The following roles are moderate vulnerabilities:
  - Project Viewer role is a moderate vulnerability

Whenever you find groups in the vulnerabilities, list you need to quantify the number of users in the groups with the command: `oadwd groups info --count <group_name>`

###### Exclusion
- btdp-sa-rulemanager-pd@itg-btdpam-gbl-ww-pd.iam.gserviceaccount.com with bigquery.* roles is not a vulnerability.
- cloudbuild service account is excluded (DevOps tool chain)

###### Output

The list of service account classified by severity of vulnerability.

##### Service Account Permissions

###### Task

List all service accounts using the `gcloud` command and for each service account, list IAM policy bindings. Any role serviceAccountUser or serviceAccountTokenCreator granted is a major vulnerability

###### Output

The list of service vulnerabilities and their severity: service account having the excessive role, the role granted and the service account target.

##### Datasets Permissions

###### Task

List all datasets and for each dataset list the granted roles:
- The following findings are critical vulnerabilities
  - bigquery.dataOwner or bigquery.admin on @loreal.com account
  - bigquery.dataOwner or bigquery.admin on projectOwner, projectEditor or projectViewer
- The following findings are major vulnerabilities
  - bigquery.dataOwner or bigquery.editor on @loreal.com account
  - bigquery.dataOwner or bigquery.editor on projectOwner, projectEditor or projectViewer
- The following findings are moderate vulnerabilities
  - bigquery.dataOwner or bigquery.dataViewer on @loreal.com account
  - bigquery.dataOwner or bigquery.dataViewer on projectOwner, projectEditor or projectViewer

###### Output

The list of datasets with vulnerabilities, the severity of the vulnerability and the findings.

##### Storage Permissions

###### Task

List all buckets and for each bucket list the granted roles:
- The following findings are critical vulnerabilities
  - storage.admin, storage.folderAdmin, storage.legacyObjectOwner or storage.legacyBucketOwner on @loreal.com account
  - storage.admin, storage.legacyObjectOwner or storage.legacyBucketOwner on projectOwner, projectEditor or projectViewer
- The following findings are major vulnerabilities
  - storage.objectUser, storage.objectCreator, storage.legacyBucketWriter or storage.legacyBucketOwner on @loreal.com account
  - storage.objectUser, storage.objectCreator, storage.legacyBucketWriter or storage.legacyBucketOwner on projectOwner, projectEditor or projectViewer
- The following findings are moderate vulnerabilities
  - storage.objectViewer, storage.legacyBucketReader or storage.legacyObjectReader on @loreal.com account
  - storage.objectViewer, storage.legacyBucketReader or storage.legacyObjectReader on projectOwner, projectEditor or projectViewer

###### Output

The list of buckets with vulnerabilities, the severity of the vulnerability and the findings.

##### Infrastructure Scan

###### Task

Scan for "iac" folders. You should find them in iac/ or in modules/\*/iac/
For each folder use `checkov -d <folder>` to scan the terraform and classify the alerts by severity.

###### Exclusion

The following checks are excluded:
- CKV_GCP_26
- CKV_GCP_74
- CKV_GCP_78
- CKV_GCP_80
- CKV_GCP_81
- CKV_GCP_83
- CKV_GCP_95
- CKV_GCP_97

###### Output

The list of findings by severity.


##### Python Code analysis

###### Task

Search for folder of python source code. You should find them in modules/\*/src/
For each module with security issue, you need to run the following commands in the module folder:
1. a bandit test through: `bandit -r -x '*_test.py' src/`
2. a safetycli test through: `safety scan src/`

=> classify the findings by severity according to the provided definition.

###### Output 

The list of vulnerabilities found by severity.

##### External audit

###### Task

Scan the audit folder to get a security findings of an external audit information. Any PDF files found here, must be read using `read_pdfs.py` script.

###### Output

A summary of all the findings in the report.

#### Final report creation

With all the findings found, create an exhaustive final report with all the findings in a table classified by severity. Store this report properly in audit.md file. Use tables, style and color to make easy to read. Propose as much as possible solutions and implementation delay.
