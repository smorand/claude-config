# SQL Coding Rules & Optimization

Complete SQL standards and best practices for BigQuery in BTDP environment.

## Format Standards

### UPPERCASE Keywords (MANDATORY)

All SQL keywords MUST be uppercase:

```sql
-- ✅ CORRECT
SELECT
    user_id,
    email,
    DATE(created_at) AS registration_date,
    COUNT(*) OVER (PARTITION BY country) AS country_users
FROM `project.dataset.users`
WHERE created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
    AND active = TRUE
GROUP BY user_id, email, registration_date
HAVING COUNT(*) > 1
ORDER BY user_id
LIMIT 100;

-- ❌ INCORRECT - Lowercase keywords
select user_id, email
from project.dataset.users
where active = true
order by user_id;
```

**Keywords include**: SELECT, FROM, WHERE, JOIN, ON, GROUP BY, HAVING, ORDER BY, LIMIT, WITH, AS, CASE, WHEN, THEN, ELSE, END, AND, OR, NOT, IN, EXISTS, BETWEEN, LIKE, IS, NULL, TRUE, FALSE, DISTINCT, ALL, UNION, INTERSECT, EXCEPT, CREATE, INSERT, UPDATE, DELETE, MERGE, INTO, VALUES, SET, etc.

### Indentation and Formatting

**Standard indentation**: 4 spaces (not tabs)

```sql
-- ✅ CORRECT formatting
SELECT
    column1,
    column2,
    CASE
        WHEN condition1 THEN 'value1'
        WHEN condition2 THEN 'value2'
        ELSE 'default'
    END AS category
FROM table_name
WHERE condition = TRUE
ORDER BY column1;

-- Multi-line conditions
WHERE
    condition1 = TRUE
    AND condition2 IS NOT NULL
    AND condition3 IN ('A', 'B', 'C')
    AND (
        condition4 > 100
        OR condition5 < 50
    )
```

### JOIN Syntax (MANDATORY)

**Always use explicit JOIN keywords** - Never use implicit comma joins for tables:

```sql
-- ✅ CORRECT: Explicit join types
SELECT
    u.user_id,
    u.email,
    o.order_id,
    p.product_name
FROM `project.dataset.users` u
INNER JOIN `project.dataset.orders` o
    ON u.user_id = o.user_id
LEFT OUTER JOIN `project.dataset.products` p
    ON o.product_id = p.product_id
WHERE u.active = TRUE;

-- ✅ CORRECT: Comma join ONLY for UNNEST
SELECT
    user_id,
    tag
FROM `project.dataset.users`,
UNNEST(tags) AS tag;

-- ❌ INCORRECT: Comma join for tables
SELECT u.user_id, o.order_id
FROM users u, orders o
WHERE u.user_id = o.user_id;

-- ❌ INCORRECT: Abbreviated joins
SELECT *
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id;  -- Missing OUTER keyword
```

**Required JOIN keywords**:
- `INNER JOIN` - Returns matching rows only
- `LEFT OUTER JOIN` - All left rows + matching right
- `RIGHT OUTER JOIN` - All right rows + matching left
- `FULL OUTER JOIN` - All rows from both sides
- `CROSS JOIN` - Cartesian product

### SELECT Statement Rules

**NEVER use SELECT *** - Always specify columns explicitly:

```sql
-- ✅ CORRECT: Explicit columns
SELECT
    user_id,
    email,
    first_name,
    last_name,
    created_at
FROM `project.dataset.users`;

-- ✅ CORRECT: With table aliases
SELECT
    u.user_id,
    u.email,
    o.order_id,
    o.amount
FROM `project.dataset.users` u
INNER JOIN `project.dataset.orders` o
    ON u.user_id = o.user_id;

-- ❌ INCORRECT: SELECT *
SELECT * FROM `project.dataset.users`;

-- ❌ INCORRECT: Even with WHERE clause
SELECT * FROM users WHERE active = TRUE;
```

**Exception**: SELECT * allowed ONLY in subqueries for EXCEPT/EXCEPT DISTINCT:

```sql
-- ✅ ALLOWED: For finding differences
SELECT * FROM new_data
EXCEPT DISTINCT
SELECT * FROM old_data;
```

