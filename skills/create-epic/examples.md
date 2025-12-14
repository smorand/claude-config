# Epic Creation Examples

## Example 1: Security Initiative (Provided in SKILL.md)

**Title**: New Security Module for Excessive Roles Management

**Business Needs**
Reduce the attack surface by preventing potential security breaches caused by overly permissive roles assigned to projects.

**Current Status**
Currently managed manually by the security team or addressed on a case-by-case basis by individual teams.

**Target of the Epic**
Create a service that operates based on a reference configuration table to identify and flag excessive roles, enabling automated detection and remediation.

**Impact on BTDP**
Transform team workflows by implementing automatic IAM remediation at the project level, ensuring security policies remain current and consistently enforced.

---

## Example 2: Data Quality Initiative

**User Request**: "We need to improve data quality across our BigQuery datasets. Too many inconsistencies and missing values are causing issues downstream."

**Generated Epic**:

**Title**: Data Quality Framework for BTDP BigQuery Datasets

**Business Needs**
Improve data reliability and reduce downstream processing failures caused by inconsistent data quality. Current data quality issues result in approximately 15% of analytics queries failing or returning inaccurate results, undermining stakeholder confidence in BTDP data.

**Current Status**
Data quality is checked inconsistently across different teams and services. Each team implements their own validation logic (if any), leading to duplicated effort and gaps in coverage. No centralized monitoring or alerting for data quality issues.

**Target of the Epic**
Build a centralized data quality framework that:
- Automatically validates data against defined quality rules
- Provides real-time monitoring and alerting for quality violations
- Generates data quality dashboards for stakeholders
- Implements automated remediation for common data issues
- Establishes data quality SLAs for critical datasets

**Impact on BTDP**
- **Teams**: Reduced time spent debugging data issues, standardized quality checks across services
- **Stakeholders**: Increased confidence in data accuracy, better decision-making
- **Operations**: Proactive issue detection before downstream impacts
- **Compliance**: Better audit trail and data lineage for regulatory requirements
- **Expected Improvement**: Reduce data-related query failures by 80%, decrease mean time to detect data issues from days to minutes

---

## Example 3: Developer Experience Enhancement

**User Request**: "Our deployment process is too slow and manual. We need to modernize our CI/CD pipeline."

**Generated Epic**:

**Title**: Modernized CI/CD Pipeline for BTDP Services

**Business Needs**
Accelerate deployment velocity and reduce production incidents caused by manual deployment errors. Current average deployment time of 4 hours per service creates bottlenecks in delivering business value and responding to critical issues. Manual processes also increase risk of configuration drift and human error.

**Current Status**
Deployments require manual steps including:
- Manual Terraform apply commands
- Manual validation of deployment success
- Manual rollback procedures when issues occur
- No automated testing in deployment pipeline
- Deployments only possible during business hours with specific team members

Average deployment time: 4 hours
Deployment success rate: 75% (25% require rollback or fixes)

**Target of the Epic**
Implement fully automated CI/CD pipeline that:
- Automatically tests code changes (unit, integration, security scans)
- Deploys infrastructure and applications via GitOps workflow
- Implements blue-green deployment strategy for zero-downtime updates
- Provides automated rollback capabilities
- Includes deployment status dashboards and notifications
- Enables self-service deployments for development teams

**Impact on BTDP**
- **Deployment Speed**: Reduce average deployment time from 4 hours to 20 minutes
- **Reliability**: Increase deployment success rate from 75% to 95%
- **Developer Productivity**: Enable multiple deployments per day vs. current 1-2 per week
- **Risk Reduction**: Automated testing catches issues before production
- **Team Autonomy**: Teams can deploy independently without waiting for platform team
- **Incident Response**: Faster rollback capabilities reduce mean time to recovery
- **Cost Efficiency**: Reduce manual effort by approximately 20 hours per week across teams

---

## Example 4: Observability Enhancement

**User Request**: "We need better monitoring and logging. When things break, we spend too long figuring out what went wrong."

**Generated Epic**:

**Title**: Unified Observability Platform for BTDP Services

**Business Needs**
Improve incident detection and resolution times by providing comprehensive observability across all BTDP services. Current mean time to detect (MTTD) issues is 45 minutes and mean time to resolve (MTTR) is 3 hours, resulting in extended service disruptions and poor user experience. Lack of visibility into system behavior prevents proactive issue prevention and root cause analysis.

**Current Status**
Observability is fragmented across multiple tools and platforms:
- Logs scattered across Cloud Logging, application logs, and local files
- No centralized metrics dashboard
- Limited distributed tracing capabilities
- Manual correlation of logs across services
- Reactive alerting based only on basic infrastructure metrics
- No application performance monitoring (APM)

Teams spend 60% of incident response time gathering diagnostic information rather than fixing issues.

**Target of the Epic**
Deploy unified observability platform that provides:
- Centralized log aggregation with powerful search and filtering
- Comprehensive metrics collection and visualization dashboards
- Distributed tracing across all microservices
- Application performance monitoring (APM) with code-level insights
- Intelligent alerting based on anomaly detection and SLOs
- Service dependency mapping and health visualization
- Pre-built dashboards for common troubleshooting scenarios

**Impact on BTDP**
- **Incident Response**: Reduce MTTD from 45 min to 5 min, MTTR from 3 hours to 30 minutes
- **Developer Efficiency**: Reduce time spent troubleshooting by 50%
- **Proactive Prevention**: Enable identification of performance degradation before user impact
- **User Experience**: Faster issue resolution results in better service reliability
- **Cost Optimization**: Identify resource waste and optimization opportunities
- **Team Collaboration**: Shared visibility improves cross-team communication during incidents
- **Compliance**: Better audit trail and system behavior documentation
- **Expected ROI**: 40 hours per week saved across teams in troubleshooting time

---

## Example 5: Cost Optimization Initiative

**User Request**: "Our GCP costs are growing too fast. We need to get spending under control."

**Generated Epic**:

**Title**: BTDP Cloud Cost Optimization and Governance Framework

**Business Needs**
Control rapidly growing cloud infrastructure costs that have increased 250% year-over-year without corresponding increase in business value. Current spending trend is unsustainable and puts pressure on BTDP budget. Need visibility and control over resource usage to optimize spend while maintaining performance and reliability.

**Current Status**
Limited visibility into cost drivers:
- No cost allocation by team, service, or project
- Resources provisioned without cost awareness
- No automated cleanup of unused resources
- Over-provisioned resources "just in case"
- No budget alerts or spending limits
- Teams unaware of cost impact of their architectural decisions

Monthly GCP spend: €150k (projected €450k by year-end if unchecked)

**Target of the Epic**
Implement comprehensive cost optimization framework:
- Automated cost allocation and showback reporting by team/service
- Right-sizing recommendations for compute and storage resources
- Automated cleanup of unused resources (orphaned disks, old snapshots, etc.)
- Budget alerts and spending limits per project/team
- Cost-aware architectural guidelines and review process
- Reserved instance and committed use discount optimization
- Storage lifecycle policies for archival and deletion

**Impact on BTDP**
- **Cost Savings**: Target 30% reduction in monthly cloud spend (€45k/month saved)
- **Financial Visibility**: Teams understand their cost contribution and can make informed decisions
- **Resource Efficiency**: Eliminate waste from over-provisioned and unused resources
- **Budget Predictability**: Better forecasting and budget management
- **Team Accountability**: Cost ownership drives more responsible resource usage
- **Sustainability**: Reduced resource usage aligns with environmental goals
- **ROI**: Projected annual savings of €540k with one-time implementation cost of €80k
