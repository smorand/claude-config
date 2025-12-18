# BigQuery Resources (Datasets & Tables)

## Datasets

### Method 1: RAG Index (smo_dataset_v1)

**Best for:** Quick semantic search

```python
mcp__mcprelay__rag_query_rag(
    index="smo_dataset_v1",
    query="<search_term>",
    limit=10
)
```

**Examples:**
```python
# Find domain datasets
query_rag(index="smo_dataset_v1", query="consumer data domain")

# Find specific dataset
query_rag(index="smo_dataset_v1", query="agile project management")
```

### Method 2: SDDS List Datasets

```python
mcp__mcprelay__sdds_list_datasets(
    project_id=None,   # Filter by project
    limit=100,         # Max results (default: 100)
    offset=None        # Pagination offset
)
```

### Method 3: SDDS Search Datasets

**Best for:** Regexp pattern matching with environment filters

```python
mcp__mcprelay__sdds_search_datasets(
    pattern="<regexp_pattern>",
    project_id=None,         # Optional: filter by project
    environment=None,        # Optional: "dv", "qa", "np", "pd"
    use_not=False,          # If True, returns datasets NOT matching pattern
    limit=100,              # Max results (default: 100)
    offset=None             # Pagination offset
)
```

**Examples:**
```python
# Find all agile datasets
sdds_search_datasets(pattern=".*agile.*")

# Find production datasets only
sdds_search_datasets(pattern=".*", environment="pd", limit=50)

# Find datasets in specific project
sdds_search_datasets(
    pattern="btdp_ds.*",
    project_id="itg-btdppublished-gbl-ww-pd"
)

# Exclude test datasets
sdds_search_datasets(pattern=".*test.*", use_not=True)
```

**Dataset Naming Pattern:**
```
btdp_ds_c{tier}_{domain_id}_{label}_eu_{env}

Examples:
- btdp_ds_c1_0a1_gcpassets_eu_pd
- btdp_ds_c1_054_agile_eu_pd
- btdp_ds_c1_055_itbm_eu_pd
```

---

## Tables

### Method 1: RAG Index (smo_table_v1)

**Best for:** Quick semantic search

```python
mcp__mcprelay__rag_query_rag(
    index="smo_table_v1",
    query="<search_term>",
    limit=10
)
```

**Examples:**
```python
# Find user story tables
query_rag(index="smo_table_v1", query="user stories agile")

# Find enhancement tables
query_rag(index="smo_table_v1", query="enhancements ITBM")
```

### Method 2: SDDS List Tables

```python
mcp__mcprelay__sdds_list_tables(
    project_id=None,   # Filter by project
    dataset_id=None,   # Filter by dataset
    limit=100,
    offset=None
)
```

**Examples:**
```python
# List all tables in a dataset
sdds_list_tables(
    project_id="itg-btdppublished-gbl-ww-pd",
    dataset_id="btdp_ds_c1_054_agile_eu_pd"
)

# List tables in a project
sdds_list_tables(project_id="oa-data-btdpexploration-np", limit=200)
```

### Method 3: SDDS Search Tables

**Best for:** Regexp pattern matching with filters

```python
mcp__mcprelay__sdds_search_tables(
    pattern="<regexp_pattern>",
    project_id=None,         # Optional: filter by project
    dataset_id=None,         # Optional: filter by dataset
    environment=None,        # Optional: "dv", "qa", "np", "pd"
    use_not=False,          # If True, returns tables NOT matching
    limit=100,
    offset=None
)
```

**Examples:**
```python
# Find all story tables
sdds_search_tables(pattern=".*story.*")

# Find version 2 tables
sdds_search_tables(pattern=".*_v[2-9]$")

# Find tables in production only
sdds_search_tables(pattern=".*", environment="pd")

# Find tables in specific dataset
sdds_search_tables(
    pattern=".*",
    dataset_id="btdp_ds_c1_054_agile_eu_pd"
)

# Exclude snapshot tables
sdds_search_tables(pattern=".*snapshot.*", use_not=True)
```

---

## Table Schema

### Get Schema

**Retrieve column information for a table**

```python
mcp__mcprelay__sdds_get_schema(
    project_id="<project_id>",
    dataset_id="<dataset_id>",
    table_id="<table_id>",
    force=False  # Set True to bypass cache and reload from BigQuery
)
```

