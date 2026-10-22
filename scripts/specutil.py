"""Shared helpers: load the spec, resolve local $refs, and turn an OpenAPI 3.0 schema into JSON Schema."""
import copy
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC_PATH = os.path.join(ROOT, "openapi.json")


def load_spec(path=SPEC_PATH):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def resolve(spec, node):
    """Follow a local '#/...' $ref until a concrete object is reached."""
    while isinstance(node, dict) and "$ref" in node:
        ref = node["$ref"]
        if not ref.startswith("#/"):
            raise ValueError("only local refs are supported: " + ref)
        target = spec
        for part in ref[2:].split("/"):
            target = target[part]
        node = target
    return node


def to_json_schema(spec, schema):
    """Inline $refs and map OpenAPI 3.0 'nullable: true' onto a JSON Schema null type."""
    schema = copy.deepcopy(resolve(spec, schema))
    if isinstance(schema, dict):
        if schema.pop("nullable", False) and "type" in schema:
            t = schema["type"]
            schema["type"] = (t if isinstance(t, list) else [t]) + ["null"]
        for key in ("properties", "patternProperties"):
            if key in schema:
                schema[key] = {k: to_json_schema(spec, v) for k, v in schema[key].items()}
        for key in ("items", "additionalProperties", "not"):
            if isinstance(schema.get(key), dict):
                schema[key] = to_json_schema(spec, schema[key])
        for key in ("allOf", "anyOf", "oneOf"):
            if key in schema:
                schema[key] = [to_json_schema(spec, s) for s in schema[key]]
        for key in ("example", "xml", "externalDocs", "discriminator", "readOnly", "writeOnly", "deprecated"):
            schema.pop(key, None)
    return schema


def operations(spec):
    """Yield (path, method, operation) for every operation in the spec."""
    for path, item in spec.get("paths", {}).items():
        for method, op in item.items():
            if method in ("get", "put", "post", "delete", "patch", "head", "options") and isinstance(op, dict):
                yield path, method, op


def parameter(spec, op, name):
    """The resolved parameter object called `name` on an operation, or None."""
    for p in op.get("parameters", []):
        p = resolve(spec, p)
        if p.get("name") == name:
            return p
    return None
