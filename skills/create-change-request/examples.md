# Change Request Builder Examples

## Example 1: Standard Deployment with Multiple Stories

**User Request**: "I need to create a change request for btdplogs. The CR number is CHG0012345 and release is RLSE0027806. Deployment is scheduled for tomorrow at 2 PM and should complete by 5 PM."

**Process Flow**:

1. **Template Identification**: btdplogs template
2. **Git Analysis** (in `../btdplogs/` directory):
   - Last merge: `a1b2c3d Merge branch 'mep/CHG0012300/sprint-18-mep-1' into 'master'`
   - Extracted: Sprint 18, MEP 1
   - **Ask user**: "I see the last release was Sprint 18 MEP 1. Should this be Sprint 18 MEP 2?"
   - User confirms: Sprint 18 MEP 2

3. **Commit History** (master..develop):
   ```
   d4e5f6g [STRY0686916] Add excessive roles detection module
   h7i8j9k [STRY0632835] Refactor dashboard industrialization
   l0m1n2o [STRY0680946] Update contacts service integration
   p3q4r5s Fix typo in configuration
   t6u7v8w Update dependencies
   ```

4. **Story Extraction**: STRY0686916, STRY0632835, STRY0680946

5. **BigQuery Results**:
   ```
   STRY0686916: "Excessive Roles Detection" - Implement automated detection of excessive IAM roles
   STRY0632835: "Dashboard Industrialization" - Standardize dashboard creation process
   STRY0680946: "Contacts Integration" - Update integration with contacts service
   ```

6. **Technical Changes**:
   ```
   M  src/modules/security/excessive_roles.py
   M  src/modules/security/__init__.py
   A  src/dashboards/factory.py
   M  src/services/contacts_client.py
   M  terraform/modules/cloud_function/main.tf
   M  requirements.txt
   ```

**Generated Change Request** (`output/change_requests/btdplogs_CHG0012345.yaml`):

```yaml
number: CHG0012345
short_description: "Deployment of excessive roles detection, dashboard industrialization and contacts refactoring"
description: |
  ## Summary
  This release deploys Sprint 18 MEP 2 for BTDP Security Services, including new excessive roles detection capabilities, dashboard standardization, and improved contacts service integration.

  ## Functional Requirements

  **STRY0686916 - Excessive Roles Detection**
  Implements automated detection and alerting for excessive IAM roles assigned to GCP projects. The system monitors role assignments and flags violations based on security policies defined in the configuration table.

  **STRY0632835 - Dashboard Industrialization**
  Standardizes the dashboard creation process by introducing a factory pattern. This reduces code duplication and ensures consistent dashboard configurations across all security services.

  **STRY0680946 - Contacts Integration Enhancement**
  Updates the contacts service client to use the latest API version with improved error handling and retry logic.

  ## Technical Changes

  **Security Module**
  - Added new excessive_roles.py module with detection logic
  - Integrated with existing security monitoring pipeline
  - Updated Terraform to deploy new Cloud Function trigger

  **Dashboard Factory**
  - Introduced factory pattern for dashboard creation
  - Centralized dashboard configuration
  - Reduced code duplication across services

  **Contacts Service**
  - Updated client to API v2.1
  - Improved error handling and retry logic
  - Added connection pooling for better performance

  ## Commit History
  d4e5f6g [STRY0686916] Add excessive roles detection module
  h7i8j9k [STRY0632835] Refactor dashboard industrialization
  l0m1n2o [STRY0680946] Update contacts service integration
  p3q4r5s Fix typo in configuration
  t6u7v8w Update dependencies

release: RLSE0027806
release_short_description: "[BTDPLOGS]SPRINT 18 MEP 2"
planned_start_date: "2025-10-24 14:00:00"
planned_end_date: "2025-10-24 17:00:00"
# ... other template fields preserved as-is
```

**Post-Creation Actions**:
1. Branch created: `mep/CHG0012345/sprint-18-mep-2`
2. Branch pushed to origin with upstream tracking
3. User notified of branch name and location

---

## Example 2: Hotfix Deployment (Single Story)

**User Request**: "Quick CR for housekeeping project. CR: CHG0098765, Release: RLSE0099999. Deploy today at noon, finish by 1 PM. It's just a hotfix for the memory leak."

**Process Flow**:

1. **Template**: housekeeping
2. **Git Analysis**:
   - Last merge: Sprint 22 MEP 4
   - **Suggest**: Sprint 22 MEP 5 (user confirms)
3. **Commit History**:
   ```
   x9y8z7a [STRY0700123] Fix memory leak in data processor
   ```
4. **BigQuery**:
   ```
   STRY0700123: "Memory Leak Fix" - Resolve memory leak causing pod restarts
   ```

**Generated CR** (simplified):

