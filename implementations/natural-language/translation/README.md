# Translate text and speech

## Exercise

**Translate text and speech**.

## Text translation

```text
Python app -> Azure Translator -> translated text
```

`azure-translate-text.py` uses `TextTranslationClient`, `get_supported_languages`, automatic source-language detection, and `translate(...)`. The user selects a supported target language code, then enters text until `quit`.

## Speech translation

```text
Microphone -> TranslationRecognizer -> translated text -> SpeechSynthesizer -> speaker
```

`azure-translate-speech.py` uses `SpeechTranslationConfig`, `TranslationRecognizer`, source language `en-US`, and target languages `fr`, `es`, and `hi`. Translated speech uses:

- French: `fr-FR-HenriNeural`
- Spanish: `es-ES-ElviraNeural`
- Hindi: `hi-IN-MadhurNeural`

## Important distinction

Text translation uses Azure Translator. Speech translation uses Azure Speech. Translation is not transcription: transcription converts speech to text in the same language, while translation converts content from one language to another. Speech translation can combine recognition, translation, and synthesis.

## Files and authentication

- `microsoft-starter-translate-text.py` and `microsoft-starter-translate-speech.py` preserve the Microsoft starters and TODOs.
- `azure-translate-text.py` is the completed Azure Translator client.
- `azure-translate-speech.py` is the completed Azure Speech translation client.
- `.env.example` contains placeholder configuration only.
- `requirements.txt` preserves the Microsoft dependency versions.

Both services use the Foundry Cognitive Services endpoint in this format:

```text
https://<resource>.cognitiveservices.azure.com/
```

Both implementations use `DefaultAzureCredential`. No local workaround is created yet.

## Codespaces limitation

Azure CLI / Entra authentication is blocked in this Codespace, and browser Codespaces do not provide the desktop microphone/speaker workflow expected by the speech exercise. The official Azure implementations are preserved as reference code, and no runtime verification is claimed unless a real Azure request succeeds. Microphone and speaker access are not attempted here.

This module has structural verification only; no Azure translation runtime was executed.

## Verification

### Text Translator

- `azure-translate-text.py` passed `python -m py_compile`.
- `DefaultAzureCredential`, `TextTranslationClient`, and `InputTextItem` imported successfully.
- Installed `azure-ai-translation-text 1.0.1` exposes `get_supported_languages` and `translate` with the parameters used here.
- Missing `FOUNDRY_ENDPOINT` reports `FOUNDRY_ENDPOINT is required` before client creation or a Translator request.
- No real Azure Translator call occurred.

### Speech translation

- `azure-translate-speech.py` passed `python -m py_compile`.
- Speech SDK imports loaded successfully, including `SpeechTranslationConfig`, `TranslationRecognizer`, `SpeechConfig`, `SpeechSynthesizer`, `AudioConfig`, and `ResultReason`.
- The configured source/target flow is internally consistent: `en-US` input, `fr`/`es`/`hi` translations, and `fr-FR-HenriNeural`/`es-ES-ElviraNeural`/`hi-IN-MadhurNeural` voices.
- Missing `FOUNDRY_ENDPOINT` reports `FOUNDRY_ENDPOINT is required` before Speech client creation, microphone access, or a Speech request.
- No microphone, speaker, or real Azure Speech translation call occurred.

### Local workaround

No local workaround was created. A plain OpenAI translation implementation would duplicate prior local exercises and would not validate `TextTranslationClient`, `SpeechTranslationConfig`, `TranslationRecognizer`, or the Azure Speech synthesis voices.

### Runtime limitation

Azure authentication remains blocked by tenant security defaults, and browser Codespaces is not the expected microphone/speaker environment. The official implementations are preserved as reference code, and no Azure runtime success is claimed.
