#!/usr/bin/env python3
"""
Fix pages 20-22 where party splits up to investigate different locations.
"""

import json
from pathlib import Path

# Location descriptions
GRAND_LIBRARY = """Location: The Grand Library - soaring ceilings with endless shelves of ancient tomes and scrolls. Tall arched windows filtering light onto reading tables. Floating magical lights providing illumination. Wooden ladders on rails to reach high shelves. Dust motes in air. Scholar's paradise with books floor to ceiling. Ancient manuscripts, star-charts, arcane diagrams visible. Quiet, reverent atmosphere. High elven architecture - elegant carved wood and stone. Medieval fantasy grand library."""

OBSERVATORY = """Location: The Observatory - small domed chamber at citadel's peak. Glass ceiling showing sky and stars. Brass orrery at center with moving spheres representing celestial bodies. Star-charts on walls. Telescopes and astronomical instruments. Cold blue magical light from runes. Ancient elven construction with precision clockwork mechanisms. Sense of cosmic significance. Medieval fantasy astronomical chamber."""

BALCONY_CAFE = """Location: Balcony Garden Café - impossible sunny terrace high in snow-covered mountains. Lush greenery everywhere - flowering vines, potted exotic plants, herbs growing. Magical warmth despite winter outside. Wooden tables and chairs with nature carvings. Stone balcony railing overlooks snow-covered citadel below. Sunlight streaming through leaves creating dappled shadows. High fantasy garden oasis. NO modern items. Medieval fantasy aesthetic."""

COURIER_HQ = """Location: Courier Guild Headquarters - small stone office/meeting room in Everpeak Citadel. Chalk route maps on walls showing tunnel networks. Simple wooden desks and benches. Couriers coming and going. Dispatch boards with delivery assignments. Medieval fantasy guild hall. Winter cloaks hanging on pegs. Practical working space."""

CITADEL_INTERIOR = """Location: Everpeak Citadel interior corridors - white stone hallways with high vaulted ceilings. Ancient high elven architecture with elegant arches. Magical lanterns providing warm light. Winter decorations (festival ribbons, banners). Medieval fantasy castle interior."""

FANTASY_STYLE = "medieval fantasy setting, high fantasy atmosphere"

