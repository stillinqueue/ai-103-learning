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

- [ ] **Understand `web_search`**
  Built-in Responses API tool. The model issues a live search and incorporates current web results into its response.

- [ ] **Explain grounding vs relying only on model knowledge**
  Without grounding, the model answers from training data only (potentially stale or wrong). With grounding, retrieved content is injected as context and the model answers from it.

- [ ] **Understand how conversation context + retrieved data can work together**
  `previous_response_id` chains conversation history. On each turn, `file_search` or `web_search` retrieve relevant data. Both are active simultaneously in the same Responses API call.

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

- [ ] **Explain system prompt vs platform content filter**
  System prompt: guides the model's behaviour — can be overridden by jailbreak attempts. Content filter: enforced by the platform before/after the model — not bypassable via prompts.

- [ ] **Understand that model refusal and platform filtering are separate safety layers**
  The model may refuse based on training (RLHF). The platform filter is a separate layer that can block even if the model would comply. Both can be active simultaneously.

### Practical architecture questions

- [ ] **Can I explain the path: user → app → model → tool/retrieval → model → response?**
  User sends input → app calls the model API → model optionally calls a tool → app (or API) executes retrieval/function → result returned to model → model generates final response → app shows output.

- [ ] **Can I explain where secrets should be stored?**
  In environment variables or secret managers (Key Vault, Codespaces secrets). Never in source code, never committed to version control, never in `.env` files that are tracked by git.

- [ ] **Can I explain why API keys should never be committed?**
  Git history is permanent and often public. A committed key can be extracted from any clone and misused. Secret scanning tools can detect and alert on committed keys.

- [ ] **Can I explain what parts of my implementation were OpenAI Platform vs Azure/Foundry?**
  OpenAI Platform: model calls, vector stores, `file_search`, `web_search`, streaming. Azure/Foundry: not tested directly due to quota limitations — see comparison documents.

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

