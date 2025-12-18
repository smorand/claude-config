# SQL Fallback Queries

Use SQL fallbacks when RAG/MCP tools fail or need complex filtering.

**Exploration Project:** `oa-data-btdpexploration-np`

**SDDS Project:** `itg-btdppublished-gbl-ww-pd`

---

## Execute Query

```python
mcp__mcprelay__sdds_execute_query(
    sql_query="<sql>",
    project_id=None,    # Optional: defaults to exploration project
    limit=100,          # Max results (default: 100)
    offset=None         # Pagination offset
)
```

**Note:** The tool applies LIMIT and OFFSET automatically. Don't include them in your SQL.

---

## Repositories

**Table:** `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.repositories_v1`

```sql
SELECT
    repository_name,
    repository_description,
    repository_url,
    primary_language,
    topics,
    visibility,
    is_archived,
    default_branch,
    created_at,
    updated_at,
    pushed_at,
    stargazers_count,
    forks_count,
    size
FROM `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.repositories_v1`
WHERE REGEXP_CONTAINS(LOWER(repository_name), r'<pattern>')
   OR REGEXP_CONTAINS(LOWER(repository_description), r'<pattern>')
ORDER BY updated_at DESC
```

**Examples:**
```sql
-- BTDP framework repositories
WHERE REGEXP_CONTAINS(repository_name, r'btdp.*framework')

-- FastAPI repositories
WHERE REGEXP_CONTAINS(repository_name, r'.*(fastapi|api).*')
  AND primary_language = 'Python'

-- Active repositories (not archived)
WHERE is_archived = false
  AND REGEXP_CONTAINS(repository_name, r'btdp.*')
ORDER BY updated_at DESC

-- Popular repositories
WHERE stargazers_count > 5
  AND NOT is_archived
ORDER BY stargazers_count DESC

-- Recent repositories
WHERE created_at >= TIMESTAMP('2024-01-01')
ORDER BY created_at DESC
```

---

## GCP Projects

**Table:** `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.projects_v3`

```sql
SELECT
    project_id,
    project_name,
    project_number,
    lifecycle_state,
    create_time,
    labels
FROM `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.projects_v3`
WHERE REGEXP_CONTAINS(project_id, r'<pattern>')
ORDER BY create_time DESC
```

**Examples:**
```sql
-- All BTDP projects
WHERE REGEXP_CONTAINS(project_id, r'.*btdp.*')

-- Production projects
WHERE REGEXP_CONTAINS(project_id, r'.*-pd$')

-- Exploration/sandbox projects
WHERE REGEXP_CONTAINS(project_id, r'.*(exploration|sandbox).*')

-- Specific environment
WHERE REGEXP_CONTAINS(project_id, r'.*-(dv|qa|np|pd)$')

-- Active projects only
WHERE lifecycle_state = 'ACTIVE'
  AND REGEXP_CONTAINS(project_id, r'oa-data.*')

-- Projects with labels
SELECT
    project_id,
    label.key AS label_key,
    label.value AS label_value
FROM `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.projects_v3`,
UNNEST(labels) AS label
WHERE label.key = 'environment'
  AND label.value = 'pd'
```

---

## BigQuery Datasets

**Table:** `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.datasets_v1`

```sql
SELECT
    project_id,
    dataset_id,
    location,
    creation_time,
    last_modified_time,
    description,
    labels
FROM `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.datasets_v1`
WHERE REGEXP_CONTAINS(dataset_id, r'<pattern>')
ORDER BY creation_time DESC
```

**Examples:**
```sql
-- BTDP datasets
WHERE REGEXP_CONTAINS(dataset_id, r'^btdp_ds.*')

-- Production datasets
WHERE REGEXP_CONTAINS(dataset_id, r'.*_pd$')

-- Specific domain
WHERE REGEXP_CONTAINS(dataset_id, r'btdp_ds_c1_054.*')  -- Agile domain

-- Recently modified
WHERE last_modified_time >= TIMESTAMP('2024-01-01')
ORDER BY last_modified_time DESC

-- EU location only
WHERE location = 'EU'
  AND REGEXP_CONTAINS(dataset_id, r'btdp.*')
```

---

## BigQuery Tables

**Table:** `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.tables_v2`

```sql
SELECT
    project_id,
    dataset_id,
    table_id,
    table_type,
    creation_time,
    row_count,
    size_bytes,
    description,
    labels
FROM `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.tables_v2`
WHERE REGEXP_CONTAINS(table_id, r'<pattern>')
ORDER BY creation_time DESC
```

