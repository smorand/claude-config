# Ad-hoc Analysis Patterns

Use for: Quick analysis, one-time queries, exploratory work, data investigation.

## When to Use

✅ **Good for**:
- One-time analysis requests
- Exploratory data analysis
- Quick business questions
- Data validation
- Testing hypotheses

❌ **Not suitable for**:
- Repeated/scheduled queries → Use materialized views
- Updating existing tables → Use data preparation patterns
- Long-running transformations → Use stored procedures

## Pattern: Pure SQL with CTEs

Ad-hoc queries use only WITH clauses (Common Table Expressions) for clarity and organization.

### Basic Structure

```sql
WITH step1 AS (
    -- First transformation
    SELECT ...
    FROM ...
    WHERE ...
),
step2 AS (
    -- Second transformation
    SELECT ...
    FROM step1
    WHERE ...
)
SELECT
    -- Final output
    ...
FROM step1
INNER JOIN step2
    ON ...
ORDER BY ...;
```

## Complete Examples

### Example 1: Customer Segmentation

```sql
-- Segment customers by purchase behavior in last 90 days
WITH active_customers AS (
    SELECT
        user_id,
        email,
        country,
        created_at
    FROM `project.dataset.users`
    WHERE active = TRUE
        AND created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY)
),
purchase_summary AS (
    SELECT
        user_id,
        COUNT(DISTINCT order_id) AS order_count,
        SUM(amount) AS total_spent,
        AVG(amount) AS avg_order_value,
        MAX(order_date) AS last_purchase_date,
        MIN(order_date) AS first_purchase_date
    FROM `project.dataset.orders`
    WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
        AND status = 'completed'
    GROUP BY user_id
),
customer_segments AS (
    SELECT
        user_id,
        order_count,
        total_spent,
        avg_order_value,
        last_purchase_date,
        first_purchase_date,
        CASE
            WHEN order_count >= 10 AND total_spent >= 1000 THEN 'VIP'
            WHEN order_count >= 5 AND total_spent >= 500 THEN 'Loyal'
            WHEN order_count >= 2 THEN 'Regular'
            ELSE 'New'
        END AS segment,
        DATE_DIFF(CURRENT_DATE(), last_purchase_date, DAY) AS days_since_last_purchase
    FROM purchase_summary
)
SELECT
    c.user_id,
    c.email,
    c.country,
    c.created_at,
    s.segment,
    s.order_count,
    s.total_spent,
    s.avg_order_value,
    s.last_purchase_date,
    s.days_since_last_purchase,
    CASE
        WHEN s.days_since_last_purchase > 60 THEN TRUE
        ELSE FALSE
    END AS is_at_risk
FROM active_customers c
INNER JOIN customer_segments s
    ON c.user_id = s.user_id
ORDER BY s.total_spent DESC;
```

### Example 2: Product Performance Analysis

```sql
-- Analyze product performance with category metrics
WITH product_sales AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        p.price,
        COUNT(DISTINCT o.order_id) AS order_count,
        SUM(o.quantity) AS units_sold,
        SUM(o.quantity * o.unit_price) AS revenue
    FROM `project.dataset.products` p
    INNER JOIN `project.dataset.order_items` o
        ON p.product_id = o.product_id
    WHERE o.order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
    GROUP BY
        p.product_id,
        p.product_name,
        p.category,
        p.price
),
category_metrics AS (
    SELECT
        category,
        SUM(revenue) AS category_revenue,
        AVG(revenue) AS avg_product_revenue,
        COUNT(DISTINCT product_id) AS product_count
    FROM product_sales
    GROUP BY category
)
SELECT
    ps.product_id,
    ps.product_name,
    ps.category,
    ps.price,
    ps.order_count,
    ps.units_sold,
    ps.revenue,
    cm.category_revenue,
    cm.product_count AS products_in_category,
    ROUND(ps.revenue / cm.category_revenue * 100, 2) AS pct_of_category_revenue,
    CASE
        WHEN ps.revenue > cm.avg_product_revenue THEN 'Above Average'
        ELSE 'Below Average'
    END AS performance
FROM product_sales ps
INNER JOIN category_metrics cm
    ON ps.category = cm.category
ORDER BY ps.revenue DESC;
```

### Example 3: Cohort Analysis

