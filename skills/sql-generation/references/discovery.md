# Discovery Tools Guide

Complete guide to discovering tables, datasets, and schemas in BTDP environment.

## Discovery Workflow

Follow this sequence when writing SQL:

1. **Find tables/datasets** → Use RAG or SDDS search tools
2. **Get schema** → Use `sdds_get_schema`
3. **Preview data** → Query first 20-40 rows
4. **Understand relationships** → Ask about join keys
5. **Write query** → Follow coding standards

## Tool Selection Guide

### When to Use RAG Tools

Use for **semantic/concept-based search**:
- "I need customer order data"
- "Find tables related to product inventory"
- "Where is sales data stored?"
- "Tables containing user information"

RAG tools use AI embeddings to understand meaning and find relevant resources.

### When to Use SDDS Tools

Use for **pattern-based/exact search**:
- "Find all tables named *_orders"
- "List datasets in project X"
- "Search for table exactly named 'users'"
- "Get schema of specific table"

SDDS tools use regex patterns and direct database queries.

## RAG Tools (Semantic Search)

### Available RAG Indices

1. **smo_table_v1** - Search BigQuery tables
2. **smo_dataset_v1** - Search BigQuery datasets
3. **smo_project_v1** - Search GCP projects

### RAG Query Function

```python
mcp__mcprelay__rag_query_rag(
    index="smo_table_v1",
    query="your search terms",
    limit=5  # Optional, defaults to 1
)
```

### RAG Examples

#### Example 1: Find Customer Tables

```python
# Search for customer-related tables
rag_query_rag(
    index="smo_table_v1",
    query="customer orders purchases",
    limit=5
)

# Returns tables semantically related to customers and orders
```

#### Example 2: Find Sales Datasets

```python
# Search for datasets containing sales data
rag_query_rag(
    index="smo_dataset_v1",
    query="sales revenue transactions",
    limit=5
)
```

#### Example 3: Find Project by Purpose

```python
# Find project related to data warehouse
rag_query_rag(
    index="smo_project_v1",
    query="data warehouse analytics",
    limit=3
)
```

#### Example 4: Product Information

```python
# Find tables with product catalog information
rag_query_rag(
    index="smo_table_v1",
    query="product catalog inventory",
    limit=5
)
```

### RAG Best Practices

**✅ DO**:
- Use natural language descriptions
- Include related concepts
- Search by business purpose
- Be specific about what you need

```python
# GOOD: Descriptive, purposeful
rag_query_rag(index="smo_table_v1", query="customer lifetime value metrics")
rag_query_rag(index="smo_table_v1", query="product sales by region")
```

**❌ DON'T**:
- Include the word "table" or "dataset" unless meaningful
- Use overly generic terms
- Mix unrelated concepts

```python
# BAD: Redundant, too generic
rag_query_rag(index="smo_table_v1", query="table")  # Too generic
rag_query_rag(index="smo_table_v1", query="data table information")  # Redundant
```

### Understanding RAG Results

RAG returns ranked results with similarity scores:

```json
{
  "results": [
    {
      "table_name": "customer_orders",
      "project_id": "project-id",
      "dataset_id": "dataset-id",
      "description": "Customer order transactions",
      "similarity_score": 0.92
    }
  ]
}
```

Higher similarity scores indicate better matches.

## SDDS Tools (Direct Search)

### Available SDDS Functions

1. **sdds_search_datasets** - Search datasets by pattern
2. **sdds_search_tables** - Search tables by pattern
3. **sdds_list_datasets** - List all datasets in project
4. **sdds_list_tables** - List all tables in dataset
5. **sdds_get_schema** - Get table schema details
6. **sdds_execute_query** - Execute SQL queries

### Search Functions (Pattern-Based)

#### sdds_search_datasets

```python
# Search datasets by regex pattern
sdds_search_datasets(
    pattern=".*sales.*",  # Regex pattern
    project_id="project-id",  # Optional
    environment="pd",  # Optional: dv, qa, np, pd
    use_not=False,  # Optional: invert match
    limit=100,  # Optional: max results
    offset=0  # Optional: skip results
)
```

**Examples**:
```python
# Find all datasets containing "sales"
sdds_search_datasets(pattern=".*sales.*")

# Find datasets starting with "customer"
sdds_search_datasets(pattern="^customer.*")

# Find datasets in specific project
sdds_search_datasets(
    pattern=".*analytics.*",
    project_id="oa-data-btdpexploration-np"
)

# Find datasets NOT matching pattern
sdds_search_datasets(
    pattern=".*test.*",
    use_not=True  # Excludes test datasets
)
```