def fix_page_20():
    """Fix page 20 locations."""
    page_file = Path("pages/page-020.json")
    with open(page_file, 'r') as f:
        page = json.load(f)

    # Panel 1: Party deciding to split (still in tunnels exit or citadel interior)
    page['panels'][0]['prompt'] = f"""Professional comic book panel illustration.

{CITADEL_INTERIOR}

Characters:
- Prismor: Blue crystal dragonborn paladin, 7 feet tall, imposing presence, muscular powerful build, crystalline blue-green scales, deep sapphire eyes, noble bearing, plate armor with nature symbols, greatsword on back, forest green cape
- Malrik: Drow rogue, 5'6\", slim agile build, dark gray-blue drow skin, white short hair, pale lavender eyes, sharp features, dark leather armor, colorful street performer's vest
- Apocalypse Winter / Pocky: Human wizard, young man in early 20s, 5'10\", strong scholarly build, dark unkempt hair, keen blue eyes, pale skin, deep blue wizard robes with silver trim, leather satchel with scrolls, component pouch, ink-stained fingers, reading glasses

Scene: Party gathered in citadel hallway discussing strategy. Pocky animated and excited suggesting they split up to cover more ground. Prismor agreeing, gesturing that he and Malrik will check the observatory for celestial lenses. Group planning poses. Winter citadel setting.

Dialogue: Pocky: "We should split up! Cover more ground!" Prismor: "Agreed. Malrik and I will check the observatory. The celestial lenses are key."

Include speech bubbles with the dialogue text clearly readable.

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {FANTASY_STYLE}."""

    # Panel 2: Groups separating
    page['panels'][1]['prompt'] = f"""Professional comic book panel illustration.

{CITADEL_INTERIOR}

Characters:
- Lunara: High elf druid, 5'8\", graceful athletic build, long flowing chestnut hair with flowers, vibrant green eyes, fair skin, pointed ears, practical druid robes in earthy greens and browns, living vines in clothing, wooden staff
- Val: Brass dragonborn monk, just under 7 feet, lean athletic build, warm brass/copper-bronze scales, ember-glow orange eyes, kind reptilian face, simple earth-tone monastery robes with chalk dust, bare clawed feet, prayer beads on wrist

Scene: Lunara and Val standing together, discussing their plans. Lunara gesturing toward garden direction. Val pointing toward courier areas. Party visibly splitting into groups - others visible in background heading different directions. Citadel corridor intersection. Planning and determination.

Dialogue: Lunara: "I'll return to the garden with Marivielle. Check the Nature Essence directly." Val: "And I'll question the couriers. Someone must have seen something."

Include speech bubbles with the dialogue text clearly readable.

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {FANTASY_STYLE}."""

    # Panel 3: SPLIT PANEL showing all investigations
    page['panels'][2]['prompt'] = f"""Professional comic book panel illustration.

SPLIT PANEL LAYOUT showing four separate locations simultaneously:

Top Left - LIBRARY:
{GRAND_LIBRARY}
Pocky and Marge examining crystal lenses and manuscripts.

Top Right - OBSERVATORY:
{OBSERVATORY}
Prismor and Malrik investigating, Malrik examining locks and compartments.

Bottom Left - GARDEN:
{BALCONY_CAFE}
Lunara communing with plants, hands on vines, eyes glowing with druidic magic.

Bottom Right - COURIER HQ:
{COURIER_HQ}
Val talking to frightened halfling couriers, taking notes.

Characters visible in their respective locations as described in visuals.

Scene: Simultaneous investigations happening across Everpeak. Split panel composition clearly showing four distinct locations and activities. Each quadrant shows different investigation in progress. Medieval fantasy setting.

No dialogue (visual montage).

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {FANTASY_STYLE}, split panel layout."""

    # Panel 4: Marge + Pocky in library
    page['panels'][3]['prompt'] = f"""Professional comic book panel illustration.

{GRAND_LIBRARY}

Characters:
- Marge (Head Librarian): Human woman, middle-aged (40s-50s), 5'4\", slightly stooped from years of reading, modest scholar's robes in muted colors, ink-stained fingers/sleeves/hem, tired wise eyes, graying hair in practical bun, surrounded by books and scrolls
- Apocalypse Winter / Pocky: Human wizard, young man in early 20s, 5'10\", strong scholarly build, dark unkempt hair, keen blue eyes wide with alarm and realization, pale skin, deep blue wizard robes with silver trim, leather satchel, ink-stained fingers, reading glasses, examining crystal lenses

Scene: Close-up in library. Marge holding up crystal lenses to light, showing Pocky that they're FAKE - wrong refraction, crude construction visible. Pocky's expression shocked as he realizes someone replaced the True Lenses with counterfeits. Lenses catching light showing they're wrong. Books and star-charts visible on table between them. Library setting with ancient tomes in background.

Dialogue:
- Marge (grave, showing lenses): "These should focus Celestial Essence. But they're counterfeits!"
- Pocky (alarmed, realizing conspiracy): "Someone replaced the True Lenses!"

Include speech bubbles with the dialogue text clearly readable.

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {FANTASY_STYLE}."""

    with open(page_file, 'w') as f:
        json.dump(page, f, indent=2)
    print("✓ Fixed page 20")