```sql
-- Monthly cohort retention analysis
WITH user_cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC(created_at, MONTH) AS cohort_month
    FROM `project.dataset.users`
    WHERE created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH)
),
user_activity AS (
    SELECT
        o.user_id,
        DATE_TRUNC(o.order_date, MONTH) AS activity_month
    FROM `project.dataset.orders` o
    WHERE o.order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH)
        AND o.status = 'completed'
    GROUP BY o.user_id, activity_month
),
cohort_activity AS (
    SELECT
        c.cohort_month,
        a.activity_month,
        DATE_DIFF(a.activity_month, c.cohort_month, MONTH) AS months_since_join,
        COUNT(DISTINCT c.user_id) AS active_users
    FROM user_cohorts c
    INNER JOIN user_activity a
        ON c.user_id = a.user_id
    GROUP BY
        c.cohort_month,
        a.activity_month,
        months_since_join
),
cohort_sizes AS (
    SELECT
        cohort_month,
        COUNT(DISTINCT user_id) AS cohort_size
    FROM user_cohorts
    GROUP BY cohort_month
)
SELECT
    ca.cohort_month,
    cs.cohort_size,
    ca.months_since_join,
    ca.active_users,
    ROUND(ca.active_users / cs.cohort_size * 100, 2) AS retention_rate
FROM cohort_activity ca
INNER JOIN cohort_sizes cs
    ON ca.cohort_month = cs.cohort_month
ORDER BY
    ca.cohort_month,
    ca.months_since_join;
```

### Example 4: Time Series Analysis

```sql
-- Daily sales trend with moving averages
WITH daily_sales AS (
    SELECT
        DATE(order_date) AS sale_date,
        COUNT(DISTINCT order_id) AS order_count,
        SUM(amount) AS daily_revenue,
        AVG(amount) AS avg_order_value
    FROM `project.dataset.orders`
    WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
        AND status = 'completed'
    GROUP BY sale_date
),
sales_with_moving_avg AS (
    SELECT
        sale_date,
        order_count,
        daily_revenue,
        avg_order_value,
        AVG(daily_revenue) OVER (
            ORDER BY sale_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS revenue_7day_ma,
        AVG(daily_revenue) OVER (
            ORDER BY sale_date
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ) AS revenue_30day_ma
    FROM daily_sales
)
SELECT
    sale_date,
    order_count,
    daily_revenue,
    avg_order_value,
    ROUND(revenue_7day_ma, 2) AS revenue_7day_moving_avg,
    ROUND(revenue_30day_ma, 2) AS revenue_30day_moving_avg,
    ROUND(
        (daily_revenue - revenue_7day_ma) / revenue_7day_ma * 100,
        2
    ) AS pct_diff_from_7day_avg
FROM sales_with_moving_avg
ORDER BY sale_date;
```

### Example 5: Funnel Analysis

```sql
-- User conversion funnel analysis
WITH funnel_steps AS (
    SELECT
        user_id,
        MAX(CASE WHEN event_name = 'page_view' THEN 1 ELSE 0 END) AS viewed,
        MAX(CASE WHEN event_name = 'add_to_cart' THEN 1 ELSE 0 END) AS added_to_cart,
        MAX(CASE WHEN event_name = 'checkout_start' THEN 1 ELSE 0 END) AS started_checkout,
        MAX(CASE WHEN event_name = 'purchase' THEN 1 ELSE 0 END) AS completed_purchase
    FROM `project.dataset.events`
    WHERE event_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
    GROUP BY user_id
),
funnel_summary AS (
    SELECT
        SUM(viewed) AS total_viewers,
        SUM(added_to_cart) AS total_add_to_cart,
        SUM(started_checkout) AS total_checkout_start,
        SUM(completed_purchase) AS total_purchases
    FROM funnel_steps
)
SELECT
    'Page View' AS step,
    1 AS step_number,
    total_viewers AS users,
    100.0 AS conversion_rate,
    0.0 AS drop_off_rate
FROM funnel_summary
UNION ALL
SELECT
    'Add to Cart' AS step,
    2 AS step_number,
    total_add_to_cart AS users,
    ROUND(total_add_to_cart / total_viewers * 100, 2) AS conversion_rate,
    ROUND((total_viewers - total_add_to_cart) / total_viewers * 100, 2) AS drop_off_rate
FROM funnel_summary
UNION ALL
SELECT
    'Checkout Start' AS step,
    3 AS step_number,
    total_checkout_start AS users,
    ROUND(total_checkout_start / total_viewers * 100, 2) AS conversion_rate,
    ROUND((total_add_to_cart - total_checkout_start) / total_add_to_cart * 100, 2) AS drop_off_rate
FROM funnel_summary
UNION ALL
SELECT
    'Purchase' AS step,
    4 AS step_number,
    total_purchases AS users,
    ROUND(total_purchases / total_viewers * 100, 2) AS conversion_rate,
    ROUND((total_checkout_start - total_purchases) / total_checkout_start * 100, 2) AS drop_off_rate
FROM funnel_summary
ORDER BY step_number;
```

