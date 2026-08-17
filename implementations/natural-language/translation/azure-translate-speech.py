"""Official Azure Speech translation implementation pattern."""

import os

import azure.cognitiveservices.speech as speech_sdk
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


VOICES = {
    "fr": "fr-FR-HenriNeural",
    "es": "es-ES-ElviraNeural",
    "hi": "hi-IN-MadhurNeural",
}


def main() -> None:
    try:
        os.system("cls" if os.name == "nt" else "clear")
        load_dotenv()
        foundry_endpoint = os.getenv("FOUNDRY_ENDPOINT")
        if not foundry_endpoint:
            raise ValueError("FOUNDRY_ENDPOINT is required")

        credential = DefaultAzureCredential()
        translation_cfg = speech_sdk.translation.SpeechTranslationConfig(
            token_credential=credential,
            endpoint=foundry_endpoint,
        )
        translation_cfg.speech_recognition_language = "en-US"
        for language in VOICES:
            translation_cfg.add_target_language(language)

        audio_in_cfg = speech_sdk.AudioConfig(use_default_microphone=True)
        translator = speech_sdk.translation.TranslationRecognizer(
            translation_config=translation_cfg,
            audio_config=audio_in_cfg,
        )
        print("Ready to translate from", translation_cfg.speech_recognition_language)

        speech_cfg = speech_sdk.SpeechConfig(
            token_credential=credential,
            endpoint=foundry_endpoint,
        )
        print("Ready to use speech service.")

        print("Speak now...")
        translation_results = translator.recognize_once_async().get()
        print(f"Translating '{translation_results.text}'")

        for translation_language, translated_text in translation_results.translations.items():
            print(f"{translation_language}: '{translated_text}'")
            speech_cfg.speech_synthesis_voice_name = VOICES.get(translation_language)
            audio_out_cfg = speech_sdk.audio.AudioOutputConfig(
                use_default_speaker=True
            )
            speech_synthesizer = speech_sdk.SpeechSynthesizer(
                speech_cfg,
                audio_out_cfg,
            )
            speak = speech_synthesizer.speak_text_async(translated_text).get()
            if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
                print(speak.reason)
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
