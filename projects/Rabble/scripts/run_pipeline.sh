#!/bin/bash
# run_pipeline.sh

# Set environment variables
export GCS_BUCKET_NAME="europe-west2-rabble-5e308dc8-bucket"
export GOOGLE_CLOUD_PROJECT="rabble-424818"
export GOOGLE_APPLICATION_CREDENTIALS="/Users/anna/Documents/MakeSweat_Reports/FileRequests/rabble-424818-6a7d8ba56cc5.json"

# Function to run pipeline
run_pipeline() {
    local mode=$1
    if [ "$mode" == "historical" ]; then
        /opt/anaconda3/bin/python /Users/anna/Documents/GitHub/Portfolio/projects/Rabble/scripts/makesweat_pipeline.py --historical
    else
        /opt/anaconda3/bin/python /Users/anna/Documents/GitHub/Portfolio/projects/Rabble/scripts/makesweat_pipeline.py
    fi
}

# Check if historical flag is passed
if [ "$1" == "--historical" ]; then
    echo "Running historical pipeline..."
    run_pipeline "historical"
else
    echo "Running weekly pipeline..."
    run_pipeline "weekly"
fi