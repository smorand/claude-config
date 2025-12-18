#!/bin/bash
# Create a new RAG index
# Usage: ./rag_create.sh <table_reference> <object_name> <fields_to_include_comma_separated>
# Example: ./rag_create.sh "itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.tables_v2" "tables_rag_v1" "table_id,description"

set -euo pipefail

# Configuration
RAG_API_URL="https://api.loreal.net/global/it4it/btdp-mcprag"
TOKEN_FILE="$HOME/.gcp/access_token"

# Check arguments
if [ $# -ne 3 ]; then
    echo "ERROR: Table reference, object name, and fields are required"
    echo "Usage: $0 <table_reference> <object_name> <fields_to_include_comma_separated>"
    echo ""
    echo "Example:"
    echo "  $0 'itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.tables_v2' 'tables_rag_v1' 'table_id,description'"
    echo ""
    echo "Note: Only C1 and C2 datasets are supported (dataset pattern: *_ds_c[12]_*)"
    exit 1
fi

TABLE_REF="$1"
OBJECT_NAME="$2"
FIELDS_CSV="$3"

# Validate dataset confidentiality level (C1 or C2 only)
if ! echo "$TABLE_REF" | grep -qE '_ds_c[12]_'; then
    echo "ERROR: Table reference must be from a C1 or C2 dataset"
    echo "Dataset pattern must match: *_ds_c1_* or *_ds_c2_*"
    echo "C3 datasets are not supported due to high sensitivity"
    exit 1
fi

# Check token file exists
if [ ! -f "$TOKEN_FILE" ]; then
    echo "ERROR: Token file not found at $TOKEN_FILE"
    exit 1
fi

# Read token
ACCESS_TOKEN=$(cat "$TOKEN_FILE")

# Convert comma-separated fields to JSON array
IFS=',' read -ra FIELDS_ARRAY <<< "$FIELDS_CSV"
FIELDS_JSON=$(printf '%s\n' "${FIELDS_ARRAY[@]}" | jq -R . | jq -s .)

# Build request body
REQUEST_BODY=$(jq -n \
    --arg table_ref "$TABLE_REF" \
    --arg object_name "$OBJECT_NAME" \
    --argjson fields "$FIELDS_JSON" \
    '{
        table_reference: $table_ref,
        object_name: $object_name,
        fields_to_include: $fields,
        task_type: "SEMANTIC_SIMILARITY"
    }')

echo "Creating RAG index with configuration:"
echo "$REQUEST_BODY" | jq '.'
echo ""

# Make API call
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
    "${RAG_API_URL}/v1/ragconfigs" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "$REQUEST_BODY")

# Extract HTTP status code (last line)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

# Extract response body (all lines except last)
BODY=$(echo "$RESPONSE" | sed '$d')

# Check HTTP status
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then
    echo "SUCCESS: RAG index '$OBJECT_NAME' created successfully"
    echo ""
    echo "Details:"
    echo "$BODY" | jq '.'
else
    echo "ERROR: API request failed with status $HTTP_CODE"
    echo "$BODY" | jq -r '.error.message // .message // .'
    exit 1
fi
