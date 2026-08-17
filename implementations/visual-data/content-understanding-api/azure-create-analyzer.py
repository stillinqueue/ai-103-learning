"""Create a Content Understanding analyzer from the Microsoft business-card schema."""

import json
import os

from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv


def main() -> None:
    try:
        schema_path = os.path.join(os.path.dirname(__file__), "biz-card.json")
        with open(schema_path, encoding="utf-8") as schema_file:
            schema = schema_file.read()

        load_dotenv()
        endpoint = os.getenv("ENDPOINT")
        key = os.getenv("KEY")
        analyzer_name = os.getenv("ANALYZER_NAME")
        if not endpoint:
            raise ValueError("ENDPOINT is required")
        if not key:
            raise ValueError("KEY is required")
        if not analyzer_name:
            raise ValueError("ANALYZER_NAME is required")

        create_analyzer(schema, analyzer_name, endpoint, key)
        print()
    except Exception as ex:
        print(ex)


def create_analyzer(schema: str, analyzer: str, endpoint: str, key: str) -> None:
    print(f"Creating {analyzer}")
    client = ContentUnderstandingClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )
    analyzer_definition = json.loads(schema)
    poller = client.begin_create_analyzer(
        analyzer_id=analyzer,
        resource=analyzer_definition,
        allow_replace=True,
    )
    result = poller.result()
    print(f"Analyzer '{analyzer}' created successfully.")
    print(f"Status: {result['status'] if isinstance(result, dict) else 'Succeeded'}")


if __name__ == "__main__":
    main()
