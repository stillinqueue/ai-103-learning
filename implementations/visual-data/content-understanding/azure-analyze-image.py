"""Official Azure Content Understanding image-analysis pattern."""

import os
import sys

from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.ai.contentunderstanding.models import AnalysisInput, AnalysisResult
from azure.core.exceptions import AzureError
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


API_VERSION = "2025-11-01"


def print_fields(result: AnalysisResult) -> None:
    fields = result.contents[0].fields
    if "Description" in fields:
        print(f"Description:\n{fields['Description'].value_string}\n")
    if "Tags" in fields:
        print("Tags:")
        for tag in fields["Tags"].value_array:
            print("  -", tag.value_string)


def main() -> None:
    load_dotenv()
    endpoint = os.getenv("ENDPOINT")
    analyzer_id = os.getenv("ANALYZER")
    if not endpoint:
        raise ValueError("ENDPOINT is required")
    if not analyzer_id:
        raise ValueError("ANALYZER is required")

    credential = DefaultAzureCredential()
    client = ContentUnderstandingClient(
        endpoint=endpoint,
        credential=credential,
        api_version=API_VERSION,
    )

    while True:
        file_no = input("\nChoose a file (1, 2, or 3), or anything else to exit: ")
        if file_no not in {"1", "2", "3"}:
            break

        file_path = os.path.join(
            os.path.dirname(__file__), "images", f"image{file_no}.jpg"
        )
        with open(file_path, "rb") as image_file:
            file_bytes = image_file.read()

        print(f"Analyzing with {analyzer_id} analyzer...")
        print(f"  File: {file_path}\n")
        try:
            poller = client.begin_analyze(
                analyzer_id=analyzer_id,
                inputs=[AnalysisInput(data=file_bytes)],
            )
            result: AnalysisResult = poller.result()
            print_fields(result)
        except AzureError as err:
            print(f"[Azure Error]: {err.message}")
            sys.exit(1)
        except Exception as ex:
            print(f"[Unexpected Error]: {ex}")
            sys.exit(1)


if __name__ == "__main__":
    main()