## Optimization Best Practices

### 1. Use CTEs for Complex Queries

Break complex queries into readable, optimized steps:

```sql
-- ✅ CORRECT: Clear, maintainable CTEs
WITH active_users AS (
    SELECT
        user_id,
        email,
        country,
        created_at
    FROM `project.dataset.users`
    WHERE active = TRUE
        AND created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY)
),
user_orders AS (
    SELECT
        user_id,
        COUNT(DISTINCT order_id) AS order_count,
        SUM(amount) AS total_amount,
        MAX(order_date) AS last_order_date
    FROM `project.dataset.orders`
    WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY)
        AND status = 'completed'
    GROUP BY user_id
)
SELECT
    u.user_id,
    u.email,
    u.country,
    COALESCE(o.order_count, 0) AS order_count,
    COALESCE(o.total_amount, 0) AS total_amount,
    o.last_order_date
FROM active_users u
LEFT OUTER JOIN user_orders o
    ON u.user_id = o.user_id
ORDER BY total_amount DESC;
```

### 2. Filter Early

Apply filters as early as possible to reduce data volume:

```sql
-- ✅ CORRECT: Filter in CTEs
WITH recent_orders AS (
    SELECT
        order_id,
        user_id,
        amount
    FROM `project.dataset.orders`
    WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)  -- Filter early
        AND status = 'completed'
)
SELECT
    user_id,
    COUNT(*) AS order_count
FROM recent_orders
GROUP BY user_id;

-- ❌ LESS EFFICIENT: Filter after processing
WITH all_orders AS (
    SELECT
        order_id,
        user_id,
        amount,
        order_date,
        status
    FROM `project.dataset.orders`  -- Processes all data
)
SELECT
    user_id,
    COUNT(*) AS order_count
FROM all_orders
WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
    AND status = 'completed'
GROUP BY user_id;
```

### 3. Pre-Aggregate Before Joins

Reduce data volume before joining tables:

```sql
-- ✅ CORRECT: Aggregate first, then join
WITH order_summary AS (
    SELECT
        user_id,
        COUNT(*) AS order_count,
        SUM(amount) AS total_spent
    FROM `project.dataset.orders`
    WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
    GROUP BY user_id  -- Reduce to one row per user
)
SELECT
    u.user_id,
    u.email,
    COALESCE(s.order_count, 0) AS order_count,
    COALESCE(s.total_spent, 0) AS total_spent
FROM `project.dataset.users` u
LEFT OUTER JOIN order_summary s
    ON u.user_id = s.user_id;

-- ❌ LESS EFFICIENT: Join then aggregate
SELECT
    u.user_id,
    u.email,
    COUNT(o.order_id) AS order_count,
    SUM(o.amount) AS total_spent
FROM `project.dataset.users` u
LEFT OUTER JOIN `project.dataset.orders` o
    ON u.user_id = o.user_id
    AND o.order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
GROUP BY u.user_id, u.email;
```

### 4. Optimal Join Order

Start with the largest table for better performance:

```sql
-- ✅ CORRECT: Largest table first
SELECT
    o.order_id,
    u.email,
    p.product_name
FROM `project.dataset.orders` o  -- Largest table
INNER JOIN `project.dataset.users` u  -- Medium table
    ON o.user_id = u.user_id
INNER JOIN `project.dataset.products` p  -- Smallest table
    ON o.product_id = p.product_id;
```

### 5. Partition and Cluster Awareness

Leverage table partitioning and clustering:

```sql
-- ✅ CORRECT: Filter on partition column
SELECT
    user_id,
    event_name,
    event_timestamp
FROM `project.dataset.events`
WHERE DATE(event_timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)  -- Partition filter
    AND user_id = '12345';  -- Cluster filter

-- ❌ LESS EFFICIENT: Missing partition filter
SELECT
    user_id,
    event_name,
    event_timestamp
FROM `project.dataset.events`
WHERE user_id = '12345';  -- Scans all partitions
```

### 6. Avoid Cartesian Products

Always use proper JOIN conditions:

