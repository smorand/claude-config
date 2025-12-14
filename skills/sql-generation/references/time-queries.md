# Time-Based Queries

Dynamic date and time handling in BigQuery - NEVER hardcode dates.

## Core Rule

**NEVER hardcode dates** for time-based queries. Always use dynamic date functions that calculate relative to CURRENT_DATE(), CURRENT_DATETIME(), or CURRENT_TIMESTAMP().

## Why Dynamic Dates?

### ❌ Problems with Hardcoded Dates

```sql
-- BAD: Hardcoded dates
SELECT *
FROM orders
WHERE order_date >= '2024-01-01'
    AND order_date < '2024-02-01';

-- Problems:
-- 1. Query becomes outdated immediately
-- 2. Must be manually updated regularly
-- 3. Not reusable across time periods
-- 4. Causes confusion about data freshness
```

### ✅ Benefits of Dynamic Dates

```sql
-- GOOD: Dynamic dates
SELECT *
FROM orders
WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY);

-- Benefits:
-- 1. Always current - no manual updates needed
-- 2. Reusable across any time period
-- 3. Clear intent - "last 30 days"
-- 4. Works in scheduled queries
```

## Date Functions (DATE Type)

### CURRENT_DATE()

Returns current date in UTC timezone:

```sql
-- Get current date
SELECT CURRENT_DATE() AS today;
-- Result: 2024-01-15

-- Last 7 days
SELECT *
FROM orders
WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY);

-- Last 30 days
SELECT *
FROM orders
WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY);

-- Last 90 days
SELECT *
FROM orders
WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY);

-- Last 12 months
SELECT *
FROM orders
WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH);

-- Last year (365 days)
SELECT *
FROM orders
WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY);
```

### DATE_SUB() - Subtract Intervals

```sql
-- Subtract days
DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)

-- Subtract weeks
DATE_SUB(CURRENT_DATE(), INTERVAL 2 WEEK)

-- Subtract months
DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH)

-- Subtract years
DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR)
```

### DATE_ADD() - Add Intervals

```sql
-- Add days (future dates)
DATE_ADD(CURRENT_DATE(), INTERVAL 7 DAY)

-- Next 30 days
SELECT *
FROM scheduled_tasks
WHERE task_date BETWEEN CURRENT_DATE()
    AND DATE_ADD(CURRENT_DATE(), INTERVAL 30 DAY);
```

### DATE_TRUNC() - Truncate to Period

```sql
-- Start of current month
DATE_TRUNC(CURRENT_DATE(), MONTH)

-- Start of current quarter
DATE_TRUNC(CURRENT_DATE(), QUARTER)

-- Start of current year
DATE_TRUNC(CURRENT_DATE(), YEAR)

-- Start of current week (Sunday)
DATE_TRUNC(CURRENT_DATE(), WEEK)

-- Start of current week (Monday)
DATE_TRUNC(CURRENT_DATE(), WEEK(MONDAY))
```

### DATE_DIFF() - Calculate Differences

```sql
-- Days between dates
DATE_DIFF(CURRENT_DATE(), order_date, DAY) AS days_since_order

-- Months between dates
DATE_DIFF(CURRENT_DATE(), created_at, MONTH) AS months_since_creation

-- Years between dates
DATE_DIFF(CURRENT_DATE(), birth_date, YEAR) AS age_years
```

## DateTime Functions (DATETIME Type)

### CURRENT_DATETIME()

Returns current datetime in UTC timezone:

```sql
-- Get current datetime
SELECT CURRENT_DATETIME() AS now;
-- Result: 2024-01-15 14:30:25

-- Last 24 hours
SELECT *
FROM events
WHERE event_datetime >= DATETIME_SUB(CURRENT_DATETIME(), INTERVAL 24 HOUR);

-- Last 7 days
SELECT *
FROM events
WHERE event_datetime >= DATETIME_SUB(CURRENT_DATETIME(), INTERVAL 7 DAY);
```

### DATETIME_SUB() - Subtract Intervals

```sql
-- Subtract hours
DATETIME_SUB(CURRENT_DATETIME(), INTERVAL 2 HOUR)

-- Subtract minutes
DATETIME_SUB(CURRENT_DATETIME(), INTERVAL 30 MINUTE)

-- Subtract days
DATETIME_SUB(CURRENT_DATETIME(), INTERVAL 7 DAY)

-- Last 6 hours
SELECT *
FROM events
WHERE event_datetime >= DATETIME_SUB(CURRENT_DATETIME(), INTERVAL 6 HOUR);
```

### DATETIME_TRUNC() - Truncate to Period

```sql
-- Start of current hour
DATETIME_TRUNC(CURRENT_DATETIME(), HOUR)

-- Start of current day
DATETIME_TRUNC(CURRENT_DATETIME(), DAY)

-- Start of current month
DATETIME_TRUNC(CURRENT_DATETIME(), MONTH)
```

## Timestamp Functions (TIMESTAMP Type)

### CURRENT_TIMESTAMP()

Returns current timestamp with timezone:

