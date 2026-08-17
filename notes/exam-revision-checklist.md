# AI-103 Exam Revision Checklist

---

## Learning Path 1 — Develop generative AI apps in Azure ✅

### Azure / Foundry basics

- [ ] **Explain what Microsoft Foundry is used for**
  An Azure platform for building, deploying, and managing AI applications. Provides model deployment, prompt flow authoring, evaluation, guardrails, and connections to other Azure services.

- [ ] **Understand projects, model deployments, endpoints, and connections**
  A Foundry *project* groups resources. A *deployment* maps a model name to a specific version and quota. An *endpoint* is the URL the app calls. *Connections* link to external services (Azure AI Search, storage, etc.).

- [ ] **Understand the difference between Azure-hosted models and OpenAI Platform-hosted models**
  Same models, different infrastructure. Azure = your Azure subscription, region, data residency, and enterprise controls. OpenAI Platform = OpenAI's infrastructure, API key auth, per-account quota.

- [ ] **Understand Azure authentication vs API-key authentication**
  Azure: `DefaultAzureCredential` resolves identity from managed identity, environment, CLI login, etc. — no key stored in code. OpenAI Platform: `OPENAI_API_KEY` environment variable.

- [ ] **Know that model availability and quota affect deployment**
  Not all models are available in all Azure regions. Quota limits the tokens-per-minute and requests-per-minute for a deployment. Free Trial subscriptions have restricted quota eligibility.

### Generative AI development

- [ ] **Explain the role of a system/developer instruction vs user input**
  The system instruction (or `instructions` in the Responses API) sets the assistant's role, tone, and constraints. The user input is the per-turn message. The model treats instructions as authoritative.

- [ ] **Use the OpenAI Python SDK conceptually**
  `from openai import OpenAI; client = OpenAI()` — constructs an authenticated client. For Azure: `AzureOpenAI(azure_endpoint=..., azure_ad_token_provider=...)`.

- [ ] **Understand `client.responses.create()`**
  Newer alternative to Chat Completions. Takes `model`, `instructions`, `input`, optional `tools` and `previous_response_id`. Returns a structured response object.

- [ ] **Understand `response.output_text`**
  Convenience property — extracts the assistant's text from the response. Equivalent to `response.choices[0].message.content` in Chat Completions.

- [ ] **Explain multi-turn conversation state and `previous_response_id`**
  Pass the previous response's `.id` to link turns server-side. The API maintains history — no need to resend the full message array. Omit on the first turn.

- [ ] **Explain streaming and why it improves user experience**
  Tokens are returned as they are generated rather than after the full response is complete. Users see output immediately; perceived latency is lower. Use `client.responses.stream()`.

- [ ] **Understand synchronous vs asynchronous calls**
  Sync (`OpenAI`) blocks until the response arrives — fine for scripts and CLI tools. Async (`AsyncOpenAI`) returns a coroutine — required in async web frameworks (FastAPI, aiohttp).

### Tools and function calling

- [ ] **Explain function/tool calling**
  Lets the model request execution of developer-defined functions. The model outputs a structured call; the application runs the function and passes the result back.

- [ ] **Remember: developer defines available tools**
  You provide the list of tools (name, description, parameters) in the API call. The model does not know about tools unless you declare them.

- [ ] **Remember: model chooses which tool to request**
  The model decides whether to call a tool and which one, based on the user's input and the tool descriptions. It does not execute code.

- [ ] **Remember: application executes the actual function**
  Your code runs the function and returns the result. For built-in tools (`file_search`, `web_search`) the API handles execution server-side.

- [ ] **Understand how tool results are passed back to the model**
  The application sends the function result back in the next API call. The model incorporates it into its final response.

- [ ] **Distinguish a tool schema from a function implementation**
  The schema describes what the model may request: the tool name, description, argument types, required fields, and validation rules. The application still owns and executes the real Python implementation.

- [ ] **Understand strict function schemas**
  `strict: true` together with `required` and `additionalProperties: false` constrains the model's JSON arguments to the declared contract.

- [ ] **Understand the complete custom-function response loop**
  The model returns function arguments as JSON. The application parses them, executes the matching local function, returns a `function_call_output` using the original `call_id`, and continues with `previous_response_id`.

- [ ] **Process every returned function call**
  A response can contain multiple function calls. Process all of them, not just the first, and continue iteratively until the model returns no more function calls.

- [ ] **Remember that tools are developer-exposed capabilities**
  The model can request only the tools supplied by the application. It cannot call arbitrary local Python functions or execute local code by itself.

- [ ] **Understand custom function tools vs MCP tools**
  Custom function tools are application-defined direct function integrations. MCP is a standardized protocol boundary for discovering and invoking external tools through an MCP server and client.

- [ ] **Know the MCP discovery and invocation methods**
  `list_tools()` discovers the tools available from an MCP server. `call_tool(...)` invokes one of those discovered tools with arguments.

- [ ] **Understand stdio as an MCP transport**
  Stdio is one MCP transport pattern: the client launches or connects to a server process over standard input and output.

- [ ] **Do not confuse tool discovery with tool execution**
  `list_tools()` returns tool definitions only. The application must explicitly execute a selected tool through `call_tool(...)` and return the result to the model.

