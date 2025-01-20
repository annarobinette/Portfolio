#!/bin/bash

# Configuration
PROJECT_ID="rabble-424818"
CURRENT_DATASET="RabbleIngest"
HISTORICAL_DATASET="RabbleIngest_Historical"
BUCKET="europe-west2-rabble-5e308dc8-bucket"
CLUBS=(225 227)
REPORTS=(
    "assocclubusage"
    "clubcomments"
    "clubpayments"
    "eventattendance"
    "followersummary"
    "gdproptin"
    "leadersattendees"
    "peopleinfo"
)

function create_current_transfer {
    local club=$1
    local report=$2
    
    bq mk --transfer_config \
        --project_id=$PROJECT_ID \
        --target_dataset=$CURRENT_DATASET \
        --display_name="Current Transfer ${report} club${club}" \
        --data_source=google_cloud_storage \
        --params='{
            "data_path_template":"gs://'${BUCKET}'/data/'${report}'_club'${club}'_*.csv",
            "destination_table_name_template":"'${report}'_club'${club}'",
            "file_format":"CSV",
            "max_bad_records":10,
            "write_disposition":"MIRROR",
            "allow_jagged_rows":true,
            "allow_quoted_newlines":true,
            "skip_leading_rows":1,
            "field_delimiter":",",
            "quote":"\"",
            "encoding":"UTF-8"
        }' \
        --schedule_start_time="2025-01-20T09:45:00Z" \
        --schedule="weekly monday,friday 09:45" \
        --location=europe-west2
    
    echo "Created current transfer for ${report}_club${club}"
}

function create_historical_transfer {
    local club=$1
    local report=$2
    
    bq mk --transfer_config \
        --project_id=$PROJECT_ID \
        --target_dataset=$HISTORICAL_DATASET \
        --display_name="Historical Transfer ${report} club${club}" \
        --data_source=google_cloud_storage \
        --params='{
            "data_path_template":"gs://'${BUCKET}'/backup/'${report}'_club'${club}'_*.csv",
            "destination_table_name_template":"'${report}'_club'${club}'",
            "file_format":"CSV",
            "max_bad_records":10,
            "write_disposition":"MIRROR",
            "allow_jagged_rows":true,
            "allow_quoted_newlines":true,
            "skip_leading_rows":1,
            "field_delimiter":",",
            "quote":"\"",
            "encoding":"UTF-8"
        }' \
        --schedule_start_time="2025-01-20T09:45:00Z" \
        --schedule="quarterly 09:45" \
        --location=europe-west2
    
    echo "Created historical transfer for ${report}_club${club}"
}

# First, delete the existing historical dataset if it exists
#echo "Removing existing historical dataset if it exists..."
#bq rm -r -f ${PROJECT_ID}:${HISTORICAL_DATASET}

# Create the historical dataset with correct location
# echo "Creating historical dataset in europe-west2..."
#bq mk --dataset \
#    --description "Historical Rabble data from MakeSweat" \
 #   --location=europe-west2 \
 #   ${PROJECT_ID}:${HISTORICAL_DATASET}

# Create transfers for current data
echo "Creating current data transfers..."
for club in "${CLUBS[@]}"
do
    for report in "${REPORTS[@]}"
    do
        create_current_transfer "$club" "$report"
        sleep 2
    done
done

# Create transfers for historical data
echo "Creating historical data transfers..."
for club in "${CLUBS[@]}"
do
    for report in "${REPORTS[@]}"
    do
        create_historical_transfer "$club" "$report"
        sleep 2
    done
done

echo "Script execution completed."





<<Errors
igQuery error in mk operation: The specified schedule is invalid: [weekly monday,friday 09:45]
Created current transfer for followersummary_club227
BigQuery error in mk operation: The specified schedule is invalid: [weekly monday,friday 09:45]
Created current transfer for gdproptin_club227
BigQuery error in mk operation: The specified schedule is invalid: [weekly monday,friday 09:45]
Created current transfer for leadersattendees_club227
BigQuery error in mk operation: The specified schedule is invalid: [weekly monday,friday 09:45]
Created current transfer for peopleinfo_club227
Creating historical data transfers...
BigQuery error in mk operation: The specified schedule is invalid: [quarterly 09:45]
Created historical transfer for assocclubusage_club225
BigQuery error in mk operation: The specified schedule is invalid: [quarterly 09:45]
Created historical transfer for clubcomments_club225
BigQuery error in mk operation: The specified schedule is invalid: [quarterly 09:45]
Created historical transfer for clubpayments_club225
BigQuery error in mk operation: The specified schedule is invalid: [quarterly 09:45]
Created historical transfer for eventattendance_club225
BigQuery error in mk operation: The specified schedule is inv
Errors