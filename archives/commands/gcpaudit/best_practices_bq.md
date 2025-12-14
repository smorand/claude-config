# BigQuery, Workflows & Terraform Best Practices

Focused best practices guide for BigQuery optimization, Google Cloud Workflows, and Terraform infrastructure management in RMSP Cockpit project. Analyze code against language-specific best practices, coding standards, and community conventions to improve code quality and maintainability.

## Instructions for Claude

When checking best practices:

1. **Apply Relevant Standards**: Use appropriate style guides and conventions
2. **Context Awareness**: Consider project-specific patterns and existing conventions
3. **Actionable Feedback**: Provide specific examples of improvements
4. **Prioritize Issues**: Focus on impactful improvements over nitpicks

## BigQuery Best Practices

### Query Optimization
- **Efficient Filtering**: Use WHERE clauses early in query processing
- **Partition Pruning**: Leverage table partitioning for large datasets
- **Clustering Strategy**: Apply clustering for frequently filtered columns
- **Cost Management**: Avoid SELECT *, use LIMIT for development queries
- **Data Types**: Choose appropriate data types for storage efficiency

**Example Patterns:**
```sql
-- Good: Efficient query with proper filtering and partitioning
SELECT
    project_id,
    delivery_date,
    SUM(quantity) as total_quantity
FROM `${datasets["fact_data"].reference}.fact_supplier_delivery`
WHERE delivery_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
  AND project_id IS NOT NULL
GROUP BY project_id, delivery_date
ORDER BY delivery_date DESC;

-- Bad: Inefficient query with full table scan
SELECT *
FROM `project.dataset.fact_supplier_delivery`
WHERE EXTRACT(YEAR FROM delivery_date) = 2024;
```

### Stored Procedures Design
- **Parameter Validation**: Validate input parameters at procedure start
- **Error Logging**: Log execution with start/end timestamps
- **Transaction Management**: Use appropriate transaction boundaries
- **Template References**: Use `${tables["table_name"].reference}` for table references

**RMSP Cockpit Procedure Pattern:**
```sql
CREATE OR REPLACE PROCEDURE `${datasets["fact_data"].reference}.sproc_load_fact_supplier_delivery`()
BEGIN
  DECLARE procedure_name STRING DEFAULT 'sproc_load_fact_supplier_delivery';
  DECLARE start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP();

  -- Log procedure start
  CALL `${datasets["others"].reference}.sproc_log_procedure_execution`(
    procedure_name, 'START', start_time, NULL, NULL
  );

  BEGIN
    -- MERGE Pattern B (Incremental)
    MERGE `${tables["fact_supplier_delivery"].reference}` AS target
    USING (
      SELECT supplier_id, delivery_date, quantity
      FROM `itg-btdppublished-gbl-ww-${project_env}.btdp_ds_c1_201_wise_eu_${project_env}.supplier_deliveries`
      WHERE delivery_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
    ) AS source
    ON source.supplier_id = target.supplier_id
       AND source.delivery_date = target.delivery_date
    WHEN MATCHED THEN UPDATE SET
      quantity = source.quantity,
      updated_at = CURRENT_TIMESTAMP()
    WHEN NOT MATCHED BY TARGET THEN INSERT VALUES(
      source.supplier_id, source.delivery_date, source.quantity, CURRENT_TIMESTAMP()
    );
    -- Note: DELETE not considered for this MERGE pattern

    CALL `${datasets["others"].reference}.sproc_log_procedure_execution`(
      procedure_name, 'SUCCESS', start_time, CURRENT_TIMESTAMP(), 'Processed supplier deliveries'
    );

  EXCEPTION WHEN ERROR THEN
    CALL `${datasets["others"].reference}.sproc_log_procedure_execution`(
      procedure_name, 'ERROR', start_time, CURRENT_TIMESTAMP(), @@error.message
    );
    RAISE;
  END;
END;
```

