"""Official Microsoft Foundry client pattern for the text analysis agent lab."""

from dotenv import load_dotenv
import os

# Official Azure/Foundry client namespaces.
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient


def main() -> None:
    try:
        # Clear the console
        os.system("cls" if os.name == "nt" else "clear")

        # Get configuration settings
        load_dotenv()
        foundry_endpoint = os.getenv("FOUNDRY_ENDPOINT")
        agent_name = os.getenv("AGENT_NAME")
        if not foundry_endpoint:
            raise ValueError("FOUNDRY_ENDPOINT is required")
        if not agent_name:
            raise ValueError("AGENT_NAME is required")

        # Get project client for the existing Foundry project.
        project_client = AIProjectClient(
            endpoint=foundry_endpoint,
            credential=DefaultAzureCredential(),
        )

        # Get an OpenAI-compatible client from the Foundry project.
        openai_client = project_client.get_openai_client()

        # Use the existing Foundry agent, which is configured with the Azure
        # Language MCP tool in the Foundry portal.
        prompt = input("User prompt: ")
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
        print(f"\nResponse Details: {response.model_dump_json(indent=2)}")

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
