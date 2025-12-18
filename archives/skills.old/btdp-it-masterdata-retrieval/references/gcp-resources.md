# GCP Resources (Projects)

## GCP Projects

### RAG Index: smo_project_v1

**Best for:** Quick semantic search of GCP projects

```python
mcp__mcprelay__rag_query_rag(
    index="smo_project_v1",
    query="<search_term>",
    limit=10  # default: 1, max: 100
)
```

**Examples:**
```python
# Find BTDP projects
query_rag(index="smo_project_v1", query="btdp data platform projects")

# Find exploration projects
query_rag(index="smo_project_v1", query="exploration sandbox")

# Find production projects
query_rag(index="smo_project_v1", query="production data services")

# Find specific domain projects
query_rag(index="smo_project_v1", query="consumer data domain")
```

**Tips:**
- Results include project_id, project_name, environment indicators
- Use environment keywords: "dv", "qa", "np", "pd" for filtering
- Combine domain + environment for precision

### SQL Fallback: projects_v3

**Use when:** Need specific filters or regexp patterns

**Table:** `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.projects_v3`

```sql
SELECT
    project_id,
    project_name,
    project_number,
    labels,
    create_time,
    lifecycle_state
FROM `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.projects_v3`
WHERE REGEXP_CONTAINS(LOWER(project_id), r'<pattern>')
   OR REGEXP_CONTAINS(LOWER(project_name), r'<pattern>')
ORDER BY create_time DESC
LIMIT 50
```

**Common Patterns:**
```sql
-- Find all BTDP projects
WHERE REGEXP_CONTAINS(project_id, r'.*btdp.*')

-- Find production projects
WHERE REGEXP_CONTAINS(project_id, r'.*-pd$')

-- Find exploration/sandbox projects
WHERE REGEXP_CONTAINS(project_id, r'.*(exploration|sandbox|np).*')

-- Find specific environment
WHERE REGEXP_CONTAINS(project_id, r'.*-(dv|qa|np|pd)$')

-- Find by domain pattern
WHERE REGEXP_CONTAINS(project_id, r'oa-data-btdp.*')
```

**Project Naming Convention:**
```
{prefix}-{service}-{zone}-{domain}-{env}

Examples:
- oa-data-btdpexploration-np
- itg-btdppublished-gbl-ww-pd
- oa-data-btdpservices-gbl-ww-pd
```

**Environment Suffixes:**
- `dv` - Development
- `qa` - Quality Assurance
- `np` - Non-Production
- `pd` - Production

---

## Project Labels Query

**Extract labels from projects:**

```sql
SELECT
    project_id,
    label.key AS label_key,
    label.value AS label_value
FROM `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.projects_v3`,
UNNEST(labels) AS label
WHERE REGEXP_CONTAINS(project_id, r'<pattern>')
  AND label.key IN ('environment', 'domain', 'owner', 'cost-center')
ORDER BY project_id, label.key
```

**Common Label Keys:**
- `environment` - dv, qa, np, pd
- `domain` - Business domain
- `owner` - Technical owner
- `cost-center` - Billing code
- `data-classification` - Data sensitivity level

---

## Best Practices

1. **RAG first** for quick project discovery
2. **SQL fallback** when filtering by:
   - Environment suffix patterns
   - Label values
   - Creation date ranges
   - Lifecycle state
3. **Use regexp anchors** (`^`, `$`) for precise matching
4. **Include environment** in search terms for better RAG results
5. **Order by create_time DESC** to see recent projects first
