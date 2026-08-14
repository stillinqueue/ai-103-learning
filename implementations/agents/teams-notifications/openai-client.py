import json
import os
import sys
from pathlib import Path

from openai import OpenAI


DEFAULT_MODEL = "gpt-5-mini"
VECTOR_STORE_NAME = "teams-notification-policy"
POLICY_PATH = Path(__file__).with_name("notification-policy.txt")
CSV_PATH = Path(__file__).with_name("system_performance.csv")
SYSTEM_INSTRUCTIONS = """
You are a Teams notification assistant and a data-analysis assistant.

Tool routing rules:
- Use file_search only for notification-policy or reference-document retrieval.
- Use code_interpreter only for CSV analysis, calculations, statistics, filtering, aggregation, and chart generation.
- Do not use File Search to analyze CSV data.

Notification mode:
- Produce concise, professional Teams notifications.
- Use only user-provided information and the retrieved notification policy from File Search.
- Never invent causes, risks, actions, stakeholders, timelines, resolutions, or future updates.
- Use the next_action field only when the source explicitly provides one.
- If no next action is supplied, use "Await further information."
- Urgency must be classified using the retrieved notification policy.
- Do not invent urgency rules.
- If the policy cannot classify the incident, set the urgency value to an empty string.
- Return JSON only.
- Do not include citations, annotations, footnotes, or source markers inside the JSON.

Urgency classification policy:
Critical:
- A complete outage of a business-critical service affecting all or nearly all users.
- A confirmed active security incident with significant impact.
- A critical business process is completely unavailable across the organization.

High:
- A service outage or degradation affecting a significant group of users.
- An important business process is unavailable for some users or teams.
- Users are unable to complete an important task, but there is no evidence of organization-wide impact.

Medium:
- Limited user impact.
- A workaround is available.
- A non-critical service is degraded.

Low:
- Informational update.
- Planned maintenance.
- No immediate user impact.

Classification rules:
- Use only evidence explicitly provided in the incident information and the retrieved notification policy.
- Do not assume organization-wide impact.
- Do not classify an incident as Critical unless the provided information explicitly supports a Critical condition.
- If scope is unclear, choose the lower applicable severity.
- If the policy cannot classify the incident, return an empty urgency string.

Exact JSON output schema:
{
  "title": "",
  "what_happened": "",
  "impact": "",
  "current_status": "",
  "urgency": "",
  "next_action": ""
}

Data-analysis mode:
- If the request is about a CSV file, use code_interpreter and provide a normal explanatory response.
- Do not force the six-field Teams JSON schema for CSV analysis tasks.
- For chart requests, create the chart using code_interpreter and then summarize the results.
- Do not use File Search for CSV analysis.

Output requirements:
- JSON only for notification requests.
- Natural explanatory responses for data-analysis requests.
- no markdown fences when returning Teams JSON.
- no prose outside the JSON object for notification requests.
- preserve the exact keys and field names shown above for notification JSON.
"""


def get_model_name() -> str:
    return os.environ.get("OPENAI_MODEL", DEFAULT_MODEL)


def get_or_create_vector_store(client):
    vector_stores = client.vector_stores.list().data
    for store in vector_stores:
        if store.name == VECTOR_STORE_NAME:
            return store
    return client.vector_stores.create(name=VECTOR_STORE_NAME)


def ensure_policy_file_in_store(client, vector_store_id):
    try:
        existing_files = client.vector_stores.files.list(vector_store_id=vector_store_id).data
        for file_obj in existing_files:
            if getattr(file_obj, "filename", "") == POLICY_PATH.name:
                return file_obj
    except Exception:
        pass

    with POLICY_PATH.open("rb") as file_handle:
        uploaded_file = client.files.create(file=file_handle, purpose="assistants")

    client.vector_stores.file_batches.create(
        vector_store_id=vector_store_id,
        file_ids=[uploaded_file.id],
    )
    return uploaded_file


def is_data_analysis_request(user_text: str) -> bool:
    lower_text = user_text.lower()
    csv_markers = [".csv", "csv", "chart", "graph", "line chart", "bar chart", "analyze", "analysis", "statistics", "aggregate", "filter", "summarize"]
    return any(marker in lower_text for marker in csv_markers)


