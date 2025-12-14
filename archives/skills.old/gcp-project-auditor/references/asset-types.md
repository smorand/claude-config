# GCP Asset Types Reference

This document provides a comprehensive list of GCP asset types to scan during audits, organized by category.

## Data & Analytics

### BigQuery
- `bigquery.googleapis.com/Dataset` - BigQuery datasets
- `bigquery.googleapis.com/Table` - BigQuery tables

**Key Checks:**
- Dataset IAM policies (who has access)
- Authorized views and datasets
- Table-level security
- Public datasets (allUsers, allAuthenticatedUsers)
- Data encryption settings
- Row/column-level security

**Commands:**
```bash
# List BigQuery datasets
gcloud --account sebastien.morand-adm@loreal.com alpha bq datasets list --project <PROJECT_ID>

# Get dataset IAM policy
gcloud --account sebastien.morand-adm@loreal.com alpha bq datasets get-iam-policy <DATASET_ID> --project <PROJECT_ID>
```

### Data Processing
- `dataflow.googleapis.com/Job` - Dataflow jobs
- `dataproc.googleapis.com/Cluster` - Dataproc clusters
- `dataproc.googleapis.com/Job` - Dataproc jobs
- `composer.googleapis.com/Environment` - Cloud Composer environments
- `workflows.googleapis.com/Workflow` - Cloud Workflows

**Key Checks:**
- Service account used for execution
- Network configuration
- Encryption settings
- Resource quotas

## Compute & Applications

### Cloud Run
- `run.googleapis.com/Service` - Cloud Run services

**Key Checks:**
- Ingress settings (allow all, internal only, internal and Cloud Load Balancing)
- Authentication (require authentication vs allow unauthenticated)
- Service account permissions
- Environment variables (check for secrets)
- Revision traffic split

**Commands:**
```bash
# List Cloud Run services
gcloud --account sebastien.morand-adm@loreal.com run services list --project <PROJECT_ID> --region europe-west1

# Get service details
gcloud --account sebastien.morand-adm@loreal.com run services describe <SERVICE> --project <PROJECT_ID> --region europe-west1
```

### Cloud Functions
- `cloudfunctions.googleapis.com/CloudFunction` - Cloud Functions (1st gen)
- `cloudfunctions.googleapis.com/Function` - Cloud Functions (2nd gen)

**Key Checks:**
- Trigger type (HTTP, Pub/Sub, Storage, etc.)
- Authentication requirements
- Service account
- Environment variables
- VPC connector

### App Engine
- `appengine.googleapis.com/Application` - App Engine application
- `appengine.googleapis.com/Service` - App Engine services
- `appengine.googleapis.com/Version` - App Engine versions

**Key Checks:**
- Service account
- Ingress settings
- Environment variables
- Scaling configuration

### Compute Engine
- `compute.googleapis.com/Instance` - Virtual machine instances
- `compute.googleapis.com/Disk` - Persistent disks
- `compute.googleapis.com/InstanceTemplate` - Instance templates
- `compute.googleapis.com/InstanceGroup` - Instance groups
- `compute.googleapis.com/InstanceGroupManager` - Managed instance groups

**Key Checks:**
- Service account attached
- External IP addresses
- SSH keys
- Metadata (check for sensitive data)
- Disk encryption
- OS Login enabled/disabled

### Kubernetes (GKE)
- `container.googleapis.com/Cluster` - GKE clusters
- `container.googleapis.com/NodePool` - GKE node pools

**Key Checks:**
- Control plane network exposure
- Workload Identity enabled
- Node service accounts
- Network policies
- Binary authorization
- Pod security policies

## Databases

### Cloud SQL
- `sqladmin.googleapis.com/Instance` - Cloud SQL instances

**Key Checks:**
- Public IP (should be disabled for production)
- Authorized networks
- SSL/TLS enforcement
- Backup configuration
- High availability
- Deletion protection

**Commands:**
```bash
# List Cloud SQL instances
gcloud --account sebastien.morand-adm@loreal.com sql instances list --project <PROJECT_ID>

# Get instance details
gcloud --account sebastien.morand-adm@loreal.com sql instances describe <INSTANCE> --project <PROJECT_ID>
```

### AlloyDB
- `alloydb.googleapis.com/Cluster` - AlloyDB clusters
- `alloydb.googleapis.com/Instance` - AlloyDB instances

**Key Checks:**
- VPC network
- Encryption settings
- Backup configuration
- High availability

### Spanner
- `spanner.googleapis.com/Instance` - Spanner instances
- `spanner.googleapis.com/Database` - Spanner databases

