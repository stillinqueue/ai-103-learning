# astronomy-custom-tools

Completed Microsoft AI agents exercise: **Use a custom function in an AI agent**.

## Implementations

- `agent.py` is the official Microsoft Foundry reference implementation. It uses `AIProjectClient`, `DefaultAzureCredential`, `PromptAgentDefinition`, and Azure `FunctionTool` definitions.
- `openai-agent.py` is the Codespaces/OpenAI Platform implementation. It uses `OpenAI()`, the Responses API, and the same local Python functions and equivalent JSON schemas.

The OpenAI client is a practical fallback for testing the function-calling pattern when Azure/Foundry authentication or quota is unavailable. It does not copy the function implementations; it imports them from `functions.py`.

## Custom tools

The model can request these developer-defined tools:

- `next_visible_event` — finds the next astronomy event visible from a location.
- `calculate_observation_cost` — calculates telescope cost from tier, hours, and priority.
- `generate_observation_report` — creates a report using the event, booking, and observer details.

A function schema describes what the model may request: the tool name, description, parameter types, required arguments, and validation rules. The schema is not the function implementation. The model supplies arguments as JSON, but the application executes the real Python function locally. The model cannot call arbitrary local functions; only functions exposed by the developer are available.

Both implementations use strict schemas with `required` fields and `additionalProperties: False`.

## Function-calling flow

1. The user sends a request to the model with the available function tools.
2. The model returns one or more `function_call` items with JSON arguments.
3. The application parses each call's arguments, selects and executes the matching Python function, and logs the tool name.
4. The application returns each result as `function_call_output`, using the call's `call_id` to link the result to the original request.
5. The application continues with `previous_response_id` until the model returns no more function calls, then prints the final response.

The application must process every returned function call, not only the first. A model can request multiple tools in sequence, as demonstrated by the report request: event lookup, cost calculation, and report generation were all called before the final answer was produced.

## Verified tests

- `next_visible_event` succeeded for North America and returned the Perseids Meteor Shower.
- `calculate_observation_cost` returned `$125.00` for a standard telescope, 2 hours, and normal priority.
- The report request successfully chained all three functions.
- The verified run generated `report_perseids_meteor_shower_2026-08-12_1300.txt`; generated astronomy reports are runtime artifacts and are not tracked.

The current OpenAI client logs tool names, such as `Tool called: next_visible_event`, but does not log raw JSON arguments or raw function outputs. Any detailed JSON arguments or output values recorded from these tests are reconstructed from the successful execution and final response, not copied verbatim from runtime logs.

## Key lesson

Function calling separates decision-making from execution: the model decides which exposed tool to request, while the application controls arguments, executes the real Python code, and returns the result for the model to use in its final response.
