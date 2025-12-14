#!/bin/bash
# Get table lineage from BTDP Data Health Check API
# Usage: ./get_lineage.sh <table_full_id> [--parents|--children]

set -e

TABLE_ID="$1"
DIRECTION="${2:-both}"

if [ -z "$TABLE_ID" ]; then
    echo "Error: Table ID required"
    echo "Usage: $0 <table_full_id> [--parents|--children]"
    echo "Example: $0 itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.tables_v2 --parents"
    exit 1
fi

BASE_URL="https://api.loreal.net/global/it4it/btdpdatahealth/v1/lineage"
TOKEN=$(gcloud auth print-access-token 2>/dev/null)

if [ -z "$TOKEN" ]; then
    echo "Error: Failed to get GCloud auth token"
    exit 1
fi

fetch_lineage() {
    local endpoint="$1"
    curl -s -X GET \
        "${BASE_URL}/node/${TABLE_ID}/${endpoint}" \
        -H "Accept: application/json" \
        -H "Authorization: Bearer ${TOKEN}"
}

case "$DIRECTION" in
    --parents)
        fetch_lineage "parents"
        ;;
    --children)
        fetch_lineage "children"
        ;;
    both|*)
        echo '{"parents":'
        fetch_lineage "parents"
        echo ',"children":'
        fetch_lineage "children"
        echo '}'
        ;;
esac
