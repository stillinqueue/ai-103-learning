"""Search an existing Azure AI Search knowledge-mining index."""

import os

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv


SELECTED_FIELDS = ["title", "locations", "persons", "keyPhrases"]


def main() -> None:
    try:
        load_dotenv()
        search_endpoint = os.getenv("SEARCH_ENDPOINT")
        query_key = os.getenv("QUERY_KEY")
        index_name = os.getenv("INDEX_NAME")
        if not search_endpoint:
            raise ValueError("SEARCH_ENDPOINT is required")
        if not query_key:
            raise ValueError("QUERY_KEY is required")
        if not index_name:
            raise ValueError("INDEX_NAME is required")

        search_client = SearchClient(
            endpoint=search_endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(query_key),
        )

        while True:
            query_text = input("Enter a query (or type 'quit' to exit): ")
            if query_text.lower() == "quit":
                break
            if not query_text:
                print("Please enter a query.")
                continue

            found_documents = search_client.search(
                search_text=query_text,
                select=SELECTED_FIELDS,
                order_by=["title"],
                include_total_count=True,
            )
            print(f"\nSearch returned {found_documents.get_count()} documents:")
            for document in found_documents:
                print(f"\nDocument: {document['title']}")
                print(" - Locations:")
                for location in document.get("locations", []):
                    print(f"   - {location}")
                print(" - People:")
                for person in document.get("persons", []):
                    print(f"   - {person}")
                print(" - Key phrases:")
                for phrase in document.get("keyPhrases", []):
                    print(f"   - {phrase}")
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
