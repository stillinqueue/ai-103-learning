# agent-framework

Completed Microsoft AI agents exercise: **Develop an Azure AI chat agent with the Microsoft Agent Framework SDK**.

## Official Microsoft Agent Framework implementation

`agent-framework.py` uses Microsoft Agent Framework as the application-level agent abstraction and orchestration layer. The framework provides:

- `Agent` for agent lifecycle, instructions, tool registration, and agent execution
- `tool` for exposing the local `submit_claim` function to the agent
- `FoundryChatClient` for connecting the framework to the Azure-hosted model/backend
- `agent.run(...)` for sending the expense request and receiving the agent response

The application reads `data.txt`, asks what to do with the expense data, and passes the request plus data to `ExpenseClaimAgent`. The agent is instructed to compose an itemized expense claim and use `submit_claim` to simulate sending an email to `expenses@contoso.com`.

Conversation/chat execution is managed by the Agent Framework run abstraction. The official code depends on Azure/Foundry authentication through `AzureCliCredential`, a real `PROJECT_ENDPOINT`, a deployed model named by `MODEL_DEPLOYMENT_NAME`, and access to Azure AI Agent Service. The reference code was completed and syntax-checked, but not executed in this Codespace because Azure CLI/tenant authentication is blocked and the copied endpoint is only a placeholder.

## Local runnable implementation

`openai-expense-agent.py` is a separate Codespaces workaround. It uses `OpenAI()` and the Responses API to reproduce the same expense-processing behavior, but it is **not Microsoft Agent Framework**.

It:

- loads the same `data.txt` expense records
- accepts interactive expense-related requests
- exposes a local `submit_claim` function as a Responses API function tool
- executes the email simulation in the application
- maintains multi-turn context with `previous_response_id`
- does not invent reimbursement policy, eligibility rules, limits, or approvals that are absent from the lab data

## Verified runtime behavior

The local workaround executed successfully with these prompts:

1. `Submit an expense claim`
2. `What expense items were included in the claim?`

The first response simulated an email to `expenses@contoso.com` with subject `Expense Claim` and the following itemized data:

```text
07-Mar-2025, taxi, 24.00
07-Mar-2025, dinner, 65.50
07-Mar-2025, hotel, 125.90

Total: 215.40
```

The final response confirmed that the claim was submitted and repeated the recipient, subject, three expense items, and total of `215.40`.

The follow-up response correctly listed the same three items and total:

```text
The claim included these items:
- 07-Mar-2025 — taxi — 24.00
- 07-Mar-2025 — dinner — 65.50
- 07-Mar-2025 — hotel — 125.90

Total: 215.40
```

Conversation state worked across turns through `previous_response_id`. No local workaround errors occurred. The limitation is that the OpenAI implementation reproduces the behavior and tool-calling pattern but does not provide Microsoft Agent Framework's abstractions or Azure Foundry backend integration.
