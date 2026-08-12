import json
import os

from openai import OpenAI

from functions import (
    calculate_observation_cost,
    generate_observation_report,
    next_visible_event,
)


TOOLS = [
    {
        "type": "function",
        "name": "next_visible_event",
        "description": "Get the next visible event in a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "continent to find the next visible event in (e.g. 'north_america', 'south_america', 'australia')",
                },
            },
            "required": ["location"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "calculate_observation_cost",
        "description": "Calculate the cost of an observation based on the telescope tier, number of hours, and priority level.",
        "parameters": {
            "type": "object",
            "properties": {
                "telescope_tier": {
                    "type": "string",
                    "description": "the tier of the telescope (e.g. 'standard', 'advanced', 'premium')",
                },
                "hours": {
                    "type": "number",
                    "description": "the number of hours for the observation",
                },
                "priority": {
                    "type": "string",
                    "description": "the priority level of the observation (e.g. 'low', 'normal', 'high')",
                },
            },
            "required": ["telescope_tier", "hours", "priority"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "generate_observation_report",
        "description": "Generate a report summarizing an astronomical observation",
        "parameters": {
            "type": "object",
            "properties": {
                "event_name": {
                    "type": "string",
                    "description": "the name of the astronomical event being observed",
                },
                "location": {
                    "type": "string",
                    "description": "the location of the observer",
                },
                "telescope_tier": {
                    "type": "string",
                    "description": "the tier of the telescope used for the observation (e.g. 'standard', 'advanced', 'premium')",
                },
                "hours": {
                    "type": "number",
                    "description": "the number of hours the telescope was used for the observation",
                },
                "priority": {
                    "type": "string",
                    "description": "the priority level of the observation (e.g. 'low', 'normal', 'high')",
                },
                "observer_name": {
                    "type": "string",
                    "description": "the name of the person who conducted the observation",
                },
            },
            "required": ["event_name", "location", "telescope_tier", "hours", "priority", "observer_name"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]


FUNCTIONS = {
    "next_visible_event": next_visible_event,
    "calculate_observation_cost": calculate_observation_cost,
    "generate_observation_report": generate_observation_report,
}


INSTRUCTIONS = (
    "You are an astronomy observations assistant that helps users find information "
    "about astronomical events and calculate telescope rental costs. "
    "Use the available tools to assist users with their inquiries."
)


def run_turn(client: OpenAI, model: str, user_request: str) -> None:
    response = client.responses.create(
        model=model,
        instructions=INSTRUCTIONS,
        tools=TOOLS,
        input=user_request,
    )

    while True:
        function_calls = [
            item for item in response.output if item.type == "function_call"
        ]
        if not function_calls:
            print(f"AGENT: {response.output_text}")
            return

        function_outputs = []
        for item in function_calls:
            print(f"Tool called: {item.name}")
            function = FUNCTIONS.get(item.name)
            if function is None:
                result = json.dumps({"error": f"Unknown function '{item.name}'."})
            else:
                arguments = json.loads(item.arguments)
                result = function(**arguments)

            function_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": result,
                }
            )

        response = client.responses.create(
            model=model,
            tools=TOOLS,
            previous_response_id=response.id,
            input=function_outputs,
        )


def main() -> None:
    client = OpenAI()
    model = os.getenv("OPENAI_MODEL", "gpt-5-mini")

    while True:
        user_request = input(
            "Enter a prompt for the astronomy agent. Use 'quit' to exit.\nUSER: "
        ).strip()
        if user_request.lower() == "quit":
            print("Exiting chat.")
            break

        run_turn(client, model, user_request)


if __name__ == "__main__":
    main()
