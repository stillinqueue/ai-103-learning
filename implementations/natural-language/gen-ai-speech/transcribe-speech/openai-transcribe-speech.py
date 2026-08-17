"""Local OpenAI API practice implementation - not Azure Foundry/AzureOpenAI runtime verification."""

from pathlib import Path

from openai import OpenAI


MODEL = "gpt-4o-mini-transcribe"
AUDIO_PATH = Path(__file__).parent / "speech.wav"


def main() -> None:
    client = OpenAI()
    with AUDIO_PATH.open("rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=MODEL,
            file=audio_file,
            response_format="text",
        )

    print(transcription)


if __name__ == "__main__":
    main()
