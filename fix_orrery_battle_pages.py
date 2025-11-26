#!/usr/bin/env python3
"""
Fix pages 22-39 with correct locations:
- Pages 22-23: Sorrel transformation (citadel interior)
- Pages 24-39: Orrery battle (Elven Sanctum)
"""

import json
from pathlib import Path

# Location descriptions
CITADEL_INTERIOR = """Location: Everpeak Citadel interior corridors - white stone hallways with high vaulted ceilings. Ancient high elven architecture with elegant arches and carved pillars. Magical lanterns providing warm light. Winter decorations (festival ribbons, banners). Spacious wide corridors. Medieval fantasy castle interior with high elven craftsmanship."""

ELVEN_SANCTUM = """Location: The Elven Sanctum - hidden cavern deep beneath Everpeak Citadel. Massive central chamber with the Orrery at center - enormous magical device with rotating crystal spheres, suspended lenses, glowing runes, intricate clicking gears and metallic arms. Ancient high elven architecture with carved stone pillars, vaulted ceiling covered in constellation maps and celestial charts. Five alcoves housing the True Lenses for elemental essences. Magical energy crackling through air - emerald (nature), silver-blue (mechanistic), lavender (celestial), golden (harmony), shifting prisms (displacement). Sense of ancient power and sacrifice. Ruins and scars from century-old battle visible on walls and floor. Cathedral-like scale with reverent atmosphere. Medieval high fantasy sanctum with high elven precision engineering."""

# Sorrel dragon description
SORREL_DRAGON = """Sorrel (Dragon Form): Small gold dragon wyrmling, about the size of a large dog, compact but majestic. Brilliant metallic gold scales that shimmer in any light, catching and reflecting magical glow. Ancient wise amber eyes, glowing with draconic intelligence and centuries of knowledge. Delicate but powerful wings spread wide - golden membranes. Reptilian features with noble bearing. Small horns curving back from head. Claws and talons visible. Young dragon but radiating power and authority. Beautiful and terrible simultaneously. Guardian of good."""

FANTASY_STYLE = "medieval fantasy setting, high fantasy atmosphere"

