# foundry-iq

Completed Microsoft AI agents exercise: **Integrate an AI agent with Foundry IQ**.

## Official Foundry reference

`agent_client.py` is the official Azure/Foundry reference client. It:

- creates an `AIProjectClient`
- authenticates with `DefaultAzureCredential`
- retrieves an existing Foundry agent by name
- creates a conversation
- uses the Responses API
- detects `mcp_approval_request` items
- creates `mcp_approval_response` items for approval or denial
- continues the conversation after the approval decision
- displays the agent response and any available citations

The real Foundry IQ workflow requires Azure-side configuration that was not created in this Codespace:

- a Microsoft Foundry project and model deployment
- a Foundry agent configured with Foundry IQ knowledge
- an Azure AI Search resource
- an Azure Storage account and Blob container containing the product documents
- a Foundry IQ knowledge base and indexed knowledge source
- Entra authentication and permissions for the project, agent, and connected resources

The copied `.env` retains placeholders and contains no real Azure values.

## Local Codespaces approximation

`openai-approval-agent.py` uses `OpenAI()` and the Responses API to reproduce the approval-control pattern locally. It:

- exposes a local `search_knowledge_base` tool
- searches the copied Contoso Markdown documents
- pauses before executing the lookup
- requires explicit user approval
- executes the lookup only after `yes`
- returns a denial result instead of executing after `no`
- preserves `call_id` in `function_call_output`
- continues the response with `previous_response_id`

This reproduces the approval-control pattern but is **not Foundry IQ**. The local Markdown search is not Azure AI Search, and it does not connect to a Foundry project, agent, or knowledge base.

## Verified tests

### Approved lookup

Question: `What backpacks are available for a multi-day hiking trip?`

- The model requested `search_knowledge_base`.
- Execution paused before the lookup.
- The user approved the request.
- The lookup executed successfully after approval.
- The summarized grounded result included weekend packs around 40–50 L and expedition packs around 60–75 L.

### Denied lookup

Question: `What tents are available for camping?`

- The model requested `search_knowledge_base`.
- Execution paused before the lookup.
- The user denied the request.
- The knowledge lookup did not execute.
- The application returned:

```json
{"status":"denied","message":"The user denied the knowledge lookup."}
```

- The model then produced a general non-grounded answer.

The current OpenAI script does not print the raw function output for the approved lookup. The backpack result above is summarized from successful execution and the final response, not presented as verbatim runtime JSON.

## Key lesson

A tool request is not tool execution. Approval is a control point between model intent and application execution. Grounding and approval are separate concepts: approval controls whether the lookup may run, while grounding controls the source of information used to answer. Foundry IQ knowledge integration is a specific Azure knowledge-base workflow and is not the same as generic File Search.
