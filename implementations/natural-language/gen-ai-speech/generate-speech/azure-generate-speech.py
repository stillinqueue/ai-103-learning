"""Official Azure OpenAI speech-synthesis implementation pattern."""

import os
from pathlib import Path

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import AzureOpenAI


def main() -> None:
    try:
        load_dotenv()
        endpoint = os.getenv("MODEL_ENDPOINT")
        model_deployment = os.getenv("MODEL_NAME")
        if not endpoint:
            raise ValueError("MODEL_ENDPOINT is required")
        if not model_deployment:
            raise ValueError("MODEL_NAME is required")

        # Official Azure authentication pattern for the speech-capable model.
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(),
            "https://ai.azure.com/.default",
        )
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            azure_ad_token_provider=token_provider,
            api_version="2025-03-01-preview",
        )

        speech_file_path = Path(__file__).parent / "speech.mp3"
        with client.audio.speech.with_streaming_response.create(
            model=model_deployment,
            voice="alloy",
            input="My voice is my passport!",
            instructions="Speak in a serious tone.",
        ) as response:
            response.stream_to_file(speech_file_path)

        print(f"Speech saved to {speech_file_path}")
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