def fix_page_22():
    """Fix page 22 - Party reconvening, Sorrel transformation."""
    page_file = Path("pages/page-022.json")
    with open(page_file, 'r') as f:
        page = json.load(f)

    # Panel 1: Party reconvening in citadel
    page['panels'][0]['prompt'] = f"""Professional comic book panel illustration.

{CITADEL_INTERIOR}

Characters:
- Prismor: Blue crystal dragonborn paladin, 7 feet tall, imposing presence, muscular powerful build, crystalline blue-green scales, deep sapphire eyes, noble bearing, plate armor with nature symbols, greatsword on back, forest green cape
- Malrik: Drow rogue, 5'6", slim agile build, dark gray-blue drow skin, white short hair, pale lavender eyes, sharp features, dark leather armor, colorful street performer's vest
- Lunara: High elf druid, 5'8", graceful athletic build, long flowing chestnut hair with flowers, vibrant green eyes, fair skin, pointed ears, practical druid robes in earthy greens and browns, living vines in clothing, wooden staff
- Apocalypse Winter / Pocky: Human wizard, young man in early 20s, 5'10", strong scholarly build, dark unkempt hair, keen blue eyes, pale skin, deep blue wizard robes with silver trim, leather satchel with scrolls, component pouch, ink-stained fingers, reading glasses

Scene: Party reconvening in citadel corridor after their separate investigations. All four main characters gathered together urgently sharing discoveries. Pocky excited about fake lenses. Malrik reporting evidence from observatory. Prismor showing crimson emblem. Lunara describing vision from plants. Animated discussion, gesturing, urgent body language. Realization dawning that conspiracy is real and immediate. Winter citadel setting with magical light.

Dialogue: Pocky: "They have the True Lenses!" Malrik: "And the frozen iron!" Prismor: "They're going to corrupt the Dawn's Crown alignment!" Lunara: "We have to stop them!"

Include speech bubbles with the dialogue text clearly readable.

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {FANTASY_STYLE}."""

    # Panel 2: Sorrel appearing
    page['panels'][1]['npcs'] = {}  # Remove from npcs if present
    page['panels'][1]['characters']['Sorrel'] = SORREL_DRAGON.replace("Sorrel (Dragon Form): ", "")

    # But this is BEFORE transformation, so use halfling form
    page['panels'][1]['prompt'] = f"""Professional comic book panel illustration.

{CITADEL_INTERIOR}

Characters:
- Sorrel (Halfling Disguise - about to transform): Halfling child appearance, 3'2" tall, chubby build, messy sandy-brown hair, oversized scarf and mittens, worn leather satchel, cheerful demeanor BUT eyes showing ancient wisdom - amber eyes with depth and knowledge beyond years, mysterious knowing smile, standing before party with magical aura beginning to glow around them

Scene: Sorrel appearing before the party in citadel corridor. Halfling form but beginning to glow with golden magical energy. Party turning to see them. Sorrel's expression serious and wise despite childlike appearance. Faint shimmer of transformation magic starting. Mysterious and momentous. Citadel corridor with magical lanterns.

Dialogue: Sorrel: "You've done well to piece it together. But you'll need help for what comes next."

Include speech bubble with dialogue text clearly readable.

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {FANTASY_STYLE}, magical transformation energy beginning."""

    # Panel 3: Sorrel beginning to glow
    page['panels'][2]['characters']['Sorrel'] = SORREL_DRAGON.replace("Sorrel (Dragon Form): ", "")
    page['panels'][2]['prompt'] = f"""Professional comic book panel illustration.

{CITADEL_INTERIOR}

Characters:
- Sorrel (Mid-Transformation): Halfling form surrounded by brilliant golden magical light, body beginning to shift and grow, shimmer effect, silhouette changing, draconic features starting to emerge through light, wings unfurling, transformation in progress
- Party members visible in background stepping back in shock and awe

Scene: Sorrel glowing with intense golden magical energy, transformation magic enveloping them. Halfling form shifting into dragon wyrmling. Party members recoiling in surprise, shielding eyes from bright light, expressions of shock. Golden light filling corridor. Magical transformation visualization - body outlined in gold, wings spreading, growing larger. Dramatic reveal moment. Citadel corridor bathed in golden glow.

Sound Effects: Large bold "SHIMMMMMER" showing magical transformation sound.

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {FANTASY_STYLE}, dramatic magical transformation effects."""

    # Panel 4: Sorrel transformed into dragon
    page['panels'][3]['characters']['Sorrel'] = SORREL_DRAGON.replace("Sorrel (Dragon Form): ", "")
    page['panels'][3]['prompt'] = f"""Professional comic book panel illustration.

{CITADEL_INTERIOR}

Characters:
- {SORREL_DRAGON}
- Party members visible in background, shocked expressions, awe and wonder

Scene: Sorrel fully transformed into gold dragon wyrmling form. Wings spread magnificently filling frame. Golden light radiating from scales. Standing proudly in citadel corridor - beautiful and powerful. Party members in background with expressions of shock, awe, some backing away, some stepping forward in wonder. Golden light filling entire corridor from dragon's presence. Dramatic full reveal. Transformation complete. Ancient draconic majesty contrasted with corridor's elven architecture.

Sound Effects: Large bold "WHOOOOOOSH" showing dragon wings spreading and magical energy release.

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {FANTASY_STYLE}, dramatic draconic reveal with golden light effects."""

    with open(page_file, 'w') as f:
        json.dump(page, f, indent=2)
    print("✓ Fixed page 22")

