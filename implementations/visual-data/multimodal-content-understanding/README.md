# Extract information from multimodal content

## Exercise

**Extract information from multimodal content** with Azure Content Understanding.

This is primarily a Microsoft Foundry and Content Understanding Studio exercise. Exercise 01 has no Python starter; the separate `02-content-understanding-api` exercise is the SDK/client-programming lab and is intentionally not mixed into this module.

## Important difference from the previous module

The previous Content Understanding exercise focused on:

```text
image -> predefined analyzer -> Description + Tags
```

This exercise broadens the concept to documents, images, audio, and video, with emphasis on designing and testing custom schemas in Content Understanding Studio.

## Prebuilt and custom analyzers

The prebuilt **Read** analyzer extracts text-oriented content such as words, paragraphs, formulas, and barcodes. **Layout** adds tables, figures, document structure, hyperlinks, and annotations. Read/Layout are useful for general extraction but do not automatically provide domain-specific fields such as vendor names or caller actions.

A custom analyzer follows:

```text
sample content -> schema -> build analyzer -> test on new content -> structured fields
```

The schema defines the fields the application wants extracted, and the analyzer is a reusable implementation of that schema.

## Four modalities

- **Invoice document**: `invoiceanalyzer`; train/sample `invoice-1234.pdf`; test `invoice-1235.pdf`; Invoice template plus custom `TotalQuantity`.
- **Slide image**: `slideanalyzer`; train/sample `slide-1.jpg`; test `slide-2.jpg`; title, summary, chart count, quarterly revenue, and product-category percentages.
- **Voicemail audio**: `voicemailanalyzer`; train/sample `call-1.mp3`; test `call-2.mp3`; caller, summary, actions, callback number, and alternative contacts. Content Understanding can provide a transcription preview before schema extraction.
- **Meeting video**: `meetinganalyzer`; train/sample `meeting-1.mp4`; test `meeting-2.mp4`; summary, participant count/names, shared-slide descriptions, and assigned actions. Video analysis can use segments/shots plus transcript and visual information.

## Samples and schema references

The `samples/` directory contains the eight public Microsoft files. The `schemas/` JSON files are concise learning references only, not exported or deployed analyzer definitions:

- `invoice-schema-reference.json`
- `slide-schema-reference.json`
- `voicemail-schema-reference.json`
- `meeting-schema-reference.json`

## Resource-side requirements

The complete Microsoft exercise requires a Microsoft Foundry resource/project, Content Understanding Studio, Azure Blob Storage with a container such as `content-understanding`, required underlying models, a Content Understanding project, and built/published custom analyzers. The exercise notes auto-deployment of models including `GPT-4.1`, `GPT-4.1-mini`, and `text-embedding-3-large`. None are provisioned here.

## Mental model and limitation

- Prebuilt analyzer = fixed general extraction capability.
- Custom analyzer = schema tailored to business fields.
- Schema = contract describing desired structured output.
- Multimodal Content Understanding handles documents, images, audio, and video.
- Transcription is not full information extraction; OCR/layout extraction is not custom business-field extraction.
- Training/sample content is distinct from test content.
- Analyzer built is not the same as analyzer successfully tested.
- Studio results are not Python SDK runtime results.

Azure CLI / Entra authentication is blocked by tenant security defaults, so this Codespace cannot currently reproduce Foundry project creation, storage/container setup, Studio connections, analyzer creation/building, or real multimodal analysis. Security settings will not be weakened and authentication will not be repeatedly retried. No fake local LLM workaround is created, and no analyzer/runtime success is claimed.

## Verification

- All eight Microsoft sample files were preserved and read successfully: two invoice PDFs, two slide images, two voicemail MP3s, and two meeting MP4s.
- All four schema-reference JSON files parsed successfully and are explicitly marked as learning references, not analyzer exports.
- The analyzer lifecycle, sample/test relationships, Read/Layout/custom-analyzer distinction, modality notes, and resource-side requirements were cross-checked against the official exercise.
- No Azure analyzer was created, built, published, tested, or executed.
- No local workaround was created because a prompt-based imitation would not validate Content Understanding Studio, templates, schema configuration, build lifecycle, reusable analyzer semantics, or multimodal analyzer behavior.
- Exercise 01 remains Studio-focused; Exercise 02, `02-content-understanding-api`, is the separate programmatic SDK exercise.
