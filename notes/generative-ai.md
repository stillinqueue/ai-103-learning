# Generative AI Apps on Azure — Study Notes

Microsoft Learn path: **Develop generative AI apps in Azure** (6/6 modules completed)

---

## SDK Landscape

### OpenAI SDK vs Microsoft Foundry SDK

The `openai` Python package works against both the OpenAI Platform and Azure OpenAI Service.
The difference is the client constructor:

```python
# OpenAI Platform
from openai import OpenAI
client = OpenAI()  # reads OPENAI_API_KEY from environment

# Azure OpenAI / Foundry
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
client = AzureOpenAI(azure_endpoint=ENDPOINT, azure_ad_token_provider=token_provider)
```

Microsoft also provides its own Foundry SDK (`azure-ai-projects`) which adds project-level concepts
like connections, evaluations, and agent management that don't exist in the base `openai` package.

### Azure-hosted model vs OpenAI Platform-hosted model

| | Azure OpenAI / Foundry | OpenAI Platform |
|---|---|---|
| Auth | Azure AD / managed identity | API key |
| Model reference | Deployment name (e.g. `my-gpt5-deployment`) | Model ID (e.g. `gpt-5`) |
| Data residency | Configurable Azure region | OpenAI infrastructure |
| Enterprise controls | Content Safety, Foundry guardrails, RBAC | OpenAI moderation defaults |
| Quota | Azure subscription quota per region | OpenAI account tier |

---

## Responses API

The Responses API is a newer OpenAI interface that replaces Chat Completions for many use cases.
It is stateful at the API level, supports built-in tools, and returns a structured response object.

### `client.responses.create()`

```python
response = client.responses.create(
    model="gpt-5",
    instructions="You are a helpful assistant.",
    input="What is RAG?",
)
```

- `instructions` is the system-level behaviour prompt (equivalent to a `system` message in Chat Completions)
- `input` is the user message
- Returns a `ParsedResponse` object

### `response.output_text`

Convenience property that extracts the assistant's text from the response object.
Equivalent to `response.choices[0].message.content` in Chat Completions.

### `previous_response_id` and multi-turn state

The Responses API maintains conversation state server-side.
Pass `previous_response_id` to link turns rather than resending the full message history:

```python
response = client.responses.create(
    model="gpt-5",
    instructions="...",
    input="Follow-up question",
    previous_response_id=last_response_id,
)
last_response_id = response.id
```

Omit `previous_response_id` on the first turn. This approach is simpler than managing a
`messages` array, but the conversation history lives on the API server rather than locally.

See: [`../implementations/generative-ai/responses-api/chat-app.py`](../implementations/generative-ai/responses-api/chat-app.py)

---

## Streaming

Streaming returns tokens incrementally instead of waiting for the complete response.
With the Responses API (SDK v2.x), iterate the stream and filter for text delta events:

```python
from openai.lib.streaming.responses._events import ResponseTextDeltaEvent

with client.responses.stream(model=..., instructions=..., input=...) as stream:
    for event in stream:
        if isinstance(event, ResponseTextDeltaEvent):
            print(event.delta, end="", flush=True)
    response_id = stream.get_final_response().id
print()
```

`stream.text_deltas` is not available in SDK v2.x — iterate events directly.

---

## Synchronous vs Asynchronous API

| | Sync | Async |
|---|---|---|
| Import | `from openai import OpenAI` | `from openai import AsyncOpenAI` |
| Call | `client.responses.create(...)` | `await client.responses.create(...)` |
| Use case | Scripts, CLI tools, notebooks | Web servers, async frameworks (FastAPI, aiohttp) |

The `chat-async.py` file in the Microsoft lab skeleton demonstrates the async pattern.
Both use the same API; the difference is execution model only.

---

## Function / Tool Calling

Tool calling lets a model request that the application run a function and return the result.
The model does not execute code — it outputs a structured call that the application handles.

**Flow:**
1. Developer defines available tools (name, description, parameters)
2. Model decides which tool to call and with what arguments
3. Application executes the function and returns the result
4. Model incorporates the result into its response

Built-in Responses API tools (`file_search`, `web_search`) follow the same pattern but are
handled server-side — no application-side execution needed.

---

## RAG — Retrieval-Augmented Generation

RAG grounds a model's responses in external documents rather than relying on training data.
The general pattern:

1. Index documents in a vector store (embed chunks, store vectors)
2. At query time, retrieve semantically relevant chunks
3. Inject retrieved content into the model's context
4. Model generates a response grounded in the retrieved material

RAG reduces hallucinations for domain-specific content and allows use of private or up-to-date data.

### Vector Stores

A vector store holds embedded document chunks. With the OpenAI SDK:

```python
vector_store = client.vector_stores.create(name="my-store")
client.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id,
    files=[(filename, file_handle), ...],
)
```