**Examples:**
```python
# Get story table schema
sdds_get_schema(
    project_id="itg-btdppublished-gbl-ww-pd",
    dataset_id="btdp_ds_c1_054_agile_eu_pd",
    table_id="story_v1"
)

# Force reload schema (bypass cache)
sdds_get_schema(
    project_id="itg-btdppublished-gbl-ww-pd",
    dataset_id="btdp_ds_c1_055_itbm_eu_pd",
    table_id="enhancement_v1",
    force=True
)
```

**Returns:** List of columns with:
- `name` - Column name
- `type` - Data type (STRING, INTEGER, TIMESTAMP, etc.)
- `mode` - NULLABLE, REQUIRED, REPEATED
- `description` - Column description

---

## Dataset Permissions

### List Permissions

```python
mcp__mcprelay__sdds_list_dataset_permissions(
    project_id="<project_id>",
    dataset_id="<dataset_id>",
    show_inherited=False,      # Include inherited from project/org
    include_views=False,       # Include authorized views
    include_datasets=False,    # Include authorized datasets
    include_routines=False     # Include authorized routines
)
```

**Examples:**
```python
# List dataset permissions
sdds_list_dataset_permissions(
    project_id="itg-btdppublished-gbl-ww-pd",
    dataset_id="btdp_ds_c1_054_agile_eu_pd"
)

# Include inherited permissions
sdds_list_dataset_permissions(
    project_id="oa-data-btdpexploration-np",
    dataset_id="my_dataset",
    show_inherited=True
)

# Include all authorized resources
sdds_list_dataset_permissions(
    project_id="itg-btdppublished-gbl-ww-pd",
    dataset_id="btdp_ds_c1_0a1_gcpassets_eu_pd",
    include_views=True,
    include_datasets=True
)
```

### Grant Permission

```python
mcp__mcprelay__sdds_grant_dataset_permission(
    project_id="<project_id>",
    dataset_id="<dataset_id>",
    entity_type="<type>",      # "user", "group", "view", "dataset", "routine"
    entity_id="<identifier>",  # Email or full reference
    role="<role>"              # "READER", "WRITER", "OWNER"
)
```

**Examples:**
```python
# Grant user read access
sdds_grant_dataset_permission(
    project_id="oa-data-btdpexploration-np",
    dataset_id="my_dataset",
    entity_type="user",
    entity_id="sebastien.morand@loreal.com",
    role="READER"
)

# Grant group write access
sdds_grant_dataset_permission(
    project_id="oa-data-btdpexploration-np",
    dataset_id="my_dataset",
    entity_type="group",
    entity_id="IT-GLOBAL-GCP-BTDP-TEAM@loreal.com",
    role="WRITER"
)
```

### Revoke Permission

```python
mcp__mcprelay__sdds_revoke_dataset_permission(
    project_id="<project_id>",
    dataset_id="<dataset_id>",
    entity_type="<type>",
    entity_id="<identifier>",
    revoke_project_roles=False  # Also revoke projectOwner/Viewer/Editor
)
```

---

## SQL Fallback

### Tables Query

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
    description
FROM `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.tables_v2`
WHERE REGEXP_CONTAINS(LOWER(table_id), r'<pattern>')
  AND REGEXP_CONTAINS(dataset_id, r'.*_pd$')  -- Production only
ORDER BY creation_time DESC
LIMIT 100
```

**Common Patterns:**
```sql
-- Version pattern
WHERE REGEXP_CONTAINS(table_id, r'.*_v[0-9]+$')

-- Exclude snapshots/backups
WHERE NOT REGEXP_CONTAINS(table_id, r'.*(snapshot|backup|temp).*')

-- Find large tables
WHERE size_bytes > 1000000000  -- > 1GB
ORDER BY size_bytes DESC
```

---

## Best Practices

1. **RAG first** for discovery
2. **SDDS search** for filtered regexp queries
3. **Use environment filters** to reduce noise (dv, qa, np, pd)
4. **Get schema** before querying unfamiliar tables
5. **Check permissions** before granting access
6. **Use limit/offset** for large result sets
7. **SQL fallback** for complex joins or metadata queries
