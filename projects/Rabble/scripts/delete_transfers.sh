#!/bin/bash

# Configuration
PROJECT_ID="rabble-424818"
LOCATION="europe-west2"

echo "Fetching and processing transfer configs..."

# List all transfers and grep for patterns
bq ls --transfer_config | grep -E "club225|club227|_225|_227" | while read -r line
do
    # Extract the transfer ID from the line
    transfer_id=$(echo "$line" | awk '{print $1}')
    display_name=$(echo "$line" | cut -d' ' -f2-)
    
    if [ ! -z "$transfer_id" ]; then
        echo "Found transfer: $display_name"
        echo "Deleting transfer ID: $transfer_id"
        bq rm --transfer_config "$transfer_id" -f
        sleep 1
    fi
done

echo "Deletion completed."