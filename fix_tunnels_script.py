#!/usr/bin/env python3
"""
Quick script to fix pages 13-14 tunnel descriptions en masse.
"""

import json
from pathlib import Path

TUNNEL_LOCATION = """Location: Courier Tunnels - rough-hewn stone passages carved through mountain rock. Narrow winding maze-like tunnels with cramped passages. Chalk runes and magical symbols covering walls in white and colored chalk (red, blue, green, yellow) showing different magical routes. Some runes glowing faintly with cold blue magical energy, others flickering erratically showing corruption. Smudged and tampered runes visible in places - deliberate sabotage. Dim magical lighting creating mysterious ominous atmosphere. Occasional spatial distortions visible. Medieval fantasy dungeon with corrupted displacement magic."""

TUNNEL_STYLE_SUFFIX = "medieval fantasy dungeon atmosphere, underground tunnel setting"

# Enhanced character descriptions
CHARS = {
    "Apocalypse Winter": "Human wizard, young man in early 20s. 5'10\" tall, strong but scholarly build. Dark hair, somewhat unkempt from library hours. Keen blue eyes, intelligent and curious. Pale skin from indoor studying. Determined jawline, slight worry lines from concentration. Practical wizard robes in deep blue with silver trim. Leather satchel stuffed with scrolls and books. Component pouch at belt. Ink-stained fingers. Reading glasses. Carries himself with quiet determination despite youth.",
    "Malrik": "Drow rogue, young adult. 5'6\" tall, slim agile acrobat's build. Dark gray-blue drow skin. White hair kept short and practical. Pale lavender eyes, sharp and observant. Sharp cheekbones, mischievous smile. Dark leather armor, well-maintained but not flashy. Street performer's colorful vest underneath. Multiple hidden pockets. Deck of cards always within reach. Quick fluid movements.",
    "Val": "Brass dragonborn monk, early 20s appearance. Just under 7 feet tall, lean athletic build with wiry monk strength. Warm brass/copper-bronze scales with metallic sheen. Ember-glow orange eyes, bright and expressive. Reptilian face with kind open expression, shorter snout. Simple monastery robes in earth tones (browns, tans) with chalk dust marks. Bare clawed feet. Prayer beads around wrist. Always in motion, expressive hand gestures.",
    "Prismor": "Blue crystal dragonborn paladin, middle-aged. 7 feet tall, imposing presence, muscular powerful warrior's physique. Crystalline blue scales with hints of green, gem-like quality. Deep sapphire blue eyes, wise and contemplative. Noble dignified reptilian features. Plate armor with crystalline accents, Oath of the Ancients symbols (leaves, vines) etched in armor. Greatsword on back. Forest green cape. Perfect military posture."
}

