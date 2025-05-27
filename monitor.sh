#!/bin/bash

# Default interval in seconds
INTERVAL=30

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -i|--interval)
            INTERVAL="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [-i|--interval SECONDS]"
            exit 1
            ;;
    esac
done

# Validate interval is a number
if ! [[ "$INTERVAL" =~ ^[0-9]+$ ]]; then
    echo "Error: Interval must be a positive integer"
    exit 1
fi

# Create directories if they don't exist
mkdir -p output/json
mkdir -p output/archives

# Function to get current Unix timestamp
get_timestamp() {
    date +%s
}

# Function to get current date in YYYY-MM-DD format
get_date() {
    date +"%Y-%m-%d"
}

# Function to archive JSON files
archive_files() {
    local date_str=$(get_date)
    local archive_name="output/archives/gas_prices_${date_str}.tar.gz"
    
    # Only create archive if there are files to archive
    if [ -n "$(ls -A output/json)" ]; then
        echo "Creating archive for ${date_str}..."
        tar -czf "$archive_name" -C output/json .
        rm -f output/json/*.json
        echo "Archive created: ${archive_name}"
    fi
}

# Get the date when we last archived
last_archive_date=$(get_date)

# Main loop
while true; do
    # Get current timestamp and date
    timestamp=$(get_timestamp)
    current_date=$(get_date)
    
    # Check if we need to archive (if date has changed)
    if [ "$current_date" != "$last_archive_date" ]; then
        archive_files
        last_archive_date=$current_date
    fi
    
    # Run the command and save output to timestamped file
    echo "Fetching gas prices at $(date -d @${timestamp})..."
    ./evm-gas --currencies all --json > "output/json/${timestamp}.json"
    
    # Wait for specified interval
    sleep $INTERVAL
done 