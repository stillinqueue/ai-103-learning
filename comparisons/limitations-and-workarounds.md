# Limitations and Workarounds — Learning Path 1

## Context

This document records the practical constraints I encountered while working through
**Develop generative AI apps in Azure** (Microsoft Learn AI-103, Learning Path 1)
and explains the decisions made to continue hands-on practice within those constraints.

---

## Constraints Encountered

### Azure Subscription

I used an **Azure Free Trial** subscription for this learning path. The Free Trial provides
sufficient access to explore the Azure portal and some services, but has restricted model
deployment eligibility for newer GPT models.

### GPT-5.2 Quota Unavailable

The Microsoft Learn labs for this path require a **Global Standard GPT-5.2** deployment.
My quota request for this model tier was denied on the Free Trial subscription. Microsoft's
guidance indicated that Pay-As-You-Go subscription status is required for quota eligibility
on current frontier models.

I chose not to upgrade my subscription solely for the introductory labs, as the primary goal
was to understand application-development concepts rather than Azure infrastructure operations.

### VS Code Desktop Not Available

I could not install VS Code Desktop on my company laptop. **GitHub Codespaces** was used as
the development environment throughout this learning path. This was a transparent substitution —
Codespaces runs VS Code in the browser with the same extensions and terminal access.

---

## Workaround Chosen

Where Azure-hosted model calls were blocked by quota, I used the **OpenAI Platform API**
(`api.openai.com`) with the `gpt-5` model available on my OpenAI account.

The `openai` Python SDK works against both Azure OpenAI Service and the OpenAI Platform —
only the client constructor differs. This meant all SDK-level concepts transferred directly.

### Secret Management

- `OPENAI_API_KEY` was stored as a **GitHub Codespaces secret** (encrypted, not visible in logs)
- No secrets were placed in source code
- No secrets were committed to the repository
- `.env` files were used only for non-secret configuration such as `OPENAI_MODEL="gpt-5"`
- `.env` is excluded from version control via `.gitignore`

---

## What the Workaround Allowed Me to Practise

| Concept | Notes |
|---|---|
| Responses API | `client.responses.create()`, `response.output_text` |
| Streaming | `client.responses.stream()`, `ResponseTextDeltaEvent` token iteration |
| Multi-turn conversation state | `previous_response_id` chaining across turns |
| Vector stores | `client.vector_stores.create()`, reuse-or-create pattern |
| `file_search` | PDF batch upload via `upload_and_poll`, retrieval over brochure documents |
| `web_search` | Live search tool attached to a Responses API call |
| RAG | Combining vector store retrieval + web search + conversation context in one call |
| Fine-tuning baseline evaluation | JSONL dataset analysis, format validation, and base model behaviour comparison |

---

## What Remained Azure-Specific

The workaround reproduced **application-development concepts** but did not replace the
**Azure infrastructure experience** that the official labs are designed to provide.

| Area | Why not reproduced |
|---|---|
| Azure OpenAI / Foundry model deployment | Requires quota approval; Free Trial quota denied |
| Azure quota management | No deployable model; quota request and management not practised |
| Azure AD authentication flow | No Azure OpenAI endpoint; `DefaultAzureCredential` and bearer token provider not exercised |
| Foundry portal deployment experience | No deployed Foundry project; portal-based model management not practised |
| Foundry guardrail / content filter configuration | No Foundry deployment; content safety filter threshold and category configuration not practised |
| Azure-specific fine-tuning deployment workflow | Fine-tuning preparation only; job submission and custom endpoint deployment not completed |

---

## Summary

The workaround was a deliberate, transparent decision to maximise learning value within real
constraints. The concepts that transfer directly between Azure OpenAI and the OpenAI Platform —
SDK usage, API design, tool calling, RAG, streaming, and prompt/fine-tuning strategy — were all
practised hands-on. The gap is operational: provisioning, quota management, Azure authentication,
and Foundry-specific portal workflows remain to be completed when adequate Azure access is available.
