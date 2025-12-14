#!/usr/bin/env python3
"""
Generate detailed HTML pages for locations with descriptions and scene images.
"""

import json
from pathlib import Path

# Input and output paths
LOCATIONS_JSON = Path("locations.json")
OUTPUT_DIR = Path("docs/locations")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load locations data
with open(LOCATIONS_JSON, 'r') as f:
    LOCATIONS = json.load(f)

# Additional context for each location
LOCATION_CONTEXT = {
    "Everpeak Citadel Exterior": {
        "significance": "The magnificent fortress that serves as the primary setting for the adventure. Built by ancient high elves atop converging ley lines, it harnesses elemental essences that power the citadel's magic.",
        "features": ["Multiple crystalline towers", "Terrace gardens at impossible altitudes", "Grand courtyards and winding staircases", "Festival decorations throughout", "Visible ley line energy"],
        "mood": "Grand, ancient, festive"
    },
    "Festival Marketplace": {
        "significance": "The bustling heart of Everpeak's winter festival where diverse races gather to trade, celebrate, and share news. This is where many adventures begin and where the party first encounters key NPCs.",
        "features": ["Colorful vendor stalls", "Winter goods and crafts", "Diverse fantasy races", "Festival decorations", "Warm lantern lighting"],
        "mood": "Festive, busy, welcoming"
    },
    "Grand Courtyard": {
        "significance": "The ceremonial center of Everpeak Citadel where important gatherings and festivals take place. The Yule Tree ceremony occurs here during the Dawn's Crown alignment.",
        "features": ["White stone paving", "Elegant high elven architecture", "View of crystalline towers", "Space for large gatherings", "Winter decorations"],
        "mood": "Majestic, ceremonial, open"
    },
    "The Grand Library": {
        "significance": "A scholar's paradise containing ancient knowledge about Everpeak's history, the high elves' sacrifice, and the elemental essences. Marge, the head librarian, helps guide researchers seeking to understand the citadel's mysteries.",
        "features": ["Endless shelves of ancient tomes", "Floating magical lights", "Mezzanine levels", "Star-charts and arcane diagrams", "Reading desks and ladders"],
        "mood": "Quiet, scholarly, reverent"
    },
    "The Observatory": {
        "significance": "A small chamber accessed from the Grand Library where Celestial Essence studies occurred. Recently restored, it holds clues about the Dawn's Crown alignment and missing star-lenses.",
        "features": ["Glass ceiling showing sky", "Ancient magical telescope", "Celestial maps and charts", "Brass and crystal instruments", "Gentle starlight"],
        "mood": "Intimate, astronomical, restored"
    },
    "Courier Tunnels": {
        "significance": "The working infrastructure beneath Everpeak where couriers use chalk runes and displacement magic to navigate. Evidence of tampering suggests someone is interfering with the displacement network.",
        "features": ["Rough stone passages", "Chalk runes on every surface", "Glowing magical symbols", "Spatial distortions", "Evidence of tampering"],
        "mood": "Maze-like, utilitarian, mysterious"
    },
    "Balcony Garden Café": {
        "significance": "Marivielle's magical garden infused with Nature Essence, creating an impossible oasis of warmth and greenery high in the mountains. She provided Lunara with a special seed tied to the garden's magic.",
        "features": ["Lush flowering vines", "Exotic potted plants", "Rustic wooden furniture", "Stone balcony with views", "Magical warmth and sunlight"],
        "mood": "Peaceful, impossible, nurturing"
    },
    "Barth's Forge": {
        "significance": "The drow blacksmith's workshop where Mechanistic Essence is harnessed for metalworking. Strange frozen iron was recently stolen, suggesting someone is forging keys for the orrery.",
        "features": ["Large brick forge with coals", "Metal anvil and tools", "Sparks and red-hot metal", "Weapons on display", "Workshop atmosphere"],
        "mood": "Hot, industrious, skilled"
    },
    "Sled Race Course": {
        "significance": "A winter festival attraction that showcases Everpeak's dramatic mountain setting and the community's festive spirit.",
        "features": ["Starting line area", "Winding course down mountain", "Wooden sleds", "Decorative flags and banners", "Dramatic mountain vistas"],
        "mood": "Exciting, winter sports, festive"
    },
    "The Elven Sanctum": {
        "significance": "The hidden heart of Everpeak where the Orrery controls elemental essence flows. This is where the high elves made their final sacrifice and where the climactic confrontation with Lord Alric occurs.",
        "features": ["The Orrery (massive magical device)", "Five elemental lens alcoves", "Constellation-covered vaulted ceiling", "Ancient carved pillars", "Crackling elemental energy", "Battle scars from century ago"],
        "mood": "Ancient, powerful, sacred"
    },
    "Mountain Path": {
        "significance": "The approach to Everpeak Citadel, showing the citadel's dramatic mountain setting and the journey travelers must make to reach it.",
        "features": ["Steep winding trail", "Snow-covered rocks", "Pine trees", "View of citadel above", "Mountain vistas"],
        "mood": "Cold, dramatic, remote"
    }
}

