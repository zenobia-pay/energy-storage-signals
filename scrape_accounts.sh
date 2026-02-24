#!/bin/bash
# Scrape Twitter accounts for energy storage briefing

OUTFILE="twitter-accounts.jsonl"
LOGFILE="scrape-progress.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOGFILE"
}

add_account() {
    local handle="$1"
    local name="$2"
    local authorId="$3"
    local source="$4"
    
    # Check if already exists
    if ! grep -q "\"handle\":\"$handle\"" "$OUTFILE" 2>/dev/null; then
        echo "{\"handle\":\"$handle\",\"name\":\"$name\",\"authorId\":\"$authorId\",\"bio\":\"\",\"followers\":0,\"following\":0,\"source\":\"$source\"}" >> "$OUTFILE"
        return 0
    fi
    return 1
}

count_accounts() {
    wc -l < "$OUTFILE" 2>/dev/null || echo "0"
}

log "Starting energy storage Twitter scrape"
log "Target: 100,000 accounts"
touch "$OUTFILE"

