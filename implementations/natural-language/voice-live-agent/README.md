# Develop a Voice Live agent

## Exercise

**Develop a Voice Live agent**.

## Architecture

```text
Microphone -> Voice Live SDK -> Foundry agent -> Voice Live SDK -> speaker
```

This is a persistent real-time conversation session, not a sequence of independent audio-file requests. The Voice Live SDK streams microphone audio to the connected Foundry agent and streams response audio back to the speaker.

## Core API and session flow

`azure-voice-live-client.py` preserves the official sequence:

1. `connect(...)` opens the asynchronous Voice Live connection.
2. `AgentConfig` identifies the existing Foundry project/agent.
3. `AudioProcessor` manages microphone capture and speaker playback.
4. `RequestSession` configures text/audio modalities, PCM formats, semantic multilingual VAD, echo cancellation, and noise reduction.
5. The asynchronous server event loop handles transcripts, response audio, completion, interruption, and errors.

The client uses `AzureCliCredential` from `azure.identity.aio`, `azure.ai.voicelive.aio.connect`, and Voice Live API version `2026-01-01-preview`.

## Real-time audio concepts

- Voice Activity Detection determines conversational turns.
- Noise reduction helps clean microphone input.
- Echo cancellation helps prevent playback from being interpreted as new input.
- Interruption/barge-in clears queued response audio when the user starts speaking.
- Audio is streamed continuously rather than handled only as independent files.

## Files and configuration

- `microsoft-starter-chat-client.py` preserves the Microsoft starter and TODOs.
- `azure-voice-live-client.py` completes the official `VoiceAssistant.start()` flow and preserves the audio/event helper classes.
- `.env.example` contains placeholders only.
- `requirements.txt` preserves the local Microsoft starter requirements: `dotenv`, `aiohttp`, and `pyaudio`.

The starter expects:

- `AZURE_VOICELIVE_ENDPOINT`: base Voice Live/Foundry resource endpoint.
- `AZURE_VOICELIVE_PROJECT_NAME`: Foundry project name.
- `AZURE_VOICELIVE_AGENT_ID`: agent identifier, with the starter instructions referring to `chat-agent`/`Chat-Agent` using inconsistent casing.

The exercise instructions also install preview packages separately: `azure-ai-voicelive==1.2.0b4 --pre` and `azure-ai-projects==2.0.0b4`. Those packages are not present in the starter's local `requirements.txt`, so the copied requirements file remains the source of truth and the difference is documented here.

## Authentication and runtime limits

The official lab requires a Foundry project, existing agent, suitable deployed model, Voice mode/Voice Live enabled, Azure authentication, microphone access, speaker playback, and a Voice Live-compatible environment. Azure CLI/Entra authentication is blocked by tenant security defaults in this Codespace. Browser-based Codespaces may also lack the desktop microphone/speaker environment expected by the lab.

Security settings will not be weakened, authentication will not be repeatedly retried, and no Voice Live connection or audio runtime is claimed. The Microsoft implementation is preserved as reference code.

## Verification

### Structural verification

- `azure-voice-live-client.py` passed `python -m py_compile`.
- The official preview packages `azure-ai-voicelive==1.2.0b4 --pre` and `azure-ai-projects==2.0.0b4` were installed for static API validation; `azure-identity` and `aiohttp` are available.
- `azure.ai.voicelive.aio.connect` and all required model symbols imported successfully. `connect` accepts `endpoint`, `credential`, `api_version`, and `agent_config`.
- Missing `AZURE_VOICELIVE_ENDPOINT`, `AZURE_VOICELIVE_AGENT_ID`, and `AZURE_VOICELIVE_PROJECT_NAME` each produce a clear validation error before opening a Voice Live connection.
- `pyaudio` could not be installed because the environment lacks the native `portaudio.h` header. No repeated native build attempts were made.

### Agent-name and endpoint notes

- The official instructions use `chat-agent` during agent creation and later mention `Chat-Agent`; agent names are case-sensitive. The actual configured agent name must be used exactly in `AZURE_VOICELIVE_AGENT_ID`.
- `AZURE_VOICELIVE_ENDPOINT` should be the base Voice Live/Foundry resource endpoint, not a project URL with an `/api/projects/...` suffix.

### Runtime status

No real Voice Live connection occurred. No microphone capture, speaker playback, interruption/barge-in, or other audio behavior was runtime-tested. Browser Codespaces may not provide the direct microphone/speaker environment expected by the desktop-style lab, and Azure CLI authentication is blocked by tenant policy.

### Local workaround

No local workaround was created. A fake real-time audio loop would not validate Voice Live semantics or the expected microphone/speaker environment.
