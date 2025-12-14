# Data Preparation (MERGE Patterns)

Use for: Updating existing tables, ETL workflows, incremental loads, table synchronization.

## When to Use

✅ **Good for**:
- Updating existing tables with new data
- ETL/ELT pipelines
- Incremental data loads
- Table synchronization
- Upsert operations (INSERT + UPDATE)

❌ **Not suitable for**:
- One-time analysis → Use ad-hoc patterns
- Creating new aggregations → Use materialized views
- Simple appends → Use INSERT

## Two Main MERGE Patterns

### Pattern 1: Full Refresh (ON FALSE)

**Use when**: Complete table replacement, reference data, lookup tables, full synchronization.

**Characteristics**:
- Replaces all data in target table
- Deletes rows not in source
- Simple and predictable
- Higher processing cost

### Pattern 2: Incremental Update (ON key match)

**Use when**: Large tables, frequent updates, preserving existing data, delta updates.

**Characteristics**:
- Updates only changed rows
- Inserts only new rows
- Lower processing cost
- Requires primary key logic

## Pattern 1: Full Refresh Examples

### Example 1: Simple Full Refresh

```sql
-- Full table replacement using ON FALSE
MERGE INTO `project.dataset.target_table` t
USING (
    SELECT
        FARM_FINGERPRINT(product_id) AS pk,
        product_id,
        product_name,
        category,
        price,
        active,
        CURRENT_TIMESTAMP() AS last_updated
    FROM `project.dataset.source_products`
    WHERE active = TRUE
) s
ON FALSE  -- Never matches - forces complete refresh
WHEN NOT MATCHED THEN
    INSERT (pk, product_id, product_name, category, price, active, last_updated)
    VALUES (s.pk, s.product_id, s.product_name, s.category, s.price, s.active, s.last_updated)
WHEN NOT MATCHED BY SOURCE THEN
    DELETE;  -- Remove rows that don't exist in source
```

### Example 2: Full Refresh with Transformations

```sql
-- Replace target table with transformed source data
MERGE INTO `project.dataset.customer_summary` t
USING (
    SELECT
        FARM_FINGERPRINT(CAST(user_id AS STRING)) AS pk,
        user_id,
        email,
        country,
        CASE
            WHEN total_orders >= 10 THEN 'VIP'
            WHEN total_orders >= 5 THEN 'Loyal'
            ELSE 'Regular'
        END AS customer_tier,
        total_orders,
        total_spent,
        last_order_date,
        CURRENT_TIMESTAMP() AS refreshed_at
    FROM `project.dataset.customer_metrics_view`
) s
ON FALSE
WHEN NOT MATCHED THEN
    INSERT (pk, user_id, email, country, customer_tier, total_orders, total_spent, last_order_date, refreshed_at)
    VALUES (s.pk, s.user_id, s.email, s.country, s.customer_tier, s.total_orders, s.total_spent, s.last_order_date, s.refreshed_at)
WHEN NOT MATCHED BY SOURCE THEN
    DELETE;
```

### Example 3: Full Refresh with Multiple Sources

```sql
-- Combine multiple sources into target table
MERGE INTO `project.dataset.unified_products` t
USING (
    -- Union data from multiple sources
    SELECT
        FARM_FINGERPRINT(CONCAT('web_', CAST(product_id AS STRING))) AS pk,
        product_id,
        product_name,
        category,
        price,
        'web' AS source_system,
        CURRENT_TIMESTAMP() AS last_updated
    FROM `project.dataset.web_products`

    UNION ALL

    SELECT
        FARM_FINGERPRINT(CONCAT('mobile_', CAST(product_id AS STRING))) AS pk,
        product_id,
        product_name,
        category,
        price,
        'mobile' AS source_system,
        CURRENT_TIMESTAMP() AS last_updated
    FROM `project.dataset.mobile_products`

    UNION ALL

    SELECT
        FARM_FINGERPRINT(CONCAT('pos_', CAST(product_id AS STRING))) AS pk,
        product_id,
        product_name,
        category,
        price,
        'pos' AS source_system,
        CURRENT_TIMESTAMP() AS last_updated
    FROM `project.dataset.pos_products`
) s
ON FALSE
WHEN NOT MATCHED THEN
    INSERT (pk, product_id, product_name, category, price, source_system, last_updated)
    VALUES (s.pk, s.product_id, s.product_name, s.category, s.price, s.source_system, s.last_updated)
WHEN NOT MATCHED BY SOURCE THEN
    DELETE;
```

