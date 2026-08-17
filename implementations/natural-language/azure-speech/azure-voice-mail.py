"""Official Azure Speech SDK voice-mail implementation pattern."""

import os
from pathlib import Path

import azure.cognitiveservices.speech as speech_sdk
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from playsound3 import playsound


VOICE_NAME = "en-US-Serena:DragonHDLatestNeural"


def record_greeting(speech_config: speech_sdk.SpeechConfig) -> None:
    print("Recording greeting...")
    greeting_message = input("Enter your greeting message: ")

    output_file = "greeting.wav"
    audio_config = speech_sdk.audio.AudioOutputConfig(filename=output_file)
    speech_config.speech_synthesis_voice_name = VOICE_NAME
    speech_synthesizer = speech_sdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config,
    )
    result = speech_synthesizer.speak_text_async(greeting_message).get()

    if result.reason == speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Greeting recorded and saved to {output_file}")
        speech_synthesizer = None
    else:
        print(f"Error recording greeting: {result.reason}")


def transcribe_messages(speech_config: speech_sdk.SpeechConfig) -> None:
    print("Transcribing messages...")
    messages_folder = Path(__file__).parent / "messages"
    for file_path in sorted(messages_folder.glob("*.wav")):
        print(f"\nTranscribing {file_path.name}...")
        playsound(str(file_path))

        audio_config = speech_sdk.audio.AudioConfig(filename=str(file_path))
        speech_recognizer = speech_sdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config,
        )
        result = speech_recognizer.recognize_once_async().get()
        if result.reason == speech_sdk.ResultReason.RecognizedSpeech:
            print(f"Transcription: {result.text}")
        else:
            print(f"Error transcribing message: {result.reason}")


def main() -> None:
    try:
        os.system("cls" if os.name == "nt" else "clear")
        load_dotenv()
        foundry_endpoint = os.getenv("FOUNDRY_ENDPOINT")
        if not foundry_endpoint:
            raise ValueError("FOUNDRY_ENDPOINT is required")

        credential = DefaultAzureCredential()
        speech_config = speech_sdk.SpeechConfig(
            token_credential=credential,
            endpoint=foundry_endpoint,
        )

        input_text = ""
        while input_text.lower() != "3":
            input_text = input(
                "Choose an option:\n"
                "1: Record a greeting\n"
                "2: Transcribe messages\n"
                "3: Exit\n"
            )
            if input_text == "1":
                record_greeting(speech_config)
            elif input_text == "2":
                transcribe_messages(speech_config)
            elif input_text != "3":
                print("Invalid option, please try again.")

        print("Exiting...")
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
