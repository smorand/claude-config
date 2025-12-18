#!/bin/bash
# List members of a Google Cloud Identity group via Groups API
# Usage: ./list_members.sh <group_email> [output_file]
# Example: ./list_members.sh data-gcp-team@loreal.com /tmp/members.txt

set -euo pipefail

# Configuration
SERVICE_URL="https://api.loreal.net/global/it4it/itg-groupsapi"
TOKEN_FILE="$HOME/.gcp/access_token_adm"

# Check arguments
if [ $# -lt 1 ]; then
    echo "ERROR: Group email is required"
    echo "Usage: $0 <group_email> [output_file]"
    exit 1
fi

GROUP_EMAIL="$1"
OUTPUT_FILE="${2:-/tmp/group_members.txt}"

# Check token file exists
if [ ! -f "$TOKEN_FILE" ]; then
    echo "ERROR: ADM token file not found at $TOKEN_FILE"
    exit 1
fi

# Read token
ACCESS_TOKEN=$(cat "$TOKEN_FILE")

# Make API call
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET \
    "${SERVICE_URL}/v1/groups/${GROUP_EMAIL}/members" \
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

# Extract members and save to file
echo "$BODY" | jq -r '.data.members[]' > "$OUTPUT_FILE"

# Count members
MEMBER_COUNT=$(wc -l < "$OUTPUT_FILE" | tr -d ' ')

# Output result
echo "SUCCESS: Group $GROUP_EMAIL has $MEMBER_COUNT members"
echo "Members list saved to: $OUTPUT_FILE"
