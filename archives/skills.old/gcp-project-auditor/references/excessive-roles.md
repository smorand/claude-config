# Excessive Roles - Security Violation List

This document lists all roles that are considered **EXCESSIVE** and should NOT be granted to users in **production (pd)** and **non-production (np)** environments at L'Oréal.

These roles grant too much access and violate security best practices. They should be flagged as **CRITICAL** security violations during audits.

## Context

- **Environment Tags**: Projects are tagged with `env=pd` (production), `env=np` (non-production), `env=qa` (QA), or `env=dv` (development)
- **Scope**: This list applies to **pd** and **np** environments only
- **Exceptions**: Service Agent roles are acceptable for service accounts but NOT for user accounts

## Excessive Roles List

### Data & Analytics - Service Agents
```
roles/dataflow.serviceAgent
roles/dataplex.serviceAgent
roles/datafusion.serviceAgent
roles/dataproc.serviceAgent
roles/datapipelines.serviceAgent
roles/dataprep.serviceAgent
roles/dataprocessing.admin
roles/datastream.serviceAgent
```

### IAM & Security - Administrative Roles
```
roles/iam.databasesAdmin
roles/iam.infrastructureAdmin
roles/iam.mlEngineer
roles/iam.dataScientist
roles/iam.securityAdmin
roles/iam.devOps
roles/iam.securityAuditor
roles/iam.securityReviewer
roles/iam.supportUser
roles/iam.principalAccessBoundaryAdmin
roles/iam.serviceAccountTokenCreator
roles/iam.networkAdmin
roles/iam.denyAdmin
roles/iam.principalAccessBoundaryUser
roles/iam.workloadIdentityUser
roles/iam.organizationRoleAdmin
roles/iam.organizationRoleViewer
roles/iam.serviceAccountOpenIdTokenCreator
```

### Storage - Administrative Roles
```
roles/storage.admin
roles/storage.legacyBucketOwner
roles/storage.folderAdmin
roles/storage.objectAdmin
roles/storage.objectUser
roles/storage.expressModeUserAccess
roles/storage.legacyBucketWriter
roles/storage.legacyObjectOwner
roles/storage.objectCreator
roles/storage.expressModeServiceInput
roles/storage.expressModeServiceOutput
roles/storage.legacyBucketReader
```

### Billing - All Roles
```
roles/billing.admin
roles/billing.viewer
roles/billing.costsManager
roles/billing.carbonViewer
roles/billing.user
roles/billing.creator
roles/billing.projectCostsManager
```

### Compute - Administrative Roles
```
roles/compute.admin
roles/compute.xpnAdmin
roles/compute.serviceAgent
```

### BigQuery - Administrative Roles
```
roles/bigquery.admin
roles/bigquery.studioAdmin
roles/bigquery.dataOwner
roles/bigquery.dataEditor
roles/bigquery.securityAdmin
roles/bigquery.connectedSheetsServiceAgent
```

### Firebase - All Roles
```
roles/firebase.admin
roles/firebase.developAdmin
roles/firebase.sdkAdminServiceAgent
roles/firebase.developViewer
roles/firebase.viewer
roles/firebase.managementServiceAgent
roles/firebaseapphosting.computeRunner
roles/firebaseappcheck.admin
roles/firebaseappcheck.tokenVerifier
roles/firebasecrashlytics.serviceAgent
roles/firebaserules.system
roles/firebasestorage.serviceAgent
```

### Resource Management - Administrative Roles
```
roles/resourcemanager.folderAdmin
roles/resourcemanager.folderEditor
roles/resourcemanager.organizationAdmin
roles/resourcemanager.folderIamAdmin
roles/resourcemanager.folderCreator
roles/resourcemanager.folderMover
roles/resourcemanager.projectCreator
```

