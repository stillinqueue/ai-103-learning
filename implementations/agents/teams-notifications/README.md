# teams-notifications

- Agent name: `teams-notifications`
- Platform: Microsoft Foundry Agent Service
- Model: `gpt-5-mini`
- Purpose: turn incident/event information into concise Teams notification JSON, grounded in policy and reference documentation

## Foundry implementation

This exercise used a Foundry-style agent configuration with:

- agent name: `teams-notifications`
- model: `gpt-5-mini`
- File Search ground on `notification-policy.txt`
- Code Interpreter over the official Microsoft `system_performance.csv` dataset
- strict JSON output for incident notification requests
- citation/annotation suppression in the JSON response

The grounding file was used to classify urgency based on an explicit policy. The agent instructions were written to route:

- `file_search` → reference-policy retrieval and urgency classification
- `code_interpreter` → CSV analysis, statistics, calculations, and chart generation

This distinction matters because the same agent is expected to handle both operational notification tasks and data analysis requests without forcing the notification schema onto CSV analysis prompts.

## Output schema

```json
{
  "title": "",
  "what_happened": "",
  "impact": "",
  "current_status": "",
  "urgency": "",
  "next_action": ""
}
```

## Behavior

The agent should:

- use only user-provided or tool-retrieved information
- not invent causes, actions, status, timelines, or resolutions
- use File Search against `notification-policy.txt` to classify urgency
- default `next_action` to `Await further information.` when none is provided
- return JSON only for incident-notification requests
- suppress citations/annotations from the JSON output
- use Code Interpreter for CSV analysis and charting rather than File Search

## Programmatic client implementations

- `foundry-client.py` remains the reference Azure Foundry SDK implementation.
- It uses `AIProjectClient` and `DefaultAzureCredential`.
- It could not be runtime-tested from Codespaces because tenant security defaults blocked Azure CLI/device-code authentication.
- `openai-client.py` is the browser/Codespaces workaround using OpenAI Platform.
- It uses the Responses API, retains multi-turn state with `previous_response_id`, and uses OpenAI File Search with a reusable vector store.
- It also uses Code Interpreter with the official Microsoft `system_performance.csv` dataset.

## Verified tests

These checks were performed successfully against the official CSV and the policy file:

- Finance API notification returned urgency `High`
- File Search was invoked successfully
- vector store `teams-notification-policy` was reused
- Code Interpreter correctly identified 19 CSV rows with CPU usage above 80%
- Code Interpreter generated a memory-usage line chart
- memory ranged from 42% to 88%, mean about 58.5%, median about 54%
- generated files included a high-CPU CSV export and a memory chart

## What I learned

- instructions, tools, grounding data, and conversation state all serve different purposes
- attaching a tool does not guarantee the model chooses it correctly
- explicit routing instructions are required for correct tool selection
- policy grounding and system instructions are not interchangeable
- a tenant policy block on Azure CLI authentication is not an SDK/API failure
- persistent agent configuration differs from passing tools directly on each Responses API call

## Test case

Input:

`The Finance API has been unavailable for 15 minutes. Users cannot submit invoices. Support is investigating.`

Expected urgency:

`High`