- [ ] **Remember the application owns MCP execution**
  The model requests a discovered tool and arguments, but the application remains responsible for executing the MCP call and returning the result. The model never directly runs the MCP server's Python code.

- [ ] **Distinguish a tool request from tool execution**
  A model `function_call` or `mcp_approval_request` expresses intent; it does not execute the application action. The application controls whether and when the tool runs.

- [ ] **Understand approval as a control point**
  `mcp_approval_request` asks the application or user for permission. `mcp_approval_response` returns an approve or deny decision before the external knowledge/tool action continues.

- [ ] **Know the effect of denial**
  Denial can prevent grounding or tool execution, while the model may still produce an answer from its general model knowledge. That answer should not be treated as grounded in the denied source.

- [ ] **Separate grounding from approval**
  Grounding determines which external knowledge source supports an answer. Approval determines whether the application is permitted to access that source for the current request.

- [ ] **Separate grounding from deployment**
  Grounding supplies knowledge to the agent; deployment determines where users can access the agent. An agent can work correctly in a development or playground environment before it is published to a channel.

- [ ] **Understand Teams as a channel target**
  Microsoft Teams is a deployment and user-access channel, not the grounding mechanism. File Search or another knowledge integration provides grounding independently of Teams.

- [ ] **Recognize deployment governance concerns**
  Publishing to Teams or Microsoft 365 Copilot introduces identity, permissions, tenant policy, and administrator approval requirements. Organization-wide publishing can require admin approval.

- [ ] **Know Microsoft 365 Copilot licensing implications**
  Microsoft 365 Copilot integration may require an appropriate Copilot license in addition to the Azure and Microsoft 365 configuration.

- [ ] **Understand workflow orchestration vs a single agent call**
  A workflow coordinates variables, loops, model steps, conditions, and outputs. It is a control-flow design around agent calls, not just one model request.

- [ ] **Know that workflow variables hold state**
  Set-variable nodes initialize values, and later nodes read those values as workflow state.

- [ ] **Understand `For each` collection processing**
  A `For each` node processes a collection item by item, applying the same downstream workflow logic independently to each item.

- [ ] **Use structured output for reliable branching**
  Structured JSON makes fields such as category and confidence predictable for downstream conditions.

- [ ] **Understand condition nodes route execution**
  If/Else conditions use model output to select the next workflow branch, such as low confidence, Billing escalation, or automated resolution.

- [ ] **Recognize separate responsibilities for separate agents**
  A Triage Agent can classify and score an issue while a Resolution-Agent drafts the customer response. Different steps can have different instructions and responsibilities.

- [ ] **Remember that a branch can prevent later agent calls**
  A Billing branch can terminate or escalate a ticket without invoking the Resolution-Agent. Deterministic workflow logic controls whether later probabilistic model steps run.

- [ ] **Combine deterministic orchestration with probabilistic model output**
  The workflow loop and conditions are deterministic application logic, while classification and drafting are probabilistic model operations.

- [ ] **Understand Microsoft Agent Framework's role**
  Microsoft Agent Framework is an application framework and abstraction layer for building and orchestrating agents, including instructions, tools, lifecycle, and conversation execution.

- [ ] **Separate the framework from the model provider**
  Microsoft Agent Framework and the model provider are separate concerns. A framework implementation can use a provider-specific backend such as Azure Foundry through `FoundryChatClient`.

- [ ] **Understand Foundry's role in the Agent Framework lab**
  Microsoft Foundry provides the hosted Azure model and agent backend, endpoint, deployment, and authentication context used by the Agent Framework client.

- [ ] **Know what the agent abstraction can manage**
  An agent abstraction can manage conversation/state, tool orchestration, instructions, and execution while the application supplies the provider client and local tools.

- [ ] **Do not equate similar behavior with the same framework**
  A local OpenAI Responses API implementation can reproduce expense processing and tool-calling behavior, but it is not equivalent to Microsoft Agent Framework.

### Multi-agent orchestration

- [x] **Understand a multi-agent system**
  Multiple specialized agents work together, with each agent focused on a narrower responsibility.

- [x] **Understand orchestration**
  Orchestration determines how agents interact, including their execution order and how outputs move between them.

- [x] **Understand sequential orchestration**
  Sequential orchestration passes work through agents in a defined order. In the exercise, the flow is `Summarizer -> Classifier -> Recommended Action`.

- [x] **Understand `participants` ordering**
  `participants=[summarizer_agent, classifier_agent, action_agent]` determines the sequence in which agents execute.

- [x] **Understand intermediate output flow**
  Later agents can consume earlier-agent outputs. The Classifier receives the summary, and Recommended Action receives the summary and classification.

- [x] **Understand `output_from="all"`**
  `output_from="all"` exposes intermediate outputs as well as the final output, allowing the application to collect and display every participant result.

- [x] **Understand specialization**
  Specialization can reduce the complexity of each individual agent's responsibility and make the overall workflow easier to reason about.

- [x] **Separate orchestration from the model/provider**
  The orchestration strategy and the model or provider are separate concerns. Microsoft Agent Framework can orchestrate agents backed by Azure Foundry, while a Python chain of OpenAI model calls can reproduce similar behavior without being Microsoft Agent Framework.

