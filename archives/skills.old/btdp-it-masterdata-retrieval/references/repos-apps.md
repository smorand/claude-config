# Repositories & Application Services

## Repositories

### RAG Index: smo_repository_v1

**Best for:** Quick semantic search of repositories

```python
mcp__mcprelay__rag_query_rag(
    index="smo_repository_v1",
    query="<search_term>",
    limit=10  # default: 1, max: 100
)
```

**Examples:**
```python
# Find data platform repositories
query_rag(index="smo_repository_v1", query="data platform core libraries")

# Find FastAPI repositories
query_rag(index="smo_repository_v1", query="FastAPI applications")

# Find specific framework repos
query_rag(index="smo_repository_v1", query="btdp framework modules")
```

**Tips:**
- Use descriptive terms without redundant keywords
- Results include repository metadata, description, URL
- Limit results to reduce noise (default is 1)

### SQL Fallback: repositories_v1

**Use when:** RAG returns insufficient results or need specific filters

**Table:** `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.repositories_v1`

```sql
SELECT
    repository_name,
    repository_description,
    repository_url,
    primary_language,
    topics,
    last_updated
FROM `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.repositories_v1`
WHERE REGEXP_CONTAINS(LOWER(repository_name), r'<pattern>')
   OR REGEXP_CONTAINS(LOWER(repository_description), r'<pattern>')
ORDER BY last_updated DESC
LIMIT 50
```

**Pattern Examples:**
- `r'btdp.*framework'` - BTDP framework repos
- `r'(fastapi|api).*service'` - API service repos
- `r'data.*platform'` - Data platform repos

---

## Application Services

### Method 1: RAG Index (application_service_name_v1)

**Best for:** Quick lookup by service name or description

```python
mcp__mcprelay__rag_query_rag(
    index="application_service_name_v1",
    query="<service_name_or_description>",
    limit=10
)
```

**Examples:**
```python
# Find BTDP services
query_rag(index="application_service_name_v1", query="btdp data services")

# Find specific application
query_rag(index="application_service_name_v1", query="looker analytics")
```

### Method 2: ITBM Search Tool

**Best for:** Detailed filtering and exact matches

```python
mcp__mcprelay__itbm_search_application(
    name=None,                      # Partial match on service name
    number=None,                    # Partial match on service number (SNSVCxxxxxxx)
    business_application=None,      # Partial match
    it_owner=None,                  # Partial match
    business_owner=None,            # Partial match
    description=None,               # Partial match
    operational_status=None,        # Exact match (e.g., "Operational")
    service_classification=None,    # Exact match (e.g., "Business", "Technical")
    business_divisions=None,        # Partial match
    hosting_type=None,              # Exact match (e.g., "Cloud", "On-Premise")
    cloud_service_provider=None,    # Exact match (e.g., "GCP", "AWS")
    tier=None,                      # Exact match (e.g., "1", "2", "3", "4")
    limit=50                        # Max: 100, default: 50
)
```

**Examples:**
```python
# Find GCP cloud services
itbm_search_application(
    cloud_service_provider="GCP",
    hosting_type="Cloud",
    limit=50
)

# Find services by IT owner
itbm_search_application(
    it_owner="sebastien.morand",
    operational_status="Operational"
)

# Find Tier 1 critical services
itbm_search_application(
    tier="1",
    service_classification="Business"
)

# Search by partial name
itbm_search_application(
    name="data platform",
    limit=20
)
```

**Common Values:**
- **operational_status:** `Operational`, `Non-Operational`, `In Development`
- **service_classification:** `Business`, `Technical`, `Infrastructure`
- **hosting_type:** `Cloud`, `On-Premise`, `Hybrid`
- **cloud_service_provider:** `GCP`, `AWS`, `Azure`
- **tier:** `1`, `2`, `3`, `4` (1=Critical, 4=Low priority)

### SQL Fallback: application_service_v1

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
LIMIT 50
```

---

## Best Practices

1. **RAG first** for quick searches without specific filters
2. **ITBM tools** when you need exact operational status, tier, or owner filters
3. **SQL fallback** for complex regexp patterns or custom joins
4. **Limit results** appropriately (10-50 for exploration, increase if needed)
5. **Use partial matches** - ITBM tools use CONTAINS operator automatically
