import os
from dotenv import load_dotenv
from openai import OpenAI
from openai.lib.streaming.responses._events import ResponseTextDeltaEvent


def main():
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Get configuration settings
        load_dotenv()
        model_name = os.getenv("OPENAI_MODEL")

        if not model_name:
            raise ValueError("Please set OPENAI_MODEL in your .env file.")

        # Initialize the OpenAI client using the standard OPENAI_API_KEY environment variable
        client = OpenAI()

        previous_response_id = None

        # Loop until the user wants to quit
        while True:
            input_text = input('\nEnter a prompt (or type "quit" to exit): ')
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue

            # Get a response
            with client.responses.stream(
                model=model_name,
                instructions="You are a helpful AI assistant that answers questions and provides information.",
                input=input_text,
                **({"previous_response_id": previous_response_id} if previous_response_id else {}),
            ) as stream:
                for event in stream:
                    if isinstance(event, ResponseTextDeltaEvent):
                        print(event.delta, end="", flush=True)
                previous_response_id = stream.get_final_response().id
            print()

    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
