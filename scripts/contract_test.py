"""Call the live API and check each JSON response against the response schema in openapi.json.

Keeps the request count small (one call per operation and sample value) and pauses between calls.
Usage: python scripts/contract_test.py [--base https://betbetter.world]
"""
import argparse
import sys
import time

import jsonschema
import requests
from specutil import load_spec, operations, parameter, to_json_schema

SAMPLES = {"league": ["nfl", "nba", "soccer/epl"], "sport": ["nfl", "nhl"]}


def expand(path, spec, op):
    """Concrete URL paths for a templated path, using SAMPLES restricted to the enum in the spec."""
    urls = [path]
    for name, values in SAMPLES.items():
        if "{" + name + "}" not in path:
            continue
        p = parameter(spec, op, name)
        allowed = (p or {}).get("schema", {}).get("enum")
        values = [v for v in values if not allowed or v in allowed]
        urls = [u.replace("{" + name + "}", v) for u in urls for v in values]
    return urls


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=None)
    args = ap.parse_args()
    spec = load_spec()
    base = (args.base or spec["servers"][0]["url"]).rstrip("/")
    failures = checked = 0
    for path, method, op in operations(spec):
        if method != "get":
            continue
        js = op.get("responses", {}).get("200", {}).get("content", {}).get("application/json", {})
        schema = to_json_schema(spec, js["schema"]) if js.get("schema") else None
        for url_path in expand(path, spec, op):
            url = base + url_path + "?format=json"
            checked += 1
            try:
                resp = requests.get(url, timeout=90, headers={"User-Agent": "betbetter-openapi-contract-test"})
                ok = resp.status_code == 200 and "json" in resp.headers.get("Content-Type", "")
                if ok and schema:
                    jsonschema.validate(resp.json(), schema)
                print(("PASS " if ok else "FAIL ") + "%s %s -> %s" % (op.get("operationId"), url, resp.status_code))
                failures += 0 if ok else 1
            except jsonschema.ValidationError as exc:
                failures += 1
                print("FAIL %s %s schema: %s at /%s" % (op.get("operationId"), url, exc.message, "/".join(map(str, exc.absolute_path))))
            except Exception as exc:
                failures += 1
                print("FAIL %s %s: %s" % (op.get("operationId"), url, exc))
            time.sleep(1.0)
    print("%d checked, %d failed" % (checked, failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