**Key Checks:**
- Instance IAM policies
- Database IAM policies
- Encryption settings
- Backup configuration

### Bigtable
- `bigtable.googleapis.com/Instance` - Bigtable instances
- `bigtable.googleapis.com/Table` - Bigtable tables
- `bigtable.googleapis.com/Cluster` - Bigtable clusters

**Key Checks:**
- Instance IAM policies
- Table IAM policies
- Replication configuration
- Deletion protection

### Firestore
- `firestore.googleapis.com/Database` - Firestore databases

**Key Checks:**
- Security rules
- Database mode (Firestore Native vs Datastore mode)
- Point-in-time recovery

## Storage

### Cloud Storage
- `storage.googleapis.com/Bucket` - Cloud Storage buckets

**Key Checks:**
- Bucket IAM policies
- Public access prevention
- Uniform bucket-level access
- Encryption (Google-managed vs customer-managed)
- Versioning
- Lifecycle policies
- CORS configuration

**Commands:**
```bash
# List buckets
gcloud --account sebastien.morand-adm@loreal.com storage buckets list --project <PROJECT_ID>

# Get bucket IAM policy
gcloud --account sebastien.morand-adm@loreal.com storage buckets get-iam-policy gs://<BUCKET_NAME>

# Check public access
gcloud --account sebastien.morand-adm@loreal.com storage buckets describe gs://<BUCKET_NAME> --format="value(iamConfiguration.publicAccessPrevention)"
```

## Identity & Access Management

### Service Accounts
- `iam.googleapis.com/ServiceAccount` - Service accounts

**Key Checks:**
- Who can impersonate (roles/iam.serviceAccountUser, roles/iam.serviceAccountTokenCreator)
- Keys created (should use Workload Identity instead)
- Permissions granted to the service account
- Usage (last used timestamp)

**Commands:**
```bash
# List service accounts
gcloud --account sebastien.morand-adm@loreal.com iam service-accounts list --project <PROJECT_ID>

# Get service account IAM policy (who can impersonate)
gcloud --account sebastien.morand-adm@loreal.com iam service-accounts get-iam-policy <SA_EMAIL> --project <PROJECT_ID>

# Get service account keys
gcloud --account sebastien.morand-adm@loreal.com iam service-accounts keys list --iam-account <SA_EMAIL> --project <PROJECT_ID>
```

### Service Account Keys
- `iam.googleapis.com/ServiceAccountKey` - Service account keys

**Key Checks:**
- User-managed keys (should be minimal or zero)
- Key age (rotate old keys)
- Key usage

**🚨 CRITICAL**: User-managed service account keys are a security risk. Use Workload Identity or short-lived tokens instead.

### Workload Identity Pool
- `iam.googleapis.com/WorkloadIdentityPool` - Workload Identity pools
- `iam.googleapis.com/WorkloadIdentityPoolProvider` - Workload Identity pool providers

**Key Checks:**
- Provider configuration
- Attribute mappings
- Attribute conditions

## Networking

### VPC Networks
- `compute.googleapis.com/Network` - VPC networks
- `compute.googleapis.com/Subnetwork` - Subnetworks

**Key Checks:**
- Auto-create subnets (should be disabled)
- Private Google Access enabled
- Flow logs enabled
- VPC peering

**Commands:**
```bash
# List networks
gcloud --account sebastien.morand-adm@loreal.com compute networks list --project <PROJECT_ID>

# List subnets
gcloud --account sebastien.morand-adm@loreal.com compute networks subnets list --project <PROJECT_ID>
```

### Firewall Rules
- `compute.googleapis.com/Firewall` - VPC firewall rules

**Key Checks:**
- Overly permissive rules (source 0.0.0.0/0 with broad port ranges)
- Ingress vs egress rules
- Target tags/service accounts
- Priority conflicts

**🚨 CRITICAL**: Flag any rule with source `0.0.0.0/0` and ports like `0-65535`, `22` (SSH), `3389` (RDP), `3306` (MySQL), `5432` (PostgreSQL)

**Commands:**
```bash
# List firewall rules
gcloud --account sebastien.morand-adm@loreal.com compute firewall-rules list --project <PROJECT_ID>

# Describe specific rule
gcloud --account sebastien.morand-adm@loreal.com compute firewall-rules describe <RULE_NAME> --project <PROJECT_ID>
```

