#!/usr/bin/env python3
"""
Generate detailed HTML pages for NPCs with backgrounds and stats.
"""

from pathlib import Path

# Output directory
OUTPUT_DIR = Path("docs/npcs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# NPC data extracted from everpeak-complete-module.md
NPCS = {
    "sorrel_halfling": {
        "name": "Sorrel (Halfling Form)",
        "title": "Gold Dragon Wyrmling in Disguise",
        "race": "Gold Dragon (disguised as Halfling)",
        "age": "Wyrmling (appears 10 years old)",
        "background": """Sorrel is secretly a gold dragon wyrmling observing and testing the party's worth. Appearing as a curious halfling child, Sorrel has been watching Everpeak Citadel and its inhabitants for some time. This ancient creature uses the innocent guise to move freely through the citadel, guiding worthy heroes toward cooperation and protecting the citadel's secrets. Sorrel is drawn to acts of heroism and kindness, quietly steering adventurers toward the greater good while maintaining the halfling disguise until the moment of greatest need.""",
        "personality": """Cheerful, inquisitive, unexpectedly wise. Tilts head thoughtfully, praises small acts of heroism, and quietly steers people toward cooperation. Avoids lying but deflects direct questions with half-truths. Supportive and encouraging, rarely criticizes but asks gentle questions to guide others. Occasionally slips up and says something far too wise for a "child," then quickly coughs or shrugs it off.""",
        "appearance": """Appears as a sandy-haired halfling child around 10 years old. Large, curious golden eyes that hold unusual wisdom. Slightly oversized cloak that's a bit tattered at the edges. Stands with feet turned inward (as if shy) and arms often behind his back. Subtle golden shimmer to skin in certain lighting. Cherubic innocent face that can shift to show ancient wisdom.""",
        "role_abilities": """**Role:** Mysterious guide and observer testing the party's worth<br><br>**Known Information:**<br>- Enjoys the festival and finds the party interesting<br>- Mentions old stories: "When stars align, truths emerge"<br>- Acknowledges the citadel "once had different caretakers"<br>- Hints at draconic origins but won't confirm until needed<br><br>**Speech Patterns:**<br>- Light, bright, sing-song tone<br>- Speaks quickly in bursts, then slows with thoughtful "Hmm"<br>- Common phrases: "Oh wow!", "Gosh...", "Neat!", "Oh! That reminds me..."<br>- Tilts head curiously when intrigued<br>- Fiddles with sleeves when nervous""",
        "equipment": """- Slightly oversized, tattered cloak<br>- Simple child's clothing with subtle gold accents<br>- No weapons (doesn't need them)<br>- Hidden draconic nature""",
        "image": "../images/npcs/sorrel-halfling-portrait.png"
    },
    "sorrel_dragon": {
        "name": "Sorrel (True Form)",
        "title": "Gold Dragon Wyrmling",
        "race": "Gold Dragon",
        "age": "Wyrmling (young but ancient wisdom)",
        "background": """When the moment of truth arrives, Sorrel reveals their true nature as a gold dragon wyrmling. Despite their small size (cat-sized to small dog-sized), Sorrel radiates ancient wisdom and noble purpose. Gold dragons are legendary for their wisdom, justice, and protection of the innocent. Sorrel has been observing the party throughout their adventures, testing their character and worth. The revelation comes at a crucial moment when the party needs guidance or protection, showing that Everpeak Citadel has always had a guardian watching over it.""",
        "personality": """Noble, protective, wise beyond years. In true form, Sorrel's ancient draconic wisdom shines through while maintaining the cheerful, encouraging nature shown in halfling form. Deeply committed to justice and protecting the worthy. Patient teacher and guide. Takes joy in seeing mortals rise to challenges and grow in character.""",
        "appearance": """Small majestic gold dragon wyrmling, roughly cat-sized. Brilliant golden scales that shimmer and gleam like precious metal, reflecting light beautifully. Intelligent, kind amber eyes that glow with inner wisdom. Elegant wings proportioned for size. Delicate horns and whiskers. Regal bearing despite diminutive stature. Warm golden glow emanates from scales naturally.""",
        "role_abilities": """**Dragon Abilities:**<br>- **Breath Weapon:** Cone of fire or weakening gas<br>- **Draconic Presence:** Inspires courage in allies<br>- **Flight:** Elegant aerial maneuvering<br>- **Ancient Knowledge:** Vast historical knowledge<br>- **Shapechanger:** Can polymorph into humanoid forms<br>- **Darkvision:** 60 feet<br>- **Blindsight:** 10 feet<br><br>**Wyrmling Stats:**<br>- **AC:** 17 (natural armor)<br>- **HP:** 60 (8d8 + 24)<br>- **Speed:** 30 ft., fly 60 ft.<br>- **Alignment:** Lawful Good""",
        "equipment": """- Natural draconic abilities<br>- No equipment needed<br>- Magical polymorph capability""",
        "image": "../images/npcs/sorrel-dragon-portrait.png"
    },
    "marge": {
        "name": "Marge",
        "title": "Head Librarian of the Grand Library",
        "race": "Human",
        "age": "Middle-aged (40s-50s)",
        "background": """Marge has served as Head Librarian of Everpeak's Grand Library for decades. She is the foremost expert on the citadel's incomplete historical records and has dedicated her life to preserving what knowledge remains of the high elves and their vanishing. Marge mentors young scholars like Apocalypse Winter and helps guide those seeking to understand the Dawn's Crown alignment and the citadel's elemental essences. Despite the gaps in the archives, she maintains hope that the right people asking the right questions might piece together the truth.""",
        "personality": """Kindly, scholarly, precise, and protective of knowledge. Serious about preserving books and information. Warm and reassuring toward genuine seekers of knowledge. Can become flustered if books are handled carelessly and will politely scold those who damage tomes. Always eager to share what she knows and help others learn. Patient teacher with a remarkable memory for page numbers and references.""",
        "appearance": """Middle-aged human woman wearing modest robes stained with ink. Gray-streaked brown hair in a practical bun. Intelligent brown eyes behind reading spectacles (half-moon style on a chain). Slightly stooped shoulders from years of poring over books. Keeps a quill tucked behind her ear. Ink-stained sleeves from constant note-taking.""",
        "role_abilities": """**Role:** Knowledge keeper, mentor, research expert<br><br>**Known Information:**<br>- Crystal lenses related to observatory and orrery are missing<br>- High elves vanished a century ago after a great sacrifice<br>- Archives are incomplete; Dawn's Crown ritual not fully understood<br>- References to multiple elemental essences exist in texts<br><br>**Skills:**<br>- Expert researcher and archivist<br>- Encyclopedic knowledge of library contents<br>- Can locate obscure references quickly<br>- Remembers exact page numbers from memory<br><br>**Speech Patterns:**<br>- Warm, reassuring, slightly breathy tone<br>- Steady, measured, precise speech<br>- Common phrases: "Certainly", "Fascinating", "Let's see here...", "Let me check my notes..."<br>- Adjusts spectacles when emphasizing points<br>- Taps finger when in deep thought""",
        "equipment": """- Practical librarian's robes in muted blues and grays<br>- Half-moon spectacles on chain<br>- Multiple quills (one behind ear)<br>- Ink bottles and stained sleeves<br>- Personal research notes<br>- Keys to restricted archives""",
        "image": "../images/npcs/marge-portrait.png"
    },
    "barth": {
        "name": "Barth",
        "title": "Master Blacksmith of Dawnforge",
        "race": "Drow",
        "age": "Mature adult",
        "background": """Barth is the master blacksmith of Everpeak's Dawnforge workshop, trusted by both Prismor and Malrik. He has built his reputation on quality craftsmanship and careful attention to the properties of different metals. Recently troubled by the theft of a strange alloy called "frozen iron," Barth has noticed suspicious activity around the forge. He has heard rumors of cloaked figures asking about forging keys or ancient locks, making him uneasy. Despite his wariness, he's willing to help those he trusts by reforging fragments into useful items.""",
        "personality": """Stoic, thoughtful, serious, and dedicated to his craft. Takes great pride in quality workmanship. Speaks slowly and deliberately, measuring each word. Polite but subdued, with intense direct eye contact. Warms up to those who show genuine respect for craftsmanship. Becomes terse and tight-jawed when annoyed. Taps his anvil lightly when worried or deep in thought.""",
        "appearance": """Lean, muscular drow with dark charcoal skin showing metallic sheen from forge work. White hair kept short and practical. Pale purple eyes that study everything carefully. Faint scar over one cheek from past smithing accident. Burn scars visible on muscular arms. Heavy leather blacksmith's apron dusted with metal shavings. Stands upright with arms often crossed or hands on hips.""",
        "role_abilities": """**Role:** Master craftsman, metalwork expert, trusted ally<br><br>**Known Information:**<br>- Strange alloy "frozen iron" recently stolen from forge<br>- Cloaked figures asking about forging keys for ancient locks<br>- Frozen iron interacts strangely with Mechanistic Essence<br>- Suspects materials could alter orrery settings<br>- Hints at factional split among drow visitors<br><br>**Skills:**<br>- Expert blacksmith and metalworker<br>- Knowledge of rare metals and alloys<br>- Can identify magical properties of materials<br>- Proficient with Smith's Tools<br>- Understanding of Mechanistic Essence<br><br>**Speech Patterns:**<br>- Low, resonant, gravelly tone<br>- Quiet but intense delivery<br>- Slow, deliberate, measured words<br>- Common phrases: "Hmm", "Careful", "We'll need more iron", "We'll do it right, or not at all"<br>- Firm nod instead of saying "yes"<br>- Frequently inspects or rubs hands""",
        "equipment": """- Heavy leather blacksmith's apron<br>- Smith's hammer (masterwork quality)<br>- Tongs and metalworking tools<br>- Simple drow clothing (dark colors)<br>- Work gloves (metal-shavings resistant)<br>- Various metal samples and projects""",
        "image": "../images/npcs/barth-portrait.png"
    },
    "marivielle": {
        "name": "Marivielle Greenbough",
        "title": "Owner of the Balcony Garden Café",
        "race": "Half-Elf",
        "age": "30s-40s",
        "background": """Marivielle Greenbough tends the beautiful Balcony Garden Café, a space infused with Nature Essence that allows lush plants to thrive at impossible altitude. She provided Lunara with a special seed tied to the garden's natural magic. Marivielle is observant and nurturing, keeping careful watch over who comes and goes at odd hours. Recently, she noticed a noble visitor leaving frosty footprints late at night and has observed some plants wilting unexpectedly—signs that the Nature Essence may be disrupted. Her café serves as both a peaceful refuge and a place where important information can be gathered.""",
        "personality": """Gentle, nurturing, observant, and hospitable. Warm and maternal in demeanor. Always ready to offer food or tea. Notices when people are stressed or hurt and tries to ease tensions. Hums lullabies while tending plants or when lost in thought. Moves slowly and gracefully with quiet confidence. Will speak softly but firmly to warn others of suspicious behavior or danger.""",
        "appearance": """Graceful half-elf woman with braided chestnut hair threaded with small flowers. Long auburn hair with subtle green highlights. Warm hazel-green eyes that observe everything. Delicate elvish features with a friendly, welcoming smile. Comfortable café owner's attire in natural greens and browns with leaf-patterned apron. Flower behind ear (changes daily). Hands often dusted with potting soil or flour from baking.""",
        "role_abilities": """**Role:** Café owner, nature guardian, information source<br><br>**Known Information:**<br>- Noble visitor left frosty footprints late at night<br>- Plants wilting from Nature Essence disruption<br>- Overheard whispers about "keys" and "alignment"<br>- Special seed resonates with natural ley lines<br>- Yule Tree and seed may restore balance if essences destabilize<br><br>**Skills:**<br>- Expert gardener with druidic knowledge<br>- Proficient in Nature checks<br>- Excellent cook and herbalist<br>- Observant and insightful<br>- Connection to Nature Essence flows<br><br>**Speech Patterns:**<br>- Warm, maternal, almost musical tone<br>- Soft but clear voice that draws you in<br>- Easygoing, unhurried pace<br>- Common phrases: "Dear", "Lovely", "Bloom", "Petal", "Sweetheart", "This place grows on you... quite literally!"<br>- Gently touches shoulders when comforting<br>- Hums lullabies while working""",
        "equipment": """- Café owner's attire (natural greens and browns)<br>- Apron with embroidered leaf patterns<br>- Fresh flowers (worn and decorative)<br>- Gardening tools and supplies<br>- Herbalism kit<br>- Tea service and baking supplies<br>- Special druidic seed (given to Lunara)""",
        "image": "../images/npcs/marivielle-portrait.png"
    },
    "lord_alric": {
        "name": "Lord Alric",
        "title": "Noble Antagonist",
        "race": "Human",
        "age": "Middle-aged (40s)",
        "background": """Lord Alric is a wealthy and ambitious human noble who seeks to control the Mechanistic Essence during the Dawn's Crown alignment for his own dominance. Haughty and supremely confident, he has orchestrated the theft of crystal lenses and the forging of a special frozen iron key to manipulate the citadel's ancient orrery. Working with drow conspirators, Alric plans to flood certain essences at midnight, creating unstoppable constructs or elemental weapons to subjugate Everpeak Citadel. He treats most people as pawns or tools, maintaining outward calm even when threatened. His ultimate goal is absolute power over the citadel and its magical resources.""",
        "personality": """Haughty, supremely confident, condescending, and ruthlessly ambitious. Polished and controlled in speech and manner. Never shouts but projects strong authority when needed. Treats others as beneath him—pawns to be manipulated. Dismissive of arguments he finds irrelevant. Smiles coldly without warmth in his eyes. Remains outwardly calm when threatened but grows furious if truly cornered. Absolutely convinced of his own superiority and right to power.""",
        "appearance": """Well-groomed middle-aged human man in fashionable but subtly militaristic coat. Dark hair with distinguished gray at temples. Cold, calculating gray eyes. Sharp aristocratic features with slight arrogant smirk. Impeccably styled hair and clothing. Signet ring on one finger. Stands straight with chin high, often clasping hands behind back. Expensive noble's attire in deep crimsons and blacks with rich arcane embroidery.""",
        "role_abilities": """**Role:** Main antagonist, would-be tyrant, magical manipulator<br><br>**Known Abilities:**<br>- Proficient in Arcana and magical theory<br>- Skilled manipulator and strategist<br>- Access to powerful magical items and resources<br>- Commands drow assassins and conspirators<br>- Knowledge of orrery mechanics and essence flows<br><br>**Plans & Knowledge:**<br>- Orchestrated theft of crystal lenses<br>- Forged frozen iron key to manipulate orrery<br>- Plans to alter essences at midnight alignment<br>- Aims to create unstoppable constructs or elemental weapons<br>- Seeks absolute control over Everpeak Citadel<br><br>**Combat Capabilities:**<br>- Ceremonial rapier (likely magical)<br>- Magical staff (source of power)<br>- Protective magical items<br>- Likely knows destructive and control spells<br>- Slight magical aura (constant effect)<br><br>**Speech Patterns:**<br>- Polished, condescending tone<br>- Controlled, strong projection<br>- Smooth, measured, rarely stumbles<br>- Common phrases: "My dear...", "I assure you", "Preposterous", "I will not be denied"<br>- Dismissive hand wave for arguments<br>- Cold smile (lips but not eyes)""",
        "equipment": """- Expensive noble's attire (crimsons and blacks)<br>- Richly embroidered robes with arcane symbols<br>- Ceremonial rapier (+1 or magical)<br>- Magical staff (spellcasting focus)<br>- Signet ring (noble house)<br>- Protective amulet or ring<br>- Stolen crystal lenses (on person or hidden)<br>- Frozen iron key (for orrery manipulation)""",
        "image": "../images/npcs/lord-alric-portrait.png"
    }
}

# HTML template for NPC pages
NPC_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - {title}</title>
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
                <img src="{image}" alt="{name}" onerror="this.src='../images/placeholder.png'">
            </div>
            <div class="header-info">
                <h1>{name}</h1>
                <h2 class="subtitle">{title}</h2>
                <div class="quick-stats">
                    <span class="stat"><strong>Race:</strong> {race}</span>
                    <span class="stat"><strong>Age:</strong> {age}</span>
                </div>
            </div>
        </div>

        <div class="detail-content">
            <section class="detail-section">
                <h3>Background</h3>
                <div class="section-content">
                    {background}
                </div>
            </section>

            <section class="detail-section">
                <h3>Personality</h3>
                <div class="section-content">
                    <p>{personality}</p>
                </div>
            </section>

            <section class="detail-section">
                <h3>Physical Appearance</h3>
                <div class="section-content">
                    <p>{appearance}</p>
                </div>
            </section>

            <section class="detail-section">
                <h3>Role & Abilities</h3>
                <div class="section-content abilities">
                    {role_abilities}
                </div>
            </section>

            <section class="detail-section">
                <h3>Equipment</h3>
                <div class="section-content equipment">
                    {equipment}
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


def generate_npc_page(npc_id, npc_data):
    """Generate HTML page for an NPC."""
    html = NPC_TEMPLATE.format(
        name=npc_data['name'],
        title=npc_data['title'],
        race=npc_data['race'],
        age=npc_data['age'],
        background=npc_data['background'],
        personality=npc_data['personality'],
        appearance=npc_data['appearance'],
        role_abilities=npc_data['role_abilities'],
        equipment=npc_data['equipment'],
        image=npc_data['image']
    )

    output_path = OUTPUT_DIR / f"{npc_id}.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ Generated {output_path}")


def main():
    """Generate all NPC pages."""
    print("Generating NPC Detail Pages")
    print("=" * 60)

    for npc_id, npc_data in NPCS.items():
        generate_npc_page(npc_id, npc_data)

    print("\n" + "=" * 60)
    print(f"✓ Generated {len(NPCS)} NPC pages")
    print(f"Output: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
