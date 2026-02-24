#!/bin/bash
# Scrape a batch of Twitter accounts
# Usage: ./scrape-twitter-batch.sh <start_line> <end_line> <output_dir>

START=$1
END=$2
OUTPUT_DIR=$3
DATE=$(date +%Y-%m-%d)

ACCOUNTS_FILE="twitter-accounts.jsonl"

# Extract handles for this batch
HANDLES=$(cat "$ACCOUNTS_FILE" | jq -r '.handle' | sed -n "${START},${END}p")

echo "Scraping accounts $START to $END..."
echo "Output: $OUTPUT_DIR"

for handle in $HANDLES; do
    echo "Scraping @$handle..."
    OUTPUT_FILE="$OUTPUT_DIR/${handle}.json"
    
    # Skip if already scraped today
    if [ -f "$OUTPUT_FILE" ]; then
        echo "  Already scraped, skipping"
        continue
    fi
    
    # Scrape with bird, get last 20 tweets as JSON
    bird user-tweets "$handle" -n 20 --json > "$OUTPUT_FILE" 2>/dev/null
    
    # Check if successful
    if [ $? -eq 0 ] && [ -s "$OUTPUT_FILE" ]; then
        TWEET_COUNT=$(cat "$OUTPUT_FILE" | jq 'length' 2>/dev/null || echo "0")
        echo "  Got $TWEET_COUNT tweets"
    else
        echo "  Failed or empty"
        rm -f "$OUTPUT_FILE"
    fi
    
    # Rate limit: 1 second between requests
    sleep 1
done

echo "Batch $START-$END complete"
