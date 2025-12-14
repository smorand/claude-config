#!/bin/bash
# List all available RAG indices
# Usage: ./rag_list.sh [output_format]
# output_format: json (default) | summary
# Example: ./rag_list.sh summary

set -euo pipefail

# Configuration
RAG_API_URL="https://api.loreal.net/global/it4it/btdp-mcprag"
TOKEN_FILE="$HOME/.gcp/access_token"

# Check token file exists
if [ ! -f "$TOKEN_FILE" ]; then
    echo "ERROR: Token file not found at $TOKEN_FILE"
    exit 1
fi

# Read token
ACCESS_TOKEN=$(cat "$TOKEN_FILE")

# Default output format
OUTPUT_FORMAT="${1:-json}"

# Make API call
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET \
    "${RAG_API_URL}/v1/ragconfigs" \
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

# Output based on format
case "$OUTPUT_FORMAT" in
    json)
        echo "$BODY" | jq '.'
        ;;
    summary)
        TOTAL=$(echo "$BODY" | jq '.configurations | length')
        echo "Total RAG indices: $TOTAL"
        echo ""
        echo "$BODY" | jq -r '.configurations[] | "  - \(.object_name) (\(.record_count) records)"'
        ;;
    *)
        echo "ERROR: Invalid output format. Use: json or summary"
        exit 1
        ;;
esac