### Security & IAM
- **Parameterized Queries**: Prevent SQL injection through proper templating
- **Column-Level Security**: Use BigQuery row-level security for sensitive data
- **IAM Roles**: Apply principle of least privilege
- **Data Classification**: Implement c1/c2/c3 confidentiality levels

## Google Cloud Workflows Best Practices

### Workflow Structure
- **Error Handling**: Implement comprehensive retry mechanisms
- **Lazy Execution**: Check timestamps before processing (avoid unnecessary runs)
- **Modular Design**: Break complex workflows into manageable steps
- **Logging**: Include proper step logging and error reporting

**RMSP Workflow Pattern:**
```yaml
# configuration/workflows/load_supplier_data.yaml
workflow_name: load_supplier_data_workflow
steps:
  - name: check_new_data
    call: http.get
    args:
      url: https://api.wise.loreal.com/check-timestamp
      auth:
        type: OAuth2
    result: timestamp_check

  - name: conditional_processing
    switch:
      - condition: ${timestamp_check.body.has_new_data}
        next: call_procedure
      - condition: true
        next: skip_processing

  - name: call_procedure
    call: googleapis.bigquery.v2.jobs.query
    args:
      projectId: ${project}
      body:
        query: CALL `${datasets["fact_data"].project}.${datasets["fact_data"].dataset_id}.sproc_load_fact_supplier_delivery`()
        useLegacySql: false
    result: procedure_result

  - name: log_completion
    call: http.post
    args:
      url: https://logging.googleapis.com/v2/entries:write
      body:
        entries:
          - logName: projects/${project}/logs/workflow-execution
            resource:
              type: global
            jsonPayload:
              workflow: load_supplier_data_workflow
              status: completed
              timestamp: ${time.format(sys.now())}
```

### State Machine Integration
- **Trigger Patterns**: Use appropriate triggers (EventArc for external data, Scheduler for internal)
- **External Table Strategy**: Leverage external tables when possible for efficiency
- **Workflow References**: Use proper templating for workflow calls

## Terraform Best Practices

### Module Organization
- **Environment Separation**: Clear separation between dv, qa, np, pd environments
- **Reusable Modules**: Create modules for common RMSP patterns
- **Variable Validation**: Implement validation rules for inputs
- **Resource Naming**: Follow BTDP naming conventions

**RMSP Terraform Structure:**
```hcl
# modules/rmsp-dataset/main.tf
resource "google_bigquery_dataset" "main" {
  dataset_id                  = var.dataset_id
  friendly_name              = var.friendly_name
  description                = var.description
  location                   = var.location
  delete_contents_on_destroy = var.delete_contents_on_destroy

  dynamic "access" {
    for_each = var.access_entries
    content {
      role          = access.value.role
      user_by_email = access.value.user_by_email
      group_by_email = access.value.group_by_email
    }
  }

  labels = merge(var.labels, {
    environment = var.environment
    project     = "rmsp-cockpit"
    domain      = "sourcing"
  })
}

# Variable validation
variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dv", "qa", "np", "pd"], var.environment)
    error_message = "Environment must be one of: dv, qa, np, pd."
  }
}

variable "confidentiality" {
  description = "Data confidentiality level"
  type        = string
  validation {
    condition     = contains(["c1", "c2", "c3"], var.confidentiality)
    error_message = "Confidentiality must be c1, c2, or c3."
  }
}
```

### State Management
- **Remote State**: Use GCS backend with state locking
- **Environment Isolation**: Separate state files per environment
- **Backup Strategy**: Regular state backups and versioning

```hcl
# terraform/environments/dv/backend.tf
terraform {
  backend "gcs" {
    bucket = "rmsp-terraform-state-dv"
    prefix = "terraform/state"
  }
}
```

### Security Configuration
- **Sensitive Variables**: Mark secrets as sensitive
- **Service Accounts**: Use appropriate service accounts per environment
- **IAM Bindings**: Implement least privilege access

