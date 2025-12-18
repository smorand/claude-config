# BTDP IT Masterdata Retrieval Skill

Expert in retrieving IT masterdata from L'Oréal's BTDP infrastructure.

## Purpose

This skill focuses on retrieving masterdata using various methods:
- RAG indices (via rag-manager skill)
- MCP tools
- SQL queries on BigQuery

## When to Use

Trigger this skill when users ask about:
- "What is the <masterdata_type> for <something>"
- Searching for repositories, applications, projects, datasets, tables
- Finding domains, IT organizations, groups
- Looking for stories, epics, sprints, enhancements
- Querying APIs or Confluence pages
- Requests about "in the SDDS"
- Questions about specific IT organization names

## Masterdata Types Supported

- Git repositories
- Applications (Application Services)
- GCP Projects
- Datasets
- Tables
- Domains (Data Domain)
- IT Organisations (IT Orgs)
- Groups (Google Cloud Identity)
- Stories
- Epics
- Sprints
- Enhancements
- APIs (L'Oréal API)

## Retrieval Strategy

1. **RAG Index** (fastest, semantic search)
   - Delegates to `rag-manager` skill for all RAG operations

2. **MCP Tools** (API-based, structured data)
   - Uses `loreal-api-search` for APIs
   - Uses Confluence MCP for Confluence pages

3. **SQL Fallback** (direct BigQuery, complex filtering)
   - Uses `bq` command for direct queries
   - Handles complex filtering and aggregations

## Integration

This skill leverages other skills:
- `rag-manager` - For all RAG index operations
- `loreal-api-search` - For API searches

## Environment Context

- **SDDS Project**: `itg-btdppublished-gbl-ww-pd`
- **Exploration Project**: `oa-data-btdpexploration-np`
- **Environments**: dv, qa, np, pd
