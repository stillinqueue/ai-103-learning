# Use speech-capable generative AI models

## Exercise

**Use speech-capable generative AI models**.

## Two scenarios

- **Text-to-speech / speech synthesis**: `generate-speech/azure-generate-speech.py` generates speech and streams it to `speech.mp3`.
- **Speech-to-text / transcription**: `transcribe-speech/azure-transcribe-speech.py` submits the Microsoft `speech.wav` sample and prints the transcription.

## Architecture

```text
Python app -> AzureOpenAI client -> Azure-hosted speech-capable model deployment
```

Both applications use `DefaultAzureCredential` with `get_bearer_token_provider` to obtain Azure authentication for the `AzureOpenAI` client. The model deployment is selected through `MODEL_NAME`, and the model endpoint is supplied through `MODEL_ENDPOINT`.

## Main APIs

Speech generation uses:

```python
client.audio.speech.with_streaming_response.create(...)
```

Speech transcription uses:

```python
client.audio.transcriptions.create(...)
```

The preserved Microsoft requirements are identical for both apps: `python-dotenv`, `playsound3`, `azure-identity`, and `openai`.

## Files

- `generate-speech/microsoft-starter-generate-speech.py` is the preserved Microsoft starter.
- `generate-speech/azure-generate-speech.py` is the completed Azure speech-synthesis pattern.
- `generate-speech/.env.example` contains placeholders only.
- `transcribe-speech/microsoft-starter-transcribe-speech.py` is the preserved Microsoft starter.
- `transcribe-speech/azure-transcribe-speech.py` is the completed Azure transcription pattern.
- `transcribe-speech/.env.example` contains placeholders only.
- `transcribe-speech/speech.wav` is the Microsoft sample audio input.

## Important distinction

This lab uses generative AI speech-capable models through the OpenAI SDK and an Azure-hosted `AzureOpenAI` client. It is distinct from the classic Azure AI Speech SDK/service APIs.

## Azure limitations in this Codespace

The official exercise requires a Microsoft Foundry project, deployed speech-generation and speech-transcription models, model target URIs, and Azure authentication. Azure CLI / Entra authentication is blocked by tenant security defaults in this Codespace. Security settings will not be weakened, and Azure authentication will not be repeatedly retried.

The official Azure implementations are preserved as reference code and are not claimed to have run successfully unless a real Azure request succeeds. The separate OpenAI API practice implementations are useful for similar speech concepts, but they do not verify Azure Foundry or Azure-hosted model behavior and are labelled separately.

The module is recorded as completed in the learning-path tracker based on the implemented and locally verified exercise patterns. Azure-hosted runtime execution remains unavailable in this Codespace.

## Verification

### Azure implementation

- Both Azure implementations passed `python -m py_compile`.
- Azure imports for `AzureOpenAI`, `DefaultAzureCredential`, `get_bearer_token_provider`, `openai`, and `dotenv` loaded successfully.
- Missing `MODEL_ENDPOINT` reports `MODEL_ENDPOINT is required` before any client or model request.
- Missing `MODEL_NAME` reports `MODEL_NAME is required` before any client or model request.
- No Azure request occurred because Azure authentication, endpoint access, and model deployments are unavailable in this Codespace.

### Local OpenAI practice

- `generate-speech/openai-generate-speech.py` ran successfully with `gpt-4o-mini-tts` and voice `alloy`.
- It generated `generate-speech/openai-speech.mp3`, which was non-empty at 41,088 bytes; the generated output was removed as a transient artifact after verification.
- `transcribe-speech/openai-transcribe-speech.py` ran successfully against the Microsoft `speech.wav` sample.
- The exact captured transcription was: `Oh man, on the other side of the screen, it all looks so easy.`
- No optional round-trip transcription of the generated MP3 was performed.

The local OpenAI practice implementations demonstrate speech generation/transcription concepts but do not verify Azure-hosted speech model deployments or Azure authentication.