```sql
-- Get current timestamp
SELECT CURRENT_TIMESTAMP() AS now;
-- Result: 2024-01-15 14:30:25.123456 UTC

-- Last hour
SELECT *
FROM logs
WHERE log_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR);

-- Last 15 minutes
SELECT *
FROM realtime_events
WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 15 MINUTE);
```

### TIMESTAMP_SUB() - Subtract Intervals

```sql
-- Subtract seconds
TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 SECOND)

-- Subtract minutes
TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 5 MINUTE)

-- Subtract hours
TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR)
```

### TIMESTAMP_TRUNC() - Truncate to Period

```sql
-- Start of current minute
TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), MINUTE)

-- Start of current hour
TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), HOUR)

-- Start of current day
TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), DAY)
```

## Common Time-Based Patterns

### Pattern 1: Last N Days

```sql
-- Last 30 days of orders
SELECT
    order_id,
    user_id,
    order_date,
    amount
FROM `project.dataset.orders`
WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
ORDER BY order_date DESC;
```

### Pattern 2: Current Month

```sql
-- All orders in current month
SELECT
    order_id,
    order_date,
    amount
FROM `project.dataset.orders`
WHERE order_date >= DATE_TRUNC(CURRENT_DATE(), MONTH)
ORDER BY order_date;
```

### Pattern 3: Previous Month

```sql
-- All orders from previous month
SELECT
    order_id,
    order_date,
    amount
FROM `project.dataset.orders`
WHERE order_date >= DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), MONTH)
    AND order_date < DATE_TRUNC(CURRENT_DATE(), MONTH)
ORDER BY order_date;
```

### Pattern 4: Current Quarter

```sql
-- All orders in current quarter
SELECT
    order_id,
    order_date,
    amount
FROM `project.dataset.orders`
WHERE order_date >= DATE_TRUNC(CURRENT_DATE(), QUARTER)
ORDER BY order_date;
```

### Pattern 5: Year-to-Date

```sql
-- All orders from start of year
SELECT
    order_id,
    order_date,
    amount
FROM `project.dataset.orders`
WHERE order_date >= DATE_TRUNC(CURRENT_DATE(), YEAR)
ORDER BY order_date;
```

### Pattern 6: Rolling Window

```sql
-- 7-day rolling average
WITH daily_sales AS (
    SELECT
        DATE(order_date) AS sale_date,
        SUM(amount) AS daily_total
    FROM `project.dataset.orders`
    WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
    GROUP BY sale_date
)
SELECT
    sale_date,
    daily_total,
    AVG(daily_total) OVER (
        ORDER BY sale_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS rolling_7day_avg
FROM daily_sales
ORDER BY sale_date;
```

### Pattern 7: Same Period Last Year

```sql
-- Compare with same period last year
WITH current_period AS (
    SELECT
        SUM(amount) AS current_sales
    FROM `project.dataset.orders`
    WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
),
last_year_period AS (
    SELECT
        SUM(amount) AS last_year_sales
    FROM `project.dataset.orders`
    WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 395 DAY)
        AND order_date < DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY)
)
SELECT
    c.current_sales,
    l.last_year_sales,
    (c.current_sales - l.last_year_sales) / l.last_year_sales * 100 AS growth_pct
FROM current_period c
CROSS JOIN last_year_period l;
```

### Pattern 8: Business Hours Filter

```sql
-- Events during business hours only
SELECT
    event_id,
    event_timestamp
FROM `project.dataset.events`
WHERE event_timestamp >= DATETIME_SUB(CURRENT_DATETIME(), INTERVAL 7 DAY)
    AND EXTRACT(HOUR FROM event_timestamp) BETWEEN 9 AND 17
    AND EXTRACT(DAYOFWEEK FROM event_timestamp) BETWEEN 2 AND 6  -- Monday-Friday
ORDER BY event_timestamp;
```

### Pattern 9: Recent Active Users

```sql
-- Users active in last 7 days
SELECT
    user_id,
    email,
    MAX(last_login) AS most_recent_login,
    DATE_DIFF(CURRENT_DATE(), MAX(DATE(last_login)), DAY) AS days_since_login
FROM `project.dataset.user_activity`
WHERE last_login >= DATETIME_SUB(CURRENT_DATETIME(), INTERVAL 7 DAY)
GROUP BY user_id, email
ORDER BY most_recent_login DESC;
```

### Pattern 10: Time-Based Cohorts

```sql
-- Monthly cohorts with retention
WITH user_cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC(created_at, MONTH) AS cohort_month
    FROM `project.dataset.users`
    WHERE created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH)
),
user_activity AS (
    SELECT
        user_id,
        DATE_TRUNC(activity_date, MONTH) AS activity_month
    FROM `project.dataset.user_activity`
    WHERE activity_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH)
    GROUP BY user_id, activity_month
)
SELECT
    c.cohort_month,
    a.activity_month,
    DATE_DIFF(a.activity_month, c.cohort_month, MONTH) AS months_since_join,
    COUNT(DISTINCT c.user_id) AS active_users
FROM user_cohorts c
INNER JOIN user_activity a
    ON c.user_id = a.user_id
GROUP BY c.cohort_month, a.activity_month, months_since_join
ORDER BY c.cohort_month, months_since_join;
```

