"""Official Azure Language implementation pattern for the Analyze Text lab."""

import os
from pathlib import Path

from azure.ai.textanalytics import TextAnalyticsClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


def format_confidence(value: float | None) -> str:
    return f"{value:.3f}" if value is not None else "unavailable"


def main() -> None:
    # Official Azure Language implementation pattern: load the Foundry endpoint
    # and authenticate with the Azure identity chain rather than an API key.
    load_dotenv()
    ai_endpoint = os.getenv("FOUNDRY_ENDPOINT")
    if not ai_endpoint:
        raise ValueError("FOUNDRY_ENDPOINT is required")

    credential = DefaultAzureCredential()
    client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)

    reviews_folder = Path(__file__).parent / "reviews"
    for review_path in sorted(reviews_folder.glob("*.txt")):
        text = review_path.read_text(encoding="utf-8")
        print(f"\n-------------\n{review_path.name}")
        print(f"\n{text}")

        # Official Azure Language operation: detect the review language.
        detected_language = client.detect_language(documents=[text])[0]
        language_name = detected_language.primary_language.name
        language_code = getattr(
            detected_language.primary_language,
            "iso6391_name",
            None,
        )
        if language_code:
            print(f"\nLanguage: {language_name} ({language_code})")
        else:
            print(f"\nLanguage: {language_name}")

        # Official Azure Language operation: recognize named entities.
        entities = client.recognize_entities(documents=[text])[0].entities
        if entities:
            print("\nEntities")
            for entity in entities:
                subcategory = getattr(entity, "subcategory", None)
                confidence = getattr(entity, "confidence_score", None)
                details = f"{entity.text} ({entity.category}"
                if subcategory:
                    details += f", {subcategory}"
                details += f", confidence={format_confidence(confidence)})"
                print(f"\t{details}")

        # Official Azure Language operation: recognize and redact PII.
        pii_result = client.recognize_pii_entities(documents=[text])[0]
        if pii_result.entities:
            print("\nPII Entities")
            for pii_entity in pii_result.entities:
                confidence = getattr(pii_entity, "confidence_score", None)
                print(
                    f"\t{pii_entity.text} ({pii_entity.category}, "
                    f"confidence={format_confidence(confidence)})"
                )
            print(f"Redacted Text:\n{pii_result.redacted_text}")


if __name__ == "__main__":
    main()
