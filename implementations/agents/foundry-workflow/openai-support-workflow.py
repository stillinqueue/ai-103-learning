import json

from openai import OpenAI


TICKETS = [
    "The API returns a 403 error when creating invoices, but our API key hasn't changed.",
    "Is there a way to export all invoices as a CSV?",
    "I was charged twice for the same invoice last Friday and my customer is also seeing two receipts. Can someone fix this?",
]

TRIAGE_INSTRUCTIONS = """
Classify the user's problem description into exactly ONE category from the list below. Provide a confidence score from 0 to 1.

Billing
- Charges, refunds, duplicate payments
- Missing or incorrect payouts
- Subscription pricing or invoices being charged

Technical
- API errors, integrations, webhooks
- Platform bugs or unexpected behavior

General
- How-to questions
- Feature availability
- Data exports, reports, or UI navigation

Important rules
- Questions about exporting, viewing, or downloading invoices are General, not Billing
- Billing ONLY applies when money was charged, refunded, or paid incorrectly
"""

RESOLUTION_INSTRUCTIONS = """
You are a customer support resolution assistant for ContosoPay, a B2B payments and invoicing platform.

Your task is to draft a clear, professional, and friendly support response based on the issue category and customer message.

Guidelines:
If the issue category is Technical:
Suggest 1–2 common troubleshooting steps at a high level.

Avoid asking for logs, credentials, or sensitive data.

Do not imply fault by the customer.
If the issue category is General:
Provide a concise, helpful explanation or guidance.
Keep the response under 5 sentences.

Tone:
Professional, calm, and supportive
Clear and concise
No emojis

Output:
Return only the drafted response text.
Do not include internal reasoning or analysis.
"""

TRIAGE_SCHEMA = {
    "type": "object",
    "properties": {
        "customer_issue": {"type": "string"},
        "category": {
            "type": "string",
            "enum": ["Billing", "Technical", "General"],
        },
        "confidence": {"type": "number"},
    },
    "additionalProperties": False,
    "required": ["customer_issue", "category", "confidence"],
}


def triage_ticket(client: OpenAI, ticket: str) -> dict:
    response = client.responses.create(
        model=MODEL,
        instructions=TRIAGE_INSTRUCTIONS,
        input=ticket,
        text={
            "format": {
                "type": "json_schema",
                "name": "category_response",
                "schema": TRIAGE_SCHEMA,
                "strict": True,
            }
        },
    )
    return json.loads(response.output_text)


def resolve_ticket(client: OpenAI, ticket: str, triage: dict) -> str:
    input_text = json.dumps(
        {
            "customer_ticket": ticket,
            "triage_result": triage,
        }
    )
    response = client.responses.create(
        model=MODEL,
        instructions=RESOLUTION_INSTRUCTIONS,
        input=input_text,
    )
    return response.output_text.strip()


def process_ticket(client: OpenAI, ticket: str) -> dict:
    # Triage Agent workflow node
    triage = triage_ticket(client, ticket)

    # Confidence condition workflow node
    if triage["confidence"] <= 0.6:
        return {
            "customer_issue": triage["customer_issue"],
            "category": triage["category"],
            "confidence": triage["confidence"],
            "response": (
                "The support ticket classification has low confidence. "
                f"Requesting more details about the issue: \"{ticket}\""
            ),
        }

    # Category condition workflow node
    if triage["category"] == "Billing":
        response = "Escalate billing issue to human support team."
    else:
        # Resolution Agent workflow node
        response = resolve_ticket(client, ticket, triage)

    return {
        "customer_issue": triage["customer_issue"],
        "category": triage["category"],
        "confidence": triage["confidence"],
        "response": response,
    }


def main() -> None:
    client = OpenAI()

    # Set tickets workflow node
    tickets = TICKETS

    # For each workflow node
    for ticket_number, ticket in enumerate(tickets, start=1):
        result = process_ticket(client, ticket)
        print(f"Ticket {ticket_number}: {json.dumps(result)}")


if __name__ == "__main__":
    MODEL = __import__("os").environ.get("OPENAI_MODEL", "gpt-5-mini")
    main()
