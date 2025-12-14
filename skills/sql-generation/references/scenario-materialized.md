# Materialized Views Pattern

Use for: Reusable queries, scheduled refreshes, performance optimization, dashboard queries.

## When to Use

✅ **Good for**:
- Queries that run repeatedly
- Dashboard/report data sources
- Performance-critical queries
- Scheduled data refreshes
- Complex aggregations used multiple times

❌ **Not suitable for**:
- One-time analysis → Use ad-hoc patterns
- Updating existing tables → Use data preparation patterns
- Real-time data requirements

## Pattern: Stored Procedures with TEMP Tables

Materialized views use stored procedures that create temporary intermediate tables and final materialized tables.

### Basic Structure

```sql
CREATE OR REPLACE PROCEDURE `project.dataset.procedure_name`()
BEGIN
    -- Step 1: Create temporary tables for intermediate results
    CREATE OR REPLACE TEMP TABLE temp_step1 AS
    SELECT ...
    FROM ...
    WHERE ...;

    -- Step 2: Create final materialized table
    CREATE OR REPLACE TABLE `project.dataset.materialized_table` AS
    SELECT ...
    FROM temp_step1
    ...;
END;
```

## Complete Examples

### Example 1: User Metrics Materialization

```sql
-- Stored procedure to refresh user metrics daily
CREATE OR REPLACE PROCEDURE `project.dataset.refresh_user_metrics`()
BEGIN
    -- Step 1: Aggregate order data
    CREATE OR REPLACE TEMP TABLE temp_order_summary AS
    SELECT
        user_id,
        COUNT(DISTINCT order_id) AS order_count,
        SUM(amount) AS total_spent,
        AVG(amount) AS avg_order_value,
        MAX(order_date) AS last_order_date,
        MIN(order_date) AS first_order_date
    FROM `project.dataset.orders`
    WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY)
        AND status = 'completed'
    GROUP BY user_id;

    -- Step 2: Calculate product metrics
    CREATE OR REPLACE TEMP TABLE temp_product_summary AS
    SELECT
        o.user_id,
        COUNT(DISTINCT oi.product_id) AS unique_products_purchased,
        ARRAY_AGG(DISTINCT oi.category IGNORE NULLS) AS categories_purchased
    FROM `project.dataset.orders` o
    INNER JOIN `project.dataset.order_items` oi
        ON o.order_id = oi.order_id
    WHERE o.order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY)
        AND o.status = 'completed'
    GROUP BY o.user_id;

    -- Step 3: Create final materialized table
    CREATE OR REPLACE TABLE `project.dataset.user_metrics_materialized` AS
    SELECT
        u.user_id,
        u.email,
        u.country,
        u.created_at,
        COALESCE(os.order_count, 0) AS order_count,
        COALESCE(os.total_spent, 0) AS total_spent,
        COALESCE(os.avg_order_value, 0) AS avg_order_value,
        os.last_order_date,
        os.first_order_date,
        COALESCE(ps.unique_products_purchased, 0) AS unique_products,
        ps.categories_purchased,
        DATE_DIFF(CURRENT_DATE(), os.last_order_date, DAY) AS days_since_last_order,
        CASE
            WHEN os.order_count >= 10 AND os.total_spent >= 1000 THEN 'VIP'
            WHEN os.order_count >= 5 AND os.total_spent >= 500 THEN 'Loyal'
            WHEN os.order_count >= 2 THEN 'Regular'
            ELSE 'New'
        END AS customer_segment,
        CURRENT_TIMESTAMP() AS refreshed_at
    FROM `project.dataset.users` u
    LEFT OUTER JOIN temp_order_summary os
        ON u.user_id = os.user_id
    LEFT OUTER JOIN temp_product_summary ps
        ON u.user_id = ps.user_id
    WHERE u.active = TRUE;
END;
```

### Example 2: Product Performance Dashboard

