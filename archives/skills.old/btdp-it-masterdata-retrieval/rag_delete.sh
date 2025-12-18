#!/bin/bash
# Delete a RAG index
# Usage: ./rag_delete.sh <object_name>
# Example: ./rag_delete.sh groups_v1

set -euo pipefail

# Configuration
RAG_API_URL="https://api.loreal.net/global/it4it/btdp-mcprag"
TOKEN_FILE="$HOME/.gcp/access_token"

# Check arguments
if [ $# -ne 1 ]; then
    echo "ERROR: Object name is required"
    echo "Usage: $0 <object_name>"
    exit 1
fi

OBJECT_NAME="$1"

# Check token file exists
if [ ! -f "$TOKEN_FILE" ]; then
    echo "ERROR: Token file not found at $TOKEN_FILE"
    exit 1
fi

# Read token
ACCESS_TOKEN=$(cat "$TOKEN_FILE")

# Confirm deletion
echo "WARNING: You are about to delete RAG index '$OBJECT_NAME'"
read -p "Are you sure? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Deletion cancelled"
    exit 0
fi

# Make API call
RESPONSE=$(curl -s -w "\n%{http_code}" -X DELETE \
    "${RAG_API_URL}/v1/ragconfigs/${OBJECT_NAME}" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}")

# Extract HTTP status code (last line)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

# Extract response body (all lines except last)
BODY=$(echo "$RESPONSE" | sed '$d')

# Check HTTP status
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "204" ]; then
    echo "SUCCESS: RAG index '$OBJECT_NAME' deleted successfully"
else
    echo "ERROR: API request failed with status $HTTP_CODE"
    echo "$BODY" | jq -r '.error.message // .message // .'
    exit 1
fi
