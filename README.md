# AI-103-learning

Hands-on labs and notes for **Microsoft AI-103: Developing AI Apps and Agents on Azure**.

> **Current milestone: Develop generative AI apps in Azure and Develop AI agents on Azure completed. Next: Develop natural language solutions in Azure.**

---

## Progress

| Learning Path | Progress | Status |
|---|---|---|
| [Develop generative AI apps in Azure](https://learn.microsoft.com/en-us/training/paths/develop-generative-ai-apps/) | 6 / 6 modules | ✅ Completed |
| [Develop AI agents on Azure](https://learn.microsoft.com/en-us/training/paths/develop-ai-agents-azure/) | 9 / 9 modules | ✅ Completed |
| [Develop natural language solutions in Azure](https://learn.microsoft.com/en-us/training/paths/develop-language-solutions-azure-ai/) | 7 / 7 modules | ✅ Completed |
| [Extract insights from visual data on Azure](https://learn.microsoft.com/en-us/training/paths/insight-visual-data/) | 2 / 8 modules | 🟡 In progress |

---

## Completed so far

**Learning Path 1 — Develop generative AI apps in Azure** was completed via Microsoft Learn. Hands-on
labs were adapted to run in GitHub Codespaces against the OpenAI Platform API because Azure Free Trial
quota limitations prevented the required Foundry model deployment (GPT-5.2). Core SDK concepts —
Responses API, streaming, tool use, RAG, and fine-tuning preparation — were all practised and are
documented here. See [comparisons/official-lab-vs-my-implementation.md](comparisons/official-lab-vs-my-implementation.md)
for a full breakdown of what was and was not reproduced on Azure.

| Area | Location |
|---|---|
| Responses API chat app (streaming, multi-turn) | [implementations/generative-ai/responses-api/](implementations/generative-ai/responses-api/) |
| RAG with file search and web search tools | [implementations/generative-ai/rag/](implementations/generative-ai/rag/) |
| Fine-tuning dataset, validation, and baseline | [implementations/generative-ai/fine-tuning/](implementations/generative-ai/fine-tuning/) |
| Official lab vs my implementation comparison | [comparisons/official-lab-vs-my-implementation.md](comparisons/official-lab-vs-my-implementation.md) |

---

## Next learning path

**[Develop natural language solutions in Azure](https://learn.microsoft.com/en-us/training/paths/develop-language-solutions-azure-ai/) — 7 / 7 modules**

This is the current area of active work. The completed AI agent exercises are located under `implementations/agents/`, and natural-language implementations are located under `implementations/natural-language/`. Additional modules will be added as the learning path progresses.

### Completed natural-language module

- `analyze-text`: completed
  - Azure Language reference implementation using `TextAnalyticsClient`, language detection, named entity recognition, and PII detection/redaction
  - Local OpenAI practice approximation verified against all five Microsoft review files
  - Azure service execution remains unavailable in the Codespace because the required endpoint and supported authentication are not available
- `language-agent`: completed
  - Azure/Foundry client pattern using `AIProjectClient`, `DefaultAzureCredential`, `get_openai_client()`, and `agent_reference`
  - Existing Foundry `Text-Analysis-Agent` architecture with Azure Language MCP tool documented and structurally verified
  - No real Foundry runtime call was executed because the required project, agent, MCP connection, endpoint, and authentication were unavailable
- `gen-ai-speech`: completed
  - AzureOpenAI text-to-speech and speech-to-text implementations using bearer-token authentication
  - Microsoft `speech.wav` sample preserved for transcription
  - Local OpenAI TTS and transcription practice verified; Azure-hosted runtime remains unavailable
- `azure-speech`: completed
  - Azure Speech SDK synthesis with `SpeechSynthesizer` and recognition with `SpeechRecognizer`
  - Microsoft voice-message samples preserved under `messages/`
  - Structural SDK verification completed; Azure Speech runtime remains unavailable
- `speech-mcp-agent`: completed
  - Foundry client targets the existing `speech-agent` with `agent_reference`
  - Azure Speech capabilities are mediated by the configured Speech MCP server
  - Blob Storage/SAS integration and MCP approval boundaries documented; runtime remains unavailable
- `voice-live-agent`: completed
  - Real-time Voice Live client with asynchronous connection, session configuration, streamed audio, and server-event processing
  - Microphone/speaker runtime remains unavailable because Azure authentication and native audio support are blocked in the Codespace
- `translation`: completed
  - Azure Translator text translation with supported-language selection and automatic source-language detection
  - Azure Speech translation from `en-US` to French, Spanish, and Hindi with language-specific synthesis voices
  - Structural SDK verification completed; Azure translation and audio runtime remains unavailable

### Current visual-data module

- `vision-enabled-chat`: completed
  - Azure multimodal Responses API pattern with remote URL and local base64 image inputs
  - Local OpenAI multimodal practice verified both image-input paths; Azure runtime remains unavailable
- `generate-image`: completed
  - Azure image-generation client with `images.generate(...)`, `b64_json` decoding, and sequential PNG saving
  - Local OpenAI `gpt-image-2` practice verified; generated runtime PNG was removed after inspection

### Completed exercise

- `teams-notifications` agent exercise: completed
  - Foundry/agent configuration with `gpt-5-mini`
  - File Search grounding over `notification-policy.txt`
  - Code Interpreter over `system_performance.csv`
  - JSON notification schema with strict policy grounding
- `astronomy-custom-tools` custom-function exercise: completed
  - Official Foundry reference in `agent.py`
  - Codespaces/OpenAI implementation in `openai-agent.py`
  - Custom tools for event lookup, observation cost, and report generation
  - Application-side Python execution with iterative `function_call_output` handling
- `mcp-integration` MCP exercise: completed
  - FastMCP `Inventory` server over stdio
  - Dynamic discovery of `get_inventory_levels` and `get_weekly_sales`
  - OpenAI workaround using `session.call_tool(...)` and `function_call_output`
- `foundry-iq` approval-flow exercise: completed
  - Official Foundry client using `AIProjectClient` and `DefaultAzureCredential`
  - Foundry IQ approval handling with `mcp_approval_request` and `mcp_approval_response`
  - Codespaces/OpenAI approximation with explicit approval before local knowledge lookup
- `m365-teams-integration` exercise: completed
  - Local enterprise knowledge agent using OpenAI File Search
  - Verified grounding over IT security and remote-work policies
  - Official Teams and optional Microsoft 365 Copilot publishing flow documented
  - Azure/M365 publishing was not executed in the current environment
- `foundry-workflow` exercise: completed
  - Set-variable, For-each, triage, confidence, category, resolution, and output stages
  - Local OpenAI workflow with separate Triage and Resolution model calls
  - Verified independent processing of all three support tickets
- `agent-framework` exercise: completed
  - Official Microsoft Agent Framework reference using `FoundryChatClient` and `Agent`
  - Local OpenAI Responses API workaround with the same expense data and `submit_claim` behavior
  - Verified multi-turn expense-claim context and total calculation
- `agent-framework-multi-agents` exercise: completed
  - Official Microsoft Agent Framework reference using `FoundryChatClient`, `AzureCliCredential`, and `SequentialBuilder`
  - Summarizer, Classifier, and Recommended Action agents run in defined participant order
  - `output_from="all"` collects intermediate and final workflow outputs
  - Local OpenAI Responses API workaround verified with exactly three sequential model calls
- `a2a-remote-agents` exercise: completed
  - Official Foundry/A2A reference with a host/routing agent and remote Title and Outline agents
  - A2A agent-card discovery and HTTP-based agent-to-agent task communication
  - Local OpenAI workaround verified with separate HTTP Title and Outline agents and host-side A2A-compatible requests

---

## Exam revision

[notes/exam-revision-checklist.md](notes/exam-revision-checklist.md) — a quick revision checklist for the AI-103 exam, covering the key concepts from the completed first learning path.
