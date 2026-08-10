import os
from dotenv import load_dotenv
from openai import OpenAI

SYSTEM_PROMPT = (
    "You are an AI travel assistant that helps people plan their trips. "
    "Your objective is to offer support for travel-related inquiries, such as "
    "visa requirements, weather forecasts, local attractions, and cultural norms. "
    "You should not provide any hotel, flight, rental car or restaurant recommendations. "
    "Ask engaging questions to help someone plan their trip and think about what "
    "they want to do on their holiday."
)

PROMPTS = [
    "What's a must-see in Paris?",
    "What should I do in Tokyo?",
    "Can you recommend a hotel in London?",
    "Tell me something about quantum computing.",
]


def main():
    load_dotenv()
    model_name = os.getenv("OPENAI_MODEL")
    if not model_name:
        raise ValueError("Please set OPENAI_MODEL in your .env file.")

    client = OpenAI()

    for prompt in PROMPTS:
        print(f"\n{'='*60}")
        print(f"USER: {prompt}")
        print(f"{'='*60}")
        response = client.responses.create(
            model=model_name,
            instructions=SYSTEM_PROMPT,
            input=prompt,
        )
        print(f"ASSISTANT: {response.output_text}")


if __name__ == "__main__":
    main()
