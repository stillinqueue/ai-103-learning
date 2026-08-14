# foundry-workflow

Completed Microsoft AI agents exercise: **Build a workflow in Microsoft Foundry**.

## Official Foundry workflow concept

The portal workflow processes ContosoPay support tickets through these visual nodes:

`Set variable -> For each -> Triage Agent -> confidence If/Else -> category If/Else -> Resolution-Agent -> workflow output`

- **Set variable** initializes the support-ticket array.
- **For each** processes one ticket at a time.
- **Triage Agent** classifies each ticket as `Billing`, `Technical`, or `General` and returns structured JSON containing `customer_issue`, `category`, and `confidence`.
- **Confidence If/Else** sends classifications with confidence `<= 0.6` to a request-for-more-details message.
- **Category If/Else** routes high-confidence `Billing` tickets to human escalation.
- **Resolution-Agent** drafts responses for eligible high-confidence `Technical` and `General` tickets.
- **Workflow output** presents each ticket's classification and resulting response.

The real version uses visual workflow nodes and Azure/Microsoft Foundry resources. It was not deployed in this environment.

## Local implementation

`openai-support-workflow.py` reproduces the workflow logic with `OpenAI()` and the Responses API:

- processes the exact three tickets independently in a Python loop
- makes a separate model call for the Triage Agent
- uses structured JSON output with the official fields and categories
- enforces the confidence threshold `<= 0.6`
- routes high-confidence Billing issues to `Escalate billing issue to human support team.`
- routes eligible non-Billing issues to a separate Resolution-Agent model call
- keeps Resolution-Agent responses under five sentences through its instructions

The official categories are exactly:

- `Billing`
- `Technical`
- `General`

## Verified runtime behavior

All three tickets were processed independently inside the loop. Every ticket received a separate Triage Agent call. Tickets 1 and 2 reached the Resolution-Agent; ticket 3 followed the Billing branch and did not call the Resolution-Agent. No runtime ticket had confidence `<= 0.6`, and no errors occurred. All Resolution-Agent outputs stayed under five sentences.

### Ticket 1

```text
The API returns a 403 error when creating invoices, but our API key hasn't changed.
```

```json
{
  "customer_issue": "The API returns a 403 error when creating invoices even though the API key hasn't changed.",
  "category": "Technical",
  "confidence": 0.91
}
```

Branch: Resolution-Agent.

### Ticket 2

```text
Is there a way to export all invoices as a CSV?
```

```json
{
  "customer_issue": "Is there a way to export all invoices as a CSV?",
  "category": "General",
  "confidence": 0.95
}
```

Branch: Resolution-Agent.

### Ticket 3

```text
I was charged twice for the same invoice last Friday and my customer is also seeing two receipts. Can someone fix this?
```

```json
{
  "customer_issue": "I was charged twice for the same invoice last Friday and my customer is also seeing two receipts. Can someone fix this?",
  "category": "Billing",
  "confidence": 0.95
}
```

Branch: Billing escalation.

```text
Escalate billing issue to human support team.
```

The local Python version reproduces the workflow logic, but it is not an actual deployed Microsoft Foundry workflow. The real Foundry version uses visual workflow nodes, Azure resources, and Foundry-hosted agents.