def fix_page_23():
    """Fix page 23 - Party reaction, Sorrel speaks, call to action."""
    page_file = Path("pages/page-023.json")
    with open(page_file, 'r') as f:
        page = json.load(f)

    # Panel 1: Party's shocked reactions
    page['panels'][0]['prompt'] = f"""Professional comic book panel illustration.

{CITADEL_INTERIOR}

Characters:
- Val: Brass dragonborn monk, just under 7 feet, lean athletic build, warm brass/copper-bronze scales, ember-glow orange eyes WIDE with shock, kind reptilian face showing disbelief, earth-tone monastery robes with chalk dust, bare clawed feet, prayer beads on wrist, jaw dropped expression
- Malrik: Drow rogue, 5'6", slim agile build, dark gray-blue drow skin, white short hair, pale lavender eyes showing shock, sharp features with eyebrows raised, dark leather armor, colorful vest, defensive stance
- Lunara: High elf druid, 5'8", graceful athletic build, long flowing chestnut hair with flowers, vibrant green eyes showing recognition and awe, fair skin, pointed ears, practical druid robes in earthy greens and browns, living vines in clothing, wooden staff, hand to chest in reverence

Scene: Party's shocked reactions to Sorrel's dragon reveal. Three characters showing different expressions - Val's comedic shock, Malrik's suspicious vindication, Lunara's reverent recognition. Citadel corridor still glowing with residual golden light from transformation. Sorrel visible in background (dragon form). Reaction panel capturing character personalities through their responses. Medieval fantasy setting.

Dialogue: Val: "The halfling kid was a DRAGON?!" Malrik: "I knew something was off!" Lunara: "A gold dragon... guardian of good."

Include speech bubbles with dialogue text clearly readable.

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {FANTASY_STYLE}."""

    # Panel 2: Sorrel speaking
    page['panels'][1]['characters']['Sorrel'] = SORREL_DRAGON.replace("Sorrel (Dragon Form): ", "")
    page['panels'][1]['characters'].pop('Lord Alric', None)  # Remove Alric, he's not here yet

    page['panels'][1]['prompt'] = f"""Professional comic book panel illustration.

{CITADEL_INTERIOR}

Characters:
- {SORREL_DRAGON}

Scene: Close-up of Sorrel in dragon form, speaking with ancient wisdom and authority. Amber eyes glowing with intelligence. Noble draconic features. Wings partially spread. Golden scales catching magical light from corridor lanterns. Speaking seriously, explaining the threat. Ancient guardian revealing truth. Citadel corridor background with elven architecture. Majestic and powerful presence.

Dialogue: Sorrel: "I have watched you all. You have proven worthy. Lord Alric seeks to corrupt the Orrery for his own power."

Include speech bubble with dialogue text clearly readable.

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {FANTASY_STYLE}."""

    # Panel 3: Close on Sorrel's wise eyes
    page['panels'][2]['characters']['Sorrel'] = SORREL_DRAGON.replace("Sorrel (Dragon Form): ", "")
    page['panels'][2]['prompt'] = f"""Professional comic book panel illustration.

{CITADEL_INTERIOR}

Characters:
- {SORREL_DRAGON}

Scene: Extreme close-up on Sorrel's wise amber dragon eyes. Ancient wisdom and centuries of knowledge visible in glowing amber irises. Dragon's reptilian eye with slit pupil, glowing softly. Surrounding golden scales. Reflection of party visible in dragon's eye. Speaking the challenge and question. Emotional weight of high elven sacrifice. Close intimate shot showing depth of wisdom. Citadel corridor softly out of focus in background.

Dialogue: Sorrel: "The high elves sacrificed everything to protect this place. Will you do the same?"

Include speech bubble with dialogue text clearly readable.

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {FANTASY_STYLE}, detailed eye illustration."""

    # Panel 4: Party standing together
    page['panels'][3]['characters'] = {
        "Prismor": "Blue crystal dragonborn paladin, 7 feet tall, imposing presence, muscular powerful build, crystalline blue-green scales, deep sapphire eyes determined, noble bearing, plate armor with nature symbols, greatsword DRAWN and raised, forest green cape billowing",
        "Malrik": "Drow rogue, 5'6\", slim agile build, dark gray-blue drow skin, white short hair, pale lavender eyes fierce, sharp features determined, dark leather armor, colorful vest, daggers drawn",
        "Lunara": "High elf druid, 5'8\", graceful athletic build, long flowing chestnut hair with flowers, vibrant green eyes glowing with magic readying, fair skin, pointed ears, practical druid robes in earthy greens and browns, living vines in clothing glowing, wooden staff raised with green magic swirling",
        "Apocalypse Winter": "Human wizard, young man in early 20s, 5'10\", strong scholarly build, dark unkempt hair, keen blue eyes determined, pale skin, deep blue wizard robes with silver trim, leather satchel, component pouch open, hands glowing with arcane blue magic readying spell",
        "Val": "Brass dragonborn monk, just under 7 feet, lean athletic build, warm brass/copper-bronze scales, ember-glow orange eyes fierce, kind reptilian face now serious, earth-tone monastery robes, bare clawed feet in fighting stance, prayer beads glowing, fists wreathed in ki energy"
    }

    page['panels'][3]['prompt'] = f"""Professional comic book panel illustration.

{CITADEL_INTERIOR}

Characters:
- Prismor: Blue crystal dragonborn paladin, 7 feet tall, imposing presence, muscular powerful build, crystalline blue-green scales, deep sapphire eyes determined, noble bearing, plate armor with nature symbols, greatsword DRAWN and raised, forest green cape billowing
- Malrik: Drow rogue, 5'6", slim agile build, dark gray-blue drow skin, white short hair, pale lavender eyes fierce, sharp features determined, dark leather armor, colorful vest, daggers drawn
- Lunara: High elf druid, 5'8", graceful athletic build, long flowing chestnut hair with flowers, vibrant green eyes glowing with magic readying, fair skin, pointed ears, practical druid robes in earthy greens and browns, living vines in clothing glowing, wooden staff raised with green magic swirling
- Apocalypse Winter / Pocky: Human wizard, young man in early 20s, 5'10", strong scholarly build, dark unkempt hair, keen blue eyes determined, pale skin, deep blue wizard robes with silver trim, leather satchel, component pouch open, hands glowing with arcane blue magic readying spell
- Val: Brass dragonborn monk, just under 7 feet, lean athletic build, warm brass/copper-bronze scales, ember-glow orange eyes fierce, kind reptilian face now serious, earth-tone monastery robes, bare clawed feet in fighting stance, prayer beads glowing, fists wreathed in ki energy

Scene: All five party members standing together in heroic formation. Weapons drawn - Prismor's greatsword raised, Malrik's daggers ready. Spells prepared - Lunara's staff glowing green with druidic magic, Pocky's hands crackling with arcane blue energy, Val's fists wreathed in golden ki energy. Determined expressions on all faces. United stand. Heroes ready for battle. Citadel corridor with dramatic lighting from magical energies. Epic hero shot. Ready to save Everpeak.

Dialogue: Prismor: "We will protect Everpeak!" ALL: "Together!"

Include speech bubbles with dialogue text clearly readable.

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {FANTASY_STYLE}, heroic pose with magical effects."""

    with open(page_file, 'w') as f:
        json.dump(page, f, indent=2)
    print("✓ Fixed page 23")