### A2A remote agents

- [x] **Understand A2A**
  A2A is an agent-to-agent communication protocol. It connects agents to other agents through a protocol boundary.

- [x] **Distinguish A2A from MCP**
  MCP primarily connects agents or applications to tools and resources. A2A connects one agent to another agent with its own logic and runtime.

- [x] **Understand remote-agent ownership**
  A remote agent owns its implementation, model call, and runtime. The host should communicate with it through the protocol boundary rather than directly executing its Python implementation.

- [x] **Understand HTTP as an A2A transport boundary**
  HTTP endpoints can expose agent metadata, accept A2A messages, and return task responses while keeping the host and remote agents separate.

- [x] **Understand A2A agent discovery**
  The host can resolve remote agent cards to learn an agent's name, description, endpoint, capabilities, skills, and supported message modes before sending work.

- [x] **Understand remote-agent context flow**
  The output from one remote agent can become context for another remote agent. In the exercise, the Title result is included in the Outline request.

- [x] **Separate orchestration from A2A transport**
  Multi-agent orchestration describes which agents perform which steps and in what order. A2A describes the protocol and transport boundary used to communicate with a remote agent.

- [x] **Compare function calling, MCP, and A2A**
  `Function calling -> app calls local function`

  `MCP -> app/agent calls external tool through MCP`

  `A2A -> agent communicates with another agent`

### Azure Language text analysis

- [x] **Understand the Azure Language client pattern**
  `TextAnalyticsClient` is the service client, authenticated with `DefaultAzureCredential` and configured with the `FOUNDRY_ENDPOINT` service endpoint.

- [x] **Understand language detection**
  `detect_language` returns the detected language and ISO language code. It is useful when downstream processing depends on knowing the text language.

- [x] **Understand Named Entity Recognition**
  `recognize_entities` finds and categorizes entities such as people, organizations, locations, dates, and other concepts. Entity recognition is a specialized NLP operation.

- [x] **Understand PII detection and redaction**
  `recognize_pii_entities` identifies personally identifiable information, returns categorized PII entities, and provides redacted text.

- [x] **Keep the Azure Language mental model**
  Azure Language provides specialized NLP service APIs. NER identifies and categorizes real-world entities in text; PII detection identifies sensitive personal information and can redact it. A specialized NLP API is not general-purpose LLM prompting, and a local OpenAI approximation is not Azure Language. Syntax/import verification is not successful Azure service execution.

### Foundry text analysis agent

- [x] **Understand the Foundry agent client pattern**
  `AIProjectClient` uses `DefaultAzureCredential`; `get_openai_client()` provides the Responses API client, and `agent_reference` targets an existing Foundry agent by name.

- [x] **Understand the agent-mediated architecture**
  `Python client -> Foundry Agent -> Azure Language MCP tool`. The client does not call `TextAnalyticsClient` directly. The agent can choose the appropriate connected language capability based on the prompt, while MCP exposes external tools and capabilities to the agent.

- [x] **Recognize language-agent tasks**
  Lab examples include named entity recognition, PII identification and redaction, and sentiment analysis.

- [x] **Keep the direct-versus-agent mental model**
  Direct SDK call is not the same as an agent-mediated tool call. Module 1 is `app -> Azure Language directly`; Module 2 is `app -> Foundry agent -> Azure Language MCP`. `agent_reference` selects the existing Foundry agent, and a local direct OpenAI prompt would not reproduce this Microsoft agent/MCP architecture.

- [x] **Separate structural and runtime verification**
  Syntax/import and SDK-surface checks do not prove successful Foundry runtime execution.

- [x] **Remember the SDK version boundary**
  The Microsoft lab pins `azure-ai-projects==2.0.0b4`, while this Codespace had `2.3.0`. The API surface used here remained compatible in this environment; do not generalize that result to every beta or stable SDK version.

### Speech-capable generative AI

- [x] **Understand the Azure speech-capable client pattern**
  `AzureOpenAI` uses `DefaultAzureCredential` with `get_bearer_token_provider`; `MODEL_ENDPOINT` selects the Azure endpoint and `MODEL_NAME` selects the deployed speech model.

- [x] **Understand text-to-speech**
  `client.audio.speech.with_streaming_response.create(...)` generates audio from text. The voice can be selected, instructions can influence delivery or style where supported, and the response can be streamed to an audio file.

- [x] **Understand speech-to-text**
  `client.audio.transcriptions.create(...)` accepts an audio file opened in binary mode and returns transcription text from the deployed model.

- [x] **Keep the speech mental model**
  TTS is `text -> audio`; STT/transcription is `audio -> text`. This lab uses speech-capable generative AI models through the OpenAI SDK, not the classic Azure AI Speech SDK/service APIs. `AzureOpenAI` represents an Azure-hosted deployment/client, while local OpenAI practice is direct OpenAI API usage and not Azure runtime verification. Syntax/import verification is not successful Azure model execution.

### Azure Speech SDK

- [x] **Understand Azure Speech SDK configuration**
  `azure.cognitiveservices.speech` provides `SpeechConfig`, using `DefaultAzureCredential` with the Foundry/Cognitive Services endpoint.

