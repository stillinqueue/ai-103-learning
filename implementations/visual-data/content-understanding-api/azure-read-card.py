"""Analyze a business card with a published Content Understanding analyzer."""

import json
import os
import sys

from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv


def main() -> None:
    try:
        image_file = "biz-card-1.png"
        if len(sys.argv) > 1:
            image_file = sys.argv[1]

        load_dotenv()
        endpoint = os.getenv("ENDPOINT")
        key = os.getenv("KEY")
        analyzer = os.getenv("ANALYZER_NAME")
        if not endpoint:
            raise ValueError("ENDPOINT is required")
        if not key:
            raise ValueError("KEY is required")
        if not analyzer:
            raise ValueError("ANALYZER_NAME is required")

        analyze_card(image_file, analyzer, endpoint, key)
        print()
    except Exception as ex:
        print(ex)


def analyze_card(image_file: str, analyzer: str, endpoint: str, key: str) -> None:
    print(f"Analyzing {image_file}")
    client = ContentUnderstandingClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    with open(image_file, "rb") as image_handle:
        image_data = image_handle.read()

    print("Submitting request...")
    poller = client.begin_analyze_binary(
        analyzer_id=analyzer,
        binary_input=image_data,
    )
    result = poller.result()
    print("Analysis succeeded:\n")

    output_file = "results.json"
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(dict(result), json_file, indent=4, default=str)
    print(f"Response saved in {output_file}\n")

    for content in result.contents:
        if hasattr(content, "fields") and content.fields:
            for field_name, field_data in content.fields.items():
                value = field_data.value if hasattr(field_data, "value") else None
                print(f"{field_name}: {value}")


if __name__ == "__main__":
    main()
