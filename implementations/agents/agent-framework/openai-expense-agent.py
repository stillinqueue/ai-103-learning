import json
import os
from pathlib import Path

from openai import OpenAI


MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
EXPENSE_DATA = (Path(__file__).parent / "data.txt").read_text(encoding="utf-8").strip()

# This is a local OpenAI workaround, not Microsoft Agent Framework.
# It reproduces the expense-agent learning behavior with the Responses API.
INSTRUCTIONS = """
You are an AI assistant for expense claim submission.
At the user's request, create an expense claim and use the submit_claim tool to
send an email to expenses@contoso.com with the subject 'Expense Claim' and a
body that contains itemized expenses with a total. Then confirm to the user that
you've done so. Do not ask for more information when the provided expense data
is sufficient. Use only the expense data supplied by the application. Do not
invent reimbursement policy, eligible categories, limits, or approval rules.
"""

TOOLS = [
    {
        "type": "function",
        "name": "submit_claim",
        "description": "Simulate sending the completed expense claim by email.",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "Who to send the email to",
                },
                "subject": {
                    "type": "string",
                    "description": "The subject of the email.",
                },
                "body": {
                    "type": "string",
                    "description": "The text body of the email.",
                },
            },
            "required": ["to", "subject", "body"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]


def submit_claim(to: str, subject: str, body: str) -> str:
    """Simulate the official starter's email tool locally."""
    print(f"\nTo: {to}\nSubject: {subject}\n{body}\n")
    return json.dumps({"status": "Expense claim email simulated", "recipient": to})


def run_turn(client: OpenAI, user_request: str, previous_response_id: str | None):
    if previous_response_id is None:
        input_text = f"Expense data:\n{EXPENSE_DATA}\n\nUser request: {user_request}"
    else:
        input_text = user_request

    response = client.responses.create(
        model=MODEL,
        instructions=INSTRUCTIONS,
        tools=TOOLS,
        input=input_text,
        previous_response_id=previous_response_id,
    )

    while True:
        function_calls = [
            item for item in response.output if item.type == "function_call"
        ]
        if not function_calls:
            print(f"AGENT: {response.output_text}")
            return response.id

        function_outputs = []
        for item in function_calls:
            if item.name == "submit_claim":
                arguments = json.loads(item.arguments)
                result = submit_claim(**arguments)
            else:
                result = json.dumps({"error": f"Unknown tool: {item.name}"})

            function_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": result,
                }
            )

        response = client.responses.create(
            model=MODEL,
            tools=TOOLS,
            previous_response_id=response.id,
            input=function_outputs,
        )


def main() -> None:
    client = OpenAI()
    previous_response_id = None

    while True:
        user_request = input(
            "What would you like me to do with the expenses data? Use 'quit' to exit.\nUSER: "
        ).strip()
        if user_request.lower() == "quit":
            print("Exiting chat.")
            return

        previous_response_id = run_turn(client, user_request, previous_response_id)


if __name__ == "__main__":
    main()