**Examples:**
```sql
-- Find story tables
WHERE REGEXP_CONTAINS(table_id, r'.*story.*')

-- Find version 2+ tables
WHERE REGEXP_CONTAINS(table_id, r'.*_v[2-9]$')

-- Production tables only
WHERE REGEXP_CONTAINS(dataset_id, r'.*_pd$')

-- Large tables (> 1GB)
WHERE size_bytes > 1000000000
ORDER BY size_bytes DESC

-- Recently created tables
WHERE creation_time >= TIMESTAMP('2024-01-01')
ORDER BY creation_time DESC

-- Exclude snapshots and temp tables
WHERE NOT REGEXP_CONTAINS(table_id, r'.*(snapshot|backup|temp|test).*')
  AND table_type = 'TABLE'

-- Tables in specific dataset
WHERE dataset_id = 'btdp_ds_c1_054_agile_eu_pd'
  AND project_id = 'itg-btdppublished-gbl-ww-pd'

-- High row count tables
WHERE row_count > 1000000
ORDER BY row_count DESC
```

---

## Application Services

**Table:** `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_053_apm_eu_pd.application_service_v1`

```sql
SELECT
    name,
    number,
    business_application,
    it_owner,
    business_owner,
    operational_status,
    service_classification,
    tier,
    hosting_type,
    cloud_service_provider,
    description
FROM `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_053_apm_eu_pd.application_service_v1`
WHERE REGEXP_CONTAINS(LOWER(name), r'<pattern>')
   OR REGEXP_CONTAINS(LOWER(description), r'<pattern>')
ORDER BY tier ASC, name ASC
```

**Examples:**
```sql
-- GCP cloud services
WHERE cloud_service_provider = 'GCP'
  AND hosting_type = 'Cloud'
  AND operational_status = 'Operational'

-- Critical services (Tier 1)
WHERE tier = '1'
  AND operational_status = 'Operational'
ORDER BY name

-- Services by IT owner
WHERE REGEXP_CONTAINS(LOWER(it_owner), r'sebastien.*morand')

-- BTDP services
WHERE REGEXP_CONTAINS(LOWER(name), r'.*btdp.*')
  OR REGEXP_CONTAINS(LOWER(description), r'.*data platform.*')

-- Business services
WHERE service_classification = 'Business'
  AND tier IN ('1', '2')
ORDER BY tier, name
```

---

## User Stories

**Table:** `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_054_agile_eu_pd.story_v1`

```sql
SELECT
    number,
    short_description,
    priority,
    state,
    story_points,
    assignment_group,
    assigned_to,
    product,
    epic,
    sprint,
    theme,
    sys_created_on,
    sys_updated_on,
    sys_created_by,
    sys_updated_by
FROM `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_054_agile_eu_pd.story_v1`
WHERE REGEXP_CONTAINS(LOWER(short_description), r'<pattern>')
ORDER BY sys_updated_on DESC
```

**Examples:**
```sql
-- Active stories (not draft or complete/cancelled)
WHERE state IN ('2', '3', '4', '5')  -- Ready, WIP, Ready for Testing, Testing
ORDER BY priority ASC, sys_updated_on DESC

-- High priority stories in progress
WHERE priority IN ('1', '2')  -- Critical, High
  AND state = '3'  -- Work In Progress
ORDER BY priority, sys_updated_on DESC

-- Stories by assignment group
WHERE REGEXP_CONTAINS(assignment_group, r'.*BTDP.*DATA.*')
  AND state IN ('2', '3', '4')

-- Stories with story points
WHERE story_points BETWEEN 5 AND 13
  AND state = '3'

-- Recent stories
WHERE sys_created_on >= TIMESTAMP('2025-01-01')
ORDER BY sys_created_on DESC

-- Stories by epic
WHERE REGEXP_CONTAINS(epic, r'EPIC0001234')

-- Stories by sprint
WHERE REGEXP_CONTAINS(sprint, r'Sprint 2025-01')

-- Stories by theme
WHERE REGEXP_CONTAINS(LOWER(theme), r'.*data platform.*')
  AND state != '7'  -- Not cancelled
```

---

## Epics

**Table:** `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_054_agile_eu_pd.epic_v1`

```sql
SELECT
    number,
    short_description,
    state,
    priority,
    product,
    assignment_group,
    theme,
    business_process,
    percent_complete,
    planned_start_date,
    planned_end_date,
    actual_start_date,
    actual_end_date,
    total_story_count,
    rag_status,
    sys_created_on,
    sys_updated_on
FROM `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_054_agile_eu_pd.epic_v1`
WHERE REGEXP_CONTAINS(LOWER(short_description), r'<pattern>')
ORDER BY sys_updated_on DESC
```

**Examples:**
```sql
-- Active epics
WHERE state IN ('In Progress', 'New', 'Planned')
ORDER BY priority ASC, sys_updated_on DESC

-- Epics by completion percentage
WHERE percent_complete BETWEEN 50 AND 90
  AND state = 'In Progress'
ORDER BY percent_complete DESC

-- Epics by product
WHERE REGEXP_CONTAINS(product, r'.*BTDP.*')
  AND state != 'Complete'

-- At-risk epics (Red RAG status)
WHERE rag_status = 'Red'
  AND state = 'In Progress'

-- Epics starting in date range
WHERE planned_start_date >= '2025-01-01'
  AND planned_start_date <= '2025-03-31'

-- Large epics (many stories)
WHERE total_story_count > 20
  AND state = 'In Progress'
ORDER BY total_story_count DESC

-- Epics by assignment group
WHERE REGEXP_CONTAINS(assignment_group, r'.*BTDP.*')
  AND state IN ('New', 'In Progress')
```

