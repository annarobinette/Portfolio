#!/bin/bash
export GOOGLE_APPLICATION_CREDENTIALS="/Users/anna/Documents/MakeSweat_Reports/FileRequests/rabble-424818-6a7d8ba56cc5.json"
export GCS_BUCKET_NAME="europe-west2-rabble-5e308dc8-bucket"
export GOOGLE_CLOUD_PROJECT="rabble-424818"

export PROJECT_ID="rabble-424818"
gcloud config set project $PROJECT_ID

current_time=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

bq ls --transfer_config \
   --project_id=$PROJECT_ID \
   --location=europe-west2 \
   --transfer_location=europe-west2 | grep "Historical Transfer" | while read -r line; do
   transfer_name=$(echo "$line" | awk -F' ' '{print $1}')
   echo "Triggering transfer: $transfer_name"
   bq mk --transfer_run --run_time="$current_time" "$transfer_name"
   sleep 2
done