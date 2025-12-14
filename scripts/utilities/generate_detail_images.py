#!/usr/bin/env python3
"""
Generate detailed images for characters, NPCs, monsters, and locations
using the Nano Banana Pro technique from generate_nanobananapro.py
"""

import json
import sys
from pathlib import Path

# Add scripts/core to path to import generate_nanobananapro
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from generate_nanobananapro import generate_single_image, OUTPUT_DIR

# Output directories
CHAR_OUTPUT_DIR = Path("docs/images/characters")
NPC_OUTPUT_DIR = Path("docs/images/npcs")
MONSTER_OUTPUT_DIR = Path("docs/images/monsters")
LOCATION_OUTPUT_DIR = Path("docs/images/locations")

# Create output directories
for dir_path in [CHAR_OUTPUT_DIR, NPC_OUTPUT_DIR, MONSTER_OUTPUT_DIR, LOCATION_OUTPUT_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


# CHARACTER PORTRAITS (Main Party)
CHARACTERS = {
    "val": {
        "name": "Val",
        "output_file": CHAR_OUTPUT_DIR / "val-portrait.png",
        "prompt": """Professional character portrait illustration.

Character: Val - Brass Dragonborn Monk

Physical Appearance:
- Just under 7 feet tall with a lean, athletic build
- Warm brass-colored scales that gleam copper-bronze in light
- Gentle, expressive amber eyes that radiate kindness
- Draconic head with smooth brass scales and small backward-facing horns
- Strong but graceful physique from years of courier work

Clothing & Equipment:
- Simple monk's robes in earth tones (browns, ochre, cream)
- Lightweight traveling gear designed for mountain climbing
- Minimal armor, emphasizing mobility
- Courier's satchel with chalk symbols
- Prayer beads on wrist

Expression & Pose:
- Warm, friendly smile
- Confident but humble posture
- Eyes showing curiosity and determination
- Slight lean forward suggesting readiness to help

Setting: Mountain monastery background with snow-capped peaks

Art Style: Professional fantasy character portrait, bold ink linework, vibrant warm colors emphasizing brass dragon heritage, detailed facial features, painted illustration quality"""
    },

    "prismor": {
        "name": "Prismor",
        "output_file": CHAR_OUTPUT_DIR / "prismor-portrait.png",
        "prompt": """Professional character portrait illustration.

Character: Prismor - Blue Crystal Dragonborn Paladin

Physical Appearance:
- Tall, powerful build (7+ feet)
- Brilliant blue crystal-like scales that shimmer and refract light
- Wise, steady blue eyes
- Middle-aged for a dragonborn, mature and experienced
- Strong jaw and dignified bearing
- Crystalline scales create a shimmering, faceted appearance

Clothing & Equipment:
- Polished plate armor with blue-silver finish
- Holy symbol of ancient oath prominently displayed
- Well-maintained shield with crystalline embellishments
- Cape in deep blue with silver trim
- Longsword at side

Expression & Pose:
- Calm, protective stance
- One hand resting on shield
- Noble bearing, guardian's confidence
- Serene expression showing wisdom and dedication
- Slight metallic gleam to scales catching light

Setting: Citadel balcony overlooking mountains

Art Style: Professional fantasy character portrait, bold ink linework, cool blues and silvers with crystalline shimmer effects, regal composition, painted illustration quality"""
    },

    "apocalypse_winter": {
        "name": "Apocalypse Winter",
        "output_file": CHAR_OUTPUT_DIR / "apocalypse-winter-portrait.png",
        "prompt": """Professional character portrait illustration.

Character: Apocalypse Winter (Pocky) - Human Wizard

Physical Appearance:
- Young human in early twenties
- Slender, scholarly build
- Pale skin from spending time in libraries
- Messy dark hair often falling over eyes
- Intense, intelligent dark eyes behind round spectacles
- Ink stains on fingers from note-taking

Clothing & Equipment:
- Wizard's robes in deep navy blue with silver star embroidery
- Multiple pockets and pouches for spell components
- Leather-bound spellbook tucked under arm
- Arcane focus pendant (crystal)
- Slightly disheveled from constant research
- Warm winter cloak over robes

Expression & Pose:
- Curious, eager expression
- Holding an ancient tome or scroll
- One finger raised as if making a point
- Excited energy about discovering knowledge
- Ink-stained hands visible

Setting: Grand Library interior with books and scrolls

Art Style: Professional fantasy character portrait, bold ink linework, cool blues and silvers with arcane glow effects, scholarly atmosphere, painted illustration quality"""
    },

    "lunara": {
        "name": "Lunara",
        "output_file": CHAR_OUTPUT_DIR / "lunara-portrait.png",
        "prompt": """Professional character portrait illustration.

Character: Lunara - High Elf Druid

Physical Appearance:
- Tall, graceful high elf (6+ feet)
- Ageless beauty with ancient wisdom in eyes
- Long silver-white hair often adorned with flowers and vines
- Bright green eyes that seem to glow with nature magic
- Delicate elven features with pointed ears
- Pale skin with slight green undertones from nature connection

Clothing & Equipment:
- Flowing robes of natural greens, browns, and earth tones
- Living vines and flowers woven into clothing and hair
- Wooden staff carved with nature symbols
- Druidic focus (seed pendant from Marivielle)
- Barefoot or simple leather sandals
- Natural jewelry (flowers, leaves, wooden beads)

Expression & Pose:
- Serene, peaceful expression
- Gentle smile
- One hand touching a living plant
- Connection with nature evident in posture
- Graceful, fluid stance

Setting: Everpeak gardens with lush greenery and magical plants

Art Style: Professional fantasy character portrait, bold ink linework, vibrant greens and natural earth tones, ethereal druidic magic effects, painted illustration quality"""
    },

    "malrik": {
        "name": "Malrik",
        "output_file": CHAR_OUTPUT_DIR / "malrik-portrait.png",
        "prompt": """Professional character portrait illustration.

Character: Malrik - Drow Rogue and Street Performer

Physical Appearance:
- Lean, agile drow build (about 5'9")
- Distinctive charcoal-dark skin
- Striking white hair pulled back in a ponytail
- Sharp violet eyes, always observing
- Angular, handsome features
- Graceful, performer's movements

Clothing & Equipment:
- Colorful street performer's garb (purples, reds, golds)
- Dark leather armor hidden beneath flashy clothing
- Multiple daggers concealed in various places
- Playing cards visible in hand or pocket
- Acrobat's gear (light, flexible clothing)
- Subtle makeup enhancing theatrical appearance

Expression & Pose:
- Charming, roguish grin
- One eyebrow raised playfully
- Holding playing cards mid-trick
- Confident, theatrical stance
- Eyes showing both mischief and watchfulness

Setting: Festival marketplace with colorful stalls

Art Style: Professional fantasy character portrait, bold ink linework, vibrant contrasting colors, theatrical lighting, painted illustration quality"""
    }
}

# NPCS
NPCS = {
    "sorrel_halfling": {
        "name": "Sorrel (Halfling Form)",
        "output_file": NPC_OUTPUT_DIR / "sorrel-halfling-portrait.png",
        "prompt": """Professional character portrait illustration.

Character: Sorrel - Gold Dragon Wyrmling in Halfling Disguise

Physical Appearance (Halfling Form):
- Appears as a young halfling child (about 3 feet tall)
- Sandy-blond to light brown hair, slightly messy
- Warm golden eyes with unusual wisdom for a child
- Cherubic, innocent face with subtle knowing smile
- Slight golden shimmer to skin in certain light
- Small, well-proportioned halfling build

Clothing:
- Simple but clean child's clothing
- Earth tones with subtle gold accents
- Comfortable, practical attire
- Small cloak or jacket
- Bare feet (halfling tradition)

Expression & Pose:
- Enigmatic smile, knowing more than appears
- Kind, protective posture
- Eyes showing ancient wisdom despite young appearance
- Slight magical aura (very subtle gold shimmer)
- Watchful but non-threatening

Setting: Citadel courtyard, observing from a distance

Art Style: Professional fantasy character portrait, bold ink linework, warm golden undertones, subtle magical glow, painted illustration quality"""
    },

    "sorrel_dragon": {
        "name": "Sorrel (Dragon Form)",
        "output_file": NPC_OUTPUT_DIR / "sorrel-dragon-portrait.png",
        "prompt": """Professional creature portrait illustration.

Character: Sorrel - Gold Dragon Wyrmling (True Form)

Physical Appearance:
- Small but majestic gold dragon wyrmling
- Brilliant golden scales that shimmer like precious metal
- Cat-sized body with elegant proportions
- Wings folded gracefully against sides
- Intelligent, kind amber eyes
- Delicate horns and whiskers
- Long serpentine neck
- Tail curled around body

Details:
- Each scale catches light individually
- Regal bearing despite small size
- Wise, ancient presence in young form
- Warm golden glow emanating from scales
- Benevolent expression

Expression & Pose:
- Noble, protective stance
- Head held high with dignity
- Wings partially spread showing golden membrane
- Kind, knowing gaze
- Emanating warmth and wisdom

Setting: Elven Sanctum, bathed in golden light

Art Style: Professional fantasy creature portrait, bold ink linework, brilliant golds and warm metallics, radiant lighting, painted illustration quality"""
    },

    "marge": {
        "name": "Marge",
        "output_file": NPC_OUTPUT_DIR / "marge-portrait.png",
        "prompt": """Professional character portrait illustration.

Character: Marge - Head Librarian (Human)

Physical Appearance:
- Middle-aged human woman (40s-50s)
- Kind but stern librarian bearing
- Gray-streaked brown hair in practical bun
- Intelligent brown eyes behind reading spectacles
- Weathered but kind face showing years of study
- Slightly hunched from years of reading
- Ink stains on fingers

Clothing:
- Practical librarian's robes in muted blues and grays
- Many pockets for notes and bookmarks
- Reading spectacles on chain around neck
- Comfortable but professional attire
- Ink-stained sleeves from cataloging
- Small holy symbol or scholarly medallion

Expression & Pose:
- Intelligent, focused expression
- Holding ancient tome or scroll
- Slight frown of concentration
- One hand raised to adjust spectacles
- Scholarly posture

Setting: Grand Library with towering bookshelves

Art Style: Professional fantasy character portrait, bold ink linework, cool scholarly tones, atmospheric library lighting, painted illustration quality"""
    },

    "barth": {
        "name": "Barth",
        "output_file": NPC_OUTPUT_DIR / "barth-portrait.png",
        "prompt": """Professional character portrait illustration.

Character: Barth - Drow Blacksmith

Physical Appearance:
- Muscular, broad-shouldered drow male
- Dark charcoal skin with slight metallic sheen from forge work
- White hair kept short and practical
- Pale purple eyes showing focus and skill
- Burn scars on arms from blacksmithing
- Strong, calloused hands
- Tall (6 feet), powerful build

Clothing & Equipment:
- Heavy leather blacksmith's apron over simple clothes
- Soot and metal filings on clothing
- Tool belt with hammers and tongs
- Protective arm wraps
- Simple but well-made boots
- Mechanistic Essence symbols on apron

Expression & Pose:
- Serious, focused expression
- Holding a hammer or examining metalwork
- Proud craftsman's bearing
- Slight concern in eyes (missing frozen iron)
- Competent, trustworthy demeanor

Setting: Dawnforge workshop with glowing forge

Art Style: Professional fantasy character portrait, bold ink linework, warm forge colors with dramatic lighting, metallic details, painted illustration quality"""
    },

    "marivielle": {
        "name": "Marivielle Greenbough",
        "output_file": NPC_OUTPUT_DIR / "marivielle-portrait.png",
        "prompt": """Professional character portrait illustration.

Character: Marivielle Greenbough - Café Owner (Half-Elf)

Physical Appearance:
- Graceful half-elf woman in her 30s-40s
- Long auburn hair with green highlights
- Warm hazel-green eyes
- Delicate elvish features mixed with human warmth
- Friendly, welcoming smile
- Slightly pointed ears

Clothing:
- Practical café owner's attire in natural greens and browns
- Apron decorated with leaf and vine patterns
- Comfortable but elegant clothing
- Nature-inspired jewelry (wooden, floral)
- Flower tucked behind ear
- Well-worn but clean working clothes

Expression & Pose:
- Warm, hospitable smile
- Holding a teacup or serving tray
- Welcoming gesture
- Kind but observant eyes
- Graceful, nurturing presence

Setting: Balcony Garden Café with lush plants and sunshine

Art Style: Professional fantasy character portrait, bold ink linework, warm natural tones, inviting atmosphere, painted illustration quality"""
    },

    "lord_alric": {
        "name": "Lord Alric",
        "output_file": NPC_OUTPUT_DIR / "lord-alric-portrait.png",
        "prompt": """Professional character portrait illustration.

Character: Lord Alric - Noble Antagonist (Human)

Physical Appearance:
- Middle-aged human noble (40s)
- Well-groomed but sinister appearance
- Dark hair with gray at temples
- Cold, calculating gray eyes
- Sharp, aristocratic features
- Slight smirk showing arrogance
- Tall, commanding presence

Clothing & Equipment:
- Expensive noble's attire in deep crimsons and blacks
- Richly embroidered robes with arcane symbols
- Gold and silver jewelry showing wealth
- Ceremonial rapier at side
- Mechanist's staff (magical focus)
- Fine cloak with crimson symbol

Expression & Pose:
- Arrogant, scheming expression
- One hand gesturing dramatically
- Confident, superior stance
- Eyes showing ambition and manipulation
- Slight magical aura of power

Setting: Dark chamber with orrery in background

Art Style: Professional fantasy character portrait, bold ink linework, dark rich colors with magical energy effects, villainous lighting, painted illustration quality"""
    }
}

# MONSTERS/CREATURES
MONSTERS = {
    "verdant_mephit": {
        "name": "Verdant Mephit",
        "output_file": MONSTER_OUTPUT_DIR / "verdant-mephit.png",
        "prompt": """Professional creature illustration.

Creature: Verdant Mephit (Nature Essence Elemental)

Physical Appearance:
- Small elemental creature (2-3 feet tall)
- Body composed of living vines, leaves, and thorny branches
- Glowing green eyes like fireflies
- Vine-like limbs that writhe and grasp
- Moss and small flowers growing on body
- Thorn-covered hands and feet
- Wispy, plant-like form
- Green magical aura

Features:
- Animated, predatory plant appearance
- Sharp thorns protruding from vines
- Constantly shifting, growing form
- Leaves rustling with movement
- Faint green glow from within
- Small but aggressive demeanor

Expression & Pose:
- Hostile, territorial stance
- Vines extended menacingly
- Thorns prominent and sharp
- Feral, protective of nature

Setting: Corrupted garden area

Art Style: Professional fantasy creature design, bold ink linework, vibrant greens and natural tones, magical nature essence glow, painted illustration quality"""
    },

    "gear_mephit": {
        "name": "Gear Mephit",
        "output_file": MONSTER_OUTPUT_DIR / "gear-mephit.png",
        "prompt": """Professional creature illustration.

Creature: Gear Mephit (Mechanistic Essence Elemental)

Physical Appearance:
- Small mechanical creature (2-3 feet tall)
- Body made of interlocking gears, cogs, and metal parts
- Glowing blue-white mechanical eyes
- Clockwork limbs with spinning components
- Bronze, brass, and iron construction
- Steam vents releasing pressure
- Constantly ticking and whirring
- Sharp metal edges and blades

Features:
- Complex gear mechanisms visible
- Small furnace or energy core glowing inside
- Articulated metal joints
- Tool-like appendages (wrenches, blades)
- Frozen iron components
- Rhythmic mechanical movement

Expression & Pose:
- Aggressive, mechanical precision
- Gears spinning menacingly
- Steam hissing from vents
- Blade appendages extended

Setting: Dawnforge workshop

Art Style: Professional fantasy creature design, bold ink linework, metallic colors with glowing blue energy, mechanical details, painted illustration quality"""
    },

    "starlight_mephit": {
        "name": "Starlight Mephit",
        "output_file": MONSTER_OUTPUT_DIR / "starlight-mephit.png",
        "prompt": """Professional creature illustration.

Creature: Starlight Mephit (Celestial Essence Elemental)

Physical Appearance:
- Small celestial creature (2-3 feet tall)
- Body composed of shimmering starlight and cosmic dust
- Multiple points of bright light like stars
- Semi-transparent, ethereal form
- Glowing white-blue eyes
- Trails of stardust following movement
- Constellation patterns visible in body
- Radiant aura

Features:
- Constantly shifting celestial patterns
- Sparkles and motes of light
- Nebula-like wisps of color
- Star-field visible through translucent form
- Radiating gentle but blinding light
- Floating, weightless movement

Expression & Pose:
- Otherworldly, alien demeanor
- Hovering above ground
- Radiating light intensely
- Star-patterns shifting

Setting: Observatory chamber with open sky

Art Style: Professional fantasy creature design, bold ink linework, brilliant whites and blues with cosmic effects, ethereal glow, painted illustration quality"""
    },

    "blink_mephit": {
        "name": "Blink Mephit",
        "output_file": MONSTER_OUTPUT_DIR / "blink-mephit.png",
        "prompt": """Professional creature illustration.

Creature: Blink Mephit (Displacement Essence Elemental)

Physical Appearance:
- Small spatial creature (2-3 feet tall)
- Constantly flickering in and out of visibility
- Semi-transparent with distortion effects
- Multiple overlapping silhouettes
- Purple-violet energy crackling
- Indistinct, shifting form
- Reality seems to warp around it
- Eyes appear in multiple places simultaneously

Features:
- Displacement aura creating afterimages
- Spatial rifts and tears around body
- Teleportation trail effects
- Unstable, phasing appearance
- Hard to focus on directly
- Multiple simultaneous positions

Expression & Pose:
- Disorienting, unpredictable stance
- Mid-teleport blur effect
- Spatial distortion visible
- Appears in several places at once

Setting: Courier tunnels with spatial distortion

Art Style: Professional fantasy creature design, bold ink linework, purples and violets with displacement effects, motion blur and multiple exposures, painted illustration quality"""
    },

    "melody_mephit": {
        "name": "Melody Mephit",
        "output_file": MONSTER_OUTPUT_DIR / "melody-mephit.png",
        "prompt": """Professional creature illustration.

Creature: Melody Mephit (Harmony Essence Elemental)

Physical Appearance:
- Small sonic creature (2-3 feet tall)
- Body composed of visible sound waves and musical notes
- Pastel colors (pink, lavender, cyan) in wave patterns
- Musical notation symbols floating around
- Vibrating, resonating form
- Glowing eyes that pulse with rhythm
- Harmonic rings emanating from body
- Translucent layers of sound waves

Features:
- Visible soundwave patterns
- Musical notes and symbols orbiting
- Pulsing in rhythm
- Color-coded frequency bands
- Resonance effects
- Harmonic aura affecting surroundings

Expression & Pose:
- Aggressive sonic stance
- Sound waves emanating forcefully
- Vibrating with discordant energy
- Mid-shriek attack

Setting: Hall of Instruments

Art Style: Professional fantasy creature design, bold ink linework, pastel colors with sound wave visualizations, harmonic effects, painted illustration quality"""
    }
}

def main():
    """Generate all detail images."""
    print("Everpeak Detail Image Generation")
    print("="*60)

    # Generate character portraits
    print("\n📸 GENERATING CHARACTER PORTRAITS")
    print("-"*60)
    for char_id, char_data in CHARACTERS.items():
        print(f"\n[{char_data['name']}]")
        print(f"Output: {char_data['output_file']}")

        if char_data['output_file'].exists():
            print(f"⏭️  Already exists, skipping...")
            continue

        try:
            generate_single_image(
                prompt=char_data['prompt'],
                output_path=char_data['output_file'],
                size="1024x1024"
            )
            print(f"✓ Generated successfully")
        except Exception as e:
            print(f"✗ Error: {e}")

    # Generate NPC portraits
    print("\n\n👥 GENERATING NPC PORTRAITS")
    print("-"*60)
    for npc_id, npc_data in NPCS.items():
        print(f"\n[{npc_data['name']}]")
        print(f"Output: {npc_data['output_file']}")

        if npc_data['output_file'].exists():
            print(f"⏭️  Already exists, skipping...")
            continue

        try:
            generate_single_image(
                prompt=npc_data['prompt'],
                output_path=npc_data['output_file'],
                size="1024x1024"
            )
            print(f"✓ Generated successfully")
        except Exception as e:
            print(f"✗ Error: {e}")

    # Generate monster images
    print("\n\n👹 GENERATING MONSTER/CREATURE IMAGES")
    print("-"*60)
    for monster_id, monster_data in MONSTERS.items():
        print(f"\n[{monster_data['name']}]")
        print(f"Output: {monster_data['output_file']}")

        if monster_data['output_file'].exists():
            print(f"⏭️  Already exists, skipping...")
            continue

        try:
            generate_single_image(
                prompt=monster_data['prompt'],
                output_path=monster_data['output_file'],
                size="1024x1024"
            )
            print(f"✓ Generated successfully")
        except Exception as e:
            print(f"✗ Error: {e}")

    print("\n\n" + "="*60)
    print("Image generation complete!")
    print(f"Characters: {len(CHARACTERS)}")
    print(f"NPCs: {len(NPCS)}")
    print(f"Monsters: {len(MONSTERS)}")

if __name__ == "__main__":
    main()
