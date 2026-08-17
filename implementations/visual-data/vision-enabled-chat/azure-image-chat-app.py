"""Official Azure OpenAI multimodal image-chat implementation pattern."""

import base64
import os
from pathlib import Path

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import OpenAI


SYSTEM_MESSAGE = (
    "You are an AI assistant in a grocery store that sells fruit. "
    "You provide detailed answers to questions about produce."
)
REMOTE_IMAGE_URL = (
    "https://microsoftlearning.github.io/mslearn-ai-vision/"
    "Labfiles/gen-ai-vision/orange.jpeg"
)


def create_client() -> tuple[OpenAI, str]:
    load_dotenv()
    openai_endpoint = os.getenv("ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT")
    if not openai_endpoint:
        raise ValueError("ENDPOINT is required")
    if not model_deployment:
        raise ValueError("MODEL_DEPLOYMENT is required")

    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(
        credential,
        "https://ai.azure.com/.default",
    )
    client = OpenAI(
        base_url=openai_endpoint,
        api_key=token_provider(),
    )
    return client, model_deployment


def ask_about_url_image(client: OpenAI, model: str, prompt: str) -> str:
    response = client.responses.create(
        model=model,
        input=[
            {"role": "developer", "content": SYSTEM_MESSAGE},
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": REMOTE_IMAGE_URL},
                ],
            },
        ],
    )
    return response.output_text


def local_image_data_url(image_path: Path) -> str:
    with image_path.open("rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{image_data}"


def ask_about_local_image(client: OpenAI, model: str, prompt: str) -> str:
    image_path = Path(__file__).parent / "mystery-fruit.jpeg"
    data_url = local_image_data_url(image_path)
    response = client.responses.create(
        model=model,
        input=[
            {"role": "developer", "content": SYSTEM_MESSAGE},
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": data_url},
                ],
            },
        ],
    )
    return response.output_text


def main() -> None:
    try:
        client, model = create_client()
        while True:
            prompt = input("\nAsk a question about the image (or type 'quit' to exit)\n")
            if prompt.lower() == "quit":
                break
            if not prompt:
                print("Please enter a question.")
                continue

            print("Getting a response for the remote image ...\n")
            print(ask_about_url_image(client, model, prompt))
            print("\nGetting a response for the local image ...\n")
            print(ask_about_local_image(client, model, prompt))
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
