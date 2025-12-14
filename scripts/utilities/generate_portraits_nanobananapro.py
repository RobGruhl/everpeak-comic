#!/usr/bin/env python3
"""
Generate detailed portrait images for characters, NPCs, and monsters using Nano Banana Pro.
Uses parallel generation with adaptive rate limiting.
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

# Output directories
CHAR_OUTPUT_DIR = Path("docs/images/characters")
NPC_OUTPUT_DIR = Path("docs/images/npcs")
MONSTER_OUTPUT_DIR = Path("docs/images/monsters")

# Create output directories
for dir_path in [CHAR_OUTPUT_DIR, NPC_OUTPUT_DIR, MONSTER_OUTPUT_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Rate limiting settings
MIN_CONCURRENT = 2
MAX_CONCURRENT = 10
INITIAL_CONCURRENT = 6

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


# Character prompts (main party)
CHARACTERS = {
    "val": {
        "name": "Val",
        "output": CHAR_OUTPUT_DIR / "val-portrait.png",
        "prompt": "Professional fantasy character portrait. Val, brass dragonborn monk, just under 7 feet tall, lean athletic build, warm brass-colored scales gleaming copper-bronze, gentle amber eyes, draconic head with backward-facing horns, wearing simple monk's robes in earth tones, courier's satchel, warm friendly smile, mountain monastery background. Bold ink linework, vibrant warm colors, detailed facial features, painted illustration quality."
    },
    "prismor": {
        "name": "Prismor",
        "output": CHAR_OUTPUT_DIR / "prismor-portrait.png",
        "prompt": "Professional fantasy character portrait. Prismor, blue crystal dragonborn paladin, 7+ feet tall, brilliant blue crystalline scales that shimmer and refract light, wise blue eyes, mature middle-aged, polished plate armor with blue-silver finish, holy symbol, shield, noble protective stance, citadel balcony background. Bold ink linework, cool blues and silvers with crystalline shimmer, regal composition, painted illustration quality."
    },
    "apocalypse_winter": {
        "name": "Apocalypse Winter",
        "output": CHAR_OUTPUT_DIR / "apocalypse-winter-portrait.png",
        "prompt": "Professional fantasy character portrait. Apocalypse Winter (Pocky), young human wizard in early 20s, slender scholarly build, pale skin, messy dark hair, round spectacles, wizard's robes in deep navy blue with silver star embroidery, holding ancient tome, ink-stained fingers, eager curious expression, Grand Library background. Bold ink linework, cool blues with arcane glow, scholarly atmosphere, painted illustration quality."
    },
    "lunara": {
        "name": "Lunara",
        "output": CHAR_OUTPUT_DIR / "lunara-portrait.png",
        "prompt": "Professional fantasy character portrait. Lunara, high elf druid, 6+ feet tall, graceful, long silver-white hair adorned with flowers and vines, bright green glowing eyes, ageless beauty, flowing robes of natural greens and browns, living vines and flowers woven into clothing, wooden staff, serene expression, touching a plant, Everpeak gardens background. Bold ink linework, vibrant greens and earth tones, ethereal druidic magic, painted illustration quality."
    },
    "malrik": {
        "name": "Malrik",
        "output": CHAR_OUTPUT_DIR / "malrik-portrait.png",
        "prompt": "Professional fantasy character portrait. Malrik, drow rogue and street performer, 5'9\" lean agile build, charcoal-dark skin, striking white hair in ponytail, sharp violet eyes, colorful performer's garb in purples reds and golds, dark leather armor hidden beneath, holding playing cards mid-trick, charming roguish grin, festival marketplace background. Bold ink linework, vibrant contrasting colors, theatrical lighting, painted illustration quality."
    }
}

# NPC prompts
NPCS = {
    "sorrel_halfling": {
        "name": "Sorrel (Halfling)",
        "output": NPC_OUTPUT_DIR / "sorrel-halfling-portrait.png",
        "prompt": "Professional fantasy character portrait. Sorrel disguised as halfling child, 3 feet tall, sandy-blond hair slightly messy, warm golden eyes with unusual wisdom, cherubic innocent face with knowing smile, subtle golden shimmer to skin, simple child's clothing with gold accents, enigmatic smile showing ancient wisdom, citadel courtyard background. Bold ink linework, warm golden undertones, subtle magical glow, painted illustration quality."
    },
    "sorrel_dragon": {
        "name": "Sorrel (Dragon)",
        "output": NPC_OUTPUT_DIR / "sorrel-dragon-portrait.png",
        "prompt": "Professional fantasy creature portrait. Sorrel true form, gold dragon wyrmling, small majestic dragon, brilliant golden scales shimmering like precious metal, cat-sized body, elegant wings, intelligent kind amber eyes, delicate horns and whiskers, regal bearing despite small size, noble protective stance, warm golden glow from scales, Elven Sanctum background bathed in golden light. Bold ink linework, brilliant golds and warm metallics, radiant lighting, painted illustration quality."
    },
    "marge": {
        "name": "Marge",
        "output": NPC_OUTPUT_DIR / "marge-portrait.png",
        "prompt": "Professional fantasy character portrait. Marge, head librarian, middle-aged human woman 40s-50s, gray-streaked brown hair in practical bun, intelligent brown eyes behind reading spectacles, kind but stern expression, practical librarian's robes in muted blues and grays, ink-stained sleeves, holding ancient tome, focused scholarly expression, Grand Library background with towering bookshelves. Bold ink linework, cool scholarly tones, atmospheric library lighting, painted illustration quality."
    },
    "barth": {
        "name": "Barth",
        "output": NPC_OUTPUT_DIR / "barth-portrait.png",
        "prompt": "Professional fantasy character portrait. Barth, drow blacksmith, muscular broad-shouldered male, dark charcoal skin with metallic sheen from forge work, white hair kept short, pale purple eyes, burn scars on arms, heavy leather blacksmith's apron, holding hammer, examining metalwork, serious focused expression, proud craftsman bearing, Dawnforge workshop background with glowing forge. Bold ink linework, warm forge colors with dramatic lighting, metallic details, painted illustration quality."
    },
    "marivielle": {
        "name": "Marivielle",
        "output": NPC_OUTPUT_DIR / "marivielle-portrait.png",
        "prompt": "Professional fantasy character portrait. Marivielle Greenbough, half-elf café owner, graceful woman 30s-40s, long auburn hair with green highlights, warm hazel-green eyes, delicate elvish features, friendly welcoming smile, practical café owner's attire in natural greens and browns, apron with leaf patterns, flower behind ear, holding teacup, warm hospitable expression, Balcony Garden Café background with lush plants. Bold ink linework, warm natural tones, inviting atmosphere, painted illustration quality."
    },
    "lord_alric": {
        "name": "Lord Alric",
        "output": NPC_OUTPUT_DIR / "lord-alric-portrait.png",
        "prompt": "Professional fantasy character portrait. Lord Alric, noble antagonist, middle-aged human male 40s, dark hair with gray at temples, cold calculating gray eyes, sharp aristocratic features, slight arrogant smirk, expensive noble's attire in deep crimsons and blacks, richly embroidered robes with arcane symbols, ceremonial rapier, magical staff, one hand gesturing dramatically, confident superior stance, slight magical aura, dark chamber with orrery background. Bold ink linework, dark rich colors with magical energy, villainous lighting, painted illustration quality."
    }
}

# Monster prompts
MONSTERS = {
    "verdant_mephit": {
        "name": "Verdant Mephit",
        "output": MONSTER_OUTPUT_DIR / "verdant-mephit.png",
        "prompt": "Professional fantasy creature design. Verdant Mephit nature elemental, small creature 2-3 feet tall, body composed of living vines leaves and thorny branches, glowing green firefly eyes, vine-like limbs writhing, moss and flowers growing on body, sharp thorns, wispy plant-like form, faint green magical glow, hostile territorial stance, vines extended menacingly, corrupted garden background. Bold ink linework, vibrant greens and natural tones, magical nature essence glow, painted illustration quality."
    },
    "gear_mephit": {
        "name": "Gear Mephit",
        "output": MONSTER_OUTPUT_DIR / "gear-mephit.png",
        "prompt": "Professional fantasy creature design. Gear Mephit mechanistic elemental, small mechanical creature 2-3 feet tall, body made of interlocking gears cogs and metal parts, glowing blue-white mechanical eyes, clockwork limbs with spinning components, bronze brass and iron construction, steam vents releasing pressure, constantly ticking and whirring, sharp metal edges and blades, aggressive mechanical precision, gears spinning menacingly, Dawnforge workshop background. Bold ink linework, metallic colors with glowing blue energy, mechanical details, painted illustration quality."
    },
    "starlight_mephit": {
        "name": "Starlight Mephit",
        "output": MONSTER_OUTPUT_DIR / "starlight-mephit.png",
        "prompt": "Professional fantasy creature design. Starlight Mephit celestial elemental, small celestial creature 2-3 feet tall, body composed of shimmering starlight and cosmic dust, multiple bright points of light like stars, semi-transparent ethereal form, glowing white-blue eyes, trails of stardust, constellation patterns visible in body, radiant aura, constantly shifting celestial patterns, sparkles and motes of light, hovering above ground, radiating intense light, Observatory chamber background. Bold ink linework, brilliant whites and blues with cosmic effects, ethereal glow, painted illustration quality."
    },
    "blink_mephit": {
        "name": "Blink Mephit",
        "output": MONSTER_OUTPUT_DIR / "blink-mephit.png",
        "prompt": "Professional fantasy creature design. Blink Mephit displacement elemental, small spatial creature 2-3 feet tall, constantly flickering in and out of visibility, semi-transparent with distortion effects, multiple overlapping silhouettes, purple-violet energy crackling, indistinct shifting form, reality warping around it, displacement aura creating afterimages, spatial rifts and tears, teleportation trail effects, appears in several places at once, mid-teleport blur, courier tunnels background. Bold ink linework, purples and violets with displacement effects, motion blur, painted illustration quality."
    },
    "melody_mephit": {
        "name": "Melody Mephit",
        "output": MONSTER_OUTPUT_DIR / "melody-mephit.png",
        "prompt": "Professional fantasy creature design. Melody Mephit harmony elemental, small sonic creature 2-3 feet tall, body composed of visible sound waves and musical notes, pastel colors pink lavender and cyan in wave patterns, musical notation symbols floating around, vibrating resonating form, glowing eyes pulsing with rhythm, harmonic rings emanating from body, translucent layers of sound waves, visible soundwave patterns, pulsing in rhythm, aggressive sonic stance, mid-shriek attack, Hall of Instruments background. Bold ink linework, pastel colors with sound wave visualizations, harmonic effects, painted illustration quality."
    }
}


async def generate_image_async(name, prompt, output_path):
    """Generate a single portrait image with Nano Banana Pro."""

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
                    if stats['successful'] % 5 == 0:
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
            image_config=types.ImageConfig(aspect_ratio='1:1')  # Square portraits
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
    logger.info("NANO BANANA PRO PORTRAIT GENERATION")
    logger.info("=" * 70)
    logger.info(f"Model: {PRO_MODEL_ID}")
    logger.info(f"Characters: {len(CHARACTERS)}")
    logger.info(f"NPCs: {len(NPCS)}")
    logger.info(f"Monsters: {len(MONSTERS)}")
    logger.info(f"Total: {len(CHARACTERS) + len(NPCS) + len(MONSTERS)} portraits")
    logger.info(f"Initial concurrency: {INITIAL_CONCURRENT}")
    logger.info(f"Adaptive range: {MIN_CONCURRENT}-{MAX_CONCURRENT}")
    logger.info("=" * 70)

    stats['total'] = len(CHARACTERS) + len(NPCS) + len(MONSTERS)
    stats['start_time'] = time_module.time()

    # Build all generation tasks
    tasks = []

    logger.info("\n📸 GENERATING CHARACTER PORTRAITS")
    for char_id, char_data in CHARACTERS.items():
        tasks.append(generate_image_async(char_data['name'], char_data['prompt'], char_data['output']))

    logger.info("\n👥 GENERATING NPC PORTRAITS")
    for npc_id, npc_data in NPCS.items():
        tasks.append(generate_image_async(npc_data['name'], npc_data['prompt'], npc_data['output']))

    logger.info("\n👹 GENERATING MONSTER/CREATURE IMAGES")
    for monster_id, monster_data in MONSTERS.items():
        tasks.append(generate_image_async(monster_data['name'], monster_data['prompt'], monster_data['output']))

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
    logger.info(f"Total: {completed}/{stats['total']} portraits")
    logger.info(f"  Generated: {stats['successful']}")
    logger.info(f"  Skipped: {stats['skipped']}")
    logger.info(f"  Failed: {stats['failed']}")
    logger.info(f"  Rate limited: {stats['rate_limited']}")
    logger.info("=" * 70)

    if stats['failed'] > 0:
        logger.warning(f"\n⚠️  {stats['failed']} portraits failed - you can re-run to retry")


if __name__ == "__main__":
    asyncio.run(main())