```sql
-- Stored procedure for product performance metrics
CREATE OR REPLACE PROCEDURE `project.dataset.refresh_product_performance`()
BEGIN
    -- Step 1: Calculate daily sales metrics
    CREATE OR REPLACE TEMP TABLE temp_daily_sales AS
    SELECT
        oi.product_id,
        DATE(o.order_date) AS sale_date,
        COUNT(DISTINCT o.order_id) AS order_count,
        SUM(oi.quantity) AS units_sold,
        SUM(oi.quantity * oi.unit_price) AS revenue
    FROM `project.dataset.orders` o
    INNER JOIN `project.dataset.order_items` oi
        ON o.order_id = oi.order_id
    WHERE o.order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
        AND o.status = 'completed'
    GROUP BY
        oi.product_id,
        sale_date;

    -- Step 2: Calculate trends and moving averages
    CREATE OR REPLACE TEMP TABLE temp_product_trends AS
    SELECT
        product_id,
        sale_date,
        units_sold,
        revenue,
        AVG(revenue) OVER (
            PARTITION BY product_id
            ORDER BY sale_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS revenue_7day_ma,
        AVG(revenue) OVER (
            PARTITION BY product_id
            ORDER BY sale_date
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ) AS revenue_30day_ma
    FROM temp_daily_sales;

    -- Step 3: Aggregate summary metrics
    CREATE OR REPLACE TEMP TABLE temp_product_summary AS
    SELECT
        product_id,
        SUM(units_sold) AS total_units_sold,
        SUM(revenue) AS total_revenue,
        AVG(revenue) AS avg_daily_revenue,
        MAX(sale_date) AS last_sale_date
    FROM temp_daily_sales
    GROUP BY product_id;

    -- Step 4: Create final materialized table
    CREATE OR REPLACE TABLE `project.dataset.product_performance_materialized` AS
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        p.price,
        ps.total_units_sold,
        ps.total_revenue,
        ps.avg_daily_revenue,
        ps.last_sale_date,
        ROUND(ps.total_revenue / NULLIF(ps.total_units_sold, 0), 2) AS revenue_per_unit,
        DATE_DIFF(CURRENT_DATE(), ps.last_sale_date, DAY) AS days_since_last_sale,
        CURRENT_TIMESTAMP() AS refreshed_at
    FROM `project.dataset.products` p
    LEFT OUTER JOIN temp_product_summary ps
        ON p.product_id = ps.product_id
    WHERE p.active = TRUE;

    -- Step 5: Create trend detail table
    CREATE OR REPLACE TABLE `project.dataset.product_trends_materialized` AS
    SELECT
        pt.product_id,
        p.product_name,
        pt.sale_date,
        pt.units_sold,
        pt.revenue,
        ROUND(pt.revenue_7day_ma, 2) AS revenue_7day_moving_avg,
        ROUND(pt.revenue_30day_ma, 2) AS revenue_30day_moving_avg,
        CURRENT_TIMESTAMP() AS refreshed_at
    FROM temp_product_trends pt
    INNER JOIN `project.dataset.products` p
        ON pt.product_id = p.product_id;
END;
```

### Example 3: Cohort Analysis Materialization

```sql
-- Stored procedure for monthly cohort retention
CREATE OR REPLACE PROCEDURE `project.dataset.refresh_cohort_retention`()
BEGIN
    -- Step 1: Identify user cohorts
    CREATE OR REPLACE TEMP TABLE temp_user_cohorts AS
    SELECT
        user_id,
        DATE_TRUNC(created_at, MONTH) AS cohort_month
    FROM `project.dataset.users`
    WHERE created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH);

    -- Step 2: Track monthly activity
    CREATE OR REPLACE TEMP TABLE temp_monthly_activity AS
    SELECT
        o.user_id,
        DATE_TRUNC(o.order_date, MONTH) AS activity_month
    FROM `project.dataset.orders` o
    WHERE o.order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH)
        AND o.status = 'completed'
    GROUP BY o.user_id, activity_month;

    -- Step 3: Calculate cohort sizes
    CREATE OR REPLACE TEMP TABLE temp_cohort_sizes AS
    SELECT
        cohort_month,
        COUNT(DISTINCT user_id) AS cohort_size
    FROM temp_user_cohorts
    GROUP BY cohort_month;

    -- Step 4: Create final retention table
    CREATE OR REPLACE TABLE `project.dataset.cohort_retention_materialized` AS
    SELECT
        c.cohort_month,
        cs.cohort_size,
        a.activity_month,
        DATE_DIFF(a.activity_month, c.cohort_month, MONTH) AS months_since_join,
        COUNT(DISTINCT c.user_id) AS active_users,
        ROUND(COUNT(DISTINCT c.user_id) / cs.cohort_size * 100, 2) AS retention_rate,
        CURRENT_TIMESTAMP() AS refreshed_at
    FROM temp_user_cohorts c
    INNER JOIN temp_monthly_activity a
        ON c.user_id = a.user_id
    INNER JOIN temp_cohort_sizes cs
        ON c.cohort_month = cs.cohort_month
    GROUP BY
        c.cohort_month,
        cs.cohort_size,
        a.activity_month,
        months_since_join
    ORDER BY
        c.cohort_month,
        months_since_join;
END;
```