### Service Agents (All Product Service Agents)
```
roles/dlp.serviceAgent
roles/ml.serviceAgent
roles/composer.serviceAgent
roles/visualinspection.serviceAgent
roles/clouddeploymentmanager.serviceAgent
roles/aiplatform.extensionCustomCodeServiceAgent
roles/composer.worker
roles/composer.environmentAndStorageObjectAdmin
roles/dataproc.worker
roles/discoveryengine.serviceAgent
roles/aiplatform.customCodeServiceAgent
roles/aiplatform.tuningServiceAgent
roles/appengineflex.serviceAgent
roles/aiplatform.serviceAgent
roles/aiplatform.batchPredictionServiceAgent
roles/aiplatform.modelMonitoringServiceAgent
roles/cloudasset.serviceAgent
roles/automl.serviceAgent
roles/automlrecommendations.serviceAgent
roles/ces.serviceAgent
roles/cloudbuild.serviceAgent
roles/cloudfunctions.serviceAgent
roles/retail.serviceAgent
roles/visionai.serviceAgent
roles/cloudconfig.serviceAgent
roles/contactcenterinsights.serviceAgent
roles/integrations.serviceAgent
roles/pubsub.serviceAgent
roles/cloudsecuritycompliance.serviceAgent
roles/config.agent
roles/container.serviceAgent
roles/datalabeling.serviceAgent
roles/dialogflow.serviceAgent
roles/edgecontainer.clusterServiceAgent
roles/metastore.serviceAgent
roles/privilegedaccessmanager.serviceAgent
roles/saasservicemgmt.serviceAgent
roles/aiplatform.ragServiceAgent
roles/appengine.serviceAgent
roles/auditmanager.serviceAgent
roles/chronicle.soarServiceAgent
roles/cloudoptimization.serviceAgent
roles/connectors.serviceAgent
roles/contentwarehouse.serviceAgent
roles/documentaicore.serviceAgent
roles/enterpriseknowledgegraph.serviceAgent
roles/eventarc.serviceAgent
roles/livestream.serviceAgent
roles/run.serviceAgent
roles/serverless.serviceAgent
roles/aiedgeportal.serviceAgent
roles/aiplatform.extensionServiceAgent
roles/apigateway.serviceAgent
roles/apigee.serviceAgent
roles/cloudscheduler.serviceAgent
roles/cloudtasks.serviceAgent
roles/dspm.serviceAgent
roles/firestore.serviceAgent
roles/mediaasset.serviceAgent
roles/privilegedaccessmanager.folderServiceAgent
roles/privilegedaccessmanager.organizationServiceAgent
roles/routeoptimization.serviceAgent
roles/runapps.serviceAgent
roles/spanner.serviceAgent
roles/spectrumsas.serviceAgent
roles/speech.serviceAgent
roles/transcoder.serviceAgent
roles/workflows.serviceAgent
roles/bigquerycontinuousquery.serviceAgent
roles/bigquerydatatransfer.serviceAgent
roles/bigquerymigration.worker
roles/bigqueryomni.serviceAgent
roles/bigqueryspark.serviceAgent
roles/cloudbuild.loggingServiceAgent
roles/clouddeploy.serviceAgent
roles/cloudtranslate.serviceAgent
roles/containerregistry.ServiceAgent
roles/krmapihosting.anthosApiEndpointServiceAgent
roles/krmapihosting.serviceAgent
roles/kuberun.eventsControlPlaneServiceAgent
roles/looker.serviceAgent
roles/meshcontrolplane.serviceAgent
roles/monitoring.notificationServiceAgent
roles/notebooks.serviceAgent
roles/riskmanager.serviceAgent
roles/securesourcemanager.serviceAgent
roles/securitycenter.controlServiceAgent
roles/securitycenter.securityResponseServiceAgent
roles/securitycenter.serviceAgent
roles/sourcerepo.serviceAgent
roles/stream.serviceAgent
roles/vectorsearch.serviceAgent
roles/vpcaccess.serviceAgent
```

### Design & Testing
```
roles/designcenter.admin
roles/designcenter.user
roles/designcenter.serviceAgent
roles/cloudtestservice.testAdmin
```

### Organization Policy & Security
```
roles/orgpolicy.policyAdmin
roles/securityposture.admin
roles/securityposture.postureDeployer
```

### Container & Kubernetes
```
roles/container.admin
roles/container.hostServiceAgentUser
```

### Cloud Run & Serverless
```
roles/run.sourceDeveloper
roles/clouddeploy.jobRunner
```

### Data Processing & Analytics
```
roles/dataflow.admin
roles/dataflow.worker
roles/datacatalog.admin
roles/datacatalog.categoryFineGrainedReader
roles/datacatalog.tagEditor
roles/dataplex.storageDataOwner
roles/dataplex.storageDataWriter
roles/datastream.bigqueryWriter
```

### Security & Compliance
```
roles/securitycenter.admin
roles/securitycenter.adminEditor
roles/securitycenter.adminViewer
roles/securitycenter.assetsViewer
roles/resourcesettings.admin
roles/privilegedaccessmanager.settingsAdmin
```

### Consumer & Procurement
```
roles/consumerprocurement.orderAdmin
roles/consumerprocurement.procurementAdmin
roles/consumerprocurement.orderViewer
roles/consumerprocurement.procurementViewer
```

