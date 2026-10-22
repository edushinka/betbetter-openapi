"""Validate openapi.json against the OpenAPI specification. Exit code 1 on any error."""
import sys

from openapi_spec_validator import validate
from specutil import SPEC_PATH, load_spec


def main():
    spec = load_spec()
    try:
        validate(spec)
    except Exception as exc:  # the validator raises a subclass of OpenAPIValidationError
        print("INVALID " + SPEC_PATH + ": " + str(exc))
        return 1
    print("OK %s - OpenAPI %s, version %s, %d paths" % (SPEC_PATH, spec["openapi"], spec["info"]["version"], len(spec["paths"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
