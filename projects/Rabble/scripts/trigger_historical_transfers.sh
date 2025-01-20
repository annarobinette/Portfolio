#!/bin/bash
# trigger_historical_transfers.sh

PROJECT_ID="rabble-424818"
LOCATION="europe-west2"

echo "Starting manual trigger of historical transfers..."

# List all transfer configs that match the historical pattern
historical_transfers=$(bq ls --transfer_config \
    --filter='displayName LIKE "Historical Transfer%"' \
    --format=json \
    --location=$LOCATION)

# Trigger each transfer
echo "$historical_transfers" | jq -r '.[] | .name' | while read -r transfer_name; do
    echo "Triggering transfer: $transfer_name"
    bq mk --transfer_run "$transfer_name"
    sleep 2  # Brief pause between triggers
done

echo "Historical transfers triggered successfully."