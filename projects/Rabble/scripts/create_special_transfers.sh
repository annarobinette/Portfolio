#!/bin/bash

# Configuration
PROJECT_ID="rabble-424818"
CURRENT_DATASET="RabbleIngest"
BUCKET="europe-west2-rabble-5e308dc8-bucket"

# Special tables
SPECIAL_TABLES=(
    "Locations_input"
    "Passes_input"
)

# Create transfers for special tables
echo "Creating transfers for special tables..."
for table in "${SPECIAL_TABLES[@]}"
do
    bq mk --transfer_config \
        --project_id=$PROJECT_ID \
        --target_dataset=$CURRENT_DATASET \
        --display_name="Special Transfer ${table}" \
        --data_source=google_cloud_storage \
        --params='{
            "data_path_template":"gs://'${BUCKET}'/data/'${table}'_*.csv",
            "destination_table_name_template":"'${table}'",
            "file_format":"CSV",
            "max_bad_records":"10",
            "write_disposition":"MIRROR",
            "allow_jagged_rows":"true",
            "allow_quoted_newlines":"true",
            "skip_leading_rows":"1",
            "field_delimiter":",",
            "quote":"\"",
            "encoding":"UTF8"
        }' \
        --schedule_start_time="2025-02-14T11:35:00Z" \
        --schedule="every mon,fri of month 09:45" \
        --location=europe-west2
    
    echo "Created transfer for ${table}"
    sleep 2
done

echo "Special transfers creation completed."