---

## Sprints

**Table:** `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_054_agile_eu_pd.sprint_v1`

```sql
SELECT
    number,
    short_description,
    state,
    assignment_group,
    release,
    story_points,
    team_points,
    actual_points,
    planned_start_date,
    planned_end_date,
    actual_start_date,
    actual_end_date,
    sys_created_on,
    sys_updated_on
FROM `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_054_agile_eu_pd.sprint_v1`
WHERE REGEXP_CONTAINS(LOWER(short_description), r'<pattern>')
ORDER BY planned_start_date DESC
```

**Examples:**
```sql
-- Active sprints
WHERE state = 'Active'
ORDER BY planned_end_date ASC

-- Sprints by assignment group
WHERE REGEXP_CONTAINS(assignment_group, r'.*BTDP.*DATA.*')
  AND state IN ('Active', 'Planned')

-- Sprints in date range
WHERE planned_start_date >= '2025-01-01'
  AND planned_end_date <= '2025-12-31'
ORDER BY planned_start_date

-- High velocity sprints
WHERE actual_points > 50
  AND state = 'Complete'
ORDER BY actual_points DESC

-- Sprint performance analysis
SELECT
    number,
    short_description,
    story_points,
    actual_points,
    ROUND(actual_points / story_points * 100, 2) AS completion_rate
FROM `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_054_agile_eu_pd.sprint_v1`
WHERE state = 'Complete'
  AND story_points > 0
ORDER BY completion_rate DESC
```

---

## Enhancements

**Table:** `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_055_itbm_eu_pd.enhancement_v1`

```sql
SELECT
    number,
    short_description,
    state,
    substate,
    priority,
    service,
    product,
    assignment_group,
    assigned_to,
    requester,
    country,
    enhancement_type,
    committee_decision,
    rag_status,
    epic,
    theme,
    sys_created_on,
    sys_updated_on
FROM `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_055_itbm_eu_pd.enhancement_v1`
WHERE REGEXP_CONTAINS(LOWER(short_description), r'<pattern>')
ORDER BY priority ASC, sys_updated_on DESC
```

**Examples:**
```sql
-- Active enhancements
WHERE state IN ('New', 'In Progress', 'Awaiting Decision')
  AND active = 'true'
ORDER BY priority ASC, sys_updated_on DESC

-- Critical enhancements
WHERE priority = 'Critical'
  AND state != 'Closed'
ORDER BY sys_created_on DESC

-- Enhancements by service
WHERE REGEXP_CONTAINS(LOWER(service), r'.*btdp.*data.*')
  AND state = 'In Progress'

-- Approved enhancements
WHERE committee_decision = 'Approved'
  AND state IN ('New', 'In Progress')

-- At-risk enhancements
WHERE rag_status = 'Red'
  AND state = 'In Progress'

-- Enhancements by requester
WHERE REGEXP_CONTAINS(LOWER(requester), r'sebastien.*morand')
  AND state != 'Closed'

-- Recent enhancements
WHERE sys_created_on >= TIMESTAMP('2025-01-01')
ORDER BY sys_created_on DESC
```

---

## Best Practices

1. **Use REGEXP_CONTAINS** for flexible pattern matching
2. **Use LOWER()** for case-insensitive searches
3. **Filter by state/status** to exclude closed items
4. **Order by dates DESC** for recent items
5. **Use BETWEEN** for numeric ranges (story points, sizes)
6. **Exclude test/temp** data with NOT REGEXP_CONTAINS
7. **Use TIMESTAMP()** for date comparisons
8. **Combine filters** for precise results
9. **Use UNNEST** for repeated/array fields (labels)
10. **Let tool apply LIMIT/OFFSET** - don't include in SQL

## Common Patterns

```sql
-- Case-insensitive pattern
WHERE REGEXP_CONTAINS(LOWER(field), r'<pattern>')

-- Exclude patterns
WHERE NOT REGEXP_CONTAINS(field, r'.*(test|temp|snapshot).*')

-- Date range
WHERE date_field >= TIMESTAMP('2025-01-01')
  AND date_field <= TIMESTAMP('2025-12-31')

-- Multiple states
WHERE state IN ('state1', 'state2', 'state3')

-- Numeric range
WHERE numeric_field BETWEEN 10 AND 100

-- Environment suffix
WHERE REGEXP_CONTAINS(id, r'.*-(dv|qa|np|pd)$')

-- Version pattern
WHERE REGEXP_CONTAINS(id, r'.*_v[0-9]+$')

-- Start/end anchors
WHERE REGEXP_CONTAINS(id, r'^prefix.*suffix$')
```
