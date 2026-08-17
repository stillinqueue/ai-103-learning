# Analyze images with Azure Content Understanding

## Exercise

**Analyze images with Azure Content Understanding**.

## Architecture

```text
image bytes -> Content Understanding analyzer -> structured analysis result
```

The analyzer is configured separately in Content Understanding Studio. The Python client references the already-built analyzer through `ANALYZER`; it does not define the schema on every request.

## Custom schema

The Microsoft exercise defines:

- `Description`: String, generated image description.
- `Tags`: List of Strings, generated image tags.

Content Understanding converts unstructured image content into application-friendly structured fields useful for indexing, search, automation, and metadata.

## Async API and SDK types

`ContentUnderstandingClient` uses `AnalysisInput` to submit image bytes and returns a long-running poller from `begin_analyze(...)`. `poller.result()` waits for the completed `AnalysisResult`. The implementation reads `Description` through `value_string` and iterates `Tags` through `value_array`, reading each tag's `value_string`.

## Endpoint and resources

The endpoint is the Foundry resource endpoint:

```text
https://<resource>.services.ai.azure.com
```

It is not an Azure OpenAI `/openai/v1/` endpoint and not a Foundry project `/api/projects/...` endpoint. The complete Microsoft lab requires a Foundry project, Content Understanding configuration, Azure Storage, an underlying deployed model, a Content Understanding project, and a built/published analyzer. The `Description`/`Tags` schema is configured on the resource side.

## Files

- `microsoft-starter-analyze-image.py` preserves the Microsoft starter and TODOs.
- `azure-analyze-image.py` completes the Azure Content Understanding client, async analysis, error handling, and field extraction.
- `images/` contains the three public Microsoft sample images.
- `.env.example` contains placeholder configuration only.
- `requirements.txt` preserves the Microsoft package names.

## Codespaces limitation

Azure CLI / Entra authentication is blocked by tenant security defaults, and the required analyzer, storage, project, and model resources cannot be provisioned through the current Codespaces authentication path. Security settings will not be weakened, and blocked authentication will not be repeatedly retried. The official implementation is preserved as reference code, and no analyzer runtime success is claimed unless a real Content Understanding call succeeds. No local workaround is created.

## Verification

### SDK and configuration

- `azure-analyze-image.py` passed `python -m py_compile`.
- Installed `azure-ai-contentunderstanding` version is `1.1.0`; `azure-identity 1.25.3` and `python-dotenv 1.2.2` are available.
- `ContentUnderstandingClient`, `AnalysisInput`, `AnalysisResult`, `AzureError`, and `DefaultAzureCredential` imported successfully. The client exposes `begin_analyze(...)` with `analyzer_id` and `inputs`.
- `ENDPOINT` and `ANALYZER` validation fails clearly before client creation or analysis: `ENDPOINT is required` and `ANALYZER is required`.
- The implementation uses API version `2025-11-01` and expects the Foundry resource endpoint `https://<resource>.services.ai.azure.com`.

### Structured schema and samples

- All three public sample images loaded successfully as bytes and were accepted by local `AnalysisInput(data=...)` construction.
- Local fake-result verification confirmed `Description` uses `value_string` and `Tags` iterates `value_array`, reading each tag's `value_string`.
- No real Azure Content Understanding analyzer request was executed. Runtime requires a built/published analyzer and Azure authentication/resources.

### Local workaround

No local workaround was created. A plain multimodal description script would duplicate Module 1 and would not validate a published analyzer, custom schema enforcement, `ContentUnderstandingClient`, or long-running poller behavior.
