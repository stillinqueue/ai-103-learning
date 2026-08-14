# m365-teams-integration

Completed Microsoft AI agents exercise: **Deploy agents to Microsoft Teams and Copilot**.

## Local enterprise knowledge agent

`openai-enterprise-agent.py` is the Codespaces/OpenAI learning implementation. It:

- uses `OpenAI()` and the Responses API
- uses OpenAI File Search
- creates or reuses the `enterprise-knowledge-policy` vector store
- grounds answers on `sample_documents/it_security_policy.txt` and `sample_documents/remote_work_policy.txt`
- maintains multi-turn context with `previous_response_id`
- refuses to invent answers when the policy files do not contain the requested information

The local implementation reproduces grounded enterprise-policy behavior. It does not reproduce Teams deployment or Microsoft 365 Copilot publishing.

## Verified tests

- Password requirements: File Search returned the IT Security Policy rules, including a minimum of 12 characters, uppercase/lowercase/numbers/special characters, 90-day changes, and no reuse of the last five passwords.
- Remote-work core hours: File Search returned the Remote Work Policy schedule of Monday-Friday, 9:00 AM-3:00 PM in the employee's local time zone, along with the documented response expectations.
- Disk encryption: File Search returned the IT Security Policy requirement that BitLocker full-disk encryption is required on all company laptops.
- Unsupported vacation-days question: File Search was invoked, but the model correctly said the information was not available in the provided policies and did not invent a vacation allowance.

Each supported answer stayed within the facts in the copied policy documents and identified the relevant policy source.

## Official Microsoft deployment flow

The real lab flow is:

`Foundry agent -> publish/deploy -> Teams app -> optional Microsoft 365 Copilot`

The official configuration is:

- Agent name: `enterprise-knowledge-agent`
- Purpose: Enterprise Knowledge Assistant
- Grounding: uploaded policy documents through File Search

The deployment flow requires more than a working agent:

- Teams publishing requires Microsoft 365 and Teams access.
- Custom Teams app upload may depend on tenant and administrator settings.
- Organization-wide publishing requires admin approval.
- Microsoft 365 Copilot publishing requires the relevant Copilot license.
- Real publishing can create or use Azure-side resources such as Azure Bot Service.

Those deployment steps were not executed because of the current Azure/Microsoft 365 environment constraints. No Teams app was created or published, and no Microsoft 365 Copilot extension was published.
