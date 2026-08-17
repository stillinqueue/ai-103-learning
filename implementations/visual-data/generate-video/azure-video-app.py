"""Official Azure OpenAI Sora video-generation implementation pattern."""

import os
import time

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import OpenAI


def create_client() -> tuple[OpenAI, str]:
    load_dotenv()
    endpoint = os.getenv("OPENAI_BASE_URL")
    model_deployment = os.getenv("MODEL_DEPLOYMENT")
    if not endpoint:
        raise ValueError("OPENAI_BASE_URL is required")
    if not model_deployment:
        raise ValueError("MODEL_DEPLOYMENT is required")

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://cognitiveservices.azure.com/.default",
    )
    client = OpenAI(
        base_url=endpoint,
        api_key=token_provider,
    )
    return client, model_deployment


def poll_video_status(client: OpenAI, video_id: str):
    """Poll every 20 seconds until the video reaches a terminal state."""
    video = client.videos.retrieve(video_id)
    while video.status not in {"completed", "failed", "cancelled"}:
        print(f"Status: {video.status}. Waiting 20 seconds...")
        time.sleep(20)
        video = client.videos.retrieve(video_id)

    if video.status == "completed":
        print("Video successfully completed!")
    else:
        print(f"Video creation ended with status: {video.status}")
    return video


def download_video(client: OpenAI, video_id: str, output_filename: str = "output.mp4") -> None:
    print(f"Downloading video {video_id}...")
    content = client.videos.download_content(video_id, variant="video")
    content.write_to_file(output_filename)
    print(f"Video saved as {output_filename}")


def remix_video(client: OpenAI, video_id: str, prompt: str):
    print(f"Starting video remix for: {video_id}")
    video = client.videos.remix(video_id=video_id, prompt=prompt)
    print(f"Remix started. New video ID: {video.id}")
    print(f"Initial status: {video.status}")
    return poll_video_status(client, video.id)


def generate_video_from_image(
    client: OpenAI,
    model_deployment: str,
    image_path: str,
    prompt: str,
    size: str = "1280x720",
    seconds: str = "4",
):
    print(f"Starting video generation from image: {image_path}")
    with open(image_path, "rb") as reference_image:
        video = client.videos.create(
            model=model_deployment,
            prompt=prompt,
            size=size,
            seconds=seconds,
            input_reference=reference_image,
        )
    print(f"Video creation started. ID: {video.id}")
    print(f"Initial status: {video.status}")
    return poll_video_status(client, video.id)


def main() -> None:
    try:
        client, model_deployment = create_client()

        print("=== Video Generation Application ===\n")
        print("Step 1: Generating video from text prompt...")
        video = client.videos.create(
            model=model_deployment,
            prompt="A peaceful mountain lake at sunrise with mist rising from the water",
            size="1280x720",
            seconds="4",
        )
        video = poll_video_status(client, video.id)
        if video.status == "completed":
            download_video(client, video.id, "original_video.mp4")
            original_video_id = video.id

            print("\nStep 2: Remixing the video with a different style...")
            remixed = remix_video(
                client,
                original_video_id,
                "Use an inviting instrumental as the background music.",
            )
            if remixed.status == "completed":
                download_video(client, remixed.id, "remixed_video.mp4")

        print("\nStep 3: Generating a video from a reference image...")
        image_video = generate_video_from_image(
            client,
            model_deployment,
            "reference.png",
            "The scene comes to life with gentle movement and ambient lighting",
            size="1280x720",
            seconds="4",
        )
        if image_video.status == "completed":
            download_video(client, image_video.id, "image_based_video.mp4")
        print("\n=== Video generation complete ===")
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
