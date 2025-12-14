#!/bin/bash
# Add members to a Google Cloud Identity group
# Usage: ./add_members.sh <group_email> <member1> [member2] [member3] ...
# Example: ./add_members.sh data-gcp-team@loreal.com user1@loreal.com user2@loreal.com

set -euo pipefail

# Configuration
SERVICE_URL="https://api.loreal.net/global/it4it/itg-groupsapi"
TOKEN_FILE="$HOME/.gcp/access_token_adm"

# Check arguments
if [ $# -lt 2 ]; then
    echo "ERROR: Group email and at least one member email are required"
    echo "Usage: $0 <group_email> <member1> [member2] [member3] ..."
    exit 1
fi

GROUP_EMAIL="$1"
shift
MEMBERS=("$@")

# Check token file exists
if [ ! -f "$TOKEN_FILE" ]; then
    echo "ERROR: ADM token file not found at $TOKEN_FILE"
    exit 1
fi

# Read token
ACCESS_TOKEN=$(cat "$TOKEN_FILE")

# Build JSON array of members
MEMBERS_JSON=$(printf '%s\n' "${MEMBERS[@]}" | jq -R . | jq -s .)

# Build request body
REQUEST_BODY=$(jq -n --argjson members "$MEMBERS_JSON" '{members: $members}')

# Make API call
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
    "${SERVICE_URL}/v1/groups/${GROUP_EMAIL}/members?return_members=false" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "$REQUEST_BODY")

# Extract HTTP status code (last line)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

# Extract response body (all lines except last)
BODY=$(echo "$RESPONSE" | sed '$d')

# Check HTTP status
case "$HTTP_CODE" in
    200)
        echo "SUCCESS: All ${#MEMBERS[@]} member(s) added to $GROUP_EMAIL"
        ;;
    206)
        echo "PARTIAL SUCCESS: Some members added, some failed"
        echo "$BODY" | jq -r '.data.errors[]? | "  ERROR: \(.member) - \(.error)"'
        ;;
    *)
        echo "ERROR: API request failed with status $HTTP_CODE"
        echo "$BODY" | jq -r '.error.message // .message // .'
        exit 1
        ;;
esac