## Pattern 2: Incremental Update Examples

### Example 1: Simple Incremental Update

```sql
-- Update only changed rows, insert new ones
MERGE INTO `project.dataset.target_table` t
USING (
    SELECT
        FARM_FINGERPRINT(product_id) AS pk,
        product_id,
        product_name,
        category,
        price,
        active,
        updated_at
    FROM `project.dataset.source_products`
    WHERE updated_at >= (
        SELECT COALESCE(MAX(updated_at), TIMESTAMP('1970-01-01'))
        FROM `project.dataset.target_table`
    )
) s
ON t.pk = s.pk  -- Match on primary key
WHEN MATCHED AND s.updated_at > t.updated_at THEN
    UPDATE SET
        product_name = s.product_name,
        category = s.category,
        price = s.price,
        active = s.active,
        updated_at = s.updated_at
WHEN NOT MATCHED THEN
    INSERT (pk, product_id, product_name, category, price, active, updated_at)
    VALUES (s.pk, s.product_id, s.product_name, s.category, s.price, s.active, s.updated_at);
```

### Example 2: Incremental with Soft Deletes

```sql
-- Handle soft deletes in incremental updates
MERGE INTO `project.dataset.users` t
USING (
    SELECT
        FARM_FINGERPRINT(CAST(user_id AS STRING)) AS pk,
        user_id,
        email,
        first_name,
        last_name,
        active,
        deleted_at,
        updated_at
    FROM `project.dataset.source_users`
    WHERE updated_at >= (
        SELECT COALESCE(MAX(updated_at), TIMESTAMP('1970-01-01'))
        FROM `project.dataset.users`
    )
) s
ON t.pk = s.pk
WHEN MATCHED AND s.updated_at > t.updated_at THEN
    UPDATE SET
        email = s.email,
        first_name = s.first_name,
        last_name = s.last_name,
        active = s.active,
        deleted_at = s.deleted_at,  -- Handle soft delete
        updated_at = s.updated_at
WHEN NOT MATCHED THEN
    INSERT (pk, user_id, email, first_name, last_name, active, deleted_at, updated_at)
    VALUES (s.pk, s.user_id, s.email, s.first_name, s.last_name, s.active, s.deleted_at, s.updated_at);
```

### Example 3: Incremental with Change Tracking

```sql
-- Track what changed in each update
MERGE INTO `project.dataset.product_inventory` t
USING (
    SELECT
        FARM_FINGERPRINT(CONCAT(location_id, '_', product_id)) AS pk,
        location_id,
        product_id,
        quantity,
        last_restock_date,
        CURRENT_TIMESTAMP() AS updated_at
    FROM `project.dataset.source_inventory`
    WHERE last_restock_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
) s
ON t.pk = s.pk
WHEN MATCHED AND (
    t.quantity != s.quantity
    OR t.last_restock_date != s.last_restock_date
) THEN
    UPDATE SET
        quantity = s.quantity,
        last_restock_date = s.last_restock_date,
        previous_quantity = t.quantity,  -- Track previous value
        quantity_change = s.quantity - t.quantity,  -- Calculate change
        change_count = t.change_count + 1,  -- Increment counter
        updated_at = s.updated_at
WHEN NOT MATCHED THEN
    INSERT (pk, location_id, product_id, quantity, last_restock_date, previous_quantity, quantity_change, change_count, updated_at)
    VALUES (s.pk, s.location_id, s.product_id, s.quantity, s.last_restock_date, 0, s.quantity, 1, s.updated_at);
```

### Example 4: Daily Partition Incremental Load

