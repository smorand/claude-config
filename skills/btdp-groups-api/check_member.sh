#!/bin/bash
# Check if a user is a member of a Google Cloud Identity group
# Usage: ./check_member.sh <group_email> <user_email>
# Example: ./check_member.sh data-gcp-team@loreal.com sebastien.morand@loreal.com

set -euo pipefail

# Configuration
SERVICE_URL="https://api.loreal.net/global/it4it/itg-groupsapi"
TOKEN_FILE="$HOME/.gcp/access_token_adm"

# Check arguments
if [ $# -ne 2 ]; then
    echo "ERROR: Both group email and user email are required"
    echo "Usage: $0 <group_email> <user_email>"
    exit 1
fi

GROUP_EMAIL="$1"
USER_EMAIL="$2"

# Check token file exists
if [ ! -f "$TOKEN_FILE" ]; then
    echo "ERROR: ADM token file not found at $TOKEN_FILE"
    exit 1
fi

# Read token
ACCESS_TOKEN=$(cat "$TOKEN_FILE")

# Make API call
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET \
    "${SERVICE_URL}/v1/groups/${GROUP_EMAIL}/members/${USER_EMAIL}" \
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

# Extract membership status
IS_MEMBER=$(echo "$BODY" | jq -r '.data')

# Output result
if [ "$IS_MEMBER" = "true" ]; then
    echo "YES: $USER_EMAIL is a member of $GROUP_EMAIL"
    exit 0
else
    echo "NO: $USER_EMAIL is NOT a member of $GROUP_EMAIL"
    exit 0
fi
