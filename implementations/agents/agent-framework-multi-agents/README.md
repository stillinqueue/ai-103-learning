# Multi-agent orchestration

Completed Microsoft Learn exercise: **Develop a multi-agent solution with Microsoft Agent Framework**.

## Official Microsoft Agent Framework implementation

[`agents.py`](agents.py) is the completed official reference implementation. It uses:

- `FoundryChatClient` to connect Microsoft Agent Framework to an Azure AI Foundry project.
- `AzureCliCredential` for Azure CLI-based authentication.
- Three specialized agents:
  - **Summarizer**: creates a short, neutral summary of customer feedback.
  - **Classifier**: classifies feedback as `Positive`, `Negative`, or `Feature request`.
  - **Recommended Action**: suggests the next action using the summary and classification.
- `SequentialBuilder` for sequential orchestration.

The workflow is configured as:

```python
SequentialBuilder(
    participants=[summarizer_agent, classifier_agent, action_agent],
    output_from="all",
).build()
```

`participants=[...]` defines execution order: Summarizer, then Classifier, then Recommended Action. `output_from="all"` collects outputs from every participant, including intermediate outputs. The workflow is run with `workflow.run(...)`, collected with `result.get_outputs()`, and displayed by iterating through the returned messages.

The official implementation was completed and syntax-validated. It was not executable in this Codespaces environment because the `agent_framework` package was not installed, Azure CLI was unauthenticated, and a valid Foundry project endpoint and deployed model are required. This is an environment and dependency limitation, not a failure of Microsoft Agent Framework.

The Azure configuration is supplied through `.env`:

- `AZURE_AI_PROJECT_ENDPOINT`: Foundry project endpoint.
- `AZURE_AI_MODEL_DEPLOYMENT_NAME`: deployed model name, using `gpt-5` in the starter template.

## Local runnable implementation

[`openai-multi-agent.py`](openai-multi-agent.py) reproduces the same behavior with `OpenAI()` and the Responses API. It makes exactly three sequential model calls:

```text
Summarizer -> Classifier -> Recommended Action
```

The Classifier receives the original feedback and Summarizer output. Recommended Action receives the original feedback, the summary, and the classification. The three responsibilities remain separate, and the script prints all three outputs.

This workaround reproduces the orchestration behavior but is not Microsoft Agent Framework.

## Verified runtime example

Input feedback:

> I use the dashboard every day to monitor metrics, and it works well overall. But when I'm working late at night, the bright screen is really harsh on my eyes. If you added a dark mode option, it would make the experience much more comfortable.

Verified outputs:

**Summarizer**

> User requests a dark mode to reduce eye strain when using the dashboard at night.

**Classifier**

> Feature request

**Recommended Action**

> Implement a dark mode theme for the dashboard to reduce eye strain for nighttime users.

All three stages ran successfully, execution order was preserved, no stage was skipped, and no runtime errors occurred.