```hcl
# Security best practices
resource "google_secret_manager_secret" "api_key" {
  secret_id = "rmsp-api-key-${var.environment}"

  replication {
    automatic = true
  }
}

# Don't expose sensitive values in outputs
output "secret_name" {
  value     = google_secret_manager_secret.api_key.secret_id
  sensitive = false
}

# Mark sensitive variables
variable "api_key" {
  description = "API key for external service"
  type        = string
  sensitive   = true
}
```

## RMSP Cockpit Specific Patterns

### Dataset Naming Convention
```
rmsp_ds_c[123]_[purpose]_eu_[env]
- c1/c2/c3: Confidentiality level
- purpose: base, masterdata, fact_data, fact_data_expose, launchv1
- env: dv, qa, np, pd
```

### Table Template Usage
```yaml
# configuration/tables/fact_supplier_delivery.yaml
table_id: fact_supplier_delivery
dataset: fact_data  # References fact_data.yaml
version: 1
schema:
  - name: supplier_id
    type: STRING
    mode: REQUIRED
  - name: delivery_date
    type: DATE
    mode: REQUIRED
  - name: quantity
    type: NUMERIC
    mode: REQUIRED
```

### Workflow Template Integration
```yaml
# configuration/workflows/load_dim_master.yaml
workflow_name: load_dim_master
steps:
  - name: load_suppliers
    call: ${datasets["masterdata"].project}.${datasets["masterdata"].dataset_id}.sproc_load_dim_supplier
  - name: load_materials
    call: ${datasets["masterdata"].project}.${datasets["masterdata"].dataset_id}.sproc_load_dim_material
```

## Performance Optimization

### BigQuery Cost Reduction
- **Query Slots**: Monitor and optimize slot usage
- **Materialized Views**: Use for frequently accessed aggregations
- **Partitioning Strategy**: Implement date partitioning for time-series data
- **Clustering Keys**: Choose optimal clustering columns

### Workflow Efficiency
- **Parallel Execution**: Use parallel steps where possible
- **Caching Strategy**: Implement workflow result caching
- **Resource Allocation**: Right-size compute resources

### Terraform Performance
- **Plan Optimization**: Use targeted plans when possible
- **Module Caching**: Leverage module registry for reuse
- **Dependency Management**: Minimize resource dependencies

## Monitoring & Alerting

### BigQuery Monitoring
- **Query Performance**: Monitor execution times and costs
- **Data Quality**: Implement data validation checks
- **Usage Patterns**: Track table access and query patterns

### Workflow Monitoring
- **Execution Tracking**: Monitor workflow success/failure rates
- **Performance Metrics**: Track execution duration and resource usage
- **Error Alerting**: Implement proper error notification

### Infrastructure Monitoring
- **Resource Utilization**: Monitor compute and storage usage
- **Cost Tracking**: Implement cost attribution and budgets
- **Security Compliance**: Regular security posture assessment


### Output Format

Structure the analysis and generate report at .claude/reports folder:

```markdown
## Best Practices Review

### Summary
- Language/Framework: [Detected stack]
- Overall Score: X/10
- Key Areas for Improvement: [List]

### Excellent Practices Found
- [Practice 1]: Brief explanation
- [Practice 2]: Brief explanation

### Areas for Improvement

#### High Priority
1. **[Issue Name]**
   - Current: `code example`
   - Recommended: `improved code`
   - Reason: Explanation of why this matters

#### Medium Priority
[Similar format]

#### Low Priority
[Similar format]

### Quick Wins
- [Easy improvement 1]
- [Easy improvement 2]

### Long-term Recommendations
- [Strategic improvement 1]
- [Strategic improvement 2]
```

Focus on:
- Practical, implementable suggestions
- Learning opportunities
- Maintaining consistency with existing code
- Balancing perfection with pragmatism