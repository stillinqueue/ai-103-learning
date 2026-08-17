"""Local OpenAI API image-generation practice - not Azure OpenAI runtime verification."""

import base64
import json
from pathlib import Path

from openai import OpenAI


MODEL = "gpt-image-2"
PROMPT = "A watercolor illustration of a red fox reading a book under a tree, simple educational style."
OUTPUT_PATH = Path(__file__).parent / "openai-image.png"


def main() -> None:
    client = OpenAI()
    image_response = client.images.generate(
        model=MODEL,
        prompt=PROMPT,
        n=1,
    )
    json_response = json.loads(image_response.model_dump_json())
    image_data = json_response["data"][0].get("b64_json")
    if not image_data:
        raise ValueError("Image response did not contain b64_json")

    image_bytes = base64.b64decode(image_data)
    OUTPUT_PATH.write_bytes(image_bytes)
    print(f"Generated {OUTPUT_PATH.name} with model {MODEL} ({len(image_bytes)} bytes).")


if __name__ == "__main__":
    main()
