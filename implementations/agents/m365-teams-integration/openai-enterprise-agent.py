import os
from pathlib import Path

from openai import OpenAI


MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
VECTOR_STORE_NAME = "enterprise-knowledge-policy"
POLICY_DIR = Path(__file__).parent / "sample_documents"
POLICY_FILES = [
    POLICY_DIR / "it_security_policy.txt",
    POLICY_DIR / "remote_work_policy.txt",
]

INSTRUCTIONS = """
You are the Contoso Enterprise Knowledge Assistant.
Answer enterprise policy questions only from content retrieved from the attached
policy files. If the policy files do not support an answer, say exactly that the
information is not available in the provided policies. Do not invent policy
facts, dates, benefits, limits, or procedures. Keep answers concise and name the
policy document that supports the answer when possible.
"""


def get_or_create_vector_store(client: OpenAI):
    for vector_store in client.vector_stores.list().data:
        if vector_store.name == VECTOR_STORE_NAME:
            return vector_store
    return client.vector_stores.create(name=VECTOR_STORE_NAME)


def ensure_policy_files(client: OpenAI, vector_store) -> None:
    existing_names = set()
    for vector_store_file in client.vector_stores.files.list(
        vector_store_id=vector_store.id
    ).data:
        file = client.files.retrieve(vector_store_file.id)
        existing_names.add(file.filename)

    for policy_path in POLICY_FILES:
        if policy_path.name in existing_names:
            continue
        with policy_path.open("rb") as policy_file:
            uploaded_file = client.files.create(file=policy_file, purpose="assistants")
        client.vector_stores.files.create_and_poll(
            vector_store_id=vector_store.id,
            file_id=uploaded_file.id,
        )


def run_turn(client: OpenAI, request: str, previous_response_id: str | None = None):
    response = client.responses.create(
        model=MODEL,
        instructions=INSTRUCTIONS,
        tools=[
            {
                "type": "file_search",
                "vector_store_ids": [run_turn.vector_store_id],
            }
        ],
        input=request,
        previous_response_id=previous_response_id,
    )
    file_search_invoked = any(
        item.type == "file_search_call" for item in response.output
    )
    print(f"File Search invoked: {file_search_invoked}")
    print(f"AGENT: {response.output_text}")
    return response.id


def main() -> None:
    client = OpenAI()
    vector_store = get_or_create_vector_store(client)
    ensure_policy_files(client, vector_store)
    run_turn.vector_store_id = vector_store.id

    print(f"Using vector store: {VECTOR_STORE_NAME}")
    previous_response_id = None
    while True:
        request = input("Ask about company policies. Use 'quit' to exit.\nUSER: ").strip()
        if request.lower() == "quit":
            print("Exiting chat.")
            return
        previous_response_id = run_turn(client, request, previous_response_id)


if __name__ == "__main__":
    main()
