#!/usr/bin/env python3
"""
Generate detailed HTML pages for monsters with D&D 5e stat blocks.
"""

from pathlib import Path

# Output directory
OUTPUT_DIR = Path("docs/monsters")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Monster data extracted from everpeak-complete-module.md
MONSTERS = {
    "verdant_mephit": {
        "name": "Verdant Mephit",
        "title": "Nature Essence Elemental",
        "type": "Small Elemental (Neutral)",
        "cr": "1/2 (100 XP)",
        "stats": {
            "AC": "12",
            "HP": "21 (6d6)",
            "Speed": "30 ft., fly 30 ft.",
            "STR": "8 (-1)",
            "DEX": "15 (+2)",
            "CON": "10 (+0)",
            "INT": "7 (-2)",
            "WIS": "12 (+1)",
            "CHA": "10 (+0)"
        },
        "features": """**Skills:** Perception +3, Stealth +4<br>
**Damage Immunities:** Poison<br>
**Condition Immunities:** Poisoned<br>
**Senses:** Darkvision 60 ft., passive Perception 13<br>
**Languages:** Sylvan, Terran (understands but can't speak)""",
        "description": """A small, fey-like imp woven from vines, leaves, and moss. Flowers bloom around its feet, but when angered, thorny vines lash out viciously. It appears mischievous yet protective of natural spaces. These mephits are manifestations of disturbed Nature Essence found in ancient elven structures, particularly in gardens and sanctuaries where natural magic has been corrupted or disrupted.""",
        "abilities": """**Verdant Body:** The mephit's form is composed of living plant matter; faint pollen drifts in its wake.<br><br>

**Thorn Strike (Ranged Attack):** <br>
*Ranged Weapon Attack:* +4 to hit, range 30/60 ft., one target<br>
*Hit:* 5 (1d6 + 2) piercing damage<br><br>

**Roots of Wrath (Action):**<br>
The mephit slams a clawed vine into the ground, forcing each creature in a 10-foot radius to make a Strength or Dexterity saving throw (DC 13). On a failure, a creature becomes Restrained by thick, writhing vines. A Restrained creature can use its action to repeat the save, freeing itself on a success. The vines remain for up to 1d4 rounds or until the mephit is destroyed. This area also becomes difficult terrain for all creatures except the Verdant Mephit.<br><br>

**Bloomstrike (Ranged Vine Lash):**<br>
*Ranged Weapon Attack:* +4 to hit, range 30 ft., one target<br>
*Hit:* 6 (1d6 + 2) slashing damage plus 3 (1d4) poison damage<br>
*Special:* If the target is Large or smaller, the mephit may pull the target 10 feet closer or push it 10 feet away (like a *thorn whip* effect).<br><br>

**Growth Spurt (Bonus Action; Recharge 5-6):**<br>
The mephit channels a surge of Nature Essence, regaining 1d6+2 hit points. The area around it briefly flourishes with blossoms; allied plant creatures within 10 feet either regain 1d4 hit points or have advantage on their next attack.""",
        "tactics": """**Playful Guardian:** Attacks only if it senses "unnatural" intrusion.<br><br>
**Tactical Approach:** Prefers to entangle foes with Roots of Wrath, then whip them from short range with Bloomstrike or yank them into hazards. Uses Growth Spurt to sustain itself in extended combat.<br><br>
**Environment:** Found in corrupted gardens, nature sanctuaries, or areas where Nature Essence has been disturbed.""",
        "image": "../images/monsters/verdant-mephit.png"
    },
    "gear_mephit": {
        "name": "Gear Mephit",
        "title": "Mechanistic Essence Elemental",
        "type": "Small Elemental (Neutral)",
        "cr": "1/2 (100 XP)",
        "stats": {
            "AC": "13 (metallic plates)",
            "HP": "22 (5d6+5)",
            "Speed": "20 ft., fly 30 ft. (clumsy)",
            "STR": "10 (+0)",
            "DEX": "14 (+2)",
            "CON": "12 (+1)",
            "INT": "7 (-2)",
            "WIS": "10 (+0)",
            "CHA": "8 (-1)"
        },
        "features": """**Damage Resistances:** Bludgeoning, Piercing, and Slashing from nonmagical attacks<br>
**Condition Immunities:** Poisoned<br>
**Senses:** Darkvision 60 ft., passive Perception 10<br>
**Languages:** Understands Terran and one planar language (cannot speak)""",
        "description": """A tiny, mechanical imp assembled from interlocking brass gears and metal plates. Steam hisses from its joints, and it moves with steady clockwork efficiency. These mephits manifest when Mechanistic Essence is disrupted, particularly in forges, workshops, or areas with complex machinery.""",
        "abilities": """**Clockwork Frame:** The mephit's mechanical body clanks and whirrs, occasionally emitting a soft ticking.<br><br>

**Serrated Blade (Melee Attack):**<br>
The mephit attacks with a spinning saw-like appendage of whirring gears.<br>
*Melee Weapon Attack:* +4 to hit, reach 5 ft., one target<br>
*Hit:* 6 (1d8 + 2) slashing damage<br><br>

**Gear Grenades (Action):**<br>
The mephit hurls a whirring orb to a point within 30 ft. After 1 round, the grenade explodes in a 10-foot radius, dealing 7 (2d6) piercing damage; creatures in the area can attempt a Dexterity save (DC 13) for half damage. On a failed save, a creature is also Slowed (speed reduced by 10 ft.) until the end of its next turn.<br><br>

**Clockwork Counter (Reaction; Recharge 4-6):**<br>
When hit by a melee attack, the mephit's chassis emits a teeth-rattling gear-grind. The attacker must make a Dexterity save (DC 13) or take 4 (1d6) thunder damage and be pushed 10 ft. away. This can also shatter fragile objects in the area or rattle allies.<br><br>

**Precision Overdrive (Bonus Action):**<br>
The mephit targets one creature (ally or enemy) within 30 ft. with a sudden burst of mechanical insight. If targeting an ally, that ally has advantage on its next attack or skill check before the end of its next turn. If targeting an enemy, the mephit attempts to cause an "overload": the enemy has disadvantage on its next attack roll.""",
        "tactics": """**Robotic & Efficient:** Methodical, focusing on disabling threats.<br><br>
**Tactical Approach:** Tosses gear grenades into clustered foes, then uses Clockwork Counter to deter melee attackers. Uses Precision Overdrive strategically to swing combat in its favor.<br><br>
**Environment:** Found in forges, workshops, mechanical puzzles, or areas with disrupted Mechanistic Essence.""",
        "image": "../images/monsters/gear-mephit.png"
    },
    "starlight_mephit": {
        "name": "Starlight Mephit",
        "title": "Celestial Essence Elemental",
        "type": "Small Elemental (Neutral)",
        "cr": "1/2 (100 XP)",
        "stats": {
            "AC": "11",
            "HP": "20 (5d6)",
            "Speed": "30 ft., fly 30 ft.",
            "STR": "8 (-1)",
            "DEX": "12 (+1)",
            "CON": "10 (+0)",
            "INT": "8 (-1)",
            "WIS": "11 (+0)",
            "CHA": "12 (+1)"
        },
        "features": """**Damage Resistances:** Radiant; Nonmagical attacks that are not silvered<br>
**Condition Immunities:** Blinded<br>
**Senses:** Darkvision 60 ft., passive Perception 10<br>
**Languages:** Auran, Celestial (understands but can't speak)""",
        "description": """A luminous, ethereal figure composed of swirling star-fields and cosmic dust. It glides silently, trailing motes of radiance behind it. Its eyes shimmer with otherworldly light. These mephits appear when Celestial Essence is disturbed, particularly in observatories or places aligned with celestial magic.""",
        "abilities": """**Luminous Form:** The mephit sheds dim light in a 10-foot radius, which it can brighten or dim as a bonus action.<br><br>

**Astral Ray (Ranged Attack):**<br>
The mephit fires a concentrated beam of starlight.<br>
*Ranged Weapon Attack:* +4 to hit, range 40/120 ft., one target<br>
*Hit:* 5 (1d6 + 2) radiant damage<br><br>

**Cosmic Radiance (Action):**<br>
The mephit channels celestial power in a 20-foot cone of sparkling starlight. Creatures in the area must succeed on a Constitution save (DC 13) or take 7 (2d6) radiant damage. A creature that fails also glows (shedding dim light in a 5-foot radius) for 1 minute, giving advantage on the next attack against it. On a success, half damage and no glow.<br><br>

**Stellar Veil (Bonus Action; Recharge 5-6):**<br>
The mephit creates a 10-foot-radius zone of twilight centered on itself. For 1 round, this area becomes lightly obscured to normal vision (disadvantage on Perception checks). Allies with darkvision or celestial-based senses see normally. The mephit often uses this to reposition or help an ally close in unseen.<br><br>

**Glimpse of Infinity (Reaction):**<br>
When an enemy within 15 ft. casts a spell or uses an ability that requires a saving throw, the mephit warps fate, imposing disadvantage on that save. Flavored as the mephit briefly bending cosmic threads to hinder success.""",
        "tactics": """**Otherworldly & Serene:** Communicates in soft, musical hums; unleashes radiant fury when threatened.<br><br>
**Tactical Approach:** Punishes clustered foes with Cosmic Radiance and uses Stellar Veil to protect itself or allies. Glimpse of Infinity can turn the tide of magical combat.<br><br>
**Environment:** Found in observatories, celestial chambers, or areas where Celestial Essence has been disrupted.""",
        "image": "../images/monsters/starlight-mephit.png"
    },
    "blink_mephit": {
        "name": "Blink Mephit",
        "title": "Displacement Essence Elemental",
        "type": "Small Elemental (Neutral)",
        "cr": "1/2 (100 XP)",
        "stats": {
            "AC": "13",
            "HP": "18 (4d6+4)",
            "Speed": "30 ft., fly 40 ft.",
            "STR": "6 (-2)",
            "DEX": "16 (+3)",
            "CON": "12 (+1)",
            "INT": "7 (-2)",
            "WIS": "10 (+0)",
            "CHA": "8 (-1)"
        },
        "features": """**Damage Resistances:** Bludgeoning, Piercing, and Slashing from nonmagical attacks<br>
**Condition Immunities:** Poisoned, Grappled<br>
**Senses:** Darkvision 60 ft., passive Perception 10<br>
**Languages:** Auran, Primordial (understands but can't speak)""",
        "description": """A nearly invisible creature whose edges flicker like a mirage. Each flap of its wings leaves a shimmering afterimage, and its footsteps echo from unexpected directions. These mephits emerge from disrupted Displacement Essence, haunting courier tunnels and teleportation passages.""",
        "abilities": """**Blink Shift (1/Turn):** As a bonus action, the mephit can teleport up to 10 ft. to an unoccupied space it can see, without provoking opportunity attacks.<br><br>

**Spatial Shard (Ranged Attack):**<br>
The mephit hurls a crystalline fragment of warped space that seems to bend light around it.<br>
*Ranged Weapon Attack:* +5 to hit, range 30/60 ft., one target<br>
*Hit:* 5 (1d6 + 2) force damage<br>
*Special:* The target must succeed on a DC 13 Constitution saving throw or their vision becomes briefly distorted until the end of their next turn, imposing disadvantage on their next attack roll.<br><br>

**Spatial Flicker (Action):**<br>
The mephit chooses up to two creatures within 20 ft. Each target must succeed on a Wisdom save (DC 13) or become Disoriented, granting advantage on attack rolls against them until the end of their next turn. Visually, it warps their sense of space, making the environment seem twisted.<br><br>

**Reality Tear (Bonus Action; Recharge 4-6):**<br>
The mephit opens a brief rift in space within 30 ft. One ally (including itself) can step through the rift as part of the same bonus action, emerging in another unoccupied space within 10 ft. of the rift. Offensively, it can place an ally behind the party's backline. Defensively, it can aid escape.<br><br>

**Phantom Echo (Reaction):**<br>
When a creature moves adjacent to the mephit or provokes an opportunity attack, the mephit may teleport up to 15 ft. away, leaving behind an illusory double for 1 round. The double disappears if attacked (AC 10), potentially wasting an enemy's attack.""",
        "tactics": """**Trickster & Elusive:** Loves to isolate or confuse a single target, darting around the battlefield.<br><br>
**Tactical Approach:** Teleports itself or allies into advantageous positions, sowing chaos with illusions and warps. Uses Spatial Flicker to disorient multiple foes, then Reality Tear to reposition.<br><br>
**Environment:** Found in courier tunnels, teleportation chambers, or areas with disrupted Displacement Essence.""",
        "image": "../images/monsters/blink-mephit.png"
    },
    "melody_mephit": {
        "name": "Melody Mephit",
        "title": "Harmony Essence Elemental",
        "type": "Small Elemental (Neutral)",
        "cr": "1/2 (100 XP)",
        "stats": {
            "AC": "11",
            "HP": "19 (5d6-5)",
            "Speed": "30 ft., fly 30 ft.",
            "STR": "8 (-1)",
            "DEX": "12 (+1)",
            "CON": "8 (-1)",
            "INT": "10 (+0)",
            "WIS": "10 (+0)",
            "CHA": "14 (+2)"
        },
        "features": """**Damage Resistances:** Thunder; Bludgeoning, Piercing, and Slashing from nonmagical attacks<br>
**Condition Immunities:** Deafened<br>
**Senses:** Darkvision 60 ft., passive Perception 10<br>
**Languages:** Auran, Aquan (understands but can't speak)""",
        "description": """A pastel swirl of colored sound waves. Its form hums with gentle chords, drifting like a dancer. Every movement leaves sparkling motes and faint echoes behind. These mephits manifest when Harmony Essence is disrupted, appearing in concert halls and places of musical magic.""",
        "abilities": """**Harmonic Aura:** Creatures within 10 ft. of the mephit have disadvantage on Charisma (Deception) checks due to the mephit's resonating hum.<br><br>

**Sonic Strike (Ranged Attack):**<br>
The mephit releases a focused burst of discordant sound.<br>
*Ranged Weapon Attack:* +4 to hit, range 30/60 ft., one target<br>
*Hit:* 5 (1d6 + 2) thunder damage<br><br>

**Resonant Pulse (Action):**<br>
The mephit emits a 15-foot sphere of harmonic energy (centered on itself). Each creature in the area makes a Charisma save (DC 13) or takes 5 (2d4) thunder damage and must drop any held item or lose concentration on a spell. On a success, half damage and no extra effect.<br><br>

**Discordant Duet (Bonus Action; Recharge 5-6):**<br>
The mephit conjures a harmonic echo that sings out of key. Enemies within 10 ft. have disadvantage on Perception checks and spell attack rolls for 1 round. Allies can use verbal communication (e.g., the Help action) from 10 ft. further away, as the mephit's supportive resonance amplifies calls.<br><br>

**Harmony Chain (Reaction):**<br>
If there is another Melody Mephit or an allied "musical" entity nearby, they can chain their energies. When an ally hits a creature with an attack, the mephit spends its reaction to cause psychic feedback, dealing an extra 3 (1d6) thunder or psychic damage.""",
        "tactics": """**Eerie & Mesmerizing:** Attempts to subdue enemies with dissonant chords rather than raw violence.<br><br>
**Tactical Approach:** Uses Resonant Pulse to break concentration and force weapon drops, then follows up with Sonic Strike. Discordant Duet disrupts enemy coordination while aiding allies.<br><br>
**Environment:** Found in concert halls, music chambers, or areas where Harmony Essence has been corrupted.""",
        "image": "../images/monsters/melody-mephit.png"
    }
}