def fix_page_21():
    """Fix page 21 locations."""
    page_file = Path("pages/page-021.json")
    with open(page_file, 'r') as f:
        page = json.load(f)

    # Panel 1: Malrik in observatory
    page['panels'][0]['prompt'] = f"""Professional comic book panel illustration.

{OBSERVATORY}

Characters:
- Malrik (investigating): Drow rogue, 5'6\", slim agile build, dark gray-blue drow skin, white short hair, pale lavender eyes sharp and observant, sharp features focused with rogue's attention to detail, dark leather armor, colorful vest, crouched examining door/lock, fingers tracing scratches

Scene: Malrik crouched at observatory door or compartment, examining lock mechanism with rogue's keen eye for detail. Fresh scratches visible on metal lock - recent forced entry. Finger pointing at evidence. Prismor visible in background looking at orrery or charts. Observatory setting with astronomical instruments and starlight through glass dome. Detective work in action.

Dialogue: Malrik (pointing at evidence, serious): "Look. Scratches on the lock. Recent."

Include speech bubble with dialogue text clearly readable.

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {FANTASY_STYLE}."""

    # Panel 2: Prismor in observatory
    page['panels'][1]['prompt'] = f"""Professional comic book panel illustration.

{OBSERVATORY}

Characters:
- Prismor (discovering): Blue crystal dragonborn paladin, 7 feet tall, imposing muscular build, crystalline blue-green scales catching observatory's mystical light, deep sapphire eyes showing recognition and alarm, noble reptilian features, plate armor with nature symbols, greatsword on back, forest green cape, holding crimson emblem in armored hand

Scene: Prismor pulling hidden compartment open in observatory wall or furniture, revealing crimson emblem inside - same symbol he saw at forge on cloaked figures. His expression shows grim recognition connecting the dots. Hidden compartment details visible. Observatory with brass orrery and astronomical charts in background. Discovery of conspiracy evidence.

Dialogue: Prismor (grim recognition, holding emblem): "This symbol... I saw it at the forge. On cloaked figures."

Include speech bubble with dialogue text clearly readable.

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {FANTASY_STYLE}."""

    # Panel 3: Lunara in garden
    page['panels'][2]['prompt'] = f"""Professional comic book panel illustration.

{BALCONY_CAFE}

Characters:
- Lunara (communing with nature): High elf druid, 5'8\", graceful athletic build, long flowing chestnut hair with flowers woven in, vibrant green eyes GLOWING with druidic magic, fair skin, pointed ears, serene but focused expression, practical druid robes in earthy greens and browns, living vines woven into clothing visibly reacting to her magic, wooden staff, bare feet on garden soil, hands touching flowering vines

Scene: Lunara kneeling in lush garden, hands on vines and plants, eyes glowing bright green with druidic Speak with Plants magic. Plants around her glowing faintly, responding to her communion. Ghostly vision/memory visible in magical aura - shadowy figure (noble silhouette) stealing metal objects at night. Plants sharing their memories with her. Sunlit garden with impossible greenery despite winter. Nature magic visualization.

Dialogue: Lunara (eyes glowing, channeling plant memories): "The plants remember... a noble. Stealing frozen iron in the night."

Include speech bubble with dialogue text clearly readable.

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {FANTASY_STYLE}, magical nature effects."""

    # Panel 4: Val in courier HQ
    page['panels'][3]['prompt'] = f"""Professional comic book panel illustration.

{COURIER_HQ}

Characters:
- Val (questioning): Brass dragonborn monk, just under 7 feet, lean athletic build, warm brass/copper-bronze scales, ember-glow orange eyes showing concern and alarm, kind reptilian face serious and focused, simple earth-tone monastery robes with chalk dust, bare clawed feet, prayer beads on wrist, leaning forward listening intently
- Halfling Courier (frightened): Small halfling, 3-4 feet tall, young adult, practical courier clothing - sturdy travel clothes in earth tones, courier's satchel, very frightened expression, gesturing frantically as he recounts what he saw, fear in eyes

Scene: Val crouched or leaning down to halfling courier level, listening intently as frightened halfling recounts what he witnessed. Halfling animated, scared, pointing downward (toward deep sanctum). Courier headquarters setting with route maps on walls, other couriers visible in background pausing to listen. Urgent intelligence gathering. Val's expression shows this is serious forbidden news.

Dialogue:
- Courier (frightened, gesturing frantically): "I saw them! Drow and a human noble! Going down to the deep sanctum!"
- Val (alarmed, serious): "The Elven Sanctum? But that's forbidden!"

Include speech bubbles with dialogue text clearly readable.

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {FANTASY_STYLE}."""

    with open(page_file, 'w') as f:
        json.dump(page, f, indent=2)
    print("✓ Fixed page 21")

def main():
    """Fix pages 20-21 with correct split party locations."""
    print("="*70)
    print("FIXING SPLIT PARTY INVESTIGATION PAGES (20-21)")
    print("="*70)
    print()

    fix_page_20()
    fix_page_21()

    print()
    print("="*70)
    print("✓ COMPLETE: Fixed pages 20-21 with correct locations")
    print("="*70)

if __name__ == "__main__":
    main()
