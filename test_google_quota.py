#!/usr/bin/env python3
"""
Test Google Gemini 3 Pro Image API quota and access.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure API
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("❌ ERROR: GOOGLE_API_KEY not found in .env file")
    sys.exit(1)

print("=" * 70)
print("GOOGLE GEMINI API QUOTA TEST")
print("=" * 70)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Test configuration
model_name = 'gemini-3-pro-image-preview'
test_prompt = """Professional comic book panel illustration.

Location: Medieval fantasy tavern with wooden tables and stone walls.

Characters:
- A human warrior in plate armor, sitting at a table.

Scene: Warrior drinking from a tankard, relaxed atmosphere.

Style: Bold ink line art, vibrant colors, dynamic composition. Medieval fantasy setting."""

print(f"Model: {model_name}")
print(f"Test: Generating single test image...")
print()

try:
    # Attempt generation
    print("→ Calling Gemini API...")

    # Create client and config (matching generate_nanobananapro.py)
    client = genai.Client(api_key=api_key)

    config = types.GenerateContentConfig(
        response_modalities=['Image'],
        image_config=types.ImageConfig(aspect_ratio='2:3')
    )

    response = client.models.generate_content(
        model=model_name,
        contents=test_prompt,
        config=config
    )

    # If we get here, the API call succeeded
    print("✓ SUCCESS: API call completed")
    print()

    # Check response
    if hasattr(response, 'candidates') and response.candidates:
        candidate = response.candidates[0]
        if hasattr(candidate, 'content') and candidate.content.parts:
            image_data = candidate.content.parts[0].inline_data.data
            print(f"✓ Image generated: {len(image_data)} bytes")

            # Save test image
            test_file = Path("output/quota_test.png")
            test_file.parent.mkdir(parents=True, exist_ok=True)
            test_file.write_bytes(image_data)
            print(f"✓ Saved to: {test_file}")
    else:
        print("⚠️  Response received but no image data found")
        print(f"Response: {response}")

    print()
    print("=" * 70)
    print("✓ QUOTA TEST PASSED")
    print("=" * 70)
    print()
    print("The API is accessible and generating images successfully.")
    print("You should be able to retry generating the missing panels:")
    print()
    print("  python generate_nanobananapro.py 38-39 --concurrent 1")
    print("  python generate_nanobananapro.py 43-45 --concurrent 2")
    print()

except Exception as e:
    error_str = str(e)

    print("✗ FAILED: API call failed")
    print()
    print(f"Error: {error_str}")
    print()

    # Analyze error
    if '429' in error_str:
        print("=" * 70)
        print("⚠️  RATE LIMIT ERROR (429)")
        print("=" * 70)
        print()
        print("The API is still rate limiting requests.")
        print()
        print("Possible causes:")
        print("  1. Daily quota not yet reset (resets at midnight Pacific Time)")
        print("  2. Per-minute rate limit still active (wait 1 hour)")
        print("  3. Free tier quota exhausted")
        print()
        print("Actions:")
        print("  • Check quota status: https://aistudio.google.com/app/apikey")
        print("  • Review billing: https://console.cloud.google.com/billing")
        print("  • Consider upgrading to paid tier if needed")
        print("  • Wait and retry in a few hours")

    elif '403' in error_str:
        print("=" * 70)
        print("❌ PERMISSION ERROR (403)")
        print("=" * 70)
        print()
        print("API key may not have access to this model.")
        print()
        print("Actions:")
        print("  • Verify API key has Gemini API enabled")
        print("  • Check if model requires paid tier")
        print("  • Review project settings: https://console.cloud.google.com")

    elif 'quota' in error_str.lower():
        print("=" * 70)
        print("❌ QUOTA EXCEEDED")
        print("=" * 70)
        print()
        print("API quota has been exceeded.")
        print()
        print("Actions:")
        print("  • Check quota limits: https://console.cloud.google.com/iam-admin/quotas")
        print("  • Wait for quota reset (usually 24 hours)")
        print("  • Upgrade to paid tier for higher limits")

    else:
        print("=" * 70)
        print("❌ UNKNOWN ERROR")
        print("=" * 70)
        print()
        print("An unexpected error occurred.")
        print()
        print("Actions:")
        print("  • Check API key is valid")
        print("  • Verify internet connection")
        print("  • Review Google Cloud Console for service status")

    print()
    sys.exit(1)
