# Use Azure Speech in an agent

## Exercise

**Use Azure Speech in an agent**.

## Architecture

```text
Python client -> Foundry Agent -> Azure Speech MCP server -> Azure Speech
```

The Python client does not call the Azure Speech SDK directly. It targets an existing Foundry agent named `speech-agent`; that agent is configured in Foundry with an Azure Speech MCP server connection. The agent interprets the prompt and invokes the relevant connected tool for speech synthesis or transcription.

## Foundry agent and MCP

The Microsoft lab expects an existing `speech-agent` with instructions indicating that it uses Azure Speech for transcription and synthesis. The Azure Speech MCP server exposes speech capabilities as agent tools, including:

- synthesize speech
- transcribe speech

The Foundry playground may request approval before invoking Azure Speech MCP tools. Tool availability is not tool execution: the agent must choose and invoke the connected MCP capability for a request.

The Python client uses `AIProjectClient`, `DefaultAzureCredential`, `get_openai_client()`, and `agent_reference` to target the existing agent. It does not use `SpeechSynthesizer`, `SpeechRecognizer`, or `OPENAI_API_KEY`.

## Azure Blob Storage

The Azure Speech MCP synthesis flow generates audio files, so the exercise uses an Azure Blob Storage container to persist and retrieve those files. The MCP connection receives a container SAS URL with the required permissions for the server to upload speech output and return downloadable results. No SAS URL, token, or storage secret is included here.

## Authentication

There are two separate authentication relationships:

1. **Python client -> Foundry project**: `DefaultAzureCredential`.
2. **Foundry MCP connection -> Azure Speech**: the official exercise shows key-based configuration and notes that Entra authentication may be used when key-based authentication is disabled by policy.

These are distinct authentication patterns and should not be collapsed into one mechanism.

## Files

- `speech-client/microsoft-starter-speech-client.py` is the preserved Microsoft starter with TODOs.
- `speech-client/azure-speech-agent-client.py` is the completed client pattern.
- `speech-client/.env.example` contains placeholder configuration only.
- `speech-client/requirements.txt` preserves the Microsoft dependencies.
- `speech-client/samples/speech_1.wav` and `speech_2.wav` are public Module 5 sample assets copied for reference.

## Mental model

- Module 3: app -> `AzureOpenAI` speech model
- Module 4: app -> Azure Speech SDK
- Module 5: app -> Foundry agent -> Azure Speech MCP
- MCP exposes speech capabilities as agent tools.
- The agent interprets the prompt and invokes speech tools.
- Generated speech may require external file storage.

## Codespaces limitation

Complete Microsoft runtime execution requires an Azure subscription and resources, a Foundry project, a deployed `speech-agent`, an Azure Speech MCP connection, an Azure Storage container, appropriate MCP authentication, and Azure authentication from the Python client.

Azure CLI / Entra authentication is blocked by tenant security defaults in this Codespace. Security settings will not be weakened, and blocked authentication will not be repeatedly retried. The official architecture is preserved as reference code; no runtime success is claimed unless a real agent/MCP request succeeds. No Azure resources, storage account, SAS token, Foundry agent, or MCP connection is created by this implementation.

This module has structural verification only; no Azure Speech MCP runtime execution occurred.

## Verification

### Structural verification

- `speech-client/azure-speech-agent-client.py` passed `python -m py_compile`.
- `DefaultAzureCredential`, `AIProjectClient`, and `dotenv` imports loaded successfully.
- Installed SDK versions are `azure-ai-projects 2.3.0`, `azure-identity 1.25.3`, and `python-dotenv 1.2.2`; the Microsoft requirements preserve `azure-ai-projects==2.0.0b4`.
- The installed `AIProjectClient(endpoint, credential)` constructor and `get_openai_client()` method are compatible with this client pattern. The installed OpenAI Responses API exposes `input` and `extra_body`, including the `agent_reference` payload used by the Microsoft exercise.
- Missing `FOUNDRY_ENDPOINT` reports `FOUNDRY_ENDPOINT is required` before client creation.
- Missing `AGENT_NAME` reports `AGENT_NAME is required` before client creation.

### Runtime status

No real Foundry agent call occurred. No Azure Speech MCP tool call occurred. No Blob Storage operation occurred, and no SAS URL or token was created or used.

### Local workaround decision

No local workaround was created. A simple OpenAI speech script would duplicate the completed speech practice from Module 3, while a larger local MCP/router simulation would duplicate the agent/MCP concepts already covered by the completed Agents exercises without validating Microsoft Foundry, Azure Speech MCP, Azure Blob Storage, or Azure authentication.
