"""Fetch one league feed and print each selection.

Usage: python fetch_feed.py nfl
"""
import sys

import requests

league = sys.argv[1] if len(sys.argv) > 1 else "nfl"
resp = requests.get("https://betbetter.world/%s/picks" % league, params={"format": "json"}, timeout=60)
resp.raise_for_status()
feed = resp.json()
print("%s - %s selections (updated %s)" % (feed.get("sport"), feed.get("count"), feed.get("updatedUtc")))
for pick in feed.get("picks") or []:
    print(pick)
