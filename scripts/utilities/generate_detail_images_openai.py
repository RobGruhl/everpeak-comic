#!/usr/bin/env python3
"""
Generate detailed images for characters, NPCs, and monsters using OpenAI
"""

import os
import json
import time
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import base64

# Load environment
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Output directories
CHAR_OUTPUT_DIR = Path("docs/images/characters")
NPC_OUTPUT_DIR = Path("docs/images/npcs")
MONSTER_OUTPUT_DIR = Path("docs/images/monsters")

# Create output directories
for dir_path in [CHAR_OUTPUT_DIR, NPC_OUTPUT_DIR, MONSTER_OUTPUT_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


def generate_image(prompt, output_path, size="1024x1024"):
    """Generate a single image using OpenAI."""
    print(f"  Generating... ", end='', flush=True)

    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        n=1,
        size=size,
        quality="high"
    )

    # Decode and save
    image_data = base64.b64decode(response.data[0].b64_json)
    with open(output_path, 'wb') as f:
        f.write(image_data)

    print(f"✓ Saved to {output_path}")
    time.sleep(1)  # Rate limiting


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

def main():
    """Generate all images."""
    print("Everpeak Detail Image Generation (OpenAI)")
    print("="*60)

    total_generated = 0
    total_skipped = 0

    # Generate characters
    print("\n📸 GENERATING CHARACTER PORTRAITS")
    print("-"*60)
    for char_id, char_data in CHARACTERS.items():
        print(f"\n[{char_data['name']}]")

        if char_data['output'].exists():
            print(f"  ⏭️  Already exists, skipping...")
            total_skipped += 1
            continue

        try:
            generate_image(char_data['prompt'], char_data['output'])
            total_generated += 1
        except Exception as e:
            print(f"  ✗ Error: {e}")

    # Generate NPCs
    print("\n\n👥 GENERATING NPC PORTRAITS")
    print("-"*60)
    for npc_id, npc_data in NPCS.items():
        print(f"\n[{npc_data['name']}]")

        if npc_data['output'].exists():
            print(f"  ⏭️  Already exists, skipping...")
            total_skipped += 1
            continue

        try:
            generate_image(npc_data['prompt'], npc_data['output'])
            total_generated += 1
        except Exception as e:
            print(f"  ✗ Error: {e}")

    # Generate monsters
    print("\n\n👹 GENERATING MONSTER/CREATURE IMAGES")
    print("-"*60)
    for monster_id, monster_data in MONSTERS.items():
        print(f"\n[{monster_data['name']}]")

        if monster_data['output'].exists():
            print(f"  ⏭️  Already exists, skipping...")
            total_skipped += 1
            continue

        try:
            generate_image(monster_data['prompt'], monster_data['output'])
            total_generated += 1
        except Exception as e:
            print(f"  ✗ Error: {e}")

    print("\n\n" + "="*60)
    print("Image generation complete!")
    print(f"Generated: {total_generated}")
    print(f"Skipped (already exist): {total_skipped}")
    print(f"Total: {total_generated + total_skipped}")

if __name__ == "__main__":
    main()
