#!/usr/bin/env python3
"""
Generate detailed HTML pages for characters, NPCs, and monsters
with stats, backstories, and generated images.
"""

import json
import re
from pathlib import Path

DOCS_DIR = Path("docs")
CHAR_DIR = DOCS_DIR / "characters"
NPC_DIR = DOCS_DIR / "npcs"
MONSTER_DIR = DOCS_DIR / "monsters"

# Create output directories
for dir_path in [CHAR_DIR, NPC_DIR, MONSTER_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


def markdown_to_html(text):
    """Convert simple markdown to HTML."""
    if not text:
        return ""

    # Convert **bold** to <strong>
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

    # Split into lines
    lines = text.split('\n')
    html_lines = []
    in_list = False
    list_items = []

    for line in lines:
        stripped = line.strip()

        # Handle list items
        if stripped.startswith('- '):
            if not in_list:
                in_list = True
                list_items = []
            list_items.append(stripped[2:])  # Remove '- '
        else:
            # Close any open list
            if in_list:
                html_lines.append('<ul>')
                for item in list_items:
                    html_lines.append(f'<li>{item}</li>')
                html_lines.append('</ul>')
                in_list = False
                list_items = []

            # Add regular line
            if stripped:
                html_lines.append(stripped)
            elif html_lines:  # Add line breaks for paragraph separation
                html_lines.append('<br><br>')

    # Close any remaining list
    if in_list:
        html_lines.append('<ul>')
        for item in list_items:
            html_lines.append(f'<li>{item}</li>')
        html_lines.append('</ul>')

    return '\n'.join(html_lines)


# Character data from everpeak-complete-module
CHARACTERS = {
    "val": {
        "name": "Val",
        "title": "Brass Dragonborn Monk",
        "class": "Monk",
        "race": "Brass Dragonborn",
        "age": "Early 20s",
        "background": """Val was born high in the Dawnforge Mountains, just a few ridges away from Everpeak Citadel. Raised by monks who answered the century-old call to resettle the citadel after the high elves vanished, Val grew up with few certainties but many quiet rituals.

Now in his early twenties, Val serves as a courier for the Citadel, using his knowledge of hidden footpaths and chalk-marked routes to deliver messages throughout Everpeak. His training emphasizes balance and service, and he carries the monks' teachings of harmony wherever he goes.""",
        "personality": """Warm, friendly, and deeply committed to serving his community. Val radiates kindness through his expressive amber eyes and carries himself with humble confidence. He's curious about the world and always ready to help others.""",
        "physical": """Just under 7 feet tall with a lean, athletic build. Warm brass-colored scales that gleam copper-bronze in light. Gentle, expressive amber eyes. Strong but graceful physique from years of courier work running mountain paths.""",
        "abilities": """**Monk Abilities:**
- **Unarmored Defense:** High AC from Dexterity and Wisdom
- **Martial Arts:** Unarmed strikes deal increased damage
- **Ki Points:** Fuels special abilities like Flurry of Blows
- **Step of the Wind:** Enhanced movement and jumping
- **Deflect Missiles:** Catch and redirect projectiles

**Brass Dragonborn Traits:**
- **Fire Resistance:** Resistant to fire damage
- **Breath Weapon:** 15-foot cone of fire
- **Draconic Ancestry:** Natural affinity for elemental magic""",
        "equipment": """- Simple monk's robes in earth tones
- Lightweight traveling gear for mountain climbing
- Courier's satchel with chalk symbols
- Prayer beads
- Simple staff (+1 weapon potential)
- Flickerfoot Shoes (Displacement essence item)""",
        "player_notes": """**Player: Jasper (Age 13)**

**Playstyle:** Strategic combat, puzzle-solving, careful planning with calculated risks. Excels at observational details and discovering hidden secrets.

**Theme Preferences:** Exploration, mystery-solving, tactical engagement""",
        "image": "../images/characters/val-portrait.png"
    },

    "prismor": {
        "name": "Prismor",
        "title": "Blue Crystal Dragonborn Paladin",
        "class": "Paladin (Oath of the Ancients)",
        "race": "Blue Crystal Dragonborn",
        "age": "Middle decades (mature)",
        "background": """Prismor is older than many who now call Everpeak home. Approaching his middle decades, he came to the citadel decades ago after hearing tales of a place where the old magics of vanished high elves lingered in the very stones.

He settled here to fulfill his paladin's vow: to defend this citadel born of sacrifice and mystery. His long service has made him a mentor to younger settlers and a trusted guardian of Everpeak's fragile harmony.""",
        "personality": """Calm, protective, and steadfast. Prismor carries himself with noble bearing and quiet wisdom. He is deeply dedicated to defending Everpeak and upholding his sacred oaths.""",
        "physical": """Tall and powerfully built (7+ feet). Brilliant blue crystal-like scales that shimmer and refract light. Wise, steady blue eyes. Mature bearing showing experience and dedication. Crystalline scales create a faceted, gem-like appearance.""",
        "abilities": """**Paladin Abilities:**
- **Lay on Hands:** Heal wounds with divine power
- **Divine Smite:** Channel divine energy into weapon strikes
- **Aura of Protection:** Allies gain bonus to saving throws
- **Channel Divinity:** Turn the Unholy, Nature's Wrath
- **Oath Spells:** Ensnaring Strike, Moonbeam, Plant Growth

**Crystal Dragonborn Traits:**
- **Radiant Resistance:** Resistant to radiant damage
- **Crystalline Breath:** Cone of radiant energy
- **Light Refraction:** Scales shimmer and catch light""",
        "equipment": """- Polished plate armor with blue-silver finish
- Holy symbol of the Oath of the Ancients
- Well-maintained shield (+1 shield potential)
- Longsword (primary weapon)
- Cape in deep blue with silver trim
- Gearplate Buckler (Mechanistic essence item)""",
        "player_notes": """**Player: Max (Age 13)**

**Playstyle:** Strategic frontline combat with meaningful tactical decisions. Values story-driven content and moral choices.

**Theme Preferences:** Protecting others, character backstory integration""",
        "image": "../images/characters/prismor-portrait.png"
    },

    "apocalypse_winter": {
        "name": "Apocalypse Winter",
        "title": "Human Wizard and Scholar",
        "class": "Wizard",
        "race": "Human",
        "age": "Early 20s",
        "background": """Apocalypse Winter (nicknamed "Pocky") grew up far away in a small human town with only vague stories of Everpeak. As he came of age, he felt drawn to the citadel by scholarly ambition and the mysteries left by the vanished high elves.

Now he spends most of his days in the Grand Library, studying fragments of old manuscripts and piecing together the secrets of the Dawn's Crown alignment and the elemental essences that power Everpeak.""",
        "personality": """Intensely curious and eager to learn. Apocalypse radiates excitement about discovering knowledge and solving arcane riddles. Slightly awkward socially but brilliant academically. Often gets lost in research.""",
        "physical": """Young human in early twenties. Slender, scholarly build. Pale skin from library time. Messy dark hair often falling over eyes. Intelligent dark eyes behind round spectacles. Ink stains on fingers from constant note-taking.""",
        "abilities": """**Wizard Abilities:**
- **Spellcasting:** Access to vast wizard spell list
- **Arcane Recovery:** Recover spell slots during short rest
- **Ritual Casting:** Cast spells as rituals
- **Spell Mastery:** Master specific spells for free casting
- **School Specialization:** Enhanced spells from chosen school

**Human Traits:**
- **Versatile:** Extra skill proficiency and feat
- **Adaptable:** Bonus to all ability scores""",
        "equipment": """- Wizard's robes in deep navy with silver stars
- Multiple pockets for spell components
- Leather-bound spellbook
- Arcane focus pendant (crystal)
- Reading spectacles
- Warm winter cloak
- Star-Touched Focus (Celestial essence item)
- Spell scrolls""",
        "player_notes": """**Player: Avery (Age 13)**

**Playstyle:** Puzzle-solving, tactical spellcasting, creative problem-solving. Values narrative depth and player agency.

**Theme Preferences:** Mystery-solving, experimentation, knowledge acquisition""",
        "image": "../images/characters/apocalypse-winter-portrait.png"
    },

    "lunara": {
        "name": "Lunara",
        "title": "High Elf Druid",
        "class": "Druid (Circle of the Moon)",
        "race": "High Elf",
        "age": "Mature (centuries old)",
        "background": """Lunara is old enough to remember a world before she journeyed to Everpeak, though she did not grow up in the citadel. She came decades ago, following the quiet plea spread through many lands after the last alignment.

Drawn by her druidic calling and curiosity, Lunara has dedicated herself to tending Everpeak's living gardens and green spaces that thrive at this unnatural altitude. She helps maintain the delicate balance of Nature Essence flowing through the citadel.""",
        "personality": """Serene, peaceful, and deeply connected to nature. Lunara moves with grace and speaks with ancient wisdom. She accepts ambiguity like nature's shifting seasons and nurtures what she can with patient care.""",
        "physical": """Tall, graceful high elf (6+ feet). Ageless beauty with ancient wisdom in bright green eyes. Long silver-white hair adorned with flowers and vines. Delicate elven features. Pale skin with slight green undertones from nature connection.""",
        "abilities": """**Druid Abilities:**
- **Wild Shape:** Transform into beasts
- **Spellcasting:** Nature-themed divine magic
- **Combat Wild Shape:** Enhanced animal forms (Circle of Moon)
- **Nature's Sanctuary:** Beasts find it hard to attack
- **Speak with Animals:** Communicate with beasts

**High Elf Traits:**
- **Fey Ancestry:** Advantage against charm, immune to sleep
- **Trance:** Meditate instead of sleep (4 hours)
- **Cantrip:** Knows one wizard cantrip
- **Darkvision:** See in dim light""",
        "equipment": """- Flowing robes of natural greens and browns
- Living vines and flowers woven into clothing
- Wooden staff carved with nature symbols
- Druidic focus (special seed from Marivielle)
- Natural jewelry (flowers, wooden beads)
- Greenbriar Band (Nature essence item)""",
        "player_notes": """**Player: Sofia (Age 13)**

**Playstyle:** Nature-focused roleplay, environmental interaction, diplomatic solutions. Comfortable with both combat and social encounters.

**Theme Preferences:** Nature connection, environmental stewardship, balance""",
        "image": "../images/characters/lunara-portrait.png"
    },

    "malrik": {
        "name": "Malrik",
        "title": "Drow Rogue and Street Performer",
        "class": "Rogue",
        "race": "Drow",
        "age": "Young adult",
        "background": """Malrik never truly fit in anywhere else. He came to Everpeak as a young adult a couple of decades ago, after hearing rumors of a mountain citadel that welcomed all races who wished to rebuild and protect something precious.

He arrived hoping for acceptance away from the old prejudices of his homeland. Now he performs in the marketplace, using his illusions and sleight-of-hand to delight crowds while keeping a watchful eye for threats to the citadel's gentle peace.""",
        "personality": """Charming, theatrical, and watchful. Malrik presents a roguish, playful exterior while maintaining sharp observation of everything around him. He seeks purpose and has found it in protecting Everpeak.""",
        "physical": """Lean, agile drow build (about 5'9"). Distinctive charcoal-dark skin. Striking white hair pulled back in a ponytail. Sharp violet eyes, always observing. Angular, handsome features with graceful, performer's movements.""",
        "abilities": """**Rogue Abilities:**
- **Sneak Attack:** Massive damage to surprised foes
- **Cunning Action:** Bonus action Dash, Disengage, or Hide
- **Evasion:** Take half damage on failed Dex saves
- **Uncanny Dodge:** Reduce incoming damage
- **Expertise:** Double proficiency in chosen skills

**Drow Traits:**
- **Superior Darkvision:** See 120 feet in darkness
- **Sunlight Sensitivity:** Disadvantage in bright light
- **Drow Magic:** Dancing Lights, Faerie Fire, Darkness
- **Fey Ancestry:** Advantage against charm""",
        "equipment": """- Colorful performer's garb (purples, reds, golds)
- Dark leather armor hidden beneath
- Multiple daggers (concealed)
- Deck of playing cards for tricks
- Acrobat's gear (light, flexible)
- Venomous Dagger (drow item) or Flickerfoot Shoes""",
        "player_notes": """**Player: Liam (Age 13)**

**Playstyle:** Stealth, skill-based solutions, social manipulation. Values narrative integration and creative problem-solving.

**Theme Preferences:** Intrigue, subterfuge, theatrical flair""",
        "image": "../images/characters/malrik-portrait.png"
    }
}


def generate_character_page(char_id, char_data):
    """Generate detailed character page HTML."""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{char_data['name']} - {char_data['title']}</title>
    <link rel="stylesheet" href="../css/main.css">
    <link rel="stylesheet" href="../css/detail-page.css">
</head>
<body>
    <header class="site-header">
        <div class="header-content">
            <h1 class="site-title">Everpeak Citadel</h1>
            <nav class="site-nav">
                <a href="../index.html" class="nav-link">Read</a>
                <a href="../characters.html" class="nav-link active">Characters</a>
                <a href="../locations.html" class="nav-link">Locations</a>
                <a href="../about.html" class="nav-link">About</a>
                <a href="../download.html" class="nav-link">Download</a>
            </nav>
        </div>
    </header>

    <main class="detail-container">
        <nav class="breadcrumb">
            <a href="../characters.html">← Back to Characters</a>
        </nav>

        <div class="detail-header">
            <div class="portrait">
                <img src="{char_data['image']}" alt="{char_data['name']}" onerror="this.src='../images/placeholder.png'">
            </div>
            <div class="header-info">
                <h1>{char_data['name']}</h1>
                <h2 class="subtitle">{char_data['title']}</h2>
                <div class="quick-stats">
                    <span class="stat"><strong>Class:</strong> {char_data['class']}</span>
                    <span class="stat"><strong>Race:</strong> {char_data['race']}</span>
                    <span class="stat"><strong>Age:</strong> {char_data['age']}</span>
                </div>
            </div>
        </div>

        <div class="detail-content">
            <section class="detail-section">
                <h3>Background</h3>
                <div class="section-content">
                    <p>{char_data['background'].replace(chr(10) + chr(10), '</p><p>')}</p>
                </div>
            </section>

            <section class="detail-section">
                <h3>Personality</h3>
                <div class="section-content">
                    <p>{char_data['personality']}</p>
                </div>
            </section>

            <section class="detail-section">
                <h3>Physical Appearance</h3>
                <div class="section-content">
                    <p>{char_data['physical']}</p>
                </div>
            </section>

            <section class="detail-section">
                <h3>Abilities & Traits</h3>
                <div class="section-content abilities">
                    {markdown_to_html(char_data['abilities'])}
                </div>
            </section>

            <section class="detail-section">
                <h3>Equipment</h3>
                <div class="section-content equipment">
                    {markdown_to_html(char_data['equipment'])}
                </div>
            </section>

            <section class="detail-section player-info">
                <h3>Player Information</h3>
                <div class="section-content">
                    {markdown_to_html(char_data['player_notes'])}
                </div>
            </section>
        </div>

        <div class="navigation-footer">
            <a href="../characters.html" class="btn-secondary">← All Characters</a>
            <a href="../index.html" class="btn-primary">Start Reading →</a>
        </div>
    </main>

    <footer class="site-footer">
        <p>&copy; 2024 Everpeak Citadel | AI-generated comic</p>
    </footer>
</body>
</html>
"""
    return html


def main():
    """Generate all detail pages."""
    print("Generating character detail pages...")

    for char_id, char_data in CHARACTERS.items():
        output_file = CHAR_DIR / f"{char_id}.html"
        html = generate_character_page(char_id, char_data)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✓ Generated {output_file}")

    print(f"\n✓ Generated {len(CHARACTERS)} character pages")

if __name__ == "__main__":
    main()
