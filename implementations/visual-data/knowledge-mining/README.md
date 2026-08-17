# Knowledge mining with Azure AI Search

## Exercise

Reference implementation for the Microsoft knowledge-mining lab using an existing Azure AI Search index.

## Architecture

```text
Blob Storage -> indexer -> AI enrichment -> search index -> SearchClient
```

The enrichment pipeline can use AI skills such as key phrase extraction, person recognition, location recognition, and image OCR/tagging. The indexer and skillset create those enriched fields before the application queries them. `azure-search-app.py` queries the already-created `margies-index`; it does not create an index or upload/index documents from Python.

The query selects `title`, `locations`, `persons`, and `keyPhrases`, and orders results by `title`. The current Microsoft lab excludes knowledge-store steps.

## Files

- `microsoft-starter-search-app.py` preserves the Microsoft starter.
- `azure-search-app.py` validates `SEARCH_ENDPOINT`, `QUERY_KEY`, and `INDEX_NAME`, then queries the existing Search index.
- `documents/` contains the six public travel brochure PDFs used by the lab's ingestion workflow.
- `.env.example` contains placeholders only.
- `requirements.txt` preserves `azure-search-documents==11.6.0` and `python-dotenv`.

## Limitation

No real Azure AI Search/indexer query occurred because the required Azure resources and authentication are unavailable in Codespaces. No local workaround, index, document upload, or generated search result was created.

## Verification

- `azure-search-app.py` compiled and imported successfully; `SearchClient` and `AzureKeyCredential` APIs are available.
- Installed versions are `azure-search-documents 11.6.0` and `python-dotenv 1.2.2`, matching the pinned Search SDK requirement and the dotenv dependency.
- Missing `SEARCH_ENDPOINT`, `QUERY_KEY`, and `INDEX_NAME` each fail before client creation. The search flow selects `title`, `locations`, `persons`, and `keyPhrases`, ordered by `title`.
- All six brochure PDFs are present and non-empty.
- No real Azure Search/indexer query occurred.
