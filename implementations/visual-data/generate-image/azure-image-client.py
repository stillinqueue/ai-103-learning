"""Official Azure OpenAI image-generation implementation pattern."""

import base64
import json
import os
from pathlib import Path

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import OpenAI


def create_client() -> tuple[OpenAI, str]:
    load_dotenv()
    endpoint = os.getenv("ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT")
    if not endpoint:
        raise ValueError("ENDPOINT is required")
    if not model_deployment:
        raise ValueError("MODEL_DEPLOYMENT is required")

    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(
        credential,
        "https://ai.azure.com/.default",
    )
    client = OpenAI(
        base_url=endpoint,
        api_key=token_provider(),
    )
    return client, model_deployment


def save_image(image_data: bytes, file_name: str) -> None:
    image_dir = Path.cwd() / "images"
    image_dir.mkdir(exist_ok=True)
    image_path = image_dir / file_name
    image_path.write_bytes(image_data)
    print(f"Image saved as {image_path}")


def main() -> None:
    try:
        client, model_deployment = create_client()
        image_number = 0
        while True:
            input_text = input("Enter the prompt (or type 'quit' to exit): ")
            if input_text.lower() == "quit":
                break
            if not input_text:
                print("Please enter a prompt.")
                continue

            image_response = client.images.generate(
                model=model_deployment,
                prompt=input_text,
                n=1,
            )
            json_response = json.loads(image_response.model_dump_json())
            image_data = json_response["data"][0].get("b64_json")
            if not image_data:
                raise ValueError("Image response did not contain b64_json")
            image_data_in_bytes = base64.b64decode(image_data)

            image_number += 1
            save_image(image_data_in_bytes, f"image_{image_number}.png")
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