### Example 4: Multi-Dataset Aggregation

```sql
-- Stored procedure combining data from multiple sources
CREATE OR REPLACE PROCEDURE `project.dataset.refresh_unified_metrics`()
BEGIN
    -- Step 1: Get sales data
    CREATE OR REPLACE TEMP TABLE temp_sales AS
    SELECT
        user_id,
        COUNT(DISTINCT order_id) AS order_count,
        SUM(amount) AS total_sales
    FROM `project.dataset.orders`
    WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
    GROUP BY user_id;

    -- Step 2: Get engagement data from events
    CREATE OR REPLACE TEMP TABLE temp_engagement AS
    SELECT
        user_id,
        COUNT(*) AS event_count,
        COUNT(DISTINCT DATE(event_timestamp)) AS active_days
    FROM `project.dataset.events`
    WHERE event_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
    GROUP BY user_id;

    -- Step 3: Get support tickets
    CREATE OR REPLACE TEMP TABLE temp_support AS
    SELECT
        user_id,
        COUNT(*) AS ticket_count,
        AVG(satisfaction_score) AS avg_satisfaction
    FROM `project.dataset.support_tickets`
    WHERE created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
    GROUP BY user_id;

    -- Step 4: Combine all metrics
    CREATE OR REPLACE TABLE `project.dataset.unified_user_metrics` AS
    SELECT
        u.user_id,
        u.email,
        u.country,
        COALESCE(s.order_count, 0) AS order_count,
        COALESCE(s.total_sales, 0) AS total_sales,
        COALESCE(e.event_count, 0) AS event_count,
        COALESCE(e.active_days, 0) AS active_days,
        COALESCE(sp.ticket_count, 0) AS ticket_count,
        COALESCE(sp.avg_satisfaction, 0) AS avg_satisfaction,
        CASE
            WHEN s.total_sales > 1000 AND sp.avg_satisfaction >= 4.5 THEN 'High Value'
            WHEN sp.ticket_count > 5 AND sp.avg_satisfaction < 3.0 THEN 'At Risk'
            WHEN e.active_days >= 30 THEN 'Highly Engaged'
            ELSE 'Standard'
        END AS user_status,
        CURRENT_TIMESTAMP() AS refreshed_at
    FROM `project.dataset.users` u
    LEFT OUTER JOIN temp_sales s
        ON u.user_id = s.user_id
    LEFT OUTER JOIN temp_engagement e
        ON u.user_id = e.user_id
    LEFT OUTER JOIN temp_support sp
        ON u.user_id = sp.user_id
    WHERE u.active = TRUE;
END;
```

## Orchestration and Scheduling

### BigQuery Scheduled Queries

Use BigQuery Data Transfer Service for scheduling:

```bash
# Create scheduled query using gcloud
gcloud transfer create \
  --display-name="User Metrics Refresh" \
  --schedule="every 1 hours" \
  --data-source=scheduled_query \
  --target-dataset=dataset_name \
  --params='{
    "query": "CALL `project.dataset.refresh_user_metrics`()",
    "destination_table_name_template": "user_metrics_materialized",
    "write_disposition": "WRITE_TRUNCATE"
  }'
```

### Using BigQuery Transfer API

Create scheduled query via API:

```bash
# Using curl with gcloud auth
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  https://bigquerydatatransfer.googleapis.com/v1/projects/PROJECT_ID/transferConfigs \
  -d @schedule_config.json
```

**schedule_config.json**:
```json
{
  "displayName": "Daily User Metrics Refresh",
  "dataSourceId": "scheduled_query",
  "destinationDatasetId": "dataset_name",
  "schedule": "every day 02:00",
  "params": {
    "query": "CALL `project.dataset.refresh_user_metrics`()",
    "destination_table_name_template": "user_metrics_materialized",
    "write_disposition": "WRITE_TRUNCATE",
    "partitioning_field": ""
  }
}
```