```sql
-- Incremental load for partitioned table
MERGE INTO `project.dataset.daily_events` t
USING (
    SELECT
        FARM_FINGERPRINT(event_id) AS pk,
        event_id,
        user_id,
        event_name,
        event_timestamp,
        DATE(event_timestamp) AS event_date,
        properties
    FROM `project.dataset.source_events`
    WHERE DATE(event_timestamp) = CURRENT_DATE()  -- Today's data only
) s
ON t.pk = s.pk
    AND t.event_date = s.event_date  -- Match on partition key
WHEN MATCHED THEN
    UPDATE SET
        user_id = s.user_id,
        event_name = s.event_name,
        event_timestamp = s.event_timestamp,
        properties = s.properties
WHEN NOT MATCHED THEN
    INSERT (pk, event_id, user_id, event_name, event_timestamp, event_date, properties)
    VALUES (s.pk, s.event_id, s.user_id, s.event_name, s.event_timestamp, s.event_date, s.properties);
```

## Advanced MERGE Patterns

### Pattern 3: Conditional Updates

```sql
-- Update only when certain conditions are met
MERGE INTO `project.dataset.product_prices` t
USING (
    SELECT
        FARM_FINGERPRINT(product_id) AS pk,
        product_id,
        price,
        effective_date
    FROM `project.dataset.source_prices`
    WHERE effective_date = CURRENT_DATE()
) s
ON t.pk = s.pk
WHEN MATCHED AND (
    s.effective_date >= t.effective_date  -- Only update if newer
    AND ABS(s.price - t.price) > 0.01  -- Only update if price changed significantly
) THEN
    UPDATE SET
        price = s.price,
        effective_date = s.effective_date,
        previous_price = t.price,
        price_change_pct = (s.price - t.price) / t.price * 100,
        updated_at = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN
    INSERT (pk, product_id, price, effective_date, previous_price, price_change_pct, updated_at)
    VALUES (s.pk, s.product_id, s.price, s.effective_date, NULL, 0, CURRENT_TIMESTAMP());
```

### Pattern 4: Multi-Condition MERGE

```sql
-- Different actions based on multiple conditions
MERGE INTO `project.dataset.customer_status` t
USING (
    SELECT
        FARM_FINGERPRINT(CAST(customer_id AS STRING)) AS pk,
        customer_id,
        last_order_date,
        total_orders,
        total_spent,
        CASE
            WHEN last_order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) THEN 'active'
            WHEN last_order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY) THEN 'at_risk'
            ELSE 'churned'
        END AS status
    FROM `project.dataset.customer_orders_summary`
) s
ON t.pk = s.pk
WHEN MATCHED AND s.status = 'active' AND t.status != 'active' THEN
    UPDATE SET
        status = s.status,
        last_order_date = s.last_order_date,
        total_orders = s.total_orders,
        total_spent = s.total_spent,
        reactivation_date = CURRENT_DATE(),  -- Customer reactivated
        updated_at = CURRENT_TIMESTAMP()
WHEN MATCHED AND s.status = 'churned' AND t.status != 'churned' THEN
    UPDATE SET
        status = s.status,
        last_order_date = s.last_order_date,
        total_orders = s.total_orders,
        total_spent = s.total_spent,
        churn_date = CURRENT_DATE(),  -- Customer churned
        updated_at = CURRENT_TIMESTAMP()
WHEN MATCHED THEN
    UPDATE SET
        status = s.status,
        last_order_date = s.last_order_date,
        total_orders = s.total_orders,
        total_spent = s.total_spent,
        updated_at = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN
    INSERT (pk, customer_id, status, last_order_date, total_orders, total_spent, reactivation_date, churn_date, updated_at)
    VALUES (s.pk, s.customer_id, s.status, s.last_order_date, s.total_orders, s.total_spent, NULL, NULL, CURRENT_TIMESTAMP());
```

## Primary Key Generation

### Using FARM_FINGERPRINT

Best practice for generating consistent primary keys:

```sql
-- Single column key
FARM_FINGERPRINT(product_id)

-- Composite key
FARM_FINGERPRINT(CONCAT(user_id, '_', order_id))

-- Multi-column composite key
FARM_FINGERPRINT(CONCAT(
    CAST(location_id AS STRING), '_',
    CAST(product_id AS STRING), '_',
    CAST(DATE(timestamp) AS STRING)
))
```

### Alternative: GENERATE_UUID

```sql
-- Generate unique ID (not deterministic)
GENERATE_UUID()

-- Use with COALESCE to preserve existing IDs
COALESCE(existing_id, GENERATE_UUID())
```

## Best Practices

### 1. Always Use Primary Key (pk)

