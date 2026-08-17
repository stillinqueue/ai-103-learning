# Analyze Text

## Exercise

**Analyze text with Azure Language in Foundry Tools**.

## Core concepts

- Language detection with `detect_language`
- Named Entity Recognition (NER) with `recognize_entities`
- Personally Identifiable Information (PII) detection with `recognize_pii_entities`
- Service-provided PII redaction

## Files

- `microsoft-starter-text-analysis.py` is the preserved Microsoft Learn starter with its TODOs.
- `azure-text-analysis.py` is the completed official Azure SDK implementation pattern.
- `reviews/` contains the Microsoft sample hotel review text files.
- `.env.example` contains placeholder configuration only.
- `requirements.txt` preserves the Microsoft dependency versions, including `azure-ai-textanalytics==5.3.0`.

## Azure SDK mental model

`TextAnalyticsClient` is the Azure Language service client. The application sends review text to specialized NLP service operations: `detect_language`, `recognize_entities`, and `recognize_pii_entities`. These are specialized Azure Language APIs, not general LLM prompting.

## Codespaces limitation

The official Microsoft exercise expects Azure authentication through `DefaultAzureCredential`, with Azure CLI login as part of the lab workflow. In this Codespace, Azure CLI / Entra device-code authentication is blocked by tenant security defaults. We will not weaken those security settings or repeatedly retry blocked authentication.

The official Azure implementation is preserved as reference code until compatible Azure authentication and resources are available. `openai-text-analysis.py` is a separate local/OpenAI approximation for runnable practice; it is not Azure Language and does not prove that this Azure SDK implementation ran successfully.

The current Microsoft instructions recommend Python 3.13.x because some dependencies may not yet support Python 3.14. The Codespace Python version is not changed by this exercise.

The exercise is documented and locally verified, but the Azure service path is not runtime-verified because no Azure Language request succeeded.

## Verification

### Azure implementation

- `azure-text-analysis.py` compiled successfully with `python -m py_compile`.
- `DefaultAzureCredential`, `TextAnalyticsClient`, and `dotenv` imports loaded successfully.
- All five review files were discoverable.
- With `FOUNDRY_ENDPOINT` absent, the script failed clearly with `ValueError: FOUNDRY_ENDPOINT is required` before creating a client or making a service request.
- No real Azure Language service call was executed. The Codespace lacks a configured endpoint and supported Azure authentication is blocked by the current tenant security defaults.

### Local OpenAI approximation

[`openai-text-analysis.py`](openai-text-analysis.py) ran successfully against all five review files. Each response parsed as strict JSON and included detected language, ISO language code, named entities, PII entities, and redacted text.

The captured practice run detected English (`en`) for reviews 1 through 4 and French (`fr`) for review 5. It identified an email address in review 1 and `John Smith` as a person in review 2, with redacted text returned for those reviews. Reviews 3, 4, and 5 returned no PII entities in the captured run. No runtime errors occurred.

The OpenAI practice implementation is not Azure Language and does not count as successful execution of the Azure Language service. Its entity categories and redaction behavior are practice approximations and are not asserted to match Azure Language categories or results.