# HTML template for monster pages
MONSTER_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - {title}</title>
    <link rel="stylesheet" href="../css/main.css">
    <link rel="stylesheet" href="../css/detail-page.css">
    <style>
        .stat-block {{
            background: var(--bg-secondary);
            border: 2px solid var(--accent-color);
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }}
        .stat-row {{
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 10px;
            margin: 15px 0;
        }}
        .stat-item {{
            text-align: center;
            padding: 10px;
            background: var(--bg-primary);
            border-radius: 4px;
        }}
        .stat-item strong {{
            display: block;
            color: var(--accent-color);
            margin-bottom: 5px;
        }}
    </style>
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
                    <span class="stat"><strong>Type:</strong> {type_str}</span>
                    <span class="stat"><strong>CR:</strong> {cr}</span>
                </div>
            </div>
        </div>

        <div class="detail-content">
            <section class="detail-section">
                <h3>Description</h3>
                <div class="section-content">
                    {description}
                </div>
            </section>

            <section class="detail-section">
                <h3>Stat Block</h3>
                <div class="stat-block">
                    <p><strong>Armor Class:</strong> {ac}<br>
                    <strong>Hit Points:</strong> {hp}<br>
                    <strong>Speed:</strong> {speed}</p>

                    <div class="stat-row">
                        <div class="stat-item"><strong>STR</strong><span>{str}</span></div>
                        <div class="stat-item"><strong>DEX</strong><span>{dex}</span></div>
                        <div class="stat-item"><strong>CON</strong><span>{con}</span></div>
                        <div class="stat-item"><strong>INT</strong><span>{int}</span></div>
                        <div class="stat-item"><strong>WIS</strong><span>{wis}</span></div>
                        <div class="stat-item"><strong>CHA</strong><span>{cha}</span></div>
                    </div>

                    <div style="margin-top: 15px;">
                        {features}
                    </div>
                </div>
            </section>

            <section class="detail-section">
                <h3>Abilities & Actions</h3>
                <div class="section-content abilities">
                    {abilities}
                </div>
            </section>

            <section class="detail-section">
                <h3>Combat Tactics</h3>
                <div class="section-content">
                    {tactics}
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


