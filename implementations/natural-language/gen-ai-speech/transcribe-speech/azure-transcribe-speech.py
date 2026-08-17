"""Official Azure OpenAI speech-transcription implementation pattern."""

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

        file_path = Path(__file__).parent / "speech.wav"
        with file_path.open("rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=model_deployment,
                file=audio_file,
                response_format="text",
            )

        print(transcription)
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