- [x] **Understand speech synthesis**
  `AudioOutputConfig` selects the output file, `SpeechSynthesizer` handles synthesis, and `speak_text_async(...).get()` returns the result. `ResultReason.SynthesizingAudioCompleted` indicates success, and output can be written to `greeting.wav`.

- [x] **Understand speech recognition**
  `AudioConfig` supplies an audio file to `SpeechRecognizer`; `recognize_once_async().get()` performs recognition. `ResultReason.RecognizedSpeech` indicates success and recognized text is available through `result.text`.

- [x] **Keep the Azure Speech mental model**
  Module 3 uses generative speech models through `AzureOpenAI`; Module 4 uses the specialized Azure Speech SDK. TTS is `text -> speech`, STT is `speech -> text`, `SpeechSynthesizer` handles synthesis, and `SpeechRecognizer` handles recognition. Structural SDK validation is not successful Azure Speech runtime execution, and direct OpenAI speech practice is not Azure Speech SDK verification.

- [x] **Understand authentication patterns**
  The Microsoft starter contains `FOUNDRY_KEY`, while the completed Entra pattern uses `DefaultAzureCredential` with `FOUNDRY_ENDPOINT`. Key-based and Entra-based authentication are different patterns; do not mix them without understanding which constructor or API expects each one.

### Azure Speech MCP agent

- [x] **Understand the Foundry agent client pattern**
  `AIProjectClient` uses `DefaultAzureCredential`; `get_openai_client()` provides the Responses API client, and `agent_reference` targets the existing `speech-agent`.

- [x] **Understand the agent/tool architecture**
  `Python client -> Foundry agent -> Azure Speech MCP -> Azure Speech`. The client does not call the Azure Speech SDK directly. MCP exposes speech capabilities as agent tools, and the agent interprets the prompt to invoke the appropriate speech operation.

- [x] **Understand the storage role**
  Synthesized audio may need persistent storage. The lab uses Azure Blob Storage for generated audio, while SAS/container access belongs to the MCP tool and storage integration, not the Python client's Foundry authentication.

- [x] **Separate authentication relationships**
  Python client to Foundry uses `DefaultAzureCredential`. The Foundry MCP connection to Azure Speech and storage uses the configured connection credentials or SAS mechanism required by the lab.

- [x] **Keep the Module 3/4/5 mental model**
  Module 3 is `app -> AzureOpenAI speech model`; Module 4 is `app -> Azure Speech SDK directly`; Module 5 is `app -> Foundry agent -> Azure Speech MCP`. A connected MCP tool is not necessarily executed, and a tool request is not tool execution. Agent-mediated speech is distinct from a direct SDK speech call, structural verification is not runtime verification, and Blob Storage may be part of a speech-generation tool workflow.

- [x] **Remember the SDK boundary**
  The Microsoft lab pins `azure-ai-projects==2.0.0b4`, while this Codespace has `2.3.0`. The APIs used by this exercise remained compatible here; do not assume all beta and stable versions are interchangeable.

### Voice Live agent

- [x] **Understand the Voice Live client pattern**
  `azure.ai.voicelive` provides asynchronous `connect(...)`; `AzureCliCredential` authenticates the client, `AgentConfig` identifies the Foundry project/agent, `RequestSession` configures the session, and server events drive the conversation.

- [x] **Understand real-time audio**
  Microphone audio is streamed into an ongoing session and synthesized response audio is streamed back. Voice Activity Detection identifies turns; multilingual semantic VAD helps detect boundaries, noise reduction improves microphone input, echo cancellation avoids treating speaker output as new input, and interruption/barge-in allows the user to interrupt agent speech.

- [x] **Know the important Voice Live APIs**
  `InputAudioFormat`, `OutputAudioFormat`, `Modality`, `ServerEventType`, `AudioNoiseReduction`, `AudioEchoCancellation`, and `AzureSemanticVadMultilingual` configure and process the real-time session.

- [x] **Keep the Module 3-6 mental model**
  Module 3 is `app -> AzureOpenAI` speech model; Module 4 is direct Azure Speech SDK; Module 5 is Foundry agent -> Azure Speech MCP; Module 6 is a persistent real-time Voice Live session -> Foundry agent. A streaming voice session is not independent TTS/STT requests; VAD decides conversational turns, echo cancellation is distinct from noise reduction, and structural SDK validation is not a successful real-time audio session.

- [x] **Remember endpoint and agent configuration**
  Voice Live expects the base Foundry resource endpoint without `/api/projects/...`. Agent names/IDs are case-sensitive, and the official text inconsistently uses `chat-agent` and `Chat-Agent`; the deployed agent value must be used exactly.

- [x] **Remember the runtime boundary**
  Azure CLI authentication is blocked in this Codespace and `pyaudio`/native microphone-speaker support is unavailable, so no real Voice Live session was runtime-verified.

### Translation

- [x] **Understand Azure Translator**
  `TextTranslationClient` accepts `InputTextItem` values; `get_supported_languages(scope="translation")` provides valid target codes, and `translate(...)` performs translation with automatic source-language detection and an application-supplied target language.