```sql
-- ✅ CORRECT: Explicit pk column
SELECT
    FARM_FINGERPRINT(key_field) AS pk,
    key_field,
    data_fields
FROM source;

-- ❌ INCORRECT: Matching on business key directly
ON t.key_field = s.key_field  -- Less efficient
```

### 2. Filter Source Data

```sql
-- ✅ GOOD: Only process new/changed data
SELECT *
FROM source
WHERE updated_at >= (
    SELECT COALESCE(MAX(updated_at), TIMESTAMP('1970-01-01'))
    FROM target
);

-- ❌ BAD: Processing all source data
SELECT * FROM source;
```

### 3. Add Timestamps

```sql
-- Always track when data was updated
SELECT
    *,
    CURRENT_TIMESTAMP() AS updated_at,
    CURRENT_TIMESTAMP() AS processed_at
FROM source;
```

### 4. Test MERGE Before Running

```sql
-- First: Count what will be affected
SELECT
    COUNT(*) AS total_source_rows,
    COUNT(CASE WHEN pk IN (SELECT pk FROM target) THEN 1 END) AS will_update,
    COUNT(CASE WHEN pk NOT IN (SELECT pk FROM target) THEN 1 END) AS will_insert
FROM source_query;
```

### 5. Use Transaction for Safety

```sql
-- Wrap MERGE in transaction for rollback capability
BEGIN TRANSACTION;

MERGE INTO target t
USING source s
ON t.pk = s.pk
WHEN MATCHED THEN UPDATE SET ...
WHEN NOT MATCHED THEN INSERT ...;

-- Verify results
SELECT COUNT(*) FROM target WHERE updated_at = CURRENT_TIMESTAMP();

-- If good: COMMIT TRANSACTION;
-- If bad: ROLLBACK TRANSACTION;
```

### 6. Handle NULL Keys

```sql
-- Ensure NULL keys don't cause issues
SELECT
    FARM_FINGERPRINT(COALESCE(key_field, 'NULL_KEY')) AS pk,
    key_field,
    data_fields
FROM source
WHERE key_field IS NOT NULL;  -- Or handle NULLs explicitly
```

## Common Patterns by Use Case

### Reference Data Updates
→ Use **Full Refresh (ON FALSE)**

### Transaction Log Loading
→ Use **Incremental (ON pk = pk)** with timestamp filter

### Dimension Table (SCD Type 1)
→ Use **Incremental (ON pk = pk)** with UPDATE SET

### Daily Partition Load
→ Use **Incremental (ON pk = pk AND partition_key = partition_key)**

### Multi-Source Consolidation
→ Use **Full Refresh (ON FALSE)** with UNION ALL

## Monitoring MERGE Operations

### Check Affected Rows

```sql
-- After MERGE, check statistics
SELECT
    COUNT(*) AS total_rows,
    COUNT(CASE WHEN updated_at = CURRENT_TIMESTAMP() THEN 1 END) AS recently_updated,
    MAX(updated_at) AS last_update
FROM target_table;
```

### Compare Before/After

```sql
-- Before MERGE
CREATE OR REPLACE TEMP TABLE before_counts AS
SELECT COUNT(*) AS row_count FROM target;

-- Run MERGE
MERGE INTO target ...;

-- After MERGE
SELECT
    b.row_count AS before_count,
    (SELECT COUNT(*) FROM target) AS after_count,
    (SELECT COUNT(*) FROM target) - b.row_count AS rows_added
FROM before_counts b;
```

## Error Handling

### Validate Source Data

```sql
-- Check for duplicates in source
SELECT
    key_field,
    COUNT(*) AS dup_count
FROM source
GROUP BY key_field
HAVING COUNT(*) > 1;

-- Check for NULL keys
SELECT COUNT(*)
FROM source
WHERE key_field IS NULL;
```

### Dry Run Test

```sql
-- Test MERGE logic without actually updating
CREATE OR REPLACE TEMP TABLE merge_preview AS
SELECT
    CASE
        WHEN s.pk IN (SELECT pk FROM target) THEN 'UPDATE'
        ELSE 'INSERT'
    END AS action,
    s.*
FROM source s;

-- Review what would happen
SELECT action, COUNT(*)
FROM merge_preview
GROUP BY action;
```
