# Microsoft Foundry client implementation for the AI-103 learning lab.

import os

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient


load_dotenv()

PROJECT_ENDPOINT = os.getenv("PROJECT_ENDPOINT")
AGENT_NAME = os.getenv("AGENT_NAME", "teams-notifications")


def get_agent_by_name(project_client, agent_name: str):
    agents = project_client.agents.list_agents()
    for agent in agents:
        if getattr(agent, "name", None) == agent_name:
            return agent
    raise ValueError(f"No Foundry agent found with name: {agent_name}")


def main():
    if not PROJECT_ENDPOINT:
        raise ValueError("PROJECT_ENDPOINT is required. Set it in your environment or .env file.")

    credential = DefaultAzureCredential()
    project_client = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential)
    openai_client = project_client.get_openai_client()

    agent = get_agent_by_name(project_client, AGENT_NAME)
    conversation = project_client.agents.create_conversation()

    print(f"Connected to Foundry agent: {AGENT_NAME}")
    print("Type 'exit', 'quit', or 'bye' to end the chat.")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit", "bye"}:
            print("Ending chat.")
            break

        if not user_input:
            continue

        project_client.agents.create_message(
            thread_id=conversation.id,
            role="user",
            content=user_input,
        )

        response = project_client.agents.create_run(
            thread_id=conversation.id,
            agent_id=agent.id,
        )

        while True:
            run_status = project_client.agents.get_run(
                thread_id=conversation.id,
                run_id=response.id,
            )
            if run_status.status in {"completed", "failed", "cancelled", "expired"}:
                break

        if run_status.status == "completed":
            messages = project_client.agents.list_messages(thread_id=conversation.id)
            for message in messages.data:
                if getattr(message, "role", None) == "assistant":
                    content = getattr(message, "content", [])
                    if content:
                        for item in content:
                            if getattr(item, "type", None) == "text":
                                print("Agent:", item.text.value)
                                break
                    break
        else:
            print(f"Agent run ended with status: {run_status.status}")


if __name__ == "__main__":
    main()
