# Gemini Image Generation API (Python)

> Local developer reference for using Google's Gemini API for image generation, editing, and style transfer via `google-genai`.

---

## Overview

Gemini can generate and process images conversationally. You can prompt Gemini with text, images, or both — allowing you to create, edit, and iterate on visuals programmatically.

### Capabilities
- **Text-to-Image** – Generate images from descriptive text.
- **Image + Text-to-Image (Editing)** – Modify or enhance images using text prompts.
- **Multi-Image Composition** – Combine multiple images into a single coherent scene.
- **Style Transfer** – Render existing content in new artistic styles.
- **Iterative Refinement** – Generate, review, and refine images conversationally.
- **High-Fidelity Text Rendering** – Generate legible and well-placed text (logos, diagrams, etc.).

All generated images include a [SynthID watermark](https://ai.google.dev/responsible/docs/safeguards/synthid).

---

## 1. Text-to-Image

Generate a high-quality image from a descriptive text prompt.

```python
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

client = genai.Client()

prompt = "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme"

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[prompt],
)

for part in response.candidates[0].content.parts:
    if part.inline_data is not None:
        image = Image.open(BytesIO(part.inline_data.data))
        image.save("generated_image.png")
