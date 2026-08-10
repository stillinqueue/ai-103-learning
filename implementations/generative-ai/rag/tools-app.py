import os
from dotenv import load_dotenv
import glob
from openai import OpenAI


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

        # Reuse an existing vector store named 'travel-brochures', or create and populate one
        existing = [vs for vs in client.vector_stores.list() if vs.name == "travel-brochures"]
        if existing:
            vector_store = existing[0]
            print(f"Reusing existing vector store: {vector_store.id}")
        else:
            print("Creating vector store and uploading brochures...")
            vector_store = client.vector_stores.create(name="travel-brochures")
            pdf_paths = glob.glob("brochures/*.pdf")
            file_handles = [open(p, "rb") for p in pdf_paths]
            try:
                client.vector_stores.file_batches.upload_and_poll(
                    vector_store_id=vector_store.id,
                    files=[(os.path.basename(p), fh) for p, fh in zip(pdf_paths, file_handles)],
                )
            finally:
                for fh in file_handles:
                    fh.close()
            print(f"Created new vector store: {vector_store.id} ({len(pdf_paths)} brochures uploaded)")

        tools = [
            {"type": "file_search", "vector_store_ids": [vector_store.id]},
            {"type": "web_search"},
        ]

        instructions = (
            "You are a travel assistant that provides information on travel services "
            "available from Margie's Travel. Answer questions about services offered by "
            "Margie's Travel using the provided travel brochures. Search the web for "
            "general information about destinations or current travel advice."
        )

        # Track conversation state
        last_response_id = None

        # Loop until the user wants to quit
        while True:
            input_text = input('\nEnter a question (or type "quit" to exit): ')
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a question.")
                continue

            # Get a response using tools
            response = client.responses.create(
                model=model_name,
                instructions=instructions,
                input=input_text,
                tools=tools,
                **({"previous_response_id": last_response_id} if last_response_id else {}),
            )
            last_response_id = response.id
            print(response.output_text)

    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
