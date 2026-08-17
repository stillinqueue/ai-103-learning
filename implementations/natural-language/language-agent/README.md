# Develop a text analysis agent

## Exercise

**Develop a text analysis agent** using Azure Language in Foundry Tools.

## Architecture

```text
Python client -> Foundry Agent -> Azure Language MCP server
```

`azure-text-agent.py` does not call `TextAnalyticsClient`. It sends prompts to an existing Foundry agent through the Foundry project OpenAI-compatible client. The Foundry agent is configured in the portal with the Azure Language MCP tool, including its connection and tool approval or auto-approval settings. The agent chooses the appropriate Azure Language operation for the prompt.

Examples from the lab include named entity extraction, PII identification and redaction, and sentiment analysis.

## Important concepts

- `AIProjectClient` connects the application to the Foundry project.
- `DefaultAzureCredential` supplies Azure authentication.
- `get_openai_client()` provides the project client used to submit Responses API requests.
- `agent_reference` selects the existing `Text-Analysis-Agent` by name.
- The Azure Language MCP tool exposes specialized text-analysis operations to the agent.
- MCP lets an agent invoke specialized external tools based on the prompt.

The client flow is:

```text
AIProjectClient -> get_openai_client() -> responses.create(agent_reference) -> existing Foundry agent -> Azure Language MCP tool
```

## Files

- `microsoft-starter-text-agent.py` is the preserved Microsoft Learn starter with TODOs.
- `azure-text-agent.py` is the completed official client pattern.
- `.env.example` contains placeholder configuration only.
- `requirements.txt` preserves the Microsoft dependency versions.

## Environment limitation

The official exercise requires:

- a Microsoft Foundry project
- a deployed model
- an existing `Text-Analysis-Agent`
- an Azure Language MCP connection
- Azure authentication

Azure CLI / Entra authentication from this Codespace is blocked by tenant security defaults. Security settings will not be weakened, and blocked authentication will not be repeatedly retried. The official implementation is preserved as Azure reference code and is not claimed to have run successfully. No Foundry agent or Azure resource is created by this code.

A local/OpenAI approximation was not created. A direct OpenAI call would duplicate Module 1's direct NLP practice rather than demonstrate the central Module 2 architecture: a Foundry agent routing to the Azure Language MCP tool.

## Mental model

- Module 1: app -> Azure Language directly
- Module 2: app -> Foundry agent -> Azure Language MCP tool
- MCP lets the agent invoke specialized external tools.
- The agent decides which connected tool operation to use based on the prompt.

The module is recorded as completed in the learning-path tracker based on the implemented and structurally verified reference pattern. No real Foundry runtime call has been executed from this Codespace.

## Verification

### Azure/Foundry implementation

- `azure-text-agent.py` passed `python -m py_compile`.
- `DefaultAzureCredential` and `AIProjectClient` imported successfully.
- The installed SDK is `azure-ai-projects 2.3.0`; the Microsoft exercise pins `azure-ai-projects==2.0.0b4`. The installed version exposes the compatible `AIProjectClient(endpoint, credential)` constructor and `get_openai_client()` method used by this implementation. The Microsoft dependency pin remains unchanged.
- With `FOUNDRY_ENDPOINT` absent, the script reports `FOUNDRY_ENDPOINT is required` before creating a client.
- With `AGENT_NAME` absent, the script reports `AGENT_NAME is required` before creating a client.
- No real Foundry agent call was executed. Azure authentication, a Foundry project, a deployed model, an existing `Text-Analysis-Agent`, and an Azure Language MCP connection are unavailable in this Codespace.

### Local workaround

No local workaround was created. A direct OpenAI implementation would not reproduce the Foundry Agent plus Azure Language MCP architecture and would only duplicate the preceding Analyze Text exercise. No service-level verification was performed.