```sql
-- ✅ CORRECT: Proper join condition
SELECT
    u.user_id,
    o.order_id
FROM `project.dataset.users` u
INNER JOIN `project.dataset.orders` o
    ON u.user_id = o.user_id;

-- ❌ INCORRECT: Cartesian product
SELECT
    u.user_id,
    o.order_id
FROM `project.dataset.users` u
CROSS JOIN `project.dataset.orders` o;  -- Every user matched with every order
```

### 7. Use ARRAY_AGG Efficiently

When aggregating arrays, limit size to avoid memory issues:

```sql
-- ✅ CORRECT: Limited array aggregation
SELECT
    user_id,
    ARRAY_AGG(order_id ORDER BY order_date DESC LIMIT 10) AS recent_orders
FROM `project.dataset.orders`
GROUP BY user_id;

-- ⚠️ RISKY: Unlimited array
SELECT
    user_id,
    ARRAY_AGG(order_id) AS all_orders  -- Could be huge
FROM `project.dataset.orders`
GROUP BY user_id;
```

## Naming Conventions

### Table and Column Aliases

```sql
-- ✅ CORRECT: Clear, meaningful aliases
SELECT
    u.user_id,
    u.email,
    os.order_count,
    os.total_amount
FROM `project.dataset.users` u
INNER JOIN order_summary os
    ON u.user_id = os.user_id;

-- ❌ UNCLEAR: Single letter aliases (except for simple queries)
SELECT
    a.user_id,
    b.order_count
FROM users a
INNER JOIN orders b ON a.id = b.user_id;
```

### Column Names

```sql
-- ✅ CORRECT: Descriptive names with proper aliases
SELECT
    user_id,
    first_name,
    last_name,
    CONCAT(first_name, ' ', last_name) AS full_name,
    DATE_DIFF(CURRENT_DATE(), created_at, DAY) AS account_age_days
FROM `project.dataset.users`;
```

## Comments

Use comments for complex logic:

```sql
-- Calculate user lifetime value with 90-day recency filter
WITH recent_active_users AS (
    SELECT
        user_id,
        email,
        country
    FROM `project.dataset.users`
    WHERE active = TRUE
        AND last_login_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
),
-- Aggregate all completed orders in the last year
user_order_summary AS (
    SELECT
        user_id,
        COUNT(DISTINCT order_id) AS order_count,
        SUM(amount) AS total_spent,
        AVG(amount) AS avg_order_value,
        MAX(order_date) AS last_order_date
    FROM `project.dataset.orders`
    WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY)
        AND status = 'completed'
    GROUP BY user_id
)
SELECT
    u.user_id,
    u.email,
    u.country,
    COALESCE(s.order_count, 0) AS order_count,
    COALESCE(s.total_spent, 0) AS lifetime_value,
    COALESCE(s.avg_order_value, 0) AS avg_order_value,
    s.last_order_date
FROM recent_active_users u
LEFT OUTER JOIN user_order_summary s
    ON u.user_id = s.user_id
ORDER BY lifetime_value DESC;
```

## Query Validation

### Dry Run for Syntax

```bash
# Validate syntax before execution
bq query --dry_run --use_legacy_sql=false \
    "SELECT user_id, email FROM \`project.dataset.users\` LIMIT 10"
```

### Cost Estimation

```bash
# Check bytes processed
bq query --dry_run --use_legacy_sql=false --format=json \
    "SELECT * FROM \`project.dataset.large_table\`" | \
    jq '.statistics.query.totalBytesProcessed'

# Human-readable format
bq query --dry_run --use_legacy_sql=false \
    "SELECT user_id FROM \`project.dataset.users\`"
# Output: Query will process X bytes
```

## Performance Checklist

Before running a query, verify:

- [ ] All SQL keywords are UPPERCASE
- [ ] Explicit JOIN keywords used (INNER, LEFT OUTER, etc.)
- [ ] No SELECT * statements
- [ ] Filters applied early in CTEs
- [ ] Pre-aggregation before joins where possible
- [ ] Partition columns used in WHERE clauses
- [ ] No unnecessary Cartesian products
- [ ] Array aggregations have limits
- [ ] Dry run executed for cost estimation
- [ ] Complex logic documented with comments
