#!/bin/bash
# trigger_weekly_transfers.sh

PROJECT_ID="rabble-424818"
LOCATION="europe-west2"

echo "Starting manual trigger of weekly transfers..."

# List all transfer configs that match the weekly pattern
weekly_transfers=$(bq ls --transfer_config \
    --filter='displayName LIKE "Current Transfer%"' \
    --format=json \
    --location=$LOCATION)

# Trigger each transfer
echo "$weekly_transfers" | jq -r '.[] | .name' | while read -r transfer_name; do
    echo "Triggering transfer: $transfer_name"
    bq mk --transfer_run "$transfer_name"
    sleep 2  # Brief pause between triggers
done

echo "Weekly transfers triggered successfully."