### Notebooks & AI Platform
```
roles/notebooks.legacyAdmin
roles/axt.admin
roles/cloudaicompanion.topicAdmin
```

### Assured Workloads
```
roles/assuredworkloads.admin
roles/assuredworkloads.editor
```

### Chronicle & SOAR
```
roles/chronicle.serviceAgent
roles/chronicle.soarAdmin
roles/chronicle.soarThreatManager
roles/chronicle.soarVulnerabilityManager
```

### Cloud Support
```
roles/cloudsupport.techSupportEditor
```

### Logging & Monitoring
```
roles/logging.bucketWriter
```

### Remote Build Execution
```
roles/remotebuildexecution.actionCacheWriter
```

### Cloud Migration
```
roles/cloudmigration.storageaccess
roles/cloudmigration.inframanager
```

### Service Directory
```
roles/servicedirectory.pscAuthorizedService
```

### Workstations
```
roles/workstations.user
```

### BigQuery Data Policies
```
roles/bigquerydatapolicy.maskedReader
roles/bigquerydatapolicy.rawDataReader
```

### Recommender
```
roles/recommender.bigQueryCapacityCommitmentsBillingAccountAdmin
roles/recommender.bigQueryCapacityCommitmentsBillingAccountViewer
roles/recommender.billingAccountCudAdmin
roles/recommender.billingAccountCudViewer
roles/recommender.ucsAdmin
roles/recommender.ucsViewer
```

### Beyond Corp
```
roles/beyondcorp.clientConnectorServiceUser
```

### Backup & DR
```
roles/backupdr.cloudStorageOperator
```

### BigQuery Filtered Data
```
roles/bigquery.filteredDataViewer
```

### Secured Landing Zone
```
roles/securedlandingzone.bqdwProjectRemediator
```

### Cloud Build
```
roles/cloudbuild.builds.builder
```

### Custom L'Oréal Roles
```
organizations/1090299993982/roles/prismaCloudViewerlufxl
organizations/1090299993982/roles/custom_oa_billing_viewer
organizations/1090299993982/roles/custom_iam_updater
organizations/1090299993982/roles/CustomRole271
organizations/1090299993982/roles/custom_iam_viewer
organizations/1090299993982/roles/HyperGlanceTests
organizations/1090299993982/roles/custom.oa.datatx.objectUser
organizations/1090299993982/roles/custom_oa_storage_iamupdate
organizations/1090299993982/roles/prismaCloudViewerdrqty
organizations/1090299993982/roles/prismaCloudViewerqxmjn
organizations/1090299993982/roles/CustomRole232
organizations/1090299993982/roles/acl_viewer
organizations/1090299993982/roles/custom_bq_reservation_assignment_admin
organizations/1090299993982/roles/orca_security_side_scanner_role
```

## Detection Logic

When auditing a GCP project:

1. **Check Environment Tag**: Get project tags and identify if `env=pd` or `env=np`
2. **If pd or np**: Scan all IAM policies for the roles listed above
3. **Flag Violations**: Any **user** (not service account) with these roles = **CRITICAL** violation
4. **Service Accounts**: Service Agent roles are acceptable for service accounts, but still flag if unusual
5. **Report**: List all violations in the audit report with severity level

## Severity Levels

- **CRITICAL**: User has owner, editor, or *Admin role in pd/np environment
- **HIGH**: User has service agent role or token creator role
- **MEDIUM**: User has viewer or other excessive role in pd/np
- **LOW**: User has excessive role in dv/qa (development) environment

## Exceptions

The following accounts may have elevated permissions:
- `sebastien.morand-adm@loreal.com` (CTO account)
- `*-adm@loreal.com` (Admin accounts)
- Service accounts (*.iam.gserviceaccount.com)
- Google-managed service agents (@gcp-sa-*.iam.gserviceaccount.com)

However, even these should be reviewed and justified in the audit report.

## Recommendations

When excessive roles are detected:

1. **Immediate Action**: Remove excessive roles from users in pd/np environments
2. **Least Privilege**: Grant only the minimum permissions needed
3. **Time-Limited Access**: Use temporary access (12-hour expiration) for elevated permissions
4. **Service Accounts**: Use service accounts instead of user accounts for automated processes
5. **Custom Roles**: Create custom roles with specific permissions instead of broad predefined roles
6. **Regular Audits**: Conduct regular audits to detect and remove excessive permissions

## References

- Source: `/Users/sebastien.morand/projects/claude/excessive_roles.txt`
- L'Oréal Organization ID: 1090299993982
- Last Updated: 2025-01-14
