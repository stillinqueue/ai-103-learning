"""Local OpenAI API multimodal practice - not Azure OpenAI/Foundry runtime verification."""

import base64
from pathlib import Path

from openai import OpenAI


MODEL = "gpt-4o-mini"
SYSTEM_MESSAGE = (
    "You are an AI assistant in a grocery store that sells fruit. "
    "You provide detailed answers to questions about produce."
)
REMOTE_IMAGE_URL = (
    "https://microsoftlearning.github.io/mslearn-ai-vision/"
    "Labfiles/gen-ai-vision/orange.jpeg"
)
LOCAL_IMAGE_PATH = Path(__file__).parent / "mystery-fruit.jpeg"
PROMPT = "What fruit is shown, and what are two useful observations about it?"


def local_image_data_url() -> str:
    with LOCAL_IMAGE_PATH.open("rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{image_data}"


def ask(client: OpenAI, image_url: str) -> str:
    response = client.responses.create(
        model=MODEL,
        input=[
            {"role": "developer", "content": SYSTEM_MESSAGE},
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": PROMPT},
                    {"type": "input_image", "image_url": image_url},
                ],
            },
        ],
    )
    return response.output_text.strip()


def main() -> None:
    client = OpenAI()
    print(f"URL image response ({MODEL}):")
    print(ask(client, REMOTE_IMAGE_URL))
    print("\nLocal base64 image response:")
    print(ask(client, local_image_data_url()))


if __name__ == "__main__":
    main()
