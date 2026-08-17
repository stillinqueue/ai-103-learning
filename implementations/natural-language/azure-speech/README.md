# Recognize and synthesize speech

## Exercise

**Recognize and synthesize speech** with Azure Speech in Foundry Tools.

## Architecture

```text
Python app -> Azure Speech SDK -> Azure Speech in Foundry Tools
```

## Speech synthesis

The greeting path uses:

- `SpeechConfig`
- `AudioOutputConfig`
- `SpeechSynthesizer`
- `speak_text_async`
- voice `en-US-Serena:DragonHDLatestNeural`
- output file `greeting.wav`

## Speech recognition

The message path uses:

- `AudioConfig` for each file in `messages/`
- `SpeechRecognizer`
- `recognize_once_async`
- `ResultReason.RecognizedSpeech` before printing `result.text`

## Files and configuration

- `microsoft-starter-voice-mail.py` preserves the Microsoft starter and TODOs.
- `azure-voice-mail.py` is the completed Azure Speech SDK implementation.
- `messages/` contains the two Microsoft sample voice messages.
- `.env.example` contains placeholder configuration only.
- `requirements.txt` preserves the Microsoft dependency versions, including `azure-cognitiveservices-speech==1.48.2`.

`DefaultAzureCredential` is used with the Foundry Cognitive Services endpoint from `FOUNDRY_ENDPOINT`. The Microsoft lab expects `az login` before runtime, but no authentication is attempted in this Codespace.

## Important distinction

- Module 3 uses generative speech models through `AzureOpenAI`.
- Module 4 uses the Azure Speech SDK.
- Both can support speech-to-text and text-to-speech, but they use different services and client APIs.
- The Azure Speech SDK is specialized for speech capabilities.

## Codespaces limitation

Azure CLI / Entra authentication is blocked by tenant security defaults. Security settings will not be weakened, and blocked authentication will not be repeatedly retried. The official Azure code is preserved as reference code, and no Azure runtime success is claimed unless a real request succeeds. No local workaround is created for this exercise because Module 3 already provides local OpenAI TTS/STT practice; duplicating it here would not demonstrate Azure Speech SDK behavior.

This module has structural verification only; Azure Speech runtime execution remains unavailable.

## Verification

### Structural verification

- `azure-voice-mail.py` passed `python -m py_compile`.
- `DefaultAzureCredential` and `azure.cognitiveservices.speech` imported successfully.
- Installed Speech SDK version: `azure-cognitiveservices-speech 1.48.2`, matching the Microsoft requirement.
- The installed SDK exposes `SpeechConfig`, `SpeechSynthesizer`, `SpeechRecognizer`, `AudioOutputConfig`, `AudioConfig`, `ResultReason.SynthesizingAudioCompleted`, and `ResultReason.RecognizedSpeech`.
- `messages/message_1.wav` and `messages/message_2.wav` were found. `greeting.wav` is configured only as generated output, not source input.
- Missing `FOUNDRY_ENDPOINT` produces `FOUNDRY_ENDPOINT is required` before any Azure Speech operation.

### Runtime status

No real Azure Speech synthesis or recognition request was executed. Azure authentication and the required Cognitive Services endpoint remain unavailable in this Codespace.

### FOUNDRY_KEY note

The Microsoft starter includes and reads `FOUNDRY_KEY`, but the completed Entra-based implementation uses `DefaultAzureCredential` with `SpeechConfig(token_credential=..., endpoint=...)` and `FOUNDRY_ENDPOINT`. The key is therefore not used by this implementation; the Microsoft reference starter was preserved rather than altered to hide the difference.
