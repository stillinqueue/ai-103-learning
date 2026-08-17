"""Official Microsoft Foundry client pattern for the Azure Speech MCP lab."""

import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


def main() -> None:
    try:
        load_dotenv()
        foundry_endpoint = os.getenv("FOUNDRY_ENDPOINT")
        agent_name = os.getenv("AGENT_NAME")
        if not foundry_endpoint:
            raise ValueError("FOUNDRY_ENDPOINT is required")
        if not agent_name:
            raise ValueError("AGENT_NAME is required")

        # The Python client authenticates to the Foundry project. The existing
        # Foundry agent owns the Azure Speech MCP tool configuration.
        project_client = AIProjectClient(
            endpoint=foundry_endpoint,
            credential=DefaultAzureCredential(),
        )
        openai_client = project_client.get_openai_client()

        while True:
            prompt = input("User prompt (or 'quit'): ")
            if prompt == "quit" or not prompt:
                break

            response = openai_client.responses.create(
                input=[{"role": "user", "content": prompt}],
                extra_body={
                    "agent_reference": {
                        "name": agent_name,
                        "type": "agent_reference",
                    }
                },
            )
            print(f"{agent_name}: {response.output_text}")
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