def fix_page_13():
    """Fix page 13 panels."""
    page_file = Path("pages/page-013.json")
    with open(page_file, 'r') as f:
        page = json.load(f)

    # Panel 1: Pocky examining runes
    page['panels'][0]['characters'] = {"Apocalypse Winter": CHARS["Apocalypse Winter"]}
    page['panels'][0]['prompt'] = f"""Professional comic book panel illustration.

{TUNNEL_LOCATION}

Characters:
- Apocalypse Winter / Pocky (investigating): {CHARS["Apocalypse Winter"]} Crouching close to tunnel wall, examining chalk runes with intense scholarly focus, reading glasses on, one finger tracing smudged marks, expression showing he's discovered tampering.

Scene: Close-up shot of Pocky crouching at tunnel wall, examining chalk runes very closely. His face inches from the wall, studying smudged and deliberately altered chalk marks. Finger pointing at or tracing the tampering. Reading glasses reflecting rune glow. Serious investigator expression. Tunnel wall in focus showing damaged/altered runes with finger smudge marks visible in chalk. Other party members blurred in background. Underground detective work. Fantasy dungeon with evidence of sabotage.

Dialogue: Pocky (serious, detective mode): "These chalk marks have been smudged. Deliberately altered."

Include speech bubble with dialogue text clearly readable.

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {TUNNEL_STYLE_SUFFIX}, investigative focus."""

    # Panel 2: Malrik investigating
    page['panels'][1]['characters'] = {"Malrik": CHARS["Malrik"]}
    page['panels'][1]['prompt'] = f"""Professional comic book panel illustration.

{TUNNEL_LOCATION}

Characters:
- Malrik (investigating, analyzing): {CHARS["Malrik"]} Standing back looking at bigger picture, sharp lavender eyes scanning tunnel layout and rune patterns, one hand on chin thinking, rogue's mind working through the puzzle, connecting dots.

Scene: Malrik standing in tunnel looking at the overall pattern of tampered runes - not just one spot but seeing the bigger picture. Sharp analytical expression as rogue instincts kick in. Viewing multiple tunnel passages or branching paths, seeing which directions have altered runes versus which don't. Hand on chin or gesturing at pattern. Light bulb moment as he realizes the saboteurs aren't trying to trap randomly - they're steering people AWAY from something specific. Tunnel walls showing pattern of tampering directing away from one particular passage. Fantasy dungeon with strategic sabotage becoming clear.

Dialogue: Malrik (realizing, analytical): "They're not trying to trap us randomly. They're steering us away from something specific."

Include speech bubble with dialogue text clearly readable.

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {TUNNEL_STYLE_SUFFIX}, detective work visualization."""

    # Panel 3: Val pointing
    page['panels'][2]['characters'] = {"Val": CHARS["Val"]}
    page['panels'][2]['prompt'] = f"""Professional comic book panel illustration.

{TUNNEL_LOCATION}

Characters:
- Val (determined, pointing): {CHARS["Val"]} Standing tall, ember-glow orange eyes focused and determined, one arm extended pointing down unexplored dark passage, expression shows he knows courier secrets and has figured out where tampering is steering them AWAY from, brave determination.

Scene: Val standing in tunnel crossroads or junction, arm extended pointing definitively down one specific unexplored passage that looks darker and more ominous than others. The passage he's indicating has NO tampered runes - the saboteurs left it alone because they don't want anyone going that way. Val's body language confident - he knows these tunnels and has figured out the pattern. Other passages visible with visible tampering, but the one Val points to is "clean" which makes it suspicious. Dramatic lighting with tunnel Val indicates disappearing into darkness. Party gathering around listening to Val's courier expertise. Fantasy dungeon with crucial navigation decision.

Dialogue: Val (determined, certain): "That direction. Whatever they're hiding is that way."

Include speech bubble with dialogue text clearly readable.

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {TUNNEL_STYLE_SUFFIX}, dramatic decision moment."""

    # Panel 4: Party deciding
    page['panels'][3]['characters'] = {
        "Prismor": CHARS["Prismor"],
        "Apocalypse Winter": CHARS["Apocalypse Winter"]
    }
    page['panels'][3]['prompt'] = f"""Professional comic book panel illustration.

{TUNNEL_LOCATION}

Characters:
- Prismor (resolute, leader): {CHARS["Prismor"]} Standing tall and imposing, crystalline blue-green scales catching dim tunnel light, deep sapphire eyes resolute and determined, noble bearing, plate armor, greatsword on back, forest green cape, taking charge with paladin authority.
- Apocalypse Winter / Pocky (cautious, warning): {CHARS["Apocalypse Winter"]} Standing beside Prismor, keen blue eyes worried but determined, one hand raised in cautioning gesture, other hand near component pouch ready for danger, scholarly concern mixed with bravery.

Scene: Party gathered in tunnel, making decision to proceed into dangerous unexplored passage. Prismor standing tall as party leader, making command decision with paladin authority and confidence. Pocky beside him offering tactical warning - whoever sabotaged the runes might have left guardians or traps to protect their secret. Other party members visible in background readying weapons and preparing for danger. Tunnel atmosphere tense - about to enter forbidden area. Dark passage ahead looking ominous. Group unity and determination despite danger. Fantasy dungeon with heroes choosing to face unknown threat.

Dialogue:
- Prismor (commanding, resolute): "Then that's where we need to go."
- Pocky (cautious, tactical): "But carefully. Whoever did this might have left guardians."

Include speech bubbles with dialogue text clearly readable.

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {TUNNEL_STYLE_SUFFIX}, team unity and resolve."""

    with open(page_file, 'w') as f:
        json.dump(page, f, indent=2)
    print("✓ Fixed page 13")

