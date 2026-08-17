"""Official Azure Translator text translation implementation pattern."""

import os

from azure.ai.translation.text import TextTranslationClient
from azure.ai.translation.text.models import InputTextItem
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


def main() -> None:
    try:
        os.system("cls" if os.name == "nt" else "clear")
        load_dotenv()
        foundry_endpoint = os.getenv("FOUNDRY_ENDPOINT")
        if not foundry_endpoint:
            raise ValueError("FOUNDRY_ENDPOINT is required")

        credential = DefaultAzureCredential()
        client = TextTranslationClient(
            credential=credential,
            endpoint=foundry_endpoint,
        )

        languages_response = client.get_supported_languages(scope="translation")
        print(f"{len(languages_response.translation)} languages supported.")
        print("Enter a target language code for translation (for example, 'en'):")
        target_language = input().strip()
        while target_language not in languages_response.translation:
            print(f"{target_language} is not a supported language.")
            target_language = input().strip()

        input_text = ""
        while input_text.lower() != "quit":
            input_text = input("Enter text to translate ('quit' to exit): ")
            if input_text.lower() == "quit":
                break

            input_text_elements = [InputTextItem(text=input_text)]
            translation_response = client.translate(
                body=input_text_elements,
                to_language=[target_language],
            )
            translation = translation_response[0] if translation_response else None
            if translation:
                source_language = translation.detected_language
                for translated_text in translation.translations:
                    print(
                        f"'{input_text}' was translated from "
                        f"{source_language.language} to {translated_text.to} "
                        f"as '{translated_text.text}'."
                    )
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
