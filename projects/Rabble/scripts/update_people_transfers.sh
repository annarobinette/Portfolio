#!/bin/bash

# Configuration
PROJECT_ID="rabble-424818"
CURRENT_DATASET="RabbleIngest"
HISTORICAL_DATASET="RabbleIngest_Historical"
BUCKET="europe-west2-rabble-5e308dc8-bucket"

function create_current_transfer {
    local club=$1
    
    bq mk --transfer_config \
        --project_id=$PROJECT_ID \
        --target_dataset=$CURRENT_DATASET \
        --display_name="Current Transfer Player_Data_${club}" \
        --data_source=google_cloud_storage \
        --params='{
            "data_path_template":"gs://'${BUCKET}'/data/peopleinfo_club'${club}'_*.csv",
            "destination_table_name_template":"Player_Data_'${club}'",
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
        --schedule_start_time="2025-01-30T09:45:00Z" \
        --schedule="every mon,fri of month 09:45" \
        --location=europe-west2
    
    echo "Created current transfer for Player_Data_${club}"
}

function create_historical_transfer {
    local club=$1
    
    bq mk --transfer_config \
        --project_id=$PROJECT_ID \
        --target_dataset=$HISTORICAL_DATASET \
        --display_name="Historical Transfer People Data ${club}" \
        --data_source=google_cloud_storage \
        --params='{
            "data_path_template":"gs://'${BUCKET}'/backup/peopleinfo_club'${club}'_*.csv",
            "destination_table_name_template":"Player_Data_'${club}'",
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
        --schedule_start_time="2025-01-30T09:45:00Z" \
        --schedule="1 of quarter 09:45" \
        --location=europe-west2
    
    echo "Created historical transfer for People Data ${club}"
}

# Create transfers for club 225
echo "Creating transfers for club 225..."
create_current_transfer "225"
sleep 2
create_historical_transfer "225"
sleep 2

# Create transfers for club 227
echo "Creating transfers for club 227..."
create_current_transfer "227"
sleep 2
create_historical_transfer "227"

echo "Script execution completed."