#!/bin/bash
# Search a RAG index with a query
# Usage: ./rag_search.sh <index_name> <query> [limit] [output_file]
# Example: ./rag_search.sh groups_v1 "explorationaladvanced" 10
# Example: ./rag_search.sh smo_table_v1 "GCP costs" 5 /tmp/results.json

set -euo pipefail

# Configuration
RAG_API_URL="https://api.loreal.net/global/it4it/btdp-mcprag"
TOKEN_FILE="$HOME/.gcp/access_token"

# Check arguments
if [ $# -lt 2 ]; then
    echo "ERROR: Index name and query are required"
    echo "Usage: $0 <index_name> <query> [limit] [output_file]"
    exit 1
fi

INDEX_NAME="$1"
QUERY="$2"
LIMIT="${3:-10}"
OUTPUT_FILE="${4:-}"

# Check token file exists
if [ ! -f "$TOKEN_FILE" ]; then
    echo "ERROR: Token file not found at $TOKEN_FILE"
    exit 1
fi

# Read token
ACCESS_TOKEN=$(cat "$TOKEN_FILE")

# URL encode the query
ENCODED_QUERY=$(printf %s "$QUERY" | jq -sRr @uri)

# Make API call
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET \
    "${RAG_API_URL}/v1/rag/${INDEX_NAME}?query=${ENCODED_QUERY}&limit=${LIMIT}" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}")

# Extract HTTP status code (last line)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

# Extract response body (all lines except last)
BODY=$(echo "$RESPONSE" | sed '$d')

# Check HTTP status
if [ "$HTTP_CODE" != "200" ]; then
    echo "ERROR: API request failed with status $HTTP_CODE"
    echo "$BODY" | jq -r '.error.message // .message // .'
    exit 1
fi

# Save to file if specified
if [ -n "$OUTPUT_FILE" ]; then
    echo "$BODY" | jq '.' > "$OUTPUT_FILE"
    RESULT_COUNT=$(echo "$BODY" | jq '.results | length')
    echo "SUCCESS: Found $RESULT_COUNT results for query '$QUERY' in index '$INDEX_NAME'"
    echo "Results saved to: $OUTPUT_FILE"
else
    # Output to stdout with formatted display
    RESULT_COUNT=$(echo "$BODY" | jq '.results | length')
    echo "Query: $QUERY"
    echo "Index: $INDEX_NAME"
    echo "Results: $RESULT_COUNT"
    echo ""
    echo "$BODY" | jq '.'
fi
