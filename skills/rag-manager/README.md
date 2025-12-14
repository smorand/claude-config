# RAG Manager Skill

Expert in managing RAG (Retrieval-Augmented Generation) indices for L'Oréal's BTDP infrastructure.

## Purpose

This skill provides all RAG index management capabilities:
- List available RAG indices
- Search RAG indices with semantic queries
- Create new RAG indices
- Delete existing RAG indices

## When to Use

Trigger this skill when users ask about:
- "list RAG"
- "create RAG"
- "delete RAG"
- "search RAG"
- "available RAG indices"
- Any operation involving RAG index management

## Scripts

All RAG operations are handled by shell scripts in this directory:

- `rag_list.sh` - List all available RAG indices
- `rag_search.sh` - Search a RAG index with semantic queries
- `rag_create.sh` - Create a new RAG index
- `rag_delete.sh` - Delete a RAG index

## Integration

This skill is referenced by:
- `btdp-it-masterdata-retrieval` - Uses RAG search for masterdata retrieval

## API

Uses the BTDP RAG API: `https://api.loreal.net/global/it4it/btdp-mcprag`

Authentication: OAuth token from `~/.gcp/access_token`