def fix_page_14():
    """Fix page 14 panels."""
    page_file = Path("pages/page-014.json")
    with open(page_file, 'r') as f:
        page = json.load(f)

    # Panel 1: Pocky fixing runes
    page['panels'][0]['characters'] = {"Apocalypse Winter": CHARS["Apocalypse Winter"]}
    page['panels'][0]['prompt'] = f"""Professional comic book panel illustration.

{TUNNEL_LOCATION}

Characters:
- Apocalypse Winter / Pocky (concentrating, attempting fix): {CHARS["Apocalypse Winter"]} Crouching at tunnel wall, chalk in hand (white or colored chalk), keen blue eyes narrowed in concentration, brow furrowed with effort, one hand extended touching/redrawing rune symbol, trying to realign corrupted displacement magic, ink-stained fingers working carefully.

Scene: Close-up of Pocky attempting to fix the tampered runes. He's crouching at tunnel wall with piece of chalk in hand, carefully trying to redraw or realign the smudged displacement symbol to restore proper function. Expression shows intense concentration and worry - this is delicate magical work. Hand extended touching wall, chalk making marks. Corrupted rune visible - partially smudged with Pocky's attempted corrections. Soft blue magical glow beginning to form as he works. Sweat on brow despite cool tunnel. Other party members watching tensely in background. Fantasy dungeon with risky magical repair attempt.

Dialogue: Pocky (concentrating, hopeful): "If I can just realign this symbol..."

Include speech bubble with dialogue text clearly readable.

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {TUNNEL_STYLE_SUFFIX}, tense magical repair attempt."""

    # Panel 2: Rune sparking
    page['panels'][1]['characters'] = {"Apocalypse Winter": CHARS["Apocalypse Winter"]}
    page['panels'][1]['prompt'] = f"""Professional comic book panel illustration.

{TUNNEL_LOCATION}

Characters:
- Apocalypse Winter / Pocky (alarmed, jerking back): {CHARS["Apocalypse Winter"]} Recoiling backward from wall as rune sparks violently, keen blue eyes WIDE with alarm, mouth open shouting warning, one arm raised shielding face, other hand dropping chalk, robes billowing from magical backlash energy.

Scene: Dramatic moment as Pocky's repair attempt goes WRONG - the corrupted rune SPARKS violently with wild magical energy. Bright crackling electrical-like magical discharge shooting from the rune symbol - blue-white lightning-like energy arcing outward. Pocky jerking backward in alarm, dropping chalk, shielding himself. Rune glowing dangerously bright - angry red and orange colors mixing with blue showing corruption is deeper than expected. Chunks of chalk or stone dust flying from wall. Other party members in background diving for cover or raising shields. Magical trap or defense mechanism triggered. Fantasy dungeon with dangerous arcane backlash.

Dialogue: Pocky (alarmed, warning cut off): "No! It's not—"

Sound Effects: Large bold "CRACKLE!" showing magical electrical discharge.

Include speech bubble and sound effect clearly readable.

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {TUNNEL_STYLE_SUFFIX}, dramatic magical explosion effect."""

    # Panel 3: Blink Mephit materializing
    # Keep creature description, add location
    page['panels'][2]['prompt'] = f"""Professional comic book panel illustration.

{TUNNEL_LOCATION}

Creatures:
- Blink Mephit (materializing, hostile): Small elemental corrupted by displaced essence, about 2-3 feet tall. Form nearly INVISIBLE - edges flicker and shimmer like mirage or heat distortion. Translucent wings leaving shimmering afterimages. Body phases in and out of visibility - sometimes solid, sometimes ghostly transparent. Eyes visible as glowing points. Distorted warped appearance. Malevolent presence. Displacement essence corrupted into hostile creature.

Scene: Dramatic reveal of Blink Mephit materializing from the magical sparks. The corrupted displacement magic summoned this guardian creature. Mephit appearing in mid-air near the damaged rune - NEARLY INVISIBLE with only flickering edges visible, like looking through heat shimmer. Multiple ghostly afterimages trailing behind it showing displacement nature. Translucent wings barely visible. Glowing eyes. Tunnel air distorting around creature. Pocky and party reacting in alarm. Magical summoning complete - guardian activated. Fantasy dungeon combat about to begin.

Caption: "BLINK MEPHIT - DISPLACEMENT ESSENCE CORRUPTED" (in dramatic caption box)

Sound Effects: "SHHHHRRRR" showing displacement/phasing sound.

Include caption and sound effect clearly readable.

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {TUNNEL_STYLE_SUFFIX}, creature horror reveal, emphasis on nearly-invisible threat."""

    # Panel 4: Val disoriented
    page['panels'][3]['characters'] = {"Val": CHARS["Val"]}
    page['panels'][3]['prompt'] = f"""Professional comic book panel illustration.

{TUNNEL_LOCATION}

Characters:
- Val (disoriented, confused): {CHARS["Val"]} Stumbling, off-balance, ember-glow orange eyes unfocused and confused, kind reptilian face twisted with disorientation, one hand reaching out trying to find wall or ground, other hand to head, brass/copper-bronze scales, monk robes disheveled, lost sense of direction completely.

Scene: Val being hit by Blink Mephit's spatial displacement attack. Reality WARPING around him - tunnel walls bending impossibly, floor and ceiling twisting, multiple overlapping images of same space, Val seeing several directions at once, spatial geometry breaking down. Val stumbling and disoriented, can't tell which way is up or forward, reaching blindly for support. Visible distortion effects - wavy lines, duplicated images, kaleidoscope geometry, Escher-like impossible angles. Blink Mephit barely visible in background (flickering transparent form). Other party members shouting but Val can't orient to their voices. Displacement magic attacking Val's sense of space and direction - his courier navigation abilities completely scrambled. Fantasy dungeon combat with reality-warping magical attack.

Dialogue: Val (disoriented, confused): "Can't... which way is...?"

Include speech bubble with dialogue text clearly readable.

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {TUNNEL_STYLE_SUFFIX}, emphasis on spatial distortion and disorientation effects."""

    with open(page_file, 'w') as f:
        json.dump(page, f, indent=2)
    print("✓ Fixed page 14")

if __name__ == "__main__":
    fix_page_13()
    fix_page_14()
    print("\n✓ Pages 13-14 tunnel descriptions fixed!")