- [x] **Understand Azure Speech translation**
  `SpeechTranslationConfig` configures the service, `TranslationRecognizer` recognizes source speech such as `en-US`, multiple target languages can be added, translated text is returned per target language, and `SpeechSynthesizer` can speak each translated result.

- [x] **Remember the lab voice mapping**
  French uses `fr-FR-HenriNeural`, Spanish uses `es-ES-ElviraNeural`, and Hindi uses `hi-IN-MadhurNeural`.

- [x] **Keep the translation mental model**
  Translation is not transcription: transcription is `speech -> text` in the same language, while text translation is `text in language A -> text in language B`. Speech translation can combine recognition, translation, and synthesis. Azure Translator handles text translation; Azure Speech handles speech translation and synthesis here. Structural SDK verification is not successful Azure service execution, and direct LLM translation is not Azure Translator SDK verification.

- [x] **Remember the translation architectures**
  Text is `app -> Azure Translator -> translated text`. Speech is `microphone -> TranslationRecognizer -> translated text -> SpeechSynthesizer -> speaker`. Both use the base Cognitive Services endpoint and `DefaultAzureCredential`; Azure CLI/Entra authentication remains unavailable in this Codespace.

### Multimodal vision input

- [x] **Understand multimodal input**
  One model request can contain both text and image input. `input_text`, `input_image`, and `response.output_text` form the core Responses API pattern.

- [x] **Understand image transport methods**
  A remote URL can be supplied directly as image input. A local image can be read as bytes, base64 encoded, and sent as a `data:image/jpeg;base64,...` data URL.

- [x] **Understand the Responses API request**
  `client.responses.create(...)` accepts developer/system instructions and user content combining text and an image in the same request.

- [x] **Understand Azure vision authentication and endpoint**
  `DefaultAzureCredential` and `get_bearer_token_provider` supply Entra authentication for the Azure OpenAI client. The endpoint is `https://<resource>.openai.azure.com/openai/v1/`, and `MODEL_DEPLOYMENT` identifies the Azure model deployment.

- [x] **Keep the vision mental model**
  Multimodal means multiple input modalities in one model interaction. Generative multimodal image understanding is distinct from specialized computer-vision SDK analysis. URL and base64 images are transport methods, not different vision capabilities. A CLI loop is not conversation memory; independent `responses.create(...)` calls remain stateless unless history or conversation state is supplied. Local OpenAI success is not Azure runtime verification, and payload validation is not successful Azure service execution.

### Image generation

- [x] **Understand the image generation API**
  `client.images.generate(...)` accepts the model or deployment, a text prompt, and `n=1`, then returns generated image data.

- [x] **Understand base64 response handling**
  Generated image data may be returned as `b64_json`. Base64 text is an encoding/transport representation, not the image itself; decode it with `base64.b64decode(...)` before writing the resulting bytes to a `.png` file.

- [x] **Understand Azure image authentication and endpoint**
  `DefaultAzureCredential` with `get_bearer_token_provider` supplies Entra authentication for the Azure OpenAI client. The endpoint is `https://<resource>.openai.azure.com/openai/v1/`, and `MODEL_DEPLOYMENT` identifies the Azure image-model deployment.

- [x] **Keep the generation mental model**
  Module 1 analyzes an existing image; Module 2 generates a new image from a prompt. Image generation is not image understanding: `text prompt -> image model -> image bytes`, then `b64_json -> base64 decode -> PNG bytes`. A CLI loop does not automatically preserve image-generation history or context. Local OpenAI generation success is not Azure runtime verification, and structural SDK validation is not successful Azure service execution.

- [x] **Remember the model boundary**
  The Microsoft exercise recommends `gpt-image-2`, and local OpenAI practice also succeeded with `gpt-image-2`; Azure deployment availability and quota may differ from direct OpenAI availability.

### Sora video generation

- [x] **Understand the video generation API**
  `client.videos.create(...)` returns a video job/object with an ID and status. Generation is asynchronous: creation success does not mean the finished video is ready.

- [x] **Understand polling and terminal states**
  `client.videos.retrieve(video_id)` polls the job until `completed`, `failed`, or `cancelled`. Failed and cancelled jobs must not be treated as downloadable successes.

- [x] **Understand video download**
  `client.videos.download_content(video_id, variant="video")` retrieves completed content, and `write_to_file(...)` can save it as an MP4.

- [x] **Understand remix**
  `client.videos.remix(...)` combines an existing generated video with a new prompt and creates a new asynchronous job. The new job must be polled separately; remix is not in-place modification.

- [x] **Understand image-to-video**
  `input_reference` supplies a binary-opened reference image that guides generation. Image-to-video is distinct from still-image generation.

- [x] **Keep the video mental model**
  Module 1 understands an existing image; Module 2 generates a still image; Module 3 generates or remixes video. Still-image generation may return output directly, while video uses `create -> poll -> terminal status -> download`. Structural API verification is not Azure Sora runtime access, and model availability/quota/access can differ by Azure subscription.

- [x] **Remember Sora configuration**
  The starter uses `OPENAI_BASE_URL`, `MODEL_DEPLOYMENT`, the `https://<resource>.openai.azure.com/openai/v1/` endpoint, and the official `Sora-2` model deployment.

