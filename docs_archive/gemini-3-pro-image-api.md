# Gemini 3 Pro Image API Documentation

**Model ID:** `gemini-3-pro-image-preview`
**Status:** Preview (requires billing)
**Last Updated:** 2025-01-25

## Overview

Gemini 3 Pro Image (aka "Nano Banana Pro") is Google's advanced text-to-image generation model with:
- **Thinking mode** - Shows reasoning process before generating
- **4K resolution** - Up to 4K image generation
- **Google Search grounding** - Real-time data integration
- **Multi-turn editing** - Conversational refinement workflow
- **Sharp text rendering** - Legible text and diagrams in images

## Billing Requirements

⚠️ **No free tier** - Requires Google Cloud billing enabled

**Pricing:**
- Text input: $2/1M tokens
- Image output: $0.134 (1K/2K) or $0.24 (4K)
- Batch API: 50% discount (24h processing delay)

## Supported Aspect Ratios

```
1:1   (square)
2:3   (portrait, ideal for comic panels)
3:2   (landscape)
3:4   (portrait)
4:3   (landscape)
4:5   (portrait)
5:4   (landscape)
9:16  (vertical)
16:9  (widescreen)
21:9  (ultra-wide)
```

## Resolution Options

- `"1K"` - Default, fastest
- `"2K"` - Higher detail
- `"4K"` - Maximum quality

⚠️ **Case sensitive** - Must use uppercase K

## Python Setup

### Installation

```bash
pip install google-genai python-dotenv pillow
```

### API Key

