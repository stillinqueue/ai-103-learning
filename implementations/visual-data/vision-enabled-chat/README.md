# Develop a vision-enabled chat app

## Exercise

**Develop a vision-enabled chat app**.

## Core concept

A multimodal generative model can reason over text and image input in the same request.

## Image input approaches

`azure-image-chat-app.py` demonstrates both transport methods:

1. **Remote URL**: sends the Microsoft `orange.jpeg` URL as `input_image`.
2. **Local image**: reads `mystery-fruit.jpeg`, encodes it as base64, and sends a `data:image/jpeg;base64,...` URL as `input_image`.

The grocery-store developer instruction is preserved for both requests. The Responses API uses `client.responses.create(...)` with `input_text` and `input_image`, then displays `response.output_text`.

## Authentication and endpoint

The Azure implementation uses `DefaultAzureCredential` and `get_bearer_token_provider(...)` to supply an Entra token to `OpenAI`. The Microsoft lab expects the Azure OpenAI endpoint in this form:

```text
https://<resource>.openai.azure.com/openai/v1/
```

This is an Azure OpenAI endpoint, not a Microsoft Foundry project endpoint. `ENDPOINT` and `MODEL_DEPLOYMENT` are validated before client creation. The exercise suggests `gpt-5.2`, with compatible alternatives such as `gpt-5.2-mini` or `gpt-4o` when quota or regional availability requires it.

## Files

- `microsoft-starter-image-chat-app.py` preserves the Microsoft starter and TODOs.
- `azure-image-chat-app.py` is the completed official Azure multimodal client pattern.
- `mystery-fruit.jpeg`, `orange.jpeg`, and `mango.jpeg` are Microsoft reference images.
- `.env.example` contains placeholder configuration only.
- `requirements.txt` preserves the Microsoft dependencies.

## Stateless behavior

Each `responses.create(...)` call is independent. The CLI loop does not automatically create conversation history because no `previous_response_id` or prior message history is supplied.

## Important mental model

- A multimodal model accepts multiple modalities in one model request.
- Image understanding here is performed by a generative multimodal model, not a specialized classic computer-vision SDK operation.
- Attaching an image does not create conversation history.
- URL and base64 data URL are two transport methods for image input.

## Codespaces limitation

Azure CLI / Entra authentication is blocked by tenant security defaults. Security settings will not be weakened, and blocked authentication will not be repeatedly retried. The official Azure implementation is preserved as reference code, and no Azure runtime success is claimed unless a real request succeeds. `openai-image-chat-app.py` is a separate local practice implementation and is not Azure runtime verification.

## Verification

### Azure implementation

- `azure-image-chat-app.py` compiled successfully and required Azure/OpenAI imports loaded.
- The installed Responses API exposes the `create(...)` parameters used by the implementation.
- Missing `ENDPOINT` and `MODEL_DEPLOYMENT` fail before client creation or a remote request.
- The remote URL payload contains `input_text` and `input_image` with the Microsoft `orange.jpeg` URL.
- The local payload reads `mystery-fruit.jpeg` in binary mode, base64-encodes it, and uses a `data:image/jpeg;base64,` image URL.
- No Azure multimodal request occurred.

### Local OpenAI practice

`openai-image-chat-app.py` ran successfully with `gpt-4o-mini` for both image-input modes. The captured URL-image response identified the image as an orange. The captured local/base64-image response identified the mystery fruit as dragon fruit, also known as pitaya. Both responses were non-empty.

Local OpenAI multimodal success does not verify Azure OpenAI endpoint, authentication, or deployment runtime.