### RAG and grounding

- [ ] **Expand RAG as Retrieval-Augmented Generation**

- [ ] **Explain why RAG is used**
  Grounds responses in external, up-to-date, or private documents without retraining the model. Reduces hallucinations for factual queries.

- [ ] **Explain what a vector store is**
  An index of embedded document chunks. Documents are split, converted to numerical vectors (embeddings), and stored so they can be retrieved by similarity.

- [ ] **Understand embeddings conceptually**
  Numerical representations of text where semantically similar content produces vectors that are close together in multi-dimensional space.

- [ ] **Explain semantic/vector retrieval**
  A query is embedded and compared to stored vectors. The closest chunks (most semantically similar to the query) are returned — no exact keyword match needed.

- [ ] **Understand `file_search`**
  Built-in Responses API tool. Attach a vector store; the model retrieves relevant document chunks automatically as part of response generation.

- [ ] **Distinguish Foundry IQ from generic File Search**
  Foundry IQ integrates an Azure knowledge base, connected Azure resources, and Foundry agent configuration. It is a specific Azure knowledge integration and is not interchangeable with a generic File Search vector-store tool.

- [ ] **Understand `web_search`**
  Built-in Responses API tool. The model issues a live search and incorporates current web results into its response.

- [ ] **Explain grounding vs relying only on model knowledge**
  Without grounding, the model answers from training data only (potentially stale or wrong). With grounding, retrieved content is injected as context and the model answers from it.

- [ ] **Understand how conversation context + retrieved data can work together**
  `previous_response_id` chains conversation history. On each turn, `file_search` or `web_search` retrieve relevant data. Both are active simultaneously in the same Responses API call.

- [ ] **Remember the agent design pattern: model + instructions + tools + context/state + actions**
  An agent is more than a model call. It combines the model, the system instructions, the available tools, the retrieved context, and the application actions that execute tool results.

- [ ] **Remember the difference between File Search and Code Interpreter**
  File Search is for retrieval and grounding over knowledge/reference files. Code Interpreter is for computation, analysis, statistics, filtering, aggregation, and chart generation over data files.

- [ ] **Remember that attaching a tool does not guarantee correct tool selection**
  The model may choose the wrong tool unless instructions clearly direct routing between file retrieval and analysis tasks.

- [ ] **Understand that grounding data and system instructions serve different purposes**
  Grounding data provides factual/reference content; system instructions define the role, constraints, and output behaviour.

### Prompt engineering and fine-tuning

- [ ] **Explain prompt engineering**
  Shaping model output through the instructions and examples you provide — no model weight changes. Fast to iterate, but limited to the model's existing capabilities.

- [ ] **Explain fine-tuning**
  Training a base model on a curated dataset to bake in a specific behaviour, style, or persona. Changes model weights. Slower and more expensive than prompting.

- [ ] **Know when prompting is preferable to fine-tuning**
  Preferred when: behaviour can be described in instructions, the task varies, or fast iteration matters. Also preferable when factual knowledge needs to stay current.

- [ ] **Know when fine-tuning may be useful**
  Useful when: a consistent style or persona is hard to describe, the output format must be precise, or the base model consistently ignores instructions despite good prompting.

- [ ] **Understand system/user/assistant JSONL training examples**
  Each training line: `{"messages": [{"role":"system","content":"..."},{"role":"user","content":"..."},{"role":"assistant","content":"..."}]}`. Every example must have at least one assistant message.

- [ ] **Understand why a baseline test should be performed before fine-tuning**
  Establishes the base model's behaviour on your target prompts. Provides a reference to judge whether fine-tuning actually improved anything.

- [ ] **Understand that fine-tuning is not a replacement for RAG when current or private factual knowledge is required**
  Fine-tuning bakes in style, not facts. Facts change; retraining is expensive. Use RAG for knowledge that needs to be current, accurate, or private.

### Responsible AI and safety

- [ ] **Explain Responsible AI at a high level**
  A framework for building AI that is fair, reliable, private, inclusive, transparent, and accountable. Microsoft's six principles underpin Foundry's safety tooling.

- [ ] **Understand the identify → measure → mitigate → monitor lifecycle**
  *Identify* potential harms. *Measure* their likelihood and severity. *Mitigate* through design, prompts, and filters. *Monitor* deployed systems continuously.

- [ ] **Explain Foundry content filters / guardrails**
  Platform-level filters that evaluate both input prompts and output completions across harm categories. Configured per deployment; enforced independently of the model.

- [ ] **Know the major harm categories: hate, violence, sexual, self-harm**
  Each has configurable severity thresholds (safe, low, medium, high). Requests/responses exceeding the threshold are blocked or flagged.

- [ ] **Understand Safe / Low / Medium / High severity and how thresholds affect blocking**
  Each harm category returns a severity level. You configure the *threshold* per category — content at or above the threshold is blocked. E.g. set threshold to Medium: Low severity passes, Medium and High are blocked.

- [ ] **Default guardrails vs custom guardrails**
  Default: Microsoft's preset thresholds applied automatically to every deployment. Custom: you configure per-category thresholds, add blocklists, and enable optional detectors in the Foundry portal.