#### sdds_search_tables

```python
# Search tables by regex pattern
sdds_search_tables(
    pattern=".*orders.*",  # Regex pattern
    project_id="project-id",  # Optional
    dataset_id="dataset-id",  # Optional
    environment="pd",  # Optional: dv, qa, np, pd
    use_not=False,  # Optional: invert match
    limit=100,  # Optional: max results
    offset=0  # Optional: skip results
)
```

**Examples**:
```python
# Find all tables containing "user"
sdds_search_tables(pattern=".*user.*")

# Find tables in specific dataset
sdds_search_tables(
    pattern=".*metrics.*",
    dataset_id="analytics_dataset"
)

# Find tables starting with "fact_"
sdds_search_tables(pattern="^fact_.*")

# Find all dimension tables
sdds_search_tables(pattern="^dim_.*")
```

### List Functions (Direct Listing)

#### sdds_list_datasets

```python
# List all datasets in a project
sdds_list_datasets(
    project_id="oa-data-btdpexploration-np",  # Optional
    limit=100,  # Optional
    offset=0  # Optional
)
```

**Examples**:
```python
# List all datasets in SDDS project
sdds_list_datasets(project_id="itg-btdppublished-gbl-ww-pd")

# List all datasets (no filter)
sdds_list_datasets(limit=50)
```

#### sdds_list_tables

```python
# List all tables in a dataset
sdds_list_tables(
    project_id="project-id",  # Optional
    dataset_id="dataset-id",  # Optional
    limit=100,  # Optional
    offset=0  # Optional
)
```

**Examples**:
```python
# List all tables in specific dataset
sdds_list_tables(
    project_id="itg-btdppublished-gbl-ww-pd",
    dataset_id="sdds"
)

# List first 50 tables across all datasets
sdds_list_tables(limit=50)
```

### Schema Discovery

#### sdds_get_schema

```python
# Get complete schema for a table
sdds_get_schema(
    project_id="project-id",
    dataset_id="dataset-id",
    table_id="table-id",
    force=False  # Optional: bypass cache
)
```

**Returns**:
```json
[
  {
    "column_name": "user_id",
    "data_type": "STRING",
    "is_nullable": "NO",
    "description": "Unique user identifier"
  },
  {
    "column_name": "email",
    "data_type": "STRING",
    "is_nullable": "YES",
    "description": "User email address"
  }
]
```

**Examples**:
```python
# Get schema for specific table
sdds_get_schema(
    project_id="itg-btdppublished-gbl-ww-pd",
    dataset_id="sdds",
    table_id="users"
)

# Force refresh from BigQuery (bypass cache)
sdds_get_schema(
    project_id="itg-btdppublished-gbl-ww-pd",
    dataset_id="sdds",
    table_id="users",
    force=True
)
```

### Data Preview

#### sdds_execute_query

```python
# Execute SQL query to preview data
sdds_execute_query(
    sql_query="SELECT * FROM `project.dataset.table` LIMIT 20",
    project_id="project-id",  # Optional: for billing
    limit=100,  # Optional: max rows returned
    offset=0  # Optional: skip rows
)
```

**Examples**:
```python
# Preview first 30 rows
sdds_execute_query(
    sql_query="""
        SELECT
            user_id,
            email,
            created_at
        FROM `itg-btdppublished-gbl-ww-pd.sdds.users`
        LIMIT 30
    """
)

# Preview with specific conditions
sdds_execute_query(
    sql_query="""
        SELECT *
        FROM `project.dataset.orders`
        WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
        LIMIT 40
    """
)
```

## Complete Discovery Workflow Examples

### Example 1: Find and Explore Customer Data

```python
# Step 1: Find relevant tables using RAG
rag_result = rag_query_rag(
    index="smo_table_v1",
    query="customer information profiles",
    limit=5
)

# Step 2: Get schema for best match
schema = sdds_get_schema(
    project_id="project-id",
    dataset_id="dataset-id",
    table_id="customers"
)

# Step 3: Preview data
preview = sdds_execute_query(
    sql_query="""
        SELECT *
        FROM `project.dataset.customers`
        LIMIT 30
    """
)

# Step 4: Write final query using discovered information
```