```yaml
number: CHG0098765
short_description: "Hotfix deployment for memory leak in data processor"
description: |
  ## Summary
  Emergency hotfix for Sprint 22 MEP 5 to resolve memory leak in the data processing pipeline causing frequent pod restarts.

  ## Functional Requirements

  **STRY0700123 - Memory Leak Fix**
  Resolves critical memory leak in the data processing service that was causing pods to restart every 2-4 hours due to OOM errors. Root cause identified as unclosed database connections in the connection pool.

  ## Technical Changes

  **Data Processor Service**
  - Fixed connection pool leak in database client
  - Added proper connection cleanup in error handlers
  - Improved connection pool monitoring

  ## Commit History
  x9y8z7a [STRY0700123] Fix memory leak in data processor

release: RLSE0099999
release_short_description: "[HOUSEKEEPING]SPRINT 22 MEP 5"
planned_start_date: "2025-10-23 12:00:00"
planned_end_date: "2025-10-23 13:00:00"
```

**Branch**: `mep/CHG0098765/sprint-22-mep-5` created and pushed

---

## Example 3: Template Inheritance Usage

**Scenario**: User has a custom template `dataleak.yaml` that inherits from `btdplogs.yaml`

**dataleak.yaml**:
```yaml
# Heritated from template btdplogs
assignment_group: "BTDP Security - Data Leak"
change_type: "Security Enhancement"
# All other fields inherited from btdplogs.yaml
```

**User Request**: "Create CR for dataleak template, CHG0055555, RLSE0011111"

**Process**:
1. Read `.claude/skills/change-request-builder/templates/dataleak.yaml`
2. Detect inheritance: `# Heritated from template btdplogs`
3. Load base template: `.claude/skills/change-request-builder/templates/btdplogs.yaml`
4. Merge: Start with btdplogs fields, override with dataleak fields
5. Result: CR has all btdplogs fields except `assignment_group` and `change_type` which use dataleak values

---

## Example 4: User Interaction for Missing Information

**User Request**: "Create a change request for btdplogs"

**Assistant Response**:
"I'll help you create a change request for btdplogs. I need some information:

1. What is the Change Request number? (format: CHG0012345)
2. What is the Release number? (format: RLSE0027806)
3. When is the planned start date and time? (format: YYYY-MM-DD HH:MM:SS)
4. When is the planned end date and time? (format: YYYY-MM-DD HH:MM:SS)

I'll analyze the git history and suggest the sprint and MEP numbers after you provide this information."

**User Provides**:
- CR: CHG0012345
- Release: RLSE0027806
- Start: 2025-10-25 (no time specified)
- End: 2025-10-25 (no time specified)

**Assistant**:
"Thanks! I'll use the default time of 12:00:00 (noon) for both dates since you didn't specify times.

Now analyzing the git history in ../btdplogs/..."

[Continues with normal flow]

---

## Example 5: Complex Multi-Feature Release

**User Request**: "Big deployment coming up for btdplogs. CR CHG0077777, Release RLSE0088888. Deployment window is 2025-11-01 from 8 AM to 6 PM."

**Git History Shows**: 25 commits across 5 different stories

**Process**:
- Extracts all 5 story numbers
- Queries BigQuery for all functional requirements
- Analyzes 50+ file changes
- Groups changes by functionality:
  - Security enhancements (12 files)
  - Performance optimizations (8 files)
  - New API endpoints (15 files)
  - Infrastructure updates (10 files)
  - Bug fixes (5 files)

**Generated Description**:
```
## Summary
Major release for Sprint 19 MEP 1 delivering security enhancements, performance optimizations, new API capabilities, and infrastructure modernization across BTDP Security Services.

## Functional Requirements

**STRY0710001 - Enhanced Role-Based Access Control**
Implements fine-grained RBAC with support for custom roles and conditional access policies...

**STRY0710002 - API Performance Optimization**
Improves API response times by 60% through caching, connection pooling, and query optimization...

[3 more stories...]

## Technical Changes

**Security & Access Control** (12 files modified)
- Implemented custom RBAC engine with policy evaluation
- Added conditional access based on user context
- Enhanced audit logging for all access decisions

**Performance Improvements** (8 files modified)
- Introduced Redis caching layer for frequently accessed data
- Optimized database queries with new indexes
- Implemented connection pooling for BigQuery client

**API Enhancements** (15 files modified)
- Added 8 new REST endpoints for role management
- Implemented GraphQL interface for complex queries
- Enhanced API documentation with OpenAPI 3.0 spec

**Infrastructure** (10 files modified)
- Migrated to Cloud Run Gen 2
- Updated Terraform modules for new GCP features
- Implemented auto-scaling based on request latency

**Bug Fixes** (5 files modified)
- Fixed race condition in cache invalidation
- Resolved memory leak in async task processor
- Corrected timezone handling in scheduler

## Commit History
[Full 25-commit history listed]
```

---

## Key Patterns Demonstrated

1. **Automatic Sprint/MEP Detection**: Always analyze last merge and ask user to confirm
2. **Time Defaulting**: Use 12:00:00 when user doesn't provide time
3. **Summarization**: Group technical changes by functionality, don't list every file
4. **Business Context**: Explain what each story delivers in business terms
5. **Template Inheritance**: Support reusable base templates with overrides
6. **Automated Branch Creation**: Always create and push release branch after CR generation
7. **User Guidance**: Ask for missing required information clearly and specifically