## Timezone Handling

### Convert UTC to Specific Timezone

```sql
-- Convert UTC timestamp to Paris timezone
DATETIME(timestamp_field, 'Europe/Paris') AS paris_time

-- Convert UTC to New York timezone
DATETIME(timestamp_field, 'America/New_York') AS ny_time
```

### Filter by Local Time

```sql
-- Orders made during Paris business hours
SELECT *
FROM orders
WHERE EXTRACT(HOUR FROM DATETIME(order_timestamp, 'Europe/Paris')) BETWEEN 9 AND 17;
```

## Date Extraction

### Extract Components

```sql
-- Extract year, month, day
SELECT
    order_date,
    EXTRACT(YEAR FROM order_date) AS year,
    EXTRACT(MONTH FROM order_date) AS month,
    EXTRACT(DAY FROM order_date) AS day,
    EXTRACT(DAYOFWEEK FROM order_date) AS day_of_week,  -- 1=Sunday, 7=Saturday
    EXTRACT(DAYOFYEAR FROM order_date) AS day_of_year,
    EXTRACT(WEEK FROM order_date) AS week_number,
    EXTRACT(QUARTER FROM order_date) AS quarter
FROM orders;
```

### Format Dates for Grouping

```sql
-- Group by year-month
SELECT
    FORMAT_DATE('%Y-%m', order_date) AS year_month,
    COUNT(*) AS order_count
FROM orders
WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH)
GROUP BY year_month
ORDER BY year_month;
```

## Complete Examples

### Example 1: Weekly Performance Report

```sql
-- Performance metrics for last 12 weeks
WITH weekly_metrics AS (
    SELECT
        DATE_TRUNC(order_date, WEEK) AS week_start,
        COUNT(DISTINCT order_id) AS order_count,
        COUNT(DISTINCT user_id) AS unique_customers,
        SUM(amount) AS total_revenue,
        AVG(amount) AS avg_order_value
    FROM `project.dataset.orders`
    WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 84 DAY)
        AND status = 'completed'
    GROUP BY week_start
)
SELECT
    week_start,
    order_count,
    unique_customers,
    total_revenue,
    avg_order_value,
    LAG(total_revenue) OVER (ORDER BY week_start) AS prev_week_revenue,
    (total_revenue - LAG(total_revenue) OVER (ORDER BY week_start)) /
        LAG(total_revenue) OVER (ORDER BY week_start) * 100 AS revenue_growth_pct
FROM weekly_metrics
ORDER BY week_start;
```

### Example 2: User Engagement Trends

```sql
-- Daily active users for last 30 days
SELECT
    DATE(event_timestamp) AS event_date,
    COUNT(DISTINCT user_id) AS daily_active_users,
    COUNT(*) AS total_events,
    AVG(COUNT(*)) OVER (
        ORDER BY DATE(event_timestamp)
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS events_7day_avg
FROM `project.dataset.events`
WHERE event_timestamp >= DATETIME_SUB(CURRENT_DATETIME(), INTERVAL 30 DAY)
GROUP BY event_date
ORDER BY event_date;
```

### Example 3: Abandoned Cart Analysis

```sql
-- Carts abandoned in last 24 hours
SELECT
    cart_id,
    user_id,
    created_at,
    items_count,
    total_value,
    DATETIME_DIFF(CURRENT_DATETIME(), created_at, HOUR) AS hours_abandoned
FROM `project.dataset.shopping_carts`
WHERE status = 'abandoned'
    AND created_at >= DATETIME_SUB(CURRENT_DATETIME(), INTERVAL 24 HOUR)
    AND created_at < DATETIME_SUB(CURRENT_DATETIME(), INTERVAL 1 HOUR)  -- At least 1 hour old
ORDER BY total_value DESC;
```

## Best Practices Summary

✅ **Always Do**:
- Use CURRENT_DATE(), CURRENT_DATETIME(), CURRENT_TIMESTAMP()
- Use DATE_SUB(), DATETIME_SUB(), TIMESTAMP_SUB() for relative dates
- Use DATE_TRUNC() for period starts
- Document time ranges in comments

❌ **Never Do**:
- Hardcode dates like '2024-01-01'
- Use static date ranges
- Forget timezone considerations
- Mix DATE, DATETIME, and TIMESTAMP types without converting

## Quick Reference

| Need | Use This |
|------|----------|
| Last N days | `WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL N DAY)` |
| Current month | `WHERE date >= DATE_TRUNC(CURRENT_DATE(), MONTH)` |
| Last N hours | `WHERE datetime >= DATETIME_SUB(CURRENT_DATETIME(), INTERVAL N HOUR)` |
| Year-to-date | `WHERE date >= DATE_TRUNC(CURRENT_DATE(), YEAR)` |
| Previous month | `WHERE date >= DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), MONTH) AND date < DATE_TRUNC(CURRENT_DATE(), MONTH)` |
| Last N minutes | `WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL N MINUTE)` |
