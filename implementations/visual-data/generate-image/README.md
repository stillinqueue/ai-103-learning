# Generate images with AI

## Exercise

**Generate images with AI**.

## Architecture

```text
text prompt -> image-generation model -> base64 image -> decoded PNG
```

## Core API

`azure-image-client.py` uses the Azure OpenAI-compatible `OpenAI` client, `client.images.generate(...)`, `MODEL_DEPLOYMENT`, the user prompt, and `n=1`. The recommended Microsoft model is `gpt-image-2`; availability and quota can vary.

The response contains generated image data as `b64_json`. The application decodes the base64 value into image bytes and writes sequential files such as `images/image_1.png`, `images/image_2.png`, and so on. No images are generated during this setup/verification work.

## Authentication and endpoint

The Azure implementation uses `DefaultAzureCredential` with `get_bearer_token_provider`. The endpoint is the Azure OpenAI `/openai/v1/` endpoint:

```text
https://<resource>.openai.azure.com/openai/v1/
```

This is not the Microsoft Foundry project endpoint. `ENDPOINT` and `MODEL_DEPLOYMENT` are validated before client creation, and `OPENAI_API_KEY` is not used.

## Files and behavior

- `microsoft-starter-image-client.py` preserves the Microsoft starter and helper/save pattern.
- `azure-image-client.py` completes the Azure image-generation and base64 decode/save flow.
- `mystery-fruit.jpeg`, `orange.jpeg`, and `mango.jpeg` are reference images in the preceding vision module; this module generates new images and does not require source images.
- `.env.example` contains placeholder configuration only.
- `requirements.txt` preserves the Microsoft dependencies.

Each prompt is an independent `images.generate(...)` request. The CLI loop does not preserve conversational image-edit history.

## Mental model

- Image generation is a prompt -> new synthetic image operation.
- Image generation is not image understanding.
- Module 1 analyzed an existing image; Module 2 creates a new image.
- `b64_json` is encoded image bytes, not text describing the image.
- Base64 decoding is required before writing a PNG file.
- Repeated CLI prompts do not imply conversational image-generation history.

## Verification

### Azure implementation

- `azure-image-client.py` passed syntax and import/API validation.
- `ENDPOINT` and `MODEL_DEPLOYMENT` validation occurs before client creation or an Azure request.
- The base64 decode/save helper was verified with synthetic local bytes; it creates `images/`, decodes bytes, and writes sequential PNG names.
- No real Azure image-generation request occurred.

### Local OpenAI practice

`openai-image-client.py` ran successfully with model `gpt-image-2`. The response returned `b64_json`, which decoded successfully to `openai-image.png`; the captured file was 2,735,574 bytes and 1329 x 1183 pixels. The generated PNG was removed after inspection as transient runtime output.

Local OpenAI image-generation success does not verify Azure OpenAI endpoint, authentication, or deployment runtime.

## Codespaces limitation

Azure CLI / Entra authentication is blocked by tenant security defaults. Security settings will not be weakened, and blocked authentication will not be repeatedly retried. The official Azure implementation is preserved as reference code, and no Azure runtime success is claimed unless an actual image-generation call succeeds. `openai-image-client.py` is local API practice, not Azure runtime verification.
