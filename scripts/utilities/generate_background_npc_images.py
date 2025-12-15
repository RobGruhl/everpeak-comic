#!/usr/bin/env python3
"""
Generate images for background NPCs using Nano Banana Pro.
"""

import os
import asyncio
import logging
import time as time_module
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image

# Load environment
load_dotenv()

# Output directory
OUTPUT_DIR = Path("docs/images/npcs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Model configuration
PRO_MODEL_ID = "gemini-3-pro-image-preview"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Background NPC prompts
BACKGROUND_NPCS = {
    "fantasy_crowd": {
        "name": "Fantasy Crowd",
        "output": OUTPUT_DIR / "fantasy-crowd.png",
        "prompt": "Professional fantasy character group illustration. Diverse fantasy crowd of various races gathering in medieval marketplace, mixture of elves dwarves humans halflings dragonborn, wearing medieval fantasy winter clothing and warm cloaks, variety of ages and builds, merchants adventurers townsfolk, busy marketplace atmosphere, winter festival setting with decorations, warm friendly atmosphere, no single focal character, group scene showing diversity of fantasy races. Bold ink linework, vibrant warm colors, crowd composition, painted illustration quality."
    },
    "festival_crowd": {
        "name": "Festival Crowd",
        "output": OUTPUT_DIR / "festival-crowd.png",
        "prompt": "Professional fantasy crowd scene. Large festive gathering of diverse fantasy races celebrating winter festival, elves dwarves humans halflings in colorful winter attire, festival decorations ribbons and lanterns, people laughing talking celebrating, medieval fantasy marketplace setting with stalls, warm magical lighting, joyful festive atmosphere, mixture of ages and social classes, no single focal point, crowd enjoying winter celebration. Bold ink linework, vibrant festive colors, dynamic group composition, painted illustration quality."
    },
    "halfling_courier": {
        "name": "Halfling Courier",
        "output": OUTPUT_DIR / "halfling-courier.png",
        "prompt": "Professional fantasy character portrait. Halfling courier, 3-4 feet tall, stocky energetic build, cheerful expression, bright eyes, practical short hair, wearing sturdy boots and layered coat with many pockets, courier's satchel with messages, ready to dash off stance, weight shifting from foot to foot, bright scarf or bandana, friendly energetic demeanor, Everpeak courier tunnels background. Bold ink linework, warm cheerful colors, dynamic pose, painted illustration quality."
    },
    "gambler": {
        "name": "Gambler",
        "output": OUTPUT_DIR / "gambler.png",
        "prompt": "Professional fantasy character portrait. Well-dressed gambler at festival, human male in fine but practical clothes, clever calculating eyes, charming smile with hint of mischief, fashionable hat or cloak, holding playing cards, rings on fingers, confident relaxed posture, sly knowing expression, festival marketplace background with gaming tables, medieval fantasy attire with style, subtle wealthy details. Bold ink linework, rich colors with hints of red and gold, charismatic pose, painted illustration quality."
    },
    "race_contestants": {
        "name": "Race Contestants",
        "output": OUTPUT_DIR / "race-contestants.png",
        "prompt": "Professional fantasy character group illustration. Sled race contestants preparing for winter competition, diverse fantasy races (humans elves dwarves), athletic builds, competitive eager expressions, winter sports gear and warm clothing, standing near wooden sleds at starting line, excitement and determination visible, snow-covered mountain slope background, festival atmosphere with flags and spectators, dynamic group composition showing camaraderie and competition. Bold ink linework, cool winter colors with bright accents, energetic group scene, painted illustration quality."
    }
}


async def generate_image_async(name, prompt, output_path):
    """Generate a single NPC image with Nano Banana Pro."""

    # Skip if already exists
    if output_path.exists():
        logger.info(f"⏭️  Skipped {name} (already exists)")
        return True

    try:
        client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

        config = types.GenerateContentConfig(
            response_modalities=['Image'],
            image_config=types.ImageConfig(aspect_ratio='1:1')  # Square portraits
        )

        logger.info(f"🎨 Generating {name}...")
        response = client.models.generate_content(
            model=PRO_MODEL_ID,
            contents=prompt,
            config=config
        )

        # Save image
        for part in response.parts:
            if image := part.as_image():
                image.save(str(output_path))
                # Re-open with PIL to get size
                pil_img = Image.open(str(output_path))
                size = pil_img.size
                logger.info(f"✓ Generated {name} ({size[0]}x{size[1]})")
                return True

        logger.error(f"✗ No image in response for {name}")
        return False

    except Exception as e:
        logger.error(f"✗ Error {name}: {e}")
        return False


async def main():
    """Main generation pipeline."""
    logger.info("=" * 70)
    logger.info("BACKGROUND NPC IMAGE GENERATION")
    logger.info("=" * 70)
    logger.info(f"Model: {PRO_MODEL_ID}")
    logger.info(f"NPCs: {len(BACKGROUND_NPCS)}")
    logger.info("=" * 70)

    start_time = time_module.time()
    successful = 0
    skipped = 0
    failed = 0

    # Generate sequentially to avoid rate limiting
    for npc_id, npc_data in BACKGROUND_NPCS.items():
        result = await generate_image_async(npc_data['name'], npc_data['prompt'], npc_data['output'])
        if result:
            if npc_data['output'].exists():
                if npc_data['output'].stat().st_mtime > start_time:
                    successful += 1
                else:
                    skipped += 1
        else:
            failed += 1

        # Small delay between requests
        await asyncio.sleep(2)

    elapsed = time_module.time() - start_time

    logger.info("\n" + "=" * 70)
    logger.info("✓ GENERATION COMPLETE")
    logger.info("=" * 70)
    logger.info(f"Time: {elapsed/60:.1f} minutes ({elapsed:.0f}s)")
    logger.info(f"Total: {successful + skipped}/{len(BACKGROUND_NPCS)} images")
    logger.info(f"  Generated: {successful}")
    logger.info(f"  Skipped: {skipped}")
    logger.info(f"  Failed: {failed}")
    logger.info("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
