import json
import os
from pathlib import Path

from openai import OpenAI


# This is a local approximation of the Foundry IQ approval pattern, not Foundry IQ itself.
# The Markdown files stand in for a local knowledge source; no Azure Search or Foundry
# resource is contacted by this workaround.
KNOWLEDGE_DIR = Path(__file__).with_name("data")
MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")

TOOLS = [
    {
        "type": "function",
        "name": "search_knowledge_base",
        "description": "Search the local Contoso outdoor product knowledge files.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The product question to search for.",
                }
            },
            "required": ["query"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]

INSTRUCTIONS = (
    "You are a helpful Contoso outdoor-products assistant. "
    "Always use search_knowledge_base for product questions. "
    "Use only information returned by the tool and say when the knowledge files "
    "do not contain an answer."
)


def search_knowledge_base(query: str) -> str:
    """Search copied local Markdown knowledge files with simple term matching."""
    terms = {term.lower() for term in query.split() if len(term) > 2}
    matches = []

    for path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        matching_lines = [
            line.strip()
            for line in lines
            if terms.intersection(set(line.lower().split()))
        ]
        if matching_lines:
            matches.append({"source": path.name, "matches": matching_lines[:12]})

    if not matches:
        return json.dumps({"message": "No matching information found in the local knowledge files."})
    return json.dumps({"results": matches})


def run_turn(client: OpenAI, request: str, previous_response_id: str | None = None) -> str:
    response = client.responses.create(
        model=MODEL,
        instructions=INSTRUCTIONS,
        tools=TOOLS,
        input=request,
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
            arguments = json.loads(item.arguments)
            print(f"Knowledge lookup requested: {arguments['query']}")
            approval = input("Approve local knowledge lookup? (yes/no): ").strip().lower()

            if approval in {"yes", "y"}:
                result = search_knowledge_base(**arguments)
            else:
                result = json.dumps({"status": "denied", "message": "The user denied the knowledge lookup."})

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
        request = input("Ask about Contoso products. Use 'quit' to exit.\nUSER: ").strip()
        if request.lower() == "quit":
            print("Exiting chat.")
            return

        previous_response_id = run_turn(client, request, previous_response_id)


if __name__ == "__main__":
    main()