def generate_monster_page(monster_id, monster_data):
    """Generate HTML page for a monster."""
    html = MONSTER_TEMPLATE.format(
        name=monster_data['name'],
        title=monster_data['title'],
        type_str=monster_data['type'],
        cr=monster_data['cr'],
        ac=monster_data['stats']['AC'],
        hp=monster_data['stats']['HP'],
        speed=monster_data['stats']['Speed'],
        str=monster_data['stats']['STR'],
        dex=monster_data['stats']['DEX'],
        con=monster_data['stats']['CON'],
        int=monster_data['stats']['INT'],
        wis=monster_data['stats']['WIS'],
        cha=monster_data['stats']['CHA'],
        features=monster_data['features'],
        description=monster_data['description'],
        abilities=monster_data['abilities'],
        tactics=monster_data['tactics'],
        image=monster_data['image']
    )

    output_path = OUTPUT_DIR / f"{monster_id}.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ Generated {output_path}")


def main():
    """Generate all monster pages."""
    print("Generating Monster Stat Pages")
    print("=" * 60)

    for monster_id, monster_data in MONSTERS.items():
        generate_monster_page(monster_id, monster_data)

    print("\n" + "=" * 60)
    print(f"✓ Generated {len(MONSTERS)} monster pages")
    print(f"Output: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