Get from [Google AI Studio](https://aistudio.google.com/) with billing enabled.

```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
```

## Basic Usage

### Simple Text-to-Image

```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_API_KEY")
PRO_MODEL_ID = "gemini-3-pro-image-preview"

response = client.models.generate_content(
    model=PRO_MODEL_ID,
    contents="A photorealistic siamese cat with green left eye and blue right eye",
    config=types.GenerateContentConfig(
        response_modalities=['Image'],  # or ['Text', 'Image']
        image_config=types.ImageConfig(
            aspect_ratio="1:1"
        )
    )
)

# Save the image
for part in response.parts:
    if image := part.as_image():
        image.save("output.png")
        print("✓ Image saved")
```

### With 4K Resolution

```python
response = client.models.generate_content(
    model=PRO_MODEL_ID,
    contents="A detailed fantasy landscape",
    config=types.GenerateContentConfig(
        response_modalities=['Image'],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",
            image_size="4K"  # Must be uppercase
        )
    )
)
```

### With Thinking Mode

```python
response = client.models.generate_content(
    model=PRO_MODEL_ID,
    contents="Create a viral social media post about coffee",
    config=types.GenerateContentConfig(
        response_modalities=['Text', 'Image'],
        image_config=types.ImageConfig(aspect_ratio="1:1"),
        thinking_config=types.ThinkingConfig(
            include_thoughts=True
        )
    )
)

# View the model's reasoning
for part in response.parts:
    if part.thought:
        print(f"💭 Thought: {part.text}")
    elif image := part.as_image():
        image.save("viral.png")
```

### With Google Search Grounding

```python
response = client.models.generate_content(
    model=PRO_MODEL_ID,
    contents="Current weather forecast for Tokyo as a modern chart",
    config=types.GenerateContentConfig(
        response_modalities=['Image'],
        image_config=types.ImageConfig(aspect_ratio="16:9"),
        tools=[{"google_search": {}}]  # Enable real-time data
    )
)

for part in response.parts:
    if image := part.as_image():
        image.save("weather.png")

# Display sources
if response.candidates[0].grounding_metadata:
    print(response.candidates[0].grounding_metadata.search_entry_point.rendered_content)
```

## Multi-turn Editing

```python
# Initial generation
response = client.models.generate_content(
    model=PRO_MODEL_ID,
    contents="A red sports car",
    config=types.GenerateContentConfig(
        response_modalities=['Text', 'Image'],
        image_config=types.ImageConfig(aspect_ratio="16:9")
    )
)

# Save image and signatures
for part in response.parts:
    if image := part.as_image():
        image.save("car_v1.png")

# Edit - MUST include all previous response parts
edit_response = client.models.generate_content(
    model=PRO_MODEL_ID,
    contents=[
        response.candidates[0].content,  # Include original response
        "Change the car to blue and add mountains in background"
    ],
    config=types.GenerateContentConfig(
        response_modalities=['Text', 'Image'],
        image_config=types.ImageConfig(aspect_ratio="16:9")
    )
)
```

⚠️ **Critical:** Must return all thought signatures to avoid errors during edits.

## Batch Processing (50% Cost Savings)

For bulk generation with 24h processing window:

```python
# Batch API reduces costs by 50%
# Ideal for generating many panels overnight
# Documentation: Contact Google Cloud for batch access
```

## Error Handling

### Common Errors

**503 Service Unavailable:**
```
{'error': {'code': 503, 'message': 'The model is overloaded. Please try again later.'}}
```
→ Model is experiencing high demand, retry after delay

**400 Bad Request:**
```
{'error': {'code': 400, 'message': 'Invalid aspect ratio'}}
```
→ Check aspect ratio format (e.g., "16:9" not "16x9")

**401/403 Authentication:**
```
{'error': {'code': 401, 'message': 'API key not valid'}}
```
→ Check API key and billing status

**429 Rate Limit:**
```
{'error': {'code': 429, 'message': 'Resource exhausted'}}
```
→ Implement exponential backoff

### Retry Pattern

```python
import time
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(5)
)
def generate_with_retry(prompt, aspect_ratio="1:1"):
    try:
        response = client.models.generate_content(
            model=PRO_MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['Image'],
                image_config=types.ImageConfig(aspect_ratio=aspect_ratio)
            )
        )
        return response
    except Exception as e:
        if "503" in str(e):
            print("Model overloaded, retrying...")
            raise  # Will trigger retry
        elif "429" in str(e):
            print("Rate limited, backing off...")
            raise
        else:
            print(f"Error: {e}")
            return None
```

## Rate Limits

- Preview models typically have stricter rate limits
- Implement exponential backoff for 429 errors
- Consider batch API for bulk operations

## Best Practices

1. **Start with 1K resolution** for testing, use 4K for final output
2. **Use thinking mode** for complex creative prompts
3. **Enable Google Search** for factual/current information
4. **Specify aspect ratio** matching your target format
5. **Implement retry logic** for 503 errors (model overload)
6. **Cache generated images** - regeneration costs the same
7. **Use batch API** for cost savings on bulk generation

## Comparison: Nano Banana Pro vs OpenAI

| Feature | Gemini 3 Pro Image | OpenAI gpt-image-1 |
|---------|-------------------|-------------------|
| **Max Resolution** | 4K | 1792px |
| **Aspect Ratios** | 10 options | 3 (1:1, 16:9, 9:16) |
| **Thinking Mode** | ✓ (visible reasoning) | ✗ |
| **Search Grounding** | ✓ (real-time data) | ✗ |
| **Cost (1K)** | $0.134 | ~$0.04 |
| **Cost (4K)** | $0.24 | N/A |
| **Free Tier** | ✗ (billing required) | ✗ |
| **Multi-turn Edit** | ✓ (conversational) | ✗ |
| **Text in Images** | Excellent | Good |

## Use Cases for Comic Generation

**Advantages:**
- 2:3 aspect ratio perfect for comic panels
- 4K for high-quality print
- Search grounding for accurate historical/factual references
- Thinking mode for complex scene composition

**Considerations:**
- 3x more expensive than OpenAI for standard resolution
- Preview status = potential deprecation with 2 weeks notice
- 503 errors during high demand periods
- Requires Google Cloud billing setup

## Comic Panel Example

```python
# Generate comic panel with character consistency
comic_prompt = '''
Professional comic book panel illustration.

Character: Val, a brass dragonborn monk. Tall (7ft), lean athletic build,
warm brass scales with subtle copper undertones, ember-glow orange eyes.
Wearing simple brown monastery robes with chalk dust stains.

Scene: Walking through a crowded festival marketplace in a fantasy citadel.
Festival vendors setting up colorful stalls in background. Winter morning,
snow on distant peaks.

Style: Bold ink line art, vibrant colors, dynamic composition, high detail.
'''

response = client.models.generate_content(
    model=PRO_MODEL_ID,
    contents=comic_prompt,
    config=types.GenerateContentConfig(
        response_modalities=['Image'],
        image_config=types.ImageConfig(
            aspect_ratio="2:3",  # Perfect for comic panels
            image_size="2K"      # Good quality without 4K cost
        ),
        thinking_config=types.ThinkingConfig(
            include_thoughts=True  # See how model interprets prompt
        )
    )
)

for part in response.parts:
    if part.thought:
        print(f"Model reasoning: {part.text}")
    elif image := part.as_image():
        image.save("panel_val.png")
        print("✓ Panel generated at 2:3 aspect ratio")
```

## Troubleshooting

**Model always returns 503:**
- Check [Google Cloud Status](https://status.cloud.google.com/)
- Try during off-peak hours
- Use batch API for non-urgent generation

**Billing errors:**
- Verify billing enabled in Google Cloud Console
- Check quota limits in AI Platform
- Ensure Vertex AI API is enabled

**Poor image quality:**
- Increase resolution (1K → 2K → 4K)
- Be more specific in prompts
- Use thinking mode for complex scenes

## References

- [Gemini 3 Developer Guide](https://ai.google.dev/gemini-api/docs/gemini-3)
- [Image Generation Docs](https://ai.google.dev/gemini-api/docs/image-generation)
- [Nano Banana Pro Tutorial](https://dev.to/googleai/introducing-nano-banana-pro-complete-developer-tutorial-5fc8)
- [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Google Cloud Vertex AI](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-pro-image)
