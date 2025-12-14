#!/usr/bin/env python3
"""
Generate scene images for locations using Nano Banana Pro.
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
OUTPUT_DIR = Path("docs/images/locations")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Rate limiting settings
MIN_CONCURRENT = 2
MAX_CONCURRENT = 10
INITIAL_CONCURRENT = 5

# Model configuration
PRO_MODEL_ID = "gemini-3-pro-image-preview"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class AdaptiveSemaphore:
    """Semaphore with adaptive concurrency based on rate limit responses."""

    def __init__(self, initial_value, min_value=2, max_value=20):
        self.value = initial_value
        self.min_value = min_value
        self.max_value = max_value
        self._semaphore = asyncio.Semaphore(initial_value)
        self._lock = asyncio.Lock()
        self._current_permits = initial_value

    async def acquire(self):
        await self._semaphore.acquire()

    def release(self):
        self._semaphore.release()

    async def increase_concurrency(self):
        async with self._lock:
            if self._current_permits < self.max_value:
                old = self._current_permits
                self._current_permits = min(self._current_permits + 1, self.max_value)
                self._semaphore.release()
                logger.info(f"⬆️  Increased concurrency: {old} → {self._current_permits}")

    async def decrease_concurrency(self):
        async with self._lock:
            if self._current_permits > self.min_value:
                old = self._current_permits
                self._current_permits = max(self._current_permits - 2, self.min_value)
                try:
                    for _ in range(2):
                        if self._current_permits < old:
                            self._semaphore.acquire_nowait()
                except:
                    pass
                logger.warning(f"⬇️  Decreased concurrency: {old} → {self._current_permits}")

    def get_current(self):
        return self._current_permits


# Global rate limiter
adaptive_semaphore = AdaptiveSemaphore(INITIAL_CONCURRENT, MIN_CONCURRENT, MAX_CONCURRENT)

# Stats tracking
stats = {
    'total': 0,
    'successful': 0,
    'skipped': 0,
    'failed': 0,
    'rate_limited': 0,
    'start_time': None
}


# Location scene prompts
LOCATIONS = {
    "everpeak_citadel_exterior": {
        "name": "Everpeak Citadel Exterior",
        "output": OUTPUT_DIR / "everpeak_citadel_exterior.png",
        "prompt": "Epic fantasy landscape establishing shot. Massive white stone mountain fortress of Everpeak Citadel built atop converging glowing ley lines, multiple crystalline towers reaching skyward, ancient high elven architecture, grand courtyards and winding staircases carved into snow-covered mountain, terrace gardens at impossible altitudes, winter setting with snow-capped peaks surrounding, festival decorations with ribbons lanterns and banners, magical lights visible, smoke from chimneys and forges, dramatic mountain vista, medieval high fantasy architecture. Bold painted illustration style, vibrant colors, cinematic composition."
    },
    "festival_marketplace": {
        "name": "Festival Marketplace",
        "output": OUTPUT_DIR / "festival_marketplace.png",
        "prompt": "Bustling medieval fantasy marketplace. Colorful vendor stalls with wooden awnings selling winter goods crafts and food, festival decorations everywhere with ribbons garlands and lanterns, crowds of diverse fantasy races (elves dwarves humans halflings dragonborn) in warm cloaks, winter setting with snow on cobblestone ground, warm lighting from lanterns and magical lights, festive busy atmosphere, medieval fantasy architecture in background. Bold painted illustration style, vibrant warm colors, lively scene composition."
    },
    "grand_courtyard": {
        "name": "Grand Courtyard",
        "output": OUTPUT_DIR / "grand_courtyard.png",
        "prompt": "Majestic fantasy citadel courtyard. Large open ceremonial space with white stone paving, elegant high elven architecture surrounding with soaring pillars and arches, crystalline towers visible above, winter festival decorations with banners and magical lights, snow dusting the ancient stone, space for large gatherings, medieval high fantasy design, regal and ceremonial atmosphere. Bold painted illustration style, cool elegant colors, grand architectural composition."
    },
    "the_grand_library": {
        "name": "The Grand Library",
        "output": OUTPUT_DIR / "the_grand_library.png",
        "prompt": "Grand fantasy library interior. Soaring vaulted ceilings with ornate columns, endless shelves of ancient tomes and scrolls stretching floor to ceiling, tall arched windows filtering golden light onto reading tables, floating magical lights providing illumination, wooden ladders on rails to reach high shelves, dust motes floating in light shafts, ancient manuscripts star-charts and arcane diagrams visible, quiet reverent scholarly atmosphere, high elven architecture with elegant carved wood and stone, medieval fantasy grand library. Bold painted illustration style, warm scholarly lighting, atmospheric depth."
    },
    "the_observatory": {
        "name": "The Observatory",
        "output": OUTPUT_DIR / "the_observatory.png",
        "prompt": "Intimate fantasy observatory chamber. Small domed room with glass ceiling showing starry night sky, ancient magical telescope at center made of brass and crystal, celestial maps and star charts on walls, high elven precision engineering, gentle starlight filtering through glass dome, intimate space for astronomical study, recently restored condition, medieval fantasy observatory design. Bold painted illustration style, cool celestial blues and silvers, mystical starlight atmosphere."
    },
    "courier_tunnels": {
        "name": "Courier Tunnels",
        "output": OUTPUT_DIR / "courier_tunnels.png",
        "prompt": "Mysterious underground passage. Rough-hewn stone tunnel carved through mountain, cramped winding maze-like corridor, walls covered in chalk runes and symbols in different colors, some runes glowing faintly with magical energy, dim cold blue magical lighting, spatial distortions visible in air, evidence of tampering with smudged runes, working courier infrastructure, medieval fantasy magical transportation network. Bold painted illustration style, cool blues and mystical glows, atmospheric underground depth."
    },
    "balcony_garden_café": {
        "name": "Balcony Garden Café",
        "output": OUTPUT_DIR / "balcony_garden_café.png",
        "prompt": "Magical garden oasis terrace. Impossible sunny warm terrace high in snow-covered mountains, lush flowering vines and exotic potted plants everywhere, herbs growing in garden beds, small rustic wooden café building, wooden tables and chairs with nature carvings, stone balcony railing overlooking snowy citadel below, sunlight streaming through leaves creating dappled shadows, rich magical soil, peaceful sanctuary atmosphere, medieval fantasy garden paradise, NO modern items. Bold painted illustration style, vibrant greens and warm natural tones, serene magical atmosphere."
    },
    "barths_forge": {
        "name": "Barth's Forge",
        "output": OUTPUT_DIR / "barths_forge.png",
        "prompt": "Busy fantasy blacksmith forge. Large brick forge with glowing red coals and flames, heavy metal anvil center stage, blacksmith tools (hammers tongs quenching barrel) arranged around, sparks flying from red-hot metal being worked, weapons and metalwork on display, workshop atmosphere with metal shavings and coal dust, winter festival setting visible outside but forge interior is intensely hot, medieval fantasy smithy design, industrious craftsman atmosphere. Bold painted illustration style, warm oranges and reds from forge fire, dramatic forge lighting."
    },
    "sled_race_course": {
        "name": "Sled Race Course",
        "output": OUTPUT_DIR / "sled_race_course.png",
        "prompt": "Exciting winter sports scene. Mountain slope starting line for sled race, dramatic view down the mountain showing winding sled course carved into snowy mountainside, multiple wooden sleds lined up at start, decorative flags and banners marking the course, snow-covered peaks and pine trees, white stone citadel visible in background above, clear winter day with brilliant blue sky, festive winter sports atmosphere, medieval fantasy winter festival setting. Bold painted illustration style, crisp whites and blues, dynamic composition with sense of height."
    },
    "the_elven_sanctum": {
        "name": "The Elven Sanctum",
        "output": OUTPUT_DIR / "the_elven_sanctum.png",
        "prompt": "Ancient mystical cavern sanctum. Massive underground chamber with enormous magical Orrery at center (rotating crystal spheres suspended lenses glowing runes intricate gears and metallic arms), carved stone pillars supporting vaulted ceiling covered in constellation maps and celestial charts, five alcoves housing True Lenses for elemental essences, magical energy crackling through air in emerald (nature) silver-blue (mechanistic) lavender (celestial) golden (harmony) and prismatic (displacement) colors, ruins and battle scars on walls and floor from ancient conflict, cathedral-like scale, ancient high elven architecture, reverent powerful atmosphere, medieval high fantasy sanctum. Bold painted illustration style, mystical multi-colored magical energy, epic scale composition."
    },
    "mountain_path": {
        "name": "Mountain Path",
        "output": OUTPUT_DIR / "mountain_path.png",
        "prompt": "Dramatic mountain trail approach. Steep winding path carved into snowy mountainside, snow-covered rocks and hardy pine trees, white stone citadel visible towering above in distance, cold windy winter mountain setting with dramatic lighting, sense of journey and approach, medieval fantasy mountain trail, remote and majestic atmosphere. Bold painted illustration style, cool whites and grays with dramatic sky, cinematic establishing shot composition."
    }
}


async def generate_image_async(name, prompt, output_path):
    """Generate a single location scene image with Nano Banana Pro."""

    # Skip if already exists
    if output_path.exists():
        logger.info(f"⏭️  Skipped {name} (already exists)")
        stats['skipped'] += 1
        return True

    # Retry logic with exponential backoff
    max_retries = 5
    base_delay = 2

    for attempt in range(max_retries):
        try:
            # Acquire rate limiting token
            await adaptive_semaphore.acquire()

            try:
                # Run sync API call in thread pool
                success = await asyncio.to_thread(
                    generate_image_sync,
                    prompt,
                    output_path,
                    name
                )

                if success:
                    stats['successful'] += 1

                    # Occasionally increase concurrency when things go well
                    if stats['successful'] % 3 == 0:
                        await adaptive_semaphore.increase_concurrency()

                    return True
                else:
                    stats['failed'] += 1
                    return False

            finally:
                adaptive_semaphore.release()

        except Exception as e:
            error_str = str(e)

            # Handle rate limiting
            if '429' in error_str or 'rate limit' in error_str.lower():
                stats['rate_limited'] += 1
                await adaptive_semaphore.decrease_concurrency()
                delay = base_delay * (2 ** attempt)
                logger.warning(f"⚠️  Rate limited {name}, retry {attempt+1}/{max_retries} in {delay}s")
                await asyncio.sleep(delay)
                continue

            # Handle 503 (service overload)
            elif '503' in error_str:
                delay = base_delay * (2 ** attempt)
                logger.warning(f"⚠️  Service overloaded {name}, retry {attempt+1}/{max_retries} in {delay}s")
                await asyncio.sleep(delay)
                continue

            # Other errors
            else:
                logger.error(f"✗ Error {name}: {e}")
                stats['failed'] += 1
                return False

    # Max retries exhausted
    logger.error(f"✗ Failed {name} after {max_retries} attempts")
    stats['failed'] += 1
    return False


def generate_image_sync(prompt, output_path, name):
    """Synchronous generation (called from thread pool)."""
    try:
        client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

        config = types.GenerateContentConfig(
            response_modalities=['Image'],
            image_config=types.ImageConfig(aspect_ratio='16:9')  # Widescreen for scenes
        )

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
        # Re-raise to be handled by retry logic
        raise


async def main():
    """Main generation pipeline."""
    logger.info("=" * 70)
    logger.info("NANO BANANA PRO LOCATION SCENE GENERATION")
    logger.info("=" * 70)
    logger.info(f"Model: {PRO_MODEL_ID}")
    logger.info(f"Locations: {len(LOCATIONS)}")
    logger.info(f"Initial concurrency: {INITIAL_CONCURRENT}")
    logger.info(f"Adaptive range: {MIN_CONCURRENT}-{MAX_CONCURRENT}")
    logger.info("=" * 70)

    stats['total'] = len(LOCATIONS)
    stats['start_time'] = time_module.time()

    # Build all generation tasks
    tasks = []

    logger.info("\n🏰 GENERATING LOCATION SCENES")
    for loc_id, loc_data in LOCATIONS.items():
        tasks.append(generate_image_async(loc_data['name'], loc_data['prompt'], loc_data['output']))

    # Run all generations in parallel
    logger.info(f"\n🚀 Starting parallel generation...")
    await asyncio.gather(*tasks)

    # Final stats
    elapsed = time_module.time() - stats['start_time']
    completed = stats['successful'] + stats['skipped']

    logger.info("\n" + "=" * 70)
    logger.info("✓ GENERATION COMPLETE")
    logger.info("=" * 70)
    logger.info(f"Time: {elapsed/60:.1f} minutes ({elapsed:.0f}s)")
    logger.info(f"Total: {completed}/{stats['total']} scenes")
    logger.info(f"  Generated: {stats['successful']}")
    logger.info(f"  Skipped: {stats['skipped']}")
    logger.info(f"  Failed: {stats['failed']}")
    logger.info(f"  Rate limited: {stats['rate_limited']}")
    logger.info("=" * 70)

    if stats['failed'] > 0:
        logger.warning(f"\n⚠️  {stats['failed']} scenes failed - you can re-run to retry")


if __name__ == "__main__":
    asyncio.run(main())