### Example 2: Explore Dataset Contents

```python
# Step 1: List all tables in dataset
tables = sdds_list_tables(
    project_id="itg-btdppublished-gbl-ww-pd",
    dataset_id="sdds"
)

# Step 2: Get schema for interesting tables
for table in tables:
    schema = sdds_get_schema(
        project_id=table["project_id"],
        dataset_id=table["dataset_id"],
        table_id=table["table_id"]
    )

# Step 3: Preview data from selected table
preview = sdds_execute_query(
    sql_query=f"SELECT * FROM `{project}.{dataset}.{table}` LIMIT 20"
)
```

### Example 3: Find Related Tables

```python
# Step 1: Find primary table
main_table = rag_query_rag(
    index="smo_table_v1",
    query="user accounts",
    limit=1
)

# Step 2: Search for related tables in same dataset
related = sdds_list_tables(
    project_id=main_table["project_id"],
    dataset_id=main_table["dataset_id"]
)

# Step 3: Get schemas to understand relationships
for table in related:
    schema = sdds_get_schema(
        project_id=table["project_id"],
        dataset_id=table["dataset_id"],
        table_id=table["table_id"]
    )
    # Look for common column names (user_id, customer_id, etc.)
```

## Regex Patterns for SDDS Search

### Common Patterns

```python
# Exact match
pattern="^table_name$"

# Starts with
pattern="^prefix_.*"

# Ends with
pattern=".*_suffix$"

# Contains
pattern=".*keyword.*"

# Multiple keywords (OR)
pattern=".*(keyword1|keyword2|keyword3).*"

# Exclude test tables
pattern=".*"  # with use_not=False
pattern=".*test.*"  # with use_not=True

# Dimension tables
pattern="^dim_.*"

# Fact tables
pattern="^fact_.*"

# Date-based tables
pattern=".*_20[0-9]{2}[0-1][0-9][0-3][0-9]$"  # YYYYMMDD suffix
```

### Pattern Examples

```python
# All sales-related tables
sdds_search_tables(pattern=".*(sale|order|transaction).*")

# All tables in a specific project starting with "user"
sdds_search_tables(
    pattern="^user.*",
    project_id="project-id"
)

# All materialized views (ending with _mv)
sdds_search_tables(pattern=".*_mv$")

# All temp/staging tables
sdds_search_tables(pattern="^(temp|stg|staging)_.*")
```

## Discovery Best Practices

### 1. Start Broad, Then Narrow

```python
# First: Use RAG for concept discovery
tables = rag_query_rag(index="smo_table_v1", query="sales data", limit=10)

# Then: Use SDDS for specific patterns
specific = sdds_search_tables(
    pattern=".*sales_fact.*",
    dataset_id="discovered_dataset"
)
```

### 2. Always Get Schema Before Writing SQL

```python
# ✅ GOOD: Get schema first
schema = sdds_get_schema(project_id, dataset_id, table_id)
# Review columns, types, descriptions
# Then write query with correct column names

# ❌ BAD: Guess column names
# Write query without checking schema
```

### 3. Preview Data to Understand Content

```python
# Preview to understand:
# - Data patterns
# - Value formats
# - NULL handling
# - Actual vs expected content

preview = sdds_execute_query(
    sql_query="SELECT * FROM `project.dataset.table` LIMIT 40"
)
```

### 4. Document Your Findings

```sql
-- Query comment documenting discovery
-- Found table using RAG query: "customer lifetime value"
-- Schema obtained: 2025-01-15
-- Key columns: customer_id (primary key), ltv_amount, last_updated

SELECT
    customer_id,
    ltv_amount,
    last_updated
FROM `project.dataset.customer_ltv`
WHERE last_updated >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY);
```

## Troubleshooting Discovery

### No Results from RAG

Try:
- Broader search terms
- Related synonyms
- Different combinations
- Checking dataset/project indices instead

### Too Many Results from SDDS

Try:
- More specific regex patterns
- Add project_id or dataset_id filters
- Use use_not=True to exclude unwanted results

### Can't Find Expected Table

Check:
- Spelling and naming conventions
- Different environments (dv, qa, np, pd)
- Alternative table names
- Parent dataset location

### Schema Doesn't Match Preview

Try:
- Force schema refresh with force=True
- Check if viewing correct table
- Verify project/dataset/table names
- Check for recent schema changes