## Best Practices for Ad-hoc Queries

### 1. Name CTEs Descriptively

```sql
-- ✅ GOOD: Clear CTE names
WITH active_users AS (...),
     recent_orders AS (...),
     order_metrics AS (...)

-- ❌ BAD: Unclear names
WITH t1 AS (...),
     temp AS (...),
     data AS (...)
```

### 2. Keep CTEs Focused

Each CTE should have a single, clear purpose:

```sql
-- ✅ GOOD: Each CTE does one thing
WITH filtered_users AS (
    SELECT user_id, email
    FROM users
    WHERE active = TRUE
),
user_orders AS (
    SELECT user_id, COUNT(*) AS order_count
    FROM orders
    GROUP BY user_id
)

-- ❌ BAD: CTE doing too much
WITH everything AS (
    SELECT
        u.user_id,
        u.email,
        COUNT(o.order_id) AS order_count,
        SUM(p.amount) AS total_payments,
        AVG(r.rating) AS avg_rating
    FROM users u
    LEFT OUTER JOIN orders o ON u.user_id = o.user_id
    LEFT OUTER JOIN payments p ON o.order_id = p.order_id
    LEFT OUTER JOIN reviews r ON u.user_id = r.user_id
    GROUP BY u.user_id, u.email
)
```

### 3. Filter Early

Apply WHERE clauses as soon as possible:

```sql
-- ✅ GOOD: Filter in first CTE
WITH recent_orders AS (
    SELECT order_id, user_id, amount
    FROM orders
    WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
)
SELECT user_id, COUNT(*) FROM recent_orders GROUP BY user_id;

-- ❌ LESS EFFICIENT: Filter at the end
WITH all_orders AS (
    SELECT order_id, user_id, amount, order_date
    FROM orders
)
SELECT user_id, COUNT(*)
FROM all_orders
WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY user_id;
```

### 4. Comment Complex Logic

```sql
-- Calculate customer lifetime value with recency weighting
WITH customer_purchases AS (
    -- Get all completed purchases in the last year
    SELECT
        user_id,
        order_id,
        amount,
        order_date,
        -- Weight recent purchases more heavily (exponential decay)
        amount * EXP(-0.1 * DATE_DIFF(CURRENT_DATE(), order_date, DAY) / 30) AS weighted_amount
    FROM orders
    WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY)
        AND status = 'completed'
)
SELECT
    user_id,
    SUM(amount) AS total_ltv,
    SUM(weighted_amount) AS weighted_ltv
FROM customer_purchases
GROUP BY user_id;
```

## Testing Ad-hoc Queries

### 1. Start Small

```sql
-- First: Test with LIMIT
SELECT user_id, email
FROM users
WHERE active = TRUE
LIMIT 10;

-- Then: Add complexity gradually
WITH active_users AS (
    SELECT user_id, email
    FROM users
    WHERE active = TRUE
    LIMIT 100  -- Keep limit during development
)
SELECT ...
```

### 2. Validate Results

```sql
-- Add validation checks
WITH results AS (
    SELECT
        user_id,
        order_count,
        total_spent
    FROM ...
)
SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT user_id) AS unique_users,
    MIN(order_count) AS min_orders,
    MAX(order_count) AS max_orders,
    AVG(total_spent) AS avg_spent,
    SUM(CASE WHEN total_spent < 0 THEN 1 ELSE 0 END) AS negative_amounts
FROM results;
```

### 3. Check Query Cost

```bash
# Dry run to estimate cost
bq query --dry_run --use_legacy_sql=false "
WITH ...
SELECT ...
"
```
