"""Analyze the Microsoft sample invoice with the prebuilt invoice model."""

import os

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv


INVOICE_URL = (
    "https://raw.githubusercontent.com/MicrosoftLearning/"
    "mslearn-ai-information-extraction/main/Labfiles/03-document-intelligence/"
    "prebuilt/sample-invoice/sample-invoice.pdf"
)


def main() -> None:
    try:
        load_dotenv()
        endpoint = os.getenv("ENDPOINT")
        key = os.getenv("KEY")
        if not endpoint:
            raise ValueError("ENDPOINT is required")
        if not key:
            raise ValueError("KEY is required")

        client = DocumentIntelligenceClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key),
        )
        poller = client.begin_analyze_document(
            "prebuilt-invoice",
            AnalyzeDocumentRequest(url_source=INVOICE_URL),
            locale="en-US",
        )
        result = poller.result()

        for document in result.documents:
            vendor_name = document.fields.get("VendorName")
            if vendor_name:
                print(
                    f"Vendor Name: {vendor_name.get('valueString')}, "
                    f"confidence {vendor_name.get('confidence')}."
                )
            customer_name = document.fields.get("CustomerName")
            if customer_name:
                print(
                    f"Customer Name: {customer_name.get('valueString')}, "
                    f"confidence {customer_name.get('confidence')}."
                )
            invoice_total = document.fields.get("InvoiceTotal")
            if invoice_total:
                amount = invoice_total.get("valueCurrency", {})
                print(
                    f"Invoice Total: {amount.get('currencySymbol', '$')}"
                    f"{amount.get('amount')}, confidence "
                    f"{invoice_total.get('confidence')}."
                )
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
