# Changelog

## 1.3.1 (2026-10-22)
- Fix: `/predicted-scores/{sport}` JSON is an object (`sport`, `source`, `page`, `games[]`), not a bare array; rows gain
  `margin_source`. Found by `scripts/contract_test.py`.

## 1.3.0 (2026-10-22)
- Spec synced with the published version: adds `/{league}/best-bets` and `/predicted-scores/{sport}` (JSON and CSV).
- Added tooling: spec validation, offline structural tests, live contract tests, examples (Python, JavaScript, shell),
  CI workflow and a Makefile.

## 1.1.0 (2026-08-26)
- First published spec: `/{league}/picks`, `/{league}/prop-bets`, `/results`, `/scorecard`.