- [ ] **Prompt Shields — jailbreak and prompt-injection protection**
  Detects attempts to override the system prompt (jailbreak) or inject malicious instructions hidden in user-supplied or retrieved content (indirect injection). Applied at input time.

- [ ] **Custom blocklists**
  Lists of specific terms or phrases that are always blocked regardless of harm category classification. Useful for brand-specific, legal, or domain-specific content that standard filters don't cover.

- [ ] **Protected material detection — text and code**
  Detects output that reproduces copyrighted text or licensed code verbatim. Can be enabled per deployment. Flags or blocks responses containing protected material.

- [ ] **Input filtering vs output filtering**
  Input filtering: checks the user's prompt before it reaches the model. Output filtering: checks the model's response before it is returned to the app. Both can be active simultaneously.

- [ ] **Guardrail intervention points**
  - *User input*: filter applied before the prompt reaches the model.
  - *Model output*: filter applied before the response reaches the app.
  - *Tool calls (agents)*: filter checks tool call arguments before execution.
  - *Tool responses (agents)*: filter checks data returned from tools before the model sees it.

- [ ] **Testing and refining guardrails**
  Use the Foundry portal to run test inputs, review filter decisions, and adjust thresholds. Iterate until the balance between safety and usefulness is acceptable.

- [ ] **Explain system prompt vs platform content filter**
  System prompt: guides the model's behaviour — can be overridden by jailbreak attempts. Content filter: enforced by the platform before/after the model — not bypassable via prompts.

- [ ] **Understand that model refusal and platform filtering are separate safety layers**
  The model may refuse based on training (RLHF). The platform filter is a separate layer that can block even if the model would comply. Both can be active simultaneously.

> **Mental model:**
> - **System prompt** = tells the model how to behave
> - **Guardrail** = platform checks whether content is allowed
> - **Prompt Shield** = detects attempts to manipulate/inject instructions
> - **Blocklist** = explicitly blocks configured terms
> - **Content filter** = classifies risky content and applies thresholds

### Practical architecture questions

- [ ] **Can I explain the path: user → app → model → tool/retrieval → model → response?**
  User sends input → app calls the model API → model optionally calls a tool → app (or API) executes retrieval/function → result returned to model → model generates final response → app shows output.

- [ ] **Can I explain where secrets should be stored?**
  In environment variables or secret managers (Key Vault, Codespaces secrets). Never in source code, never committed to version control, never in `.env` files that are tracked by git.

- [ ] **Can I explain why API keys should never be committed?**
  Git history is permanent and often public. A committed key can be extracted from any clone and misused. Secret scanning tools can detect and alert on committed keys.

- [ ] **Can I explain what parts of my implementation were OpenAI Platform vs Azure/Foundry?**
  OpenAI Platform: model calls, vector stores, `file_search`, `web_search`, streaming. Azure/Foundry: not tested directly due to quota limitations — see comparison documents.

- [ ] **Understand `DefaultAzureCredential` and developer credentials**
  `DefaultAzureCredential` can use developer credentials such as Azure CLI credentials for local development. This is standard Azure identity flow and differs from API-key based auth.

- [ ] **Know the difference between authentication failure and SDK/API failure**
  A tenant policy that blocks `az login` or device-code auth is an authentication or environment policy issue, not a failure of the Azure SDK or the model API itself.

- [ ] **Know the difference between persistent agent configuration and per-call tool attachments**
  Agent configuration persists the tool set and instructions in the agent definition, while per-call tool attachments in `client.responses.create()` are temporary for that specific request.

---

## Azure-specific concepts I could not practice directly

- [ ] **Microsoft Foundry project**
  A container for resources in Azure AI Foundry. Groups model deployments, connections, datasets, and evaluations. Think of it as the top-level workspace for an AI application.

- [ ] **Model vs deployment vs endpoint**
  *Model*: the base AI model (e.g. GPT-5). *Deployment*: a named instance of that model in your Azure subscription with assigned quota. *Endpoint*: the HTTPS URL your app calls to reach the deployment.

- [ ] **Azure OpenAI endpoint format**
  `https://<resource-name>.openai.azure.com/` — the base URL used with `AzureOpenAI(azure_endpoint=...)`. The deployment name is passed as the `model` parameter, not the model ID.

- [ ] **Azure authentication with Entra ID**
  Azure OpenAI can be accessed without an API key using Azure Active Directory (Entra ID) tokens. Preferred for production — no secret to rotate or leak.

- [ ] **`DefaultAzureCredential`**
  Tries multiple identity sources in order: managed identity → workload identity → Azure CLI login → environment variables. Works transparently in Codespaces, VMs, and AKS without code changes.

- [ ] **API key vs Entra ID authentication**
  API key: simpler, suitable for development. Entra ID: no secret in code, supports RBAC, auditable — preferred for production and enterprise.

- [ ] **`az login` role in local development**
  `az login` authenticates the Azure CLI. `DefaultAzureCredential` can use these credentials automatically during local development without any additional config.

