#!/usr/bin/env python3
"""
Generate character reference image for Prismor.
This creates a detailed character portrait to use as a visual reference for consistency.
"""

import os
import base64
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
OUTPUT_DIR = Path("output/references")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_prismor_reference():
    """Generate a detailed character reference portrait of Prismor."""

    prompt = """Professional character reference sheet illustration for a fantasy comic book.

CHARACTER: Prismor - Blue Crystal Dragonborn Paladin

CRITICAL REQUIREMENTS:
- This is a DRAGONBORN character with a visible FACE and distinct facial features
- NOT a faceless crystal elemental or rock monster
- Must have clear dragonborn reptilian features with personality and expression

HEAD & FACE (MOST IMPORTANT):
- Dragonborn reptilian head with noble, dignified features
- Deep sapphire blue eyes that show wisdom and contemplation - EYES MUST BE VISIBLE
- Defined snout and jaw with dragonborn anatomy
- Capable of visible facial expressions
- Head covered in crystalline blue scales that have a gem-like translucent quality
- Scales catch and refract light with internal prismatic effects
- BUT maintains clear dragonborn facial structure - this is a person, not a crystal statue

BODY & SCALES:
- 7 feet tall, imposing presence
- Muscular, powerful warrior's physique
- Crystalline blue scales with hints of forest green throughout body
- Gem-like quality to scales but clearly organic dragonborn anatomy
- Scales have subtle light refraction but body maintains dragonborn form

ARMOR (EXTREMELY DETAILED):
- BASE: Silver/dull steel plate mail - realistic medieval fantasy metal armor
- Heavy plate armor covering chest, shoulders, arms with metallic shine
- VINE DECORATIONS: Forest green vines, leaves, and natural Oath of the Ancients motifs
- The green vines appear to be GROWING ON the silver armor but are PART OF the armor itself
- Vines have three-dimensional sculptural quality integrated into the metal
- Organic 3D relief patterns - realistic vine details that look like living plants but are crafted metal
- The vines are decorative elements OF the armor, not separate from it
- Silver/steel base metal visible between and beneath the green vine ornamentation
- Crystalline accents on armor that complement his blue-green scales
- Lots of fine detail work - professional craftsmanship showing nature magic and master smithing
- The overall effect: realistic metal armor decorated with incredibly detailed vine reliefs in green

CAPE:
- Forest green cape or cloak draped over shoulders
- Rich fabric with natural draping

OVERALL COMPOSITION:
- Three-quarter view or front-facing portrait showing full upper body and head
- Noble paladin bearing with protective, heroic presence
- Character reference sheet style - clear, well-lit, detailed
- Fantasy comic book art style with bold ink line work
- Vibrant colors with emphasis on blue-green crystalline scales and dark green armor
- Professional character design that could be used as art reference

STYLE: Bold ink line art, vibrant fantasy colors, high detail, comic book character design, heroic fantasy illustration, clear reference-quality rendering."""

    print("Generating Prismor character reference image...")
    print(f"Size: 1024x1536 (portrait orientation for full character view)")

    try:
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1536",
            quality="high",
            n=1
        )

        # Decode and save image
        image_data = base64.b64decode(response.data[0].b64_json)
        output_path = OUTPUT_DIR / "prismor-reference.png"

        with open(output_path, 'wb') as f:
            f.write(image_data)

        print(f"✓ Reference image saved to: {output_path}")
        print(f"\nThis reference image can be used for:")
        print(f"  - Visual consistency across all panels")
        print(f"  - Regenerating problem panels 25-3, 27-3, 45-1")
        print(f"  - Future panel generation featuring Prismor")

        return str(output_path)

    except Exception as e:
        print(f"✗ Error generating reference image: {e}")
        return None


if __name__ == "__main__":
    result = generate_prismor_reference()
    if result:
        print(f"\n✓ SUCCESS - Reference image ready at: {result}")
    else:
        print(f"\n✗ FAILED - Could not generate reference image")