### Schedule Formats

Common schedule patterns:

```text
# Hourly
"every 1 hours"
"every 1 hours 15:00"  # At 15 minutes past every hour

# Daily
"every day 02:00"
"every day 14:30"

# Weekly
"every monday 03:00"
"every sunday 01:00"

# Custom intervals
"every 4 hours"
"every 30 minutes"
```

### Using Service Account

Add service account to schedule (requires permissions):

```bash
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  "https://bigquerydatatransfer.googleapis.com/v1/projects/PROJECT_ID/transferConfigs?serviceAccountName=SERVICE_ACCOUNT_EMAIL" \
  -d @schedule_config.json
```

## Best Practices

### 1. Use TEMP Tables for Intermediate Steps

TEMP tables are automatically cleaned up and don't incur storage costs:

```sql
-- ✅ GOOD: Use TEMP for intermediate results
CREATE OR REPLACE TEMP TABLE temp_step1 AS ...
CREATE OR REPLACE TEMP TABLE temp_step2 AS ...

-- ❌ BAD: Creating permanent tables for intermediate steps
CREATE OR REPLACE TABLE `project.dataset.step1` AS ...
CREATE OR REPLACE TABLE `project.dataset.step2` AS ...
```

### 2. Add Refresh Timestamp

Always include when the data was refreshed:

```sql
CREATE OR REPLACE TABLE `project.dataset.materialized_table` AS
SELECT
    *,
    CURRENT_TIMESTAMP() AS refreshed_at
FROM temp_final_data;
```

### 3. Handle Missing Data with COALESCE

```sql
SELECT
    u.user_id,
    COALESCE(metrics.order_count, 0) AS order_count,
    COALESCE(metrics.total_spent, 0) AS total_spent
FROM users u
LEFT OUTER JOIN temp_metrics metrics
    ON u.user_id = metrics.user_id;
```

### 4. Break Complex Procedures into Steps

```sql
-- ✅ GOOD: Clear, sequential steps
CREATE OR REPLACE PROCEDURE refresh_data()
BEGIN
    -- Step 1: Filter source data
    CREATE OR REPLACE TEMP TABLE filtered_data AS ...;

    -- Step 2: Aggregate metrics
    CREATE OR REPLACE TEMP TABLE aggregated AS ...;

    -- Step 3: Join and enrich
    CREATE OR REPLACE TEMP TABLE enriched AS ...;

    -- Step 4: Create final table
    CREATE OR REPLACE TABLE final AS ...;
END;
```

### 5. Add Error Handling

```sql
CREATE OR REPLACE PROCEDURE `project.dataset.refresh_with_logging`()
BEGIN
    DECLARE row_count INT64;

    -- Refresh data
    CREATE OR REPLACE TABLE `project.dataset.target` AS
    SELECT * FROM source;

    -- Log results
    SET row_count = (SELECT COUNT(*) FROM `project.dataset.target`);

    INSERT INTO `project.dataset.refresh_log` (
        table_name,
        refresh_time,
        row_count,
        status
    )
    VALUES (
        'target',
        CURRENT_TIMESTAMP(),
        row_count,
        'SUCCESS'
    );
END;
```

### 6. Partition Large Materialized Tables

```sql
CREATE OR REPLACE TABLE `project.dataset.large_materialized`
PARTITION BY DATE(created_at)
CLUSTER BY user_id, country
AS
SELECT
    *,
    CURRENT_TIMESTAMP() AS refreshed_at
FROM temp_final_data;
```

## Testing Stored Procedures

### Test Locally First

```sql
-- Test each step individually before creating procedure
CREATE OR REPLACE TEMP TABLE temp_test AS
SELECT ...
FROM ...;

-- Verify results
SELECT COUNT(*), MIN(...), MAX(...) FROM temp_test;
```

### Call Procedure Manually

```sql
-- Execute procedure manually to test
CALL `project.dataset.refresh_user_metrics`();

-- Verify results
SELECT COUNT(*), MAX(refreshed_at)
FROM `project.dataset.user_metrics_materialized`;
```

### Monitor Scheduled Runs

```bash
# List transfer runs
gcloud transfer runs list \
  --transfer-config=CONFIG_NAME \
  --limit=10

# Get specific run details
gcloud transfer runs describe RUN_ID \
  --transfer-config=CONFIG_NAME
```
