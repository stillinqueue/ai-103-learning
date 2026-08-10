# Official Lab vs My Implementation

## Context

The Microsoft AI-103 labs are designed around **Microsoft Foundry** and **Azure OpenAI Service**.
The official pattern requires an Azure subscription with an approved model deployment (e.g. GPT-4 or GPT-5.2),
Azure endpoint credentials, and Azure Active Directory authentication via `DefaultAzureCredential`.

My Azure Free Trial account could not obtain the required GPT-5.2 deployment quota in any available region.
Rather than block all hands-on practice, I adapted the labs to run against the **OpenAI Platform API**
from a GitHub Codespaces environment, using the `OPENAI_API_KEY` Codespaces secret and the
`gpt-5` model available on my OpenAI account.

This document records what was reproduced, what was deliberately skipped, and where the two approaches
differ in a way that is material to the AI-103 exam objectives.

---

## What This Implementation Covered

- OpenAI Python SDK (`openai` ≥ 2.x)
- Responses API (`client.responses.create`, `client.responses.stream`)
- Multi-turn conversation state via `previous_response_id`
- Streaming responses with incremental token output
- Tool use: `file_search` and `web_search` attached to a single Responses API call
- Vector stores: creation, PDF batch upload, and reuse across sessions
- Retrieval-Augmented Generation (RAG) over travel brochure PDFs
- Fine-tuning preparation: dataset analysis, format validation, and baseline comparison

---

## What This Implementation Did Not Cover

- Azure OpenAI Service endpoint configuration and regional deployment
- Azure quota management and model deployment approval workflows
- Microsoft Foundry portal experience (prompt flows, evaluations, guardrails)
- Azure Active Directory authentication (`DefaultAzureCredential`, bearer token providers)
- Azure-specific content filtering and responsible AI guardrails
- Azure Monitor, logging, and cost management for deployed models
- Foundry-managed fine-tuning jobs and deployment of a fine-tuned model endpoint

---

## Comparison Table

| Area | Official Microsoft Lab | My Implementation |
|---|---|---|
| **Platform** | Microsoft Foundry / Azure OpenAI Service | OpenAI Platform API |
| **Authentication** | `DefaultAzureCredential`, `get_bearer_token_provider` | `OPENAI_API_KEY` (Codespaces secret) |
| **Client initialisation** | `AzureOpenAI(azure_endpoint=..., azure_ad_token_provider=...)` | `OpenAI()` |
| **Model reference** | Azure deployment name (e.g. `gpt-5-deployment`) | OpenAI model ID (e.g. `gpt-5`) |
| **Chat API** | Chat Completions (`client.chat.completions.create`) | Responses API (`client.responses.create`) |
| **Streaming** | Chat Completions streaming | Responses API streaming via `ResponseTextDeltaEvent` |
| **Multi-turn context** | `messages` history array | `previous_response_id` |
| **Tool calling** | Azure OpenAI function calling | Responses API `tools` parameter (`file_search`, `web_search`) |
| **RAG / file search** | Azure AI Search or Foundry knowledge index | OpenAI vector stores + `file_search` tool |
| **Vector store management** | Azure AI Search index | `client.vector_stores` with reuse-or-create pattern |
| **Fine-tuning** | Azure OpenAI fine-tuning job via Foundry portal | Dataset preparation and baseline evaluation only (job not submitted) |
| **Content safety** | Azure AI Content Safety / Foundry guardrails | OpenAI platform moderation (default) |
| **Infrastructure** | Azure subscription, resource groups, deployments | GitHub Codespaces (no Azure resources provisioned) |
| **Cost model** | Azure consumption billing per token + deployment hours | OpenAI Platform pay-per-token |
| **Environment** | Azure credentials in `.env` or managed identity | `OPENAI_API_KEY` Codespaces secret, `OPENAI_MODEL` in `.env` |

---

## Key Takeaway

The core AI programming concepts — prompt design, multi-turn conversation, tool use, RAG, streaming,
and fine-tuning preparation — transfer directly between Azure OpenAI and the OpenAI Platform because
both implement the OpenAI API specification. The primary gap is operational: Azure-specific deployment,
quota management, Foundry portal workflows, and enterprise authentication were not practised in this
implementation.
