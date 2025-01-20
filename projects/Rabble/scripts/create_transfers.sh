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
    "peoplepasses"
    "marketingoptin"
)

# Function to get the correct table name
get_table_name() {
    local report=$1
    local club=$2
    
    case $report in
        "eventattendance")
            echo "All_Attendees_${club}"
            ;;
        "assocclubusage")
            echo "Associate_Usage_${club}"
            ;;
        "leadersattendees")
            echo "Attendees_and_Leaders_${club}"
            ;;
        "clubcomments")
            echo "Club_Comments_${club}"
            ;;
        "gdproptin")
            echo "Club_Followers_${club}"
            ;;
        "clubpayments")
            echo "Club_Payments_Attendees_${club}"
            ;;
        "followersummary")
            echo "Follower_Summary_${club}"
            ;;
        "marketingoptin")
            echo "Marketing_Opt_in_${club}"
            ;;
        "peoplepasses")
            echo "People_passes_${club}"
            ;;
        *)
            echo "${report}_club${club}"
            ;;
    esac
}

function create_current_transfer {
    local club=$1
    local report=$2
    local table_name=$(get_table_name "$report" "$club")
    
    bq mk --transfer_config \
        --project_id=$PROJECT_ID \
        --target_dataset=$CURRENT_DATASET \
        --display_name="Current Transfer ${table_name}" \
        --data_source=google_cloud_storage \
        --params='{
            "data_path_template":"gs://'${BUCKET}'/data/'${report}'_club'${club}'_*.csv",
            "destination_table_name_template":"'${table_name}'",
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
        --schedule_start_time="2025-01-20T09:45:00Z" \
        --schedule="every mon,fri of month 09:45" \
        --location=europe-west2
    
    echo "Created current transfer for ${table_name}"
}

function create_historical_transfer {
    local club=$1
    local report=$2
    local table_name=$(get_table_name "$report" "$club")
    
    bq mk --transfer_config \
        --project_id=$PROJECT_ID \
        --target_dataset=$HISTORICAL_DATASET \
        --display_name="Historical Transfer ${table_name}" \
        --data_source=google_cloud_storage \
        --params='{
            "data_path_template":"gs://'${BUCKET}'/backup/'${report}'_club'${club}'_*.csv",
            "destination_table_name_template":"'${table_name}'",
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
        --schedule_start_time="2025-01-20T09:45:00Z" \
        --schedule="1 of quarter 09:45" \
        --location=europe-west2
    
    echo "Created historical transfer for ${table_name}"
}

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

# Create historical data transfers
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