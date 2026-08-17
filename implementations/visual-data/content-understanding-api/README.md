# Content Understanding API client

## Exercise distinction

- **Exercise 01** is Foundry/Content Understanding Studio analyzer design.
- **Exercise 02** is the Python SDK exercise that creates and consumes a published analyzer.

This module preserves the Exercise 02 business-card workflow and does not mix it with the Studio-only Exercise 01 implementation.

## Schema and operations

`biz-card.json` defines the business-card fields:

- `Company`
- `Name`
- `Title`
- `Email`
- `Phone`

`azure-create-analyzer.py` loads that schema and uses `begin_create_analyzer(...)` with `AzureKeyCredential`, `ANALYZER_NAME`, `resource=json.loads(schema)`, and `allow_replace=True`. `azure-read-card.py` uses `begin_analyze_binary(...)` on `biz-card-1.png` by default, or another filename supplied on the command line, then saves the full response to `results.json` and prints extracted fields.

Both `begin_*` methods are long-running operations; `.result()` uses the SDK poller to wait for completion.

## Authentication and limitation

This SDK exercise uses `AzureKeyCredential`, unlike the earlier Entra-based Content Understanding implementation. `ENDPOINT`, `KEY`, and `ANALYZER_NAME` are validated before client creation. No real key or `.env` is included.

The Azure runtime cannot currently be executed because usable Content Understanding resource credentials/configuration are unavailable in Codespaces. No analyzer creation or business-card extraction is claimed as successful, and no `results.json` was generated.

## Verification

- Both completed clients compiled successfully and the required SDK imports loaded.
- Installed versions are `azure-ai-contentunderstanding 1.1.0` and `python-dotenv 1.2.2`. The SDK exposes `begin_create_analyzer(...)` and `begin_analyze_binary(...)` with the parameters used here.
- `biz-card.json` parses and contains `Company`, `Name`, `Title`, `Email`, and `Phone`; both business-card PNGs are readable and non-empty.
- Missing `ENDPOINT`, `KEY`, and `ANALYZER_NAME` each fail clearly before client creation in both scripts.
- No analyzer was created, no card was analyzed, and no `results.json` was generated.
