# Generate video with Sora in Microsoft Foundry

## Exercise

**Generate video with Sora in Microsoft Foundry**.

## Architecture

```text
prompt/reference image -> Sora video job -> poll status -> download MP4
```

## APIs and asynchronous workflow

`azure-video-app.py` uses:

- `client.videos.create(...)` to start text-to-video or image-to-video jobs.
- `client.videos.retrieve(...)` to poll status.
- `client.videos.remix(...)` to create a new asynchronous job from an existing video plus new instructions.
- `client.videos.download_content(...)` to retrieve completed video content.

Video generation is a job: the initial response contains an ID/status and does not mean the video is immediately ready. The application polls every 20 seconds until `completed`, `failed`, or `cancelled`. Only completed jobs are downloaded. Expected outputs are `original_video.mp4`, `remixed_video.mp4`, and `image_based_video.mp4`; none were generated during setup.

## Text and reference-image generation

The text prompt is:

```text
A peaceful mountain lake at sunrise with mist rising from the water
```

The reference-image path uses `reference.png`, `input_reference`, `1280x720`, and 4 seconds with:

```text
The scene comes to life with gentle movement and ambient lighting
```

A remix creates a new video job from an existing generated video and the instruction:

```text
Use an inviting instrumental as the background music.
```

## Endpoint, model, and authentication

The Azure OpenAI endpoint is:

```text
https://<resource>.openai.azure.com/openai/v1/
```

This is not the Foundry project endpoint. The model deployment is `Sora-2`; availability and subscription access may vary, and registration may be required. Authentication uses `DefaultAzureCredential` with a bearer token provider for `https://cognitiveservices.azure.com/.default`.

## Responsible AI notes

Sora restrictions documented by the Microsoft exercise include:

- content must be suitable for audiences under 18
- copyrighted characters and copyrighted music may be rejected
- real people and public figures cannot be generated
- human-face reference images may be rejected
- input and output moderation/content filtering applies

These restrictions are not bypassed.

## Important distinction

- Module 1 understands an existing image.
- Module 2 generates a still image.
- Module 3 generates or remixes video asynchronously.
- Still-image generation was generally handled as a direct request in the previous module; video generation requires job creation, polling, and download.

## Files and limitation

- `microsoft-starter-video-app.py` preserves the Microsoft starter and TODOs.
- `azure-video-app.py` completes text-to-video, polling, download, remix, and reference-image video generation.
- `reference.png` is the Microsoft reference image.
- `.env.example` contains placeholders only.
- `requirements.txt` preserves the Microsoft dependencies.

Sora access can be restricted, video generation can take several minutes, and Azure CLI / Entra authentication is blocked in this Codespace. The official implementation is preserved as reference code; no Azure runtime success is claimed and no local workaround is created.

## Verification

### Azure implementation

- `azure-video-app.py` compiled successfully and the installed OpenAI SDK exposes `videos.create`, `retrieve`, `remix`, and `download_content`.
- Missing `OPENAI_BASE_URL` and `MODEL_DEPLOYMENT` fail before client creation or a remote request.
- `reference.png` exists, is readable, and is the Microsoft 1280 x 720 reference image.
- Local fake-job checks confirmed video IDs are retrieved, status is displayed, polling waits 20 seconds, terminal states stop polling, and downloads use `variant="video"`.
- No real Azure video job occurred and no MP4 was generated.

### Local runtime decision

No direct OpenAI video-generation test was performed. Video jobs can be slow/costly, and a direct OpenAI Sora result would not verify Azure Sora endpoint authentication, deployment access, or availability. Structural verification of the video job workflow does not prove Azure Sora runtime access or deployment availability.