# HTML template for location pages
LOCATION_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Everpeak Citadel Location</title>
    <link rel="stylesheet" href="../css/main.css">
    <link rel="stylesheet" href="../css/detail-page.css">
    <style>
        .location-image {{
            width: 100%;
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 20px 0;
            border: 2px solid var(--accent-color);
        }}
        .features-list {{
            list-style: none;
            padding: 0;
        }}
        .features-list li {{
            padding: 8px 0;
            padding-left: 24px;
            position: relative;
        }}
        .features-list li:before {{
            content: "▸";
            position: absolute;
            left: 0;
            color: var(--accent-color);
        }}
    </style>
</head>
<body>
    <header class="site-header">
        <div class="header-content">
            <h1 class="site-title">Everpeak Citadel</h1>
            <nav class="site-nav">
                <a href="../index.html" class="nav-link">Read</a>
                <a href="../characters.html" class="nav-link">Characters</a>
                <a href="../locations.html" class="nav-link active">Locations</a>
                <a href="../about.html" class="nav-link">About</a>
                <a href="../download.html" class="nav-link">Download</a>
            </nav>
        </div>
    </header>

    <main class="detail-container">
        <nav class="breadcrumb">
            <a href="../locations.html">← Back to Locations</a>
        </nav>

        <div class="detail-header" style="display: block;">
            <h1>{name}</h1>
            <h2 class="subtitle">{mood}</h2>
        </div>

        <img src="{image}" alt="{name}" class="location-image" onerror="this.src='../images/placeholder.png'">

        <div class="detail-content">
            <section class="detail-section">
                <h3>Description</h3>
                <div class="section-content">
                    <p>{description}</p>
                </div>
            </section>

            <section class="detail-section">
                <h3>Significance</h3>
                <div class="section-content">
                    <p>{significance}</p>
                </div>
            </section>

            <section class="detail-section">
                <h3>Key Features</h3>
                <div class="section-content">
                    <ul class="features-list">
                        {features_html}
                    </ul>
                </div>
            </section>
        </div>

        <div class="navigation-footer">
            <a href="../locations.html" class="btn-secondary">← All Locations</a>
            <a href="../index.html" class="btn-primary">Start Reading →</a>
        </div>
    </main>

    <footer class="site-footer">
        <p>&copy; 2024 Everpeak Citadel | AI-generated comic</p>
    </footer>
</body>
</html>
"""


def get_filename(location_name):
    """Convert location name to filename."""
    return location_name.lower().replace(' ', '_').replace("'", '')


def generate_location_page(location_name, location_data, context):
    """Generate HTML page for a location."""
    features_html = "\n".join([f"<li>{feature}</li>" for feature in context['features']])

    image_filename = get_filename(location_name)

    html = LOCATION_TEMPLATE.format(
        name=location_name,
        mood=context['mood'],
        description=location_data['full_description'],
        significance=context['significance'],
        features_html=features_html,
        image=f"../images/locations/{image_filename}.png"
    )

    output_filename = f"{image_filename}.html"
    output_path = OUTPUT_DIR / output_filename

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ Generated {output_path}")


def main():
    """Generate all location pages."""
    print("Generating Location Detail Pages")
    print("=" * 60)

    for location_name, location_data in LOCATIONS.items():
        if location_name in LOCATION_CONTEXT:
            context = LOCATION_CONTEXT[location_name]
            generate_location_page(location_name, location_data, context)
        else:
            print(f"⚠ Skipping {location_name} - no context data")

    print("\n" + "=" * 60)
    print(f"✓ Generated {len(LOCATION_CONTEXT)} location pages")
    print(f"Output: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