`upload_and_poll` blocks until indexing is complete.

### `file_search`

Attaches a vector store to the Responses API call. The model retrieves relevant chunks automatically:

```python
tools = [{"type": "file_search", "vector_store_ids": [vector_store.id]}]
response = client.responses.create(model=..., input=..., tools=tools)
```

### `web_search`

Allows the model to run a live web search during response generation:

```python
tools = [{"type": "web_search"}]
```

### Combining context + file search + web search

All three can be used simultaneously in a single Responses API call.
`previous_response_id` chains conversation turns while the model freely chooses which tool to use:

```python
tools = [
    {"type": "file_search", "vector_store_ids": [vector_store.id]},
    {"type": "web_search"},
]
response = client.responses.create(
    model=..., input=..., tools=tools,
    previous_response_id=last_response_id,
)
```

See: [`../implementations/generative-ai/rag/tools-app.py`](../implementations/generative-ai/rag/tools-app.py)

---

## Prompt Engineering

Prompt engineering shapes model behaviour without changing model weights.

- **System prompt / instructions** — sets the assistant's role, tone, and constraints
- **Few-shot examples** — include example input/output pairs in the prompt
- **Chain-of-thought** — ask the model to reason step-by-step before answering
- **Output format instructions** — specify JSON, bullet points, word limits, etc.

Prompt engineering is fast to iterate and requires no training data, but changes only apply
for the duration of the session and are limited by the model's existing capabilities.

---

## Fine-Tuning

Fine-tuning adjusts a base model's weights on a small, curated dataset to shift its default behaviour —
tone, style, persona, or adherence to a specific instruction pattern.

### Fine-tuning vs prompt engineering

| | Prompt engineering | Fine-tuning |
|---|---|---|
| Speed to iterate | Very fast | Slow (training job) |
| Cost | Per-token inference only | Training + higher inference cost |
| Consistency | Can drift across sessions | Baked into model weights |
| Best for | Behaviour that can be described | Style/tone/persona that's hard to describe |

### JSONL training format

Each line is one training example with `system`, `user`, and `assistant` messages:

```json
{"messages": [
  {"role": "system", "content": "You are a travel assistant..."},
  {"role": "user",   "content": "What should I do in Tokyo?"},
  {"role": "assistant", "content": "Head to Senso-ji at dawn..."}
]}
```

All lines must be valid JSON, all roles must be `system`/`user`/`assistant`, and every example
must include at least one `assistant` message.

### Baseline testing before fine-tuning

Before submitting a fine-tuning job, test the base model on your target prompts.
This gives a reference point to evaluate whether fine-tuning actually improved behaviour.

See: [`../implementations/generative-ai/fine-tuning/baseline-test.py`](../implementations/generative-ai/fine-tuning/baseline-test.py)

---

## Responsible AI

### Microsoft Foundry guardrails / content filters

Azure AI Foundry provides content safety filters that run independently of the model.
They operate on both input prompts and output completions, and can be configured per deployment:

- **Hate, violence, sexual, self-harm** — severity thresholds (safe, low, medium, high)
- **Jailbreak detection** — blocks prompt injection attempts to override the system prompt
- **Prompt shields** — detects indirect injections from document content (relevant in RAG)
- **Groundedness** — checks that responses are grounded in retrieved source documents

These filters are a platform-level control separate from any instructions in the system prompt.

### System prompts vs content filters

| | System prompt | Content filter |
|---|---|---|
| Controlled by | Developer at inference time | Azure platform / deployment config |
| Scope | Shapes model behaviour and persona | Blocks unsafe content categories |
| Bypassed by jailbreaks? | Potentially yes | No (enforced before/after model) |
| Applies to RAG content? | No | Yes, with prompt shields |

A well-designed system prompt and a correctly configured content filter work together —
the prompt defines what the assistant should do; the filter enforces what it must never output.

---

## What I Could Not Test Directly

Because my Azure Free Trial could not obtain the required model deployment quota (GPT-5.2 was
unavailable in all accessible regions), the following were studied on Microsoft Learn but not
reproduced hands-on:

- Azure OpenAI Service endpoint configuration and regional deployment
- Foundry portal: prompt flow authoring, evaluation runs, guardrail configuration
- Azure-managed fine-tuning jobs and deployment of a fine-tuned model endpoint
- Azure AD authentication (`DefaultAzureCredential`, bearer token providers)
- Azure content safety filter configuration per deployment
- Prompt shields and groundedness checking in a Foundry-managed RAG pipeline

Hands-on work used the OpenAI Platform API as a functionally equivalent substitute for core
SDK and API concepts. See
[`../comparisons/official-lab-vs-my-implementation.md`](../comparisons/official-lab-vs-my-implementation.md)
for the full comparison.
