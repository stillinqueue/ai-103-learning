# Azure Document Intelligence

## Exercise

**Analyze documents with Azure Document Intelligence**.

## Models and architecture

- **Read model**: OCR/text extraction with optional language detection.
- **Prebuilt model**: ready-made schema for common documents such as invoices.
- **Custom model**: trained for organization-specific forms and fields.

`DocumentIntelligenceClient` submits a document to `begin_analyze_document(...)`, a long-running operation. `.result()` waits for poller completion.

## Implementations

- `azure-prebuilt-invoice.py` uses `AzureKeyCredential`, `DocumentIntelligenceClient`, `AnalyzeDocumentRequest`, and `prebuilt-invoice` to print only `VendorName`, `CustomerName`, `InvoiceTotal`, and confidence values from the Microsoft sample invoice.
- `azure-custom-model-test.py` uses `AzureKeyCredential`, the configured `MODEL_ID`, and the Microsoft `test1.jpg` sample. It prints only fields returned by the custom model; it does not invent a trained model or field names.
- `microsoft-starter-document-analysis.py` and `microsoft-starter-test-model.py` preserve the Microsoft starters.
- `requirements-prebuilt.txt` and `requirements-custom.txt` preserve the distinct source requirements files.
- `samples/` contains the public sample invoice and custom test form.

Custom model training requires Blob Storage, Document Intelligence Studio, and a trained custom model ID. Those resources are not created here.

## Authentication and limitation

This lab uses `AzureKeyCredential`, unlike earlier Entra-based examples. The environment example contains placeholders for both starter configuration patterns. No real keys or `.env` files are included.

No Azure runtime is claimed because Document Intelligence resources, credentials, and custom-model training setup are unavailable in Codespaces. No local OpenAI workaround was created.

## Verification

- Both completed clients compiled successfully and the required SDK imports loaded.
- Installed versions are `azure-ai-documentintelligence 1.0.2` and `python-dotenv 1.2.2`. `DocumentIntelligenceClient` exposes the `begin_analyze_document(...)` poller API used here.
- The prebuilt flow uses `prebuilt-invoice`, `AnalyzeDocumentRequest(url_source=...)`, `.result()`, and the requested invoice fields/confidence values. The custom flow uses the configured `MODEL_ID`, `AnalyzeDocumentRequest(bytes_source=...)`, `.result()`, and iterates only fields returned by the model.
- Missing endpoint/key/model configuration fails clearly before client creation in both scripts; both sample assets are readable and non-empty.
- No Azure Document Intelligence request, custom-model training, or `results.json` generation occurred.
