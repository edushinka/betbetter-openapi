"""Download the published spec and overwrite openapi.json when it changed. Prints the paths added and removed."""
import json
import sys

import requests
from specutil import SPEC_PATH, load_spec

LIVE_URL = "https://betbetter.world/api/openapi.json"


def main():
    resp = requests.get(LIVE_URL, timeout=60, headers={"User-Agent": "betbetter-openapi-sync"})
    resp.raise_for_status()
    live = resp.json()
    local = load_spec()
    if live == local:
        print("openapi.json is up to date (version %s)" % local["info"]["version"])
        return 0
    added = sorted(set(live["paths"]) - set(local["paths"]))
    removed = sorted(set(local["paths"]) - set(live["paths"]))
    with open(SPEC_PATH, "w", encoding="utf-8", newline="\n") as f:
        json.dump(live, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("updated %s -> %s; paths added %s, removed %s" % (local["info"]["version"], live["info"]["version"], added, removed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