- [ ] **Model quota**
  Quota controls tokens-per-minute (TPM) and requests-per-minute (RPM) per deployment per region. Quota is per subscription and model tier. Insufficient quota blocks deployment creation.

- [ ] **Deployment types: Global Standard, Standard, Provisioned, Batch**
  *Global Standard*: traffic routed globally, higher availability. *Standard*: single-region, lower latency. *Provisioned*: reserved capacity, predictable throughput. *Batch*: async processing of large volumes.

- [ ] **Why quota can block deployment**
  Each deployment consumes quota from the subscription's regional limit. Free Trial subscriptions have minimal or zero quota for newer models like GPT-5.2.

- [ ] **Foundry portal workflow for model deployment**
  Azure AI Foundry portal → project → Deployments → Deploy model → choose model, deployment type, capacity → confirm.

- [ ] **Playground testing**
  Foundry's built-in chat/completion UI for testing deployed models interactively before writing any code. Supports system message configuration and parameter tuning.

- [ ] **Default vs custom guardrails**
  Default: Microsoft's built-in content safety settings applied automatically. Custom: configure per-category thresholds (safe/low/medium/high) per deployment in the Foundry portal.

- [ ] **Harm categories: hate, violence, sexual, self-harm**
  Four core categories evaluated by Azure AI Content Safety. Each has a severity level. Requests or responses exceeding the configured threshold are blocked.

- [ ] **Model refusal vs content filter**
  Model refusal: the model declines based on its own RLHF training — can sometimes be overridden. Content filter: enforced by the platform layer before/after the model — not bypassable via prompts.

- [ ] **Azure-specific fine-tuning workflow**
  Upload training JSONL → create fine-tuning job in Foundry or via SDK → wait for training to complete → deploy the resulting custom model to an endpoint → test and compare to baseline.

---

## High-value exam reminders

| Concept | One-line reminder |
|---|---|
| **RAG** | Retrieve external information at request time to ground the response |
| **Fine-tuning** | Adjust model behaviour or style using labelled training examples |
| **Prompt engineering** | Control model behaviour through instructions and context alone |
| **Function calling** | Model requests a function; the application executes it and returns the result |
| **Function schema** | Declares what the model may request; it is not the implementation that executes the action |
| **`function_call_output`** | Application-wrapped result returned to the model, linked by the original `call_id` |
| **`previous_response_id`** | Continues a response after application-side tool execution |
| **Multi-step tools** | Process every returned function call; the model may chain several tools before its final answer |
| **MCP server** | Exposes standardized, discoverable tools across a protocol boundary |
| **MCP client session** | Initializes the connection, calls `list_tools()`, and invokes tools with `call_tool(...)` |
| **MCP stdio** | A local transport pattern where the client communicates with a server process over standard input/output |
| **Tool discovery** | Makes tool definitions available; it does not automatically execute a tool |
| **Vector search** | Similarity-based retrieval — finds chunks semantically close to the query |
| **Grounding** | Supplying relevant source material reduces unsupported or hallucinated answers |
| **Guardrails / content filters** | Platform safety controls enforced independently of prompts — not bypassed by instructions |
| **Azure infrastructure** | Quota, deployment, identity, endpoint, and resource configuration are separate from model API logic |

---

## Must-remember distinctions

| Comparison | Key difference |
|---|---|
| **Prompting vs RAG vs Fine-tuning vs Tools** | Prompting: instructions only. RAG: inject retrieved knowledge. Fine-tuning: change model weights. Tools: model delegates execution to external code or services. |
| **OpenAI Platform vs Azure OpenAI / Foundry** | Same API spec; different auth (API key vs AAD), infrastructure, data residency, quota model, and enterprise controls. |
| **System prompt vs Guardrail/content filter** | System prompt shapes behaviour — can be jailbroken. Content filter is a platform enforcement layer — cannot be bypassed via prompts. |
| **Model knowledge vs Grounded/retrieved knowledge** | Model knowledge: baked in at training time, may be stale or wrong. Retrieved: fetched at request time from documents or the web, current and verifiable. |
| **Synchronous vs Asynchronous** | Sync: blocks until response completes — use in scripts. Async: non-blocking coroutine — use in web servers and high-concurrency apps. |
| **`file_search` vs `web_search`** | `file_search`: searches your own uploaded documents in a vector store. `web_search`: searches the live public web. Both are built-in Responses API tools. |

---

## Things to revisit because I could not fully test them

- Azure model deployment workflow (portal and CLI)
- Microsoft Foundry portal: project setup, model configuration, prompt flow
- Azure authentication using Entra ID / `DefaultAzureCredential` and managed identity
- Azure quota management: requesting, monitoring, and adjusting model quotas
- Foundry content filter configuration: harm categories, severity thresholds, prompt shields
- Azure-specific fine-tuning: job submission, monitoring, and deploying a custom endpoint

See [limitations-and-workarounds.md](../comparisons/limitations-and-workarounds.md) for full context.

---

## Reference

- [generative-ai.md](generative-ai.md) — detailed notes for Learning Path 1
- [official-lab-vs-my-implementation.md](../comparisons/official-lab-vs-my-implementation.md)
- [limitations-and-workarounds.md](../comparisons/limitations-and-workarounds.md)

