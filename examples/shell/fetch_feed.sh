#!/usr/bin/env sh
# Fetch one league feed and pretty-print it. Usage: ./fetch_feed.sh nhl
league="${1:-nhl}"
curl -fsS "https://betbetter.world/${league}/picks?format=json" | python3 -m json.tool
