"""Local OpenAI approximation for practice - not Azure Language."""

import json
import os
from pathlib import Path

from openai import OpenAI


MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
REVIEWS_FOLDER = Path(__file__).parent / "reviews"

ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {
        "detected_language": {"type": "string"},
        "iso_language_code": {"type": ["string", "null"]},
        "entities": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "category": {"type": "string"},
                },
                "required": ["text", "category"],
                "additionalProperties": False,
            },
        },
        "pii_entities": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "category": {"type": "string"},
                },
                "required": ["text", "category"],
                "additionalProperties": False,
            },
        },
        "redacted_text": {"type": "string"},
    },
    "required": [
        "detected_language",
        "iso_language_code",
        "entities",
        "pii_entities",
        "redacted_text",
    ],
    "additionalProperties": False,
}

INSTRUCTIONS = """
You are a local NLP practice assistant. Analyze one hotel review and return only
JSON matching the supplied schema.

Detect the review language and provide an ISO 639-1 code only when confident.
Extract named entities with concise, useful categories such as Person, Location,
Organization, Date, or Landmark. Detect likely personally identifiable
information separately, such as email addresses or person names, and provide a
redacted version of the review with each detected PII value replaced by [REDACTED].
If no PII is detected, return the original review as redacted_text and an empty
pii_entities array.

These categories are OpenAI practice labels and are not guaranteed to match
Azure Language categories. Do not claim to be Azure Language.
"""


def analyze_review(client: OpenAI, review_text: str) -> dict:
    response = client.responses.create(
        model=MODEL,
        instructions=INSTRUCTIONS,
        input=review_text,
        text={
            "format": {
                "type": "json_schema",
                "name": "text_analysis",
                "schema": ANALYSIS_SCHEMA,
                "strict": True,
            }
        },
    )
    return json.loads(response.output_text)


def main() -> None:
    client = OpenAI()
    review_paths = sorted(REVIEWS_FOLDER.glob("*.txt"))
    if not review_paths:
        raise FileNotFoundError(f"No review files found in {REVIEWS_FOLDER}")

    for review_path in review_paths:
        review_text = review_path.read_text(encoding="utf-8")
        analysis = analyze_review(client, review_text)
        print(f"--- {review_path.name} ---")
        print(json.dumps(analysis, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
