"""Test a configured custom Document Intelligence model with the sample form."""

import os
from pathlib import Path

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv


TEST_IMAGE = Path(__file__).parent / "samples" / "test1.jpg"


def field_value(field):
    if hasattr(field, "value"):
        return field.value
    if hasattr(field, "content"):
        return field.content
    if hasattr(field, "get"):
        return field.get("valueString") or field.get("content")
    return None


def main() -> None:
    try:
        load_dotenv()
        endpoint = os.getenv("DOC_INTELLIGENCE_ENDPOINT")
        key = os.getenv("DOC_INTELLIGENCE_KEY")
        model_id = os.getenv("MODEL_ID")
        if not endpoint:
            raise ValueError("DOC_INTELLIGENCE_ENDPOINT is required")
        if not key:
            raise ValueError("DOC_INTELLIGENCE_KEY is required")
        if not model_id:
            raise ValueError("MODEL_ID is required")

        client = DocumentIntelligenceClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key),
        )
        with TEST_IMAGE.open("rb") as image_file:
            image_data = image_file.read()

        poller = client.begin_analyze_document(
            model_id,
            AnalyzeDocumentRequest(bytes_source=image_data),
        )
        result = poller.result()

        for index, document in enumerate(result.documents, start=1):
            print(f"--------Analyzing document #{index}--------")
            print(f"Document has type {document.doc_type}")
            print(f"Document has confidence {document.confidence}")
            print(f"Document was analyzed by model with ID {result.model_id}")
            for name, field in document.fields.items():
                print(f"Found field '{name}' with value '{field_value(field)}'")
        print("-----------------------------------")
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
