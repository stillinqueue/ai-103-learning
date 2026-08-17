"""Local OpenAI API practice implementation - not Azure Foundry/AzureOpenAI runtime verification."""

from pathlib import Path

from openai import OpenAI


MODEL = "gpt-4o-mini-tts"
OUTPUT_PATH = Path(__file__).parent / "openai-speech.mp3"


def main() -> None:
    client = OpenAI()
    with client.audio.speech.with_streaming_response.create(
        model=MODEL,
        voice="alloy",
        input="My voice is my passport!",
        instructions="Speak in a serious tone.",
    ) as response:
        response.stream_to_file(OUTPUT_PATH)

    print(f"Generated {OUTPUT_PATH.name} with model {MODEL} using voice alloy.")


if __name__ == "__main__":
    main()