def upload_csv_for_code_interpreter(client):
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV file not found: {CSV_PATH}")

    with CSV_PATH.open("rb") as csv_file:
        return client.files.create(file=csv_file, purpose="assistants")


def get_response_tools(vector_store_id: str, csv_file_id: str | None = None):
    tools = [{"type": "file_search", "vector_store_ids": [vector_store_id]}]
    tools.append({
        "type": "code_interpreter",
        "container": {"type": "auto", "file_ids": [csv_file_id] if csv_file_id else []},
    })
    return tools


def extract_json_payload(response_text: str):
    cleaned = response_text.strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        cleaned = cleaned[start : end + 1]
    return json.loads(cleaned)


def extract_generated_file_names(response):
    generated = []
    for item in getattr(response, "output", []) or []:
        item_type = getattr(item, "type", None)
        if item_type == "code_interpreter_call":
            for output_item in getattr(item, "output", []) or []:
                if getattr(output_item, "type", None) == "file":
                    file_id = getattr(output_item, "id", None)
                    filename = getattr(output_item, "filename", None) or file_id or "unknown"
                    generated.append({"filename": filename, "id": file_id})
        if item_type == "file":
            file_id = getattr(item, "id", None)
            filename = getattr(item, "filename", None) or file_id or "unknown"
            generated.append({"filename": filename, "id": file_id})
    return generated


def main() -> None:
    model_name = get_model_name()
    client = OpenAI()
    previous_response_id = None

    vector_store = get_or_create_vector_store(client)
    ensure_policy_file_in_store(client, vector_store.id)
    csv_file = upload_csv_for_code_interpreter(client)

    print(f"Teams notification client using model: {model_name}")
    print(f"Using vector store: {vector_store.name} ({vector_store.id})")
    print(f"Using Code Interpreter CSV: {CSV_PATH.name} (file_id={csv_file.id})")
    print("Type 'exit' to quit.")

    while True:
        try:
            user_text = input("\nIncident details: ").strip()
        except EOFError:
            print()
            break

        if not user_text:
            continue
        if user_text.lower() in {"exit", "quit", "q"}:
            break

        if is_data_analysis_request(user_text):
            if not CSV_PATH.exists():
                print(f"Data analysis unavailable: {CSV_PATH} is not present in this folder. Please add system_performance.csv before running CSV analysis requests.")
                continue

            try:
                response = client.responses.create(
                    model=model_name,
                    input=user_text,
                    previous_response_id=previous_response_id,
                    instructions=SYSTEM_INSTRUCTIONS,
                    tools=get_response_tools(vector_store.id, csv_file.id),
                )

                code_interpreter_invoked = any(item.type == "code_interpreter_call" for item in getattr(response, "output", []) or [])
                print(f"Code Interpreter invoked: {'yes' if code_interpreter_invoked else 'no'}")

                generated_files = extract_generated_file_names(response)
                if generated_files:
                    print(f"Generated files: {generated_files}")
                else:
                    print("Generated files: none")

                print(response.output_text.strip())
                previous_response_id = response.id
            except Exception as exc:
                print(f"Error: {exc}", file=sys.stderr)
                previous_response_id = None
            continue

        try:
            response = client.responses.create(
                model=model_name,
                input=user_text,
                previous_response_id=previous_response_id,
                instructions=SYSTEM_INSTRUCTIONS,
                tools=get_response_tools(vector_store.id, csv_file.id),
            )

            file_search_invoked = any(item.type == "file_search_call" for item in response.output)
            code_interpreter_invoked = any(item.type == "code_interpreter_call" for item in response.output)
            print(f"File Search invoked: {'yes' if file_search_invoked else 'no'}")
            print(f"Code Interpreter invoked: {'yes' if code_interpreter_invoked else 'no'}")

            output_text = response.output_text.strip()
            payload = extract_json_payload(output_text)
            print(json.dumps(payload, ensure_ascii=True))

            previous_response_id = response.id

        except Exception as exc:
            print(f"Error: {exc}", file=sys.stderr)
            previous_response_id = None


if __name__ == "__main__":
    main()
