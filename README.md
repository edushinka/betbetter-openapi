# betbetter-openapi

OpenAPI 3.0 description of the Bet Better JSON feeds, with tooling to validate the spec, test it against the live
service and generate clients.

| Path | Returns |
|---|---|
| `GET /{league}/picks?format=json` | Model selections for a league (probability, fair decimal odds, verdict) |
| `GET /{league}/prop-bets?format=json` | Player-prop selections for a league |
| `GET /{league}/best-bets?format=json` | The day's highest-rated selections for a league |
| `GET /predicted-scores/{sport}?format=json` (or `csv`) | Model predicted scores per game |
| `GET /results?format=json`, `GET /scorecard?format=json` | Graded results feeds |

`openapi.json` mirrors the published spec at https://betbetter.world/api/openapi.json (`make sync` refreshes it).

## Layout

```
openapi.json              the spec
scripts/validate_spec.py  validate against the OpenAPI 3.0 schema
scripts/contract_test.py  call the live endpoints and check responses against the spec's schemas
scripts/sync_spec.py      pull the published spec and report added / removed paths
scripts/specutil.py       $ref resolution and OpenAPI-to-JSON-Schema conversion used by the scripts
tests/                    offline structural tests (pytest)
examples/                 minimal clients in Python, JavaScript (Node 18+) and shell
.github/workflows/        CI: validation + tests on every push, contract tests weekly
```

## Usage

```sh
make install         # pip install -r requirements.txt
make validate        # the spec is valid OpenAPI
make test            # offline tests
make contract        # live contract tests (about 10 requests, 1 s apart)
make sync            # refresh openapi.json from the published spec
make client-python   # generate a Python client with openapi-generator (Docker)
```

No API key is needed. Responses carry model output only, with no bookmaker prices. Data licence: CC BY 4.0 with
attribution. Code in this repository: MIT (see `LICENSE`). The data is model estimates for research, not betting
advice; 18+.

Related clients: [betbetter-python](https://github.com/edushinka/betbetter-python),
[betbetter-r](https://github.com/edushinka/betbetter-r), [betbetter-mcp](https://github.com/edushinka/betbetter-mcp).