def fix_orrery_battle_pages():
    """Fix pages 24-39 with Elven Sanctum location."""
    for page_num in range(24, 40):  # 24-39 inclusive
        page_file = Path(f"pages/page-{page_num:03d}.json")
        if not page_file.exists():
            print(f"⚠ Skipping page {page_num} (file not found)")
            continue

        with open(page_file, 'r') as f:
            page = json.load(f)

        # Update all panels on this page
        for panel in page.get('panels', []):
            prompt = panel.get('prompt', '')

            # Replace location if it's currently Courier Tunnels
            if 'Courier Tunnels' in prompt:
                # Find and replace the location block
                lines = prompt.split('\n')
                new_lines = []
                skip_location = False

                for line in lines:
                    if line.startswith('Location: Courier Tunnels'):
                        # Replace entire location description
                        new_lines.append(ELVEN_SANCTUM)
                        skip_location = True
                    elif skip_location:
                        # Skip lines until we hit a blank line (end of location)
                        if line.strip() == '':
                            skip_location = False
                            new_lines.append(line)
                    else:
                        new_lines.append(line)

                panel['prompt'] = '\n'.join(new_lines)

        with open(page_file, 'w') as f:
            json.dump(page, f, indent=2)

        print(f"✓ Fixed page {page_num}")

def main():
    """Fix pages 22-39 with correct locations."""
    print("="*70)
    print("FIXING SORREL TRANSFORMATION AND ORRERY BATTLE PAGES (22-39)")
    print("="*70)
    print()

    print("Fixing Sorrel transformation pages (22-23)...")
    fix_page_22()
    fix_page_23()

    print()
    print("Fixing Orrery battle pages (24-39)...")
    fix_orrery_battle_pages()

    print()
    print("="*70)
    print("✓ COMPLETE: Fixed pages 22-39 with correct locations")
    print("="*70)

if __name__ == "__main__":
    main()
