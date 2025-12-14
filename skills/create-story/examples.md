# Ticket Creation Examples

## Example 1: Feature Implementation with Full Specifications

**User Request**: "I need a ticket for implementing user authentication with OAuth 2.0. It should support Google and Microsoft SSO providers, store tokens in Redis, and integrate with our existing user profile service."

**Generated Ticket**:

**Title**: Implement OAuth 2.0 User Authentication

**Technical Requirements**:
- Implement OAuth 2.0 authentication flow for user login
- Support Google and Microsoft as SSO providers
- Integration with existing user profile service (user-service v2.3)
- Token storage and session management using Redis
- HTTPS required for all authentication endpoints
- Compliance with BTDP security standards

**Technical Spec**:
- Use `passport-oauth2` library for OAuth implementation
- API Endpoints:
  - `POST /auth/google` - Initiate Google OAuth flow
  - `POST /auth/microsoft` - Initiate Microsoft OAuth flow
  - `GET /auth/callback` - OAuth callback handler
  - `POST /auth/logout` - Invalidate session
- Redis schema:
  - Key: `session:{userId}:{sessionId}`
  - TTL: 24 hours
  - Value: JSON with tokens and user metadata
- Environment variables required:
  - `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`
  - `MICROSOFT_CLIENT_ID`, `MICROSOFT_CLIENT_SECRET`
  - `REDIS_URL`

**Impact**:
- **Affected Systems**: Authentication service, user-service, API gateway
- **Benefits**: Enhanced security, simplified user login experience, SSO capabilities
- **Breaking Changes**: None - new endpoints only
- **Dependencies**: Redis cluster must be provisioned before deployment
- **Security**: Reduces password management burden, implements industry-standard authentication

---

## Example 2: Bug Fix Without Technical Spec

**User Request**: "Create a ticket to fix the memory leak in the data processing pipeline. It's causing the pods to restart every few hours."

**Generated Ticket**:

**Title**: Fix Memory Leak in Data Processing Pipeline

**Technical Requirements**:
- Investigate and resolve memory leak in data processing service
- Issue: Pods restarting every 2-4 hours due to OOM errors
- Affected component: `data-processor` service (current version: 1.5.2)
- Must maintain current processing throughput (10k events/sec)
- No changes to public API or data contracts
- Root cause analysis required before implementation

**Impact**:
- **Affected Systems**: Data processing pipeline, downstream analytics services
- **Potential Risks**: May require deployment during off-peak hours if fixes affect processing logic
- **Benefits**: Improved stability, reduced pod restarts, better resource utilization
- **Dependencies**: Monitoring team to provide heap dump analysis
- **Performance**: Expected to reduce memory usage by 30-40% based on preliminary analysis

---

## Example 3: Refactoring Task

**User Request**: "We need to refactor the BigQuery client code to use connection pooling and retry logic."

**Generated Ticket**:

**Title**: Refactor BigQuery Client with Connection Pooling and Retry Logic

**Technical Requirements**:
- Refactor existing BigQuery client implementation
- Add connection pooling to reduce connection overhead
- Implement exponential backoff retry logic for transient failures
- Maintain backward compatibility with existing query methods
- Update all services using the BigQuery client (housekeeping, btdplogs, contacts)
- Add comprehensive error logging and monitoring

**Impact**:
- **Affected Systems**: All services using BigQuery client (housekeeping-service, btdplogs-service, contacts-service)
- **Potential Risks**: Regression in query performance if pooling not configured correctly
- **Benefits**: Improved reliability, reduced query latency, better error handling, reduced BigQuery quota usage
- **Dependencies**: None - internal refactoring only
- **Testing**: Requires thorough integration testing with BigQuery QA environment

---

## Example 4: Infrastructure Change

**User Request**: "Add a new Cloud Function to automatically remediate excessive IAM roles based on our security policies."

**Generated Ticket**:

**Title**: Add Cloud Function for Automated IAM Role Remediation

**Technical Requirements**:
- Create new Cloud Function triggered by Pub/Sub events
- Function reads security policies from reference configuration table
- Identifies and remediates excessive IAM roles on GCP projects
- Sends notifications to security team and project owners
- Implements dry-run mode for testing
- Must run in itg-housekeeping-dv project initially

**Technical Spec**:
- Runtime: Python 3.11
- Trigger: Pub/Sub topic `iam-role-violations`
- Configuration table: BigQuery table `btdp_ds_c1_security.role_policies_v1`
- Remediation actions:
  - Remove excessive roles from service accounts
  - Log all changes to audit table
  - Send notification via email and Slack
- IAM Requirements:
  - `roles/resourcemanager.projectIamAdmin` on target projects
  - `roles/bigquery.dataViewer` for configuration table
- Deployment: Terraform module in `terraform/modules/security/iam-remediation/`

**Impact**:
- **Affected Systems**: All BTDP GCP projects, IAM management workflows
- **Potential Risks**: Incorrect policy configuration could remove legitimate roles
- **Benefits**: Automated security compliance, reduced attack surface, consistent policy enforcement
- **Dependencies**: Security team to provide and maintain policy configuration table
- **Rollout Plan**: Deploy to dev environment first, then staged rollout across environments