### Load Balancers
- `compute.googleapis.com/ForwardingRule` - Forwarding rules
- `compute.googleapis.com/BackendService` - Backend services
- `compute.googleapis.com/UrlMap` - URL maps
- `compute.googleapis.com/TargetHttpProxy` - HTTP target proxies
- `compute.googleapis.com/TargetHttpsProxy` - HTTPS target proxies
- `compute.googleapis.com/SslCertificate` - SSL certificates

**Key Checks:**
- SSL policy
- Backend security (IAP, Cloud Armor)
- Health checks
- Session affinity

### VPC Peering & VPN
- `compute.googleapis.com/Route` - Routes
- `compute.googleapis.com/VpnGateway` - VPN gateways
- `compute.googleapis.com/VpnTunnel` - VPN tunnels
- `compute.googleapis.com/Router` - Cloud Routers

### Private Service Connect
- `compute.googleapis.com/ServiceAttachment` - Service attachments
- `compute.googleapis.com/ForwardingRule` - PSC forwarding rules

## Secret Management

### Secret Manager
- `secretmanager.googleapis.com/Secret` - Secrets
- `secretmanager.googleapis.com/SecretVersion` - Secret versions

**Key Checks:**
- IAM policies on secrets
- Rotation configuration
- Replication policy
- Usage tracking

**Commands:**
```bash
# List secrets
gcloud --account sebastien.morand-adm@loreal.com secrets list --project <PROJECT_ID>

# Get secret IAM policy
gcloud --account sebastien.morand-adm@loreal.com secrets get-iam-policy <SECRET> --project <PROJECT_ID>
```

## Pub/Sub

### Pub/Sub
- `pubsub.googleapis.com/Topic` - Pub/Sub topics
- `pubsub.googleapis.com/Subscription` - Pub/Sub subscriptions

**Key Checks:**
- Topic IAM policies
- Subscription IAM policies
- Message retention
- Dead letter topics

## Logging & Monitoring

### Logging
- `logging.googleapis.com/LogSink` - Log sinks
- `logging.googleapis.com/LogBucket` - Log buckets

**Key Checks:**
- Sink destinations
- Filter configuration
- Retention settings

### Monitoring
- `monitoring.googleapis.com/AlertPolicy` - Alert policies

## Tags & Labels

### Tags
Tags are key-value pairs attached to resources for organization and policy enforcement.

**Key Tags to Check:**
- `env` - Environment (pd, np, qa, dv)
- `cost-center` - Cost allocation
- `owner` - Resource owner
- `compliance` - Compliance requirements

**Commands:**
```bash
# Get project tags
gcloud --account sebastien.morand-adm@loreal.com projects describe <PROJECT_ID> --format=json | jq '.labels'
```

### Labels
Similar to tags, used for resource organization.

## Security-Specific Checks

### Binary Authorization
- `binaryauthorization.googleapis.com/Policy` - Binary Authorization policies

### Security Command Center
- `securitycenter.googleapis.com/Finding` - Security findings
- `securitycenter.googleapis.com/Source` - Security sources

### Organization Policy
- `orgpolicy.googleapis.com/Policy` - Organization policies

**Key Policies to Check:**
- `constraints/compute.vmExternalIpAccess` - External IP restrictions
- `constraints/sql.restrictPublicIp` - SQL public IP restrictions
- `constraints/iam.disableServiceAccountKeyCreation` - Service account key restrictions
- `constraints/storage.uniformBucketLevelAccess` - Uniform bucket-level access

## Common Asset Filters

### Filter by Resource Type
```bash
gcloud --account sebastien.morand-adm@loreal.com asset search-all-resources \
  --scope=projects/<PROJECT_ID> \
  --asset-types=compute.googleapis.com/Instance,compute.googleapis.com/Disk
```

### Filter by Location
```bash
gcloud --account sebastien.morand-adm@loreal.com asset search-all-resources \
  --scope=projects/<PROJECT_ID> \
  --asset-types=run.googleapis.com/Service \
  --filter="location:europe-west1"
```

### Filter by Labels
```bash
gcloud --account sebastien.morand-adm@loreal.com asset search-all-resources \
  --scope=projects/<PROJECT_ID> \
  --filter="labels.env=pd"
```

## Output Format

Always use `--format=json` for programmatic parsing:

```bash
gcloud --account sebastien.morand-adm@loreal.com asset search-all-resources \
  --scope=projects/<PROJECT_ID> \
  --format=json > resources.json
```

## References

- [GCP Asset Inventory Documentation](https://cloud.google.com/asset-inventory/docs/overview)
- [GCP Resource Types](https://cloud.google.com/asset-inventory/docs/supported-asset-types)
- [IAM Permissions Reference](https://cloud.google.com/iam/docs/permissions-reference)
