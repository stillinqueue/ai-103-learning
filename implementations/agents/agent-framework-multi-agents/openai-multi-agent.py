import os

from openai import OpenAI


MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
FEEDBACK = """
I use the dashboard every day to monitor metrics, and it works well overall.
But when I'm working late at night, the bright screen is really harsh on my eyes.
If you added a dark mode option, it would make the experience much more comfortable.
""".strip()

SUMMARIZER_INSTRUCTIONS = """
Summarize the customer's feedback in one short sentence. Keep it neutral and concise.
Return only the summary.
"""

CLASSIFIER_INSTRUCTIONS = """
Classify the feedback as exactly one of: Positive, Negative, or Feature request.
Return only the classification.
"""

ACTION_INSTRUCTIONS = """
Based on the customer feedback summary and classification, suggest the next action
in one short sentence. Return only the recommended action.
"""


def summarize_feedback(client: OpenAI, feedback: str) -> str:
    response = client.responses.create(
        model=MODEL,
        instructions=SUMMARIZER_INSTRUCTIONS,
        input=f"Customer feedback:\n{feedback}",
    )
    return response.output_text.strip()


def classify_feedback(client: OpenAI, feedback: str, summary: str) -> str:
    response = client.responses.create(
        model=MODEL,
        instructions=CLASSIFIER_INSTRUCTIONS,
        input=(
            f"Customer feedback:\n{feedback}\n\n"
            f"Summarizer output:\n{summary}"
        ),
    )
    return response.output_text.strip()


def recommend_action(
    client: OpenAI,
    feedback: str,
    summary: str,
    classification: str,
) -> str:
    response = client.responses.create(
        model=MODEL,
        instructions=ACTION_INSTRUCTIONS,
        input=(
            f"Customer feedback:\n{feedback}\n\n"
            f"Summarizer output:\n{summary}\n\n"
            f"Classifier output:\n{classification}"
        ),
    )
    return response.output_text.strip()


def main() -> None:
    client = OpenAI()

    summary = summarize_feedback(client, FEEDBACK)
    classification = classify_feedback(client, FEEDBACK, summary)
    recommended_action = recommend_action(
        client,
        FEEDBACK,
        summary,
        classification,
    )

    outputs = [summary, classification, recommended_action]
    if not all(outputs):
        raise RuntimeError("One or more orchestration stages returned no output.")

    print(f"Input feedback:\n{FEEDBACK}\n")
    print(f"Summarizer:\n{summary}\n")
    print(f"Classifier:\n{classification}\n")
    print(f"Recommended Action:\n{recommended_action}")


if __name__ == "__main__":
    main()
