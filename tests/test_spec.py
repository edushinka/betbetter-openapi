"""Offline structural tests for openapi.json (no network)."""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
from openapi_spec_validator import validate  # noqa: E402
from specutil import load_spec, operations, resolve, to_json_schema  # noqa: E402

SPEC = load_spec()
OPS = list(operations(SPEC))
IDS = [op.get("operationId") for _, _, op in OPS]


def test_spec_is_valid_openapi():
    validate(SPEC)


def test_has_https_server_and_license():
    assert SPEC["servers"] and SPEC["servers"][0]["url"].startswith("https://")
    assert SPEC["info"]["license"]["name"]


def test_operation_ids_are_unique():
    assert all(IDS), "every operation needs an operationId"
    assert len(IDS) == len(set(IDS))


@pytest.mark.parametrize("path,method,op", OPS, ids=IDS)
def test_operation_documents_success_response(path, method, op):
    assert "200" in op["responses"]
    assert op.get("summary") or op.get("description")


@pytest.mark.parametrize("path,method,op", OPS, ids=IDS)
def test_path_parameters_are_declared(path, method, op):
    params = [resolve(SPEC, p) for p in op.get("parameters", [])]
    declared = {p["name"] for p in params if p.get("in") == "path"}
    templated = {seg[1:-1] for seg in path.split("/") if seg.startswith("{") and seg.endswith("}")}
    assert templated == declared


def test_component_schemas_convert_to_json_schema():
    for name, schema in SPEC.get("components", {}).get("schemas", {}).items():
        assert "$ref" not in str(to_json_schema(SPEC, schema)), name
