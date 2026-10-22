.PHONY: install validate test contract sync client-python

install:
	pip install -r requirements.txt

validate:
	python scripts/validate_spec.py

test:
	pytest -q

contract:
	python scripts/contract_test.py

sync:
	python scripts/sync_spec.py

# Generate a typed Python client with OpenAPI Generator (needs Docker)
client-python:
	docker run --rm -v "$(CURDIR):/local" openapitools/openapi-generator-cli generate -i /local/openapi.json -g python -o /local/out/python
